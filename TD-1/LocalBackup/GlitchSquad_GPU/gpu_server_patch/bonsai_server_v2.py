"""
Bonsai Server v2 — Drop-in replacement for bonsai_server.py on the GPU laptop.

NEW: Supports img2img via init_image parameter for character consistency.

Usage (on the GPU laptop):
    cd Bonsai-Image-Demo
    .\.venv\Scripts\activate
    python bonsai_server_v2.py

API endpoints:
    GET  /health                          → {"status":"ok","gpu":true}
    POST /generate                        → PNG image (txt2img, original)
    POST /generate_img2img                → PNG image (img2img, new)
    POST /generate_unified                → PNG image (auto txt2img or img2img based on params)

For img2img, send JSON with:
    {
        "prompt": "...",
        "init_image": "<base64 encoded PNG>",
        "image_strength": 0.4,
        "width": 1024,
        "height": 1024,
        "steps": 4,
        "seed": 42
    }
"""
import argparse
import base64
import io
import os
import secrets
import sys
import time
from pathlib import Path

DEMO_DIR = Path(r"D:\Papaji\Bonsai-Image-Demo")
MODELS_DIR = DEMO_DIR / "models"

PATCH_DIR = Path(__file__).resolve().parent


def find_subdir(root: Path, *hints: str) -> Path:
    matches = [
        p for p in root.iterdir()
        if p.is_dir() and any(h in p.name for h in hints)
    ]
    if not matches:
        present = ", ".join(sorted(p.name for p in root.iterdir() if p.is_dir())) or "(empty)"
        raise FileNotFoundError(f"No subdir matching {hints!r} under {root}. Present: {present}")
    matches.sort(key=lambda p: len(p.name), reverse=True)
    return matches[0]


def build_app(model_root: Path, backend_id: str = "bonsai-ternary-gemlite"):
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import StreamingResponse

    from backend_gpu.pipeline_gpu import GpuPipeline
    from gemlite.core import GemLiteLinearTriton

    triton_cache = DEMO_DIR / "outputs" / ".triton_cache"
    gemlite_cache = DEMO_DIR / "outputs" / ".gemlite_cache" / "autotune.json"
    triton_cache.mkdir(parents=True, exist_ok=True)
    gemlite_cache.parent.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("TRITON_CACHE_DIR", str(triton_cache))

    text_encoder_dir = find_subdir(model_root, "text_encoder")
    transformer_dir = find_subdir(model_root, "transformer")
    vae_dir = find_subdir(model_root, "vae")

    transformer_kwarg = {
        "bonsai-ternary-gemlite": "ternary_transformer_path",
        "bonsai-binary-gemlite": "binary_transformer_path",
    }[backend_id]

    print(f"Loading pipeline from {model_root} ...")
    t0 = time.perf_counter()

    pipeline = GpuPipeline(
        backend=backend_id,
        **{transformer_kwarg: str(transformer_dir)},
        text_encoder_path=str(text_encoder_dir),
        vae_path=str(vae_dir),
        tokenizer_path=str(text_encoder_dir / "tokenizer"),
    )

    if gemlite_cache.exists():
        GemLiteLinearTriton.load_config(str(gemlite_cache), print_error=False)

    pipeline.prewarm()
    print(f"Pipeline ready in {time.perf_counter() - t0:.1f}s")

    # Import patched diffusion_klein (at vendor/image-studio/backend_gpu/)
    # with img2img support. Backward-compatible: txt2img works when init_image is None.
    from backend_gpu.diffusion_klein import diffusion_forward as diffusion_klein_patched

    from PIL import Image

    app = FastAPI(title="Bonsai Image Server v2 (img2img)")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    @app.get("/health")
    def health():
        return {"status": "ok", "gpu": True, "version": "2.0-img2img"}

    @app.post("/generate")
    async def generate(request: Request):
        body = await request.json()
        prompt = body["prompt"]
        width = body.get("width", 1024)
        height = body.get("height", 1024)
        steps = body.get("steps", 4)
        seed_val = body.get("seed") or secrets.randbits(31)
        max_seq = body.get("max_sequence_length", 1024)
        print(f"[generate] {width}x{height} seed={seed_val} seq={max_seq} prompt={prompt[:80]}...")
        t1 = time.perf_counter()

        try:
            png_bytes = pipeline.generate_png(
                prompt=prompt, seed=seed_val, steps=steps,
                height=height, width=width,
            )
            elapsed = time.perf_counter() - t1
            peak_mb = pipeline.last_peak_memory_mb or 0.0
            print(f"[generate] done in {elapsed:.1f}s  peak VRAM {peak_mb:.0f} MB")
            GemLiteLinearTriton.cache_config(str(gemlite_cache))
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                import torch
                torch.cuda.empty_cache()
                from fastapi import HTTPException
                raise HTTPException(status_code=507, detail=f"CUDA OOM at {width}x{height}")
            from fastapi import HTTPException
            import traceback
            tb = traceback.format_exc()
            print(f"  ERROR in generate: {e}\n{tb}")
            raise HTTPException(status_code=500, detail=f"generate error: {e}\n{tb}")

        return StreamingResponse(io.BytesIO(png_bytes), media_type="image/png")

    @app.post("/generate_img2img")
    async def generate_img2img(request: Request):
        import traceback
        try:
            body = await request.json()
            prompt = body["prompt"]
            width = body.get("width", 1024)
            height = body.get("height", 1024)
            steps = body.get("steps", 4)
            seed_val = body.get("seed") or secrets.randbits(31)
            image_strength = body.get("image_strength", 0.4)
            init_image_b64 = body.get("init_image", None)
            if not init_image_b64:
                from fastapi import HTTPException
                raise HTTPException(status_code=400, detail="init_image required")
            init_image = Image.open(io.BytesIO(base64.b64decode(init_image_b64))).convert("RGB")
            print(f"[img2img] {width}x{height} seed={seed_val} strength={image_strength}")
            t1 = time.perf_counter()
            result_image = diffusion_klein_patched(
                transformer=pipeline._transformer, text_encoder=pipeline._text_encoder,
                tokenizer=pipeline._tokenizer, vae=pipeline._vae,
                prompt=prompt, height=height, width=width,
                num_steps=steps, seed=seed_val, guidance=1.0,
                scheduler=pipeline._scheduler,
                init_image=init_image, image_strength=image_strength,
            )
            buf = io.BytesIO()
            result_image.save(buf, format="PNG")
            png_bytes = buf.getvalue()
            elapsed = time.perf_counter() - t1
            if torch.cuda.is_available():
                peak_mb = torch.cuda.max_memory_allocated() / (1024**2)
                print(f"[img2img] done in {elapsed:.1f}s  peak VRAM {peak_mb:.0f} MB")
            else:
                print(f"[img2img] done in {elapsed:.1f}s")
            GemLiteLinearTriton.cache_config(str(gemlite_cache))
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                import torch
                torch.cuda.empty_cache()
                from fastapi import HTTPException
                raise HTTPException(status_code=507, detail=f"CUDA OOM at {width}x{height}")
            tb = traceback.format_exc()
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail=f"img2img error: {e}\n{tb}")
        except Exception as e:
            tb = traceback.format_exc()
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail=f"img2img unexpected: {e}\n{tb}")
        return StreamingResponse(io.BytesIO(png_bytes), media_type="image/png")

    @app.post("/generate_unified")
    async def generate_unified(request: Request):
        import traceback
        try:
            body = await request.json()
            prompt = body["prompt"]
            width = body.get("width", 1024)
            height = body.get("height", 1024)
            steps = body.get("steps", 4)
            seed_val = body.get("seed") or secrets.randbits(31)
            image_strength = body.get("image_strength", 0.4)
            init_image_b64 = body.get("init_image", None)
            max_seq = body.get("max_sequence_length", 1024)

            if init_image_b64:
                init_image = Image.open(io.BytesIO(base64.b64decode(init_image_b64))).convert("RGB")
                print(f"[unified/img2img] {width}x{height} seed={seed_val} str={image_strength} seq={max_seq}")
            else:
                init_image = None
                print(f"[unified/txt2img] {width}x{height} seed={seed_val}")

            print(f"  prompt={prompt[:80]}...")
            t1 = time.perf_counter()

            import torch

            if init_image is not None:
                result_image = diffusion_klein_patched(
                    transformer=pipeline._transformer,
                    text_encoder=pipeline._text_encoder,
                    tokenizer=pipeline._tokenizer,
                    vae=pipeline._vae,
                    prompt=prompt,
                    height=height,
                    width=width,
                    num_steps=steps,
                    seed=seed_val,
                    guidance=1.0,
                    scheduler=pipeline._scheduler,
                    init_image=init_image,
                    image_strength=image_strength,
                    max_sequence_length=max_seq,
                )
                buf = io.BytesIO()
                result_image.save(buf, format="PNG")
                png_bytes = buf.getvalue()
            else:
                png_bytes = pipeline.generate_png(
                    prompt=prompt, seed=seed_val, steps=steps,
                    height=height, width=width,
                )

            elapsed = time.perf_counter() - t1
            peak_mb = 0.0
            if torch.cuda.is_available():
                peak_mb = torch.cuda.max_memory_allocated() / (1024**2)
            print(f"  done in {elapsed:.1f}s  peak VRAM {peak_mb:.0f} MB")
            GemLiteLinearTriton.cache_config(str(gemlite_cache))
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                import torch
                torch.cuda.empty_cache()
                from fastapi import HTTPException
                raise HTTPException(status_code=507, detail=f"CUDA OOM at {width}x{height}")
            tb = traceback.format_exc()
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail=f"unified error: {e}\n{tb}")
        except Exception as e:
            tb = traceback.format_exc()
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail=f"unified unexpected: {e}\n{tb}")

        return StreamingResponse(io.BytesIO(png_bytes), media_type="image/png")

    return app, pipeline


def main():
    parser = argparse.ArgumentParser(description="Bonsai Image Server v2 (img2img)")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--model-dir", type=Path, default=None)
    parser.add_argument("--model", choices=["ternary-gemlite", "binary-gemlite"], default="ternary-gemlite")
    args = parser.parse_args()

    model_subdirs = {
        "ternary-gemlite": "bonsai-image-4B-ternary-gemlite",
        "binary-gemlite": "bonsai-image-4B-binary-gemlite",
    }
    model_root = args.model_dir or (MODELS_DIR / model_subdirs[args.model])
    backend_id = f"bonsai-{args.model.split('-')[0]}-gemlite"

    if not model_root.exists():
        print(f"ERROR: Model not found at {model_root}")
        sys.exit(1)

    import torch
    if not torch.cuda.is_available():
        print("ERROR: CUDA not available")
        sys.exit(1)

    gpu_name = torch.cuda.get_device_name(0)
    vram_mb = torch.cuda.get_device_properties(0).total_memory / (1024 * 1024)
    print(f"GPU: {gpu_name}  VRAM: {vram_mb:.0f} MB")

    app, _pipeline = build_app(model_root, backend_id)

    import uvicorn
    print(f"\nServer v2 (img2img) starting on http://{args.host}:{args.port}")
    print("Endpoints: /health, /generate (txt2img), /generate_img2img, /generate_unified")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()

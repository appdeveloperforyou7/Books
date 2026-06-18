"""
Bonsai Image Server — Run on the OTHER laptop (the one with GPU).

Exposes the Bonsai pipeline over HTTP so any machine on the same network
can generate images by POSTing a JSON prompt.

Usage (on the GPU laptop):
    cd Bonsai-Image-Demo
    .\.venv\Scripts\activate
    pip install fastapi uvicorn
    python bonsai_server.py

    # Or with custom port / model dir:
    python bonsai_server.py --port 8765 --model-dir D:\Bonsai-Image-Demo\models\bonsai-image-4B-ternary-gemlite
"""
import argparse
import io
import os
import secrets
import sys
import time
from pathlib import Path

DEMO_DIR = Path(r"D:\Papaji\Bonsai-Image-Demo")
MODELS_DIR = DEMO_DIR / "models"


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

    app = FastAPI(title="Bonsai Image Server")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    @app.get("/health")
    def health():
        return {"status": "ok", "gpu": True}

    @app.post("/generate")
    async def generate(request: Request):
        body = await request.json()
        prompt = body["prompt"]
        width = body.get("width", 1024)
        height = body.get("height", 1024)
        steps = body.get("steps", 4)
        seed_val = body.get("seed") or secrets.randbits(31)
        print(f"[generate] {width}x{height} seed={seed_val} prompt={prompt[:80]}...")
        t1 = time.perf_counter()

        try:
            png_bytes = pipeline.generate_png(
                prompt=prompt,
                seed=seed_val,
                steps=steps,
                height=height,
                width=width,
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
            raise

        return StreamingResponse(io.BytesIO(png_bytes), media_type="image/png")

    return app, pipeline


def main():
    parser = argparse.ArgumentParser(description="Bonsai Image Server")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address (default 0.0.0.0 = all interfaces)")
    parser.add_argument("--port", type=int, default=8765, help="Port (default 8765)")
    parser.add_argument("--model-dir", type=Path, default=None, help="Override model directory")
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
        print("Run: cd Bonsai-Image-Demo && .\\scripts\\download_model.ps1 ternary")
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
    print(f"\nServer starting on http://{args.host}:{args.port}")
    print("Other machines can call: POST http://<THIS-LAPTOP-IP>:8765/generate")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()

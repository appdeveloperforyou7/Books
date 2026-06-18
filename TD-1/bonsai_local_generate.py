"""
Bonsai Image — Local inference on Windows with NVIDIA GPU.
Uses the official Bonsai-Image-Demo backend_gpu pipeline.

Supports aggressive CPU offloading for GPUs with limited VRAM (4-6 GB).
Text encoder runs on CPU and is never moved to GPU, saving ~2.84 GB VRAM.

Prerequisites:
  1. Run the official setup:  cd Bonsai-Image-Demo && .\setup.ps1
  2. Download the model:     .\scripts\download_model.ps1 ternary
  3. Activate the venv:      .\.venv\Scripts\activate

Usage:
  python bonsai_local_generate.py "a tiny bonsai tree in morning light"
  python bonsai_local_generate.py "cyberpunk city" --size 512x512 --seed 42
  python bonsai_local_generate.py "forest scene" --steps 4 --output my_image.png
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import secrets
from pathlib import Path

# ── Resolve paths relative to Bonsai-Image-Demo ──────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
DEMO_DIR = Path(r"D:\PrismBonsai\Bonsai-Image-Demo")
MODELS_DIR = DEMO_DIR / "models"
VENV_PY = DEMO_DIR / ".venv" / "Scripts" / "python.exe"

# Check setup has been run
if not DEMO_DIR.exists():
    print("ERROR: Bonsai-Image-Demo not found.")
    print("  Run: git clone https://github.com/PrismML-Eng/Bonsai-Image-Demo.git")
    print("  Then: cd Bonsai-Image-Demo && .\\setup.ps1")
    sys.exit(1)


def parse_size(s: str) -> tuple[int, int]:
    s = s.lower().replace("×", "x")
    try:
        w_str, h_str = s.split("x", 1)
        w, h = int(w_str), int(h_str)
    except ValueError:
        raise argparse.ArgumentTypeError(f"--size must be 'WxH' (e.g. 512x512), got {s!r}")
    for dim, name in ((w, "width"), (h, "height")):
        if not 256 <= dim <= 2048:
            raise argparse.ArgumentTypeError(f"--size {name} {dim} out of range — must be 256-2048")
        if dim % 16:
            raise argparse.ArgumentTypeError(f"--size {name} {dim} must be a multiple of 16")
    return w, h


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Bonsai Image local generation (Windows/CUDA)",
        epilog=(
            "Recommended sizes for low-VRAM GPUs:\n"
            "  512x512  — safe for 4-6 GB VRAM\n"
            "  624x416  — landscape, low-VRAM friendly\n"
            "  416x624  — portrait, low-VRAM friendly\n"
            "  1024x1024 — needs 6+ GB VRAM\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("prompt", help="Text prompt for image generation")
    p.add_argument("--size", type=parse_size, default=(512, 512),
                   help="Image size as WxH (default: 512x512)")
    p.add_argument("--steps", type=int, default=4,
                   help="Denoising steps (4 is optimal)")
    p.add_argument("--seed", type=int, default=None,
                   help="Random seed (random if not set)")
    p.add_argument("--output", type=Path, default=None,
                   help="Output PNG path (default: bonsai_output_LOCAL.png)")
    p.add_argument("--model", choices=["ternary-gemlite", "binary-gemlite"],
                   default="ternary-gemlite", help="Model variant")
    p.add_argument("--model-dir", type=Path, default=None,
                   help="Override model directory path")
    return p.parse_args()


def find_subdir(root: Path, *hints: str) -> Path:
    """Find a subdir of root matching any of the hints by substring."""
    matches = [
        p for p in root.iterdir()
        if p.is_dir() and any(h in p.name for h in hints)
    ]
    if not matches:
        present = ", ".join(sorted(p.name for p in root.iterdir() if p.is_dir())) or "(empty)"
        raise FileNotFoundError(f"No subdir matching {hints!r} under {root}. Present: {present}")
    matches.sort(key=lambda p: len(p.name), reverse=True)
    return matches[0]


def main() -> None:
    args = parse_args()
    seed = args.seed if args.seed is not None else secrets.randbits(31)
    width, height = args.size

    output_path = args.output or (SCRIPT_DIR / "bonsai_output_LOCAL.png")

    print(f"\n{'='*60}")
    print(f"  Bonsai Image — Local Generation (CUDA)")
    print(f"{'='*60}")
    print(f"  Prompt : {args.prompt}")
    print(f"  Size   : {width}x{height}")
    print(f"  Steps  : {args.steps}")
    print(f"  Seed   : {seed}")
    print(f"  Model  : {args.model}")
    print(f"  Output : {output_path}")
    print(f"{'='*60}\n")

    # ── Check VRAM ──────────────────────────────────────────────────────
    import torch
    if not torch.cuda.is_available():
        print("ERROR: CUDA not available. Check torch + NVIDIA driver.")
        sys.exit(1)

    gpu_name = torch.cuda.get_device_name(0)
    vram_mb = torch.cuda.get_device_properties(0).total_memory / (1024 * 1024)
    print(f"  GPU  : {gpu_name}")
    print(f"  VRAM : {vram_mb:.0f} MB")

    if vram_mb < 6000:
        print(f"\n  ⚠️  Low VRAM detected ({vram_mb:.0f} MB). Using CPU offloading.")
        print(f"     Text encoder stays on CPU, only transformer + VAE on GPU.")
        if width > 512 or height > 512:
            print(f"\n  ⚠️  WARNING: {width}x{height} may OOM on {vram_mb:.0f} MB VRAM.")
            print(f"     Consider using --size 512x512 for safety.")

    # ── Resolve model directory ─────────────────────────────────────────
    model_subdirs = {
        "ternary-gemlite": "bonsai-image-4B-ternary-gemlite",
        "binary-gemlite": "bonsai-image-4B-binary-gemlite",
    }
    
    if args.model_dir:
        model_root = args.model_dir
    else:
        model_root = MODELS_DIR / model_subdirs[args.model]
    
    if not model_root.exists():
        print(f"\nERROR: Model not found at: {model_root}")
        print(f"  Run: cd Bonsai-Image-Demo && .\\scripts\\download_model.ps1 ternary")
        sys.exit(1)

    print(f"  Model : {model_root}\n")

    # ── Setup Triton/Gemlite caches ────────────────────────────────────
    triton_cache = DEMO_DIR / "outputs" / ".triton_cache"
    gemlite_cache = DEMO_DIR / "outputs" / ".gemlite_cache" / "autotune.json"
    triton_cache.mkdir(parents=True, exist_ok=True)
    gemlite_cache.parent.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("TRITON_CACHE_DIR", str(triton_cache))
    os.environ.setdefault("MFLUX_STUDIO_GPU_TOKEN", "local-inference")

    # ── Load pipeline ───────────────────────────────────────────────────
    print("  [1/3] Loading pipeline (imports + model weights)...")
    t0 = time.perf_counter()

    from backend_gpu.pipeline_gpu import GpuPipeline
    from gemlite.core import GemLiteLinearTriton

    backend_id = f"bonsai-{args.model.split('-')[0]}-gemlite"
    text_encoder_dir = find_subdir(model_root, "text_encoder")
    transformer_dir = find_subdir(model_root, "transformer")
    vae_dir = find_subdir(model_root, "vae")

    transformer_kwarg = {
        "bonsai-ternary-gemlite": "ternary_transformer_path",
        "bonsai-binary-gemlite": "binary_transformer_path",
    }[backend_id]

    pipeline = GpuPipeline(
        backend=backend_id,
        **{transformer_kwarg: str(transformer_dir)},
        text_encoder_path=str(text_encoder_dir),
        vae_path=str(vae_dir),
        tokenizer_path=str(text_encoder_dir / "tokenizer"),
    )

    # Load persisted gemlite autotune cache
    if gemlite_cache.exists():
        GemLiteLinearTriton.load_config(str(gemlite_cache), print_error=False)

    pipeline.prewarm()
    setup_s = time.perf_counter() - t0
    print(f"         Done in {setup_s:.1f}s\n")

    # ── Generate ────────────────────────────────────────────────────────
    print(f"  [2/3] Generating image ({width}x{height}, {args.steps} steps)...")
    t1 = time.perf_counter()

    try:
        png_bytes = pipeline.generate_png(
            prompt=args.prompt,
            seed=seed,
            steps=args.steps,
            height=height,
            width=width,
        )
        diffusion_s = time.perf_counter() - t1
        peak_mb = pipeline.last_peak_memory_mb or 0.0
        print(f"         Done in {diffusion_s:.1f}s (peak VRAM: {peak_mb:.0f} MB)\n")
    except RuntimeError as e:
        if "out of memory" in str(e).lower():
            torch.cuda.empty_cache()
            print(f"\n  ❌ CUDA OUT OF MEMORY at {width}x{height}.")
            print(f"     Try --size 512x512 or --size 416x416")
            print(f"     Your GPU has {vram_mb:.0f} MB VRAM; this model needs 5+ GB at 512x512.")
            print(f"     For reliable generation, use the cloud script: python bonsai_generate.py")
            sys.exit(1)
        raise

    # ── Save ────────────────────────────────────────────────────────────
    print(f"  [3/3] Saving to {output_path}...")
    output_path.write_bytes(png_bytes)

    # Persist gemlite autotune cache
    GemLiteLinearTriton.cache_config(str(gemlite_cache))

    wall_s = time.perf_counter() - t0
    print(f"\n{'='*60}")
    print(f"  ✅ Generated in {wall_s:.1f}s total")
    print(f"     Setup     : {setup_s:.1f}s")
    print(f"     Diffusion : {diffusion_s:.1f}s")
    print(f"     Peak VRAM : {peak_mb:.0f} MB")
    print(f"     Saved     : {output_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
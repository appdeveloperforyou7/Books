#!/usr/bin/env python3
"""
Local Bonsai Image API Client (Gradio)
- Uses gradio_client to connect to the shared Gradio app
- Auto-discovers URL from /tmp/bonsai_gradio_url.json
- Retries on transient failures
- Saves images locally
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from gradio_client import Client, handle_file
from PIL import Image
import io


def discover_url() -> str:
    """Try to find the Gradio share URL."""
    candidates = [
        Path("/tmp/bonsai_gradio_url.json"),
        Path.home() / ".bonsai_gradio_url.json",
        Path.cwd() / "bonsai_gradio_url.json",
    ]
    for p in candidates:
        if p.exists():
            try:
                data = json.loads(p.read_text())
                url = data.get("share_url", "")
                if url.startswith("http"):
                    return url
            except Exception:
                pass

    env_url = os.environ.get("BONSAI_GRADIO_URL")
    if env_url:
        return env_url

    raise RuntimeError(
        "Could not discover Gradio URL.\n"
        "Set BONSAI_GRADIO_URL env var, ensure the notebook wrote /tmp/bonsai_gradio_url.json, or pass --url explicitly."
    )


def generate_image(
    prompt: str,
    url: str,
    seed: int | None = None,
    steps: int = 4,
    width: int = 512,
    height: int = 512,
    save_path: str = "/tmp/bonsai_output.png",
    max_retries: int = 3,
    timeout: int = 120,
) -> dict:
    """Send generation request via Gradio client and save image."""
    client = Client(url, timeout=timeout)

    seed_val = int(seed) if seed is not None else None

    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            # Gradio predict: returns (PIL.Image, seed_used)
            result = client.predict(
                prompt=prompt,
                seed=seed_val,
                steps=steps,
                width=width,
                height=height,
                api_name="/predict",
            )
            img, used_seed = result

            if isinstance(img, str):
                # Sometimes gradio returns file path
                img = Image.open(img)

            img.save(save_path)

            return {
                "success": True,
                "path": save_path,
                "prompt": prompt,
                "seed_used": int(used_seed) if used_seed is not None else None,
                "attempt": attempt,
            }
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                wait = min(2 ** attempt, 10)
                print(f"Retry {attempt}/{max_retries} in {wait}s... ({e})")
                time.sleep(wait)
            else:
                raise RuntimeError(f"Failed after {max_retries} attempts: {last_err}") from last_err


def main():
    parser = argparse.ArgumentParser(description="Local Bonsai Image API client (Gradio)")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--url", help="Gradio share URL or API endpoint")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--output", default="/tmp/bonsai_output.png")
    parser.add_argument("--retries", type=int, default=3)
    args = parser.parse_args()

    if args.url:
        api_url = args.url
    else:
        api_url = discover_url()
        print(f"Discovered Gradio URL: {api_url}")

    print(f"Prompt: {args.prompt}")
    print(f"Size: {args.width}x{args.height}, steps={args.steps}, seed={args.seed}")

    t0 = time.time()
    result = generate_image(
        prompt=args.prompt,
        url=api_url,
        seed=args.seed,
        width=args.width,
        height=args.height,
        steps=args.steps,
        save_path=args.output,
        max_retries=args.retries,
    )
    wall = time.time() - t0

    print(f"\\nDone in {wall:.2f}s")
    print(f"Saved to: {result['path']}")
    print(f"Seed used: {result['seed_used']}")


if __name__ == "__main__":
    main()

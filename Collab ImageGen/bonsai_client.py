#!/usr/bin/env python3
"""
Local Bonsai Image Client
- Sends prompts to the Colab-hosted FastAPI backend
- Auto-discovers URL from /tmp/bonsai_status.json or BONSAI_URL env var
- Retries on transient failures
- Saves generated images locally
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Missing dependency: requests\nInstall with: pip install requests")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Missing dependency: Pillow\nInstall with: pip install Pillow")
    sys.exit(1)

import io


DEFAULT_URL = "http://127.0.0.1:8000"
STATUS_FILES = [
    Path("/tmp/bonsai_status.json"),
    Path.home() / ".bonsai_status.json",
    Path.cwd() / "bonsai_status.json",
]


def discover_url() -> str:
    for path in STATUS_FILES:
        if path.exists():
            try:
                data = json.loads(path.read_text())
                if data.get("ready") and data.get("generate_endpoint"):
                    return data["generate_endpoint"]
            except Exception:
                pass

    env_url = os.environ.get("BONSAI_URL")
    if env_url:
        return env_url

    return DEFAULT_URL.rstrip("/") + "/generate"


def generate_image(
    prompt: str,
    url: str,
    seed: int | None = None,
    steps: int = 4,
    width: int = 512,
    height: int = 512,
    save_path: str = "bonsai_output.png",
    max_retries: int = 3,
    timeout: int = 120,
) -> dict:
    payload = {
        "prompt": prompt,
        "seed": seed,
        "steps": steps,
        "width": width,
        "height": height,
    }

    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(url, json=payload, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()

            if not data.get("success"):
                raise RuntimeError(f"API error: {data.get('error')}")

            img_b64 = data.get("image_base64")
            if not img_b64:
                raise RuntimeError("Missing image_base64 in response")

            img = Image.open(io.BytesIO(base64.b64decode(img_b64)))
            img.save(save_path)

            return {
                "success": True,
                "path": save_path,
                "prompt": data.get("prompt", prompt),
                "seed_used": data.get("seed_used"),
                "time": data.get("time"),
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
    parser = argparse.ArgumentParser(description="Bonsai Image local client")
    parser.add_argument("prompt", help="Text prompt")
    parser.add_argument("--url", help="API URL")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--output", default="bonsai_output.png")
    parser.add_argument("--retries", type=int, default=3)
    args = parser.parse_args()

    api_url = (args.url or discover_url()).rstrip("/")
    print(f"URL: {api_url}")
    print(f"Prompt: {args.prompt}")
    print(f"Size: {args.width}x{args.height}, steps={args.steps}, seed={args.seed}")

    t0 = time.time()
    result = generate_image(
        prompt=args.prompt,
        url=api_url,
        seed=args.seed,
        steps=args.steps,
        width=args.width,
        height=args.height,
        save_path=args.output,
        max_retries=args.retries,
    )
    wall = time.time() - t0

    print(f"Done in {wall:.2f}s")
    print(f"Saved: {result['path']}")
    print(f"Seed: {result.get('seed_used')}")


if __name__ == "__main__":
    main()

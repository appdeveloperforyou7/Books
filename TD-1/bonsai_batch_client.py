"""
Bonsai Batch Client — Run on THIS laptop.

Reads All_Image_Prompts.txt, skips images that already exist,
and calls the Bonsai server on the other laptop for each missing one.

Usage:
    # Generate all missing images
    python bonsai_batch_client.py --server 192.168.1.50

    # Custom port, 512x512 for low VRAM, retry on failure
    python bonsai_batch_client.py --server 192.168.1.50 --port 8765 --size 512 --retries 3

    # Only generate for specific characters
    python bonsai_batch_client.py --server 192.168.1.50 --only Maya Leo

    # Dry run (show what would be generated, don't actually call)
    python bonsai_batch_client.py --server 192.168.1.50 --dry-run
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json

SCRIPT_DIR = Path(__file__).resolve().parent
PROMPTS_FILE = SCRIPT_DIR / "All_Image_Prompts.txt"
CHARACTERS_DIR = SCRIPT_DIR / "Characters"
ARCHIVE_DIR_NAME = "Archive"


def parse_prompts(text: str) -> list[dict]:
    entries = []
    current_filename = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("FILENAME:"):
            current_filename = line.split(":", 1)[1].strip()
        elif line.startswith("PROMPT:") and current_filename:
            prompt = line.split(":", 1)[1].strip()
            entries.append({"filename": current_filename, "prompt": prompt})
            current_filename = None
    return entries


def image_exists(rel_path: str) -> bool:
    p = CHARACTERS_DIR.parent / rel_path
    if p.exists() and p.stat().st_size > 1000:
        return True
    stem = p.stem + p.suffix
    archive_p = p.parent / ARCHIVE_DIR_NAME / stem
    if archive_p.exists() and archive_p.stat().st_size > 1000:
        return True
    return False


def generate_one(server_url: str, prompt: str, width: int, height: int, retries: int) -> bytes:
    payload = json.dumps({
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": 4,
    }).encode("utf-8")

    req = Request(
        f"{server_url}/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with urlopen(req, timeout=300) as resp:
                if resp.status == 200:
                    return resp.read()
                body = resp.read().decode("utf-8", errors="replace")
                print(f"    HTTP {resp.status}: {body[:200]}")
                if resp.status == 507:
                    print("    Server OOM — try smaller --size")
                    return b""
        except HTTPError as e:
            print(f"    HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}")
            if e.code == 507:
                return b""
        except (URLError, ConnectionError, TimeoutError) as e:
            last_err = e
            print(f"    Attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                wait = attempt * 5
                print(f"    Retrying in {wait}s...")
                time.sleep(wait)
        except Exception as e:
            last_err = e
            print(f"    Unexpected error: {e}")
            if attempt < retries:
                time.sleep(5)

    print(f"    FAILED after {retries} attempts: {last_err}")
    return b""


def main():
    parser = argparse.ArgumentParser(description="Bonsai Batch Image Client")
    parser.add_argument("--server", required=True, help="Server IP or hostname (e.g. 192.168.1.50)")
    parser.add_argument("--port", type=int, default=8765, help="Server port (default 8765)")
    parser.add_argument("--size", type=int, default=1024, help="Image width & height (default 1024)")
    parser.add_argument("--retries", type=int, default=3, help="Retries per image (default 3)")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds between requests (default 2)")
    parser.add_argument("--only", nargs="+", help="Only generate for these characters (e.g. --only Maya Leo)")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without generating")
    parser.add_argument("--overwrite", action="store_true", help="Re-generate even if file exists")
    args = parser.parse_args()

    if not PROMPTS_FILE.exists():
        print(f"ERROR: {PROMPTS_FILE} not found")
        sys.exit(1)

    server_url = f"http://{args.server}:{args.port}"
    text = PROMPTS_FILE.read_text(encoding="utf-8")
    entries = parse_prompts(text)

    if not entries:
        print("No prompts found in All_Image_Prompts.txt")
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"  Bonsai Batch Client")
    print(f"  Server  : {server_url}")
    print(f"  Size    : {args.size}x{args.size}")
    print(f"  Prompts : {len(entries)} total")
    print(f"{'=' * 60}\n")

    if not args.dry_run:
        try:
            req = Request(f"{server_url}/health")
            with urlopen(req, timeout=10) as resp:
                if resp.status != 200:
                    print("ERROR: Server health check failed")
                    sys.exit(1)
            print("Server is reachable.\n")
        except Exception as e:
            print(f"ERROR: Cannot reach server at {server_url}: {e}")
            print("Make sure bonsai_server.py is running on the other laptop.")
            sys.exit(1)

    todo = []
    skip = []
    for entry in entries:
        rel = entry["filename"]
        char_name = Path(rel).parts[1] if len(Path(rel).parts) > 1 else ""

        if args.only and char_name not in args.only:
            skip.append((rel, "filtered"))
            continue

        if not args.overwrite and image_exists(rel):
            skip.append((rel, "exists"))
            continue

        todo.append(entry)

    for rel, reason in skip:
        tag = "EXISTS" if reason == "exists" else "SKIP"
        print(f"  [{tag}] {rel}")

    print(f"\n  To generate: {len(todo)}")
    print(f"  Skipped    : {len(skip)}")
    print()

    if args.dry_run:
        print("Dry run — no images generated.")
        for entry in todo:
            print(f"  WOULD GEN: {entry['filename']}")
            print(f"    Prompt: {entry['prompt'][:100]}...")
        return

    if not todo:
        print("Nothing to generate — all images exist!")
        return

    success = 0
    failed = 0

    for i, entry in enumerate(todo, 1):
        rel = entry["filename"]
        prompt = entry["prompt"]
        out_path = CHARACTERS_DIR.parent / rel

        print(f"[{i}/{len(todo)}] {rel}")
        print(f"  Prompt: {prompt[:100]}...")

        out_path.parent.mkdir(parents=True, exist_ok=True)

        png_bytes = generate_one(server_url, prompt, args.size, args.size, args.retries)

        if png_bytes and len(png_bytes) > 1000:
            out_path.write_bytes(png_bytes)
            kb = len(png_bytes) / 1024
            print(f"  SAVED: {out_path} ({kb:.0f} KB)\n")
            success += 1
        else:
            print(f"  FAILED: {rel}\n")
            failed += 1

        if i < len(todo):
            time.sleep(args.delay)

    print(f"\n{'=' * 60}")
    print(f"  Done!  Success: {success}  Failed: {failed}")
    print(f"{'=' * 60}\n")

    if failed > 0:
        print("Re-run to retry failed images (they won't be skipped since they weren't saved).")


if __name__ == "__main__":
    main()

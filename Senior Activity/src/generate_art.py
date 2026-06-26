"""Generate cover hero art via the Hugging Face Inference API (stdlib only).

Prerequisites (do these before running):
  1. Create a HF access token (huggingface.co -> Settings -> Access Tokens).
  2. Set it in your environment:  $env:HF_TOKEN = "hf_xxx"   (PowerShell)
  3. Open the model page and ACCEPT its license (image models are gated):
     https://huggingface.co/black-forest-labs/FLUX.1-schnell
  4. Run:  python -m src.generate_art

Default model FLUX.1-schnell is Apache-2.0 (commercial OK for KDP).
Outputs: output/<theme>/art/hero.png  -> automatically used by the cover
renderer if present (otherwise the vector motif band is drawn).
"""
from __future__ import annotations
import os
import json
import time
import urllib.request
import urllib.error

from . import config as C
from .themes.registry import THEMES


def _load_env():
    """Load PROJECT_ROOT/.env into os.environ (stdlib only)."""
    p = C.PROJECT_ROOT / ".env"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_env()

MODEL = os.environ.get("HF_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")
HF_TOKEN = os.environ.get("HF_TOKEN")
API_URL = "https://router.huggingface.co/hf-inference/models/" + MODEL

# Warm storybook style + a CONSISTENT cartoon elderly couple (locked description
# + fixed seed) as the hero on every cover, with only the themed setting
# changing. This humanizes the covers, signals "for seniors", and makes the
# series feel less computer-generated/templated. Crisp, correct puzzle grids are
# still overlaid on the cover via vector tiles (AI garbles letters/numbers).
COUPLE = ("a cheerful elderly couple doing puzzles together at a cozy table: "
          "a grandmother with silver hair in a bun, glasses and a teal cardigan, "
          "and a grandfather with a white mustache, glasses and a brown sweater, "
          "both smiling warmly, holding pencils over an open large-print puzzle "
          "book showing grid pages")

STYLE = ("warm friendly cartoon illustration, soft storybook style, gentle "
         "shading, cheerful cozy and inviting, premium feel, clean solid "
         "off-white cream background, no text, no words, no letters, no numbers, "
         "no signage, no logos, no watermark")


def _p(setting):
    return f"{COUPLE}, {setting}"


PROMPTS = {
    "gardens": _p("surrounded by flowers, songbirds and a watering can by a sunny window"),
    "food": _p("with a teapot, fresh fruit and a homemade pie on the table"),
    "travel": _p("with a globe, a suitcase, maps and little landmark souvenirs"),
    "faith": _p("with a soft glowing candle, a white dove and warm golden light"),
    "holidays": _p("with a small decorated tree, wrapped gifts and warm string lights"),
    "musicmovies": _p("with a vinyl record, a film reel and floating musical notes"),
    "nature": _p("by a window overlooking mountains, a calm lake and pine trees"),
    "animals": _p("with a friendly dog and a cat resting happily nearby"),
    "sports": _p("with a chessboard, a soccer ball and a tennis racket close by"),
    "wellness": _p("with a cup of herbal tea, a green plant and a glass of water"),
}


def _is_image(data: bytes) -> bool:
    return (data[:4] == b"\x89PNG" or data[:6] in (b"GIF87a", b"GIF89a")
            or data[:2] == b"BM" or data[:3] == b"\xff\xd8\xff")


def generate(prompt: str, seed: int, path, width=1024, height=1024,
             steps=4, tries=6) -> bool:
    payload = json.dumps({
        "inputs": f"{prompt}. {STYLE}",
        "parameters": {"seed": seed, "width": width, "height": height,
                       "num_inference_steps": steps},
    }).encode("utf-8")
    headers = {"Authorization": f"Bearer {HF_TOKEN}",
               "Content-Type": "application/json"}
    last = None
    for i in range(tries):
        req = urllib.request.Request(API_URL, data=payload, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = resp.read()
            if _is_image(data):
                path.write_bytes(data)
                return True
            last = json.loads(data).get("error", data[:160])
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:160].decode('utf-8', 'ignore')}"
        except Exception as e:  # noqa
            last = str(e)
        print(f"    retry {i + 1}/{tries}: {last}")
        time.sleep(10)  # model may be loading on the free tier
    return False


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Generate cover hero art via HF Inference API.")
    ap.add_argument("--theme", default=None, help="only generate this theme key")
    args = ap.parse_args()

    if not HF_TOKEN:
        raise SystemExit(
            "HF_TOKEN not set. Put it in .env (HF_TOKEN=...) or export it, "
            "and accept the model license on its HF page.")
    print(f"Model: {MODEL}")
    FIXED_SEED = 77  # same couple across the whole family
    for key, theme in THEMES.items():
        if args.theme and key != args.theme:
            continue
        prompt = PROMPTS.get(key, theme.title)
        out_dir = C.OUTPUT_DIR / key / "art"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / "hero.png"
        if path.exists():
            print(f"[{key}] exists, skip")
            continue
        print(f"[{key}] {prompt}")
        ok = generate(prompt, FIXED_SEED, path)
        print("    -> ok" if ok else "    -> FAILED")


if __name__ == "__main__":
    main()

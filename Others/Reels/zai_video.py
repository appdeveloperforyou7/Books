"""Generate a video clip via the Z.AI (GLM / CogVideoX) video API.

Image-to-video: uses a cover/artwork image as the first frame and animates it.
Runs entirely via the hosted API (no local GPU needed).

Setup:
  Get an API key from https://z.ai/manage-apikey/apikey-list and set it:
    PowerShell : $env:ZAI_API_KEY = "your-key-here"
    cmd        : set ZAI_API_KEY=your-key-here

Usage:
  python zai_video.py --image VAULT_B_Kindle_Cover.jpg ^
      --prompt "Cinematic slow push-in on an ancient temple..." ^
      --out clip_01.mp4 [--model cogvideox-3] [--size 1080x1920] ^
      [--duration 5] [--quality quality|speed] [--with-audio]
"""
import argparse
import base64
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
from PIL import Image

API_BASE = "https://api.z.ai/api"


def _call(method: str, path: str, key: str, body=None) -> dict:
    req = urllib.request.Request(
        API_BASE + path,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        method=method,
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "ignore")
        raise RuntimeError(f"HTTP {exc.code} {exc.reason}: {detail}") from None


def image_to_data_url(path: str, size) -> str:
    w, h = size
    im = Image.open(path).convert("RGB")
    src_ar, tgt_ar = im.width / im.height, w / h
    if src_ar > tgt_ar:
        nh = im.height
        nw = int(round(nh * tgt_ar))
        left = (im.width - nw) // 2
        im = im.crop((left, 0, left + nw, nh))
    else:
        nw = im.width
        nh = int(round(nw / tgt_ar))
        top = (im.height - nh) // 2
        im = im.crop((0, top, nw, top + nh))
    im = im.resize((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def main() -> int:
    ap = argparse.ArgumentParser(description="Z.AI CogVideoX image-to-video")
    ap.add_argument("--image", required=True, help="Reference/first-frame image")
    ap.add_argument("--prompt", required=True, help="Motion description (<=512 chars)")
    ap.add_argument("--out", required=True, help="Output .mp4 path")
    ap.add_argument("--model", default="cogvideox-3")
    ap.add_argument("--size", default="1080x1920",
                    choices=["1280x720", "720x1280", "1024x1024", "1920x1080", "1080x1920",
                             "2048x1080", "3840x2160"])
    ap.add_argument("--duration", type=int, default=5, choices=[5, 10])
    ap.add_argument("--quality", default="quality", choices=["quality", "speed"])
    ap.add_argument("--with-audio", action="store_true")
    ap.add_argument("--poll", type=int, default=15, help="Seconds between status checks")
    args = ap.parse_args()

    key = os.environ.get("ZAI_API_KEY")
    if not key:
        print("[error] ZAI_API_KEY not set. Get one at "
              "https://z.ai/manage-apikey/apikey-list", file=sys.stderr)
        return 2

    w, h = (int(x) for x in args.size.split("x"))
    data_url = image_to_data_url(args.image, (w, h))
    body = {
        "model": args.model,
        "image_url": [data_url],
        "prompt": args.prompt[:512],
        "quality": args.quality,
        "with_audio": bool(args.with_audio),
        "size": args.size,
        "fps": 30,
        "duration": args.duration,
    }
    print(f"Submitting {args.model} image->video ({args.size}, {args.duration}s, {args.quality})...")
    res = _call("POST", "/paas/v4/videos/generations", key, body)
    tid = res.get("id")
    if not tid:
        print("[error] no task id returned:", res, file=sys.stderr)
        return 1
    print("Task id:", tid, "| initial:", res.get("task_status"))

    while True:
        time.sleep(args.poll)
        st = _call("GET", f"/paas/v4/async-result/{tid}", key)
        status = st.get("task_status")
        print("  status:", status)
        if status == "SUCCESS":
            vids = st.get("video_result") or []
            if not vids:
                print("[error] SUCCESS but no video_result:", st, file=sys.stderr)
                return 1
            url = vids[0]["url"]
            print("Downloading:", url)
            urllib.request.urlretrieve(url, args.out)
            print("Saved:", args.out)
            return 0
        if status == "FAIL":
            print("[error] generation FAILED:", st, file=sys.stderr)
            return 1


if __name__ == "__main__":
    raise SystemExit(main())

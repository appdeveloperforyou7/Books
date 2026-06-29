# -*- coding: utf-8 -*-
"""Build Kindle (front-only) cover images for the DE / ES / FR editions.

The front panel is extracted from each language's combined wraparound source
image via Canny edge detection (spine boundaries), then resized/cropped to the
same Kindle dimensions used for the English edition (1838 x 2775).
"""
import os
import numpy as np
from PIL import Image
from skimage import feature
from scipy.ndimage import uniform_filter1d
from scipy.signal import find_peaks

ROOT = r"D:\Kapil\Books\Elena Vance Series\The Quiet Wife"
TARGET_W, TARGET_H = 1838, 2775  # matches the English Kindle cover


def detect_spine(img):
    gray = img.mean(axis=2)
    edges = feature.canny(gray, sigma=2, low_threshold=30, high_threshold=80)
    s = uniform_filter1d(edges.mean(axis=0), size=5)
    peaks, _ = find_peaks(s, distance=30, prominence=0.05)
    sp = peaks[np.argsort(s[peaks])[::-1]]
    for i in range(len(sp)):
        for j in range(i + 1, len(sp)):
            if 30 <= abs(sp[i] - sp[j]) <= 250:
                return tuple(sorted([sp[i], sp[j]]))
    raise ValueError("Could not detect spine boundaries")


def build(src_path, out_dir):
    arr = np.array(Image.open(src_path).convert("RGB"))
    e1, e2 = detect_spine(arr)
    front = arr[:, e2 + 1:, :]
    front_img = Image.fromarray(front)

    # Fit the full front artwork to the Kindle height (preserve everything),
    # then pad the sides with the panel's own edge color. Matches the English
    # Kindle cover: no top/bottom cropping.
    scale = TARGET_H / front_img.height
    new_w = int(round(front_img.width * scale))
    resized = front_img.resize((new_w, TARGET_H), Image.LANCZOS)

    edge_color = tuple(int(c) for c in front[:, -1, :].mean(axis=0).astype(int))
    canvas = Image.new("RGB", (TARGET_W, TARGET_H), edge_color)
    canvas.paste(resized, ((TARGET_W - new_w) // 2, 0))
    cropped = canvas

    png_path = os.path.join(out_dir, "Kindle cover.png")
    jpg_path = os.path.join(out_dir, "Kindle cover.jpg")
    cropped.save(png_path, "PNG")
    cropped.save(jpg_path, "JPEG", quality=95)
    print(f"{os.path.basename(out_dir)}: spine cols {e1}-{e2} "
          f"(front {front.shape[1]}px) -> {TARGET_W}x{TARGET_H}")


EDITIONS = [
    ("German", "German paperback image.png"),
    ("Spanish", "Spanish paperback image.png"),
    ("French", "Fench paperback image.png"),
]

for lang, src_name in EDITIONS:
    folder = os.path.join(ROOT, lang)
    build(os.path.join(folder, src_name), folder)

print("\nDone.")

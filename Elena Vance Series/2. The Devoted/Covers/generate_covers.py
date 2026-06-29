"""Generate Kindle cover image + paperback cover PDF from a combined paperback cover image.

Workflow:
  1. Split combined cover (back + spine + front) via Canny edge detection
  2. Build Kindle cover (front only, 1600x2560, 1:1.6)
  3. Build paperback cover PDF (KDP 5.5x8.5 trim, bleed, spine)

See: D:\Kapil\Books\Others\Cover generation\CoversGen.md
"""

import os
import numpy as np
from PIL import Image
from skimage import feature
from scipy.ndimage import uniform_filter1d
from scipy.signal import find_peaks
from fpdf import FPDF

# --- Config -----------------------------------------------------------------
SRC = r"D:\Kapil\Books\Elena Vance Series\2. The Devoted\Covers\Paperback image main.png"
OUT_DIR = r"D:\Kapil\Books\Elena Vance Series\2. The Devoted\Covers"
PAGE_COUNT = 150        # from The_Devoted_interior.pdf (5.5x8.5)
TRIM_W, TRIM_H = 5.5, 8.5
BLEED = 0.125
DPI = 300

BACK_PATH  = os.path.join(OUT_DIR, "back_cover.png")
SPINE_PATH = os.path.join(OUT_DIR, "spine_cover.png")
FRONT_PATH = os.path.join(OUT_DIR, "front_cover.png")
KINDLE_PATH = os.path.join(OUT_DIR, "kindle_cover.jpg")
PDF_PATH    = os.path.join(OUT_DIR, "paperback_cover.pdf")


def inches_to_px(inches):
    return int(round(inches * DPI))


def split_cover(image_path, out_dir):
    """Split a paperback cover image into back, spine, and front via Canny edges."""
    img = np.array(Image.open(image_path).convert("RGB"))
    h, w = img.shape[:2]

    gray = img.mean(axis=2)
    edges = feature.canny(gray, sigma=2, low_threshold=30, high_threshold=80)

    vertical_edge_strength = edges.mean(axis=0)
    smooth_strength = uniform_filter1d(vertical_edge_strength, size=5)

    peaks, _ = find_peaks(smooth_strength, distance=30, prominence=0.05)

    sorted_peaks = peaks[np.argsort(smooth_strength[peaks])[::-1]]
    edge1, edge2 = None, None
    for i in range(len(sorted_peaks)):
        for j in range(i + 1, len(sorted_peaks)):
            sep = abs(sorted_peaks[i] - sorted_peaks[j])
            if 30 <= sep <= 250:
                edge1, edge2 = sorted([sorted_peaks[i], sorted_peaks[j]])
                break
        if edge1 is not None:
            break

    if edge1 is None:
        raise ValueError("Could not detect spine boundaries")

    spine_start, spine_end = edge1, edge2

    Image.fromarray(img[:, :spine_start, :]).save(os.path.join(out_dir, "back_cover.png"))
    Image.fromarray(img[:, spine_start:spine_end + 1, :]).save(os.path.join(out_dir, "spine_cover.png"))
    Image.fromarray(img[:, spine_end + 1:, :]).save(os.path.join(out_dir, "front_cover.png"))

    print(f"Split OK | W={w} -> back {spine_start}px | spine {edge2-edge1+1}px | front {w-edge2-1}px")
    return spine_start, edge2 - edge1 + 1, w - edge2 - 1


def create_kindle_cover(front_path, output_path, target_w=1600, target_h=2560):
    """Resize/crop the front cover to Kindle specs (1600x2560, 1:1.6), cover crop."""
    img = Image.open(front_path).convert("RGB")

    src_w, src_h = img.size
    src_ratio = src_w / src_h
    tgt_ratio = target_w / target_h

    # Cover-crop: fill the target frame, crop overflow
    if src_ratio > tgt_ratio:
        # source is wider -> crop sides
        new_w = int(round(src_h * tgt_ratio))
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        # source is taller -> crop top/bottom
        new_h = int(round(src_w / tgt_ratio))
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    img = img.resize((target_w, target_h), Image.LANCZOS)
    img.save(output_path, quality=95)
    print(f"Kindle cover: {output_path} ({target_w}x{target_h})")


def create_paperback_cover(back_path, spine_path, front_path, output_path,
                           page_count=PAGE_COUNT, trim_w=TRIM_W, trim_h=TRIM_H, bleed=BLEED):
    """Generate KDP paperback cover PDF from 3 separate images."""
    spine_in = 0.002252 * page_count + 0.001872
    cover_w = 2 * trim_w + spine_in + 2 * bleed
    cover_h = trim_h + 2 * bleed

    back_w = trim_w + bleed
    front_w = trim_w + bleed

    sections = [
        (back_w, back_path),
        (spine_in, spine_path),
        (front_w, front_path),
    ]

    canvas = Image.new("RGB", (inches_to_px(cover_w), inches_to_px(cover_h)), (255, 255, 255))

    x_px = 0
    for w_in, img_path in sections:
        w_px = inches_to_px(w_in)
        img = Image.open(img_path).convert("RGB")
        resized = img.resize((w_px, inches_to_px(cover_h)), Image.LANCZOS)
        canvas.paste(resized, (x_px, 0))
        x_px += w_px

    canvas_path = os.path.join(os.path.dirname(output_path), "_paperback_canvas.png")
    canvas.save(canvas_path)

    pdf = FPDF(unit="in", format=(cover_w, cover_h))
    pdf.set_auto_page_break(False)
    pdf.add_page()
    pdf.image(canvas_path, x=0, y=0, w=cover_w, h=cover_h)
    pdf.output(output_path)
    print(f"Paperback cover: {output_path} ({cover_w:.3f}\" x {cover_h:.3f}\"), spine {spine_in:.3f}\"")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    split_cover(SRC, OUT_DIR)
    create_kindle_cover(FRONT_PATH, KINDLE_PATH)
    create_paperback_cover(BACK_PATH, SPINE_PATH, FRONT_PATH, PDF_PATH, page_count=PAGE_COUNT)
    print("\nDone.")

# -*- coding: utf-8 -*-
"""Build KDP paperback cover PDFs for the DE / ES / FR editions of THE QUIET WIFE.

Each language folder already contains a single combined wraparound source image
(back + spine + front). We scale it to the full KDP paperback cover width
(2 x trim + spine + 2 x bleed) using that edition's real interior page count,
center-crop to the cover height, then emit PNG + PDF.

This mirrors how the English paperback_cover.pdf was produced.
"""
import os
import numpy as np
from PIL import Image
from fpdf import FPDF

ROOT = r"D:\Kapil\Books\Elena Vance Series\1. The Quiet Wife"

DPI = 300
TRIM_W, TRIM_H = 5.5, 8.5
BLEED = 0.125
# KDP requires at least 0.0625" of clear space on both sides of the spine text.
# We target a little more for safety against binding shift.
SPINE_TEXT_MARGIN = 0.08


def spine_width(page_count):
    # KDP black-ink white-paper spine factor.
    return 0.002252 * page_count + 0.001872


def fix_spine_text_margins(cover_img, page_count):
    """Narrow the spine text so it has >= SPINE_TEXT_MARGIN inches of clear
    background on both sides of the KDP spine zone.

    The spine text is baked into the source wraparound image and, after the
    cover is scaled to the real KDP width, often ends up filling almost the
    whole spine (leaving <0.0625" on a side). We extract the exact spine zone,
    measure the text width, and if the margin is too small we uniformly shrink
    the zone (preserving the font aspect ratio) and re-center it on the spine's
    cream background.
    """
    spine = spine_width(page_count)
    sl = int(round((TRIM_W + BLEED) * DPI))
    sr = int(round((TRIM_W + BLEED + spine) * DPI))
    zone_w = sr - sl
    H = cover_img.size[1]
    if zone_w <= 1:
        return cover_img

    zone = cover_img.crop((sl, 0, sr, H)).convert("RGB")
    arr = np.asarray(zone).astype(int)
    gray = arr.mean(axis=2)

    # Spine background is a solid cream; the text is noticeably darker.
    bg_level = float(np.median(gray))
    bg_color = tuple(int(round(v)) for v in arr[0:8, 0:8].reshape(-1, 3).mean(axis=0))

    text_cols = np.where((gray < (bg_level - 45)).any(axis=0))[0]
    if len(text_cols) == 0:
        return cover_img

    text_w_px = int(text_cols[-1] - text_cols[0] + 1)
    current_margin_in = (zone_w - text_w_px) / 2.0 / DPI
    if current_margin_in >= SPINE_TEXT_MARGIN:
        return cover_img  # already compliant

    target_text_w_px = zone_w - 2 * SPINE_TEXT_MARGIN * DPI
    if target_text_w_px <= 0:
        return cover_img
    factor = target_text_w_px / float(text_w_px)

    new_w = max(1, int(round(zone_w * factor)))
    new_h = max(1, int(round(H * factor)))
    shrunk = zone.resize((new_w, new_h), Image.LANCZOS)

    new_zone = Image.new("RGB", (zone_w, H), bg_color)
    new_zone.paste(shrunk, ((zone_w - new_w) // 2, (H - new_h) // 2))
    cover_img.paste(new_zone, (sl, 0))
    return cover_img


def build(src_path, out_pdf, page_count):
    cover_w = 2 * TRIM_W + spine_width(page_count) + 2 * BLEED
    cover_h = TRIM_H + 2 * BLEED

    canvas_w = int(round(cover_w * DPI))
    canvas_h = int(round(cover_h * DPI))

    img = Image.open(src_path).convert("RGB")
    src_w, src_h = img.size

    # Scale so width matches the full cover, then center-crop the height.
    scale = canvas_w / src_w
    new_h = int(round(src_h * scale))
    resized = img.resize((canvas_w, new_h), Image.LANCZOS)
    if new_h > canvas_h:
        top = (new_h - canvas_h) // 2
        resized = resized.crop((0, top, canvas_w, top + canvas_h))
    elif new_h < canvas_h:
        resized = resized.resize((canvas_w, canvas_h), Image.LANCZOS)

    resized = fix_spine_text_margins(resized, page_count)

    png_path = out_pdf.replace(".pdf", ".png")
    resized.save(png_path, "PNG")

    pdf = FPDF(unit="in", format=(cover_w, cover_h))
    pdf.set_auto_page_break(False)
    pdf.set_margins(0, 0, 0)
    pdf.add_page()
    pdf.image(png_path, x=0, y=0, w=cover_w, h=cover_h)
    pdf.output(out_pdf)

    print(f"{os.path.basename(out_pdf)}: {cover_w:.4f}\" x {cover_h:.4f}\"  "
          f"(pages={page_count}, spine={spine_width(page_count):.4f}\")")


EDITIONS = [
    ("German", "German paperback image.png", "Die_Stille_Frau_interior.pdf", 177),
    ("Spanish", "Spanish paperback image.png", "La_Esposa_Silenciosa_interior.pdf", 163),
    ("French", "Fench paperback image.png", "L_Epouse_Silencieuse_interior.pdf", 170),
]

for lang, src_name, interior, pages in EDITIONS:
    folder = os.path.join(ROOT, lang)
    build(
        src_path=os.path.join(folder, src_name),
        out_pdf=os.path.join(folder, "paperback_cover.pdf"),
        page_count=pages,
    )

print("\nDone.")

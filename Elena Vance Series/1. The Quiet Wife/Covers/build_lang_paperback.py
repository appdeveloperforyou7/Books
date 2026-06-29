# -*- coding: utf-8 -*-
"""Build KDP paperback cover PDFs for the DE / ES / FR editions of THE QUIET WIFE.

Each language folder already contains a single combined wraparound source image
(back + spine + front). We scale it to the full KDP paperback cover width
(2 x trim + spine + 2 x bleed) using that edition's real interior page count,
center-crop to the cover height, then emit PNG + PDF.

This mirrors how the English paperback_cover.pdf was produced.
"""
import os
from PIL import Image
from fpdf import FPDF

ROOT = r"D:\Kapil\Books\Elena Vance Series\1. The Quiet Wife"

DPI = 300
TRIM_W, TRIM_H = 5.5, 8.5
BLEED = 0.125


def spine_width(page_count):
    # KDP black-ink white-paper spine factor.
    return 0.002252 * page_count + 0.001872


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

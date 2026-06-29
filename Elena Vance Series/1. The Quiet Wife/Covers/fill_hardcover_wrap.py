# -*- coding: utf-8 -*-
"""Fix the English hardcover cover so the artwork fills the wrap + bleed areas.

KDP accepted this cover's dimensions and spine but rejected it because the
front/back artwork did not extend into the wrap (0.59") and bleed (0.125")
areas - those borders were blank. Rather than change the accepted geometry
(which would risk a spine/dimension mismatch), we keep the existing canvas
exactly as-is and extend the artwork's edges outward to fill every blank
border. This satisfies KDP's "image/background must extend beyond the edge"
requirement for both the 0.125" bleed and the 0.59" wrap.

Technique: detect the content bounding box (the printed artwork), then for
each of the four borders replicate the nearest edge row/column of the artwork
so the background visually continues all the way to the canvas edge.
"""
import os
import numpy as np
from PIL import Image
from fpdf import FPDF

COVERS = r"D:\Kapil\Books\Elena Vance Series\1. The Quiet Wife\Covers"
SRC = os.path.join(COVERS, "hardcover_cover.png")
OUT_PNG = SRC
OUT_PDF = os.path.join(COVERS, "hardcover_cover.pdf")


def content_bbox(arr):
    """Bounding box of non-white content in an RGB array (top,left,bottom,right)."""
    mask = (arr[:, :, :3] < 250).any(axis=2)
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        return None
    return rows[0], cols[0], rows[-1] + 1, cols[-1] + 1


def extend_to_edges(img):
    """Fill blank borders by edge-extending the content to the full canvas."""
    arr = np.asarray(img.convert("RGB"))
    H, W, _ = arr.shape
    top, left, bottom, right = content_bbox(arr)
    if top is None:
        return img

    img = img.convert("RGB")

    # Right border: replicate the content's rightmost column across the gap.
    if right < W:
        col = img.crop((right - 1, top, right, bottom)).resize((W - right, bottom - top), Image.LANCZOS)
        img.paste(col, (right, top))

    # Left border: replicate the content's leftmost column.
    if left > 0:
        col = img.crop((left, top, left + 1, bottom)).resize((left, bottom - top), Image.LANCZOS)
        img.paste(col, (0, top))

    # Top border: replicate the top row (now full width, including side fills).
    if top > 0:
        row = img.crop((0, top, W, top + 1)).resize((W, top), Image.LANCZOS)
        img.paste(row, (0, 0))

    # Bottom border: replicate the bottom row.
    if bottom < H:
        row = img.crop((0, bottom - 1, W, bottom)).resize((W, H - bottom), Image.LANCZOS)
        img.paste(row, (0, bottom))

    return img


def main():
    img = Image.open(SRC).convert("RGB")
    canvas_w_px, canvas_h_px = img.size

    # Report the blank borders we are about to fill.
    arr = np.asarray(img)
    top, left, bottom, right = content_bbox(arr)
    print(f"Canvas: {canvas_w_px}x{canvas_h_px} "
          f"({canvas_w_px/300:.3f}x{canvas_h_px/300:.3f} in @300dpi)")
    print(f"Content bbox: top={top} left={left} bottom={bottom} right={right}")
    print(f"Blank borders (in @300dpi): "
          f"top={top/300:.3f} bottom={(canvas_h_px-bottom)/300:.3f} "
          f"left={left/300:.3f} right={(canvas_w_px-right)/300:.3f}")

    filled = extend_to_edges(img)

    # Confirm everything now reaches the edges.
    check = np.asarray(filled)
    t2, l2, b2, r2 = content_bbox(check)
    print(f"After fill, content reaches: top={t2} left={l2} bottom={b2} right={r2} "
          f"(gaps top={t2/300:.3f} left={l2/300:.3f} "
          f"bottom={(canvas_h_px-b2)/300:.3f} right={(canvas_w_px-r2)/300:.3f})")

    filled.save(OUT_PNG, "PNG")

    pdf = FPDF(unit="pt", format=(canvas_w_px, canvas_h_px))
    pdf.set_auto_page_break(False)
    pdf.set_margins(0, 0, 0)
    pdf.add_page()
    pdf.image(OUT_PNG, x=0, y=0, w=canvas_w_px, h=canvas_h_px)
    pdf.output(OUT_PDF)
    print(f"Saved: {OUT_PDF}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Build the English hardcover cover as a proper KDP case-wrap.

Previous version used low-res separate front/back/spine assets that were
scaled up and center-cropped, which made the artwork appear zoomed in, and it
left the wrap/bleed borders blank (KDP publish failure). This rebuilds from the
real paperback cover artwork (so the front/back match the paperback exactly -
no zoom), places each panel at the correct case-wrap geometry, and fills the
wrap (0.59") + bleed (0.125") borders by edge-extending the artwork.

Geometry (5.5 x 8.5 trim, 156pp):
  full width  = bleed + wrap + trim + spine + trim + wrap + bleed
  full height = bleed + wrap + trim + wrap + bleed
"""
import os
import numpy as np
from PIL import Image
from fpdf import FPDF

ROOT = r"D:\Kapil\Books\Elena Vance Series\1. The Quiet Wife"
PAPERBACK = os.path.join(ROOT, "Covers", "paperback_cover.png")
OUT_PNG = os.path.join(ROOT, "Covers", "hardcover_cover.png")
OUT_PDF = os.path.join(ROOT, "Covers", "hardcover_cover.pdf")

DPI = 300
TRIM_W, TRIM_H = 5.5, 8.5
# Exact cover size required by KDP (Case Laminate) for this title.
COVER_W, COVER_H = 13.115, 9.917
# Derived geometry (outer = wrap + bleed on every outer edge; spine between trims).
OUTER = (COVER_H - TRIM_H) / 2.0          # 0.7085"
SPINE = COVER_W - 2 * TRIM_W - 2 * OUTER  # 0.698"


def px(inches):
    return int(round(inches * DPI))


def edge_extend(panel_w, panel_h, art, ox, oy):
    """Place `art` at (ox,oy) in a panel_w x panel_h image and fill every
    exposed border by replicating the artwork's nearest edge row/column."""
    panel = Image.new("RGB", (panel_w, panel_h), (255, 255, 255))
    aw, ah = art.size
    panel.paste(art, (ox, oy))

    # Right strip (within the art's vertical span).
    if ox + aw < panel_w:
        col = art.crop((aw - 1, 0, aw, ah)).resize((panel_w - (ox + aw), ah), Image.LANCZOS)
        panel.paste(col, (ox + aw, oy))
    # Left strip.
    if ox > 0:
        col = art.crop((0, 0, 1, ah)).resize((ox, ah), Image.LANCZOS)
        panel.paste(col, (0, oy))
    # Top strip (full width, after side fills).
    if oy > 0:
        row = panel.crop((0, oy, panel_w, oy + 1)).resize((panel_w, oy), Image.LANCZOS)
        panel.paste(row, (0, 0))
    # Bottom strip.
    if oy + ah < panel_h:
        row = panel.crop((0, oy + ah - 1, panel_w, oy + ah)).resize((panel_w, panel_h - (oy + ah)), Image.LANCZOS)
        panel.paste(row, (0, oy + ah))
    return panel


def main():
    cover_w = OUTER + TRIM_W + SPINE + TRIM_W + OUTER
    cover_h = OUTER + TRIM_H + OUTER
    cw, ch = px(cover_w), px(cover_h)
    print(f"Case-wrap cover: {cover_w:.3f} x {cover_h:.3f} in  ({cw} x {ch} px)")

    pb = Image.open(PAPERBACK).convert("RGB")
    PB_BLEED = 0.125  # paperback source uses 0.125" bleed
    pb_w_in = pb.size[0] / DPI
    pb_spine = pb_w_in - (2 * TRIM_W + 2 * PB_BLEED)  # paperback spine in source
    b = px(PB_BLEED)
    tw, th = px(TRIM_W), px(TRIM_H)
    s_pb = pb.size[0] - 2 * b - 2 * tw  # paperback spine in px

    # Split paperback artwork into back / spine / front at trim size.
    back_art = pb.crop((b, b, b + tw, b + th))
    spine_art = pb.crop((b + tw, b, b + tw + s_pb, b + th))
    front_art = pb.crop((b + tw + s_pb, b, b + 2 * tw + s_pb, b + th))
    print(f"Paperback spine in source: {pb_spine:.4f} in ({s_pb}px)")

    outer = px(OUTER)
    spine_px = px(SPINE)
    back_panel_w = outer + tw          # fore-edge wrap is on the LEFT of back
    front_panel_w = cw - back_panel_w - spine_px  # fore-edge wrap on the RIGHT of front

    # Back panel: trim artwork sits at x=outer (wrap to its left), y=outer.
    back_panel = edge_extend(back_panel_w, ch, back_art, outer, outer)
    # Spine panel: spine artwork stretched to the hardcover spine width, centered vertically.
    spine_panel_art = spine_art.resize((spine_px, th), Image.LANCZOS)
    spine_panel = edge_extend(spine_px, ch, spine_panel_art, 0, outer)
    # Front panel: trim artwork at x=0 (wrap to its right), y=outer.
    front_panel = edge_extend(front_panel_w, ch, front_art, 0, outer)

    canvas = Image.new("RGB", (cw, ch), (255, 255, 255))
    canvas.paste(back_panel, (0, 0))
    canvas.paste(spine_panel, (back_panel_w, 0))
    canvas.paste(front_panel, (back_panel_w + spine_px, 0))

    # Sanity: confirm no blank (pure-white) borders remain.
    arr = np.asarray(canvas)
    mask = (arr.min(axis=2) >= 250)
    rows = np.where((~mask).any(axis=1))[0]
    cols = np.where((~mask).any(axis=0))[0]
    print(f"Content reaches rows {rows[0]}..{rows[-1]} cols {cols[0]}..{cols[-1]} "
          f"(canvas {cw}x{ch}); pure-white share = {mask.mean()*100:.2f}%")

    canvas.save(OUT_PNG, "PNG")
    # IMPORTANT: PDF page size must be in real inches (KDP reads the page size).
    # Earlier versions passed pixel counts as points, producing a ~53"x41" page.
    pdf = FPDF(unit="in", format=(cover_w, cover_h))
    pdf.set_auto_page_break(False)
    pdf.set_margins(0, 0, 0)
    pdf.add_page()
    pdf.image(OUT_PNG, x=0, y=0, w=cover_w, h=cover_h)
    pdf.output(OUT_PDF)
    print(f"Saved: {OUT_PDF}  ({cover_w:.3f} x {cover_h:.3f} in)")


if __name__ == "__main__":
    main()

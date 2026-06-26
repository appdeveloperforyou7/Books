#!/usr/bin/env python3
"""TWO CHAINS - KDP HARDCOVER Cover builder (margin-safe).

The source `Paperback image.png` is a flattened 3-panel spread laid out for the
PAPERBACK cover (back | spine | front), and the paperback version passes KDP.

The hardcover canvas is much larger (0.7085" wrap on all sides + a wider spine).
Simply stretching the whole paperback image across the hardcover canvas (what the
old script did) crushes the safe margins: content that sat 0.716" inside the
paperback trim ends up only ~0.23" inside the hardcover trim -> KDP rejection.

Fix: slice the source at its paperback panel seams and place each panel into the
correct hardcover region:
  * back  + front TRIM panels are placed 1:1 (identical to paperback) -> margins
    are guaranteed identical to the passing paperback (>=0.716" from trim, and
    >=0.4" from the spine).
  * the SPINE panel is stretched to the hardcover spine width only.
  * the 0.7085" wraps are filled from the artwork's own bleed edges.
"""
import os
from PIL import Image
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------------- paths
ROOT = r"D:\Kapil\Books\Meera Desai\MD - Two Chains"
SRC = os.path.join(ROOT, "Output", "Covers", "18Jun26", "Paperback image.png")
OUT_PDF = os.path.join(ROOT, "Output", "TWO_CHAINS_Hardcover_Cover.pdf")
OUT_JPG = os.path.join(ROOT, "Output", "TWO_CHAINS_Hardcover_Cover.jpg")

# ----------------------------------------------------------------- paperback (source)
# The source image is laid out for these paperback dimensions (this is exactly
# what build_cover.py uses, and that version passes KDP).
PB_W, PB_H = 12.0475, 8.75        # paperback full cover incl. 0.125" bleed
PB_BLEED = 0.125
PB_SPINE = 0.7975                 # 319 * 0.0025
PB_TRIM_W, PB_TRIM_H = 5.5, 8.5

# ------------------------------------------------------------------- hardcover target
# KDP-accepted hardcover canvas for 319 pages. Vertical: 8.5 + 2*0.7085 = 9.917.
# Horizontal: 0.7085 + 5.5 + spine + 5.5 + 0.7085 = 13.482  ->  spine = 1.065.
HC_W, HC_H = 13.482, 9.917
HC_WRAP = 0.7085
HC_TRIM_W, HC_TRIM_H = 5.5, 8.5
HC_SPINE = HC_W - 2 * HC_TRIM_W - 2 * HC_WRAP   # = 1.065

DPI = 300
PX_W = round(HC_W * DPI)          # 4045
PX_H = round(HC_H * DPI)          # 2975
pts = lambda v: v * 72


def sx(inch):
    """source x px for a paperback-cover inch offset."""
    return inch * src_w / PB_W


def sy(inch):
    """source y px for a paperback-cover inch offset (top-origin)."""
    return inch * src_h / PB_H


def main():
    global src_w, src_h
    src = Image.open(SRC).convert("RGB")
    src_w, src_h = src.size
    print(f"Source: {src_w} x {src_h}  (paperback {PB_W}\" x {PB_H}\")")
    print(f"Hardcover canvas: {HC_W:.3f}\" x {HC_H:.3f}\" ({PX_W} x {PX_H} px @ {DPI})")
    print(f"  wrap={HC_WRAP:.4f}\"  spine={HC_SPINE:.4f}\"  trim={HC_TRIM_W}\"x{HC_TRIM_H}\"")

    # Paperback panel seams (in inches from the source's left edge).
    pb_back_lo = PB_BLEED                       # 0.125  (start of back trim)
    pb_back_hi = PB_BLEED + PB_TRIM_W           # 5.625  (back trim | spine)
    pb_spin_hi = pb_back_hi + PB_SPINE          # 6.4225 (spine | front trim)
    pb_front_hi = pb_spin_hi + PB_TRIM_W        # 11.9225 (end of front trim)
    pb_v_lo = PB_BLEED                          # 0.125  (top of trim)
    pb_v_hi = PB_BLEED + PB_TRIM_H              # 8.625  (bottom of trim)
    print(f"  paperback seams in: back|spine={pb_back_hi:.4f}  spine|front={pb_spin_hi:.4f}")

    # Hardcover region geometry (inches, top-left origin) -> px.
    hc_left_wrap = round(HC_WRAP * DPI)                              # 213
    hc_trim_wpx = round(HC_TRIM_W * DPI)                             # 1650
    hc_spine_wpx = round(HC_SPINE * DPI)                             # 320
    hc_top_wrap = round(HC_WRAP * DPI)                               # 213
    hc_trim_hpx = round(HC_TRIM_H * DPI)                             # 2550

    back_x = hc_left_wrap                                            # 213
    spine_x = back_x + hc_trim_wpx                                   # 1863
    front_x = spine_x + hc_spine_wpx                                 # 2183
    trim_y = hc_top_wrap                                             # 213

    canvas_img = Image.new("RGB", (PX_W, PX_H), (15, 15, 20))

    # ---- WRAPS (fill first, trimmed panels paste over the centre later) -------
    # Top wrap: source top bleed strip (full source width) stretched across.
    top_strip = src.crop((0, 0, src_w, max(1, round(sy(PB_BLEED)))))
    canvas_img.paste(top_strip.resize((PX_W, hc_top_wrap)), (0, 0))
    # Bottom wrap
    bot_strip = src.crop((0, max(1, round(sy(pb_v_hi))), src_w, src_h))
    canvas_img.paste(bot_strip.resize((PX_W, PX_H - (trim_y + hc_trim_hpx))),
                     (0, trim_y + hc_trim_hpx))
    # Left wrap: source left bleed strip stretched to full canvas height.
    left_strip = src.crop((0, 0, max(1, round(sx(PB_BLEED))), src_h))
    canvas_img.paste(left_strip.resize((hc_left_wrap, PX_H)), (0, 0))
    # Right wrap
    right_strip = src.crop((max(1, round(sx(pb_front_hi + PB_BLEED))), 0, src_w, src_h))
    canvas_img.paste(right_strip.resize((PX_W - (front_x + hc_trim_wpx), PX_H)),
                     (front_x + hc_trim_wpx, 0))

    # ---- SPINE (stretch source spine to hardcover spine width) ----------------
    spine_src = src.crop((round(sx(pb_back_hi)), round(sy(pb_v_lo)),
                          round(sx(pb_spin_hi)), round(sy(pb_v_hi))))
    canvas_img.paste(spine_src.resize((hc_spine_wpx, hc_trim_hpx)),
                     (spine_x, trim_y))

    # ---- BACK TRIM (1:1 with paperback -> identical safe margins) -------------
    back_src = src.crop((round(sx(pb_back_lo)), round(sy(pb_v_lo)),
                         round(sx(pb_back_hi)), round(sy(pb_v_hi))))
    canvas_img.paste(back_src.resize((hc_trim_wpx, hc_trim_hpx)),
                     (back_x, trim_y))

    # ---- FRONT TRIM (1:1 with paperback -> identical safe margins) ------------
    front_src = src.crop((round(sx(pb_spin_hi)), round(sy(pb_v_lo)),
                          round(sx(pb_front_hi)), round(sy(pb_v_hi))))
    canvas_img.paste(front_src.resize((hc_trim_wpx, hc_trim_hpx)),
                     (front_x, trim_y))

    # ---- SAVE JPG -------------------------------------------------------------
    canvas_img.save(OUT_JPG, "JPEG", quality=92, dpi=(DPI, DPI))
    print(f"JPG: {OUT_JPG} ({os.path.getsize(OUT_JPG) // 1024} KB)")

    # ---- SAVE PDF (exact hardcover size) --------------------------------------
    c = canvas.Canvas(OUT_PDF, pagesize=(pts(HC_W), pts(HC_H)))
    c.drawImage(OUT_JPG, 0, 0, pts(HC_W), pts(HC_H), preserveAspectRatio=False)
    c.save()
    print(f"PDF: {OUT_PDF} ({os.path.getsize(OUT_PDF) // 1024} KB)")

    # ---- KDP sanity printout --------------------------------------------------
    print("\n=== KDP HARDCOVER CHECK ===")
    print(f"  Canvas : {HC_W:.3f}\" x {HC_H:.3f}\"")
    print(f"  Wrap   : {HC_WRAP:.4f}\" (all 4 outer edges)")
    print(f"  Spine  : {HC_SPINE:.4f}\"")
    print(f"  Trim   : {HC_TRIM_W}\" x {HC_TRIM_H}\" (back & front, placed 1:1 with paperback)")
    print(f"  Back  trim px: x[{back_x}:{back_x+hc_trim_wpx}] y[{trim_y}:{trim_y+hc_trim_hpx}]")
    print(f"  Spine      px: x[{spine_x}:{spine_x+hc_spine_wpx}]")
    print(f"  Front trim px: x[{front_x}:{front_x+hc_trim_wpx}]")
    print("  Safe margins inherit from the passing paperback (>=0.716\" trim, >=0.4\" spine).")


if __name__ == "__main__":
    main()
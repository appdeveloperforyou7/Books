#!/usr/bin/env python3
"""Build paperback/hardcover PDFs + Kindle image from the wraparound cover.

Trusted method: numpy-split the wraparound into back / spine / front along the
grey vertical separators, then place each panel on its face (no cropping).
Hardcover wraps carry bleed background only, so nothing extends past the trim line.
"""
import io
import os
import numpy as np
from PIL import Image

ROOT = r"D:\Kapil\Books\The Meridian"
SRC = ROOT + r"\Output\Covers\Paperback image New.png"
OUT = ROOT + r"\Output\Covers"
DPI = 300

# Grey separator columns that split back | spine | front (numpy column analysis).
L1, L2 = 670, 812


def in2(v):
    return int(round(v * DPI))


def fit(im, tw, th):
    return im.resize((tw, th), Image.LANCZOS)


def edge_bg(pan):
    a = np.array(pan)
    e = np.concatenate([a[:, 0:8].reshape(-1, 3), a[:, -8:].reshape(-1, 3),
                        a[0:8, :].reshape(-1, 3), a[-8:, :].reshape(-1, 3)])
    return tuple(int(x) for x in np.median(e, axis=0))


img = Image.open(SRC).convert("RGB")
W, H = img.size
arr = np.array(img)
back = Image.fromarray(arr[:, 0:L1])
spine = Image.fromarray(arr[:, L1:L2])
front = Image.fromarray(arr[:, L2:W])
back.save(f"{OUT}\\back.png")
spine.save(f"{OUT}\\spine.png")
front.save(f"{OUT}\\front.png")
print("split: back %dx%d | spine %dx%d | front %dx%d" % (L1, H, L2 - L1, H, W - L2, H))

# Panel edge colours -> seamless bleed/matte fills (used by both formats).
bbg, sbg, fbg = edge_bg(back), edge_bg(spine), edge_bg(front)

TRIM_W, TRIM_H = 5.5, 8.5
trimw, trimh = in2(TRIM_W), in2(TRIM_H)

# --- Paperback (KDP: 5.5x8.5, 191pp white, 0.125" bleed, spine 0.430") ---
# Per-panel placement (same trusted method as hardcover) so the spine lands on
# the real 0.430" paperback spine instead of the wider image-proportion spine.
PB_W, PB_H, PB_BLEED, PB_SPINE_W = 11.680, 8.750, 0.125, 0.430
pbw, pbh = in2(PB_W), in2(PB_H)
bl, spb_w = in2(PB_BLEED), in2(PB_SPINE_W)
pb = Image.new("RGB", (pbw, pbh), bbg)
pb.paste(Image.new("RGB", (bl, pbh), bbg), (0, 0))                       # left bleed
pb.paste(Image.new("RGB", (bl, pbh), fbg), (pbw - bl, 0))                # right bleed
for x0, x1, bg in [(0, bl + trimw, bbg),
                   (bl + trimw, bl + trimw + spb_w, sbg),
                   (bl + trimw + spb_w, pbw, fbg)]:
    pb.paste(Image.new("RGB", (x1 - x0, bl), bg), (x0, 0))               # top bleed
    pb.paste(Image.new("RGB", (x1 - x0, bl), bg), (x0, pbh - bl))        # bottom bleed
pb.paste(Image.new("RGB", (spb_w, pbh), sbg), (bl + trimw, 0))           # spine bg
pb.paste(fit(back, trimw, trimh), (bl, bl))                              # back face (fills)
_psm = in2(0.07)                                                          # spine fold clearance (KDP >=0.0625")
pb.paste(fit(spine, spb_w - 2 * _psm, trimh), (bl + trimw + _psm, bl))   # spine inset from folds
pb.paste(fit(front, trimw, trimh), (bl + trimw + spb_w, bl))             # front face (fills)
pb.save(f"{OUT}\\TheMeridian_Paperback_Cover.pdf", "PDF", resolution=DPI)
pb.save(f"{OUT}\\TheMeridian_Paperback_Preview.png")
print("paperback: 11.680 x 8.750 in | spine 0.430 | per-panel")

# --- Hardcover (KDP case-laminate) ---
HC_W, HC_H = 14.194, 10.417                 # KDP expected cover size
WRAP = (HC_H - TRIM_H) / 2                  # 0.9585"
SPINE = HC_W - 2 * TRIM_W - 2 * WRAP        # 1.2770"
wrap_px, spine_px = in2(WRAP), in2(SPINE)
hcw = wrap_px * 2 + trimw * 2 + spine_px
hch = in2(HC_H)

hc = Image.new("RGB", (hcw, hch), bbg)
# Bleed wraps (fold behind the boards): match the panel behind each strip.
hc.paste(Image.new("RGB", (wrap_px, hch), bbg), (0, 0))            # left wrap
hc.paste(Image.new("RGB", (wrap_px, hch), fbg), (hcw - wrap_px, 0))  # right wrap
for x0, x1, bg in [(0, wrap_px + trimw, bbg),
                   (wrap_px + trimw, wrap_px + trimw + spine_px, sbg),
                   (wrap_px + trimw + spine_px, hcw, fbg)]:
    hc.paste(Image.new("RGB", (x1 - x0, wrap_px), bg), (x0, 0))            # top wrap
    hc.paste(Image.new("RGB", (x1 - x0, wrap_px), bg), (x0, hch - wrap_px))  # bottom wrap
hc.paste(Image.new("RGB", (spine_px, hch), sbg), (wrap_px + trimw, 0))     # spine bg

# Place each panel to FILL its region (resize to fit, no cropping, no matte):
# back/front fill the trim face (full-bleed artwork is allowed to the trim).
# The spine is inset from the folds because KDP REQUIRES >=0.0625" of empty
# space at the spine folds (the grey split-guide lines would otherwise sit on
# the fold and trip the checker). The clearance is filled with the spine's own
# dark bg so it's invisible; the spine text stays well clear of both folds.
hc.paste(fit(back, trimw, trimh), (wrap_px, wrap_px))
_sm = in2(0.125)
hc.paste(fit(spine, spine_px - 2 * _sm, trimh), (wrap_px + trimw + _sm, wrap_px))
hc.paste(fit(front, trimw, trimh), (wrap_px + trimw + spine_px, wrap_px))

# Save as a PDF page of EXACT KDP size.
import fitz
_doc = fitz.open()
_pg = _doc.new_page(width=HC_W * 72, height=HC_H * 72)
_buf = io.BytesIO()
hc.save(_buf, format="JPEG", quality=92)
_buf.seek(0)
_pg.insert_image(_pg.rect, stream=_buf.read())
_doc.save(f"{OUT}\\TheMeridian_Hardcover_Cover.pdf")
hc.save(f"{OUT}\\TheMeridian_Hardcover_Preview.png")
print("hardcover: %.3f x %.3f in (exact) | wrap %.4f | spine %.4f | %dx%d px"
      % (HC_W, HC_H, WRAP, SPINE, hcw, hch))

# --- Kindle cover (front panel only, 1600x2560 JPEG) ---
fit(front, 1600, 2560).save(f"{OUT}\\TheMeridian_Kindle_Cover.jpg", "JPEG", quality=92)
print("kindle: 1600x2560 px")

print("\n=== BUILD COMPLETE ===")
for f in ("back.png", "spine.png", "front.png",
          "TheMeridian_Paperback_Cover.pdf", "TheMeridian_Hardcover_Cover.pdf",
          "TheMeridian_Hardcover_Preview.png", "TheMeridian_Kindle_Cover.jpg"):
    p = os.path.join(OUT, f)
    print("  %-42s %s bytes" % (f, "{:,}".format(os.path.getsize(p)) if os.path.exists(p) else "MISSING"))

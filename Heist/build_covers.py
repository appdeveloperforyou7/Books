#!/usr/bin/env python3
"""Split the NEW wraparound cover and build paperback/hardcover PDFs + Kindle image.
Uses KDP's exact expected dimensions (no cropping — resize only)."""
import numpy as np
from PIL import Image
import os

SRC = r"D:\Kapil\Books\Heist\Output\Covers\Paperback image New.png"
OUT = r"D:\Kapil\Books\Heist\Output\Covers"
DPI = 300

# Grey separator lines (detected via numpy column analysis)
L1, L2 = 670, 812

img = Image.open(SRC).convert("RGB")
W, H = img.size
arr = np.array(img)

# --- split into back / spine / front ---
back  = Image.fromarray(arr[:, 0:L1])
spine = Image.fromarray(arr[:, L1:L2])
front = Image.fromarray(arr[:, L2:W])
back.save(f"{OUT}\\back.png")
spine.save(f"{OUT}\\spine.png")
front.save(f"{OUT}\\front.png")
print("split: back %dx%d | spine %dx%d | front %dx%d" % (L1, H, L2-L1, H, W-L2, H))

def fit(im, tw, th):
    """Resize to exact dimensions (no crop — all content preserved)."""
    return im.resize((tw, th), Image.LANCZOS)

def in2px(inches):
    return int(round(inches * DPI))

# --- Paperback cover (KDP exact: 5.5x8.5 trim, 191pp white, 0.125" bleed) ---
PB_W = in2px(11.680)
PB_H = in2px(8.750)
fit(img, PB_W, PB_H).save(f"{OUT}\\TheMeridian_Paperback_Cover.pdf", "PDF", resolution=DPI)
print("paperback: 11.680 x 8.750 in (%dx%d px)" % (PB_W, PB_H))

# --- Hardcover cover (KDP exact expected dimensions) ---
HC_W = in2px(14.194)
HC_H = in2px(10.417)
fit(img, HC_W, HC_H).save(f"{OUT}\\TheMeridian_Hardcover_Cover.pdf", "PDF", resolution=DPI)
print("hardcover: 14.194 x 10.417 in (%dx%d px)" % (HC_W, HC_H))

# --- Kindle cover (front panel only, 1600x2560 JPEG) ---
fit(front, 1600, 2560).save(f"{OUT}\\TheMeridian_Kindle_Cover.jpg", "JPEG", quality=92)
print("kindle: 1600x2560 px")

print("\n=== BUILD COMPLETE ===")
for f in ("back.png", "spine.png", "front.png",
          "TheMeridian_Paperback_Cover.pdf", "TheMeridian_Hardcover_Cover.pdf",
          "TheMeridian_Kindle_Cover.jpg"):
    p = os.path.join(OUT, f)
    print(f"  {f:38} {os.path.getsize(p):>10,} bytes")

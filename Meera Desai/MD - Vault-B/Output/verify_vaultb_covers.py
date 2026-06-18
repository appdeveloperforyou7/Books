#!/usr/bin/env python3
"""Quick structural + KDP-compatibility verification for generated covers."""
import os
import numpy as np
from PIL import Image
import pikepdf

COVER_DIR = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\Covers"
DPI = 300
TRIM_W, TRIM_H = 5.5, 8.5
SPINE_PB = 257 * 0.0025
SPINE_HC = 257 * 0.002252 + 0.4375
BLEED, WRAP = 0.125, 0.7085
PB_W = BLEED + TRIM_W + SPINE_PB + TRIM_W + BLEED
HC_W = WRAP + TRIM_W + SPINE_HC + TRIM_W + WRAP

print("=== VAULT B Cover Verification ===\n")

# 1. Paperback composite structure
pb = Image.open(os.path.join(COVER_DIR, "VAULT_B_Paperback_Cover.png")).convert("RGB")
arr = np.array(pb)
w, h = pb.size
print(f"Paperback PNG: {w}x{h} px = {w/DPI:.3f}x{h/DPI:.3f} in (expected {PB_W:.3f}x8.750)")
# Back panel occupies left half; spine is the thin middle band; front is right.
# In the composed image: back=(bleed+trim)=5.625", spine=0.6425", front=(trim+bleed)=5.625"
back_r = int((BLEED + TRIM_W) * DPI)
spine_r = back_r + int(round(SPINE_PB * DPI))
back_seg = arr[:, :back_r]
spine_seg = arr[:, back_r:spine_r]
front_seg = arr[:, spine_r:]
print(f"  panels(px): back={back_seg.shape[1]}, spine={spine_seg.shape[1]}, front={front_seg.shape[1]}")
print(f"  mean brightness: back={back_seg.mean():.1f} spine={spine_seg.mean():.1f} front={front_seg.mean():.1f}")
assert abs(spine_seg.shape[1]/DPI - SPINE_PB) < 0.01, "spine width mismatch"
print()

# 2. Hardcover structure
hc = Image.open(os.path.join(COVER_DIR, "VAULT_B_Hardcover_Cover.png")).convert("RGB")
print(f"Hardcover PNG: {hc.size[0]}x{hc.size[1]} px = {hc.size[0]/DPI:.3f}x{hc.size[1]/DPI:.3f} in (expected {HC_W:.3f}x9.917)")
print()

# 3. PDF dimension + resource checks (KDP wants image-based cover, no missing fonts)
for name, exp_w, exp_h in [
    ("VAULT_B_Paperback_Cover.pdf", PB_W, 8.75),
    ("VAULT_B_Hardcover_Cover.pdf", HC_W, 9.917),
]:
    path = os.path.join(COVER_DIR, name)
    pdf = pikepdf.open(path)
    mb = pdf.pages[0].MediaBox
    W = float(mb[2]) / 72
    H = float(mb[3]) / 72
    res = pdf.pages[0].get("/Resources", {}) or {}
    xobjs = res.get("/XObject", {}) or {}
    fonts = res.get("/Font", {}) or {}
    n_imgs = sum(1 for k in xobjs if str(xobjs[k].get("/Subtype")) == "/Image")
    pdf.close()
    ok = abs(W - exp_w) < 0.01 and abs(H - exp_h) < 0.01
    print(f"{'OK' if ok else 'FAIL'} {name}: {W:.4f}x{H:.4f} in | images={n_imgs} | fonts={len(fonts)}")
print()

# 4. Kindle front
kj = Image.open(os.path.join(COVER_DIR, "VAULT_B_Kindle_Cover.jpg"))
r = kj.size[0] / kj.size[1]
print(f"Kindle JPG: {kj.size[0]}x{kj.size[1]} px | ratio={r:.3f} (KDP wants 0.625) | {os.path.getsize(os.path.join(COVER_DIR,'VAULT_B_Kindle_Cover.jpg'))//1024} KB")
print("\nAll verification checks complete.")
#!/usr/bin/env python3
"""Full KDP compliance audit of the Paperback and Hardcover cover PDFs."""
import os
import numpy as np
from PIL import Image
import pikepdf

COVER_DIR = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\Covers"
PB_PDF = os.path.join(COVER_DIR, "VAULT_B_Paperback_Cover.pdf")
PB_PNG = os.path.join(COVER_DIR, "VAULT_B_Paperback_Cover.png")
HC_PDF = os.path.join(COVER_DIR, "VAULT_B_Hardcover_Cover.pdf")
HC_PNG = os.path.join(COVER_DIR, "VAULT_B_Hardcover_Cover.png")

TRIM_W, TRIM_H = 5.5, 8.5
PAGES = 366
BLEED = 0.125
WRAP = 0.7085
SPINE_PB = PAGES * 0.0025            # 0.915
SPINE_HC = PAGES * 0.002252 + 0.4375  # 1.2617
PB_W = BLEED + TRIM_W + SPINE_PB + TRIM_W + BLEED
PB_H = TRIM_H + 2 * BLEED
HC_W = WRAP + TRIM_W + SPINE_HC + TRIM_W + WRAP
HC_H = TRIM_H + 2 * WRAP
DPI = 300
SAFE_PB = 0.25      # paperback safe margin from trim
SAFE_HC_OUT = 0.716 # hardcover outer (wrap)
SAFE_HC_SPINE = 0.40
px = lambda v: int(round(v * DPI))


def pdf_info(path, ew, eh, label):
    pdf = pikepdf.open(path)
    n = len(pdf.pages)
    b = pdf.pages[0].MediaBox
    w, h = float(b[2]) / 72, float(b[3]) / 72
    pdf.close()
    ok = n == 1 and abs(w - ew) < 0.01 and abs(h - eh) < 0.01
    print(f"  {label}: {n} page(s), {w:.4f}x{h:.4f}in (exp {ew:.4f}x{eh:.4f}) "
          f"-> {'OK' if ok else 'FAIL'}")
    return ok


def txt_mask(sub):
    r = sub[:, :, 0].astype(int); g = sub[:, :, 1].astype(int); b = sub[:, :, 2].astype(int)
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
    return (mx > 120) & ((mx - mn > 25) | ((mx > 150) & (mx - mn < 40)))


def wide_cols(mask, min_w=8):
    colsum = mask.sum(axis=0)
    cols = np.where(colsum > 0.02 * mask.shape[0])[0]
    if not cols.size:
        return cols
    groups = np.split(cols, np.where(np.diff(cols) > 3)[0] + 1)
    out = [g for g in groups if (g[-1] - g[0]) >= min_w]
    return np.concatenate(out) if out else np.array([], dtype=int)


print("=" * 64)
print("KDP COMPLIANCE AUDIT")
print("=" * 64)
allok = True

# ---- PAPERBACK ----
print("\n[1] PAPERBACK")
allok &= pdf_info(PB_PDF, PB_W, PB_H, "Paperback PDF")
arr = np.array(Image.open(PB_PNG).convert("RGB")); H, W, _ = arr.shape
ppi = W / PB_W
# trim boxes (inches from left/bottom-origin top-left image)
back_l, back_r = BLEED, BLEED + TRIM_W          # 0.125..5.625
spine_r = back_r + SPINE_PB                     # 6.54
front_l, front_r = spine_r, spine_r + TRIM_W    # 6.54..12.04
yt, yb = BLEED, BLEED + TRIM_H

def panel(name, x0i, x1i, spine_left, spine_safe):
    sub = arr[px(yt):px(yb), px(x0i):px(x1i)]
    lc = wide_cols(txt_mask(sub))
    pw_in = sub.shape[1] / ppi
    if not lc.size:
        print(f"    {name}: no text"); return True
    dL = lc.min() / ppi; dR = (sub.shape[1] - 1 - lc.max()) / ppi
    sd = dL if spine_left else dR
    outer = dR if spine_left else dL
    ok = sd >= spine_safe and outer >= SAFE_PB
    print(f"    {name}: spine={sd:.3f}in(need>={spine_safe}) "
          f"outer={outer:.3f}in(need>={SAFE_PB}) -> {'OK' if ok else 'FAIL'}")
    return ok

print("    (paperback: 0.25in safe from all trim edges, incl. spine side)")
pb_ok = panel("BACK ", back_l, back_r, spine_left=False, spine_safe=SAFE_PB)
pb_ok &= panel("FRONT", front_l, front_r, spine_left=True, spine_safe=SAFE_PB)
allok &= pb_ok

# ---- HARDCOVER ----
print("\n[2] HARDCOVER")
allok &= pdf_info(HC_PDF, HC_W, HC_H, "Hardcover PDF")
arr = np.array(Image.open(HC_PNG).convert("RGB")); H, W, _ = arr.shape
wrap = px(WRAP); tw = px(TRIM_W); th = px(TRIM_H); spw = px(SPINE_HC)
bx0, bx1 = wrap, wrap + tw; yt, yb = wrap, wrap + th
fx0, fx1 = wrap + tw + spw, wrap + tw + spw + tw

def bright(z): return z.reshape(-1, 3).max(axis=1) > 60
print("    (hardcover: clean wrap >=0.716in from outer edges; text >=0.40in from spine)")
hc_ok = True
for nm, zone in [("top wrap", arr[0:yt, bx0:fx1]),
                 ("bottom wrap", arr[yb:H, bx0:fx1]),
                 ("back outer wrap", arr[yt:yb, 0:bx0]),
                 ("front outer wrap", arr[yt:yb, fx1:W])]:
    n = int(bright(zone).sum()); good = n == 0; hc_ok &= good
    print(f"      {nm:<18}: {'clean OK' if good else f'INK {n}px FAIL'}")
lc = wide_cols(txt_mask(arr[yt:yb, bx0:bx1]))
if lc.size:
    sd = (tw - 1 - lc.max()) / DPI; good = sd >= SAFE_HC_SPINE; hc_ok &= good
    print(f"      BACK blurb spine : {sd:.3f}in (need>={SAFE_HC_SPINE}) -> {'OK' if good else 'FAIL'}")
fr = arr[yt:yb, fx0:fx1]
r = fr[:, :, 0].astype(int); g = fr[:, :, 1].astype(int); b = fr[:, :, 2].astype(int)
tf = ((r > 150) & (g > 110) & (g < 215) & (b < 130) & ((r - b) > 60)) | \
     ((r > 180) & (g > 180) & (b > 180) & ((r - g) < 25))
lc = wide_cols(tf)
if lc.size:
    dL = lc.min() / DPI; dR = (tw - 1 - lc.max()) / DPI
    good = dL >= SAFE_HC_SPINE and dR >= SAFE_HC_SPINE; hc_ok &= good
    print(f"      FRONT title spine/outer: {dL:.3f}/{dR:.3f}in (need>={SAFE_HC_SPINE}) -> {'OK' if good else 'FAIL'}")
allok &= hc_ok

print("\n" + "=" * 64)
print(f"OVERALL: {'ALL KDP CHECKS PASS' if allok else 'FAILURES PRESENT - review above'}")
print("=" * 64)

#!/usr/bin/env python3
"""VAULT B - Generate all 3 KDP covers from a single paperback-cover source.

Source : Output/Covers/paperback cover.png  (full wrap: back + spine + front)
Outputs (same folder):
  - VAULT_B_Paperback_Cover.pdf / .png   (trim 5.5x8.5, bleed, cream spine)
  - VAULT_B_Hardcover_Cover.pdf / .png   (trim 5.5x8.5, CLEAN wrap, hardcover spine)
  - VAULT_B_Kindle_Cover.jpg / .png      (front only, 1600x2560)

The hardcover keeps all artwork inside the trim line with a solid wrap, which is
what satisfies KDP's 'no text/graphics beyond the trim line' rule.
"""
import os
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import pikepdf

COVER_DIR = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\Covers"
SRC = os.path.join(COVER_DIR, "paperback cover.png")
OUT_PB     = os.path.join(COVER_DIR, "VAULT_B_Paperback_Cover.pdf")
OUT_PB_PNG = os.path.join(COVER_DIR, "VAULT_B_Paperback_Cover.png")
OUT_HC     = os.path.join(COVER_DIR, "VAULT_B_Hardcover_Cover.pdf")
OUT_HC_PNG = os.path.join(COVER_DIR, "VAULT_B_Hardcover_Cover.png")
OUT_K_JPG  = os.path.join(COVER_DIR, "VAULT_B_Kindle_Cover.jpg")
OUT_K_PNG  = os.path.join(COVER_DIR, "VAULT_B_Kindle_Cover.png")

TRIM_W, TRIM_H = 5.5, 8.5
PAGES = 366
BLEED = 0.125
WRAP = 0.7085                       # KDP hardcover wrap, per side
SPINE_PB = PAGES * 0.0025           # cream paperback: 0.915 in
SPINE_HC = PAGES * 0.002252 + 0.4375  # hardcover: 1.2617 in
DPI = 300
WARM_BLACK = (22, 18, 15)
pts = lambda v: v * 72

PB_W = BLEED + TRIM_W + SPINE_PB + TRIM_W + BLEED
PB_H = TRIM_H + 2 * BLEED
PB_FULL_W = PB_W
HC_W = WRAP + TRIM_W + SPINE_HC + TRIM_W + WRAP
HC_H = TRIM_H + 2 * WRAP


def detect_split_columns(arr):
    h, w, _ = arr.shape
    edge = np.abs(np.diff(arr.astype(np.int32), axis=1)).sum(axis=(0, 2))
    edge = np.pad(edge, (0, 1))
    lo, hi = int(w * 0.20), int(w * 0.80)
    band = edge[lo:hi].copy()
    peaks = []
    while len(peaks) < 2 and band.size:
        p = int(np.argmax(band)); x = p + lo; peaks.append((edge[x], x))
        a, b = max(0, p - 40), min(band.size, p + 41); band[a:b] = 0
    peaks.sort(key=lambda t: t[1])
    return peaks[0][1], peaks[1][1]


def save_pdf(img, path, w_in, h_in):
    tmp = path + ".tmp.jpg"
    img.convert("RGB").save(tmp, "JPEG", quality=95)
    c = canvas.Canvas(path, pagesize=(pts(w_in), pts(h_in)))
    c.drawImage(tmp, 0, 0, pts(w_in), pts(h_in), preserveAspectRatio=False)
    c.showPage(); c.save()
    try: os.remove(tmp)
    except OSError: pass


def build_paperback(back, spine, front):
    pw = int(round(PB_W * DPI)); ph = int(round(PB_H * DPI))
    bw = int(round((BLEED + TRIM_W) * DPI))
    sw = int(round(SPINE_PB * DPI))
    fw = int(round((TRIM_W + BLEED) * DPI))
    full = Image.new("RGB", (pw, ph), WARM_BLACK)
    x = 0
    full.paste(back.resize((bw, ph), Image.LANCZOS), (x, 0));  x += bw
    full.paste(spine.resize((sw, ph), Image.LANCZOS), (x, 0)); x += sw
    full.paste(front.resize((fw, ph), Image.LANCZOS), (x, 0))
    full.save(OUT_PB_PNG, dpi=(DPI, DPI))
    save_pdf(full, OUT_PB, PB_W, PB_H)
    print(f"  Paperback -> {OUT_PB_PNG} ({os.path.getsize(OUT_PB_PNG)//1024} KB)")
    print(f"             {OUT_PB} ({os.path.getsize(OUT_PB)//1024} KB)  [{PB_W:.3f}x{PB_H:.3f}in]")


def build_hardcover(back, spine, front):
    """Build hardcover from the ASSEMBLED paperback (precise trim boundaries),
    not the low-res raw split. Detects the spine in the finished paperback,
    cuts back/spine/front at the trim lines, and reassembles at hardcover size
    with a CLEAN wrap (solid background in the fold zone)."""
    pb = Image.open(OUT_PB_PNG).convert("RGB")
    arr = np.array(pb); sw, sh = pb.size
    ppi = sw / PB_FULL_W
    edge = np.abs(np.diff(arr.astype(np.int32), axis=1)).sum(axis=(0, 2))
    edge = np.pad(edge, (0, 1))
    bs_x = sf_x = None
    for exp_in in (BLEED + TRIM_W, BLEED + TRIM_W + SPINE_PB):
        c = int(round(exp_in * ppi)); lo, hi = c - 60, c + 60
        pk = (lo + int(np.argmax(edge[lo:hi]))) / ppi
        if bs_x is None: bs_x = pk
        else: sf_x = pk
    y0, y1 = BLEED, BLEED + TRIM_H

    def crop_in(a, b):
        return pb.crop((int(round(a * ppi)), int(round(y0 * ppi)),
                        int(round(b * ppi)), int(round(y1 * ppi))))
    back_c  = crop_in(BLEED, bs_x)
    spine_c = crop_in(bs_x, sf_x)
    front_c = crop_in(sf_x, sf_x + TRIM_W)
    print(f"  cut from paperback: back {back_c.size}, spine {spine_c.size}, front {front_c.size}")

    pw = int(round(HC_W * DPI)); ph = int(round(HC_H * DPI))
    tw = int(round(TRIM_W * DPI)); th = int(round(TRIM_H * DPI))
    spw = int(round(SPINE_HC * DPI)); wrap = int(round(WRAP * DPI))
    full = Image.new("RGB", (pw, ph), WARM_BLACK)
    x = wrap
    full.paste(back_c.resize((tw, th), Image.LANCZOS), (x, wrap));  x += tw
    full.paste(spine_c.resize((spw, th), Image.LANCZOS), (x, wrap)); x += spw
    full.paste(front_c.resize((tw, th), Image.LANCZOS), (x, wrap))
    full.save(OUT_HC_PNG, dpi=(DPI, DPI))
    save_pdf(full, OUT_HC, HC_W, HC_H)
    print(f"  Hardcover -> {OUT_HC_PNG} ({os.path.getsize(OUT_HC_PNG)//1024} KB)")
    print(f"             {OUT_HC} ({os.path.getsize(OUT_HC)//1024} KB)  [{HC_W:.3f}x{HC_H:.3f}in]")


def build_kindle(front):
    k = front.convert("RGB").resize((1600, 2560), Image.LANCZOS)
    k.save(OUT_K_JPG, "JPEG", quality=95)
    k.save(OUT_K_PNG, "PNG")
    print(f"  Kindle    -> {OUT_K_JPG} ({os.path.getsize(OUT_K_JPG)//1024} KB)  [1600x2560]")


def verify():
    print("\n=== Verification ===")

    def mb(path, ew, eh):
        pdf = pikepdf.open(path); b = pdf.pages[0].MediaBox; pdf.close()
        w, h = float(b[2]) / 72, float(b[3]) / 72
        ok = abs(w - ew) < 0.01 and abs(h - eh) < 0.01
        print(f"  {os.path.basename(path):<32} {w:.4f}x{h:.4f}in "
              f"(exp {ew:.4f}x{eh:.4f}) {'OK' if ok else 'MISMATCH'}")
        return ok
    mb(OUT_PB, PB_W, PB_H)
    mb(OUT_HC, HC_W, HC_H)
    ki = Image.open(OUT_K_JPG)
    r = ki.size[0] / ki.size[1]
    print(f"  {os.path.basename(OUT_K_JPG):<32} {ki.size[0]}x{ki.size[1]} "
          f"(ratio {r:.3f}, KDP ~0.625) {'OK' if abs(r-0.625)<0.01 else 'CHECK'}")

    # Hardcover KDP margin check
    arr = np.array(Image.open(OUT_HC_PNG).convert("RGB")); H, W, _ = arr.shape
    wrap = int(round(WRAP * DPI)); tw = int(round(TRIM_W * DPI)); th = int(round(TRIM_H * DPI))
    spw = int(round(SPINE_HC * DPI))
    yt, yb = wrap, wrap + th
    bx0, bx1 = wrap, wrap + tw
    fx0, fx1 = wrap + tw + spw, wrap + tw + spw + tw

    def bright(sub): return sub.reshape(-1, 3).max(axis=1) > 60
    def txt(sub):
        r = sub[:, :, 0].astype(int); g = sub[:, :, 1].astype(int); b = sub[:, :, 2].astype(int)
        mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
        return (mx > 120) & ((mx - mn > 25) | ((mx > 150) & (mx - mn < 40)))

    def wide_cols(mask, min_w=8):
        """Columns with ink that belong to a wide (real text) cluster, dropping
        thin vertical seams (e.g. the paste boundary at the spine edge)."""
        colsum = mask.sum(axis=0)
        cols = np.where(colsum > 0.02 * mask.shape[0])[0]
        if not cols.size:
            return cols
        groups = np.split(cols, np.where(np.diff(cols) > 3)[0] + 1)
        out = [g for g in groups if (g[-1] - g[0]) >= min_w]
        return np.concatenate(out) if out else np.array([], dtype=int)

    print("\n  Hardcover KDP margins:")
    ok = True
    for nm, zone in [("top wrap", arr[0:yt, bx0:fx1]),
                     ("bottom wrap", arr[yb:H, bx0:fx1]),
                     ("back outer wrap", arr[yt:yb, 0:bx0]),
                     ("front outer wrap", arr[yt:yb, fx1:W])]:
        n = int(bright(zone).sum()); good = n == 0; ok &= good
        print(f"    {nm:<18}: {'clean OK' if good else f'INK {n}px FAIL'}")
    back = arr[yt:yb, bx0:bx1]
    lc = wide_cols(txt(back))
    if lc.size:
        sd = (back.shape[1] - 1 - lc.max()) / DPI; good = sd >= 0.40; ok &= good
        print(f"    BACK blurb spine dist : {sd:.3f}in ({'OK' if good else 'FAIL'})")
    front = arr[yt:yb, fx0:fx1]
    r = front[:, :, 0].astype(int); g = front[:, :, 1].astype(int); b = front[:, :, 2].astype(int)
    tf = ((r > 150) & (g > 110) & (g < 215) & (b < 130) & ((r - b) > 60)) | \
         ((r > 180) & (g > 180) & (b > 180) & ((r - g) < 25))
    lc = wide_cols(tf)
    if lc.size:
        dL = lc.min() / DPI; dR = (front.shape[1] - 1 - lc.max()) / DPI
        good = dL >= 0.40 and dR >= 0.40; ok &= good
        print(f"    FRONT title spine/outer: {dL:.3f}/{dR:.3f}in ({'OK' if good else 'CHECK'})")
    print(f"\n  Hardcover margins: {'ALL OK' if ok else 'REVIEW NEEDED'}")


def main():
    print("=== VAULT B cover generator (all 3 formats) ===")
    print(f"Source: {SRC}")
    src = Image.open(SRC).convert("RGB"); arr = np.array(src); w, h = src.size
    b_end, s_end = detect_split_columns(arr)
    print(f"  {w}x{h}px  split: back[0:{b_end}] spine[{b_end}:{s_end}] front[{s_end}:{w}]")
    back = src.crop((0, 0, b_end, h))
    spine = src.crop((b_end, 0, s_end, h))
    front = src.crop((s_end, 0, w, h))

    print("\n[1/3] Paperback...")
    build_paperback(back, spine, front)
    print("[2/3] Hardcover...")
    build_hardcover(back, spine, front)
    print("[3/3] Kindle...")
    build_kindle(front)
    verify()
    print("\nDone.")


if __name__ == "__main__":
    main()

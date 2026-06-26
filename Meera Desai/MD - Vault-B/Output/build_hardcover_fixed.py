#!/usr/bin/env python3
"""VAULT B - Fixed KDP hardcover cover.

Source = the approved paperback cover (VAULT_B_Paperback_Cover.png), which is a
full wrap:  [bleed][back 5.5][spine 0.915][front 5.5][bleed] = 12.165 x 8.75 in.

We cut it into back / spine / front at the trim lines, then reassemble at the
KDP HARDCOVER size with a CLEAN wrap (solid background in the fold zone). Keeping
all artwork inside the trim line is what resolves the 'text/graphics beyond the
trim line' rejection. The paperback itself is not modified.

  Hardcover trim  : 5.5 x 8.5 in
  Hardcover spine : 366 * 0.002252 + 0.4375 = 1.2617 in
  Wrap            : 0.7085 in / side (18 mm KDP hardcover wrap)
  Total           : 13.679 x 9.917 in
"""
import os
import numpy as np
from PIL import Image
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import pikepdf

OUT_DIR = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\Covers"
SRC = os.path.join(OUT_DIR, "VAULT_B_Paperback_Cover.png")
OUT_PDF = os.path.join(OUT_DIR, "VAULT_B_Hardcover_Cover.pdf")
OUT_PNG = os.path.join(OUT_DIR, "VAULT_B_Hardcover_Cover.png")

TRIM_W, TRIM_H = 5.5, 8.5
PAGES = 366
WRAP = 0.7085
SPINE = PAGES * 0.002252 + 0.4375          # 1.2617 in (hardcover)
DPI = 300
WARM_BLACK = (22, 18, 15)

# paperback source geometry
PB_BLEED = 0.125
PB_SPINE = 0.915                            # paperback spine (366 * 0.0025)
PB_FULL_W = PB_BLEED + TRIM_W + PB_SPINE + TRIM_W + PB_BLEED   # 12.165
PB_FULL_H = TRIM_H + 2 * PB_BLEED                              # 8.75

FULL_W = WRAP + TRIM_W + SPINE + TRIM_W + WRAP   # 13.679
FULL_H = TRIM_H + 2 * WRAP                        # 9.917


def detect_spine_columns(arr):
    """Find back|spine and spine|front boundaries (INCHES) via horizontal edge energy."""
    h, w, _ = arr.shape
    edge = np.abs(np.diff(arr.astype(np.int32), axis=1)).sum(axis=(0, 2))
    edge = np.pad(edge, (0, 1))
    ppi = w / PB_FULL_W
    out = []
    for exp_in in (PB_BLEED + TRIM_W, PB_BLEED + TRIM_W + PB_SPINE):
        c = int(round(exp_in * ppi)); lo, hi = c - 60, c + 60
        out.append((lo + int(np.argmax(edge[lo:hi]))) / ppi)   # back to inches
    return out[0], out[1], ppi


def build():
    src = Image.open(SRC).convert("RGB")
    arr = np.array(src)
    sw, sh = src.size
    ppi = sw / PB_FULL_W
    back_spine_x, spine_front_x, _ = detect_spine_columns(arr)
    # cut at TRIM boundaries (exclude paperback bleed); make back/front exactly 5.5in
    def crop_in(x0, x1, y0, y1):
        return src.crop((int(round(x0 * ppi)), int(round(y0 * ppi)),
                         int(round(x1 * ppi)), int(round(y1 * ppi))))
    y0, y1 = PB_BLEED, PB_BLEED + TRIM_H
    back  = crop_in(PB_BLEED, back_spine_x, y0, y1)                 # ~5.5in
    spine = crop_in(back_spine_x, spine_front_x, y0, y1)            # ~0.9in
    front = crop_in(spine_front_x, spine_front_x + TRIM_W, y0, y1)  # 5.5in
    print(f"Source: {SRC}")
    print(f"  {sw}x{sh}px @ {ppi:.1f}ppi = {sw/ppi:.3f}x{sh/ppi:.3f}in")
    print(f"  cut: back {back.size}, spine {spine.size}, front {front.size}")

    tw = int(round(TRIM_W * DPI))
    th = int(round(TRIM_H * DPI))
    spw = int(round(SPINE * DPI))
    wrap = int(round(WRAP * DPI))
    fw = wrap + tw + spw + tw + wrap
    fh = wrap + th + wrap

    full = Image.new("RGB", (fw, fh), WARM_BLACK)
    x = wrap
    full.paste(back.resize((tw, th), Image.LANCZOS), (x, wrap));  x += tw
    full.paste(spine.resize((spw, th), Image.LANCZOS), (x, wrap)); x += spw
    full.paste(front.resize((tw, th), Image.LANCZOS), (x, wrap))

    full.save(OUT_PNG, dpi=(DPI, DPI))

    tmp = OUT_PDF + ".tmp.png"
    full.save(tmp, "PNG", dpi=(DPI, DPI))
    c = canvas.Canvas(OUT_PDF, pagesize=(FULL_W * inch, FULL_H * inch))
    c.drawImage(tmp, 0, 0, width=FULL_W * inch, height=FULL_H * inch,
                preserveAspectRatio=False)
    c.showPage(); c.save()
    os.remove(tmp)

    print(f"Built: {OUT_PNG} ({os.path.getsize(OUT_PNG)//1024} KB)")
    print(f"Built: {OUT_PDF} ({os.path.getsize(OUT_PDF)//1024} KB)")
    print(f"PX   : {fw}x{fh} = {fw/DPI:.3f}x{fh/DPI:.3f} in")
    return full


def verify():
    pdf = pikepdf.open(OUT_PDF)
    mb = pdf.pages[0].MediaBox
    w, h = float(mb[2]) / 72, float(mb[3]) / 72
    pdf.close()
    print(f"\nPDF MediaBox: {w:.4f} x {h:.4f} in "
          f"(expected {FULL_W:.4f} x {FULL_H:.4f}) -> "
          f"{'OK' if abs(w-FULL_W)<0.01 and abs(h-FULL_H)<0.01 else 'MISMATCH'}")

    arr = np.array(Image.open(OUT_PNG).convert("RGB"))
    H, W, _ = arr.shape
    inches = lambda v: v / DPI
    # exact integer pixel layout used by build()
    wrap = int(round(WRAP * DPI))
    tw = int(round(TRIM_W * DPI)); th = int(round(TRIM_H * DPI))
    spw = int(round(SPINE * DPI))
    back_x0, back_x1 = wrap, wrap + tw
    spine_x0, spine_x1 = back_x1, back_x1 + spw
    front_x0, front_x1 = spine_x1, spine_x1 + tw
    yt, yb = wrap, wrap + th

    def txt(sub):
        r = sub[:, :, 0].astype(int); g = sub[:, :, 1].astype(int); b = sub[:, :, 2].astype(int)
        mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
        return (mx > 120) & ((mx - mn > 25) | ((mx > 150) & (mx - mn < 40)))

    def bright(sub):  # any pixel clearly not the warm-black wrap background
        return sub.reshape(-1, 3).max(axis=1) > 60

    print("\nKDP checks (>=0.716in from outer edges = clean wrap; >=0.40in text from spine):")
    all_ok = True

    # 1) WRAP ZONES must be clean (this is the actual fix for 'beyond trim line')
    wrap_zones = [
        ("top wrap",        arr[0:yt, back_x0:front_x1]),
        ("bottom wrap",     arr[yb:H, back_x0:front_x1]),
        ("back outer wrap", arr[yt:yb, 0:back_x0]),
        ("front outer wrap",arr[yt:yb, front_x1:W]),
    ]
    print("  Wrap zones (must be clean background):")
    for nm, zone in wrap_zones:
        n = int(bright(zone).sum())
        ok = n == 0
        all_ok &= ok
        print(f"    {nm:<18}: {'clean OK' if ok else f'INK {n}px FAIL'}")

    # 2) BACK blurb text distance from spine (measure solid letter columns,
    #    not sparse anti-alias speckle)
    back = arr[yt:yb, back_x0:back_x1]; m = txt(back)
    colsum = m.sum(axis=0)
    letter_cols = np.where(colsum > 0.02 * back.shape[0])[0]
    if letter_cols.size:
        sd = inches(back.shape[1] - 1 - letter_cols.max())  # spine on the right
        ok = sd >= 0.40; all_ok &= ok
        print(f"  BACK blurb text spine distance: {sd:.3f}in ({'OK' if ok else 'FAIL <0.40'})")

    # 3) FRONT: illustrated (full-bleed) cover -> art bleeding to trim is correct.
    #    Verify the actual TITLE/AUTHOR letter strokes (dense gold/white columns)
    #    are clear of the spine and outer edges. Scattered gold art detail is not text.
    front = arr[yt:yb, front_x0:front_x1]
    r = front[:, :, 0].astype(int); g = front[:, :, 1].astype(int); b = front[:, :, 2].astype(int)
    gold = (r > 150) & (g > 110) & (g < 215) & (b < 130) & ((r - b) > 60)
    white = (r > 180) & (g > 180) & (b > 180) & ((r - g) < 25)
    tf = gold | white

    def letter_margins(name, y0, y1, thr):
        sub = tf[y0:y1]
        cols = np.where(sub.sum(axis=0) > thr * sub.shape[0])[0]
        if not cols.size:
            print(f"  FRONT {name}: no dense letters detected"); return True
        dL = cols.min() / DPI            # spine is on the left
        dR = (front.shape[1] - 1 - cols.max()) / DPI
        ok = dL >= 0.40 and dR >= 0.40
        print(f"  FRONT {name}: spine={dL:.3f}in outer={dR:.3f}in "
              f"({'OK' if ok else 'FAIL'})")
        return ok

    # title sits roughly in upper-middle; author near bottom (auto-locate densest bands)
    rowdens = tf.sum(axis=1) / front.shape[1]
    dense_rows = np.where(rowdens > 0.04)[0]
    if dense_rows.size:
        # split dense rows into clusters, take top (title) and bottom (author)
        gaps = np.where(np.diff(dense_rows) > 40)[0]
        starts = np.concatenate(([dense_rows[0]], dense_rows[gaps + 1]))
        ends = np.concatenate((dense_rows[gaps], [dense_rows[-1]]))
        bands = sorted(zip(ends - starts, starts, ends), reverse=True)
        for i, (_, s, e) in enumerate(bands[:2]):
            letter_margins("title" if i == 0 else "author", s, e + 1, 0.12)
            all_ok &= letter_margins("title" if i == 0 else "author", s, e + 1, 0.12)
    print("    (illustrated artwork bleeds to trim edge = correct full-bleed, not flagged)")

    print(f"\nRESULT: {'ALL CHECKS PASS' if all_ok else 'CHECK FAILURES ABOVE'}")
    return all_ok


if __name__ == "__main__":
    print(f"Spine={SPINE:.4f}in  Wrap={WRAP:.4f}in  Total={FULL_W:.4f}x{FULL_H:.4f}in")
    build()
    verify()

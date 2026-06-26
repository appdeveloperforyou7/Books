#!/usr/bin/env python3
"""VAULT B - KDP Cover Generator v3 (Paperback + Hardcover + Kindle front)."""
import os
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
import pikepdf

COVER_DIR = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\Covers"
SRC_IMG   = os.path.join(COVER_DIR, "paperback cover jpg.jpg")
OUT_PB    = os.path.join(COVER_DIR, "VAULT_B_Paperback_Cover.pdf")
OUT_HC    = os.path.join(COVER_DIR, "VAULT_B_Hardcover_Cover.pdf")
OUT_PB_PNG = os.path.join(COVER_DIR, "VAULT_B_Paperback_Cover.png")
OUT_HC_PNG = os.path.join(COVER_DIR, "VAULT_B_Hardcover_Cover.png")
OUT_KINDLE_JPG = os.path.join(COVER_DIR, "VAULT_B_Kindle_Cover.jpg")
OUT_KINDLE_PNG = os.path.join(COVER_DIR, "VAULT_B_Kindle_Cover.png")

TRIM_W, TRIM_H = 5.5, 8.5
PAGES = 366
BLEED = 0.125
WRAP  = 0.7085
SPINE_PB = PAGES * 0.0025
SPINE_HC = PAGES * 0.002252 + 0.4375
PB_W = BLEED + TRIM_W + SPINE_PB + TRIM_W + BLEED
PB_H = BLEED + TRIM_H + BLEED
HC_W = WRAP + TRIM_W + SPINE_HC + TRIM_W + WRAP
HC_H = TRIM_H + 2 * WRAP
DPI = 300
pts = lambda v: v * 72


def detect_split_columns(arr):
    h, w, _ = arr.shape
    edge = np.abs(np.diff(arr.astype(np.int32), axis=1)).sum(axis=(0, 2))
    edge = np.pad(edge, (0, 1))
    lo, hi = int(w * 0.20), int(w * 0.80)
    band = edge[lo:hi].copy()
    peaks = []
    while len(peaks) < 2 and band.size:
        p = int(np.argmax(band))
        x = p + lo
        peaks.append((edge[x], x))
        a = max(0, p - 40); b = min(band.size, p + 41)
        band[a:b] = 0
    peaks.sort(key=lambda t: t[1])
    back_end, spine_end = peaks[0][1], peaks[1][1]
    return back_end, spine_end, edge


def build_canvas(back_img, spine_img, front_img, full_w_in, full_h_in,
                 back_w_in, spine_w_in, front_w_in, out_pdf, out_png,
                 background=(15, 12, 10)):
    px_w = int(round(full_w_in * DPI))
    px_h = int(round(full_h_in * DPI))
    canvas_px = Image.new("RGB", (px_w, px_h), background)
    bh = px_h
    bw = int(round(back_w_in * DPI))
    sw = int(round(spine_w_in * DPI))
    fw = int(round(front_w_in * DPI))
    x = 0
    canvas_px.paste(back_img.resize((bw, bh), Image.LANCZOS), (x, 0));  x += bw
    canvas_px.paste(spine_img.resize((sw, bh), Image.LANCZOS), (x, 0)); x += sw
    canvas_px.paste(front_img.resize((fw, bh), Image.LANCZOS), (x, 0))
    canvas_px.save(out_png, dpi=(DPI, DPI))
    tmp_jpg = out_pdf + ".tmp.jpg"
    canvas_px.convert("RGB").save(tmp_jpg, "JPEG", quality=95)
    c = canvas.Canvas(out_pdf, pagesize=(pts(full_w_in), pts(full_h_in)))
    c.drawImage(tmp_jpg, 0, 0, pts(full_w_in), pts(full_h_in), preserveAspectRatio=False)
    c.showPage(); c.save()
    try: os.remove(tmp_jpg)
    except OSError: pass
    return canvas_px


def make_kindle_front(front_img, out_jpg, out_png, target=(1600, 2560)):
    """Single cut at spine separator -> full front panel -> direct resize.
    No padding, no gradient, no blur. Entire front artwork kept."""
    final = front_img.convert("RGB").resize(target, Image.LANCZOS)
    final.save(out_jpg, "JPEG", quality=95)
    final.save(out_png, "PNG")
    return final


def verify_pdf(path, expect_w, expect_h):
    pdf = pikepdf.open(path)
    mb = pdf.pages[0].MediaBox
    w = float(mb[2]) / 72; h = float(mb[3]) / 72
    pdf.close()
    ok_w = abs(w - expect_w) < 0.01
    ok_h = abs(h - expect_h) < 0.01
    tag = "OK " if (ok_w and ok_h) else "!! "
    print(f"  {tag}{os.path.basename(path)}: {w:.4f} x {h:.4f} in "
          f"(expected {expect_w:.4f} x {expect_h:.4f})")
    return ok_w and ok_h


def main():
    print("=== VAULT B Cover Generator v3 ===")
    print(f"Trim: {TRIM_W} x {TRIM_H} in | Pages: {PAGES}")
    print(f"Paperback spine: {SPINE_PB:.4f} in -> {PB_W:.4f} x {PB_H:.4f} in")
    print(f"Hardcover spine: {SPINE_HC:.4f} in -> {HC_W:.4f} x {HC_H:.4f} in")
    print()

    src = Image.open(SRC_IMG).convert("RGB")
    arr = np.array(src)
    sw_px, sh_px = src.size
    back_end, spine_end, _ = detect_split_columns(arr)
    print(f"Source image: {sw_px} x {sh_px} px")
    print(f"Detected split lines: back|spine @ x={back_end},  spine|front @ x={spine_end}")
    print(f"  -> back=0:{back_end} ({back_end}px), "
          f"spine={back_end}:{spine_end} ({spine_end-back_end}px), "
          f"front={spine_end}:{sw_px} ({sw_px-spine_end}px)")
    print()

    back_img  = src.crop((0, 0, back_end, sh_px))
    spine_img = src.crop((back_end, 0, spine_end, sh_px))
    front_img = src.crop((spine_end, 0, sw_px, sh_px))

    print("[1/3] Paperback cover...")
    build_canvas(back_img, spine_img, front_img, PB_W, PB_H,
                 BLEED + TRIM_W, SPINE_PB, TRIM_W + BLEED, OUT_PB, OUT_PB_PNG)
    print(f"  PDF: {os.path.getsize(OUT_PB)//1024} KB | PNG: {os.path.getsize(OUT_PB_PNG)//1024} KB")

    print("[2/3] Hardcover cover...")
    build_canvas(back_img, spine_img, front_img, HC_W, HC_H,
                 WRAP + TRIM_W, SPINE_HC, TRIM_W + WRAP, OUT_HC, OUT_HC_PNG)
    print(f"  PDF: {os.path.getsize(OUT_HC)//1024} KB | PNG: {os.path.getsize(OUT_HC_PNG)//1024} KB")

    print("[3/3] Kindle front image (single spine cut, direct resize)...")
    make_kindle_front(front_img, OUT_KINDLE_JPG, OUT_KINDLE_PNG)
    print(f"  JPG: {os.path.getsize(OUT_KINDLE_JPG)//1024} KB | PNG: {os.path.getsize(OUT_KINDLE_PNG)//1024} KB")
    print()

    print("=== Verification ===")
    verify_pdf(OUT_PB, PB_W, PB_H)
    verify_pdf(OUT_HC, HC_W, HC_H)
    ki = Image.open(OUT_KINDLE_JPG)
    print(f"  Kindle JPG: {ki.size[0]} x {ki.size[1]} px "
          f"(ratio {ki.size[0]/ki.size[1]:.3f}, KDP wants ~0.625)")
    print("\nDone.")


if __name__ == "__main__":
    main()
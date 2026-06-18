#!/usr/bin/env python3
"""VAULT B - KDP Cover Generator (Paperback + Hardcover + Kindle front).

Source image is a full 3-part spread (back | spine | front). We use numpy to
detect the two vertical split lines, crop the three regions, and resize each
independently so the final spine width matches the book's ACTUAL page count
(important: simply stretching the whole image would distort the spine).

Page count is taken from the current interior: VAULT_B_Interior_v3.pdf = 257 pp.
"""
import os
import numpy as np
from PIL import Image
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import pikepdf

# --- Paths -------------------------------------------------------------------
COVER_DIR = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\Covers"
SRC_IMG   = os.path.join(COVER_DIR, "paperback cover jpg.jpg")
OUT_PB    = os.path.join(COVER_DIR, "VAULT_B_Paperback_Cover.pdf")
OUT_HC    = os.path.join(COVER_DIR, "VAULT_B_Hardcover_Cover.pdf")
OUT_PB_PNG = os.path.join(COVER_DIR, "VAULT_B_Paperback_Cover.png")
OUT_HC_PNG = os.path.join(COVER_DIR, "VAULT_B_Hardcover_Cover.png")
OUT_KINDLE_JPG = os.path.join(COVER_DIR, "VAULT_B_Kindle_Cover.jpg")
OUT_KINDLE_PNG = os.path.join(COVER_DIR, "VAULT_B_Kindle_Cover.png")

# --- Book / KDP spec ---------------------------------------------------------
TRIM_W, TRIM_H = 5.5, 8.5          # inches
PAGES          = 257               # current interior (VAULT_B_Interior_v3.pdf)
BLEED          = 0.125             # paperback bleed
WRAP           = 0.7085            # hardcover wrap per side (KDP)

# Spine formulas (match Two Chains verified covers + repo convention)
SPINE_PB = PAGES * 0.0025                       # black-ink paperback
SPINE_HC = PAGES * 0.002252 + 0.4375            # white-paper hardcover w/ board

# Full canvas sizes
PB_W = BLEED + TRIM_W + SPINE_PB + TRIM_W + BLEED
PB_H = BLEED + TRIM_H + BLEED
HC_W = WRAP + TRIM_W + SPINE_HC + TRIM_W + WRAP
HC_H = TRIM_H + 2 * WRAP

DPI = 300
pts = lambda v: v * 72


def detect_split_columns(arr):
    """Return (back_end, spine_end) x-coords via vertical edge magnitude.

    Computes per-column total absolute difference between adjacent columns
    (strong where artwork changes sharply at panel boundaries), then picks the
    two strongest peaks separated by at least 40 px, ignoring the outer 5%
    borders. This is the 'vertical split lines' detection step.
    """
    h, w, _ = arr.shape
    edge = np.abs(np.diff(arr.astype(np.int32), axis=1)).sum(axis=(0, 2))
    edge = np.pad(edge, (0, 1))                      # restore width w
    lo, hi = int(w * 0.20), int(w * 0.80)            # interior band only
    band = edge[lo:hi].copy()
    peaks = []
    while len(peaks) < 2 and band.size:
        p = int(np.argmax(band))
        x = p + lo
        peaks.append((edge[x], x))
        # suppress a neighborhood so the next peak is a different boundary
        a = max(0, p - 40); b = min(band.size, p + 41)
        band[a:b] = 0
    peaks.sort(key=lambda t: t[1])                   # left-to-right
    back_end, spine_end = peaks[0][1], peaks[1][1]
    return back_end, spine_end, edge


def build_canvas(back_img, spine_img, front_img, full_w_in, full_h_in,
                 back_w_in, spine_w_in, front_w_in, out_pdf, out_png,
                 background=(15, 12, 10)):
    """Composite the three independently-resized regions into a full cover."""
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

    # Embed into a PDF at the exact KDP point dimensions
    tmp_jpg = out_pdf + ".tmp.jpg"
    canvas_px.convert("RGB").save(tmp_jpg, "JPEG", quality=95)
    c = canvas.Canvas(out_pdf, pagesize=(pts(full_w_in), pts(full_h_in)))
    c.drawImage(tmp_jpg, 0, 0, pts(full_w_in), pts(full_h_in),
                preserveAspectRatio=False)
    c.showPage(); c.save()
    try: os.remove(tmp_jpg)
    except OSError: pass
    return canvas_px


def gradient_extend(edge_strip, pad, fade=0.75):
    """Extend an edge outward as a smooth per-column gradient (no mirroring).

    edge_strip: HxWx3 numpy array of the real artwork's edge rows (top or bottom).
    pad: number of new rows to synthesize.
    fade: how much darker the outer edge becomes vs the seam (0=same, 1=black).
    Returns pad x W x3 uint8 extension that tonally continues the edge, with no
    flipped content.
    """
    h, w, _ = edge_strip.shape
    col_color = edge_strip.astype(np.float32).mean(axis=0)   # per-column seam color (Wx3)
    outer = col_color * (1.0 - fade)                          # outer color darkened toward black
    ext = np.empty((pad, w, 3), dtype=np.float32)
    for i in range(pad):
        t = i / max(1, pad - 1)                               # 0 at seam -> 1 at outer edge
        ext[i] = col_color * (1 - t) + outer * t
    return ext.astype(np.uint8)


def feather_blend(base, ext, is_top, seam_rows=12):
    """Feather the seam so the extension merges into the artwork smoothly."""
    if is_top:
        real = base[:seam_rows].astype(np.float32)
        ext_edge = ext[-seam_rows:][::-1].astype(np.float32)
    else:
        real = base[-seam_rows:].astype(np.float32)
        ext_edge = ext[:seam_rows][::-1].astype(np.float32)
    blend = (real * 0.5 + ext_edge * 0.5).astype(np.uint8)
    out = ext.copy()
    if is_top:
        out[-seam_rows:] = blend
    else:
        out[:seam_rows] = blend
    return out


def make_kindle_front(front_img, out_jpg, out_png, target=(1600, 2560)):
    """Build the Kindle front cover keeping the ENTIRE front panel.

    The front panel is isolated by the single vertical cut at the spine
    separator (no horizontal trimming of the artwork). Its native ratio (~0.71)
    is wider than Kindle's 0.625, so we reach the target ratio by adding height
    instead of cutting width: every pixel of the front artwork is preserved.

    The added height is a per-column gradient extension sampled from each edge's
    real color (warm-brown at top, near-black at bottom), faded smoothly outward
    and feathered at the seam. This continues the cover's tonal flow with NO
    mirrored/flipped content.
    """
    fw, fh = front_img.size
    ratio = target[0] / target[1]
    needed_h = int(round(fw / ratio))
    pad_total = max(0, needed_h - fh)
    pad_top = pad_total // 2
    pad_bot = pad_total - pad_top

    arr = np.array(front_img.convert("RGB"))

    if pad_total == 0:
        new_h = int(round(fw / ratio))
        off = (fh - new_h) // 2
        final = front_img.crop((0, off, fw, off + new_h)).resize(target, Image.LANCZOS)
    else:
        sample = 10  # rows to sample for edge color
        top_ext = gradient_extend(arr[:sample], pad_top, fade=0.75)
        bot_ext = gradient_extend(arr[-sample:], pad_bot, fade=0.80)
        top_ext = feather_blend(arr, top_ext, is_top=True)
        bot_ext = feather_blend(arr, bot_ext, is_top=False)
        composed = np.concatenate([top_ext, arr, bot_ext], axis=0)
        final = Image.fromarray(composed).resize(target, Image.LANCZOS)

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
    print("=== VAULT B Cover Generator ===")
    print(f"Trim: {TRIM_W} x {TRIM_H} in | Pages: {PAGES}")
    print(f"Paperback spine: {SPINE_PB:.4f} in -> {PB_W:.4f} x {PB_H:.4f} in")
    print(f"Hardcover spine: {SPINE_HC:.4f} in -> {HC_W:.4f} x {HC_H:.4f} in")
    print()

    # -- Load source + detect splits ------------------------------------------
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

    back_img   = src.crop((0, 0, back_end, sh_px))
    spine_img  = src.crop((back_end, 0, spine_end, sh_px))
    front_img  = src.crop((spine_end, 0, sw_px, sh_px))

    # -- 1. Paperback ----------------------------------------------------------
    print("[1/3] Paperback cover...")
    build_canvas(back_img, spine_img, front_img,
                 PB_W, PB_H,
                 BLEED + TRIM_W, SPINE_PB, TRIM_W + BLEED,
                 OUT_PB, OUT_PB_PNG)
    print(f"  PDF: {os.path.getsize(OUT_PB)//1024} KB | PNG: {os.path.getsize(OUT_PB_PNG)//1024} KB")

    # -- 2. Hardcover ----------------------------------------------------------
    print("[2/3] Hardcover cover...")
    build_canvas(back_img, spine_img, front_img,
                 HC_W, HC_H,
                 WRAP + TRIM_W, SPINE_HC, TRIM_W + WRAP,
                 OUT_HC, OUT_HC_PNG)
    print(f"  PDF: {os.path.getsize(OUT_HC)//1024} KB | PNG: {os.path.getsize(OUT_HC_PNG)//1024} KB")

    # -- 3. Kindle front -------------------------------------------------------
    print("[3/3] Kindle front image...")
    make_kindle_front(front_img, OUT_KINDLE_JPG, OUT_KINDLE_PNG)
    print(f"  JPG: {os.path.getsize(OUT_KINDLE_JPG)//1024} KB | PNG: {os.path.getsize(OUT_KINDLE_PNG)//1024} KB")
    print()

    # -- Verify ----------------------------------------------------------------
    print("=== Verification ===")
    verify_pdf(OUT_PB, PB_W, PB_H)
    verify_pdf(OUT_HC, HC_W, HC_H)
    ki = Image.open(OUT_KINDLE_JPG)
    print(f"  Kindle JPG: {ki.size[0]} x {ki.size[1]} px "
          f"(ratio {ki.size[0]/ki.size[1]:.3f}, KDP wants ~0.625)")
    print("\nDone.")


if __name__ == "__main__":
    main()
"""
Vault B — KDP Cover Generator
Splits 'Vault B image.png' into back/spine/front using Sobel edge detection,
then generates all 3 KDP formats: Kindle, Paperback, Hardcover.
"""

import os
import numpy as np
import cv2
from PIL import Image, ImageEnhance
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = r"D:\Kapil\Books\Meera Desai\Covers\VAULT_B"
SOURCE_IMG = os.path.join(BASE, "Vault B image.png")
OUTPUT_DIR = BASE
ARTWORK_DIR = os.path.join(BASE, "artwork")
FONTS_DIR = r"C:\Windows\Fonts"

TRIM_W, TRIM_H = 5.5, 8.5
DPI = 300
BLEED = 0.125

PAGES = 366
SPINE_PB = PAGES * 0.0025           # cream paper: 366 * 0.0025 = 0.915"
SPINE_HC = PAGES * 0.002252 + 0.288 # hardcover formula: 366 * 0.002252 + 0.288 = 1.112"

WARM_BLACK = (22, 18, 15)


def register_fonts():
    for name, file in [("Georgia", "georgia.ttf"), ("GeorgiaBold", "georgiab.ttf"),
                        ("GeorgiaItalic", "georgiai.ttf"), ("Constan", "constan.ttf")]:
        path = os.path.join(FONTS_DIR, file)
        if os.path.isfile(path):
            pdfmetrics.registerFont(TTFont(name, path))


def detect_split_lines():
    cv_img = cv2.imread(SOURCE_IMG)
    h, w = cv_img.shape[:2]
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_energy = np.sum(np.abs(grad_x), axis=0)
    grad_norm = grad_energy / grad_energy.max()
    ranked = np.argsort(grad_norm)[::-1]
    used = []
    for x in ranked:
        if all(abs(x - u) > 50 for u in used):
            used.append(int(x))
            if len(used) == 2:
                break
    used.sort()
    print(f"  Split lines: x={used[0]}, x={used[1]}")
    return cv_img, used[0], used[1]


def split_source():
    cv_img, spine_start, spine_end = detect_split_lines()
    back_cv = cv_img[:, :spine_start]
    spine_cv = cv_img[:, spine_start:spine_end]
    front_cv = cv_img[:, spine_end:]
    back = Image.fromarray(cv2.cvtColor(back_cv, cv2.COLOR_BGR2RGB))
    spine = Image.fromarray(cv2.cvtColor(spine_cv, cv2.COLOR_BGR2RGB))
    front = Image.fromarray(cv2.cvtColor(front_cv, cv2.COLOR_BGR2RGB))
    print(f"  Sections: back={back.size}, spine={spine.size}, front={front.size}")
    os.makedirs(ARTWORK_DIR, exist_ok=True)
    back.save(os.path.join(ARTWORK_DIR, "split_back.png"))
    spine.save(os.path.join(ARTWORK_DIR, "split_spine.png"))
    front.save(os.path.join(ARTWORK_DIR, "split_front.png"))
    return back, spine, front


def save_pdf(img, path, w_in, h_in):
    tmp = os.path.join(OUTPUT_DIR, "_cover_temp.png")
    img.save(tmp, "PNG", dpi=(DPI, DPI))
    register_fonts()
    c = canvas.Canvas(path, pagesize=(w_in * inch, h_in * inch))
    c.drawImage(tmp, 0, 0, width=w_in * inch, height=h_in * inch)
    c.showPage()
    c.save()
    os.remove(tmp)


def build_kindle():
    print("\n=== Kindle ===")
    _, _, front = split_source()
    kindle_w, kindle_h = 1600, 2560
    front = front.resize((kindle_w, kindle_h), Image.LANCZOS)
    front = ImageEnhance.Sharpness(front).enhance(1.1)
    out = os.path.join(OUTPUT_DIR, "VAULT_B_Kindle.jpg")
    front.save(out, "JPEG", quality=95)
    print(f"  -> {out} ({os.path.getsize(out) // 1024} KB)")


def build_paperback():
    print("\n=== Paperback ===")
    back, spine, front = split_source()

    trim_w = int(TRIM_W * DPI)
    trim_h = int(TRIM_H * DPI)
    bleed = int(BLEED * DPI)
    sp_w = int(SPINE_PB * DPI)

    back_w = trim_w + bleed
    front_w = trim_w + bleed
    total_w = back_w + sp_w + front_w
    total_h = trim_h + 2 * bleed

    print(f"  Back={back_w}x{total_h}, Spine={sp_w}x{total_h}, Front={front_w}x{total_h}")
    print(f"  Total: {total_w / DPI:.3f}\" x {total_h / DPI:.3f}\" ({total_w}x{total_h}px)")

    full = Image.new("RGB", (total_w, total_h))
    full.paste(back.resize((back_w, total_h), Image.LANCZOS), (0, 0))
    full.paste(spine.resize((sp_w, total_h), Image.LANCZOS), (back_w, 0))
    full.paste(front.resize((front_w, total_h), Image.LANCZOS), (back_w + sp_w, 0))

    # Force exact KDP dimensions regardless of pixel rounding
    exact_w = BLEED + TRIM_W + SPINE_PB + TRIM_W + BLEED  # = 12.165
    exact_h = TRIM_H + 2 * BLEED                           # = 8.750
    pdf = os.path.join(OUTPUT_DIR, "VAULT_B_Paperback.pdf")
    save_pdf(full, pdf, exact_w, exact_h)
    full.save(os.path.join(OUTPUT_DIR, "VAULT_B_Paperback.png"), dpi=(DPI, DPI))
    print(f"  -> {pdf} ({os.path.getsize(pdf) // 1024} KB)")


def build_hardcover():
    print("\n=== Hardcover ===")
    back, spine, front = split_source()

    trim_w = int(TRIM_W * DPI)
    trim_h = int(TRIM_H * DPI)
    sp_w = int(round(SPINE_HC * DPI))
    wrap = int(round(0.625 * DPI))

    back_w = trim_w + wrap
    front_w = trim_w + wrap
    total_w = back_w + sp_w + front_w
    total_h = trim_h + 2 * wrap

    print(f"  Back trim={trim_w}x{trim_h}, Spine={sp_w}x{trim_h}, Front trim={trim_w}x{trim_h}")
    print(f"  Wrap={wrap}px, Total: {total_w / DPI:.3f}\" x {total_h / DPI:.3f}\" ({total_w}x{total_h}px)")

    full = Image.new("RGB", (total_w, total_h), WARM_BLACK)
    full.paste(back.resize((trim_w, trim_h), Image.LANCZOS), (wrap, wrap))
    full.paste(spine.resize((sp_w, trim_h), Image.LANCZOS), (back_w, wrap))
    full.paste(front.resize((trim_w, trim_h), Image.LANCZOS), (back_w + sp_w, wrap))

    # Force exact KDP dimensions
    exact_hc_w = 0.625 + TRIM_W + SPINE_HC + TRIM_W + 0.625
    exact_hc_h = TRIM_H + 2 * 0.625
    pdf = os.path.join(OUTPUT_DIR, "VAULT_B_Hardcover.pdf")
    save_pdf(full, pdf, exact_hc_w, exact_hc_h)
    full.save(os.path.join(OUTPUT_DIR, "VAULT_B_Hardcover.png"), dpi=(DPI, DPI))
    print(f"  -> {pdf} ({os.path.getsize(pdf) // 1024} KB)")


if __name__ == "__main__":
    print("=" * 60)
    print("VAULT B — KDP Cover Generator")
    print("=" * 60)
    print(f"  Trim: {TRIM_W}\" x {TRIM_H}\" | Pages: {PAGES}")
    print(f"  PB spine: {SPINE_PB:.3f}\" | HC spine: {SPINE_HC:.3f}\"")
    build_kindle()
    build_paperback()
    build_hardcover()
    print("\n" + "=" * 60)
    print("  ALL COVERS DONE")
    print("=" * 60)

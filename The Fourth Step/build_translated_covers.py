import os
import sys
from PIL import Image, ImageDraw, ImageEnhance
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = r"D:\Kapil\Books\The Fourth Step"
FONTS_DIR = r"C:\Windows\Fonts"

TRIM_W, TRIM_H = 5.5, 8.5
DPI = 300
BLEED = 0.125

LANGUAGES = [
    {
        "name": "Spanish",
        "image": os.path.join(BASE, "Spanish", "FourthStep_Spanish_paperback.png"),
        "output": os.path.join(BASE, "Spanish", "El_Cuarto_Escalon_Spanish_Paperback.pdf"),
        "kindle_output": os.path.join(BASE, "Spanish", "El_Cuarto_Escalon_Spanish_Kindle.jpg"),
        "pages": 267,
    },
    {
        "name": "French",
        "image": os.path.join(BASE, "French", "FourthStep_French_paperback.png"),
        "output": os.path.join(BASE, "French", "Le_Quatrieme_Marcher_French_Paperback.pdf"),
        "kindle_output": os.path.join(BASE, "French", "Le_Quatrieme_Marcher_French_Kindle.jpg"),
        "pages": 276,
    },
    {
        "name": "German",
        "image": os.path.join(BASE, "German", "FourthStep_German_paperback.png"),
        "output": os.path.join(BASE, "German", "Die_Vierte_Stufe_German_Paperback.pdf"),
        "kindle_output": os.path.join(BASE, "German", "Die_Vierte_Stufe_German_Kindle.jpg"),
        "pages": 290,
    },
]

EN_BACK_RATIO = 723 / 1610
EN_SPINE_RATIO = 113 / 1610


def add_barcode_box(back_img, bleed_px):
    w, h = back_img.size
    bw = int(2.0 * DPI)
    bh = int(1.2 * DPI)
    margin = int(0.25 * DPI)
    bx = w - margin - bw
    by = h - bleed_px - margin - bh
    draw = ImageDraw.Draw(back_img)
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(255, 255, 255))
    return back_img


def build_paperback(lang):
    name = lang["name"]
    image_path = lang["image"]
    output_path = lang["output"]
    pages = lang["pages"]

    print(f"\n{'='*50}")
    print(f"  {name} — KDP Paperback Cover")
    print(f"{'='*50}")

    if not os.path.isfile(image_path):
        print(f"  ERROR: {image_path} not found")
        return

    img = Image.open(image_path).convert("RGB")
    iw, ih = img.size
    print(f"  Source image: {iw}x{ih} px")

    spine_w_inches = pages * 0.002252
    spine_w_px = int(spine_w_inches * DPI)
    trim_w_px = int(TRIM_W * DPI)
    trim_h_px = int(TRIM_H * DPI)
    bleed_px = int(BLEED * DPI)

    back_w = trim_w_px + bleed_px
    front_w = trim_w_px + bleed_px
    total_h = trim_h_px + 2 * bleed_px

    total_w = back_w + spine_w_px + front_w

    back_split = int(iw * EN_BACK_RATIO)
    spine_split = int(iw * (EN_BACK_RATIO + EN_SPINE_RATIO))

    back_img = img.crop((0, 0, back_split, ih))
    spine_img = img.crop((back_split, 0, spine_split, ih))
    front_img = img.crop((spine_split, 0, iw, ih))

    print(f"  Split: back={back_img.size}, spine={spine_img.size}, front={front_img.size}")

    back_img = back_img.resize((back_w, total_h), Image.LANCZOS)
    spine_img = spine_img.resize((spine_w_px, total_h), Image.LANCZOS)
    front_img = front_img.resize((front_w, total_h), Image.LANCZOS)


    full = Image.new("RGB", (total_w, total_h))
    full.paste(back_img, (0, 0))
    full.paste(spine_img, (back_w, 0))
    full.paste(front_img, (back_w + spine_w_px, 0))

    full = ImageEnhance.Sharpness(full).enhance(1.2)
    full = ImageEnhance.Contrast(full).enhance(1.05)

    temp_png = os.path.join(os.path.dirname(output_path), "_cover_temp.png")
    full.save(temp_png, "PNG", dpi=(DPI, DPI))

    pdf_w = total_w / DPI * inch
    pdf_h = total_h / DPI * inch

    c = canvas.Canvas(output_path, pagesize=(pdf_w, pdf_h))
    c.drawImage(temp_png, 0, 0, width=pdf_w, height=pdf_h)
    c.showPage()
    c.save()
    os.remove(temp_png)

    fsize = os.path.getsize(output_path)
    print(f"  Spine: {spine_w_inches:.3f}\" ({spine_w_px}px)")
    print(f"  Total: {total_w/DPI:.3f}\" x {total_h/DPI:.3f}\" ({total_w}x{total_h}px)")
    print(f"  Output: {output_path}")
    print(f"  Size: {fsize / 1024:.0f} KB")


def extract_kindle_cover(lang):
    name = lang["name"]
    image_path = lang["image"]
    kindle_path = lang.get("kindle_output", image_path.replace("_paperback.png", "_Kindle.jpg"))

    print(f"\n  {name} — Kindle front cover extraction")

    if not os.path.isfile(image_path):
        print(f"    ERROR: {image_path} not found")
        return

    img = Image.open(image_path).convert("RGB")
    iw, ih = img.size

    spine_start = int(iw * EN_BACK_RATIO)
    front_start = int(iw * (EN_BACK_RATIO + EN_SPINE_RATIO))

    front = img.crop((front_start, 0, iw, ih))

    kindle_w, kindle_h = 1600, 2560
    front = front.resize((kindle_w, kindle_h), Image.LANCZOS)
    front = ImageEnhance.Sharpness(front).enhance(1.1)

    front.save(kindle_path, "JPEG", quality=95)
    fsize = os.path.getsize(kindle_path)
    print(f"    Output: {kindle_path}")
    print(f"    Size: {fsize / 1024:.0f} KB ({kindle_w}x{kindle_h})")


def main():
    print("=" * 50)
    print("  Translated KDP Cover Generator")
    print("=" * 50)
    print(f"  Trim: {TRIM_W}\" x {TRIM_H}\"")
    print(f"  Bleed: {BLEED}\"")
    print(f"  DPI: {DPI}")

    for lang in LANGUAGES:
        build_paperback(lang)
        extract_kindle_cover(lang)

    print(f"\n{'='*50}")
    print("  ALL COVERS GENERATED")
    print(f"{'='*50}")
    for lang in LANGUAGES:
        if os.path.isfile(lang["output"]):
            print(f"  {lang['name']} Paperback: {lang['output']}")
        kindle_path = lang.get("kindle_output", lang["image"].replace("_paperback.png", "_Kindle.jpg"))
        if os.path.isfile(kindle_path):
            print(f"  {lang['name']} Kindle: {kindle_path}")
    print("Done.")


if __name__ == "__main__":
    main()

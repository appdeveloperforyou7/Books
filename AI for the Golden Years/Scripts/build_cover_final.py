"""
Definitive cover PDF generation with proper bleed extension.
Each cover panel includes bleed content so backgrounds extend to bleed edges.
No blank/cream borders visible after trimming.
"""
import os, sys
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

ASSETS = r"D:\Kapil\Books\First\Assets"
OUTPUT = r"D:\Kapil\Books\First\Output"
FRONT_IMG = os.path.join(ASSETS, "frontcover_current.jpg")
BACK_IMG = os.path.join(ASSETS, "backcover_current.png")

TRIM_W = 7.0; TRIM_H = 10.0; SPINE = 0.106; BLEED = 0.125
DPI = 300
TRIM_W_PX = int(TRIM_W * DPI); TRIM_H_PX = int(TRIM_H * DPI)
SPINE_PX = int(SPINE * DPI); BLEED_PX = int(BLEED * DPI)

FRONT_W_PX = TRIM_W_PX + BLEED_PX
BACK_W_PX = TRIM_W_PX + BLEED_PX
PANEL_H_PX = TRIM_H_PX + BLEED_PX * 2

SPREAD_W = TRIM_W * 2 + SPINE + BLEED * 2
SPREAD_H = TRIM_H + BLEED * 2
SPREAD_W_PX = FRONT_W_PX + BACK_W_PX + SPINE_PX
SPREAD_H_PX = PANEL_H_PX

CREAM = (253, 251, 247); GOLD = (201, 145, 61); WHITE = (255, 255, 255)
DARK_NAVY = (10, 21, 37)

def load_font(size, bold=False):
    paths = [
        "C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/georgiab.ttf",
        "C:/Windows/Fonts/times.ttf", "C:/Windows/Fonts/timesbd.ttf",
        "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/seguisb.ttf",
    ]
    for fp in paths:
        if os.path.exists(fp):
            try: return ImageFont.truetype(fp, size)
            except: continue
    return ImageFont.load_default()

def extend_image_to_canvas(img, target_w, target_h, edge_mode='reflect'):
    scaled = img.resize((target_w, target_h), Image.LANCZOS)
    return scaled

def build_front():
    panel_w = FRONT_W_PX
    panel_h = PANEL_H_PX

    img = Image.open(FRONT_IMG).convert('RGBA')
    img = img.resize((panel_w, panel_h), Image.LANCZOS)
    for e in [(ImageEnhance.Contrast, 1.05), (ImageEnhance.Sharpness, 1.2)]:
        img = e[0](img).enhance(e[1])
    img = img.convert('RGBA')

    overlay = Image.new('RGBA', (panel_w, panel_h), (0, 0, 0, 0))
    for y in range(panel_h):
        if y < panel_h * 0.45: continue
        ratio = (y - panel_h * 0.45) / (panel_h * 0.55)
        for x in range(panel_w):
            overlay.putpixel((x, y), CREAM + (int(255 * min(ratio * 1.2, 1.0)),))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    p = int(0.55 * DPI)

    tf = load_font(int(7 * DPI / 72), True)
    ty = panel_h - int(1.0 * DPI) - BLEED_PX
    draw.rectangle([p, ty - 14, p + 112, ty - 12], fill=GOLD)
    draw.text((p, ty), "THE COMPLETE SENIOR'S COMPANION", fill=GOLD, font=tf)

    ttl = load_font(int(38 * DPI / 72), True)
    ty = ty + 45
    for line in ["AI for the", "Golden Years"]:
        draw.text((p + 3, ty + 2), line, fill=(0, 0, 0, 70), font=ttl)
        draw.text((p, ty), line, fill=WHITE, font=ttl)
        ty += draw.textbbox((0, 0), line, font=ttl)[3] - draw.textbbox((0, 0), line, font=ttl)[1] - 8

    sf = load_font(int(10 * DPI / 72), False)
    draw.text((p + 2, ty + 2), "Your Friendly Guide to Everyday Magic & Staying Safe",
              fill=(0, 0, 0, 60), font=sf)
    draw.text((p, ty), "Your Friendly Guide to Everyday Magic & Staying Safe",
              fill=(255, 255, 255, 220), font=sf)
    ty += 48
    draw.rectangle([p, ty, p + 135, ty + 6], fill=GOLD)
    return img.convert('RGB')

def build_spine():
    spine_h = PANEL_H_PX
    img = Image.new('RGB', (SPINE_PX, spine_h), DARK_NAVY)
    draw = ImageDraw.Draw(img)
    y_top = BLEED_PX + 200
    y_bot = BLEED_PX + TRIM_H_PX - 200
    for sx in [3, SPINE_PX - 4]:
        draw.line([(sx, y_top), (sx, y_bot)], fill=GOLD, width=1)
    tf, sf = load_font(int(7*DPI/72), True), load_font(int(4.5*DPI/72), True)
    y = BLEED_PX + 400
    for ch in "AI for the Golden Years":
        cb = draw.textbbox((0, 0), ch, font=tf)
        draw.text(((SPINE_PX - (cb[2]-cb[0]))//2, y), ch, fill=WHITE, font=tf)
        y += cb[3] - cb[1] + 1
    y += 30
    for ch in "THE COMPLETE SENIOR'S COMPANION":
        cb = draw.textbbox((0, 0), ch, font=sf)
        draw.text(((SPINE_PX - (cb[2]-cb[0]))//2, y), ch, fill=GOLD, font=sf)
        y += cb[3] - cb[1] + 1
    return img

def build_back():
    panel_w = BACK_W_PX
    panel_h = PANEL_H_PX

    img = Image.open(BACK_IMG).convert('RGBA')
    img = img.resize((panel_w, panel_h), Image.LANCZOS)
    img = ImageEnhance.Brightness(img).enhance(0.88)
    img = img.convert('RGBA')

    overlay = Image.new('RGBA', (panel_w, panel_h), (0, 0, 0, 0))
    for x in range(panel_w):
        ratio = x / panel_w
        alpha = int(230 * max(0, 1 - (ratio-0.75)/0.25)) if ratio > 0.75 else min(230, 200 + int(30 * ratio))
        for y in range(panel_h):
            overlay.putpixel((x, y), (10, 20, 40) + (alpha,))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    p = int(0.55 * DPI) + BLEED_PX
    y = int(0.9 * DPI) + BLEED_PX

    draw.text((p, y), "TECHNOLOGY FOR SENIORS", fill=GOLD, font=load_font(int(6.5*DPI/72), True))
    y += 36
    for line in ["Discover the Magic of AI", "\u2014 Without the Confusion"]:
        draw.text((p, y), line, fill=WHITE, font=load_font(int(16*DPI/72), True))
        y += 58
    y -= 8
    draw.rectangle([p, y, p + 80, y + 5], fill=GOLD); y += 25

    df = load_font(int(7*DPI/72), False)
    for line in [
        'Are you hearing about "AI" and "ChatGPT" everywhere',
        "but aren't sure what it means for you? Do you worry",
        "about falling behind \u2014 or being targeted by online scams?",
        "", "This warm, easy-to-read guide breaks down complex",
        "technology into simple, everyday language, tailor-made",
        "for seniors who want to embrace the digital age with",
        "confidence and stay safe while doing it."
    ]:
        if line: draw.text((p, y), line, fill=(255, 255, 255, 200), font=df)
        y += 27

    y += 8; bf = load_font(int(6.25*DPI/72), False)
    for bullet in [
        "\u2022 What AI really is \u2014 and why it's not science fiction",
        "\u2022 Step-by-step guides to ChatGPT, voice assistants & smart apps",
        "\u2022 How to spot deepfakes, voice clones & protect your privacy",
        '\u2022 The foolproof "Safe Word" strategy against AI scams',
        "\u2022 AI for hobbies, health, travel & staying connected to loved ones"
    ]:
        draw.text((p, y), bullet, fill=(255, 255, 255, 175), font=bf)
        y += 25

    copy_txt = "\u00a9 2026 \u2022 All rights reserved"
    draw.text((p, panel_h - BLEED_PX - int(1.1*DPI)), copy_txt,
              fill=(255, 255, 255, 110), font=load_font(int(5.5*DPI/72), False))
    return img.convert('RGB')


def main():
    print("Building cover panels with bleed...")
    front = build_front()
    print(f"  Front panel: {front.size[0]}x{front.size[1]}px (incl. bleed)")
    spine = build_spine()
    print(f"  Spine panel: {spine.size[0]}x{spine.size[1]}px (incl. bleed)")
    back = build_back()
    print(f"  Back panel:  {back.size[0]}x{back.size[1]}px (incl. bleed)")

    spread = Image.new('RGB', (SPREAD_W_PX, SPREAD_H_PX), CREAM)
    spread.paste(back, (0, 0))
    spread.paste(spine, (BACK_W_PX, 0))
    spread.paste(front, (BACK_W_PX + SPINE_PX, 0))

    jpg_buf = BytesIO()
    spread.save(jpg_buf, 'JPEG', quality=95, subsampling=0)
    jpg_buf.seek(0)
    print(f"JPEG size: {jpg_buf.getbuffer().nbytes/1024:.0f} KB")

    print("Creating PDF with reportlab...")
    pdf_path = os.path.join(OUTPUT, "Cover_KDP.pdf")
    c = canvas.Canvas(pdf_path, pagesize=(SPREAD_W * inch, SPREAD_H * inch))
    c.drawImage(ImageReader(jpg_buf), 0, 0,
                width=SPREAD_W * inch, height=SPREAD_H * inch)
    c.showPage()
    c.save()

    mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"PDF saved: {pdf_path} ({mb:.2f} MB)")
    print(f"Bleed-safe spread: {SPREAD_W:.4f}\" x {SPREAD_H:.4f}\"")
    print(f"  Trim area: {TRIM_W*2 + SPINE:.4f}\" x {TRIM_H:.4f}\"")
    print(f"  Bleed: {BLEED:.3f}\" on all four sides")
    print(f"  Front panel: {FRONT_W_PX/DPI:.4f}\" x {PANEL_H_PX/DPI:.4f}\"")
    print(f"  Back panel:  {BACK_W_PX/DPI:.4f}\" x {PANEL_H_PX/DPI:.4f}\"")

    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_path)
    print(f"Pages: {len(reader.pages)} - PDF is valid")


if __name__ == '__main__':
    main()

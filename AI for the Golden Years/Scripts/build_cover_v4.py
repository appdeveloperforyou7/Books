"""
Build cover PDF v4 - use reportlab for maximum PDF compatibility.
Creates a proper PDF with embedded JPEG at full quality.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from io import BytesIO

ASSETS = r"D:\Kapil\Books\First\Assets"
OUTPUT = r"D:\Kapil\Books\First\Output"
FRONT_IMG = os.path.join(ASSETS, "frontcover_current.jpg")
BACK_IMG = os.path.join(ASSETS, "backcover_current.png")

TRIM_W = 7.0
TRIM_H = 10.0
SPINE = 0.106
BLEED = 0.125
SPREAD_W = TRIM_W * 2 + SPINE + BLEED * 2
SPREAD_H = TRIM_H + BLEED * 2

DPI = 300
TRIM_W_PX = int(TRIM_W * DPI)
TRIM_H_PX = int(TRIM_H * DPI)
SPINE_PX = int(SPINE * DPI)
BLEED_PX = int(BLEED * DPI)
SPREAD_W_PX = TRIM_W_PX * 2 + SPINE_PX + BLEED_PX * 2
SPREAD_H_PX = TRIM_H_PX + BLEED_PX * 2

CREAM = (253, 251, 247)
GOLD = (201, 145, 61)
WHITE = (255, 255, 255)
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
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
    return ImageFont.load_default()


def build_front():
    img = Image.open(FRONT_IMG).convert('RGBA')
    if img.size != (TRIM_W_PX, TRIM_H_PX):
        img = img.resize((TRIM_W_PX, TRIM_H_PX), Image.LANCZOS)
    enhancer = ImageEnhance.Contrast(img); img = enhancer.enhance(1.05)
    enhancer = ImageEnhance.Sharpness(img); img = enhancer.enhance(1.2)
    img = img.convert('RGBA')

    overlay = Image.new('RGBA', (TRIM_W_PX, TRIM_H_PX), (0, 0, 0, 0))
    for y in range(TRIM_H_PX):
        if y < TRIM_H_PX * 0.45: continue
        ratio = (y - TRIM_H_PX * 0.45) / (TRIM_H_PX * 0.55)
        for x in range(TRIM_W_PX):
            overlay.putpixel((x, y), CREAM + (int(255 * min(ratio * 1.2, 1.0)),))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    pad = int(0.55 * DPI)

    tag_font = load_font(int(7 * DPI / 72), True)
    tag_y = TRIM_H_PX - int(1.0 * DPI)
    draw.rectangle([pad, tag_y - 14, pad + 112, tag_y - 12], fill=GOLD)
    draw.text((pad, tag_y), "THE COMPLETE SENIOR'S COMPANION", fill=GOLD, font=tag_font)

    title_font = load_font(int(38 * DPI / 72), True)
    ty = tag_y + 45
    for line in ["AI for the", "Golden Years"]:
        draw.text((pad + 3, ty + 2), line, fill=(0, 0, 0, 70), font=title_font)
        draw.text((pad, ty), line, fill=WHITE, font=title_font)
        bbox = draw.textbbox((0, 0), line, font=title_font)
        ty += bbox[3] - bbox[1] - 8

    sub_font = load_font(int(10 * DPI / 72), False)
    draw.text((pad + 2, ty + 2), "Your Friendly Guide to Everyday Magic & Staying Safe",
              fill=(0, 0, 0, 60), font=sub_font)
    draw.text((pad, ty), "Your Friendly Guide to Everyday Magic & Staying Safe",
              fill=(255, 255, 255, 220), font=sub_font)

    ry = ty + 48
    draw.rectangle([pad, ry, pad + 135, ry + 6], fill=GOLD)
    return img.convert('RGB')


def build_spine():
    img = Image.new('RGB', (SPINE_PX, TRIM_H_PX), DARK_NAVY)
    draw = ImageDraw.Draw(img)
    for sx in [3, SPINE_PX - 4]:
        draw.line([(sx, 200), (sx, TRIM_H_PX - 200)], fill=GOLD, width=1)

    title_font = load_font(int(7 * DPI / 72), True)
    sub_font = load_font(int(4.5 * DPI / 72), True)
    y = 400
    for ch in "AI for the Golden Years":
        cbbox = draw.textbbox((0, 0), ch, font=title_font)
        cw, ch_h = cbbox[2] - cbbox[0], cbbox[3] - cbbox[1]
        draw.text(((SPINE_PX - cw)//2, y), ch, fill=WHITE, font=title_font)
        y += ch_h + 1
    y += 30
    for ch in "THE COMPLETE SENIOR'S COMPANION":
        cbbox = draw.textbbox((0, 0), ch, font=sub_font)
        cw, ch_h = cbbox[2] - cbbox[0], cbbox[3] - cbbox[1]
        draw.text(((SPINE_PX - cw)//2, y), ch, fill=GOLD, font=sub_font)
        y += ch_h + 1
    return img


def build_back():
    img = Image.open(BACK_IMG).convert('RGBA')
    if img.size != (TRIM_W_PX, TRIM_H_PX):
        img = img.resize((TRIM_W_PX, TRIM_H_PX), Image.LANCZOS)
    enhancer = ImageEnhance.Brightness(img); img = enhancer.enhance(0.88)
    img = img.convert('RGBA')

    overlay = Image.new('RGBA', (TRIM_W_PX, TRIM_H_PX), (0, 0, 0, 0))
    for x in range(TRIM_W_PX):
        ratio = x / TRIM_W_PX
        alpha = int(230 * (1.0 - max(0, ratio - 0.75)/0.25)) if ratio > 0.75 else 200 + int(30 * ratio)
        for y in range(TRIM_H_PX):
            overlay.putpixel((x, y), (10, 20, 40) + (alpha,))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    pad = int(0.55 * DPI)
    y = int(0.9 * DPI)

    eb_font = load_font(int(6.5 * DPI / 72), True)
    draw.text((pad, y), "TECHNOLOGY FOR SENIORS", fill=GOLD, font=eb_font)
    y += 36

    t_font = load_font(int(16 * DPI / 72), True)
    for line in ["Discover the Magic of AI", "— Without the Confusion"]:
        draw.text((pad, y), line, fill=WHITE, font=t_font)
        y += 58
    y -= 8

    draw.rectangle([pad, y, pad + 80, y + 5], fill=GOLD)
    y += 25

    d_font = load_font(int(7 * DPI / 72), False)
    for line in [
        'Are you hearing about "AI" and "ChatGPT" everywhere',
        "but aren't sure what it means for you? Do you worry",
        "about falling behind \u2014 or being targeted by online scams?",
        "",
        "This warm, easy-to-read guide breaks down complex",
        "technology into simple, everyday language, tailor-made",
        "for seniors who want to embrace the digital age with",
        "confidence and stay safe while doing it.",
    ]:
        if line:
            draw.text((pad, y), line, fill=(255, 255, 255, 200), font=d_font)
        y += 27

    y += 8
    b_font = load_font(int(6.25 * DPI / 72), False)
    for bullet in [
        "\u2022 What AI really is \u2014 and why it's not science fiction",
        "\u2022 Step-by-step guides to ChatGPT, voice assistants & smart apps",
        "\u2022 How to spot deepfakes, voice clones & protect your privacy",
        '\u2022 The foolproof "Safe Word" strategy against AI scams',
        "\u2022 AI for hobbies, health, travel & staying connected to loved ones",
    ]:
        draw.text((pad, y), bullet, fill=(255, 255, 255, 175), font=b_font)
        y += 25

    bx = TRIM_W_PX - pad - int(1.4 * DPI)
    by = TRIM_H_PX - int(1.2 * DPI)
    draw.rectangle([bx, by, bx + int(1.4 * DPI), by + int(0.9 * DPI)],
                   outline=(255, 255, 255, 50), width=2)
    s_font = load_font(int(5 * DPI / 72), False)
    draw.text((bx + 70, by + 70), "ISBN", fill=(255, 255, 255, 70), font=s_font)
    draw.text((bx + 45, by + 100), "BARCODE", fill=(255, 255, 255, 70), font=s_font)
    draw.text((bx + 55, by + 130), "HERE", fill=(255, 255, 255, 70), font=s_font)

    c_font = load_font(int(5.5 * DPI / 72), False)
    draw.text((pad, by + 250), "\u00a9 2025 \u2022 All rights reserved",
              fill=(255, 255, 255, 110), font=c_font)
    return img.convert('RGB')


def main():
    print("Building cover at 300 DPI (reportlab PDF)...")

    front = build_front()
    spine = build_spine()
    back = build_back()

    spread = Image.new('RGB', (SPREAD_W_PX, SPREAD_H_PX), CREAM)
    spread.paste(back, (BLEED_PX, BLEED_PX))
    spread.paste(spine, (BLEED_PX + TRIM_W_PX, BLEED_PX))
    spread.paste(front, (BLEED_PX + TRIM_W_PX + SPINE_PX, BLEED_PX))

    # Save JPEG at max quality
    jpg_buf = BytesIO()
    spread.save(jpg_buf, 'JPEG', quality=100, subsampling=0)
    jpg_data = jpg_buf.getvalue()
    print(f"JPEG size: {len(jpg_data)/1024:.0f} KB")

    # Create PDF with reportlab (most compatible)
    from reportlab.lib.pagesizes import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from PyPDF2 import PdfReader, PdfWriter
    from PyPDF2.generic import RectangleObject

    pdf_tmp = os.path.join(OUTPUT, "cover_tmp_rl.pdf")
    c = canvas.Canvas(pdf_tmp, pagesize=(SPREAD_W * inch, SPREAD_H * inch))
    c.drawImage(ImageReader(BytesIO(jpg_data)), 0, 0,
                width=SPREAD_W * inch, height=SPREAD_H * inch)
    c.showPage()
    c.save()
    print(f"Reportlab PDF: {pdf_tmp} ({os.path.getsize(pdf_tmp)/1024:.0f} KB)")

    # Add boxes
    reader = PdfReader(pdf_tmp)
    writer = PdfWriter()
    bw, bh = SPREAD_W * 72, SPREAD_H * 72
    tw, th = bw - BLEED * 72 * 2, bh - BLEED * 72 * 2
    ox, oy = (bw - tw) / 2, (bh - th) / 2

    for page in reader.pages:
        page.mediabox = RectangleObject([0, 0, bw, bh])
        page.trimbox = RectangleObject([ox, oy, ox + tw, oy + th])
        page.bleedbox = RectangleObject([0, 0, bw, bh])
        writer.add_page(page)

    pdf_final = os.path.join(OUTPUT, "Cover_KDP.pdf")
    with open(pdf_final, 'wb') as f:
        writer.write(f)
    os.remove(pdf_tmp)

    mb = os.path.getsize(pdf_final) / (1024 * 1024)
    print(f"FINAL PDF: {pdf_final} ({mb:.2f} MB)")
    print(f"MediaBox: {bw/72:.3f}\" x {bh/72:.3f}\"")
    print(f"TrimBox: {tw/72:.3f}\" x {th/72:.3f}\"")
    print("Done - try opening in Acrobat now.")


if __name__ == '__main__':
    main()

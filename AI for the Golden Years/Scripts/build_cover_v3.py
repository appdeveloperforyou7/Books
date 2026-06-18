"""
Build KDP cover PDF - v3. Simpler approach:
1. Composite the cover as a PIL image at 300 DPI (standard print)
2. Save as JPEG
3. Use Pillow's own PDF save (most reliable)
4. Add TrimBox/BleedBox via PyPDF2
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ASSETS = r"D:\Kapil\Books\First\Assets"
OUTPUT = r"D:\Kapil\Books\First\Output"
FRONT_IMG = os.path.join(ASSETS, "frontcover_current.jpg")
BACK_IMG = os.path.join(ASSETS, "backcover_current.png")

TRIM_W = 7.0
TRIM_H = 10.0
SPINE = 0.106
BLEED = 0.125
SPREAD_W = TRIM_W * 2 + SPINE + BLEED * 2   # 14.356"
SPREAD_H = TRIM_H + BLEED * 2                # 10.25"

DPI = 300  # Standard print DPI
TRIM_W_PX = int(TRIM_W * DPI)   # 2100
TRIM_H_PX = int(TRIM_H * DPI)   # 3000
SPINE_PX = int(SPINE * DPI)     # 32
BLEED_PX = int(BLEED * DPI)     # 38
SPREAD_W_PX = TRIM_W_PX * 2 + SPINE_PX + BLEED_PX * 2  # 4307
SPREAD_H_PX = TRIM_H_PX + BLEED_PX * 2                  # 3075

CREAM = (253, 251, 247)
GOLD = (201, 145, 61)
NAVY = (30, 42, 74)
DARK_NAVY = (10, 21, 37)
WHITE = (255, 255, 255)

print(f"Spread: {SPREAD_W_PX}x{SPREAD_H_PX}px at {DPI} DPI")


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
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.05)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)
    img = img.convert('RGBA')

    # Cream gradient at bottom
    overlay = Image.new('RGBA', (TRIM_W_PX, TRIM_H_PX), (0, 0, 0, 0))
    for y in range(TRIM_H_PX):
        if y < TRIM_H_PX * 0.45:
            continue
        ratio = (y - TRIM_H_PX * 0.45) / (TRIM_H_PX * 0.55)
        alpha = int(255 * min(ratio * 1.2, 1.0))
        for x in range(TRIM_W_PX):
            overlay.putpixel((x, y), CREAM + (alpha,))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)
    pad = int(0.55 * DPI)  # left padding

    # Tag
    tag_font = load_font(int(7 * DPI / 72), True)
    tag_y = TRIM_H_PX - int(1.0 * DPI)
    draw.rectangle([pad, tag_y - 14, pad + 112, tag_y - 12], fill=GOLD)
    draw.text((pad, tag_y), "THE COMPLETE SENIOR'S COMPANION", fill=GOLD, font=tag_font)

    # Title
    title_font = load_font(int(38 * DPI / 72), True)
    title_lines = ["AI for the", "Golden Years"]
    ty = tag_y + 45
    for line in title_lines:
        draw.text((pad + 3, ty + 3), line, fill=(0, 0, 0, 90), font=title_font)
        draw.text((pad, ty), line, fill=WHITE, font=title_font)
        bbox = draw.textbbox((0, 0), line, font=title_font)
        ty += bbox[3] - bbox[1] - 8

    # Subtitle
    sub_font = load_font(int(10 * DPI / 72), False)
    draw.text((pad + 2, ty + 2), "Your Friendly Guide to Everyday Magic & Staying Safe",
              fill=(0, 0, 0, 70), font=sub_font)
    draw.text((pad, ty), "Your Friendly Guide to Everyday Magic & Staying Safe",
              fill=(255, 255, 255, 225), font=sub_font)

    # Gold rule
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
    title = "AI for the Golden Years"
    sub = "THE COMPLETE SENIOR'S COMPANION"

    # Write vertically character by character
    y = 400
    for ch in title:
        cbbox = draw.textbbox((0, 0), ch, font=title_font)
        cw = cbbox[2] - cbbox[0]
        ch_h = cbbox[3] - cbbox[1]
        cx = (SPINE_PX - cw) // 2
        draw.text((cx, y), ch, fill=WHITE, font=title_font)
        y += ch_h + 1

    y += 30
    for ch in sub:
        cbbox = draw.textbbox((0, 0), ch, font=sub_font)
        cw = cbbox[2] - cbbox[0]
        ch_h = cbbox[3] - cbbox[1]
        cx = (SPINE_PX - cw) // 2
        draw.text((cx, y), ch, fill=GOLD, font=sub_font)
        y += ch_h + 1

    return img


def build_back():
    img = Image.open(BACK_IMG).convert('RGBA')
    if img.size != (TRIM_W_PX, TRIM_H_PX):
        img = img.resize((TRIM_W_PX, TRIM_H_PX), Image.LANCZOS)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.88)
    img = img.convert('RGBA')

    # Dark overlay from left
    overlay = Image.new('RGBA', (TRIM_W_PX, TRIM_H_PX), (0, 0, 0, 0))
    for x in range(TRIM_W_PX):
        ratio = x / TRIM_W_PX
        if ratio > 0.75:
            alpha = int(230 * (1.0 - (ratio - 0.75) / 0.25))
        else:
            alpha = 200 + int(30 * ratio)
        for y in range(TRIM_H_PX):
            overlay.putpixel((x, y), (10, 20, 40) + (alpha,))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)
    pad = int(0.55 * DPI)
    y = int(0.9 * DPI)

    # Eyebrow
    eb_font = load_font(int(6.5 * DPI / 72), True)
    draw.text((pad, y), "TECHNOLOGY FOR SENIORS", fill=GOLD, font=eb_font)
    y += 36

    # Title
    t_font = load_font(int(16 * DPI / 72), True)
    for line in ["Discover the Magic of AI", "— Without the Confusion"]:
        draw.text((pad, y), line, fill=WHITE, font=t_font)
        y += 58
    y -= 8

    # Rule
    draw.rectangle([pad, y, pad + 80, y + 5], fill=GOLD)
    y += 25

    # Description
    d_font = load_font(int(7 * DPI / 72), False)
    desc = [
        'Are you hearing about "AI" and "ChatGPT" everywhere',
        "but aren't sure what it means for you?",
        "Do you worry about falling behind — or being targeted",
        "by sophisticated online scams?",
        "",
        "This warm, easy-to-read guide breaks down complex",
        "technology into simple, everyday language, tailor-made",
        "for seniors who want to embrace the digital age",
        "with confidence and stay safe while doing it.",
    ]
    for line in desc:
        if line:
            draw.text((pad, y), line, fill=(255, 255, 255, 200), font=d_font)
        y += 27

    y += 8
    # Bullets
    b_font = load_font(int(6.25 * DPI / 72), False)
    bullets = [
        "• What AI really is — and why it's not science fiction",
        "• Step-by-step guides to ChatGPT, voice assistants & smart apps",
        "• How to spot deepfakes, voice clones & protect your privacy",
        '• The foolproof "Safe Word" strategy against AI scams',
        "• AI for hobbies, health, travel & staying connected to loved ones",
    ]
    for bullet in bullets:
        draw.text((pad, y), bullet, fill=(255, 255, 255, 175), font=b_font)
        y += 25

    # Barcode box (bottom right)
    bx = TRIM_W_PX - pad - int(1.4 * DPI)
    by = TRIM_H_PX - int(1.2 * DPI)
    draw.rectangle([bx, by, bx + int(1.4 * DPI), by + int(0.9 * DPI)],
                   outline=(255, 255, 255, 50), width=2)
    s_font = load_font(int(5 * DPI / 72), False)
    draw.text((bx + 70, by + 70), "ISBN", fill=(255, 255, 255, 70), font=s_font)
    draw.text((bx + 45, by + 100), "BARCODE", fill=(255, 255, 255, 70), font=s_font)
    draw.text((bx + 55, by + 130), "HERE", fill=(255, 255, 255, 70), font=s_font)

    # Copyright
    c_font = load_font(int(5.5 * DPI / 72), False)
    draw.text((pad, by + 250), "\u00a9 2025 \u2022 All rights reserved",
              fill=(255, 255, 255, 110), font=c_font)

    return img.convert('RGB')


def main():
    print("=" * 55)
    print("  KDP Cover Builder v3 (300 DPI, Pillow PDF)")
    print("=" * 55)

    front = build_front()
    spine = build_spine()
    back = build_back()

    spread = Image.new('RGB', (SPREAD_W_PX, SPREAD_H_PX), CREAM)
    spread.paste(back, (BLEED_PX, BLEED_PX))
    spread.paste(spine, (BLEED_PX + TRIM_W_PX, BLEED_PX))
    spread.paste(front, (BLEED_PX + TRIM_W_PX + SPINE_PX, BLEED_PX))

    # Save JPEG
    jpg_path = os.path.join(OUTPUT, "cover_spread_v3.jpg")
    spread.save(jpg_path, 'JPEG', quality=95, subsampling=0)
    print(f"Cover image: {jpg_path} ({os.path.getsize(jpg_path)/1024:.0f} KB)")

    # Convert to PDF using Pillow
    print("Converting to PDF via Pillow...")
    pdf_tmp = os.path.join(OUTPUT, "cover_tmp.pdf")
    spread.save(pdf_tmp, 'PDF', resolution=DPI)
    print(f"Raw PDF: {pdf_tmp} ({os.path.getsize(pdf_tmp)/1024:.0f} KB)")

    # Add page boxes
    print("Adding TrimBox/BleedBox...")
    from PyPDF2 import PdfReader, PdfWriter
    from PyPDF2.generic import RectangleObject

    reader = PdfReader(pdf_tmp)
    writer = PdfWriter()
    bleed_w = SPREAD_W * 72
    bleed_h = SPREAD_H * 72
    trim_w = bleed_w - BLEED * 72 * 2
    trim_h = bleed_h - BLEED * 72 * 2
    ox = (bleed_w - trim_w) / 2
    oy = (bleed_h - trim_h) / 2

    for page in reader.pages:
        page.mediabox = RectangleObject([0, 0, bleed_w, bleed_h])
        page.trimbox = RectangleObject([ox, oy, ox + trim_w, oy + trim_h])
        page.bleedbox = RectangleObject([0, 0, bleed_w, bleed_h])
        writer.add_page(page)

    pdf_final = os.path.join(OUTPUT, "Cover_KDP.pdf")
    with open(pdf_final, 'wb') as f:
        writer.write(f)
    os.remove(pdf_tmp)

    mb = os.path.getsize(pdf_final) / (1024 * 1024)
    print(f"Cover PDF: {pdf_final} ({mb:.2f} MB)")
    print(f"Dimensions: {float(bleed_w)/72:.3f}\" x {float(bleed_h)/72:.3f}\"")
    print("Done.")


if __name__ == '__main__':
    main()

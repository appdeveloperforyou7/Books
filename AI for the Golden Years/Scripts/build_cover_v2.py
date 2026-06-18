"""
Build KDP cover as a PIL image composite, then convert to PDF.
Avoids HTML/CSS/web-font issues with Chrome headless.
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import RectangleObject
import img2pdf

ASSETS = r"D:\Kapil\Books\First\Assets"
OUTPUT = r"D:\Kapil\Books\First\Output"
FRONT_IMG = os.path.join(ASSETS, "frontcover_current.jpg")
BACK_IMG = os.path.join(ASSETS, "backcover_current.png")

# KDP dimensions
TRIM_W = 7.0
TRIM_H = 10.0
SPINE = 0.106
BLEED = 0.125

SPREAD_W = TRIM_W * 2 + SPINE + BLEED * 2
SPREAD_H = TRIM_H + BLEED * 2

# At 400 DPI
DPI = 400
TRIM_W_PX = int(TRIM_W * DPI)   # 2800
TRIM_H_PX = int(TRIM_H * DPI)   # 4000
SPINE_PX = int(SPINE * DPI)     # 42
BLEED_PX = int(BLEED * DPI)     # 50
SPREAD_W_PX = TRIM_W_PX * 2 + SPINE_PX + BLEED_PX * 2
SPREAD_H_PX = TRIM_H_PX + BLEED_PX * 2

# Colors
CREAM = (253, 251, 247)
GOLD = (201, 145, 61)
NAVY = (30, 42, 74)
DARK_NAVY = (10, 21, 37)
WHITE = (255, 255, 255)
DARK_OVERLAY = (10, 20, 40)
SEMI_WHITE = (255, 255, 255, 220)

print(f"Spread: {SPREAD_W_PX}x{SPREAD_H_PX}px at {DPI} DPI")
print(f"Trim panel: {TRIM_W_PX}x{TRIM_H_PX}px")
print(f"Spine: {SPINE_PX}px wide")


def load_font(size, bold=False):
    """Try to load a font, falling back to default."""
    font_paths = [
        "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/georgiab.ttf",
        "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/timesbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
    return ImageFont.load_default()


def draw_text_gradient(draw, x, y, text, font, color_top, color_bottom):
    """Draw text with a slight vertical gradient for premium look."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    for i, ch in enumerate(text):
        ratio = i / max(len(text) - 1, 1)
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        ch_bbox = draw.textbbox((0, 0), ch, font=font)
        ch_w = ch_bbox[2] - ch_bbox[0]
        draw.text((x, y), ch, fill=(r, g, b), font=font)
        x += ch_w


def create_front_cover():
    """Create the front cover panel with text overlay."""
    img = Image.open(FRONT_IMG).convert('RGBA')
    if img.size != (TRIM_W_PX, TRIM_H_PX):
        img = img.resize((TRIM_W_PX, TRIM_H_PX), Image.LANCZOS)

    # Enhance image
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.08)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.4)
    img = img.convert('RGBA')

    # Create gradient overlay at bottom
    overlay = Image.new('RGBA', (TRIM_W_PX, TRIM_H_PX), (0, 0, 0, 0))
    for y in range(TRIM_H_PX):
        if y < TRIM_H_PX * 0.4:
            continue
        ratio = (y - TRIM_H_PX * 0.4) / (TRIM_H_PX * 0.6)
        # Cream gradient: transparent -> solid cream
        alpha = int(255 * min(ratio * 1.3, 1.0))
        color = CREAM + (alpha,)
        for x in range(TRIM_W_PX):
            overlay.putpixel((x, y), color)

    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    # Tag line
    tag_font = load_font(28, True)
    tag_text = "THE COMPLETE SENIOR'S COMPANION"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
    tag_x = 220  # left padding at 400 DPI
    tag_y = TRIM_H_PX - 380
    # Gold underline before tag
    draw.rectangle([tag_x, tag_y - 18, tag_x + 150, tag_y - 16], fill=GOLD)
    draw.text((tag_x, tag_y), tag_text, fill=GOLD, font=tag_font)

    # Title
    title_lines = ["AI for the", "Golden Years"]
    title_sizes = [152, 152]  # in px at 400 DPI (38pt equivalent)
    title_y = tag_y + 55

    for line, size in zip(title_lines, title_sizes):
        title_font = load_font(size, True)
        # Add text shadow
        draw.text((tag_x + 5, title_y + 5), line, fill=(0, 0, 0, 100), font=title_font)
        draw.text((tag_x, title_y), line, fill=WHITE, font=title_font)
        # Get updated y
        line_bbox = draw.textbbox((0, 0), line, font=title_font)
        title_y += line_bbox[3] - line_bbox[1] - 5

    # Subtitle
    sub_font = load_font(38, False)
    sub_text = "Your Friendly Guide to Everyday Magic & Staying Safe"
    sub_y = title_y + 10
    draw.text((tag_x + 3, sub_y + 2), sub_text, fill=(0, 0, 0, 80), font=sub_font)
    draw.text((tag_x, sub_y), sub_text, fill=(255, 255, 255, 230), font=sub_font)

    # Gold rule
    rule_y = sub_y + 60
    draw.rectangle([tag_x, rule_y, tag_x + 180, rule_y + 8], fill=GOLD)

    # Small gold accent dot
    dot_y = rule_y + 22
    draw.ellipse([tag_x, dot_y, tag_x + 8, dot_y + 8], fill=GOLD)

    return img.convert('RGB')


def create_spine():
    """Create spine panel with text."""
    img = Image.new('RGB', (SPINE_PX, TRIM_H_PX), DARK_NAVY)
    draw = ImageDraw.Draw(img)

    # Vertical gold lines
    for sx in [4, SPINE_PX - 5]:
        draw.line([(sx, 280), (sx, TRIM_H_PX - 280)], fill=GOLD, width=1)

    # Spine text (rendered vertically)
    title_font = load_font(28, True)
    sub_font = load_font(18, True)

    title_text = "AI for the Golden Years"
    sub_text = "THE COMPLETE SENIOR'S COMPANION"

    # Calculate text dimensions
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_h = title_bbox[3] - title_bbox[1]
    sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
    sub_h = sub_bbox[3] - sub_bbox[1]

    total_h = title_h + sub_h + 60
    start_y = (TRIM_H_PX - total_h) // 2

    # Center the text vertically and horizontally
    for ch in title_text:
        ch_bbox = draw.textbbox((0, 0), ch, font=title_font)
        ch_w = ch_bbox[2] - ch_bbox[0]
        ch_x = (SPINE_PX - ch_w) // 2
        draw.text((ch_x, start_y), ch, fill=WHITE, font=title_font)
        ch_h = ch_bbox[3] - ch_bbox[1]
        start_y += ch_h + 1

    start_y += 40
    for ch in sub_text:
        ch_bbox = draw.textbbox((0, 0), ch, font=sub_font)
        ch_w = ch_bbox[2] - ch_bbox[0]
        ch_x = (SPINE_PX - ch_w) // 2
        draw.text((ch_x, start_y), ch, fill=GOLD, font=sub_font)
        ch_h = ch_bbox[3] - ch_bbox[1]
        start_y += ch_h + 1

    return img


def create_back_cover():
    """Create the back cover panel with description."""
    img = Image.open(BACK_IMG).convert('RGBA')
    if img.size != (TRIM_W_PX, TRIM_H_PX):
        img = img.resize((TRIM_W_PX, TRIM_H_PX), Image.LANCZOS)

    # Slightly darken
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.85)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.05)
    img = img.convert('RGBA')

    # Dark overlay gradient (left-to-right)
    overlay = Image.new('RGBA', (TRIM_W_PX, TRIM_H_PX), (0, 0, 0, 0))
    for x in range(TRIM_W_PX):
        ratio = x / TRIM_W_PX
        if ratio > 0.72:
            alpha = int(255 * (1.0 - (ratio - 0.72) / 0.28))
        else:
            alpha = 220 + int(35 * ratio)
        for y in range(TRIM_H_PX):
            overlay.putpixel((x, y), DARK_OVERLAY + (alpha,))

    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    padding = 220  # at 400 DPI (~0.55in)
    y = 340

    # Eyebrow
    eyebrow_font = load_font(24, True)
    draw.text((padding, y), "TECHNOLOGY FOR SENIORS", fill=GOLD, font=eyebrow_font)
    y += 45

    # Title
    title_font = load_font(62, True)
    title_lines = ["Discover the Magic of AI", "— Without the Confusion"]
    for line in title_lines:
        draw.text((padding, y), line, fill=WHITE, font=title_font)
        y += 75
    y -= 15

    # Gold rule
    draw.rectangle([padding, y, padding + 100, y + 6], fill=GOLD)
    y += 30

    # Description
    desc_font = load_font(26, False)
    desc_texts = [
        'Are you hearing about "AI" and "ChatGPT" everywhere',
        "but aren't sure what it means for you? Do you worry about",
        "falling behind — or being targeted by online scams?",
        "",
        "This warm, easy-to-read guide breaks down complex",
        "technology into simple, everyday language, tailor-made",
        "for seniors who want to embrace the digital age with",
        "confidence and stay safe while doing it.",
    ]
    for line in desc_texts:
        if line:
            draw.text((padding, y), line, fill=(255, 255, 255, 210), font=desc_font)
        y += 36

    y += 10
    # Bullets
    bullet_font = load_font(24, False)
    bullets = [
        "• What AI really is — and why it's not science fiction",
        "• Step-by-step guides to ChatGPT, voice assistants & smart apps",
        "• How to spot deepfakes, voice clones & protect your privacy",
        "• The foolproof \"Safe Word\" strategy against AI scams",
        "• AI for hobbies, health, travel & staying connected to loved ones",
    ]
    for bullet in bullets:
        draw.text((padding, y), bullet, fill=(255, 255, 255, 180), font=bullet_font)
        y += 32

    # Footer - barcode box
    barcode_x = TRIM_W_PX - padding - 500
    barcode_y = TRIM_H_PX - 400
    draw.rectangle([barcode_x, barcode_y, barcode_x + 500, barcode_y + 280],
                   outline=(255, 255, 255, 60), width=2)
    small_font = load_font(18, False)
    draw.text((barcode_x + 90, barcode_y + 90), "ISBN", fill=(255, 255, 255, 80), font=small_font)
    draw.text((barcode_x + 50, barcode_y + 120), "BARCODE", fill=(255, 255, 255, 80), font=small_font)
    draw.text((barcode_x + 60, barcode_y + 150), "HERE", fill=(255, 255, 255, 80), font=small_font)

    # Copyright
    copy_font = load_font(20, False)
    draw.text((padding, barcode_y + 220), "\u00a9 2025 \u2022 All rights reserved",
              fill=(255, 255, 255, 120), font=copy_font)

    return img.convert('RGB')


def build_spread():
    """Composite front, spine, and back into one spread image."""
    print("\n--- Building Cover Spread ---")

    front = create_front_cover()
    spine = create_spine()
    back = create_back_cover()

    spread = Image.new('RGB', (SPREAD_W_PX, SPREAD_H_PX), CREAM)

    # Paste back cover (left)
    spread.paste(back, (BLEED_PX, BLEED_PX))

    # Paste spine
    spread.paste(spine, (BLEED_PX + TRIM_W_PX, BLEED_PX))

    # Paste front cover (right)
    spread.paste(front, (BLEED_PX + TRIM_W_PX + SPINE_PX, BLEED_PX))

    # Save high-quality JPEG
    jpg_path = os.path.join(OUTPUT, "cover_spread_final.jpg")
    spread.save(jpg_path, 'JPEG', quality=100, subsampling=0)
    size_kb = os.path.getsize(jpg_path) / 1024
    print(f"Cover image saved: {jpg_path} ({size_kb:.0f} KB)")
    return jpg_path


def convert_to_pdf(jpg_path):
    """Convert JPEG to PDF with proper page boxes."""
    print("\n--- Converting to PDF ---")
    pdf_path = os.path.join(OUTPUT, "Cover_KDP.pdf")

    # Calculate page dimensions in points
    bleed_w_pts = SPREAD_W * 72
    bleed_h_pts = SPREAD_H * 72
    trim_w_pts = bleed_w_pts - BLEED * 72 * 2
    trim_h_pts = bleed_h_pts - BLEED * 72 * 2
    ox = (bleed_w_pts - trim_w_pts) / 2
    oy = (bleed_h_pts - trim_h_pts) / 2

    # Create PDF with img2pdf
    layout_fun = img2pdf.get_layout_fun(
        pagesize=(bleed_w_pts, bleed_h_pts),
        fit=img2pdf.FitMode.fill,
        border=(0, 0, 0, 0)
    )

    with open(pdf_path + ".tmp", "wb") as f:
        f.write(img2pdf.convert(jpg_path, layout_fun=layout_fun))

    # Add TrimBox/BleedBox
    reader = PdfReader(pdf_path + ".tmp")
    writer = PdfWriter()

    for page in reader.pages:
        page.mediabox = RectangleObject([0, 0, bleed_w_pts, bleed_h_pts])
        page.trimbox = RectangleObject([ox, oy, ox + trim_w_pts, oy + trim_h_pts])
        page.bleedbox = RectangleObject([0, 0, bleed_w_pts, bleed_h_pts])
        writer.add_page(page)

    with open(pdf_path, 'wb') as f:
        writer.write(f)

    os.remove(pdf_path + ".tmp")

    size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"Cover PDF: {pdf_path} ({size_mb:.1f} MB)")
    print(f"MediaBox: {bleed_w_pts/72:.3f}\" x {bleed_h_pts/72:.3f}\"")
    print(f"TrimBox: {trim_w_pts/72:.3f}\" x {trim_h_pts/72:.3f}\"")
    return pdf_path


if __name__ == '__main__':
    print("=" * 60)
    print("  KDP Cover Builder (PIL Image Composite)")
    print("=" * 60)

    if not os.path.exists(FRONT_IMG):
        print(f"ERROR: Front image not found: {FRONT_IMG}")
        sys.exit(1)
    if not os.path.exists(BACK_IMG):
        print(f"ERROR: Back image not found: {BACK_IMG}")
        sys.exit(1)

    jpg_path = build_spread()
    pdf_path = convert_to_pdf(jpg_path)

    print(f"\n=== READY FOR KDP UPLOAD ===")
    print(f"Cover PDF: {pdf_path}")

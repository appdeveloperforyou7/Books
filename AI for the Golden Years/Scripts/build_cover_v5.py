"""
Rebuild KDP cover with reportlab native text rendering for professional quality.
Uses PIL only for background image prep, all text/shapes via reportlab canvas.
"""
import os, sys
from io import BytesIO
from PIL import Image, ImageEnhance
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, Color, white

ASSETS = r"D:\Kapil\Books\First\Assets"
OUTPUT = r"D:\Kapil\Books\First\Output"
FRONT_IMG = os.path.join(ASSETS, "frontcover_current.jpg")
BACK_IMG = os.path.join(ASSETS, "backcover_current.png")

TRIM_W, TRIM_H = 7.0, 10.0
SPINE = 0.108
BLEED = 0.125
SPREAD_W = TRIM_W * 2 + SPINE + BLEED * 2
SPREAD_H = TRIM_H + BLEED * 2

DPI = 300
TW_PX = int(TRIM_W * DPI); TH_PX = int(TRIM_H * DPI)
SP_PX = int(SPINE * DPI); BL_PX = int(BLEED * DPI)

GOLD = HexColor('#C9913D')
CREAM = HexColor('#FDFBF7')
DARK_NAVY = HexColor('#0A1525')
NAVY = HexColor('#1E2A4A')
WHITE = white


def prep_front_image():
    """Resize and enhance front cover background, return as BytesIO JPEG."""
    img = Image.open(FRONT_IMG).convert('RGB')
    if img.size != (TW_PX, TH_PX):
        img = img.resize((TW_PX, TH_PX), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.2)

    buf = BytesIO()
    img.save(buf, 'JPEG', quality=95)
    buf.seek(0)
    return ImageReader(buf), img.size


def prep_back_image():
    """Resize back cover background, darken slightly, return as BytesIO JPEG."""
    img = Image.open(BACK_IMG).convert('RGB')
    if img.size != (TW_PX, TH_PX):
        img = img.resize((TW_PX, TH_PX), Image.LANCZOS)
    img = ImageEnhance.Brightness(img).enhance(0.85)
    img = ImageEnhance.Contrast(img).enhance(1.03)

    # Dark overlay from left
    overlay = Image.new('RGBA', (TW_PX, TH_PX), (0, 0, 0, 0))
    for x in range(TW_PX):
        ratio = x / TW_PX
        if ratio > 0.78:
            alpha = int(235 * max(0, 1 - (ratio - 0.78) / 0.22))
        else:
            alpha = 190 + int(45 * ratio)
        for y in range(TH_PX):
            overlay.putpixel((x, y), (10, 20, 40, alpha))
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay)

    buf = BytesIO()
    img.convert('RGB').save(buf, 'JPEG', quality=92)
    buf.seek(0)
    return ImageReader(buf), img.size


def draw_front(c, x0, y0):
    """Draw front cover panel at (x0, y0) in points."""
    w_pt, h_pt = TRIM_W * 72, TRIM_H * 72
    front_img, _ = prep_front_image()

    # Background image
    c.drawImage(front_img, x0, y0, width=w_pt, height=h_pt)

    # Cream overlay at bottom for text readability
    c.saveState()
    c.setFillColor(Color(0.992, 0.984, 0.969, alpha=0.85))
    overlay_h = h_pt * 0.38
    c.rect(x0, y0, w_pt, overlay_h, fill=1, stroke=0)
    c.restoreState()

    # Tag line
    pad = 0.55 * inch
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(GOLD)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(x0 + pad, y0 + h_pt - 1.18 * inch, x0 + pad + 0.42 * inch, y0 + h_pt - 1.18 * inch)
    c.drawString(x0 + pad, y0 + h_pt - 1.10 * inch, "THE COMPLETE SENIOR'S COMPANION")

    # Title
    ty = y0 + h_pt - 1.45 * inch
    c.setFont('Times-Bold', 38)
    c.setFillColor(white)
    c.drawString(x0 + pad, ty, "AI for the")
    ty -= 0.38 * inch
    c.drawString(x0 + pad, ty, "Golden Years")

    # Subtitle
    ty -= 0.32 * inch
    c.setFont('Times-Roman', 10)
    c.setFillColor(Color(1, 1, 1, alpha=0.88))
    c.drawString(x0 + pad, ty, "Your Friendly Guide to Everyday Magic & Staying Safe")

    # Gold rule
    ty -= 0.22 * inch
    c.setFillColor(GOLD)
    c.roundRect(x0 + pad, ty, 0.45 * inch, 2, 1, fill=1, stroke=0)


def draw_spine(c, x0, y0):
    """Draw spine at (x0, y0)."""
    w_pt, h_pt = SPINE * 72, TRIM_H * 72
    c.setFillColor(DARK_NAVY)
    c.rect(x0, y0, w_pt, h_pt, fill=1, stroke=0)

    # Gold vertical lines
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.setStrokeAlpha(0.3)
    c.line(x0 + 3, y0 + 100, x0 + 3, y0 + h_pt - 100)
    c.line(x0 + w_pt - 3, y0 + 100, x0 + w_pt - 3, y0 + h_pt - 100)
    c.setStrokeAlpha(1.0)

    # Vertical text - use saveState/rotate
    c.saveState()
    c.setFillColor(white)
    c.setFont('Times-Bold', 7)
    # Translate to center of spine, rotate 90 degrees
    cx, cy = x0 + w_pt / 2, y0 + h_pt / 2
    # Draw title (vertically)
    title = "AI for the Golden Years"
    c.translate(cx, cy + 55)
    c.rotate(90)
    c.drawCentredString(0, 0, title)
    c.restoreState()

    c.saveState()
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 4.5)
    c.translate(cx, cy - 70)
    c.rotate(90)
    c.drawCentredString(0, 0, "THE COMPLETE SENIOR'S COMPANION")
    c.restoreState()


def draw_back(c, x0, y0):
    """Draw back cover panel at (x0, y0)."""
    w_pt, h_pt = TRIM_W * 72, TRIM_H * 72
    back_img, _ = prep_back_image()

    # Background image (already dark overlaid)
    c.drawImage(back_img, x0, y0, width=w_pt, height=h_pt)

    pad = 0.55 * inch
    py = y0 + h_pt - 0.90 * inch  # start from top

    # Eyebrow
    c.setFont('Helvetica-Bold', 6.5)
    c.setFillColor(GOLD)
    c.drawString(x0 + pad, py, "TECHNOLOGY FOR SENIORS")
    py -= 16

    # Title
    c.setFont('Times-Bold', 16)
    c.setFillColor(white)
    c.drawString(x0 + pad, py, "Discover the Magic of AI")
    py -= 22
    c.drawString(x0 + pad, py, "\u2014 Without the Confusion")
    py -= 6

    # Gold rule
    c.setFillColor(GOLD)
    c.roundRect(x0 + pad, py, 0.25 * inch, 2, 1, fill=1, stroke=0)
    py -= 12

    # Description text
    c.setFont('Times-Roman', 7.2)
    desc_lines = [
        'Are you hearing about "AI" and "ChatGPT" everywhere',
        "but aren't sure what it means for you? Do you worry",
        "about falling behind \u2014 or being targeted by",
        "sophisticated online scams?",
        "",
        "This warm, easy-to-read guide breaks down complex",
        "technology into simple, everyday language, tailor-made",
        "for seniors who want to embrace the digital age with",
        "confidence and stay safe while doing it.",
    ]
    for line in desc_lines:
        if line:
            c.setFillColor(Color(1, 1, 1, alpha=0.80))
            c.drawString(x0 + pad, py, line)
        py -= 12.5

    py -= 4
    # Bullet points
    c.setFont('Times-Roman', 6.5)
    bullets = [
        "\u2022 What AI really is \u2014 and why it's not science fiction",
        "\u2022 Step-by-step guides to ChatGPT, voice assistants & smart apps",
        "\u2022 How to spot deepfakes, voice clones & protect your privacy",
        '\u2022 The foolproof "Safe Word" strategy against AI scams',
        "\u2022 AI for hobbies, health, travel & staying connected to loved ones",
    ]
    for bullet in bullets:
        c.setFillColor(Color(1, 1, 1, alpha=0.70))
        c.drawString(x0 + pad, py, bullet)
        py -= 11.5

    # Barcode box (bottom right)
    bx = x0 + w_pt - pad - 1.4 * inch
    by = y0 + 1.2 * inch
    c.setStrokeColor(Color(1, 1, 1, alpha=0.15))
    c.setLineWidth(1)
    c.roundRect(bx, by, 1.4 * inch, 0.9 * inch, 4, fill=0, stroke=1)
    c.setFont('Helvetica', 5)
    c.setFillColor(Color(1, 1, 1, alpha=0.25))
    c.drawCentredString(bx + 0.7 * inch, by + 0.55 * inch, "ISBN")
    c.drawCentredString(bx + 0.7 * inch, by + 0.38 * inch, "BARCODE")
    c.drawCentredString(bx + 0.7 * inch, by + 0.21 * inch, "HERE")

    # Copyright
    c.setFont('Times-Roman', 5.5)
    c.setFillColor(Color(1, 1, 1, alpha=0.35))
    c.drawString(x0 + pad, by - 0.25 * inch, "\u00a9 2025 \u2022 All rights reserved")


def main():
    print("Building cover with reportlab native text...")

    w_pt, h_pt = SPREAD_W * inch, SPREAD_H * inch
    pdf_path = os.path.join(OUTPUT, "Cover_KDP.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(w_pt, h_pt))

    # Calculate panel positions
    bl_pt = BLEED * inch
    tw_pt = TRIM_W * inch
    th_pt = TRIM_H * inch
    sp_pt = SPINE * inch

    back_x = bl_pt
    spine_x = bl_pt + tw_pt
    front_x = bl_pt + tw_pt + sp_pt
    panel_y = bl_pt

    # Draw panels
    draw_back(c, back_x, panel_y)
    draw_spine(c, spine_x, panel_y)
    draw_front(c, front_x, panel_y)

    # Trim/crop marks (optional, subtle)
    c.setStrokeColor(Color(0, 0, 0, alpha=0.1))
    c.setLineWidth(0.3)
    c.setDash(4, 4)
    c.rect(bl_pt, bl_pt, tw_pt * 2 + sp_pt, th_pt, fill=0, stroke=1)

    c.showPage()
    c.save()

    mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"Cover PDF: {pdf_path} ({mb:.2f} MB)")
    print(f"Dimensions: {SPREAD_W:.3f}\" x {SPREAD_H:.3f}\" (trim: {TRIM_W}x2 + {SPINE:.3f}\" spine)")
    print("Reportlab native text rendering for crisp typography")


if __name__ == '__main__':
    main()

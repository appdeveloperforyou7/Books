"""
KDP Cover v6 - Cohesive design based on AI image analysis feedback.
Key fixes:
- Back cover: warm cream overlay instead of dark, larger readable text
- Spine: larger, visible text
- Consistent warm color palette across entire spread
- Better text contrast and hierarchy
"""
import os, sys
from io import BytesIO
from PIL import Image, ImageEnhance
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, Color, white, black

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
DARK_CREAM = HexColor('#F0EBE0')
DARK_NAVY = HexColor('#0F1F35')
NAVY = HexColor('#1E2A4A')
DARK_TEXT = HexColor('#2D2D2D')
WARM_DARK = HexColor('#3D3025')


def prep_front_image():
    img = Image.open(FRONT_IMG).convert('RGB')
    if img.size != (TW_PX, TH_PX):
        img = img.resize((TW_PX, TH_PX), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.2)
    buf = BytesIO(); img.save(buf, 'JPEG', quality=95); buf.seek(0)
    return ImageReader(buf)


def prep_back_image():
    """Back cover with warm cream overlay instead of dark."""
    img = Image.open(BACK_IMG).convert('RGBA')
    if img.size != (TW_PX, TH_PX):
        img = img.resize((TW_PX, TH_PX), Image.LANCZOS)

    # Warm cream overlay over the entire image
    overlay = Image.new('RGBA', (TW_PX, TH_PX), (0, 0, 0, 0))
    for x in range(TW_PX):
        ratio = x / TW_PX
        if ratio < 0.3:
            alpha = 240  # fully covered on left
        elif ratio > 0.75:
            alpha = int(240 * max(0, 1 - (ratio - 0.75) / 0.25))
        else:
            alpha = 240 - int(60 * (ratio - 0.3) / 0.45)
        for y in range(TH_PX):
            overlay.putpixel((x, y), (250, 248, 242, alpha))
    img = Image.alpha_composite(img, overlay)
    buf = BytesIO(); img.convert('RGB').save(buf, 'JPEG', quality=92); buf.seek(0)
    return ImageReader(buf)


def draw_front(c, x0, y0):
    """Front cover: photo background + cream bottom overlay + text."""
    w_pt, h_pt = TRIM_W * 72, TRIM_H * 72
    front_img = prep_front_image()

    c.drawImage(front_img, x0, y0, width=w_pt, height=h_pt)

    # Cream fade at bottom
    c.saveState()
    c.setFillColor(Color(0.992, 0.984, 0.969, alpha=0.88))
    c.rect(x0, y0, w_pt, h_pt * 0.35, fill=1, stroke=0)
    c.restoreState()

    pad = 0.55 * inch

    # Gold tag line
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(GOLD)
    c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    tag_y = y0 + h_pt - 1.18 * inch
    c.line(x0 + pad, tag_y, x0 + pad + 0.42 * inch, tag_y)
    c.drawString(x0 + pad, y0 + h_pt - 1.08 * inch, "THE COMPLETE SENIOR'S COMPANION")

    # Title
    c.setFont('Times-Bold', 38)
    c.setFillColor(white)
    ty = y0 + h_pt - 1.50 * inch
    c.drawString(x0 + pad, ty, "AI for the")
    ty -= 0.38 * inch
    c.drawString(x0 + pad, ty, "Golden Years")

    # Subtitle
    ty -= 0.35 * inch
    c.setFont('Times-Roman', 10)
    c.setFillColor(Color(1, 1, 1, alpha=0.88))
    c.drawString(x0 + pad, ty, "Your Friendly Guide to Everyday Magic & Staying Safe")

    # Gold rule
    ty -= 0.24 * inch
    c.setFillColor(GOLD)
    c.roundRect(x0 + pad, ty, 0.45 * inch, 2.5, 1.5, fill=1, stroke=0)


def draw_spine(c, x0, y0):
    """Spine: navy with gold accents, readable vertical text."""
    w_pt, h_pt = SPINE * 72, TRIM_H * 72
    c.setFillColor(DARK_NAVY)
    c.rect(x0, y0, w_pt, h_pt, fill=1, stroke=0)

    c.setStrokeColor(GOLD); c.setLineWidth(0.5)
    c.setStrokeAlpha(0.25)
    c.line(x0 + 3, y0 + 80, x0 + 3, y0 + h_pt - 80)
    c.line(x0 + w_pt - 3, y0 + 80, x0 + w_pt - 3, y0 + h_pt - 80)
    c.setStrokeAlpha(1.0)

    cx, cy = x0 + w_pt / 2, y0 + h_pt / 2

    # Title
    c.saveState()
    c.setFillColor(white)
    c.setFont('Times-Bold', 7.5)
    c.translate(cx, cy + 45)
    c.rotate(90)
    c.drawCentredString(0, 0, "AI for the Golden Years")
    c.restoreState()

    # Subtitle
    c.saveState()
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 5)
    c.translate(cx, cy - 80)
    c.rotate(90)
    c.drawCentredString(0, 0, "THE COMPLETE SENIOR'S COMPANION")
    c.restoreState()


def draw_back(c, x0, y0):
    """Back cover: warm cream overlay, clear readable text."""
    w_pt, h_pt = TRIM_W * 72, TRIM_H * 72
    back_img = prep_back_image()

    c.drawImage(back_img, x0, y0, width=w_pt, height=h_pt)

    pad = 0.55 * inch
    py = y0 + h_pt - 0.70 * inch  # start from near top

    # Eyebrow
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(GOLD)
    c.drawString(x0 + pad, py, "TECHNOLOGY FOR SENIORS")
    py -= 20

    # Title
    c.setFont('Times-Bold', 17)
    c.setFillColor(DARK_TEXT)
    c.drawString(x0 + pad, py, "Discover the Magic of AI")
    py -= 24
    c.setFont('Times-Italic', 14)
    c.setFillColor(HexColor('#555555'))
    c.drawString(x0 + pad, py, "Without the Confusion")
    py -= 8

    # Gold rule
    c.setFillColor(GOLD)
    c.roundRect(x0 + pad, py, 0.25 * inch, 2.5, 1.5, fill=1, stroke=0)
    py -= 16

    # Description
    c.setFont('Times-Roman', 8)
    desc = [
        'Are you hearing about "AI" and "ChatGPT" everywhere',
        "but aren't sure what it means for you? Do you worry",
        "about falling behind — or being targeted by",
        "sophisticated online scams?",
    ]
    for line in desc:
        c.setFillColor(Color(0.18, 0.18, 0.18, alpha=0.85))
        c.drawString(x0 + pad, py, line)
        py -= 14

    py -= 2
    c.setFont('Times-Roman', 7.5)
    desc2 = [
        "This warm, easy-to-read guide breaks down complex",
        "technology into simple, everyday language, tailor-made",
        "for seniors who want to embrace the digital age with",
        "confidence and stay safe while doing it.",
    ]
    for line in desc2:
        c.setFillColor(Color(0.22, 0.22, 0.22, alpha=0.78))
        c.drawString(x0 + pad, py, line)
        py -= 13

    py -= 4
    # Bullets
    c.setFont('Times-Roman', 7)
    bullets = [
        "\u2022 What AI really is — and why it's not science fiction",
        "\u2022 Step-by-step guides to ChatGPT, voice assistants & smart apps",
        "\u2022 How to spot deepfakes, voice clones & protect your privacy",
        '\u2022 The foolproof "Safe Word" strategy against AI scams',
        "\u2022 AI for hobbies, health, travel & staying connected",
    ]
    for bullet in bullets:
        c.setFillColor(Color(0.25, 0.25, 0.25, alpha=0.75))
        c.drawString(x0 + pad, py, bullet)
        py -= 12.5

    # Barcode box (bottom right)
    bx = x0 + w_pt - pad - 1.4 * inch
    by = y0 + 1.0 * inch
    c.setStrokeColor(Color(0.5, 0.45, 0.35, alpha=0.25))
    c.setLineWidth(1.5)
    c.roundRect(bx, by, 1.4 * inch, 0.9 * inch, 6, fill=0, stroke=1)
    c.setFont('Helvetica', 5.5)
    c.setFillColor(Color(0.4, 0.35, 0.25, alpha=0.35))
    c.drawCentredString(bx + 0.7 * inch, by + 0.55 * inch, "ISBN")
    c.drawCentredString(bx + 0.7 * inch, by + 0.38 * inch, "BARCODE")
    c.drawCentredString(bx + 0.7 * inch, by + 0.21 * inch, "HERE")

    # Copyright
    c.setFont('Times-Roman', 6)
    c.setFillColor(Color(0.35, 0.35, 0.35, alpha=0.45))
    c.drawString(x0 + pad, by - 0.3 * inch, "\u00a9 2025 \u2022 All rights reserved")


def main():
    print("Building cover v6 - cohesive warm design...")
    w_pt, h_pt = SPREAD_W * inch, SPREAD_H * inch
    pdf_path = os.path.join(OUTPUT, "Cover_KDP_v6.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(w_pt, h_pt))

    bl_pt = BLEED * inch
    tw_pt = TRIM_W * inch
    th_pt = TRIM_H * inch
    sp_pt = SPINE * inch

    back_x = bl_pt
    spine_x = bl_pt + tw_pt
    front_x = bl_pt + tw_pt + sp_pt
    panel_y = bl_pt

    draw_back(c, back_x, panel_y)
    draw_spine(c, spine_x, panel_y)
    draw_front(c, front_x, panel_y)

    # Subtle trim guide
    c.setStrokeColor(Color(0, 0, 0, alpha=0.06))
    c.setLineWidth(0.3)
    c.setDash(3, 5)
    c.rect(bl_pt, bl_pt, tw_pt * 2 + sp_pt, th_pt, fill=0, stroke=1)

    c.showPage()
    c.save()

    mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"Cover PDF: {pdf_path} ({mb:.2f} MB)")
    print(f"Spread: {SPREAD_W:.3f}\" x {SPREAD_H:.3f}\"")
    print("Cohesive warm palette: cream/gold/navy across entire spread")


if __name__ == '__main__':
    main()

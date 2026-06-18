"""
KDP Cover v8 - Fix KDP errors:
1. All text at least 0.5" from page edges (=0.375" from trim)
2. Better text contrast - larger, bolder, positioned over darkest part of image
3. NO spine text (43 pages < 79 minimum)
"""
import os
from io import BytesIO
from PIL import Image, ImageEnhance
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, Color, white

ASSETS = r"D:\Kapil\Books\First\Assets"
OUTPUT = r"D:\Kapil\Books\First\Output"
FRONT_IMG = os.path.join(ASSETS, "frontcover_current.jpg")

TRIM_W, TRIM_H = 7.0, 10.0
SPINE = 0.108
BLEED = 0.125
SPREAD_W = TRIM_W * 2 + SPINE + BLEED * 2
SPREAD_H = TRIM_H + BLEED * 2
DPI = 300

GOLD = HexColor('#C9913D')
CREAM = HexColor('#FDFBF7')
DARK_NAVY = HexColor('#0F1F35')
DARK_TEXT = HexColor('#2D2D2D')

# Safe margin: 0.5" from page edge = 0.375" from trim
SAFE_MARGIN = 0.50


def prep_front_image():
    img = Image.open(FRONT_IMG).convert('RGB')
    TW_PX = int(TRIM_W * DPI); TH_PX = int(TRIM_H * DPI)
    if img.size != (TW_PX, TH_PX):
        img = img.resize((TW_PX, TH_PX), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.2)
    buf = BytesIO(); img.save(buf, 'JPEG', quality=95); buf.seek(0)
    return ImageReader(buf)


def draw_front(c, x0, y0):
    w_pt, h_pt = TRIM_W * 72, TRIM_H * 72
    front_img = prep_front_image()
    c.drawImage(front_img, x0, y0, width=w_pt, height=h_pt)

    # Dark semi-transparent strip at top for text readability
    c.saveState()
    c.setFillColor(Color(0.04, 0.08, 0.18, alpha=0.55))
    strip_h = 2.8 * inch
    c.rect(x0, y0 + h_pt - strip_h, w_pt, strip_h, fill=1, stroke=0)

    # Lighter fade below the dark strip
    c.setFillColor(Color(0.04, 0.08, 0.18, alpha=0.25))
    c.rect(x0, y0 + h_pt - strip_h - 0.6 * inch, w_pt, 0.6 * inch, fill=1, stroke=0)
    c.restoreState()

    m = SAFE_MARGIN * inch  # 0.5" from page edges

    # Tag line (top of dark strip)
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(GOLD)
    c.setStrokeColor(GOLD); c.setLineWidth(2)
    tag_y = y0 + h_pt - 0.85 * inch
    c.line(x0 + m, tag_y, x0 + m + 0.55 * inch, tag_y)
    c.drawString(x0 + m, y0 + h_pt - 0.72 * inch, "THE COMPLETE SENIOR'S COMPANION")

    # Title - large, white, positioned with safe margins
    c.setFont('Times-Bold', 40)
    c.setFillColor(white)
    ty = y0 + h_pt - 1.40 * inch
    c.drawString(x0 + m, ty, "AI for the")
    ty -= 0.42 * inch
    c.drawString(x0 + m, ty, "Golden Years")

    # Subtitle
    ty -= 0.40 * inch
    c.setFont('Times-Roman', 11)
    c.setFillColor(Color(1, 1, 1, alpha=0.90))
    c.drawString(x0 + m, ty, "Your Friendly Guide to Everyday Magic & Staying Safe")

    # Gold rule
    ty -= 0.28 * inch
    c.setFillColor(GOLD)
    c.roundRect(x0 + m, ty, 0.5 * inch, 3, 1.5, fill=1, stroke=0)


def draw_spine(c, x0, y0):
    """Spine: navy ONLY, NO text (43 pages < 79 minimum)."""
    w_pt, h_pt = SPINE * 72, TRIM_H * 72
    c.setFillColor(DARK_NAVY)
    c.rect(x0, y0, w_pt, h_pt, fill=1, stroke=0)

    # Subtle gold accent lines only (no text)
    c.setStrokeColor(GOLD); c.setLineWidth(0.4); c.setStrokeAlpha(0.18)
    c.line(x0 + 3, y0 + 80, x0 + 3, y0 + h_pt - 80)
    c.line(x0 + w_pt - 3, y0 + 80, x0 + w_pt - 3, y0 + h_pt - 80)
    c.setStrokeAlpha(1.0)


def draw_back(c, x0, y0):
    """Back cover with 0.5" safe margins around all text."""
    w_pt, h_pt = TRIM_W * 72, TRIM_H * 72
    m = SAFE_MARGIN * inch  # 0.5"

    # Warm cream background
    c.setFillColor(CREAM)
    c.rect(x0, y0, w_pt, h_pt, fill=1, stroke=0)

    # Subtle warm accent at top
    c.saveState()
    c.setFillColor(HexColor('#F0EBE0'))
    c.rect(x0, y0 + h_pt - 0.25 * inch, w_pt, 0.25 * inch, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(2)
    c.line(x0 + m, y0 + h_pt - 0.30 * inch, x0 + w_pt - m, y0 + h_pt - 0.30 * inch)
    c.restoreState()

    py = y0 + h_pt - 0.70 * inch

    # Eyebrow
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(GOLD)
    c.drawString(x0 + m, py, "T E C H N O L O G Y   F O R   S E N I O R S")
    py -= 24

    # Main title
    c.setFont('Times-Bold', 19)
    c.setFillColor(DARK_NAVY)
    c.drawString(x0 + m, py, "Discover the Magic of AI")
    py -= 28
    c.setFont('Times-Italic', 14)
    c.setFillColor(GOLD)
    c.drawString(x0 + m, py, "Without the Confusion")
    py -= 14

    # Divider
    c.setStrokeColor(GOLD); c.setLineWidth(2)
    c.line(x0 + m, py, x0 + m + 0.7 * inch, py)
    py -= 24

    # Description
    c.setFont('Times-Roman', 8.5)
    desc = [
        "Are you hearing about \"AI\" and \"ChatGPT\" but",
        "aren't quite sure what it all means for you?",
        "You're not alone \u2014 and you're in the right place.",
    ]
    for line in desc:
        c.setFillColor(DARK_TEXT)
        c.drawString(x0 + m, py, line)
        py -= 16

    py -= 4
    c.setFont('Times-Roman', 8)
    desc2 = [
        "This warm guide is written specifically for seniors",
        "and older adults who want to understand artificial",
        "intelligence without technical jargon. Packed with",
        "step-by-step instructions, real-world examples, and",
        "essential safety tips \u2014 this book will help you",
        "embrace the digital age with confidence.",
    ]
    for line in desc2:
        c.setFillColor(HexColor('#4A4A4A'))
        c.drawString(x0 + m, py, line)
        py -= 14

    py -= 6
    # Bullets
    c.setFont('Helvetica', 7.5)
    bullets = [
        ("\u25C6", "How to use ChatGPT, voice assistants & smart apps"),
        ("\u25C6", "Spot deepfakes, voice clones & online scams"),
        ("\u25C6", 'The foolproof "Safe Word" family strategy'),
        ("\u25C6", "AI for health, hobbies, travel & staying connected"),
    ]
    for symbol, bullet in bullets:
        c.setFillColor(GOLD)
        c.drawString(x0 + m, py, symbol)
        c.setFillColor(Color(0.22, 0.22, 0.22, alpha=0.88))
        c.drawString(x0 + m + 16, py, bullet)
        py -= 15

    # Quote
    py -= 6
    c.setFont('Times-Italic', 8.5)
    c.setFillColor(GOLD)
    c.drawString(x0 + m, py, '\u201cFinally, a tech book that actually speaks my language.\u201d')
    py -= 18
    c.setFont('Helvetica', 7)
    c.setFillColor(HexColor('#707070'))
    c.drawString(x0 + m + 10, py, "\u2014 Perfect for beginners of any age")

    # Barcode area (lower right, within safe margins)
    bx = x0 + w_pt - m - 1.5 * inch  # m from right edge
    by = y0 + m + 0.15 * inch         # well above bottom margin
    c.setStrokeColor(Color(0.55, 0.50, 0.40, alpha=0.30))
    c.setLineWidth(1.5)
    c.roundRect(bx, by, 1.5 * inch, 1.0 * inch, 6, fill=0, stroke=1)
    c.setFont('Helvetica', 6)
    c.setFillColor(Color(0.40, 0.40, 0.40, alpha=0.45))
    c.drawCentredString(bx + 0.75 * inch, by + 0.60 * inch, "ISBN")
    c.drawCentredString(bx + 0.75 * inch, by + 0.42 * inch, "BARCODE")
    c.drawCentredString(bx + 0.75 * inch, by + 0.24 * inch, "AREA")

    # Copyright (left side, same vertical level as barcode)
    c.setFont('Times-Roman', 6.5)
    c.setFillColor(Color(0.45, 0.45, 0.45, alpha=0.50))
    c.drawString(x0 + m, by + 0.10 * inch, "\u00a9 2025 \u2022 All rights reserved")


def main():
    print("Building cover v8 - KDP compliant...")
    w_pt, h_pt = SPREAD_W * inch, SPREAD_H * inch
    pdf_path = os.path.join(OUTPUT, "Cover_KDP.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(w_pt, h_pt))

    bl_pt = BLEED * inch
    tw_pt = TRIM_W * inch; th_pt = TRIM_H * inch; sp_pt = SPINE * inch

    draw_back(c, bl_pt, bl_pt)
    draw_spine(c, bl_pt + tw_pt, bl_pt)
    draw_front(c, bl_pt + tw_pt + sp_pt, bl_pt)

    # Trim guide (very subtle)
    c.setStrokeColor(Color(0, 0, 0, alpha=0.04))
    c.setLineWidth(0.2); c.setDash(3, 6)
    c.rect(bl_pt, bl_pt, tw_pt * 2 + sp_pt, th_pt, fill=0, stroke=1)

    c.showPage()
    c.save()

    mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"Cover PDF: {pdf_path} ({mb:.2f} MB)")
    print("Safe margin: 0.50\" from all edges")
    print("Spine: no text (43 pages)")


if __name__ == '__main__':
    main()

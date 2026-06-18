"""
KDP Cover v7 - Professional redesign.
Front: photo background + text overlay (kept from before)
Spine: navy + gold text  
Back: CLEAN typographic design with warm cream/gold theme
NO dark/wrong image on back cover.
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
WARM_BG = HexColor('#F8F5EE')
DARK_NAVY = HexColor('#0F1F35')
DARK_TEXT = HexColor('#2D2D2D')
LIGHT_GOLD = HexColor('#E8D5B0')
MEDIUM_TEXT = HexColor('#4A4A4A')


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



    pad = 0.55 * inch

    c.setFont('Helvetica-Bold', 7.5)
    c.setFillColor(GOLD)
    c.setStrokeColor(GOLD); c.setLineWidth(2)
    tag_y = y0 + h_pt - 0.72 * inch
    c.line(x0 + pad, tag_y, x0 + pad + 0.48 * inch, tag_y)
    c.drawString(x0 + pad, y0 + h_pt - 0.60 * inch, "THE COMPLETE SENIOR'S COMPANION")

    c.setFont('Times-Bold', 38)
    c.setFillColor(white)
    ty = y0 + h_pt - 1.02 * inch
    c.drawString(x0 + pad, ty, "AI for the")
    ty -= 0.38 * inch
    c.drawString(x0 + pad, ty, "Golden Years")

    ty -= 0.35 * inch
    c.setFont('Times-Roman', 10)
    c.setFillColor(Color(1, 1, 1, alpha=0.88))
    c.drawString(x0 + pad, ty, "Your Friendly Guide to Everyday Magic & Staying Safe")

    ty -= 0.24 * inch
    c.setFillColor(GOLD)
    c.roundRect(x0 + pad, ty, 0.45 * inch, 2.5, 1.5, fill=1, stroke=0)


def draw_spine(c, x0, y0):
    w_pt, h_pt = SPINE * 72, TRIM_H * 72
    c.setFillColor(DARK_NAVY)
    c.rect(x0, y0, w_pt, h_pt, fill=1, stroke=0)

    c.setStrokeColor(GOLD); c.setLineWidth(0.5)
    c.setStrokeAlpha(0.25)
    c.line(x0 + 3, y0 + 80, x0 + 3, y0 + h_pt - 80)
    c.line(x0 + w_pt - 3, y0 + 80, x0 + w_pt - 3, y0 + h_pt - 80)
    c.setStrokeAlpha(1.0)

    cx, cy = x0 + w_pt / 2, y0 + h_pt / 2

    c.saveState()
    c.setFillColor(white)
    c.setFont('Times-Bold', 7.5)
    c.translate(cx, cy + 45)
    c.rotate(90)
    c.drawCentredString(0, 0, "AI for the Golden Years")
    c.restoreState()

    c.saveState()
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 5)
    c.translate(cx, cy - 80)
    c.rotate(90)
    c.drawCentredString(0, 0, "THE COMPLETE SENIOR'S COMPANION")
    c.restoreState()


def draw_back(c, x0, y0):
    """Clean typographic back cover - no photo."""
    w_pt, h_pt = TRIM_W * 72, TRIM_H * 72
    pad = 0.55 * inch

    # Warm cream background with subtle top gradient
    c.saveState()
    c.setFillColor(CREAM)
    c.rect(x0, y0, w_pt, h_pt, fill=1, stroke=0)

    # Subtle warm accent at top
    c.setFillColor(LIGHT_GOLD)
    c.setFillAlpha(0.3)
    c.rect(x0, y0 + h_pt - 0.3 * inch, w_pt, 0.3 * inch, fill=1, stroke=0)
    c.setFillAlpha(1.0)

    # Gold accent line at top
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(x0 + pad, y0 + h_pt - 0.35 * inch, x0 + w_pt - pad, y0 + h_pt - 0.35 * inch)
    c.restoreState()

    py = y0 + h_pt - 0.70 * inch

    # Eyebrow
    c.setFont('Helvetica-Bold', 7.5)
    c.setFillColor(GOLD)
    c.drawString(x0 + pad, py, "T E C H N O L O G Y   F O R   S E N I O R S")
    py -= 22

    # Main title
    c.setFont('Times-Bold', 18)
    c.setFillColor(DARK_NAVY)
    c.drawString(x0 + pad, py, "Discover the Magic of AI")
    py -= 26
    c.setFont('Times-Italic', 14)
    c.setFillColor(GOLD)
    c.drawString(x0 + pad, py, "Without the Confusion")
    py -= 12

    # Divider
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(x0 + pad, py, x0 + pad + 0.6 * inch, py)
    py -= 20

    # Description
    c.setFont('Times-Roman', 8.5)
    desc = [
        'Are you hearing about "AI" and "ChatGPT" but',
        "aren't quite sure what it all means for you?",
        "You're not alone \u2014 and you're in the right place.",
    ]
    for line in desc:
        c.setFillColor(DARK_TEXT)
        c.drawString(x0 + pad, py, line)
        py -= 15

    py -= 4
    c.setFont('Times-Roman', 8)
    desc2 = [
        "This warm, easy-to-read guide is written specifically",
        "for seniors and older adults who want to understand",
        "artificial intelligence without technical jargon.",
        "Packed with step-by-step instructions, real-world",
        "examples, and essential safety tips \u2014 this book",
        "will help you embrace the digital age with confidence.",
    ]
    for line in desc2:
        c.setFillColor(MEDIUM_TEXT)
        c.drawString(x0 + pad, py, line)
        py -= 14

    py -= 6
    # Bullet points
    c.setFont('Helvetica', 7)
    bullets = [
        ("\u25C6", "How to use ChatGPT, voice assistants & smart apps"),
        ("\u25C6", "Spot deepfakes, voice clones & online scams"),
        ("\u25C6", 'The foolproof "Safe Word" family strategy'),
        ("\u25C6", "AI for health, hobbies, travel & staying connected"),
    ]
    for symbol, bullet in bullets:
        c.setFillColor(GOLD)
        c.drawString(x0 + pad, py, symbol)
        c.setFillColor(Color(0.22, 0.22, 0.22, alpha=0.85))
        c.drawString(x0 + pad + 15, py, bullet)
        py -= 14

    py -= 8
    # Pull quote / selling point
    c.setFont('Times-Italic', 8)
    c.setFillColor(GOLD)
    cx_ref = x0 + pad
    c.drawString(cx_ref, py, '\u201cFinally, a tech book that actually speaks my language.\u201d')
    py -= 16
    c.setFont('Helvetica', 6.5)
    c.setFillColor(Color(0.4, 0.4, 0.4))
    c.drawString(cx_ref + 10, py, "\u2014 Perfect for beginners of any age")

    # Barcode area
    bx = x0 + w_pt - pad - 1.5 * inch
    by = y0 + 0.9 * inch
    c.setStrokeColor(Color(0.6, 0.55, 0.45, alpha=0.3))
    c.setLineWidth(1)
    c.roundRect(bx, by, 1.5 * inch, 1.0 * inch, 6, fill=0, stroke=1)
    c.setFont('Helvetica', 5.5)
    c.setFillColor(Color(0.4, 0.4, 0.4, alpha=0.4))
    c.drawCentredString(bx + 0.75 * inch, by + 0.60 * inch, "ISBN")
    c.drawCentredString(bx + 0.75 * inch, by + 0.42 * inch, "BARCODE")
    c.drawCentredString(bx + 0.75 * inch, by + 0.24 * inch, "AREA")

    # Copyright
    c.setFont('Times-Roman', 6)
    c.setFillColor(Color(0.4, 0.4, 0.4, alpha=0.5))
    c.drawString(x0 + pad, by - 0.3 * inch, "\u00a9 2025 \u2022 All rights reserved")


def main():
    print("Building cover v7 - clean typographic back cover...")
    w_pt, h_pt = SPREAD_W * inch, SPREAD_H * inch
    pdf_path = os.path.join(OUTPUT, "Cover_KDP_v7.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(w_pt, h_pt))

    bl_pt = BLEED * inch
    tw_pt = TRIM_W * inch; th_pt = TRIM_H * inch; sp_pt = SPINE * inch

    draw_back(c, bl_pt, bl_pt)
    draw_spine(c, bl_pt + tw_pt, bl_pt)
    draw_front(c, bl_pt + tw_pt + sp_pt, bl_pt)

    # Trim guide
    c.setStrokeColor(Color(0, 0, 0, alpha=0.04))
    c.setLineWidth(0.2)
    c.setDash(3, 6)
    c.rect(bl_pt, bl_pt, tw_pt * 2 + sp_pt, th_pt, fill=0, stroke=1)

    c.showPage()
    c.save()

    mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"Cover PDF: {pdf_path} ({mb:.2f} MB)")


if __name__ == '__main__':
    main()

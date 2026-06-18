"""
KDP Cover v9 - Fix KDP rejection errors:
1. Front cover image extends 0.125" into bleed on all sides (right, top, bottom)
2. Back cover background extends 0.125" into bleed on all sides (left, top, bottom)
3. NO trim guides, NO template text
4. Spine: navy with no text (43 pages < 79 minimum)
5. All text within 0.5" safe margin from trim edges
6. All fonts embedded via TTF (no Type1 base fonts)
"""
import os
from io import BytesIO
from PIL import Image, ImageEnhance
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = r"D:\Kapil\Books\AI for the Golden Years"
ASSETS = os.path.join(BASE, "Assets")
OUTPUT = os.path.join(BASE, "Output")
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

SAFE_MARGIN = 0.50

FONT_DIR = "C:/Windows/Fonts"

def register_fonts():
    """Register TTF fonts so they are embedded in the PDF."""
    fonts = [
        ("Arial",       os.path.join(FONT_DIR, "arial.ttf")),
        ("ArialBold",   os.path.join(FONT_DIR, "arialbd.ttf")),
        ("Georgia",     os.path.join(FONT_DIR, "georgia.ttf")),
        ("GeorgiaBold", os.path.join(FONT_DIR, "georgiab.ttf")),
        ("GeorgiaItalic", os.path.join(FONT_DIR, "georgiai.ttf")),
    ]
    for name, path in fonts:
        pdfmetrics.registerFont(TTFont(name, path))


def _fix_unembedded_fonts(pdf_path):
    """Replace any unembedded Type1 base fonts in the PDF Resources with
    their embedded TTF equivalents, updating the content stream references."""
    try:
        import pikepdf
        pdf = pikepdf.open(pdf_path, allow_overwriting_input=True)
        page = pdf.pages[0]
        fonts = page.Resources.Font

        # Find unembedded Type1 fonts
        unembedded = {}
        for fname, fobj in dict(fonts).items():
            if str(fobj.get('/Subtype', '')) == '/Type1':
                unembedded[fname] = str(fobj.get('/BaseFont', '/Helvetica'))

        if not unembedded:
            pdf.close()
            return

        # Map each unembedded font to an embedded TTF replacement
        replacements = {}
        for ufname, ubase in unembedded.items():
            for efname, efobj in dict(fonts).items():
                if str(efobj.get('/Subtype', '')) == '/TrueType':
                    ebase = str(efobj.get('/BaseFont', ''))
                    if (ubase.startswith('/Helvetica') and 'Arial' in ebase) or \
                       (ubase.startswith('/Times') and 'Georgia' in ebase) or \
                       (ubase.startswith('/Zapf') and 'Arial' in ebase):
                        replacements[ufname] = efname
                        break

        if not replacements:
            pdf.close()
            return

        # Replace references in the content stream
        raw = page.Contents.read_bytes()
        content = raw.decode('latin-1', errors='replace')
        for old_name, new_name in replacements.items():
            content = content.replace(old_name, new_name)
        page.Contents = pdf.make_stream(content.encode('latin-1'))

        # Remove the now-unreferenced Type1 font entries
        for ufname in replacements:
            del fonts[ufname]

        pdf.save(pdf_path + ".tmp")
        pdf.close()
        os.replace(pdf_path + ".tmp", pdf_path)
        print("  Stripped unembedded Type1 fonts, replaced with embedded TTF")
    except Exception as e:
        print(f"  Warning: font fix skipped ({e})")


def prep_front_image():
    """Resize front image to include bleed on right, top, and bottom edges."""
    img = Image.open(FRONT_IMG).convert('RGB')
    # Include bleed: right edge (+BLEED), top and bottom (+2*BLEED total)
    w_px = int((TRIM_W + BLEED) * DPI)
    h_px = int((TRIM_H + BLEED * 2) * DPI)
    if img.size != (w_px, h_px):
        img = img.resize((w_px, h_px), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.2)
    buf = BytesIO()
    img.save(buf, 'JPEG', quality=95)
    buf.seek(0)
    return ImageReader(buf)


def draw_front(c, x0, y0):
    """Front cover: image extends into right/top/bottom bleed."""
    w_img = (TRIM_W + BLEED) * inch   # extends into right bleed
    h_img = (TRIM_H + BLEED * 2) * inch  # extends into top and bottom bleed
    w_trim = TRIM_W * inch
    h_trim = TRIM_H * inch

    front_img = prep_front_image()
    # Draw image starting from y=0 (bottom bleed) and extending past trim into right/top bleed
    c.drawImage(front_img, x0, 0, width=w_img, height=h_img)

    # Dark semi-transparent strip at top for text readability (trim-width only)
    c.saveState()
    c.setFillColor(Color(0.04, 0.08, 0.18, alpha=0.55))
    strip_h = 2.8 * inch
    c.rect(x0, y0 + h_trim - strip_h, w_trim, strip_h, fill=1, stroke=0)

    c.setFillColor(Color(0.04, 0.08, 0.18, alpha=0.25))
    c.rect(x0, y0 + h_trim - strip_h - 0.6 * inch, w_trim, 0.6 * inch, fill=1, stroke=0)
    c.restoreState()

    m = SAFE_MARGIN * inch

    c.setFont('ArialBold', 8)
    c.setFillColor(GOLD)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    tag_y = y0 + h_trim - 0.85 * inch
    c.line(x0 + m, tag_y, x0 + m + 0.55 * inch, tag_y)
    c.drawString(x0 + m, y0 + h_trim - 0.72 * inch, "THE COMPLETE SENIOR'S COMPANION")

    c.setFont('GeorgiaBold', 40)
    c.setFillColor(white)
    ty = y0 + h_trim - 1.40 * inch
    c.drawString(x0 + m, ty, "AI for the")
    ty -= 0.42 * inch
    c.drawString(x0 + m, ty, "Golden Years")

    ty -= 0.40 * inch
    c.setFont('Georgia', 11)
    c.setFillColor(Color(1, 1, 1, alpha=0.90))
    c.drawString(x0 + m, ty, "Your Friendly Guide to Everyday Magic & Staying Safe")

    ty -= 0.28 * inch
    c.setFillColor(GOLD)
    c.roundRect(x0 + m, ty, 0.5 * inch, 3, 1.5, fill=1, stroke=0)


def draw_spine(c, x0, y0):
    """Spine: navy fills into top/bottom bleed, no text (43 pages < 79)."""
    w_pt = SPINE * inch
    h_pt = (TRIM_H + BLEED * 2) * inch  # extends into top and bottom bleed
    c.setFillColor(DARK_NAVY)
    c.rect(x0, 0, w_pt, h_pt, fill=1, stroke=0)

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.4)
    c.setStrokeAlpha(0.18)
    c.line(x0 + 3, y0 + 80, x0 + 3, y0 + TRIM_H * inch - 80)
    c.line(x0 + w_pt - 3, y0 + 80, x0 + w_pt - 3, y0 + TRIM_H * inch - 80)
    c.setStrokeAlpha(1.0)


def draw_back(c, x0, y0):
    """Back cover: cream background extends into left/top/bottom bleed."""
    w_trim = TRIM_W * inch
    h_trim = TRIM_H * inch
    m = SAFE_MARGIN * inch

    # Cream background extends into left, top, and bottom bleed
    c.setFillColor(CREAM)
    c.rect(0, 0,
           x0 + w_trim,              # from page left edge to trim end of back panel
           h_trim + BLEED * 2 * inch,  # full height including top/bottom bleed
           fill=1, stroke=0)

    # Subtle warm accent at top (trim-width)
    c.saveState()
    c.setFillColor(HexColor('#F0EBE0'))
    c.rect(x0, y0 + h_trim - 0.25 * inch, w_trim, 0.25 * inch, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(x0 + m, y0 + h_trim - 0.30 * inch, x0 + w_trim - m, y0 + h_trim - 0.30 * inch)
    c.restoreState()

    py = y0 + h_trim - 0.70 * inch

    c.setFont('ArialBold', 8)
    c.setFillColor(GOLD)
    c.drawString(x0 + m, py, "T E C H N O L O G Y   F O R   S E N I O R S")
    py -= 24

    c.setFont('GeorgiaBold', 19)
    c.setFillColor(DARK_NAVY)
    c.drawString(x0 + m, py, "Discover the Magic of AI")
    py -= 28
    c.setFont('GeorgiaItalic', 14)
    c.setFillColor(GOLD)
    c.drawString(x0 + m, py, "Without the Confusion")
    py -= 14

    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(x0 + m, py, x0 + m + 0.7 * inch, py)
    py -= 24

    c.setFont('Georgia', 8.5)
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
    c.setFont('Georgia', 8)
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
    c.setFont('Arial', 7.5)
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

    py -= 6
    c.setFont('GeorgiaItalic', 8.5)
    c.setFillColor(GOLD)
    c.drawString(x0 + m, py, '\u201cFinally, a tech book that actually speaks my language.\u201d')
    py -= 18
    c.setFont('Arial', 7)
    c.setFillColor(HexColor('#707070'))
    c.drawString(x0 + m + 10, py, "\u2014 Perfect for beginners of any age")

    bx = x0 + w_trim - m - 1.5 * inch
    by = y0 + m + 0.15 * inch
    c.setStrokeColor(Color(0.55, 0.50, 0.40, alpha=0.30))
    c.setLineWidth(1.5)
    c.roundRect(bx, by, 1.5 * inch, 1.0 * inch, 6, fill=0, stroke=1)
    c.setFont('Arial', 6)
    c.setFillColor(Color(0.40, 0.40, 0.40, alpha=0.45))
    c.drawCentredString(bx + 0.75 * inch, by + 0.60 * inch, "ISBN")
    c.drawCentredString(bx + 0.75 * inch, by + 0.42 * inch, "BARCODE")
    c.drawCentredString(bx + 0.75 * inch, by + 0.24 * inch, "AREA")

    c.setFont('Georgia', 6.5)
    c.setFillColor(Color(0.45, 0.45, 0.45, alpha=0.50))
    c.drawString(x0 + m, by + 0.10 * inch, "\u00a9 2025 \u2022 All rights reserved")


def main(format_name="Paperback"):
    print(f"Building cover v9 - KDP {format_name} bleed-compliant...")
    print("Registering embedded TTF fonts...")
    register_fonts()

    w_pt = SPREAD_W * inch
    h_pt = SPREAD_H * inch
    pdf_path = os.path.join(OUTPUT, f"Cover_KDP_{format_name}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(w_pt, h_pt))

    bl_pt = BLEED * inch
    tw_pt = TRIM_W * inch
    sp_pt = SPINE * inch

    draw_back(c, bl_pt, bl_pt)
    draw_spine(c, bl_pt + tw_pt, bl_pt)
    draw_front(c, bl_pt + tw_pt + sp_pt, bl_pt)

    c.showPage()
    c.save()

    _fix_unembedded_fonts(pdf_path)

    mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"Cover PDF: {pdf_path} ({mb:.2f} MB)")
    print(f"Spread: {SPREAD_W:.4f}\" x {SPREAD_H:.4f}\" (inc. {BLEED:.3f}\" bleed all sides)")
    print(f"Trim area: {TRIM_W * 2 + SPINE:.4f}\" x {TRIM_H:.4f}\"")
    print(f"Safe margin: 0.50\" from all trim edges")
    print(f"No trim guides, no template text")
    print("Bleed extension: backgrounds fill entire bleed zone on all sides")
    print(f"Spine: navy background only, no text ({SPINE:.3f}\")")


if __name__ == '__main__':
    main()

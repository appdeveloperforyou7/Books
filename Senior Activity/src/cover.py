"""Full KDP cover: back + spine + front + bleed, with the required badges.

Spine width is derived from the interior page count (cream ~= pages x 0.0025").
Spine text is shown only when the book is thick enough (>= 80 pp, per KDP).
"""
from __future__ import annotations
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader

from . import config as C
from .fonts import register_fonts
from . import cover_art

CREAM = HexColor("#F5EFE0")
INK = HexColor("#1A1A1A")


def _g(v=0):
    return Color(v, v, v)


def build_cover(theme, page_count: int, total_puzzles: int, out_path: str) -> None:
    register_fonts()
    spine_in = max(page_count * 0.0025, 0.0)
    spine_pt = spine_in * 72
    # full wrap = left bleed + back + spine + front + right bleed
    W = 2 * C.TRIM_W + 2 * C.BLEED + spine_pt
    H = C.TRIM_H + 2 * C.BLEED
    c = canvas.Canvas(out_path, pagesize=(W, H))
    accent = theme.accent

    front_x0 = C.BLEED + C.TRIM_W + spine_pt
    back_trim_x0 = C.BLEED

    # ----- backgrounds -----
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # spine band
    c.setFillColor(accent)
    c.rect(C.BLEED + C.TRIM_W, 0, spine_pt, H, stroke=0, fill=1)

    # front top accent band
    c.setFillColor(accent)
    c.rect(front_x0, H - C.BLEED - 1.3 * 72, C.TRIM_W + C.BLEED, 1.3 * 72,
           stroke=0, fill=1)
    # back top accent band
    c.rect(0, H - C.BLEED - 1.3 * 72, back_trim_x0 + C.TRIM_W, 1.3 * 72,
           stroke=0, fill=1)

    # ===== FRONT COVER (family template) =====
    # Series-brand lead: the CATEGORY is the dominant title (same on all 10);
    # the theme is downgraded and always paired with the volume number. Bigger
    # hero shows the couple doing puzzles; crisp tiles show the game types.
    GOLD = HexColor("#E8A317")
    fcx = front_x0 + C.TRIM_W / 2
    band_bot = H - C.BLEED - 1.3 * 72

    # top banner (fixed): LARGE PRINT - the #1 keyword
    c.setFillColor(CREAM)
    c.setFont(C.F_BOLD, 34)
    c.drawCentredString(fcx, H - C.BLEED - 0.8 * 72, "LARGE PRINT")

    # dominant series title (fixed): the memory/brain identity leads
    c.setFillColor(accent)
    c.setFont(C.F_BOLD, 30)
    c.drawCentredString(fcx, band_bot - 40, "MEMORY & BRAIN GAMES")
    c.setFont(C.F_BOLD, 15)
    c.drawCentredString(fcx, band_bot - 66, "FOR SENIORS")

    # theme DOWNGRADED + paired with volume (varies)
    c.setFillColor(_g(0.4))
    c.setFont(C.F_SEMI, 14)
    c.drawCentredString(fcx, band_bot - 94,
                        f"Volume {theme.volume}   -   {theme.title}")

    # hero (varies) - bigger, the couple doing puzzles
    art_path = C.OUTPUT_DIR / theme.key / "art" / "hero.png"
    if art_path.exists():
        _draw_hero(c, str(art_path), fcx, 410, box=215)
    else:
        cover_art.draw_band(c, fcx, 410, accent, tile=56, gap=16)

    # game-type tiles (fixed): word search / sudoku / crossword / maze
    cover_art.draw_band(c, fcx, 262, accent, tile=42, gap=10)

    # gold value seal (fixed)
    _draw_seal(c, front_x0 + C.TRIM_W - 1.1 * 72, 168, 50, total_puzzles, GOLD)

    # imprint (fixed)
    c.setFillColor(_g(0.4))
    c.setFont(C.F_SEMI, 13)
    c.drawCentredString(fcx, 78, C.IMPRINT)

    # ===== SPINE (text only at >= 80 pp). Lead with the CATEGORY so the
    # memory/activity identity isn't drowned out by the theme title. =====
    if page_count >= 80 and spine_pt > 6:
        c.saveState()
        cx = C.BLEED + C.TRIM_W + spine_pt / 2
        c.translate(cx, 0)
        c.rotate(90)  # +x now runs up the spine; y=0 centers across the width
        c.setFillColor(CREAM)
        c.setFont(C.F_BOLD, 10)
        c.drawCentredString(H * 0.74, 0, "MEMORY & BRAIN GAMES")
        c.setFont(C.F_BOLD, 13)
        c.drawCentredString(H * 0.47, 0,
                            f"VOL {theme.volume}  -  {theme.title.upper()}")
        c.setFont(C.F_SEMI, 9)
        c.drawCentredString(H * 0.13, 0, C.IMPRINT.upper())
        c.restoreState()

    # ===== BACK COVER =====
    bx0 = back_trim_x0
    bw = C.TRIM_W
    c.setFillColor(INK)
    c.setFont(C.F_BOLD, 20)
    c.drawString(bx0 + 0.4 * 72, H - C.BLEED - 1.3 * 72 - 50, "About this book")
    c.setFillColor(accent)
    c.setFont(C.F_SEMI, 13)
    c.drawString(bx0 + 0.4 * 72, H - C.BLEED - 1.3 * 72 - 72,
                 f"Volume {theme.volume}  -  {theme.title}")
    blurb = [
        f"{total_puzzles}+ large-print brain games and puzzles for adults and seniors:",
        "word search, sudoku, crosswords, word scrambles, trivia,",
        "finish-the-phrase, mazes and relaxing coloring pages - plus a page",
        "of traditional Home Remedies & Wellness Wisdom.",
        "",
        "Three gentle levels - Easy, Medium, and Challenger - with answer",
        "keys at the back. Extra-large type on every page, designed to keep",
        "the mind active and the memory sharp.",
        "",
        "A perfect gift for mom, dad, or grandparents.",
    ]
    c.setFont(C.F_REG, 13)
    yy = H - C.BLEED - 1.3 * 72 - 98
    for line in blurb:
        c.drawString(bx0 + 0.4 * 72, yy, line)
        yy -= 18

    # KDP prints the ISBN barcode in the bottom-right 2" x 1.2" zone - keep it clear

    # imprint on back
    c.setFillColor(_g(0.4))
    c.setFont(C.F_SEMI, 11)
    c.drawString(bx0 + 0.4 * 72, C.BLEED + 0.42 * 72, C.IMPRINT)

    c.showPage()
    c.save()


def _draw_wrapped_center(c, text, cx, top_y, max_w, leading):
    from reportlab.lib.utils import simpleSplit
    lines = simpleSplit(text, c._fontname, c._fontsize, max_w)
    if not lines:
        lines = [text]
    start = top_y - (len(lines) - 1) * leading / 2 if len(lines) > 1 else top_y
    # anchor: draw upward from top
    y = top_y
    for i, ln in enumerate(lines):
        c.drawCentredString(cx, y, ln)
        y -= leading


def _draw_hero(c, path, cx, cy, box=210):
    img = ImageReader(path)
    iw, ih = img.getSize()
    s = min(box / iw, box / ih)
    dw, dh = iw * s, ih * s
    c.drawImage(img, cx - dw / 2, cy - dh / 2, dw, dh, mask='auto')
    c.setStrokeColor(Color(0.55, 0.55, 0.55))
    c.setLineWidth(1)
    c.roundRect(cx - dw / 2 - 5, cy - dh / 2 - 5, dw + 10, dh + 10, 8,
                stroke=1, fill=0)


def _draw_centered_anchor_bottom(c, cx, text, bottom_y, font, size, max_w,
                                 leading, color):
    """Centered text whose LAST line sits at bottom_y (multi-line grows upward)."""
    from reportlab.lib.utils import simpleSplit
    lines = simpleSplit(text, font, size, max_w)
    c.setFont(font, size)
    c.setFillColor(color)
    y = bottom_y
    for ln in reversed(lines):
        c.drawCentredString(cx, y, ln)
        y += leading


def _draw_seal(c, cx, cy, r, count, gold):
    """Gold value medallion (premium authority + puzzle identity + count)."""
    c.saveState()
    c.setLineWidth(0)
    c.setFillColor(gold)
    c.circle(cx, cy, r, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.circle(cx, cy, r - 7, stroke=0, fill=1)
    c.setFillColor(gold)
    c.circle(cx, cy, r - 10, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont(C.F_BOLD, r * 0.60)
    c.drawCentredString(cx, cy + r * 0.12, f"{count}+")
    c.setFont(C.F_BOLD, r * 0.24)
    c.drawCentredString(cx, cy - r * 0.26, "BRAIN GAMES")
    c.setFont(C.F_SEMI, r * 0.175)
    c.drawCentredString(cx, cy - r * 0.50, "LARGE PRINT")
    c.restoreState()

"""Front matter: title, copyright, welcome/how-to-use, contents, series page."""
from __future__ import annotations
from . import config as C

SERIES_THEMES = [
    "Volume 1 - Gardens, Flowers & Birds",
    "Volume 2 - Food & Kitchen Favorites",
    "Volume 3 - Travel & Places Around the World",
    "Volume 4 - Faith, Hope & Inspiration",
    "Volume 5 - Holidays & Family Celebrations",
    "Volume 6 - Music & Movies",
    "Volume 7 - Nature & the Great Outdoors",
    "Volume 8 - Animals & Pets",
    "Volume 9 - Sports, Games & Hobbies",
    "Volume 10 - Wellness & Healthy Living",
]

DISCLAIMER = ("Traditional home remedies are shared for cultural enjoyment and "
              "general wellbeing. This is not medical advice; consult a "
              "healthcare professional.")


def render(r, theme, total_puzzles: int) -> None:
    # 1) Title page (bare)
    r.new_page(bare=True)
    c = r.c
    c.setFillColor(_g(0.3))
    c.setFont(C.F_SEMI, 16)
    c.drawCentredString(C.TRIM_W / 2, C.TRIM_H - 150, C.SERIES.upper())
    c.setStrokeColor(theme.accent)
    c.setLineWidth(3)
    c.line(C.TRIM_W * 0.32, C.TRIM_H - 175, C.TRIM_W * 0.68, C.TRIM_H - 175)
    c.setFillColor(_g(0))
    _draw_fit_title(c, C.TRIM_W / 2, C.TRIM_H * 0.60, theme.title,
                    C.F_BOLD, C.CONTENT_W)
    c.setFillColor(_g(0.25))
    _draw_fit_title(c, C.TRIM_W / 2, C.TRIM_H * 0.60 - 40, theme.subtitle,
                    C.F_REG, C.CONTENT_W, start=20, floor=13)
    c.setFillColor(_g(0))
    c.setFont(C.F_BOLD, 18)
    c.drawCentredString(C.TRIM_W / 2, C.TRIM_H * 0.46, f"Volume {theme.volume}")
    # badges
    for i, badge in enumerate(["LARGE PRINT",
                               f"{total_puzzles}+ BRAIN GAMES & PUZZLES",
                               "HOME REMEDIES & WELLNESS WISDOM INSIDE"]):
        y = 200 - i * 44
        c.setLineWidth(1.5)
        c.rect(C.TRIM_W * 0.18, y - 6, C.TRIM_W * 0.64, 32, stroke=1, fill=0)
        c.setFont(C.F_BOLD, 15)
        c.drawCentredString(C.TRIM_W / 2, y + 4, badge)
    c.setFont(C.F_SEMI, 14)
    c.drawCentredString(C.TRIM_W / 2, 60, C.IMPRINT)

    # 2) Copyright page
    r.new_page(section="Copyright", numbered=True)
    r.paragraph("Copyright (c) 2026 Bright Mind Press. All rights reserved.",
                C.CONTENT_X, C.CONTENT_Y_TOP - 40, C.CONTENT_W, size=C.SZ_BODY)
    y = C.CONTENT_Y_TOP - 90
    for line in [
        f"{theme.subtitle}: {theme.title}",
        f"Volume {theme.volume} of the {C.SERIES}.",
        "",
        "No part of this publication may be reproduced, stored in a retrieval "
        "system, or transmitted in any form without prior written permission, "
        "except brief quotations in reviews.",
        "",
        "Large-print brain games, puzzles, and memory activities for adults and seniors.",
        "",
        "Imprint: Bright Mind Press",
    ]:
        y = r.paragraph(line, C.CONTENT_X, y, C.CONTENT_W, size=C.SZ_BODY)
    y -= 20
    r.paragraph(DISCLAIMER, C.CONTENT_X, y, C.CONTENT_W,
                font=C.F_ITAL, size=C.SZ_SUB, gray=0.3)

    # 3) Welcome / How to use
    r.new_page(section="Welcome", numbered=True)
    r.centered("Welcome", C.CONTENT_Y_TOP - 20, C.F_BOLD, C.SZ_HEADING)
    y = C.CONTENT_Y_TOP - 70
    paras = [
        "This large-print activity book is made for relaxed, enjoyable brain exercise. "
        "Every page is printed in clear, extra-large type on easy-to-read pages so you "
        "can focus on the fun, not the font.",
        "Puzzles come in three gentle levels: Easy (warm-up), Medium (steady), and "
        "Challenger (a gentle stretch). Work through them in any order you like - there "
        "is no timer and no score, just the pleasure of solving.",
        "You will find word searches, sudoku, crosswords, word scrambles, trivia, mazes, "
        "coloring pages, and two pages of traditional Home Remedies & Wellness Wisdom.",
        "Answer keys for the sudoku, crosswords, scrambles, trivia and mazes are grouped "
        "at the back. (For word searches, the words to find are listed on each page.) "
        "Take your time and enjoy the puzzles!",
    ]
    for p in paras:
        y = r.paragraph(p, C.CONTENT_X, y, C.CONTENT_W, size=C.SZ_BODY)
        y -= 12

    # 4) Series page
    r.new_page(section="The Bright Mind Series", numbered=True)
    r.centered("The Bright Mind Series", C.CONTENT_Y_TOP - 20, C.F_BOLD, C.SZ_HEADING)
    r.centered("Collect all ten themed volumes", C.CONTENT_Y_TOP - 52,
               C.F_ITAL, C.SZ_SUB, gray=0.3)
    y = C.CONTENT_Y_TOP - 100
    c = r.c
    accent = theme.accent
    for line in SERIES_THEMES:
        current = line.startswith(f"Volume {theme.volume} -")
        # drawn bullet (no font-glyph dependency): accent dot for the current
        # volume, light grey dot for the others
        c.setFillColor(accent if current else _g(0.7))
        c.circle(C.CONTENT_X + 18, y + C.SZ_BODY * 0.33,
                 5.0 if current else 3.0, stroke=0, fill=1)
        c.setFillColor(accent if current else _g(0))
        c.setFont(C.F_BOLD if current else C.F_REG, C.SZ_BODY)
        c.drawString(C.CONTENT_X + 34, y, line)
        y -= C.SZ_BODY * 1.7
    c.setFont(C.F_SEMI, 13)
    c.setFillColor(_g(0.3))
    c.drawCentredString(C.TRIM_W / 2, 70, C.IMPRINT)


def _g(v=0):
    from reportlab.lib.colors import Color
    return Color(v, v, v)


def _draw_fit_title(c, cx, y, title, font, max_w, start=46, floor=28):
    """Centered title that auto-shrinks to fit `max_w`; if still too wide at the
    floor, wraps into two width-balanced lines drawn around `y`."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    size = start
    while size > floor and stringWidth(title, font, size) > max_w:
        size -= 1
    if stringWidth(title, font, size) <= max_w:
        c.setFont(font, size)
        c.drawCentredString(cx, y, title)
        return
    # too long for one line even at the floor: split into two balanced lines
    size = floor
    words = title.split()
    best = (None, " ".join(words[:-1]), words[-1])
    for i in range(1, len(words)):
        left, right = " ".join(words[:i]), " ".join(words[i:])
        w = max(stringWidth(left, font, size), stringWidth(right, font, size))
        if best[0] is None or w < best[0]:
            best = (w, left, right)
    _, line1, line2 = best
    while size > 18 and (stringWidth(line1, font, size) > max_w or
                         stringWidth(line2, font, size) > max_w):
        size -= 1
    lh = size * 1.12
    c.setFont(font, size)
    c.drawCentredString(cx, y + lh * 0.55, line1)
    c.drawCentredString(cx, y - lh * 0.45, line2)

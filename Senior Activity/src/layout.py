"""ReportLab layout engine for the interior PDF.

Renderer wraps a Canvas and supplies large-print primitives plus per-activity
drawers (word search, sudoku, scramble, trivia, maze, coloring, remedies) and
compact solutions. Geometry/font sizes come from config (the LAYOUT spec).
"""
from __future__ import annotations
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import Color

from . import config as C
from .fonts import register_fonts
from .puzzles.sudoku import BLOCK as SUDOKU_BLOCK


def _gray(g=0):
    return Color(g, g, g)


REMEDY_DISCLAIMER = ("Traditional home remedies are shared for cultural enjoyment "
                     "and general wellbeing. This is not medical advice; consult a "
                     "healthcare professional.")


class Renderer:
    def __init__(self, path: str, theme, book_title: str):
        register_fonts()
        self.c = canvas.Canvas(path, pagesize=(C.TRIM_W, C.TRIM_H))
        self.theme = theme
        self.book_title = book_title
        self.section = ""
        self.page_num = 0
        self.show_number = True

    # ---------- page machinery ----------
    def _header_footer(self):
        c = self.c
        c.setFont(C.F_REG, C.SZ_FOOTER)
        c.setFillColor(_gray(0.35))
        # header (kept ~28pt below trim top to clear KDP's 0.25" margin)
        c.drawString(C.CONTENT_X, C.TRIM_H - 42, self.section or "")
        c.drawRightString(C.TRIM_W - C.MARGIN_OUT, C.TRIM_H - 42, self.book_title)
        c.setStrokeColor(_gray(0.6))
        c.setLineWidth(0.5)
        c.line(C.CONTENT_X, C.TRIM_H - 48, C.TRIM_W - C.MARGIN_OUT, C.TRIM_H - 48)
        # footer (kept ~28pt above trim bottom)
        c.line(C.CONTENT_X, 44, C.TRIM_W - C.MARGIN_OUT, 44)
        c.drawString(C.CONTENT_X, 32, C.IMPRINT)
        if self.show_number:
            c.drawRightString(C.TRIM_W - C.MARGIN_OUT, 32, str(self.page_num))
        c.setFillColor(_gray(0))

    def new_page(self, section: str | None = None, numbered: bool = True,
                 bare: bool = False):
        if self.page_num > 0:
            self.c.showPage()
        self.page_num += 1
        self.show_number = numbered
        if section is not None:
            self.section = section
        if not bare:
            self._header_footer()

    def finish(self):
        self.c.showPage()
        self.c.save()

    # ---------- text primitives ----------
    def centered(self, text, y, font=C.F_BOLD, size=C.SZ_HEADING, gray=0):
        self.c.setFont(font, size)
        self.c.setFillColor(_gray(gray))
        self.c.drawCentredString(C.TRIM_W / 2, y, text)
        self.c.setFillColor(_gray(0))

    def left(self, text, x, y, font=C.F_REG, size=C.SZ_BODY, gray=0):
        self.c.setFont(font, size)
        self.c.setFillColor(_gray(gray))
        self.c.drawString(x, y, text)
        self.c.setFillColor(_gray(0))

    def paragraph(self, text, x, y, w, font=C.F_REG, size=C.SZ_BODY,
                  leading=None, gray=0):
        leading = leading or size * C.LEADING
        self.c.setFont(font, size)
        self.c.setFillColor(_gray(gray))
        for line in simpleSplit(text, font, size, w):
            self.c.drawString(x, y, line)
            y -= leading
        self.c.setFillColor(_gray(0))
        return y

    # ---------- section divider ----------
    def section_divider(self, label, subtitle=""):
        self.new_page(section=label, numbered=True)
        c = self.c
        c.setFillColor(_gray(0))
        self.centered(label, C.TRIM_H * 0.60, C.F_BOLD, 40)
        if subtitle:
            self._centered_wrap(subtitle, C.TRIM_H * 0.54,
                                C.F_REG, C.SZ_BODY, C.CONTENT_W * 0.8,
                                C.SZ_BODY * 1.4, gray=0.3)
        c.setLineWidth(2)
        c.line(C.TRIM_W * 0.3, C.TRIM_H * 0.46, C.TRIM_W * 0.7, C.TRIM_H * 0.46)

    def _centered_wrap(self, text, center_y, font, size, max_w, leading, gray=0):
        lines = simpleSplit(text, font, size, max_w)
        total = len(lines) * leading
        y = center_y + total / 2 - leading
        self.c.setFont(font, size)
        self.c.setFillColor(_gray(gray))
        for ln in lines:
            self.c.drawCentredString(C.TRIM_W / 2, y, ln)
            y -= leading
        self.c.setFillColor(_gray(0))

    # ---------- word search ----------
    def draw_wordsearch(self, ws):
        c = self.c
        self.centered(ws.title, C.CONTENT_Y_TOP - 8, C.F_BOLD, C.SZ_SECTION)
        size = ws.size
        title_h = 46
        list_h = 120
        avail_h = (C.CONTENT_Y_TOP - C.CONTENT_Y_BOT) - title_h - list_h
        cell = int(min((C.CONTENT_W - 10) / size, avail_h / size))
        grid_w = cell * size
        gx = (C.TRIM_W - grid_w) / 2
        gy = C.CONTENT_Y_BOT + list_h + 20
        fs = min(C.SZ_GRID, int(cell * 0.6))
        c.setFont(C.F_REG, fs)
        c.setLineWidth(0.6)
        c.setStrokeColor(_gray(0.5))
        for r in range(size):
            for col in range(size):
                x = gx + col * cell
                y = gy + (size - 1 - r) * cell
                c.rect(x, y, cell, cell, stroke=1, fill=0)
                ch = ws.grid[r][col]
                c.drawCentredString(x + cell / 2, y + (cell - fs) / 2 + 1, ch)
        # word list (columns) below
        words = [w for w, _ in ws.words]
        self._column_words(words, C.CONTENT_X, C.CONTENT_Y_BOT + list_h - 10)

    def _column_words(self, words, x, top_y):
        c = self.c
        n = len(words)
        cols = 3 if n > 9 else (2 if n > 4 else 1)
        per = (n + cols - 1) // cols
        col_w = C.CONTENT_W / cols
        fs = C.SZ_SUB
        leading = fs * 1.5
        c.setFont(C.F_REG, fs)
        for i, w in enumerate(words):
            ci = i // per
            ri = i % per
            cx = x + ci * col_w
            cy = top_y - ri * leading
            # drawn bullet dot (no font-glyph dependency)
            c.setFillColor(_gray(0.5))
            c.circle(cx + 3, cy + fs * 0.28, 1.8, stroke=0, fill=1)
            c.setFillColor(_gray(0))
            c.drawString(cx + 10, cy, w)

    # ---------- sudoku ----------
    def draw_sudoku(self, s, x, y, cell, source="puzzle", num_size=None):
        c = self.c
        n = s.size
        br, bc = SUDOKU_BLOCK[n]
        num_size = num_size or min(C.SZ_SUDOKU, int(cell * 0.55))
        grid = s.cells if source == "puzzle" else s.solution
        for r in range(n):
            for col in range(n):
                cx = x + col * cell
                cy = y + (n - 1 - r) * cell
                val = grid[r][col]
                if val:
                    bold = source == "puzzle" and s.given[r][col]
                    c.setFont(C.F_BOLD if bold else C.F_REG, num_size)
                    c.drawCentredString(cx + cell / 2, cy + (cell - num_size) / 2 + 1, str(val))
        # cell + region lines
        total = cell * n
        for i in range(n + 1):
            lx = x + i * cell
            thick = (i % bc == 0)
            c.setLineWidth(1.8 if thick else 0.6)
            c.line(lx, y, lx, y + total)
            ly = y + i * cell
            thick = (i % br == 0)
            c.setLineWidth(1.8 if thick else 0.6)
            c.line(x, ly, x + total, ly)
        c.setLineWidth(1)

    # ---------- scramble ----------
    def draw_scramble(self, sc, x, y, w, h, index):
        c = self.c
        c.setFont(C.F_BOLD, C.SZ_BODY)
        c.drawString(x, y + h - 28, f"{index}. Unscramble:")
        c.setFont(C.F_BOLD, C.SZ_GRID + 2)
        c.drawCentredString(x + w / 2, y + h - 64, sc.scrambled)
        # answer boxes
        box = min(34, (w - 40) / len(sc.answer))
        bw = box * len(sc.answer)
        bx = x + (w - bw) / 2
        by = y + h - 120
        c.setLineWidth(1)
        for i in range(len(sc.answer)):
            c.rect(bx + i * box, by, box, box, stroke=1, fill=0)
        if sc.hint:
            c.setFont(C.F_ITAL, C.SZ_SUB)
            c.drawCentredString(x + w / 2, by - 24, f"Hint: {sc.hint}")

    # ---------- trivia ----------
    def draw_trivia(self, t, x, y, w, h, index):
        c = self.c
        c.setFont(C.F_BOLD, C.SZ_BODY)
        c.drawString(x, y + h - 28, f"{index}.")
        yy = self.paragraph(t.prompt, x + 22, y + h - 28, w - 22,
                            font=C.F_BOLD, size=C.SZ_BODY, leading=C.SZ_BODY * 1.3)
        if t.kind == "mc":
            for i, opt in enumerate(t.options):
                yy -= 6
                c.setFont(C.F_REG, C.SZ_BODY)
                c.drawString(x + 30, yy, f"{chr(65+i)})  {opt}")
                yy -= C.SZ_BODY * 1.5
        else:
            yy -= 10
            c.setLineWidth(0.8)
            for _ in range(2):
                c.line(x + 10, yy, x + w - 10, yy)
                yy -= 26

    # ---------- maze ----------
    def draw_maze(self, m, x, y, cell, solve=False):
        from .puzzles.mazes import N as WN, E as WE, S as WS, W as WW
        c = self.c
        c.setLineWidth(2.2)
        c.setStrokeColor(_gray(0))
        for r in range(m.rows):
            for col in range(m.cols):
                px = x + col * cell
                py = y + (m.rows - 1 - r) * cell
                w = m.walls[r][col]
                if w & WN:
                    c.line(px, py + cell, px + cell, py + cell)
                if w & WS:
                    c.line(px, py, px + cell, py)
                if w & WE:
                    c.line(px + cell, py, px + cell, py + cell)
                if w & WW:
                    c.line(px, py, px, py + cell)
        # start/finish labels
        c.setFont(C.F_BOLD, C.SZ_SUB)
        c.drawCentredString(x + cell / 2, y + m.rows * cell + 6, "Start")
        c.drawCentredString(x + (m.cols - 0.5) * cell, y - 18, "Finish")
        if solve:
            c.setStrokeColor(_gray(0.5))
            c.setLineWidth(max(2, cell * 0.18))
            path = m.solution
            pts = [(x + (cc + 0.5) * cell, y + (m.rows - 1 - rr) * cell + cell / 2)
                   for rr, cc in path]
            p = c.beginPath()
            p.moveTo(*pts[0])
            for pt in pts[1:]:
                p.lineTo(*pt)
            c.drawPath(p, stroke=1, fill=0)
            c.setLineWidth(1)

    # ---------- coloring ----------
    def draw_coloring(self, key):
        from .puzzles import coloring
        self.centered("Coloring Page", C.CONTENT_Y_TOP - 8, C.F_BOLD, C.SZ_SECTION)
        margin = 70
        coloring.draw(self.c, key, C.CONTENT_X + margin / 2,
                      C.CONTENT_Y_BOT + 20, C.CONTENT_W - margin,
                      C.CONTENT_Y_TOP - C.CONTENT_Y_BOT - 80)

    # ---------- crossword ----------
    def _cw_grid(self, cw, x, y, cell, source="puzzle", num_size=8, letter_size=18):
        c = self.c
        n = cw.size
        c.setLineWidth(0.8)
        c.setStrokeColor(_gray(0))
        for r in range(n):
            for col in range(n):
                cx = x + col * cell
                cy = y + (n - 1 - r) * cell
                if cw.grid[r][col] is None:
                    c.setFillColor(_gray(0))
                    c.rect(cx, cy, cell, cell, stroke=0, fill=1)
                else:
                    c.setFillColor(_gray(1))
                    c.rect(cx, cy, cell, cell, stroke=1, fill=1)
                    if source == "solution":
                        c.setFillColor(_gray(0))
                        c.setFont(C.F_BOLD, letter_size)
                        c.drawCentredString(cx + cell / 2,
                                            cy + (cell - letter_size) / 2 + 1,
                                            cw.grid[r][col])
                num = cw.numbers.get((r, col))
                if num:
                    c.setFillColor(_gray(0))
                    c.setFont(C.F_REG, num_size)
                    c.drawString(cx + 2, cy + cell - num_size - 2, str(num))
        c.setFillColor(_gray(0))

    def _draw_clues(self, items, x, top_y, w, header):
        c = self.c
        c.setFont(C.F_BOLD, C.SZ_SUB)
        c.drawString(x, top_y, header)
        y = top_y - C.SZ_SUB * 1.7
        c.setFont(C.F_REG, 14)
        for e in items:
            text = f"{e['number']}. {e['clue']} ({len(e['word'])})"
            for line in simpleSplit(text, C.F_REG, 14, w):
                if y < C.CONTENT_Y_BOT + 12:
                    return
                c.drawString(x, y, line)
                y -= 14 * 1.35
            y -= 3

    def draw_crossword_full(self, cw):
        self.centered(cw.title, C.CONTENT_Y_TOP - 8, C.F_BOLD, C.SZ_SECTION)
        n = cw.size
        avail_h = C.CONTENT_Y_TOP - C.CONTENT_Y_BOT
        cell = min((C.CONTENT_W - 20) / n, (avail_h * 0.50) / n)
        gw = cell * n
        gx = (C.TRIM_W - gw) / 2
        gy = C.CONTENT_Y_TOP - 46 - gw
        self._cw_grid(cw, gx, gy, cell, source="puzzle",
                      num_size=max(7, int(cell * 0.28)),
                      letter_size=int(cell * 0.5))
        clue_top = gy - 26
        across = sorted([e for e in cw.entries if e["direction"] == "across"],
                        key=lambda e: e["number"])
        down = sorted([e for e in cw.entries if e["direction"] == "down"],
                      key=lambda e: e["number"])
        col_w = (C.CONTENT_W - 20) / 2
        self._draw_clues(across, C.CONTENT_X, clue_top, col_w, "Across")
        self._draw_clues(down, C.CONTENT_X + col_w + 20, clue_top, col_w, "Down")

    def draw_crossword_solution_half(self, cw, x, y, w, h, index):
        self.c.setFont(C.F_BOLD, C.SZ_SOLUTION + 2)
        self.c.drawString(x, y + h - 22, f"{cw.title} - solution")
        n = cw.size
        cell = min((w - 20) / n, (h - 46) / n)
        gw = cell * n
        gx = x + (w - gw) / 2
        gy = y + 8
        self._cw_grid(cw, gx, gy, cell, source="solution",
                      num_size=6, letter_size=max(8, int(cell * 0.5)))

    # ---------- full-page sudoku / maze ----------
    def draw_sudoku_half(self, s, x, y, w, h, index):
        label = {"easy": "Easy", "medium": "Medium",
                 "challenger": "Challenger"}[s.tier]
        self.c.setFont(C.F_BOLD, C.SZ_SUB)
        self.c.drawString(x, y + h - 26, f"{s.title}  -  {label}")
        n = s.size
        cell = min((w - 30) / n, (h - 60) / n)
        gw = cell * n
        gx = x + (w - gw) / 2
        gy = y + 12
        self.draw_sudoku(s, gx, gy, cell, source="puzzle")

    def draw_maze_full(self, m):
        self.centered(m.title, C.CONTENT_Y_TOP - 8, C.F_BOLD, C.SZ_SECTION)
        avail_h = C.CONTENT_Y_TOP - C.CONTENT_Y_BOT - 80
        cell = min((C.CONTENT_W - 20) / m.cols, avail_h / m.rows)
        gw, gh = cell * m.cols, cell * m.rows
        gx = (C.TRIM_W - gw) / 2
        gy = C.CONTENT_Y_BOT + (avail_h - gh) / 2 + 30
        self.draw_maze(m, gx, gy, cell)

    # ---------- remedies page(s) ----------
    def draw_remedies(self, items, title):
        self.new_page(section="Home Remedies & Wellness Wisdom")
        self.centered(title, C.CONTENT_Y_TOP - 8, C.F_BOLD, C.SZ_SECTION)
        self.c.setFont(C.F_ITAL, C.SZ_SUB)
        self.c.setFillColor(_gray(0.35))
        self.c.drawCentredString(C.TRIM_W / 2, C.CONTENT_Y_TOP - 38,
                                 "Simple, traditional comfort for everyday ailments")
        self.c.setFillColor(_gray(0))
        y = C.CONTENT_Y_TOP - 74
        for i, item in enumerate(items, 1):
            lines = simpleSplit(item["text"], C.F_REG, C.SZ_BODY, C.CONTENT_W - 34)
            block_h = C.SZ_BODY * 1.5 + len(lines) * (C.SZ_BODY * 1.35) + 16
            if y - block_h < C.CONTENT_Y_BOT + 30:
                self.new_page(section="Home Remedies & Wellness Wisdom")
                y = C.CONTENT_Y_TOP - 20
            self.c.setFont(C.F_BOLD, C.SZ_BODY)
            self.c.drawString(C.CONTENT_X + 6, y, f"{i}.  {item['condition']}")
            y -= C.SZ_BODY * 1.5
            y = self.paragraph(item["text"], C.CONTENT_X + 24, y,
                               C.CONTENT_W - 34, size=C.SZ_BODY,
                               leading=C.SZ_BODY * 1.35)
            y -= 14
        # disclaimer box (sized to its text; new page if it won't fit)
        dlines = simpleSplit(REMEDY_DISCLAIMER, C.F_ITAL, C.SZ_SUB, C.CONTENT_W - 40)
        box_h = len(dlines) * (C.SZ_SUB * 1.4) + 40
        if y - box_h - 16 < C.CONTENT_Y_BOT + 10:
            self.new_page(section="Home Remedies & Wellness Wisdom")
            y = C.CONTENT_Y_TOP - 20
        box_top = y - 6
        box_bot = box_top - box_h
        self.c.setLineWidth(1)
        self.c.rect(C.CONTENT_X, box_bot, C.CONTENT_W, box_h, stroke=1, fill=0)
        self.c.setFont(C.F_BOLD, C.SZ_SUB)
        self.c.drawString(C.CONTENT_X + 14, box_top - 22, "Please note:")
        self.paragraph(REMEDY_DISCLAIMER, C.CONTENT_X + 14, box_top - 44,
                       C.CONTENT_W - 28, font=C.F_ITAL, size=C.SZ_SUB,
                       leading=C.SZ_SUB * 1.4, gray=0.2)

    # ---------- compact solution drawers ----------
    def draw_sudoku_solution_half(self, s, x, y, w, h, index):
        self.c.setFont(C.F_BOLD, C.SZ_SOLUTION + 2)
        self.c.drawString(x, y + h - 22, f"{s.title} - solution")
        n = s.size
        cell = min((w - 20) / n, (h - 48) / n)
        gw = cell * n
        gx = x + (w - gw) / 2
        gy = y + 10
        self.draw_sudoku(s, gx, gy, cell, source="solution",
                         num_size=int(cell * 0.5))

    def draw_maze_solution_half(self, m, x, y, w, h, index):
        self.c.setFont(C.F_BOLD, C.SZ_SOLUTION + 2)
        self.c.drawString(x, y + h - 22, f"{m.title} - solution")
        cell = min((w - 30) / m.cols, (h - 60) / m.rows)
        gw, gh = cell * m.cols, cell * m.rows
        gx = x + (w - gw) / 2
        gy = y + (h - 44 - gh) / 2
        self.draw_maze(m, gx, gy, cell, solve=True)

    def flow_lines(self, sections, section_label):
        """Pack (heading, [lines]) text blocks across pages."""
        self.new_page(section=section_label)
        y = C.CONTENT_Y_TOP
        for heading, lines in sections:
            if y < C.CONTENT_Y_BOT + 60:
                self.new_page(section=section_label)
                y = C.CONTENT_Y_TOP
            self.c.setFont(C.F_BOLD, C.SZ_SOLUTION + 2)
            self.c.drawString(C.CONTENT_X, y, heading)
            y -= (C.SZ_SOLUTION + 2) * 1.5
            self.c.setFont(C.F_REG, C.SZ_SOLUTION)
            for ln in lines:
                for sub in simpleSplit(ln, C.F_REG, C.SZ_SOLUTION, C.CONTENT_W - 20):
                    if y < C.CONTENT_Y_BOT + 40:
                        self.new_page(section=section_label)
                        y = C.CONTENT_Y_TOP
                    self.c.drawString(C.CONTENT_X + 10, y, sub)
                    y -= C.SZ_SOLUTION * 1.5
            y -= 10

    # ---------- generic one/two per page ----------
    def one_per_page(self, items, draw_fn, section):
        for it in items:
            self.new_page(section=section)
            draw_fn(it)

    def two_per_page(self, items, draw_fn, section):
        i = 0
        n = len(items)
        while i < n:
            self.new_page(section=section)
            half_h = (C.CONTENT_Y_TOP - C.CONTENT_Y_BOT) / 2
            for slot in range(2):
                if i >= n:
                    break
                y = C.CONTENT_Y_TOP - half_h if slot == 0 else C.CONTENT_Y_BOT
                draw_fn(items[i], C.CONTENT_X, y, C.CONTENT_W, half_h, i + 1)
                i += 1

    def four_per_page(self, items, draw_fn, section):
        i = 0
        n = len(items)
        while i < n:
            self.new_page(section=section)
            half_w = C.CONTENT_W / 2
            half_h = (C.CONTENT_Y_TOP - C.CONTENT_Y_BOT) / 2
            for slot in range(4):
                if i >= n:
                    break
                row, col = divmod(slot, 2)
                x = C.CONTENT_X + col * half_w
                y = C.CONTENT_Y_TOP - half_h if row == 0 else C.CONTENT_Y_BOT
                draw_fn(items[i], x, y, half_w, half_h, i + 1)
                i += 1

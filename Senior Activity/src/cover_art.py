"""Vector cover art - puzzle-motif tiles (word search, sudoku, crossword, maze)
drawn as a decorative band on the front cover. No external image assets needed.
"""
from __future__ import annotations
from reportlab.lib.colors import Color


def _ink(v=0.12):
    return Color(v, v, v)


def draw_band(c, cx, cy, accent, tile=58, gap=18):
    """Draw 4 puzzle-motif tiles centered at (cx, cy)."""
    total = 4 * tile + 3 * gap
    x0 = cx - total / 2
    y0 = cy - tile / 2
    positions = [x0 + i * (tile + gap) for i in range(4)]
    _motif_wordsearch(c, positions[0], y0, tile, accent)
    _motif_sudoku(c, positions[1], y0, tile, accent)
    _motif_crossword(c, positions[2], y0, tile, accent)
    _motif_maze(c, positions[3], y0, tile, accent)


def _motif_wordsearch(c, x, y, s, accent):
    c.setStrokeColor(accent)
    c.setFillColor(accent)
    c.setLineWidth(1.4)
    n = 5
    cell = s / n
    for r in range(n + 1):
        c.line(x, y + r * cell, x + s, y + r * cell)
        c.line(x + r * cell, y, x + r * cell, y + s)
    # highlight a diagonal "found word"
    for i in range(n):
        c.setFillColor(accent)
        c.rect(x + i * cell, y + (n - 1 - i) * cell, cell, cell, stroke=0, fill=1)


def _motif_sudoku(c, x, y, s, accent):
    c.setStrokeColor(accent)
    c.setFillColor(_ink())
    c.setLineWidth(1.0)
    n = 3
    cell = s / n
    for r in range(n + 1):
        c.line(x, y + r * cell, x + s, y + r * cell)
        c.line(x + r * cell, y, x + r * cell, y + s)
    c.setLineWidth(2.2)
    c.rect(x, y, s, s, stroke=1, fill=0)
    c.setLineWidth(1.0)
    c.setFont("Helvetica-Bold", cell * 0.6)
    nums = [(0, 0, "5"), (1, 1, "3"), (2, 2, "7"), (0, 2, "2")]
    for (r, col, num) in nums:
        cx = x + col * cell + cell / 2
        cy = y + (n - 1 - r) * cell + cell * 0.22
        c.drawCentredString(cx, cy, num)


def _motif_crossword(c, x, y, s, accent):
    c.setStrokeColor(accent)
    c.setLineWidth(1.4)
    n = 4
    cell = s / n
    black = [(0, 1), (1, 3), (2, 0), (3, 2)]
    for r in range(n):
        for col in range(n):
            cx = x + col * cell
            cy = y + (n - 1 - r) * cell
            if (r, col) in black:
                c.setFillColor(_ink())
                c.rect(cx, cy, cell, cell, stroke=1, fill=1)
            else:
                c.setFillColor(Color(1, 1, 1))
                c.rect(cx, cy, cell, cell, stroke=1, fill=1)


def _motif_maze(c, x, y, s, accent):
    c.setStrokeColor(accent)
    c.setLineWidth(1.6)
    c.setFillColor(Color(1, 1, 1))
    c.rect(x, y, s, s, stroke=1, fill=1)
    # a few internal walls to suggest a maze
    third = s / 3
    c.line(x + third, y, x + third, y + 2 * third)
    c.line(x + third, y + 2 * third, x + 2 * third, y + 2 * third)
    c.line(x + 2 * third, y + third, x + s, y + third)
    c.line(x + 2 * third, y + third, x + 2 * third, y + s)

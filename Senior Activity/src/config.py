"""Central spec for the Bright Mind Large-Print Puzzles & Brain Games series.

All geometry in PostScript points (1 in = 72 pt). Source of truth mirrors the
planning docs (PLAN-/CONTENTS-/LAYOUT-). Counts ship in two presets:
SLICE (small, to validate the engine on one book) and FULL (the spec total).
"""
from __future__ import annotations
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = PROJECT_ROOT / "Atkinson_Hyperlegible_Next" / "static"
OUTPUT_DIR = PROJECT_ROOT / "output"

# --- Page geometry (KDP 8.5x11, cream, B&W interior) ---
TRIM_W = 8.5 * 72          # 612 pt
TRIM_H = 11 * 72           # 792 pt
BLEED = 0.125 * 72         # 9 pt (cover only)
MARGIN_OUT = 0.625 * 72    # 45 pt outside margin (>= KDP 0.375)
MARGIN_IN = 0.625 * 72     # binding gutter (production: size by page count)
MARGIN_TOP = 0.85 * 72    # clears the header rule with a comfortable gap
MARGIN_BOT = 0.8 * 72     # clears the footer rule
SAFE = 0.375 * 72          # safe-zone inset from trim

CONTENT_W = TRIM_W - MARGIN_OUT - MARGIN_IN
CONTENT_X = MARGIN_OUT
CONTENT_Y_BOT = MARGIN_BOT
CONTENT_Y_TOP = TRIM_H - MARGIN_TOP

# --- Typography (Atkinson Hyperlegible Next) ---
F_REG = "AtkinsonHyperlegible"
F_BOLD = "AtkinsonHyperlegible-Bold"
F_ITAL = "AtkinsonHyperlegible-Italic"
F_BOLDITAL = "AtkinsonHyperlegible-BoldItalic"
F_MED = "AtkinsonHyperlegible-Medium"
F_SEMI = "AtkinsonHyperlegible-SemiBold"

SZ_BODY = 18
SZ_GRID = 20      # word-search / scramble letters
SZ_SUDOKU = 22    # 9x9 fits content width at this size
SZ_HEADING = 28
SZ_SECTION = 22
SZ_SUB = 16
SZ_FOOTER = 14
SZ_SOLUTION = 12
LEADING = 1.5

# --- Difficulty tiers ---
TIERS = ("easy", "medium", "challenger")
# word-search grid sizes and word counts by tier
WS_GRID = {"easy": 11, "medium": 13, "challenger": 15}
WS_WORDS = {"easy": 8, "medium": 10, "challenger": 12}
WS_DIRS = {
    "easy": ("E", "S"),                                   # across, down
    "medium": ("E", "S", "SE"),                           # + diagonal
    "challenger": ("E", "S", "SE", "SW", "W", "N", "NE", "NW"),  # + reversed
}
SUDOKU_GIVENS = {  # fraction of cells shown
    "easy": 0.50,
    "medium": 0.34,
    "challenger": 0.27,
}
MAZE_GRID = {"easy": 12, "medium": 16}

# Crossword (themed, interlocking, black-square; 1 per page)
CW_GRID = {"easy": 11, "medium": 12, "challenger": 13}
CW_WORDS = {"easy": 8, "medium": 10, "challenger": 12}  # target placed words

# --- Imprint / series ---
IMPRINT = "Bright Mind Press"
SERIES = "Bright Mind Large-Print Puzzles & Brain Games"

# --- Puzzle counts ---
COUNTS_SLICE = {
    "wordsearch": {"easy": 3, "medium": 2, "challenger": 1},
    "sudoku":     {"easy": 2, "medium": 1, "challenger": 1},
    "scramble":   {"easy": 2, "medium": 1, "challenger": 1},
    "trivia":     {"easy": 2, "medium": 1, "challenger": 1},
    "crosswords": {"easy": 2, "medium": 1, "challenger": 1},
    "mazes":      {"easy": 2, "medium": 1, "challenger": 0},
}
COUNTS_FULL = {
    "wordsearch": {"easy": 20, "medium": 20, "challenger": 14},  # 54
    "sudoku":     {"easy": 18, "medium": 12, "challenger": 6},   # 36
    "scramble":   {"easy": 12, "medium": 12, "challenger": 6},   # 30
    "trivia":     {"easy": 10, "medium": 8, "challenger": 6},    # 24
    "crosswords": {"easy": 6, "medium": 6, "challenger": 6},     # 18
    "mazes":      {"easy": 13, "medium": 5, "challenger": 0},    # 18
}
COLORING_SLICE = 2
COLORING_FULL = 2

PRESETS = {"slice": COUNTS_SLICE, "full": COUNTS_FULL}
COLORING = {"slice": COLORING_SLICE, "full": COLORING_FULL}


def total_puzzles(counts: dict) -> int:
    return sum(c for grp in counts.values() for c in grp.values())

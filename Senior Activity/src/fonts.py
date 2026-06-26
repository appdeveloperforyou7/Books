"""Register Atkinson Hyperlegible Next static TTFs with ReportLab.

Uses only the static instances (Regular/Medium/SemiBold/Bold + italics) from
Atkinson_Hyperlegible_Next/static/. Variable-font files are NOT used — ReportLab
cannot embed variable-font axes reliably.
"""
from __future__ import annotations
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

from . import config as C

_REGISTERED = False


def register_fonts() -> None:
    global _REGISTERED
    if _REGISTERED:
        return
    d = C.FONT_DIR
    pairs = [
        (C.F_REG, "AtkinsonHyperlegibleNext-Regular.ttf"),
        (C.F_BOLD, "AtkinsonHyperlegibleNext-Bold.ttf"),
        (C.F_ITAL, "AtkinsonHyperlegibleNext-Italic.ttf"),
        (C.F_BOLDITAL, "AtkinsonHyperlegibleNext-BoldItalic.ttf"),
        (C.F_MED, "AtkinsonHyperlegibleNext-Medium.ttf"),
        (C.F_SEMI, "AtkinsonHyperlegibleNext-SemiBold.ttf"),
    ]
    for name, fname in pairs:
        path = d / fname
        if not path.exists():
            raise FileNotFoundError(f"Missing font: {path}")
        pdfmetrics.registerFont(TTFont(name, str(path)))
    registerFontFamily(
        C.F_REG,
        normal=C.F_REG, bold=C.F_BOLD,
        italic=C.F_ITAL, boldItalic=C.F_BOLDITAL,
    )
    _REGISTERED = True

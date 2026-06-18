#!/usr/bin/env python3
"""
VAULT B — KDP Interior PDF Typesetter
5.5x8.5 trim (digest), professional serif, chapter title pages, running headers.
"""
import re
import os
import sys
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from reportlab.lib.pagesizes import inch
from reportlab.lib.units import inch as INCH
from reportlab.lib.colors import HexColor, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    NextPageTemplate, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ─── Config ──────────────────────────────────────────────────────────────────
SRC = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Manuscript_dvc.md"
OUT = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\VAULT_B_Interior.pdf"

TRIM_W = 5.5 * INCH
TRIM_H = 8.5 * INCH
# Symmetric margins: 0.75" on ALL sides. This guarantees a >=0.625" gutter on
# BOTH left-hand and right-hand pages regardless of parity (KDP requirement for
# 300+ page books). A single non-mirrored frame previously put the gutter on the
# wrong edge for even pages, landing exactly at the 0.625" minimum and triggering
# KDP "insufficient gutter" / "text outside margins" errors.
MARGIN_OUTER = 0.75 * INCH
MARGIN_INNER = 0.75 * INCH
MARGIN_TOP = 0.75 * INCH
MARGIN_BOTTOM = 0.75 * INCH

# Colors
INK = HexColor("#1a1a1a")
ACCENT = HexColor("#8B0000")
MUTED = HexColor("#666666")
RULE = HexColor("#cccccc")

# ─── Font Registration ───────────────────────────────────────────────────────
FONT_BODY = "Times-Roman"
FONT_BODY_B = "Times-Bold"
FONT_BODY_I = "Times-Italic"
FONT_DISPLAY = "Times-Bold"
FONT_SANS = "Helvetica"

_win = os.environ.get("WINDIR", r"C:\Windows")
_font_dir = os.path.join(_win, "Fonts")

def reg(name, path):
    if os.path.exists(path):
        try:
            pdfmetrics.registerFont(TTFont(name, path))
            return True
        except Exception as e:
            print(f"  Font reg fail {name}: {e}")
    return False

# Try Garamond first
if reg("Garamond", os.path.join(_font_dir, "GARA.TTF")):
    FONT_BODY = "Garamond"
    if reg("Garamond-Bold", os.path.join(_font_dir, "GARABD.TTF")):
        FONT_BODY_B = "Garamond-Bold"
        FONT_DISPLAY = "Garamond-Bold"
    if reg("Garamond-Italic", os.path.join(_font_dir, "GARAIT.TTF")):
        FONT_BODY_I = "Garamond-Italic"
# Else try Georgia
elif reg("Georgia", os.path.join(_font_dir, "georgia.ttf")):
    FONT_BODY = "Georgia"
    if reg("Georgia-Bold", os.path.join(_font_dir, "georgiab.ttf")):
        FONT_BODY_B = "Georgia-Bold"
        FONT_DISPLAY = "Georgia-Bold"
    if reg("Georgia-Italic", os.path.join(_font_dir, "georgiai.ttf")):
        FONT_BODY_I = "Georgia-Italic"

# Sans-serif (headers, copyright): embed Arial or Calibri so ALL fonts are embedded (KDP requirement)
if reg("Arial", os.path.join(_font_dir, "arial.ttf")):
    FONT_SANS = "Arial"
    # register bold/italic Arial variants too, so <b>/<i> inside Arial paragraphs don't fall back to Helvetica
    reg("Arial-Bold", os.path.join(_font_dir, "arialbd.ttf"))
    reg("Arial-Italic", os.path.join(_font_dir, "ariali.ttf"))
    reg("Arial-BoldItalic", os.path.join(_font_dir, "arialbi.ttf"))
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold",
                                  italic="Arial-Italic", boldItalic="Arial-BoldItalic")
elif reg("Calibri", os.path.join(_font_dir, "calibri.ttf")):
    FONT_SANS = "Calibri"
    reg("Calibri-Bold", os.path.join(_font_dir, "calibrib.ttf"))
    reg("Calibri-Italic", os.path.join(_font_dir, "calibrii.ttf"))
    reg("Calibri-BoldItalic", os.path.join(_font_dir, "calibriz.ttf"))
    pdfmetrics.registerFontFamily("Calibri", normal="Calibri", bold="Calibri-Bold",
                                  italic="Calibri-Italic", boldItalic="Calibri-BoldItalic")

# Register the serif family so <b>/<i> inside body Paragraphs use the right variants (prevents Helvetica fallback)
pdfmetrics.registerFontFamily(FONT_BODY, normal=FONT_BODY, bold=FONT_BODY_B,
                              italic=FONT_BODY_I, boldItalic=FONT_BODY_B)

print(f"Fonts: body={FONT_BODY}, bold={FONT_BODY_B}, italic={FONT_BODY_I}, display={FONT_DISPLAY}, sans={FONT_SANS}")
print("Font families registered (bold/italic mapping) OK")

# ─── Styles ──────────────────────────────────────────────────────────────────
body_style = ParagraphStyle("Body", fontName=FONT_BODY, fontSize=11, leading=15.5,
    textColor=INK, alignment=TA_JUSTIFY, firstLineIndent=18, spaceBefore=0, spaceAfter=0)
body_first = ParagraphStyle("BodyFirst", parent=body_style, firstLineIndent=0)
chapter_title_style = ParagraphStyle("ChapterTitle", fontName=FONT_DISPLAY, fontSize=28,
    leading=34, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=8)
chapter_sub_style = ParagraphStyle("ChapterSub", fontName=FONT_BODY_I, fontSize=12,
    leading=16, textColor=MUTED, alignment=TA_CENTER, spaceAfter=24)
fact_para = ParagraphStyle("Fact", fontName=FONT_BODY, fontSize=10, leading=14,
    textColor=INK, alignment=TA_LEFT, leftIndent=20, rightIndent=20, spaceBefore=4, spaceAfter=8)
title_main_style = ParagraphStyle("TitleMain", fontName=FONT_DISPLAY, fontSize=42,
    leading=50, textColor=INK, alignment=TA_CENTER, spaceAfter=12)
title_sub_style = ParagraphStyle("TitleSub", fontName=FONT_BODY_I, fontSize=16,
    leading=22, textColor=MUTED, alignment=TA_CENTER)
copyright_style = ParagraphStyle("Copyright", fontName=FONT_SANS, fontSize=9,
    leading=13, textColor=MUTED, alignment=TA_CENTER)
dedication_style = ParagraphStyle("Dedication", fontName=FONT_BODY_I, fontSize=13,
    leading=18, textColor=INK, alignment=TA_CENTER)

print("Styles defined OK")

# ─── Parsing ─────────────────────────────────────────────────────────────────
def parse_manuscript(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    fact_match = re.search(r'# FACT\s*\n(.*?)\n---', text, re.DOTALL)
    fact_text = fact_match.group(1).strip() if fact_match else ""
    chapter_pattern = re.compile(r'^# (Prologue|Chapter \d+|Epilogue)\s*$', re.MULTILINE)
    chapter_starts = [(m.start(), m.group(1)) for m in chapter_pattern.finditer(text)]
    chapters = []
    for i, (start, title) in enumerate(chapter_starts):
        end = chapter_starts[i+1][0] if i+1 < len(chapter_starts) else len(text)
        body = text[start:end]
        body_lines = body.split("\n")[1:]
        body = "\n".join(body_lines).strip()
        body = re.sub(r'\n---\s*$', '', body).strip()
        chapters.append((title, body))
    return fact_text, chapters

def clean_para(text):
    """Clean a paragraph for ReportLab Paragraph: handle markdown bold/italic, escape stray XML."""
    text = text.strip()
    # Blockquote markers
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    # Bold: **text** -> <b>text</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic: *text* -> <i>text</i> (but not ** which is bold, already handled)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    # Escape stray < and > that aren't our tags
    text = text.replace("&", "&amp;")
    # Re-fix our tags that got escaped
    text = text.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    text = text.replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")
    return text

def paras_from_text(text):
    flowables = []
    raw_paras = re.split(r'\n\s*\n', text.strip())
    first = True
    for para in raw_paras:
        para = para.strip()
        if not para or para == "---":
            continue
        para = clean_para(para)
        if not para:
            continue
        try:
            style = body_first if first else body_style
            flowables.append(Paragraph(para, style))
            first = False
        except Exception as e:
            print(f"  Para parse error: {e} | text: {para[:60]}...")
            # Fallback: escape everything
            safe = para.replace("<","&lt;").replace(">","&gt;").replace("&amp;","&")
            safe = safe.replace("&","&amp;")
            flowables.append(Paragraph(safe, body_first if first else body_style))
            first = False
    return flowables

# ─── Page Templates ──────────────────────────────────────────────────────────
class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        content_w = TRIM_W - MARGIN_INNER - MARGIN_OUTER
        content_h = TRIM_H - MARGIN_TOP - MARGIN_BOTTOM
        body_frame = Frame(MARGIN_INNER, MARGIN_BOTTOM, content_w, content_h,
            id="body", showBoundary=0, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="front", frames=[body_frame], onPage=self._blank_header),
            PageTemplate(id="chapter_start", frames=[body_frame], onPage=self._blank_header),
            PageTemplate(id="body_left", frames=[body_frame], onPage=self._left_header),
            PageTemplate(id="body_right", frames=[body_frame], onPage=self._right_header),
        ])

    def _blank_header(self, canvas, doc):
        pass

    def _left_header(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT_SANS, 9)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(MARGIN_INNER + 15, MARGIN_BOTTOM - 20, str(doc.page))
        canvas.drawRightString(TRIM_W - MARGIN_OUTER - 15, MARGIN_BOTTOM - 20, "VAULT B")
        canvas.restoreState()

    def _right_header(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT_SANS, 9)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN_INNER + 15, MARGIN_BOTTOM - 20, "VAULT B")
        canvas.drawCentredString(TRIM_W - MARGIN_OUTER - 15, MARGIN_BOTTOM - 20, str(doc.page))
        canvas.restoreState()

# ─── Build ───────────────────────────────────────────────────────────────────
def main():
    print("Parsing manuscript...")
    fact_text, chapters = parse_manuscript(SRC)
    print(f"Found {len(chapters)} chapters + FACT section")

    story = []

    # Title page
    story.append(Spacer(1, 2.5 * INCH))
    story.append(Paragraph("VAULT B", title_main_style))
    story.append(Spacer(1, 0.3 * INCH))
    story.append(Paragraph("Book One of the Meera Desai Thrillers", title_sub_style))
    story.append(PageBreak())

    # Copyright
    story.append(Spacer(1, 3 * INCH))
    story.append(Paragraph("<b>VAULT B</b>", ParagraphStyle("cr1", parent=copyright_style, fontName=FONT_BODY_B, fontSize=11)))
    story.append(Spacer(1, 0.15 * INCH))
    story.append(Paragraph("Book One of the Meera Desai Thrillers", copyright_style))
    story.append(Spacer(1, 0.5 * INCH))
    story.append(Paragraph("Copyright &copy; 2026", copyright_style))
    story.append(Spacer(1, 0.05 * INCH))
    story.append(Paragraph("All rights reserved.", copyright_style))
    story.append(Spacer(1, 0.3 * INCH))
    story.append(Paragraph("This is a work of fiction. Names, characters, places, and incidents", copyright_style))
    story.append(Paragraph("are products of the author's imagination. Any resemblance to actual", copyright_style))
    story.append(Paragraph("persons, living or dead, events, or locales is entirely coincidental.", copyright_style))
    story.append(PageBreak())

    # Dedication
    story.append(Spacer(1, 3.5 * INCH))
    story.append(Paragraph("For those who guard knowledge,", dedication_style))
    story.append(Spacer(1, 0.1 * INCH))
    story.append(Paragraph("and for those who share it.", dedication_style))
    story.append(PageBreak())

    # FACT section
    story.append(NextPageTemplate("front"))
    story.append(PageBreak())
    story.append(Spacer(1, 0.5 * INCH))
    story.append(Paragraph("FACT", ParagraphStyle("facthead", parent=chapter_title_style, fontSize=20, spaceAfter=24)))
    fact_paras_raw = re.split(r'\n>\n|\n>\s*\n', fact_text)
    for fp in fact_paras_raw:
        fp = fp.strip()
        if not fp:
            continue
        fp = clean_para(fp)
        story.append(Paragraph(fp, fact_para))
    story.append(PageBreak())

    # Chapters
    for idx, (title, body) in enumerate(chapters):
        story.append(NextPageTemplate("chapter_start"))
        story.append(PageBreak())
        story.append(Spacer(1, 1.5 * INCH))
        if title == "Prologue":
            story.append(Paragraph("Prologue", chapter_title_style))
        elif title.startswith("Chapter"):
            num = title.split()[-1]
            story.append(Paragraph(f"Chapter {num}", chapter_title_style))
        else:
            story.append(Paragraph(title, chapter_title_style))
        story.append(Spacer(1, 0.3 * INCH))
        story.append(NextPageTemplate("body_right"))
        paras = paras_from_text(body)
        for p in paras:
            story.append(p)

    print(f"Building PDF: {OUT}")
    doc = BookDocTemplate(OUT, pagesize=(TRIM_W, TRIM_H),
        leftMargin=MARGIN_INNER, rightMargin=MARGIN_OUTER,
        topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
        title="VAULT B", author="Kapil",
        subject="Book One of the Meera Desai Thrillers", creator="VAULT B Typesetter")
    doc.build(story)
    sz = os.path.getsize(OUT)
    print(f"DONE: {OUT}")
    print(f"Size: {sz/1024:.0f} KB")

    clean_for_kdp(OUT)


def clean_for_kdp(path):
    """Post-process PDF with pikepdf to ensure ALL fonts are embedded for KDP.
    ReportLab may inject non-embedded base-14 fonts (Helvetica) into page resources.
    This function remaps any non-embedded font to an embedded equivalent (Arial)."""
    import pikepdf as _pp

    print("\n--- KDP Cleanup (pikepdf) ---")
    pdf = _pp.open(path)

    # Find an embedded sans-serif font to use as replacement
    embedded_sans = None
    for page in pdf.pages:
        res = page.get("/Resources")
        if res is None:
            continue
        fdict = res.get("/Font")
        if fdict is None:
            continue
        for fk in fdict.keys():
            fobj = fdict[fk]
            bname = str(fobj.get("/BaseFont", ""))
            if "Arial" in bname or "Calibri" in bname:
                desc = fobj.get("/FontDescriptor")
                if desc is not None and any(ff in desc for ff in ("/FontFile", "/FontFile2", "/FontFile3")):
                    embedded_sans = fobj
                    break
        if embedded_sans:
            break

    if embedded_sans is None:
        print("  WARNING: No embedded sans font found to remap non-embedded fonts. Skipping.")
        pdf.close()
        return

    sans_name = str(embedded_sans.get("/BaseFont", "?"))
    remapped = 0
    for page in pdf.pages:
        res = page.get("/Resources")
        if res is None:
            continue
        fdict = res.get("/Font")
        if fdict is None:
            continue
        for fk in list(fdict.keys()):
            fobj = fdict[fk]
            desc = fobj.get("/FontDescriptor")
            is_embedded = desc is not None and any(ff in desc for ff in ("/FontFile", "/FontFile2", "/FontFile3"))
            if not is_embedded:
                fdict[fk] = embedded_sans
                remapped += 1

    # Set metadata
    pdf.docinfo["/Title"] = "VAULT B"
    pdf.docinfo["/Author"] = "Kapil"
    pdf.docinfo["/Subject"] = "Book One of the Meera Desai Thrillers"

    # Save to temp file, then replace original
    tmp = path + ".tmp"
    pdf.save(tmp, object_stream_mode=_pp.ObjectStreamMode.generate)
    pdf.close()
    os.replace(tmp, path)

    sz = os.path.getsize(path)
    print(f"  Remapped {remapped} non-embedded font(s) to {sans_name}")
    print(f"  Final size: {sz/1024:.0f} KB")
    print("  ✓ All fonts embedded — KDP ready")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

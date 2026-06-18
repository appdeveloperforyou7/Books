#!/usr/bin/env python3
"""
TWO CHAINS KDP Interior PDF Typesetter
5.5x8.5 trim, Garamond, chapter title pages, running headers, epigraphs.
"""
import re, os, sys, traceback

from reportlab.lib.units import inch as INCH
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, NextPageTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

SRC = r"D:\Kapil\Books\Meera Desai\MD - Two Chains\Manuscript_v3.md"
OUT = r"D:\Kapil\Books\Meera Desai\MD - Two Chains\Output\TWO_CHAINS_Interior.pdf"

TRIM_W = 5.5 * INCH
TRIM_H = 8.5 * INCH
MARGIN = 0.75 * INCH

INK = HexColor("#1a1a1a")
ACCENT = HexColor("#8B0000")
MUTED = HexColor("#666666")

FONT_BODY = "Times-Roman"
FONT_BODY_B = "Times-Bold"
FONT_BODY_I = "Times-Italic"
FONT_DISPLAY = "Times-Bold"
FONT_SANS = "Helvetica"

_win = os.environ.get("WINDIR", r"C:\Windows")
_fd = os.path.join(_win, "Fonts")

def reg(name, path):
    if os.path.exists(path):
        try:
            pdfmetrics.registerFont(TTFont(name, path))
            return True
        except Exception:
            pass
    return False

if reg("Garamond", os.path.join(_fd, "GARA.TTF")):
    FONT_BODY = "Garamond"
    if reg("Garamond-Bold", os.path.join(_fd, "GARABD.TTF")):
        FONT_BODY_B = "Garamond-Bold"
        FONT_DISPLAY = "Garamond-Bold"
    if reg("Garamond-Italic", os.path.join(_fd, "GARAIT.TTF")):
        FONT_BODY_I = "Garamond-Italic"
elif reg("Georgia", os.path.join(_fd, "georgia.ttf")):
    FONT_BODY = "Georgia"
    if reg("Georgia-Bold", os.path.join(_fd, "georgiab.ttf")):
        FONT_BODY_B = "Georgia-Bold"
        FONT_DISPLAY = "Georgia-Bold"
    if reg("Georgia-Italic", os.path.join(_fd, "georgiai.ttf")):
        FONT_BODY_I = "Georgia-Italic"

if reg("Arial", os.path.join(_fd, "arial.ttf")):
    FONT_SANS = "Arial"
    reg("Arial-Bold", os.path.join(_fd, "arialbd.ttf"))
    reg("Arial-Italic", os.path.join(_fd, "ariali.ttf"))
    reg("Arial-BoldItalic", os.path.join(_fd, "arialbi.ttf"))
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold",
                                  italic="Arial-Italic", boldItalic="Arial-BoldItalic")
elif reg("Calibri", os.path.join(_fd, "calibri.ttf")):
    FONT_SANS = "Calibri"
    reg("Calibri-Bold", os.path.join(_fd, "calibrib.ttf"))
    reg("Calibri-Italic", os.path.join(_fd, "calibrii.ttf"))
    pdfmetrics.registerFontFamily("Calibri", normal="Calibri", bold="Calibri-Bold",
                                  italic="Calibri-Italic", boldItalic="Calibri-Bold")

pdfmetrics.registerFontFamily(FONT_BODY, normal=FONT_BODY, bold=FONT_BODY_B,
                              italic=FONT_BODY_I, boldItalic=FONT_BODY_B)

body_style = ParagraphStyle("Body", fontName=FONT_BODY, fontSize=11, leading=15.5,
    textColor=INK, alignment=TA_JUSTIFY, firstLineIndent=18)
body_first = ParagraphStyle("BodyFirst", parent=body_style, firstLineIndent=0)
chapter_title_style = ParagraphStyle("ChapterTitle", fontName=FONT_DISPLAY, fontSize=28,
    leading=34, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=8)
title_main_style = ParagraphStyle("TitleMain", fontName=FONT_DISPLAY, fontSize=42,
    leading=50, textColor=INK, alignment=TA_CENTER, spaceAfter=12)
title_sub_style = ParagraphStyle("TitleSub", fontName=FONT_BODY_I, fontSize=16,
    leading=22, textColor=MUTED, alignment=TA_CENTER)
copyright_style = ParagraphStyle("Copyright", fontName=FONT_SANS, fontSize=9,
    leading=13, textColor=MUTED, alignment=TA_CENTER)
dedication_style = ParagraphStyle("Dedication", fontName=FONT_BODY_I, fontSize=13,
    leading=18, textColor=INK, alignment=TA_CENTER)
epigraph_style = ParagraphStyle("Epigraph", fontName=FONT_BODY_I, fontSize=10,
    leading=14, textColor=MUTED, alignment=TA_CENTER, leftIndent=30, rightIndent=30,
    spaceBefore=12, spaceAfter=4)
epi_source_style = ParagraphStyle("EpiSource", fontName=FONT_SANS, fontSize=8,
    leading=11, textColor=MUTED, alignment=TA_CENTER, leftIndent=30, rightIndent=30,
    spaceBefore=2, spaceAfter=24)

def parse_manuscript(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    pat = re.compile(r'^# (Prologue|Chapter \d+|Interstitial:[^\n#]+|Epilogue)\s*$', re.MULTILINE)
    starts = [(m.start(), m.group(1).strip()) for m in pat.finditer(text)]
    chapters = []
    for i, (start, title) in enumerate(starts):
        end = starts[i+1][0] if i+1 < len(starts) else len(text)
        body = text[start:end]
        body = "\n".join(body.split("\n")[1:]).strip()
        body = re.sub(r'\n---\s*$', '', body).strip()
        chapters.append((title, body))
    return chapters

def clean_para(text):
    text = text.strip()
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    text = text.replace(chr(38), chr(38) + "amp;")
    text = text.replace(chr(60) + "lt;b" + chr(62), chr(60) + "b" + chr(62))
    text = text.replace(chr(60) + "lt;/b" + chr(62), chr(60) + "/b" + chr(62))
    text = text.replace(chr(60) + "lt;i" + chr(62), chr(60) + "i" + chr(62))
    text = text.replace(chr(60) + "lt;/i" + chr(62), chr(60) + "/i" + chr(62))
    return text

def paras_from_text(text):
    flowables = []
    raw_paras = re.split(r'\n\s*\n', text.strip())
    first = True
    for para in raw_paras:
        para = para.strip()
        if not para or para == "---":
            continue
        lines_in = para.split("\n")
        if len(lines_in) == 2:
            l1 = lines_in[0].strip()
            l2 = lines_in[1].strip()
            if l1.startswith("*") and l2.startswith(chr(8212)):
                flowables.append(Spacer(1, 0.2 * INCH))
                flowables.append(Paragraph(clean_para(l1), epigraph_style))
                flowables.append(Paragraph(clean_para(l2), epi_source_style))
                flowables.append(Spacer(1, 0.15 * INCH))
                first = False
                continue
        para = clean_para(para)
        if not para:
            continue
        try:
            flowables.append(Paragraph(para, body_first if first else body_style))
            first = False
        except Exception as e:
            print(f"  Parse error: {e}")
            safe = para.replace(chr(60), chr(60)+"lt;").replace(chr(62), chr(62)+"gt;")
            flowables.append(Paragraph(safe, body_first if first else body_style))
            first = False
    return flowables

class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, **kw)
        cw = TRIM_W - MARGIN * 2
        ch = TRIM_H - MARGIN * 2
        bf = Frame(MARGIN, MARGIN, cw, ch, id="body", showBoundary=0,
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="front", frames=[bf], onPage=self._blank),
            PageTemplate(id="cs", frames=[bf], onPage=self._blank),
            PageTemplate(id="bl", frames=[bf], onPage=self._lh),
            PageTemplate(id="br", frames=[bf], onPage=self._rh),
        ])
    def _blank(self, canvas, doc): pass
    def _lh(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT_SANS, 9)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(MARGIN + 15, MARGIN - 20, str(doc.page))
        canvas.drawRightString(TRIM_W - MARGIN - 15, MARGIN - 20, "TWO CHAINS")
        canvas.restoreState()
    def _rh(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT_SANS, 9)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN + 15, MARGIN - 20, "TWO CHAINS")
        canvas.drawCentredString(TRIM_W - MARGIN - 15, MARGIN - 20, str(doc.page))
        canvas.restoreState()

def main():
    print("Parsing manuscript...")
    chapters = parse_manuscript(SRC)
    print(f"Found {len(chapters)} chapters/sections")

    story = []

    # Title page
    story.append(Spacer(1, 2.5 * INCH))
    story.append(Paragraph("TWO CHAINS", title_main_style))
    story.append(Spacer(1, 0.3 * INCH))
    story.append(Paragraph("Book Two of the Meera Desai Thrillers", title_sub_style))
    story.append(PageBreak())

    # Copyright
    story.append(Spacer(1, 3 * INCH))
    story.append(Paragraph("<b>TWO CHAINS</b>", ParagraphStyle("cr1", parent=copyright_style, fontName=FONT_BODY_B, fontSize=11)))
    story.append(Spacer(1, 0.15 * INCH))
    story.append(Paragraph("Book Two of the Meera Desai Thrillers", copyright_style))
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
    story.append(Paragraph("and for those who seek it.", dedication_style))
    story.append(PageBreak())

    # Chapters
    for title, body in chapters:
        story.append(NextPageTemplate("cs"))
        story.append(PageBreak())
        story.append(Spacer(1, 1.5 * INCH))
        if title == "Prologue":
            story.append(Paragraph("Prologue", chapter_title_style))
        elif title.startswith("Chapter"):
            story.append(Paragraph(f"Chapter {title.split()[-1]}", chapter_title_style))
        elif title.startswith("Interstitial"):
            story.append(Paragraph(title.replace("Interstitial:", "").strip(), chapter_title_style))
        else:
            story.append(Paragraph(title, chapter_title_style))
        story.append(Spacer(1, 0.3 * INCH))
        story.append(NextPageTemplate("br"))
        for p in paras_from_text(body):
            story.append(p)

    print(f"Building PDF: {OUT}")
    doc = BookDocTemplate(OUT, pagesize=(TRIM_W, TRIM_H),
        leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN,
        title="TWO CHAINS", author="Kapil",
        subject="Book Two of the Meera Desai Thrillers", creator="TWO CHAINS Typesetter")
    doc.build(story)
    print(f"DONE: {os.path.getsize(OUT) // 1024} KB")
    clean_for_kdp(OUT)

def clean_for_kdp(path):
    import pikepdf as _pp
    print("\n--- KDP Cleanup (pikepdf) ---")
    pdf = _pp.open(path)
    embedded_sans = None
    for page in pdf.pages:
        res = page.get("/Resources")
        if res is None: continue
        fd = res.get("/Font")
        if fd is None: continue
        for fk in fd.keys():
            fo = fd[fk]
            bn = str(fo.get("/BaseFont", ""))
            if "Arial" in bn or "Calibri" in bn:
                desc = fo.get("/FontDescriptor")
                if desc is not None and any(ff in desc for ff in ("/FontFile", "/FontFile2", "/FontFile3")):
                    embedded_sans = fo
                    break
        if embedded_sans: break
    if embedded_sans is None:
        print("  WARNING: No embedded sans found. Skipping.")
        pdf.close()
        return
    remapped = 0
    for page in pdf.pages:
        res = page.get("/Resources")
        if res is None: continue
        fd = res.get("/Font")
        if fd is None: continue
        for fk in list(fd.keys()):
            fo = fd[fk]
            desc = fo.get("/FontDescriptor")
            if desc is None or not any(ff in desc for ff in ("/FontFile", "/FontFile2", "/FontFile3")):
                fd[fk] = embedded_sans
                remapped += 1
    pdf.docinfo["/Title"] = "TWO CHAINS"
    pdf.docinfo["/Author"] = "Kapil"
    tmp = path + ".tmp"
    pdf.save(tmp, object_stream_mode=_pp.ObjectStreamMode.generate)
    pdf.close()
    os.replace(tmp, path)
    print(f"  Remapped {remapped} font(s)")
    print(f"  Final: {os.path.getsize(path) // 1024} KB")
    print("  All fonts embedded - KDP ready")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
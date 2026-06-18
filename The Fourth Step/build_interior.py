"""
The Fourth Step — Interior PDF Generator (Gone Girl style)
KDP-compliant 5.5" x 8.5" paperback interior with:
  - Garamond body text (closest to Janson used in Gone Girl)
  - Mirrored margins (gutter binding)
  - Chapter starts 1/3 down the page
  - Part dividers, block-quoted text messages, italic prologue
  - Scene breaks as centered italic labels
  - Centered page numbers
"""

import os
import re
import sys
from reportlab.lib.pagesizes import inch
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, KeepTogether, Flowable,
    CondPageBreak,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = r"D:\Kapil\Books\PsyThr"
CHAPTERS_DIR = os.path.join(BASE, "Chapters")
OUTPUT_DIR = os.path.join(BASE, "Output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "The_Fourth_Step_Interior.pdf")

FONTS_DIR = r"C:\Windows\Fonts"

TRIM_W = 5.5 * inch
TRIM_H = 8.5 * inch

GUTTER = 0.75 * inch
OUTSIDE = 0.50 * inch
TOP_MARGIN = 0.65 * inch
BOTTOM_MARGIN = 0.75 * inch

BODY_SIZE = 11
BODY_LEADING = 14.5
FIRST_LINE_INDENT = 18
ORPHANS = 2

DARK = HexColor('#1a1a1a')
MID = HexColor('#333333')
DIM = HexColor('#888888')
ORNAMENT = HexColor('#999999')

PARTS = [
    {"title": "THE ARRIVAL", "range": (0, 8), "number": "ONE"},
    {"title": "THE MEMORY", "range": (8, 17), "number": "TWO"},
    {"title": "THE CONFESSION", "range": (17, 25), "number": "THREE"},
    {"title": "THE STEP", "range": (25, 31), "number": "FOUR"},
]

CHAPTER_ORDER = [
    "prologue.md",
    "chapter-01-neve.md", "chapter-02-saskia.md", "chapter-03-imogen.md",
    "chapter-04-rowan.md", "chapter-05-neve.md", "chapter-06-saskia.md",
    "chapter-07-imogen.md", "chapter-08-rowan.md", "chapter-09-neve.md",
    "chapter-10-saskia.md", "chapter-11-imogen.md", "chapter-12-rowan.md",
    "chapter-13-neve.md", "chapter-14-saskia.md", "chapter-15-imogen.md",
    "chapter-16-neve.md", "chapter-17-saskia.md", "chapter-18-imogen.md",
    "chapter-19-rowan.md", "chapter-20-saskia.md", "chapter-21-aisling.md",
    "chapter-22-neve.md", "chapter-23-saskia.md", "chapter-24-neve.md",
    "chapter-25-neve.md", "chapter-26-neve.md", "chapter-27-saskia.md",
    "chapter-28-neve.md", "chapter-29-neve.md",
    "epilogue-neve.md",
]


def register_fonts():
    fonts = [
        ("Garamond", os.path.join(FONTS_DIR, "GARA.TTF")),
        ("GaramondBold", os.path.join(FONTS_DIR, "GARABD.TTF")),
        ("GaramondItalic", os.path.join(FONTS_DIR, "GARAIT.TTF")),
        ("Georgia", os.path.join(FONTS_DIR, "georgia.ttf")),
        ("GeorgiaBold", os.path.join(FONTS_DIR, "georgiab.ttf")),
        ("GeorgiaItalic", os.path.join(FONTS_DIR, "georgiai.ttf")),
        ("Arial", os.path.join(FONTS_DIR, "arial.ttf")),
    ]
    for name, path in fonts:
        if os.path.isfile(path):
            pdfmetrics.registerFont(TTFont(name, path))


register_fonts()


def make_styles():
    s = {}

    s["body"] = ParagraphStyle(
        "Body",
        fontName="Garamond",
        fontSize=BODY_SIZE,
        leading=BODY_LEADING,
        alignment=TA_JUSTIFY,
        textColor=DARK,
        firstLineIndent=FIRST_LINE_INDENT,
        spaceBefore=0,
        spaceAfter=0,
        allowWidows=1,
        allowOrphans=1,
    )

    s["body_no_indent"] = ParagraphStyle(
        "BodyNoIndent",
        parent=s["body"],
        firstLineIndent=0,
    )

    s["body_italic"] = ParagraphStyle(
        "BodyItalic",
        parent=s["body"],
        fontName="GaramondItalic",
        textColor=MID,
    )

    s["body_italic_no_indent"] = ParagraphStyle(
        "BodyItalicNoIndent",
        parent=s["body_italic"],
        firstLineIndent=0,
    )

    s["blockquote"] = ParagraphStyle(
        "BlockQuote",
        parent=s["body"],
        fontName="GaramondItalic",
        fontSize=10.5,
        leading=13.5,
        leftIndent=36,
        rightIndent=24,
        textColor=MID,
        firstLineIndent=0,
        spaceBefore=6,
        spaceAfter=6,
    )

    s["chapter_num"] = ParagraphStyle(
        "ChapterNum",
        fontName="Garamond",
        fontSize=13,
        leading=16,
        alignment=TA_LEFT,
        textColor=DIM,
        spaceBefore=0,
        spaceAfter=4,
        characterSpacing=2,
    )

    s["chapter_title"] = ParagraphStyle(
        "ChapterTitle",
        fontName="GaramondItalic",
        fontSize=13,
        leading=16,
        alignment=TA_LEFT,
        textColor=DARK,
        spaceBefore=0,
        spaceAfter=0,
    )

    s["scene_label"] = ParagraphStyle(
        "SceneLabel",
        fontName="GaramondItalic",
        fontSize=9.5,
        leading=12,
        alignment=TA_CENTER,
        textColor=DIM,
        spaceBefore=18,
        spaceAfter=14,
        characterSpacing=1.5,
    )

    s["part_num"] = ParagraphStyle(
        "PartNum",
        fontName="Garamond",
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=DIM,
        characterSpacing=3,
    )

    s["part_title"] = ParagraphStyle(
        "PartTitle",
        fontName="GaramondItalic",
        fontSize=22,
        leading=28,
        alignment=TA_CENTER,
        textColor=DARK,
        spaceBefore=8,
    )

    s["title_main"] = ParagraphStyle(
        "TitleMain",
        fontName="Garamond",
        fontSize=32,
        leading=38,
        alignment=TA_CENTER,
        textColor=DARK,
    )

    s["title_sub"] = ParagraphStyle(
        "TitleSub",
        fontName="GaramondItalic",
        fontSize=12,
        leading=15,
        alignment=TA_CENTER,
        textColor=MID,
        spaceBefore=12,
    )

    s["title_author"] = ParagraphStyle(
        "TitleAuthor",
        fontName="Garamond",
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=DARK,
        spaceBefore=36,
        characterSpacing=2,
    )

    s["copyright"] = ParagraphStyle(
        "Copyright",
        fontName="Garamond",
        fontSize=8.5,
        leading=13,
        alignment=TA_LEFT,
        textColor=DIM,
    )

    s["page_num"] = ParagraphStyle(
        "PageNum",
        fontName="Garamond",
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=DIM,
    )

    s["epigraph"] = ParagraphStyle(
        "Epigraph",
        fontName="GaramondItalic",
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=MID,
        leftIndent=54,
        rightIndent=54,
    )

    s["epigraph_attr"] = ParagraphStyle(
        "EpigraphAttr",
        fontName="Garamond",
        fontSize=9.5,
        leading=12,
        alignment=TA_CENTER,
        textColor=DIM,
        spaceBefore=6,
    )

    return s


STYLES = make_styles()


class PageNumCanvas:
    def __init__(self, doc):
        self.doc = doc
        self._page_count = 0

    def on_page_front(self, canvas, doc):
        pass

    def on_page_body(self, canvas, doc):
        page_num = canvas.getPageNumber()
        doc._body_page_counter = getattr(doc, '_body_page_counter', 0) + 1
        num = doc._body_page_counter
        if num <= 1:
            return
        canvas.saveState()
        canvas.setFont("Garamond", 9)
        canvas.setFillColor(DIM)
        y = BOTTOM_MARGIN - 0.15 * inch
        if page_num % 2 == 1:
            canvas.drawCentredString(TRIM_W / 2, y, str(num))
        else:
            canvas.drawCentredString(TRIM_W / 2, y, str(num))
        canvas.restoreState()

    def on_page_blank(self, canvas, doc):
        pass


def escape_xml(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def format_inline(text):
    text = escape_xml(text)

    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)

    text = text.replace("\u2014", "&mdash;")
    text = text.replace("\u2013", "&ndash;")
    text = text.replace("\u201c", "&ldquo;")
    text = text.replace("\u201d", "&rdquo;")
    text = text.replace("\u2018", "&lsquo;")
    text = text.replace("\u2019", "&rsquo;")

    return text


def parse_chapter(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    header_line = lines[0].strip() if lines else ""
    is_prologue = "Prologue" in header_line
    is_epilogue = "Epilogue" in header_line
    is_chapter = not is_prologue and not is_epilogue

    chapter_info = {"prologue": is_prologue, "epilogue": is_epilogue}
    if is_chapter:
        m = re.match(r"# THE FOURTH STEP — Chapter (\d+): (.+)", header_line)
        if m:
            chapter_info["number"] = int(m.group(1))
            chapter_info["pov"] = m.group(2)

    content_lines = lines[1:]
    elements = []
    current_para = []
    in_italic_block = False
    italic_block_lines = []

    i = 0
    while i < len(content_lines):
        line = content_lines[i].rstrip("\n").rstrip("\r")
        stripped = line.strip()

        if stripped.startswith("## "):
            if current_para:
                text = " ".join(current_para)
                if text.strip():
                    elements.append(("paragraph", text))
                current_para = []
            scene_title = stripped[3:].strip()
            elements.append(("scene", scene_title))
            i += 1
            continue

        if stripped == "---":
            if current_para:
                text = " ".join(current_para)
                if text.strip():
                    elements.append(("paragraph", text))
                current_para = []
            elements.append(("break",))
            i += 1
            continue

        if stripped.startswith("*") and not stripped.startswith("**") and "—" in stripped and len(stripped) > 40:
            if current_para:
                text = " ".join(current_para)
                if text.strip():
                    elements.append(("paragraph", text))
                current_para = []

            block_lines = [stripped]
            i += 1
            while i < len(content_lines):
                next_line = content_lines[i].strip()
                if next_line.startswith("*") and not next_line.startswith("**"):
                    block_lines.append(next_line)
                    i += 1
                else:
                    break

            for bl in block_lines:
                if bl.startswith("*") and bl.endswith("*") and len(bl) > 2:
                    clean = bl[1:-1]
                else:
                    clean = bl
                elements.append(("blockquote", clean.strip()))
            continue

        if stripped.startswith("*") and stripped.endswith("*") and len(stripped) > 2 and not stripped.startswith("**"):
            if current_para:
                text = " ".join(current_para)
                if text.strip():
                    elements.append(("paragraph", text))
                current_para = []
            clean = stripped[1:-1]
            elements.append(("blockquote", clean.strip()))
            i += 1
            continue

        if stripped == "":
            if current_para:
                text = " ".join(current_para)
                if text.strip():
                    elements.append(("paragraph", text))
                current_para = []
            i += 1
            continue

        current_para.append(stripped)
        i += 1

    if current_para:
        text = " ".join(current_para)
        if text.strip():
            elements.append(("paragraph", text))

    return chapter_info, elements


def build_chapter_flowables(chapter_info, elements, styles):
    flowables = []
    is_prologue = chapter_info.get("prologue", False)
    is_epilogue = chapter_info.get("epilogue", False)

    flowables.append(Spacer(1, 0.85 * inch))

    if is_prologue:
        flowables.append(Paragraph("PROLOGUE", styles["chapter_num"]))
        flowables.append(Spacer(1, 18))
    elif is_epilogue:
        flowables.append(Paragraph("EPILOGUE", styles["chapter_num"]))
        flowables.append(Spacer(1, 18))
    else:
        num = chapter_info.get("number", 0)
        pov = chapter_info.get("pov", "")
        flowables.append(Paragraph(f"CHAPTER {num}", styles["chapter_num"]))
        flowables.append(Spacer(1, 4))
        flowables.append(Paragraph(pov.upper(), styles["chapter_title"]))
        flowables.append(Spacer(1, 24))

    for elem in elements:
        etype = elem[0]

        if etype == "scene":
            label = elem[1]
            flowables.append(Spacer(1, 12))
            flowables.append(Paragraph(format_inline(label), styles["scene_label"]))
            flowables.append(Spacer(1, 6))

        elif etype == "break":
            flowables.append(Spacer(1, 14))
            flowables.append(Paragraph("* * *", styles["scene_label"]))
            flowables.append(Spacer(1, 8))

        elif etype == "blockquote":
            text = format_inline(elem[1])
            flowables.append(Paragraph(text, styles["blockquote"]))

        elif etype == "paragraph":
            text = format_inline(elem[1])

            if is_prologue:
                flowables.append(Paragraph(text, styles["body_italic_no_indent"]))
            else:
                flowables.append(Paragraph(text, styles["body_no_indent"]))

                for j in range(len(flowables) - 1, -1, -1):
                    f = flowables[j]
                    if isinstance(f, Paragraph) and f.style == styles["body_no_indent"]:
                        f.style = styles["body"]
                        break
                    elif isinstance(f, Paragraph):
                        break

    return flowables


def build_part_page(part_info, styles):
    flowables = []
    flowables.append(Spacer(1, 2.8 * inch))
    flowables.append(Paragraph(f"PART {part_info['number']}", styles["part_num"]))
    flowables.append(Spacer(1, 12))
    flowables.append(Paragraph(part_info["title"], styles["part_title"]))
    flowables.append(PageBreak())
    return flowables


def build_title_page(styles):
    flowables = []
    flowables.append(Spacer(1, 2.5 * inch))
    flowables.append(Paragraph("THE FOURTH STEP", styles["title_main"]))
    flowables.append(Paragraph("A Novel", styles["title_sub"]))
    flowables.append(Paragraph("KAPIL GUPTA", styles["title_author"]))
    flowables.append(PageBreak())
    return flowables


def build_copyright_page(styles):
    flowables = []
    flowables.append(Spacer(1, 0.5 * inch))
    lines = [
        "THE FOURTH STEP",
        "Copyright &copy; 2026 Kapil Gupta",
        "All rights reserved.",
        "",
        "No part of this publication may be reproduced, distributed, or transmitted",
        "in any form or by any means without the prior written permission of the publisher.",
        "",
        "This is a work of fiction. Names, characters, places, and incidents either",
        "are the product of the author's imagination or are used fictitiously.",
        "Any resemblance to actual persons, living or dead, events, or locales",
        "is entirely coincidental.",
        "",
        "First Edition",
        "",
        "Published in Australia",
    ]
    for line in lines:
        if line == "":
            flowables.append(Spacer(1, 8))
        else:
            flowables.append(Paragraph(line, styles["copyright"]))
    flowables.append(PageBreak())
    return flowables


def build_epigraph_page(styles):
    flowables = []
    flowables.append(Spacer(1, 3.5 * inch))
    flowables.append(Paragraph(
        '"The body has no agenda. The body has never been gaslit."',
        styles["epigraph"]
    ))
    flowables.append(PageBreak())
    return flowables


def build_dedication_page(styles):
    flowables = []
    flowables.append(Spacer(1, 3.5 * inch))
    flowables.append(Paragraph("For those who remember.", styles["epigraph"]))
    flowables.append(PageBreak())
    flowables.append(PageBreak())
    return flowables


def get_part_for_chapter_index(idx):
    for part in PARTS:
        start, end = part["range"]
        if start <= idx < end:
            return part
    return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("THE FOURTH STEP — Interior PDF Generator")
    print("=" * 60)
    print(f"  Trim: {TRIM_W/inch:.1f}\" x {TRIM_H/inch:.1f}\"")
    print(f"  Font: Garamond {BODY_SIZE}pt / {BODY_LEADING}pt leading")
    print(f"  Chapters: {len(CHAPTER_ORDER)}")
    print(f"  Parts: {len(PARTS)}")

    class MirroredDoc(BaseDocTemplate):
        def handle_pageBegin(self, **kw):
            super().handle_pageBegin(**kw)
            pn = self.page + 1
            if pn % 2 == 0:
                self._handle_nextPageTemplate("body_even")
            else:
                self._handle_nextPageTemplate("body")

    doc = MirroredDoc(
        OUTPUT_PATH,
        pagesize=(TRIM_W, TRIM_H),
        title="The Fourth Step",
        author="Kapil Gupta",
        subject="Psychological Thriller",
    )

    gutter_odd = GUTTER
    outside_odd = OUTSIDE
    gutter_even = GUTTER
    outside_even = OUTSIDE

    avail_w = TRIM_W - gutter_odd - outside_odd
    avail_h = TRIM_H - TOP_MARGIN - BOTTOM_MARGIN

    frame_odd = Frame(
        gutter_odd, BOTTOM_MARGIN,
        avail_w, avail_h,
        id="odd",
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
    )

    frame_even = Frame(
        outside_even, BOTTOM_MARGIN,
        avail_w, avail_h,
        id="even",
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
    )

    pnc = PageNumCanvas(doc)

    templates = [
        PageTemplate(id="title", frames=[frame_odd], onPage=pnc.on_page_front),
        PageTemplate(id="body", frames=[frame_odd], onPage=pnc.on_page_body),
        PageTemplate(id="body_even", frames=[frame_even], onPage=pnc.on_page_body),
        PageTemplate(id="blank", frames=[frame_odd], onPage=pnc.on_page_blank),
    ]
    doc.addPageTemplates(templates)

    story = []

    story.extend(build_title_page(STYLES))
    story.extend(build_copyright_page(STYLES))
    story.extend(build_dedication_page(STYLES))
    story.extend(build_epigraph_page(STYLES))

    current_part = None
    for idx, chapter_file in enumerate(CHAPTER_ORDER):
        filepath = os.path.join(CHAPTERS_DIR, chapter_file)
        if not os.path.isfile(filepath):
            print(f"  WARNING: {chapter_file} not found, skipping")
            continue

        part = get_part_for_chapter_index(idx)
        if part and part is not current_part:
            current_part = part
            story.extend(build_part_page(part, STYLES))

        chapter_info, elements = parse_chapter(filepath)
        flowables = build_chapter_flowables(chapter_info, elements, STYLES)

        story.append(PageBreak())
        story.extend(flowables)

    total_content = len(CHAPTER_ORDER)
    print(f"  Parsed {total_content} chapters")

    doc.build(story)

    fsize = os.path.getsize(OUTPUT_PATH)
    print(f"\n  Output: {OUTPUT_PATH}")
    print(f"  Size: {fsize / 1024:.0f} KB ({fsize / (1024*1024):.1f} MB)")

    import pikepdf
    pdf = pikepdf.open(OUTPUT_PATH)
    page_count = len(pdf.pages)
    pdf.close()
    print(f"  Pages: {page_count}")

    if page_count % 2 != 0:
        print(f"  NOTE: Odd page count ({page_count}). KDP requires even. Will add blank.")
    else:
        print(f"  Page count is even — KDP ready")

    print("\nDone.")


if __name__ == "__main__":
    main()

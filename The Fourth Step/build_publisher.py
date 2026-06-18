"""
The Fourth Step — Publisher Submission PDF Generator
Creates FirstStep_Publisher.pdf with:
  1. Front cover image as page 1
  2. Prologue + Chapters 1-4
  3. Synopsis at the end
"""

import os
import re
from reportlab.lib.pagesizes import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

BASE = r"D:\Kapil\Books\The Fourth Step"
CHAPTERS_DIR = os.path.join(BASE, "Chapters")
OUTPUT_DIR = os.path.join(BASE, "Output")
COVER_IMG = os.path.join(BASE, "Cover", "The_Fourth_Step_Kindle.jpg")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "FirstStep_Publisher.pdf")
FONTS_DIR = r"C:\Windows\Fonts"

TRIM_W = 5.5 * inch
TRIM_H = 8.5 * inch

TOP_MARGIN = 0.65 * inch
BOTTOM_MARGIN = 0.75 * inch
LEFT_MARGIN = 0.65 * inch
RIGHT_MARGIN = 0.55 * inch

BODY_SIZE = 11
BODY_LEADING = 14.5

DARK = HexColor('#1a1a1a')
MID = HexColor('#333333')
DIM = HexColor('#888888')

CHAPTERS = [
    "prologue.md",
    "chapter-01-neve.md",
    "chapter-02-saskia.md",
    "chapter-03-imogen.md",
    "chapter-04-rowan.md",
]

SYNOPSIS_TEXT = [
    ("italic", "Some houses don\u2019t forget. They wait."),
    ("body", ""),
    ("body",
     "Twenty-five years ago, a girl died at a sleepover on the "
     "Mornington Peninsula. The case was closed. The house was "
     "renovated. Everyone moved on."),
    ("body", ""),
    ("body",
     "Now four women have returned to the house on the coast \u2014 "
     "each remembering that night differently, each hiding "
     "something, each lying to themselves."),
    ("body", ""),
    ("body",
     "Neve can\u2019t trust her own memories. Saskia measures "
     "everything because measurement doesn\u2019t lie. Imogen is "
     "running from a past that\u2019s catching up. And Rowan \u2014 "
     "the stranger among them \u2014 is documenting every crack "
     "in every story."),
    ("body", ""),
    ("body", "Someone knows what happened to Kiera."),
    ("body", "Someone has known all along."),
]


def register_fonts():
    fonts = [
        ("Garamond", os.path.join(FONTS_DIR, "GARA.TTF")),
        ("GaramondBold", os.path.join(FONTS_DIR, "GARABD.TTF")),
        ("GaramondItalic", os.path.join(FONTS_DIR, "GARAIT.TTF")),
        ("Georgia", os.path.join(FONTS_DIR, "georgia.ttf")),
        ("GeorgiaBold", os.path.join(FONTS_DIR, "georgiab.ttf")),
        ("GeorgiaItalic", os.path.join(FONTS_DIR, "georgiai.ttf")),
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
        firstLineIndent=18,
    )

    s["body_no_indent"] = ParagraphStyle(
        "BodyNoIndent",
        parent=s["body"],
        firstLineIndent=0,
    )

    s["body_italic_no_indent"] = ParagraphStyle(
        "BodyItalicNoIndent",
        parent=s["body"],
        fontName="GaramondItalic",
        textColor=MID,
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

    s["page_num"] = ParagraphStyle(
        "PageNum",
        fontName="Garamond",
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=DIM,
    )

    s["synopsis_heading"] = ParagraphStyle(
        "SynopsisHeading",
        fontName="Garamond",
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=DARK,
        characterSpacing=2,
    )

    s["synopsis_body"] = ParagraphStyle(
        "SynopsisBody",
        fontName="Garamond",
        fontSize=11,
        leading=15,
        alignment=TA_JUSTIFY,
        textColor=DARK,
        firstLineIndent=0,
    )

    s["synopsis_italic"] = ParagraphStyle(
        "SynopsisItalic",
        parent=s["synopsis_body"],
        fontName="GaramondItalic",
        textColor=MID,
    )

    return s


STYLES = make_styles()


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

        if stripped.startswith("*") and not stripped.startswith("**") and "\u2014" in stripped and len(stripped) > 40:
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

    flowables.append(Spacer(1, 0.85 * inch))

    if is_prologue:
        flowables.append(Paragraph("PROLOGUE", styles["chapter_num"]))
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


def build_synopsis(styles):
    flowables = []
    flowables.append(Spacer(1, 2.0 * inch))
    flowables.append(Paragraph("SYNOPSIS", styles["synopsis_heading"]))
    flowables.append(Spacer(1, 24))

    for style_name, text in SYNOPSIS_TEXT:
        if text == "":
            flowables.append(Spacer(1, 8))
        elif style_name == "italic":
            flowables.append(Paragraph(format_inline(text), styles["synopsis_italic"]))
        else:
            flowables.append(Paragraph(format_inline(text), styles["synopsis_body"]))

    flowables.append(Spacer(1, 36))
    comp_font = ParagraphStyle(
        "Comp",
        fontName="GaramondItalic",
        fontSize=10.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=MID,
    )
    flowables.append(Paragraph(
        "For readers of <i>Gone Girl</i> and <i>The Girl on the Train</i>.",
        comp_font
    ))
    return flowables


def on_page_body(canvas, doc):
    page_num = canvas.getPageNumber()
    if page_num <= 1:
        return
    canvas.saveState()
    canvas.setFont("Garamond", 9)
    canvas.setFillColor(DIM)
    y = BOTTOM_MARGIN - 0.15 * inch
    canvas.drawCentredString(TRIM_W / 2, y, str(page_num - 1))
    canvas.restoreState()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("THE FOURTH STEP — Publisher Submission PDF")
    print("=" * 60)

    doc = BaseDocTemplate(
        OUTPUT_PATH,
        pagesize=(TRIM_W, TRIM_H),
        title="The Fourth Step — Publisher Submission",
        author="Kapil Gupta",
    )

    frame_body = Frame(
        LEFT_MARGIN, BOTTOM_MARGIN,
        TRIM_W - LEFT_MARGIN - RIGHT_MARGIN,
        TRIM_H - TOP_MARGIN - BOTTOM_MARGIN,
        id="body",
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
    )

    frame_cover = Frame(
        0, 0, TRIM_W, TRIM_H,
        id="cover",
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
    )

    templates = [
        PageTemplate(id="cover", frames=[frame_cover]),
        PageTemplate(id="body", frames=[frame_body], onPage=on_page_body),
    ]
    doc.addPageTemplates(templates)

    story = []

    print("\n  Page 1: Front cover image")
    cover_img = Image.open(COVER_IMG).convert("RGB")
    cw, ch = cover_img.size
    from reportlab.platypus import Image as RLImage
    cover_rl = RLImage(COVER_IMG, width=TRIM_W, height=TRIM_H)
    story.append(cover_rl)
    story.append(PageBreak())

    from reportlab.platypus import NextPageTemplate
    story.append(NextPageTemplate("body"))

    for chapter_file in CHAPTERS:
        filepath = os.path.join(CHAPTERS_DIR, chapter_file)
        if not os.path.isfile(filepath):
            print(f"  WARNING: {chapter_file} not found, skipping")
            continue

        chapter_info, elements = parse_chapter(filepath)
        flowables = build_chapter_flowables(chapter_info, elements, STYLES)

        is_prologue = chapter_info.get("prologue", False)
        if is_prologue:
            print(f"  Adding: Prologue")
        else:
            num = chapter_info.get("number", 0)
            pov = chapter_info.get("pov", "")
            print(f"  Adding: Chapter {num} ({pov})")

        story.append(PageBreak())
        story.extend(flowables)

    print("\n  Adding: Synopsis")
    story.append(PageBreak())
    story.extend(build_synopsis(STYLES))

    doc.build(story)

    import pikepdf
    pdf = pikepdf.open(OUTPUT_PATH)
    page_count = len(pdf.pages)
    pdf.close()

    fsize = os.path.getsize(OUTPUT_PATH)
    print(f"\n  Output: {OUTPUT_PATH}")
    print(f"  Size: {fsize / 1024:.0f} KB ({fsize / (1024*1024):.1f} MB)")
    print(f"  Pages: {page_count}")
    print("\nDone.")


if __name__ == "__main__":
    main()

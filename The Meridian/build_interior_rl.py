#!/usr/bin/env python3
"""Build THE MERIDIAN interior PDF with reportlab — 5.5x8.5 trade paperback,
Garamond Linotype, dense justified body with hyphenation, page numbers, TOC."""
import os, re, glob
from reportlab.lib.units import inch as IN
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, Table, TableStyle, NextPageTemplate)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

ROOT = r"D:\Kapil\Books\Heist"
CH   = os.path.join(ROOT, "Chapters")
OUT  = os.path.join(ROOT, "Output", "TheMeridian.pdf")

# ---------- fonts (Garamond class — closest available to trade-thriller house serifs) ----------
FD = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Garamond", os.path.join(FD, "GARA.TTF")))
pdfmetrics.registerFont(TTFont("Garamond-Bold", os.path.join(FD, "GARABD.TTF")))
pdfmetrics.registerFont(TTFont("Garamond-Italic", os.path.join(FD, "GARAIT.TTF")))
registerFontFamily("Garamond", normal="Garamond", bold="Garamond-Bold",
                   italic="Garamond-Italic", boldItalic="Garamond-Italic")  # no BI shipped; fall back to italic

# ---------- geometry 5.5 x 8.5 ----------
PW, PH = 5.5*IN, 8.5*IN
INNER, OUTER, TOP, BOTTOM = 0.75*IN, 0.625*IN, 0.7*IN, 0.8*IN
FS, LEAD = 11, 13.6   # body font / leading -> dense trade look (Garamond runs small)

# ---------- styles ----------
body = ParagraphStyle = __import__("reportlab.lib.styles", fromlist=["ParagraphStyle"]).ParagraphStyle
S_body = body("body", fontName="Garamond", fontSize=FS, leading=LEAD, alignment=TA_JUSTIFY,
              firstLineIndent=0.26*IN, hyphenationLang="en_US", wordWrap="LTR")
S_first = body("first", parent=S_body, firstLineIndent=0)
S_chap  = body("chap", fontName="Garamond-Bold", fontSize=15, leading=19, alignment=TA_CENTER,
               spaceBefore=0, spaceAfter=4)
S_sub   = body("sub", fontName="Garamond-Italic", fontSize=9, leading=12, alignment=TA_CENTER,
               textColor=colors.HexColor("#555555"), spaceBefore=1, spaceAfter=12)
S_scene = body("scene", fontName="Garamond", fontSize=8.5, leading=11, alignment=TA_CENTER,
               textColor=colors.HexColor("#9a9a9a"), spaceBefore=6, spaceAfter=6)
S_tbig  = body("tbig", fontName="Garamond-Bold", fontSize=30, leading=36, alignment=TA_CENTER)
S_tsub  = body("tsub", fontName="Garamond-Italic", fontSize=13, leading=18, alignment=TA_CENTER)
S_ttag  = body("ttag", fontName="Garamond-Italic", fontSize=8.5, leading=12.5, alignment=TA_CENTER,
               textColor=colors.HexColor("#444444"))
S_auth  = body("auth", fontName="Garamond", fontSize=12, leading=16, alignment=TA_CENTER)
S_copy  = body("copy", fontName="Garamond", fontSize=7.5, leading=10.5, alignment=TA_LEFT)
S_ded   = body("ded", fontName="Garamond-Italic", fontSize=11, leading=15, alignment=TA_CENTER)

def inline(t):
    t = t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*",   r"<i>\1</i>", t)
    return t

# ---------- chapter parser ----------
def parse_chapter(path):
    out = []
    subs = []
    title = os.path.basename(path)
    para = []; table_rows = []; first_after_break = True

    def flush_para():
        nonlocal para, first_after_break
        if para:
            txt = inline(" ".join(para).strip())
            if txt:
                out.append(Paragraph(txt, S_first if first_after_break else S_body))
                first_after_break = False
        para = []

    def flush_table():
        nonlocal table_rows, first_after_break
        if table_rows:
            data = [[inline(c.strip()) for c in r.strip().strip("|").split("|")] for r in table_rows]
            data = [row for row in data if not all(set(c) <= set("-: ") for c in row)]  # drop sep
            if data:
                ncols = len(data[0])
                avail = PW - INNER - OUTER
                cw = [avail*0.07, avail*0.50, avail*0.20, avail*0.23][:ncols]
                if len(cw) < ncols: cw = [avail/ncols]*ncols
                tbl = Table(data, colWidths=cw, hAlign="CENTER")
                tbl.setStyle(TableStyle([
                    ("FONT",(0,0),(-1,-1),"Garamond",8),
                    ("FONT",(0,0),(-1,0),"Garamond-Bold",7.5),
                    ("TEXTCOLOR",(0,0),(-1,-1),colors.HexColor("#222222")),
                    ("LINEBELOW",(0,0),(-1,0),0.5,colors.HexColor("#888888")),
                    ("LINEBELOW",(0,-1),(-1,-1),0.5,colors.HexColor("#888888")),
                    ("ROWBACKGROUNDS",(0,0),(-1,0),[colors.HexColor("#f0f0f0")]),
                    ("TOPPADDING",(0,0),(-1,-1),2.5),("BOTTOMPADDING",(0,0),(-1,-1),2.5),
                    ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
                    ("ALIGN",(0,0),(-1,-1),"LEFT"),
                ]))
                out.append(tbl); out.append(Spacer(1, 6))
                first_after_break = False
        table_rows = []

    lines = open(path, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip().startswith("# "):
        i += 1
    if i < len(lines):
        title = lines[i].strip()[2:].strip()
        i += 1
    for l in lines[i:]:
        s = l.strip()
        if s.startswith("## "):
            flush_para(); flush_table(); subs.append(s[3:].strip())
        elif s == "---":
            flush_para(); flush_table()
            out.append(Paragraph("&#9670; &#9670; &#9670;", S_scene))
            first_after_break = True
        elif s.startswith("|"):
            flush_para(); table_rows.append(s)
        elif s == "":
            flush_para()
        else:
            para.append(s)
    flush_para(); flush_table()

    flow = [Paragraph(title.upper(), S_chap)]
    for sb in subs:
        flow.append(Paragraph(inline(sb), S_sub))
    flow.extend(out)
    return title, flow

# ---------- doc with TOC + page numbers ----------
class BookDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "chap":
            text = flowable.getPlainText()
            self.notify("TOCEntry", (0, text, self.page))

def footer(canvas, doc):
    if doc.page > 1:
        canvas.saveState()
        canvas.setFont("Garamond", 8.5)
        canvas.setFillColor(colors.HexColor("#6a6a6a"))
        canvas.drawCentredString(PW/2, 0.45*IN, str(doc.page))
        canvas.restoreState()

def blank(canvas, doc):
    pass

frame = Frame(INNER, BOTTOM, PW-INNER-OUTER, PH-TOP-BOTTOM, id="main",
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc = BookDoc(OUT, pagesize=(PW, PH),
              leftMargin=INNER, rightMargin=OUTER, topMargin=TOP, bottomMargin=BOTTOM)
doc.addPageTemplates([
    PageTemplate(id="body", frames=[frame], onPage=footer),
    PageTemplate(id="blank", frames=[frame], onPage=blank),
])

story = []
# ---- TITLE PAGE ----
story.append(NextPageTemplate("body"))
story.append(Spacer(1, 2.3*IN))
story.append(Paragraph("THE MERIDIAN", S_tbig))
story.append(Spacer(1, 0.3*IN))
story.append(Paragraph("A Heist Thriller", S_tsub))
story.append(Spacer(1, 0.2*IN))
story.append(Paragraph("Ocean's Eleven meets Murder on the Orient Express<br/>"
                       "at six hundred kilometres an hour<br/>&#8212; with codes you can "
                       "solve before the thief does.", S_ttag))
story.append(Spacer(1, 2.2*IN))
story.append(Paragraph("KAPIL GUPTA", S_auth))
story.append(PageBreak())
# ---- COPYRIGHT ----
story.append(Spacer(1, 1.6*IN))
cpy = ("THE MERIDIAN &mdash; A Heist Thriller<br/><br/>"
       "Copyright &#169; 2026 Kapil Gupta. All rights reserved.<br/><br/>"
       "No part of this publication may be reproduced, distributed, or transmitted "
       "in any form or by any means without the prior written permission of the "
       "publisher, except for brief quotations in reviews and certain noncommercial "
       "uses permitted by copyright law.<br/><br/>"
       "This is a work of fiction. Names, characters, places, and incidents are "
       "either the product of the author&rsquo;s imagination or are used fictitiously. "
       "Any resemblance to actual persons, living or dead, events, or locales is "
       "entirely coincidental.<br/><br/>First Edition")
story.append(Paragraph(cpy, S_copy))
story.append(PageBreak())
# ---- DEDICATION ----
story.append(Spacer(1, 4.6*IN))
story.append(Paragraph("For the ones who count doors.", S_ded))
story.append(PageBreak())
# ---- CHAPTERS ----
for f in sorted(glob.glob(os.path.join(CH, "*.md"))):
    title, flow = parse_chapter(f)
    story.extend(flow)
    story.append(PageBreak())
# drop trailing page break
if story and isinstance(story[-1], PageBreak):
    story.pop()

doc.build(story)
print("Built:", OUT)
from pypdf import PdfReader
print("Pages:", len(PdfReader(OUT).pages), "| Size: %.2f MB" % (os.path.getsize(OUT)/1e6))

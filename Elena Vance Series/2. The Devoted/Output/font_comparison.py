# -*- coding: utf-8 -*-
"""Font comparison PDF for THE DEVOTED."""
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle

FD = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Gara", FD + r"\GARA.TTF"))
pdfmetrics.registerFont(TTFont("Gara-B", FD + r"\GARABD.TTF"))
pdfmetrics.registerFont(TTFont("Gara-I", FD + r"\GARAIT.TTF"))
pdfmetrics.registerFontFamily("Gara", normal="Gara", bold="Gara-B", italic="Gara-I", boldItalic="Gara-B")
pdfmetrics.registerFont(TTFont("Georgia", FD + r"\georgia.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-B", FD + r"\georgiab.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-I", FD + r"\georgiai.ttf"))
pdfmetrics.registerFontFamily("Georgia", normal="Georgia", bold="Georgia-B", italic="Georgia-I", boldItalic="Georgia-B")

INK = HexColor("#1a1a1a")
GREY = HexColor("#6a6a6a")
PW, PH = 5.5 * inch, 8.5 * inch
LM, RM, TM, BM = 0.78 * inch, 0.66 * inch, 0.74 * inch, 0.72 * inch

OUT = r"D:\Kapil\Books\Elena Vance Series\Second\Output\font_comparison.pdf"

SAMPLE = (
    "The man across from me was lying, and it was the most interesting thing about him. "
    "He didn&#39;t know it. They never do. By the time a man like David has climbed into the good leather "
    "chair across from mine &mdash; fifty-two, software, a jaw you could break rocks on &mdash; he has "
    "told the story so often, to his board, his wife, the bathroom mirror, that it leaves his mouth oiled "
    "and seamless, without a single seam for the fingers to find.<br/><br/>"
    "&ldquo;The culture&#39;s the problem,&rdquo; he said. &ldquo;I keep an open door. I&#39;ve told them a hundred "
    "times. They just won&#39;t use it.&rdquo;<br/><br/>"
    "He believed it. I let the half-second go &mdash; the held breath I use in sessions, the silence that "
    "means <i>the floor is yours, take it</i> &mdash; and I watched his hands. They rested on his knees, "
    "palms down, fingers splayed: open posture, open man. But his left thumb was pressing into his kneecap, "
    "hard enough to whiten the nail, in a count of three, rest, three, rest, three. Counting something his "
    "mouth would not.<br/><br/>"
    "I noted it. I didn&#39;t name it. Naming comes later, if it comes at all."
)

fonts = [
    ("Garamond (current)", "Gara", "Gara-B", "Gara-I"),
    ("Georgia", "Georgia", "Georgia-B", "Georgia-I"),
]

story = []
for label, fn, fb, fi in fonts:
    body = ParagraphStyle("body", fontName=fn, fontSize=10.3, leading=13.4, alignment=TA_JUSTIFY, firstLineIndent=14, textColor=INK)
    bodyf = ParagraphStyle("bodyf", parent=body, firstLineIndent=0)
    hdr = ParagraphStyle("hdr", fontName=fb, fontSize=14, alignment=TA_CENTER, textColor=GREY, spaceAfter=6)
    sub = ParagraphStyle("sub", fontName=fi, fontSize=9, alignment=TA_CENTER, textColor=GREY, spaceAfter=16)

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(label, hdr))
    story.append(Paragraph(fn + " &middot; 10.3pt / 13.4 leading", sub))
    story.append(Paragraph(SAMPLE, bodyf))
    story.append(PageBreak())

doc = SimpleDocTemplate(OUT, pagesize=(PW, PH), leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM)
doc.build(story)
print("Comparison PDF:", OUT)

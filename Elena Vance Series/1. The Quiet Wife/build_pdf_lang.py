# -*- coding: utf-8 -*-
"""Interior PDF builder for THE QUIET WIFE — DE / ES / FR editions.
Reuses the English build_pdf.py machinery (reportlab + Garamond/Consolas + shaped cards)."""
import re, html
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, PageTemplate as _PT, NextPageTemplate, Flowable)
from reportlab.lib.styles import ParagraphStyle

FONTDIR = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Gara", FONTDIR + r"\GARA.TTF"))
pdfmetrics.registerFont(TTFont("Gara-B", FONTDIR + r"\GARABD.TTF"))
pdfmetrics.registerFont(TTFont("Gara-I", FONTDIR + r"\GARAIT.TTF"))
pdfmetrics.registerFontFamily("Gara", normal="Gara", bold="Gara-B", italic="Gara-I", boldItalic="Gara-B")
pdfmetrics.registerFont(TTFont("Mono", FONTDIR + r"\consola.ttf"))
pdfmetrics.registerFont(TTFont("Mono-B", FONTDIR + r"\consolab.ttf"))
pdfmetrics.registerFont(TTFont("Mono-I", FONTDIR + r"\consolai.ttf"))
pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="Mono-B", italic="Mono-I", boldItalic="Mono-B")

PW, PH = 5.5 * inch, 8.5 * inch
LM, RM, TM, BM = 0.78 * inch, 0.66 * inch, 0.74 * inch, 0.72 * inch
TEXTW = PW - LM - RM
INK = HexColor("#1a1a1a"); GREY = HexColor("#6a6a6a")

BODY = ParagraphStyle("body", fontName="Gara", fontSize=10.3, leading=13.4, alignment=TA_JUSTIFY, firstLineIndent=14, textColor=INK, allowWidows=0, allowOrphans=0)
BODYF = ParagraphStyle("bodyf", parent=BODY, firstLineIndent=0)
CNUM = ParagraphStyle("cnum", fontName="Gara", fontSize=10.5, leading=13, alignment=TA_CENTER, textColor=GREY, spaceAfter=10, keepWithNext=1)
CTITLE = ParagraphStyle("ctitle", fontName="Gara-B", fontSize=21, leading=25, alignment=TA_CENTER, textColor=INK, spaceAfter=4, keepWithNext=1)
CODE = ParagraphStyle("code", fontName="Mono", fontSize=8.3, leading=10.9, textColor=INK)
TMAIN = ParagraphStyle("tmain", fontName="Gara-B", fontSize=30, leading=36, alignment=TA_CENTER, textColor=INK)
TSUB = ParagraphStyle("tsub", fontName="Gara-I", fontSize=13, leading=18, alignment=TA_CENTER, textColor=GREY)
SCENE = ParagraphStyle("scene", fontName="Gara", fontSize=11, leading=14, alignment=TA_CENTER, textColor=GREY, spaceBefore=8, spaceAfter=8)
HDR = ParagraphStyle("hdr", fontName="Mono-B", fontSize=8, leading=10, alignment=TA_LEFT, textColor=white)
MSGBODY = ParagraphStyle("msgbody", fontName="Gara", fontSize=9.7, leading=12.6, alignment=TA_LEFT, textColor=INK)

TOOL = {
    "NOTE": {"accent":"#B8860B","tint":"#FAEFD0","label":"NOTES"},
    "SEARCH":{"accent":"#2C6FB0","tint":"#DFEAFA","label":"SEARCH"},
    "FORUM": {"accent":"#0E7C7B","tint":"#D2EEEE","label":u"DM  \u00b7  FORUM"},
    "CHAT":  {"accent":"#6A4FA6","tint":"#E8E2F4","label":"AI ASSISTANT"},
    "TRANSCRIPT":{"accent":"#54565E","tint":"#E7E7EC","label":"TRANSCRIPT"},
    "WHATSAPP":{"accent":"#1E8E3E","tint":"#DCF0DC","label":"MESSAGE"},
    "FINDMY":{"accent":"#B23A48","tint":"#F6DEE2","label":"ALERT"},
}
RADIUS = {"NOTE":12,"SEARCH":6,"FORUM":8,"CHAT":12,"TRANSCRIPT":1.5,"WHATSAPP":12,"FINDMY":12}

def _mag(c,x,y,s):
    c.setLineWidth(1.1); c.setStrokeColor(white); r=s*0.3; cx,cy=x+s*0.42,y+s*0.6
    c.circle(cx,cy,r,stroke=1,fill=0); c.line(cx+r*0.7,cy-r*0.7,x+s*0.92,y+s*0.12)
def _pencil(c,x,y,s):
    c.setLineWidth(1.2); c.setStrokeColor(white)
    c.line(x+s*0.18,y+s*0.18,x+s*0.66,y+s*0.66); c.line(x+s*0.18,y+s*0.18,x+s*0.3,y+s*0.06)
    c.line(x+s*0.66,y+s*0.66,x+s*0.8,y+s*0.52); c.line(x+s*0.18,y+s*0.18,x+s*0.3,y+s*0.3)
def _bubble(c,x,y,s):
    c.setLineWidth(1.1); c.setStrokeColor(white)
    c.roundRect(x+s*0.12,y+s*0.3,s*0.76,s*0.5,s*0.1,stroke=1,fill=0)
    p=c.beginPath(); p.moveTo(x+s*0.3,y+s*0.3); p.lineTo(x+s*0.22,y+s*0.1); p.lineTo(x+s*0.46,y+s*0.32); c.drawPath(p,stroke=1,fill=0)
def _spark(c,x,y,s):
    c.setLineWidth(1.0); c.setStrokeColor(white); cx,cy=x+s*0.5,y+s*0.5
    c.line(cx,cy+s*0.42,cx,cy-s*0.42); c.line(cx-s*0.42,cy,cx+s*0.42,cy)
    c.line(cx-s*0.18,cy-s*0.18,cx+s*0.18,cy+s*0.18); c.line(cx-s*0.18,cy+s*0.18,cx+s*0.18,cy-s*0.18)
def _scales(c,x,y,s):
    c.setLineWidth(1.0); c.setStrokeColor(white); cx=x+s*0.5
    c.line(cx,y+s*0.15,cx,y+s*0.82); c.line(x+s*0.2,y+s*0.76,x+s*0.8,y+s*0.76)
    c.circle(x+s*0.2,y+s*0.58,s*0.11,stroke=1,fill=0); c.circle(x+s*0.8,y+s*0.58,s*0.11,stroke=1,fill=0)
    c.line(x+s*0.2,y+s*0.76,x+s*0.2,y+s*0.69); c.line(x+s*0.8,y+s*0.76,x+s*0.8,y+s*0.69)
def _phone(c,x,y,s):
    c.setFillColor(white); c.setStrokeColor(white); c.setLineWidth(0); c.roundRect(x+s*0.3,y+s*0.12,s*0.4,s*0.76,s*0.07,stroke=0,fill=1)
def _pin(c,x,y,s):
    c.setFillColor(white); c.setStrokeColor(white); c.setLineWidth(0); cx=x+s*0.5
    c.circle(cx,y+s*0.62,s*0.24,stroke=0,fill=1)
    p=c.beginPath(); p.moveTo(cx-s*0.22,y+s*0.55); p.lineTo(cx,y+s*0.08); p.lineTo(cx+s*0.22,y+s*0.55); p.close(); c.drawPath(p,stroke=0,fill=1)
ICONS = {"NOTE":_pencil,"SEARCH":_mag,"FORUM":_bubble,"CHAT":_spark,"TRANSCRIPT":_scales,"WHATSAPP":_phone,"FINDMY":_pin}
ICON_S = 10

def clean(t):
    t = re.sub(r'[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F]', '', t)
    return t.replace('\u2192', '->')
def inline(t):
    t = html.escape(clean(t), quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    return t
def code_body_html(lines):
    out=[]
    for ln in lines:
        ln = clean(ln).replace('**','').replace('*','')
        ln = html.escape(ln, quote=False)
        lead = len(ln)-len(ln.lstrip(' '))
        out.append('&nbsp;'*lead + ln.lstrip(' '))
    return '<br/>'.join(out)

# code-block classifier: recognise headers in EN/DE/ES/FR
def classify_code(lines):
    first=""
    for ln in lines:
        if ln.strip(): first=clean(ln).strip().lower(); break
    if any(first.startswith(k) for k in ("note","notiz","nota")): return "NOTE"
    if any(first.startswith(k) for k in ("search","suche","recherche","busqueda","búsqueda")): return "SEARCH"
    if any(first.startswith(k) for k in ("transcript","transkript","transcripcion","transcripción","transcription")): return "TRANSCRIPT"
    if first.startswith("chat"): return "CHAT"
    if any(first.startswith(k) for k in ("dm","r/","truecrime","antwort","respuesta","reponse","réponse","reply")): return "FORUM"
    return "NOTE"

STATE = {"chapter":""}
class SetChapter(Flowable):
    def __init__(self,t): self.t=t; Flowable.__init__(self)
    def wrap(self,*_): return (0,0)
    def draw(self): STATE["chapter"]=self.t

HEADER_TITLE={"de":"","es":"","fr":""}
def normal_page(canvas,doc):
    canvas.saveState(); canvas.setFillColor(GREY); pg=doc.page; ht=HEADER_TITLE
    if pg%2==0:
        canvas.setFont("Gara-I",9); canvas.drawString(LM,PH-0.46*inch,ht)
        canvas.setFont("Gara",9); canvas.drawString(LM,0.50*inch,str(pg))
    else:
        canvas.setFont("Gara-I",9); canvas.drawRightString(PW-RM,PH-0.46*inch,STATE["chapter"] or "")
        canvas.setFont("Gara",9); canvas.drawRightString(PW-RM,0.50*inch,str(pg))
    canvas.restoreState()
def chapter_page(canvas,doc):
    canvas.saveState(); canvas.setFillColor(GREY); canvas.setFont("Gara",9)
    canvas.drawCentredString(PW/2,0.50*inch,str(doc.page)); canvas.restoreState()
def blank_page(canvas,doc):
    canvas.saveState(); canvas.restoreState()

def mixed_path(c,x,y,w,h,r,tr,br):
    p=c.beginPath()
    if tr:
        p.moveTo(x,y+h-r); p.curveTo(x,y+h,x,y+h,x+r,y+h); p.lineTo(x+w-r,y+h); p.curveTo(x+w,y+h,x+w,y+h,x+w,y+h-r)
    else:
        p.moveTo(x,y+h); p.lineTo(x+w,y+h)
    if br:
        p.lineTo(x+w,y+r); p.curveTo(x+w,y,x+w,y,x+w-r,y); p.lineTo(x+r,y); p.curveTo(x,y,x,y,x,y+r)
    else:
        p.lineTo(x+w,y); p.lineTo(x,y)
    p.close(); return p

class ShapedCard(Flowable):
    def __init__(self,kind,body_flow,header=True,top_round=True,bottom_round=True,cont_label=False):
        Flowable.__init__(self); self.kind=kind; self.body_flow=body_flow
        self.header=header; self.top_round=top_round; self.bottom_round=bottom_round; self.cont_label=cont_label
        st=TOOL[kind]; self.accent=HexColor(st["accent"]); self.tint=HexColor(st["tint"]); self.label=st["label"]
        self.radius=RADIUS[kind]; self.hpad=10; self.vpad=6; self.header_h=16; self.icon_gap=16
    def wrap(self,aw,ah):
        self.width=aw; inner_w=aw-2*self.hpad; total=0; self._bw=[]
        for f in self.body_flow:
            _,fh=f.wrap(inner_w,ah); self._bw.append((f,fh)); total+=fh
        self._body_h=total; top=self.header_h if self.header else 0; cextra=12 if self.cont_label else 0
        self.height=top+self._body_h+self.vpad+cextra; return (self.width,self.height)
    def _extras(self,c,W,H):
        if self.kind=='CHAT':
            c.setFillColor(white); dy=H-self.header_h/2.0
            for xx in (W-12,W-19,W-26): c.circle(xx,dy,1.6,stroke=0,fill=1)
        elif self.kind in ('WHATSAPP','FINDMY'):
            c.setFillColor(self.accent); r=self.radius; p=c.beginPath()
            p.moveTo(r*0.7,H); p.lineTo(r*0.7,H-12); p.lineTo(-5,H-3); p.close(); c.drawPath(p,stroke=0,fill=1)
        elif self.kind=='TRANSCRIPT':
            c.setStrokeColor(self.accent); c.setLineWidth(0.6); c.rect(2.5,2.5,W-5,H-5,stroke=1,fill=0)
    def draw(self):
        c=self.canv; W=self.width; H=self.height; r=self.radius; tr=self.top_round; br=self.bottom_round
        top=self.header_h if self.header else 0; cextra=12 if self.cont_label else 0; bh=H-top-cextra
        c.setFillColor(self.tint); c.setStrokeColor(self.tint); c.setLineWidth(0)
        c.drawPath(mixed_path(c,0,0,W,H,r,tr,br),stroke=0,fill=1)
        if self.header:
            c.setFillColor(self.accent); c.drawPath(mixed_path(c,0,H-self.header_h,W,self.header_h,r,tr,False),stroke=0,fill=1)
        if self.cont_label:
            c.setFillColor(self.accent); c.setFont("Mono-B",7); c.drawString(self.hpad,H-9,"(continued)")
        c.setStrokeColor(self.accent); c.setLineWidth(0.75); c.drawPath(mixed_path(c,0,0,W,H,r,tr,br),stroke=1,fill=0)
        if self.header:
            c.saveState(); ICONS[self.kind](c,self.hpad,(H-self.header_h)+(self.header_h-ICON_S)/2.0,ICON_S); c.restoreState()
            self._hdr=Paragraph(self.label,HDR); _,hh=self._hdr.wrap(W-2*self.hpad-self.icon_gap,H)
            self._hdr.drawOn(c,self.hpad+self.icon_gap,(H-self.header_h)+(self.header_h-hh)/2.0); self._extras(c,W,H)
        y=bh-self.vpad
        for f,fh in self._bw: y-=fh; f.drawOn(c,self.hpad,y)
    def split(self,aw,ah):
        self.wrap(aw,ah)
        if self.height<=ah: return [self]
        inner_w=aw-2*self.hpad; top=self.header_h if self.header else 0; cextra=12 if self.cont_label else 0
        avail_body=ah-top-self.vpad-cextra
        if avail_body<42: return []
        f=self.body_flow[0]; parts=f.split(inner_w,avail_body)
        if not parts or len(parts)<2: return []
        a=ShapedCard(self.kind,[parts[0]],header=self.header,top_round=self.top_round,bottom_round=False)
        b=ShapedCard(self.kind,parts[1:],header=False,top_round=False,bottom_round=True,cont_label=True)
        a.wrap(aw,ah); b.wrap(aw,ah); return [a,b]

def tool_card(lines): return [Spacer(1,13),ShapedCard(classify_code(lines),[Paragraph(code_body_html(lines),CODE)]),Spacer(1,13)]
def message_card(qlines):
    joined=clean(" ".join(qlines)).lower()
    kind="FINDMY" if any(k in joined for k in ("find my","localizar","localiser")) else "WHATSAPP"
    body_html="<br/>".join(inline(x) for x in qlines)
    return [Spacer(1,13),ShapedCard(kind,[Paragraph(body_html,MSGBODY)]),Spacer(1,13)]

# ---------- per-language data ----------
NUMW = {
 "de":["","Eins","Zwei","Drei","Vier","Fünf","Sechs","Sieben","Acht","Neun","Zehn","Elf","Zwölf",
   "Dreizehn","Vierzehn","Fünfzehn","Sechzehn","Siebzehn","Achtzehn","Neunzehn","Zwanzig",
   "Einundzwanzig","Zweiundzwanzig","Dreiundzwanzig","Vierundzwanzig","Fünfundzwanzig","Sechsundzwanzig",
   "Siebenundzwanzig","Achtundzwanzig","Neunundzwanzig","Dreißig","Einunddreißig","Zweiunddreißig",
   "Dreiunddreißig","Vierunddreißig","Fünfunddreißig","Sechsunddreißig"],
 "es":["","Uno","Dos","Tres","Cuatro","Cinco","Seis","Siete","Ocho","Nueve","Diez","Once","Doce",
   "Trece","Catorce","Quince","Dieciséis","Diecisiete","Dieciocho","Diecinueve","Veinte",
   "Veintiuno","Veintidós","Veintitrés","Veinticuatro","Veinticinco","Veintiséis","Veintisiete",
   "Veintiocho","Veintinueve","Treinta","Treinta y Uno","Treinta y Dos","Treinta y Tres",
   "Treinta y Cuatro","Treinta y Cinco","Treinta y Seis"],
 "fr":["","Un","Deux","Trois","Quatre","Cinq","Six","Sept","Huit","Neuf","Dix","Onze","Douze",
   "Treize","Quatorze","Quinze","Seize","Dix-sept","Dix-huit","Dix-neuf","Vingt",
   "Vingt et Un","Vingt-deux","Vingt-trois","Vingt-quatre","Vingt-cinq","Vingt-six","Vingt-sept",
   "Vingt-huit","Vingt-neuf","Trente","Trente et Un","Trente-deux","Trente-trois",
   "Trente-quatre","Trente-cinq","Trente-six"],
}
LANG = {
 "de":{"src":r"German\manuscript.md","out":r"German\Die_Stille_Frau_interior.pdf",
       "title":"DIE STILLE FRAU","sub":"Die Elena Vance Reihe &middot; Band 1","novel":"ein Roman",
       "header":"Die stille Frau","chapmark":"# Kapitel ","chprefix":"Kapitel "},
 "es":{"src":r"Spanish\manuscript.md","out":r"Spanish\La_Esposa_Silenciosa_interior.pdf",
       "title":"LA ESPOSA SILENCIOSA","sub":"La serie de Elena Vance &middot; Libro 1","novel":"una novela",
       "header":"La esposa silenciosa","chapmark":"# Capítulo ","chprefix":"Capítulo "},
 "fr":{"src":r"French\manuscript.md","out":r"French\L_Epouse_Silencieuse_interior.pdf",
       "title":"L&rsquo;ÉPOUSE SILENCIEUSE","sub":"Série Elena Vance &middot; Livre 1","novel":"un roman",
       "header":u"L’épouse silencieuse","chapmark":"# Chapitre ","chprefix":"Chapitre "},
}
BASE = r"D:\Kapil\Books\Elena Vance Series\1. The Quiet Wife"

def build(code):
    L=LANG[code]; numw=NUMW[code]
    global HEADER_TITLE; HEADER_TITLE=L["header"]
    with open(BASE+"\\"+L["src"],encoding="utf-8") as fh: raw=fh.read().split("\n")
    story=[Spacer(1,2.3*inch),Paragraph(L["title"],TMAIN),Spacer(1,0.18*inch),
           Paragraph(L["sub"],TSUB),Spacer(1,2.6*inch),Paragraph(L["novel"],TSUB)]
    new_section=True; para=[]; quote=[]; n=len(raw)
    def flush_para():
        nonlocal para,new_section
        if para: story.append(Paragraph(inline(" ".join(para)),BODYF if new_section else BODY)); new_section=False
        para=[]
    def flush_quote():
        nonlocal quote,new_section
        if quote: story.extend(message_card(quote)); new_section=True
        quote=[]
    i=0
    while i<n and not raw[i].startswith(L["chapmark"]): i+=1
    while i<n:
        line=raw[i]
        if line.strip().startswith("```"):
            flush_para(); flush_quote(); i+=1; buf=[]
            while i<n and not raw[i].strip().startswith("```"): buf.append(raw[i]); i+=1
            i+=1; story.extend(tool_card(buf)); new_section=True; continue
        if line.startswith(L["chapmark"]):
            flush_para(); flush_quote()
            m=re.match(re.escape(L["chapmark"])+r"(\d+)",line); num=int(m.group(1)) if m else 0
            j=i+1
            while j<n and not raw[j].startswith("## "):
                if raw[j].strip()=="": j+=1; continue
                break
            if j<n and raw[j].startswith("## "): title=raw[j][3:].strip()
            else: title=""; j=i
            story.append(NextPageTemplate("chapter")); story.append(PageBreak())
            story.append(SetChapter(title)); story.append(Spacer(1,1.25*inch))
            if num<len(numw): story.append(Paragraph(L["chprefix"]+numw[num],CNUM))
            story.append(Paragraph(inline(title),CTITLE)); story.append(Spacer(1,0.34*inch))
            story.append(NextPageTemplate("normal")); new_section=True; i=j+1; continue
        if line.startswith("## "): flush_para(); flush_quote(); i+=1; continue
        if line.strip()=="---":
            flush_para(); flush_quote(); k=i+1
            while k<n and raw[k].strip()=="": k+=1
            if k<n and raw[k].startswith(L["chapmark"]): i+=1; continue
            story.append(Paragraph("&lowast; &nbsp; &lowast; &nbsp; &lowast;",SCENE)); new_section=True; i+=1; continue
        if line.startswith(">"): flush_para(); quote.append(line[1:].lstrip()); i+=1; continue
        if line.strip()=="":
            flush_para()
            if quote: flush_quote()
            i+=1; continue
        if quote: flush_quote()
        para.append(line.strip()); i+=1
    flush_para(); flush_quote()
    frame=Frame(LM,BM,TEXTW,PH-TM-BM,id="main",leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    out=BASE+"\\"+L["out"]
    doc=BaseDocTemplate(out,pagesize=(PW,PH),leftMargin=LM,rightMargin=RM,topMargin=TM,bottomMargin=BM,
        title=L["header"],author="Elena Vance Series")
    doc.addPageTemplates([PageTemplate(id="title",frames=[frame],onPage=blank_page),
        PageTemplate(id="normal",frames=[frame],onPage=normal_page),
        PageTemplate(id="chapter",frames=[frame],onPage=chapter_page)])
    doc.build(story); print("PDF written:",out)

for code in ("de","es","fr"): build(code)

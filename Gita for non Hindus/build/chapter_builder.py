"""Reusable chapter builder — call build_chapter(data) → returns HTML string."""
import fitz, subprocess, os

ACCENTS = {
 'saffron': dict(accent='#C77A1A', tint='#FBF1E0', tint2='#F0DEB8'),
 'sage':    dict(accent='#3E9C73', tint='#EAF5EF', tint2='#CFE6DA'),
 'slate':   dict(accent='#335A8C', tint='#E9EFF7', tint2='#D2DDEC'),
 'plum':    dict(accent='#8C3A55', tint='#F3E7EB', tint2='#E2CFD7'),
 'gold':    dict(accent='#A9791A', tint='#FBF1DD', tint2='#EFE0B6'),
}

CSS_TEMPLATE = r"""
@page {{ size: 8in 10in; margin: 0.78in 0.8in 0.82in 0.82in; }}
*{{ box-sizing:border-box; }}
:root{{
  --accent:{accent}; --accent-tint:{tint}; --accent-tint2:{tint2};
  --ink:#1c1b2b; --paper:#FAF6EC;
  --plum:#8C3A55; --plum-tint:#F3E7EB; --slate:#335A8C; --slate-tint:#E9EFF7;
  --warn:#A84E29; --warn-tint:#FBEEE3; --rule:#DBCBA6; --muted:#5b5040;
}}
html,body{{ margin:0; padding:0; background:var(--paper); color:var(--ink); }}
body{{ font-family:'Noto Serif',Georgia,serif; font-size:10.5pt; line-height:1.48; }}
p{{ margin:0 0 8pt 0; text-align:justify; text-indent:13pt; hyphens:auto; }}
p.lead,p.noind,.box p,.verse+p,li p,.cv p{{ text-indent:0; }}
p.lead{{ font-size:12pt; line-height:1.52; margin-bottom:10pt; }}
em{{ color:#4a3f6b; }} b,strong{{ font-weight:700; }}
.sec{{ display:flex; align-items:center; gap:10pt; border-bottom:1.4pt solid var(--accent); padding-bottom:6pt; margin:20pt 0 11pt 0; break-after:avoid; }}
.sec .secn{{ font-family:'Inter',sans-serif; font-size:11pt; font-weight:700; color:#fff; background:var(--accent); border-radius:50%; width:18pt; height:18pt; display:inline-flex; align-items:center; justify-content:center; flex:0 0 18pt; line-height:1; }}
.sec .sect{{ font-size:15.5pt; font-weight:700; }}
h2.sec2{{ font-size:16pt; font-weight:700; margin:2pt 0 9pt 0; }}
.grp{{ font-family:'Inter',sans-serif; font-size:7.5pt; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:#9a8a5e; text-align:center; margin:16pt 0 8pt 0; display:flex; align-items:center; gap:8pt; break-after:avoid; }}
.grp::before,.grp::after{{ content:""; flex:1; border-top:.6pt solid var(--rule); }}
.vunit{{ background:#F7F0E0; border:0.7pt solid #E4D4AC; border-radius:5pt; padding:9pt 14pt 7pt; margin:8pt 0 10pt 0; }}
.vh{{ display:flex; align-items:center; gap:8pt; margin:0 0 6pt 0; break-after:avoid; }}
.vh .badge{{ font-family:'Inter',sans-serif; font-size:9pt; font-weight:700; color:#fff; background:var(--accent); padding:2pt 9pt; border-radius:9pt; }}
.vh .vht{{ font-family:'Inter',sans-serif; font-size:8pt; font-weight:700; letter-spacing:.14em; text-transform:uppercase; color:var(--accent); }}
.vcore{{ break-inside:avoid; }}
.vbody{{ margin:3pt 0 4pt 18pt; }} .vbody p{{ font-size:9.6pt; text-align:left; }}
.ln2{{ display:flex; align-items:center; gap:5pt; margin:8pt 0 1pt 0; break-after:avoid; }}
.labx{{ font-family:'Inter',sans-serif; font-size:7pt; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:var(--muted); }}
.verse{{ background:var(--accent-tint); border-radius:3pt; padding:11pt 16pt 9pt; margin:4pt 0 9pt; break-inside:avoid; }}
.verse .dev{{ font-family:'Noto Serif Devanagari',serif; font-size:14.5pt; line-height:1.75; text-align:center; font-weight:600; color:#241f2e; margin:0 0 4pt; }}
.verse .iast{{ font-family:'Noto Serif',serif; font-style:italic; font-size:9.5pt; text-align:center; color:#6a5526; margin:0 0 5pt; line-height:1.4; }}
.verse .vno{{ font-family:'Inter',sans-serif; font-size:7pt; font-weight:700; letter-spacing:.14em; text-align:center; color:var(--accent); }}
.tl{{ display:inline-flex; align-items:center; justify-content:center; width:11pt; height:11pt; border-radius:50%; font-family:'Inter',sans-serif; font-size:6.5pt; font-weight:700; color:#fff; flex:0 0 11pt; line-height:1; }}
.tl.p{{ background:#9a8a5e; }} .tl.l{{ background:var(--slate); }} .tl.m{{ background:var(--accent); }} .tl.c{{ background:var(--plum); }}
.cv{{ display:flex; gap:9pt; margin:5pt 0; padding:6pt 0; border-bottom:.4pt dotted var(--rule); break-inside:avoid; }}
.cv .cvn{{ font-family:'Inter',sans-serif; font-size:8pt; font-weight:700; color:var(--accent); flex:0 0 26pt; }}
.cv .cvt{{ flex:1; }}
.cv .devc{{ font-family:'Noto Serif Devanagari',serif; font-size:11pt; line-height:1.55; color:#2a2433; margin-bottom:3pt; }}
.cv .ln{{ display:flex; align-items:baseline; gap:5pt; margin:1.5pt 0; }}
.cv .tx{{ flex:1; }}
.cv .iastc{{ font-family:'Noto Serif',serif; font-style:italic; font-size:8pt; color:#6a5526; }}
.cv .litc{{ font-size:8.6pt; color:#3a3340; line-height:1.32; }}
.cv .meanc{{ font-size:8.6pt; color:#5a4a2a; line-height:1.32; font-style:italic; }}
.box{{ border-radius:3pt; padding:9pt 12pt; margin:8pt 0; break-inside:avoid; }}
.box p{{ font-size:9.6pt; line-height:1.4; text-align:left; }}
.box .h{{ font-family:'Inter',sans-serif; font-size:7pt; font-weight:700; letter-spacing:.16em; text-transform:uppercase; margin-bottom:3pt; }}
.box .h::before{{ content:""; display:inline-block; width:5pt; height:5pt; margin-right:6pt; vertical-align:1pt; }}
.bridge{{ background:#FFF6E4; }} .bridge .h{{ color:#A9791A; }} .bridge .h::before{{ background:#A9791A; }}
.sadhana{{ background:var(--plum-tint); }} .sadhana .h{{ color:var(--plum); }} .sadhana .h::before{{ background:var(--plum); }}
.adept{{ background:var(--slate-tint); }} .adept .h{{ color:var(--slate); }} .adept .h::before{{ background:var(--slate); }}
.warn{{ background:var(--warn-tint); }} .warn .h{{ color:var(--warn); }} .warn .h::before{{ background:var(--warn); }}
.bigpic li{{ margin-bottom:9pt; line-height:1.44; }} .bigpic li b.lead-saff{{ color:var(--accent); }}
.takeaway{{ background:var(--accent-tint); border:1.4pt solid var(--accent); border-radius:4pt; padding:13pt 17pt; margin-top:5pt; break-inside:avoid; }}
.takeaway ol{{ margin:6pt 0 0; padding-left:17pt; }} .takeaway li{{ margin-bottom:6pt; }} .takeaway .close{{ font-style:italic; margin-top:6pt; }}
.path-note{{ font-family:'Inter',sans-serif; font-size:8pt; color:#7a6b48; font-style:italic; margin-top:12pt; border-top:.6pt solid var(--rule); padding-top:6pt; }}
.xref{{ font-family:'Inter',sans-serif; font-size:7pt; color:#8a7a52; margin:6pt 0 2pt; letter-spacing:.04em; }}
.compare{{ background:#F0EFEC; border:0.7pt solid #D0CDC4; }} .compare .h{{ color:#5a5a5a; }} .compare .h::before{{ background:#8a8a8a; }}
.compare p{{ font-size:8.6pt; line-height:1.4; margin-bottom:3pt; }}
.progress{{ display:flex; gap:3pt; justify-content:center; margin:0 0 14pt; }}
.progress .dot{{ width:6pt; height:6pt; border-radius:50%; background:#D8C9A8; }}
.progress .done{{ background:var(--accent); opacity:.4; }}
.progress .here{{ background:var(--accent); }}
.lifeapp{{ background:#F4ECDB; border:0.7pt solid #E0CFA4; border-radius:4pt; padding:10pt 13pt; margin:8pt 0; break-inside:avoid; }}
.lifeapp .lh{{ font-family:'Inter',sans-serif; font-size:7.5pt; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:#8a7a4e; margin-bottom:5pt; }}
.lifeapp p{{ font-size:9.2pt; line-height:1.4; text-align:left; margin-bottom:4pt; }}
.vocab{{ background:#EAF0F7; border:0.7pt solid #D2DDEC; border-radius:4pt; padding:10pt 13pt; margin:8pt 0; break-inside:avoid; }}
.vocab .vh2{{ font-family:'Inter',sans-serif; font-size:7.5pt; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:var(--slate); margin-bottom:5pt; }}
.vocab p{{ font-size:8.6pt; line-height:1.4; margin-bottom:3pt; }}
"""

def tag(l,c): return f'<span class="tl {c}">{l}</span>'
def box(cls,h,b): return f'<div class="box {cls}"><div class="h">{h}</div><p>{b}</p></div>'
def section(n,t): return f'<div class="sec"><span class="secn">{n}</span><span class="sect">{t}</span></div>'
def groupdiv(l): return f'<div class="grp">{l}</div>'

def verse_panel(n,d,i):
    return f'<div class="verse"><div class="dev">{d}</div><div class="iast">{i}</div><div class="vno">GĪTĀ {n}</div></div>'

def compact(n,d,i,g,m):
    return (f'<div class="cv"><div class="cvn">{n}</div><div class="cvt">'
            f'<div class="devc">{d}</div>'
            f'<div class="ln">{tag("P","p")}<span class="tx iastc">{i}</span></div>'
            f'<div class="ln">{tag("L","l")}<span class="tx litc">{g}</span></div>'
            f'<div class="ln">{tag("M","m")}<span class="tx meanc">{m}</span></div>'
            f'</div></div>')

def deep(n,dd):
    out=['<div class="vunit">']
    out.append(f'<div class="vh"><span class="badge">{n}</span><span class="vht">{dd["title"]}</span></div>')
    d=dd['_dev']; i=dd['_iast']
    out.append(f'<div class="vcore">{verse_panel(n,d,i)}</div>')
    out.append('<div class="vbody">')
    for key,label,cls in [('literal','Literal','l'),('plain','In plain English','m'),('commentary','Commentary','c')]:
        if key in dd:
            out.append(f'<div class="ln2">{tag(label[0],cls)}<span class="labx">{label}</span></div><p>{dd[key]}</p>')
    # cross-references (inline, small)
    if 'xrefs' in dd:
        out.append(f'<div class="xref">↗ cf. {dd["xrefs"]}</div>')
    out.append('</div></div>')  # close vbody + vunit
    if 'bridge' in dd: out.append(box('bridge','For the new reader',dd['bridge']))
    if 'sadhana' in dd: out.append(box('sadhana','Try this — '+dd.get('sadhana_h','a practice'),dd['sadhana']))
    if 'adept' in dd: out.append(box('adept','Going deeper'+(' — '+dd['adept_h'] if 'adept_h' in dd else ''),dd['adept']))
    if 'warn' in dd: out.append(box('warn','A common misreading'+(' — '+dd['warn_h'] if 'warn_h' in dd else ''),dd['warn']))
    # translation comparison box
    if 'compare' in dd:
        c=dd['compare']
        body='<p>'.join(f'<b>{t[0]}:</b> <i>{t[1]}</i>' for t in c)+'</p>'
        out.append(box('compare','Translations compared',body))
    return '\n'.join(out)

def build_chapter(data):
    A=ACCENTS[data['accent']]
    css=CSS_TEMPLATE.format(**A)
    body=[]
    body.append(section('1','Intro Card'))
    for p in data['intro']: body.append(p)
    body.append(section('2','The Big Picture'))
    body.append('<p class="noind">'+data['bigpic_intro']+'</p>')
    body.append('<ol class="bigpic">'+''.join(f'<li>{x}</li>' for x in data['bigpic'])+'</ol>')
    body.append(section('3','The Verses'))
    body.append(f'<p class="noind" style="color:var(--muted);font-size:9.5pt;font-style:italic;margin-bottom:8pt">{data["verses_intro"]}</p>')
    # progress indicator
    gita_n = data.get('gita_ch', 12)
    dots = ''.join(f'<span class="dot {"here" if i+1==gita_n else ("done" if i+1<gita_n else "")}"></span>' for i in range(18))
    body.append(f'<div class="progress">{dots}</div>')
    V=data['verses']; DEEP=data['deep']; DIV=data.get('dividers',[])
    div_map={d[0]:d[1] for d in DIV}
    for v in V:
        n=v[0]
        if n in div_map: body.append(groupdiv(div_map[n]))
        if n in DEEP:
            dd=DEEP[n]; dd['_dev']=v[1]; dd['_iast']=v[2]
            body.append(deep(n,dd))
        else:
            body.append(compact(n,v[1],v[2],v[3],v[4]))
    body.append(section('4','Takeaway'))
    # life application (if present)
    if 'life_app' in data:
        body.append('<div class="lifeapp"><div class="lh">In Your Life</div>')
        for p in data['life_app']: body.append(f'<p>{p}</p>')
        body.append('</div>')
    body.append(f'<h2 class="sec2">{data["takeaway_title"]}</h2>')
    body.append(f'<div class="takeaway"><ol>{"".join(f"<li>{x}</li>" for x in data["takeaway"])}</ol>'
                f'<p class="close">{data["takeaway_close"]}</p></div>')
    body.append(section('5',f'The 18-Step Sādhana Path — where you are'))
    body.append(data['sadhana_text'])
    # Sanskrit vocabulary (if present)
    if 'sanskrit_vocab' in data:
        body.append('<div class="vocab"><div class="vh2">Sanskrit You Have Learned</div>')
        for p in data['sanskrit_vocab']: body.append(f'<p>{p}</p>')
        body.append('</div>')
    body.append('<div class="path-note">Reader\'s path: Wayfarer · Student · Seeker · Adept — read at whichever depth draws you.</div>')
    html=("<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>"
          f"<title>{data['title']}</title><style>{css}</style></head><body>"
          +'\n'.join(body)+'</body></html>')
    return html

def build_pdf(html_path, pdf_path, out_path, chapter_label):
    """Build a chapter PDF: content + divider + diagram (or just content + divider)."""
    CHROME=r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    BUILD=r'D:\Kapil\Books\Gita for non Hindus\build'
    def render(h,p):
        subprocess.run([CHROME,'--headless','--disable-gpu','--no-pdf-header-footer',
                        '--print-to-pdf='+p,'file:///'+h.replace('\\','/')],
                       stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=180)
    # render content
    content_pdf=BUILD+r'\_tmp_content.pdf'
    render(html_path, content_pdf)
    content=fitz.open(content_pdf)
    # render divider
    divider_html=BUILD+r'\divider.html'
    divider_pdf=BUILD+r'\_tmp_divider.pdf'
    # write a chapter-specific divider
    div_html=f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@page{{size:8in 10in;margin:0}} *{{box-sizing:border-box}} body{{margin:0}}
.b{{background:{ACCENTS[data_accent]['accent']};color:#FFF7EA;height:10in;width:8in;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;font-family:'Noto Serif',serif}}
.k{{font-family:'Inter',sans-serif;font-size:8.5pt;letter-spacing:.3em;text-transform:uppercase;opacity:.88;margin-bottom:40pt}}
.d{{font-family:'Noto Serif Devanagari',serif;font-size:30pt;font-weight:600;line-height:1.3;margin:0 0 22pt}}
.n{{font-family:'Inter',sans-serif;font-size:12pt;letter-spacing:.2em;text-transform:uppercase;margin-bottom:4pt;opacity:.92}}
.t{{font-style:italic;font-size:27pt;font-weight:600;line-height:1.18;margin:0 0 20pt}}
.s{{font-size:12.5pt;font-style:italic;opacity:.94;max-width:4.6in;line-height:1.5;margin-bottom:38pt;padding:0 .5in}}
.f{{margin-top:42pt;font-family:'Inter',sans-serif;font-size:7.5pt;letter-spacing:.2em;opacity:.82}}
</style></head><body><div class="b">
<div class="k">The Song of the Divine · Part II</div>
<div class="d">{data_dev}</div>
<div class="n">{data_label}</div>
<div class="t">{data_title}</div>
<div class="s">{data_sub}</div>
<div class="f">{data_verses} VERSES · PATH: {data_path}</div>
</div></body></html>"""
    # NOTE: the divider needs chapter-specific data — handle in caller
    return content  # caller handles divider + composite

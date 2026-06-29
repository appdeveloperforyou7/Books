"""Build Chapter 12 PDF: render + composite cream + folios."""
import subprocess, fitz, os
BUILD = r'D:\Kapil\Books\Gita for non Hindus\build'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

def render(html, pdf):
    subprocess.run([CHROME,'--headless','--disable-gpu','--no-pdf-header-footer',
                    '--print-to-pdf='+pdf,'file:///'+html.replace('\\','/')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)

# 1. Render Ch12 content
render(BUILD+r'\content_ch12.html', BUILD+r'\_ch12_content.pdf')

# 2. Write a Ch12 divider (saffron, bhakti)
div_html = """<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@page{size:8in 10in;margin:0} *{box-sizing:border-box} body{margin:0}
.b{background:#C77A1A;color:#FFF7EA;height:10in;width:8in;display:flex;flex-direction:column;
justify-content:center;align-items:center;text-align:center;font-family:'Noto Serif',serif}
.k{font-family:'Inter',sans-serif;font-size:8.5pt;letter-spacing:.3em;text-transform:uppercase;opacity:.88;margin-bottom:44pt}
.d{font-family:'Noto Serif Devanagari',serif;font-size:30pt;font-weight:600;line-height:1.3;margin:0 0 24pt}
.n{font-family:'Inter',sans-serif;font-size:12pt;letter-spacing:.2em;text-transform:uppercase;margin-bottom:4pt;opacity:.92}
.t{font-style:italic;font-size:27pt;font-weight:600;line-height:1.18;margin:0 0 22pt}
.s{font-size:12.5pt;font-style:italic;opacity:.94;max-width:4.6in;line-height:1.5;margin-bottom:38pt;padding:0 .5in}
.f{margin-top:46pt;font-family:'Inter',sans-serif;font-size:7.5pt;letter-spacing:.2em;opacity:.82}
</style></head><body><div class="b">
<div class="k">The Song of the Divine · Part II</div>
<div class="d">भक्तियोगः</div>
<div class="n">Chapter 17 · Gītā 12</div>
<div class="t">The Yoga of Devotion</div>
<div class="s">The shortest chapter — and the one that says the most about what God asks of us: not scholarship, not austerity, but love.</div>
<div class="f">20 VERSES · PATH: BHAKTI</div>
</div></body></html>"""
open(BUILD+r'\_ch12_div.html','w',encoding='utf-8').write(div_html)
render(BUILD+r'\_ch12_div.html', BUILD+r'\_ch12_div.pdf')

# 3. Composite cream + folios
W,H=576,720
CREAM=(0xFA/255,0xF6/255,0xEC/255)
F_helv=fitz.Font(fontname='helv'); F_heit=fitz.Font(fontname='heit')
LEFT='The Bhagavad Gītā Made Clear'; RIGHT='GĪTĀ 12  ·  THE YOGA OF DEVOTION'
def stamp(page, folio):
    tw=fitz.TextWriter(page.rect); tw.append((59,40),LEFT,font=F_heit,fontsize=9); tw.write_text(page)
    widths=[(c,F_helv.text_length(c,fontsize=7.5)) for c in RIGHT]
    total=sum(w for _,w in widths)+0.6*(len(widths)-1)
    tw=fitz.TextWriter(page.rect); px=576-58-total
    for c,w in widths: tw.append((px,40),c,font=F_helv,fontsize=7.5); px+=w+0.6
    tw.write_text(page)
    f=str(folio); fw=F_helv.text_length(f,fontsize=9)
    tw=fitz.TextWriter(page.rect); tw.append(((W-fw)/2,H-34),f,font=F_helv,fontsize=9); tw.write_text(page)

content=fitz.open(BUILD+r'\_ch12_content.pdf')
divider=fitz.open(BUILD+r'\_ch12_div.pdf')
out=fitz.open()
out.insert_pdf(divider)
for i in range(content.page_count):
    np=out.new_page(width=W,height=H)
    np.draw_rect(np.rect,color=CREAM,fill=CREAM)
    np.show_pdf_page(np.rect,content,i)
    stamp(np,i+2)
OUT=BUILD+r'\chapter12_FINAL.pdf'
out.save(OUT,garbage=4,deflate=True)
print('saved',OUT,'| pages',out.page_count)

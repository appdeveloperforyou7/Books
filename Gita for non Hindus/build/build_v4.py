import subprocess, fitz, os
BUILD = r'D:\Kapil\Books\Gita for non Hindus\build'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
def render(html, pdf):
    subprocess.run([CHROME,'--headless','--disable-gpu','--no-pdf-header-footer',
                    '--print-to-pdf='+pdf,'file:///'+html.replace('\\','/')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    assert os.path.exists(pdf), pdf
render(BUILD+r'\content_v4.html', BUILD+r'\content.pdf')
render(BUILD+r'\divider.html', BUILD+r'\divider.pdf')
render(BUILD+r'\diagram.html',   BUILD+r'\diagram.pdf')
content=fitz.open(BUILD+r'\content.pdf'); print('content pages:', content.page_count)
W,H=576,720
CREAM=(0xFA/255,0xF6/255,0xEC/255)
F_helv=fitz.Font(fontname='helv'); F_heit=fitz.Font(fontname='heit')
LEFT='The Bhagavad Gītā'; RIGHT='CHAPTER 16  ·  THE ROYAL SECRET'
def stamp(page, folio):
    tw=fitz.TextWriter(page.rect); tw.append((59,40),LEFT,font=F_heit,fontsize=9); tw.write_text(page)
    widths=[(c,F_helv.text_length(c,fontsize=7.5)) for c in RIGHT]
    total=sum(w for _,w in widths)+0.6*(len(widths)-1)
    tw=fitz.TextWriter(page.rect); px=576-58-total
    for c,w in widths: tw.append((px,40),c,font=F_helv,fontsize=7.5); px+=w+0.6
    tw.write_text(page)
    f=str(folio); fw=F_helv.text_length(f,fontsize=9)
    tw=fitz.TextWriter(page.rect); tw.append(((W-fw)/2,H-34),f,font=F_helv,fontsize=9); tw.write_text(page)
out=fitz.open()
out.insert_pdf(fitz.open(BUILD+r'\divider.pdf'))
for i in range(content.page_count):
    np=out.new_page(width=W,height=H)
    np.draw_rect(np.rect,color=CREAM,fill=CREAM)
    np.show_pdf_page(np.rect,content,i)
    stamp(np,i+2)
out.insert_pdf(fitz.open(BUILD+r'\diagram.pdf'))
OUT=BUILD+r'\chapter9_FINAL_v5.pdf'
out.save(OUT,garbage=4,deflate=True)
print('saved',OUT,'pages',out.page_count)

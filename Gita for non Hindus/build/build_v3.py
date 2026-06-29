import subprocess, fitz, os

BUILD = r'D:\Kapil\Books\Gita for non Hindus\build'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
def render(html, pdf):
    subprocess.run([CHROME,'--headless','--disable-gpu','--no-pdf-header-footer',
                    '--print-to-pdf='+pdf,'file:///'+html.replace('\\','/')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    assert os.path.exists(pdf), pdf

render(os.path.join(BUILD,'content_v3.html'), os.path.join(BUILD,'content.pdf'))
render(os.path.join(BUILD,'divider.html'),   os.path.join(BUILD,'divider.pdf'))
render(os.path.join(BUILD,'diagram.html'),   os.path.join(BUILD,'diagram.pdf'))

content = fitz.open(os.path.join(BUILD,'content.pdf'))
divider = fitz.open(os.path.join(BUILD,'divider.pdf'))
diagram = fitz.open(os.path.join(BUILD,'diagram.pdf'))
print('content pages:', content.page_count)

W,H = 576,720
CREAM = (0xFA/255,0xF6/255,0xEC/255)
TAN   = (0x7a/255,0x6b/255,0x48/255)
F_helv = fitz.Font(fontname='helv')
F_heit = fitz.Font(fontname='heit')
LEFT_HDR='The Bhagavad Gītā'
RIGHT_HDR='CHAPTER 16  ·  THE ROYAL SECRET'

def stamp_header(page, folio):
    # left italic
    tw=fitz.TextWriter(page.rect); tw.append((59,40), LEFT_HDR, font=F_heit, fontsize=9); tw.write_text(page)
    # right tracked caps
    widths=[]
    for ch in RIGHT_HDR:
        w=F_helv.text_length(ch,fontsize=7.5); widths.append((ch,w))
    total=sum(w for _,w in widths)+0.6*(len(widths)-1)
    tw=fitz.TextWriter(page.rect); px=576-58-total
    for ch,w in widths:
        tw.append((px,40),ch,font=F_helv,fontsize=7.5); px+=w+0.6
    tw.write_text(page)
    # folio center
    f=str(folio); fw=F_helv.text_length(f,fontsize=9)
    tw=fitz.TextWriter(page.rect); tw.append(((W-fw)/2, H-34), f, font=F_helv, fontsize=9); tw.write_text(page)

out = fitz.open()
# divider (page 1, no folio)
out.insert_pdf(divider)
# content pages: composite cream bg behind each, then header+folio
for i in range(content.page_count):
    np = out.new_page(width=W, height=H)
    np.draw_rect(np.rect, color=CREAM, fill=CREAM)
    np.show_pdf_page(np.rect, content, i)
    stamp_header(np, i+2)   # divider=1, content starts at 2
# diagram (last, no folio)
out.insert_pdf(diagram)

OUT=os.path.join(BUILD,'chapter9_FINAL_v3.pdf')
out.save(OUT, garbage=4, deflate=True)
print('saved', OUT, '| total pages:', out.page_count)

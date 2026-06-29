import subprocess, fitz, os
BUILD = r'D:\Kapil\Books\Gita for non Hindus\build'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
def render(html, pdf):
    subprocess.run([CHROME,'--headless','--disable-gpu','--no-pdf-header-footer',
                    '--print-to-pdf='+pdf,'file:///'+html.replace('\\','/')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    assert os.path.exists(pdf), pdf
render(BUILD+r'\titlepage.html', BUILD+r'\titlepage.pdf')
render(BUILD+r'\toc.html',        BUILD+r'\toc.pdf')
render(BUILD+r'\howtouse.html',  BUILD+r'\howtouse.pdf')
render(BUILD+r'\whatisgita.html', BUILD+r'\whatisgita.pdf')
render(BUILD+r'\glossary.html',  BUILD+r'\glossary.pdf')

out = fitz.open()
out.insert_pdf(fitz.open(BUILD+r'\titlepage.pdf'))      # title
out.insert_pdf(fitz.open(BUILD+r'\toc.pdf'))            # contents
out.insert_pdf(fitz.open(BUILD+r'\howtouse.pdf'))       # how to use
out.insert_pdf(fitz.open(BUILD+r'\whatisgita.pdf'))     # Part I, ch 2
out.insert_pdf(fitz.open(BUILD+r'\chapter9_FINAL_v5.pdf'))  # ch9
out.insert_pdf(fitz.open(BUILD+r'\glossary.pdf'))       # glossary
OUT = BUILD+r'\SAMPLE_BOOK.pdf'
out.save(OUT, garbage=4, deflate=True)
print('saved', OUT, '| pages', out.page_count)

import subprocess, fitz, os, sys

BUILD = r'D:\Kapil\Books\Gita for non Hindus\build'
HTML = os.path.join(BUILD, 'chapter9_v2.html')
RAW = os.path.join(BUILD, 'chapter9_v2_raw.pdf')
OUT = os.path.join(BUILD, 'chapter9_v2.pdf')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                '--print-to-pdf=' + RAW, 'file:///' + HTML.replace('\\', '/')],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
print('chrome raw exists:', os.path.exists(RAW))

TAN = (154/255, 138/255, 94/255)
LEFT_HDR = "The Bhagavad Gītā"
RIGHT_HDR = "CHAPTER 16  ·  THE ROYAL SECRET"

d = fitz.open(RAW)
n = d.page_count
print('pages:', n)
W, H = d[0].rect.width, d[0].rect.height
print('size pts:', W, H)

F_helv = fitz.Font(fontname="helv")
F_heit = fitz.Font(fontname="heit")

def place(page, text, x, y, font, fontsize, align='left', tracking=0):
    tw = fitz.TextWriter(page.rect)
    widths = []
    cx = 0.0
    for ch in text:
        w = font.text_length(ch, fontsize=fontsize)
        widths.append((ch, w))
        cx += w + tracking
    if align == 'right':
        start = x - cx
    else:
        start = x
    tw = fitz.TextWriter(page.rect)
    px = start
    for ch, w in widths:
        tw.append((px, y), ch, font=font, fontsize=fontsize)
        px += w + tracking
    tw.write_text(page)

margin_x = 58  # 0.8in
top_y = 44      # 0.61in
bot_y = H - 42

for i in range(n):
    page = d[i]
    if i == 0 or i == n - 1:
        continue  # skip full-bleed divider & diagram
    # left running head (italic)
    place(page, LEFT_HDR, margin_x, top_y, F_heit, 9)
    # right running head (caps, tracked)
    place(page, RIGHT_HDR, W - margin_x, top_y, F_helv, 7.5, align='right', tracking=0.6)
    # folio
    folio = str(i + 1)
    fw = F_helv.text_length(folio, fontsize=9)
    place(page, folio, (W - fw) / 2, bot_y, F_helv, 9)

d.save(OUT, garbage=4, deflate=True)
print('saved', OUT)

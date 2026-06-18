import os
from playwright.sync_api import sync_playwright

BASE = r"D:\Kapil\Books\Endangered Animals"
PAGES = 142
TRIM_W = 6.0
TRIM_H = 9.0
BLEED = 0.125
SPINE_PER_PAGE = 0.002347
HINGE = 0.5   # case laminate hinge gap
DPI = 300

spine = PAGES * SPINE_PER_PAGE
cover_w = BLEED + TRIM_W + HINGE + spine + HINGE + TRIM_W + BLEED
cover_h = BLEED + TRIM_H + BLEED

px_w = int(cover_w * DPI)
px_h = int(cover_h * DPI)
spine_px = int(spine * DPI)
bleed_px = int(BLEED * DPI)
hinge_px = int(HINGE * DPI)
trim_w_px = int(TRIM_W * DPI)
trim_h_px = int(TRIM_H * DPI)

print(f"Pages: {PAGES}")
print(f"Spine: {spine:.3f}\" ({spine_px}px)")
print(f"Hinge: {HINGE}\" each side ({hinge_px}px)")
print(f"Cover: {cover_w:.3f}\" x {cover_h:.3f}\" ({px_w}x{px_h}px)")

html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{px_w}px;height:{px_h}px;font-family:'Montserrat',sans-serif;overflow:hidden;background:#0a0a0a;}}
.cover-wrap{{display:flex;width:{px_w}px;height:{px_h}px;}}

.back-cover{{width:{bleed_px + hinge_px + trim_w_px}px;height:{px_h}px;position:relative;overflow:hidden;flex-shrink:0;}}
.back-bg{{position:absolute;inset:0;background-image:url('file:///{BASE.replace(chr(92),"/")}/images/forest_cover_bg.png');background-size:cover;background-position:center;}}
.back-overlay{{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(0,0,0,0.85) 0%,rgba(0,0,0,0.75) 50%,rgba(0,0,0,0.9) 100%);z-index:1;}}
.back-content{{position:relative;z-index:2;padding:{bleed_px+80}px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;height:100%;}}
.back-icon{{font-size:2.2rem;margin-bottom:18px;}}
.back-quote{{font-family:'Playfair Display',serif;font-size:1.2rem;font-style:italic;line-height:1.5;color:#f0e6d3;margin-bottom:12px;max-width:500px;}}
.back-author{{font-size:0.7rem;letter-spacing:4px;text-transform:uppercase;color:#d4a843;margin-bottom:30px;}}
.back-divider{{width:80px;height:2px;background:#d4a843;margin:0 auto 25px;}}
.back-desc{{font-size:0.68rem;line-height:1.7;color:#ccc;max-width:450px;margin:0 auto;}}
.back-barcode{{margin-top:35px;font-size:0.65rem;color:#888;letter-spacing:2px;}}

.back-hinge{{width:{hinge_px}px;height:{px_h}px;background:#0a0a0a;flex-shrink:0;}}

.spine{{width:{spine_px}px;height:{px_h}px;background:#0a0a0a;display:flex;flex-direction:column;justify-content:center;align-items:center;flex-shrink:0;border-left:1px solid rgba(212,168,67,0.3);border-right:1px solid rgba(212,168,67,0.3);}}
.spine-title{{font-family:'Playfair Display',serif;font-size:0.65rem;letter-spacing:3px;text-transform:uppercase;color:#d4a843;writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;}}

.front-hinge{{width:{hinge_px}px;height:{px_h}px;background:#0a0a0a;flex-shrink:0;}}

.front-cover{{width:{trim_w_px + bleed_px}px;height:{px_h}px;position:relative;overflow:hidden;flex-shrink:0;}}
.front-bg{{position:absolute;inset:0;background-image:url('file:///{BASE.replace(chr(92),"/")}/images/forest_cover_bg.png');background-size:cover;background-position:center;}}
.front-overlay{{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(0,0,0,0.35) 0%,rgba(0,0,0,0.55) 50%,rgba(0,0,0,0.9) 100%);z-index:1;}}
.front-blur{{position:absolute;top:50%;left:0;right:0;height:140px;transform:translateY(-50%);z-index:2;backdrop-filter:blur(16px);background:rgba(0,0,0,0.6);border-top:1px solid rgba(212,168,67,0.35);border-bottom:1px solid rgba(212,168,67,0.35);}}
.front-content{{position:relative;z-index:3;width:100%;height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;}}
.front-sub{{font-family:'Montserrat',sans-serif;font-size:0.85rem;font-weight:500;letter-spacing:10px;text-transform:uppercase;color:rgba(255,255,255,0.85);margin-bottom:10px;}}
.front-title{{font-family:'Playfair Display',serif;font-size:4rem;font-weight:900;letter-spacing:-2px;background:linear-gradient(180deg,#f5e6a3 0%,#d4a843 35%,#b8860b 65%,#f5e6a3 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;text-transform:uppercase;filter:drop-shadow(3px 3px 15px rgba(0,0,0,0.95));margin-bottom:6px;}}
.front-div{{width:100px;height:2px;background:#d4a843;margin:0 auto 20px;}}
.front-tag{{font-family:'Montserrat',sans-serif;font-size:0.7rem;letter-spacing:6px;text-transform:uppercase;color:rgba(255,255,255,0.75);}}
</style></head><body><div class="cover-wrap">

<div class="back-cover">
<div class="back-bg"></div><div class="back-overlay"></div>
<div class="back-content">
<div class="back-icon">&#127807;</div>
<div class="back-quote">"The greatness of a nation and its moral progress can be judged by the way its animals are treated."</div>
<div class="back-author">Mahatma Gandhi</div>
<div class="back-divider"></div>
<div class="back-desc">A stunning visual tribute to the world's most endangered species. Featuring 69 remarkable animals from every corner of the globe, this premium collection raises awareness about the urgent need for wildlife conservation.</div>
<div class="back-barcode">ISBN 978-1-234567-89-0</div>
</div></div>

<div class="back-hinge"></div>
<div class="spine"><div class="spine-title">Chronicles of the Endangered</div></div>
<div class="front-hinge"></div>

<div class="front-cover">
<div class="front-bg"></div><div class="front-overlay"></div><div class="front-blur"></div>
<div class="front-content">
<div class="front-sub">Chronicles of the</div><div class="front-title">Endangered</div>
<div class="front-div"></div><div class="front-tag">A Premium Wildlife Collection</div>
</div></div>

</div></body></html>"""

cover_html = os.path.join(BASE, "kdp_hardcover_cover.html")
cover_pdf = os.path.join(BASE, "Output", "KDP_Cover_Hardcover.pdf")

with open(cover_html, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Cover HTML: {cover_html}")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": px_w, "height": px_h})
    page.goto(f"file:///{cover_html.replace(chr(92),'/')}")
    page.wait_for_timeout(3000)
    page.pdf(path=cover_pdf, width=f"{cover_w}in", height=f"{cover_h}in",
             print_background=True, margin={"top":"0","bottom":"0","left":"0","right":"0"})
    browser.close()

size_mb = os.path.getsize(cover_pdf) / 1024 / 1024
print(f"Cover PDF: {cover_pdf} ({size_mb:.1f} MB)")
print(f"Dimensions: {cover_w:.3f}\" x {cover_h:.3f}\" at {DPI} DPI")
print("DONE!")

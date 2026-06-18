import json, io, os, pathlib, base64, mimetypes
from PIL import Image
from playwright.sync_api import sync_playwright

# === HARDCOVER 6x9 ALL-SPREAD GEOMETRY ===
PAGE_W = 6.25   # trim 6" + 0.125" bleed both sides
PAGE_H = 9.25   # trim 9" + 0.125" bleed top/bottom
VP_W  = 625     # viewport ~100 CSS px per inch
VP_H  = 925
SCALE = 4       # device scale factor

ROOT    = pathlib.Path(__file__).parent.resolve()
TEMPLATES = ROOT / "templates"
IMAGES   = ROOT / "images"
OUTPUT   = ROOT / "Output"

def read(p): return open(p, "r", encoding="utf-8").read()
def data_url(p):
    p = pathlib.Path(p).absolute()
    if not p.exists(): return "none"
    mime = mimetypes.guess_type(str(p))[0] or "image/png"
    with open(p, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

def iucn_class(status):
    s = status.lower()
    if "critically" in s: return ""
    if "endangered" in s: return " iucn-endangered"
    if "vulnerable" in s: return " iucn-vulnerable"
    return ""

# === EMBEDDED CSS TEMPLATES (6x9 specific) ===

# Sample page template (animal pages)
SAMPLE_CSS = """
.page-container {
    position: relative; width: 6.25in; height: 9.25in;
    overflow: hidden; background: #111;
}
.animal-photo {
    position: absolute; inset: 0;
    object-fit: {{IMAGE_FIT}};
    object-position: {{FOCAL_X}} {{FOCAL_Y}};
    width: 100%; height: 100%;
}
.gradient-top {
    position: absolute; top: 0; left: 0; right: 0; height: 25%;
    background: linear-gradient(to bottom, rgba(0,0,0,0.4) 0%, transparent 100%);
    z-index: 2;
}
.gradient-bottom {
    position: absolute; bottom: 0; left: 0; right: 0; height: 30%;
    background: linear-gradient(to top, rgba(0,0,0,0.25) 0%, transparent 100%);
    z-index: 2;
}
.gradient-blend {
    position: absolute; bottom: 0; left: 0; right: 0; height: 30%;
    background: linear-gradient(to right, transparent 55%, rgba(0,0,0,0.15) 100%);
    z-index: 2;
}
.info-box {
    position: absolute; z-index: 999;
    width: min(220px, 32%);
    background: linear-gradient(135deg, rgba(18,16,14,0.88) 0%, rgba(12,10,8,0.94) 100%);
    border: 1px solid rgba(212,168,67,0.18);
    border-top: 2px solid rgba(212,168,67,0.45);
    border-radius: 12px;
    padding: 14px 16px;
    color: #fff;
    box-shadow: 0 8px 32px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.03);
}
.info-box-minimal {
    background: linear-gradient(135deg, rgba(18,16,14,0.6) 0%, rgba(10,8,6,0.7) 100%);
    border: 1px solid rgba(212,168,67,0.1);
    border-top: 2px solid rgba(212,168,67,0.2);
    padding: 10px 14px;
}
.info-box-minimal .data-grid, .info-box-minimal .divider, .info-box-minimal .iucn-badge { display: none; }
.info-box-minimal .animal-name { font-size: 1.05rem; margin-bottom: 0; }
.animal-name {
    font-family: 'Playfair Display', serif; font-size: 1.25rem; font-weight: 700;
    color: #f0e6d3; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 14px;
}
.iucn-badge {
    display: inline-block; font-family: 'Montserrat', sans-serif;
    font-size: 0.5rem; font-weight: 600; letter-spacing: 2px;
    text-transform: uppercase; color: #ff6b6b;
    background: rgba(255,107,107,0.08); border: 1px solid rgba(255,107,107,0.3);
    border-radius: 4px; padding: 2px 6px; margin-bottom: 14px;
}
.iucn-endangered { color: #ffaa44; background: rgba(255,170,68,0.08); border-color: rgba(255,170,68,0.3); }
.iucn-vulnerable { color: #d4a843; background: rgba(212,168,67,0.08); border-color: rgba(212,168,67,0.3); }
.divider {
    height: 1px; background: linear-gradient(to right, rgba(212,168,67,0.5), rgba(212,168,67,0.05));
    margin-bottom: 14px;
}
.data-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 12px; }
.label {
    font-family: 'Montserrat', sans-serif; font-size: 0.5rem; font-weight: 500;
    text-transform: uppercase; letter-spacing: 2px; color: rgba(212,168,67,0.5);
    display: block; margin-bottom: 2px;
}
.value {
    font-family: 'Montserrat', sans-serif; font-size: 0.7rem; font-weight: 400;
    color: rgba(255,255,255,0.88); line-height: 1.3;
}
.pos-bottom-left { bottom: 5%; left: 5%; }
.pos-bottom-right { bottom: 5%; right: 5%; }
.pos-top-left { top: 5%; left: 5%; }
.pos-top-right { top: 5%; right: 5%; }
.pos-middle-left { top: 50%; left: 5%; transform: translateY(-50%); }
.pos-bottom-center { bottom: 5%; left: 50%; transform: translateX(-50%); }
"""

# TOC template
TOC_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
body,html{ margin:0; padding:0; width:6.25in; height:9.25in; background:#111; font-family:'Montserrat',sans-serif; color:#ccc; }
.toc-container{ padding:0.45in 0.55in; height:9.25in; display:flex; flex-direction:column; }
h1{ font-family:'Playfair Display',serif; font-size:2.2rem; color:#d4a843; margin-bottom:0.3in;
    border-bottom:1px solid rgba(212,168,67,0.25); padding-bottom:12px; text-align:center;
    letter-spacing:5px; text-transform:uppercase; font-weight:700; }
.toc-grid{ display:grid; grid-template-columns:1fr 1fr; column-gap:38px; row-gap:9px; flex:1; }
.toc-item{ display:flex; justify-content:space-between; align-items:baseline; font-size:0.55rem; padding:3px 0; opacity:0.9; }
.toc-name{ font-weight:400; color:#bbb; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:62%; letter-spacing:0.3px; }
.toc-dots{ flex-grow:1; border-bottom:1px dotted rgba(255,255,255,0.1); margin:0 5px; min-width:10px; position:relative; top:-2px; }
.toc-page{ font-weight:600; color:#d4a843; min-width:14px; text-align:right; font-size:0.55rem; }
</style></head><body><div class="toc-container page-container">
<h1>Contents</h1><div class="toc-grid">{{TOC_ITEMS}}</div></div></body></html>"""

# Copyright page
COPYRIGHT_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet">
<style>
body,html{ margin:0; padding:0; width:6.25in; height:9.25in; background:#1a1a1a; font-family:'Montserrat',sans-serif; color:#888; }
.copyright-wrap{ display:flex; align-items:center; justify-content:center; height:100%; padding:0.7in; }
.copyright-content{ text-align:center; max-width:400px; }
.copyright-divider{ width:2px; height:60px; background: linear-gradient(to bottom, transparent, rgba(212,168,67,0.3), transparent); margin: 20px auto; }
.copyright-text{ font-size:0.65rem; line-height:2; margin-bottom:8px; }
</style></head><body><div class="copyright-wrap page-container"><div class="copyright-content">
<div class="copyright-divider"></div>
<p class="copyright-text">Copyright 2026. All rights reserved.</p>
<p class="copyright-text">No part of this book may be reproduced in any form without written permission.</p>
<p class="copyright-text">ISBN 978-1-234567-89-0</p>
<p class="copyright-text">Printed by Kindle Direct Publishing</p>
<p class="copyright-text">Images licensed under Creative Commons or public domain.</p>
</div></div></body></html>"""

# Divider page
DIVIDER_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
.divider-page{ width:6.25in; height:9.25in; background:#080808; position:relative; display:flex; align-items:center; justify-content:center; text-align:center; overflow:hidden; }
.divider-bg{ position:absolute; inset:0; opacity:0.04; background-image: radial-gradient(circle at 20% 20%, #d4a843 0.5px, transparent 0.5px), radial-gradient(circle at 80% 80%, #d4a843 0.5px, transparent 0.5px); background-size:80px 80px; z-index:0; }
.divider-vignette{ position:absolute; inset:0; background:radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,0.55) 100%); z-index:1; }
.divider-corner{ position:absolute; width:32px; height:32px; border-color:rgba(212,168,67,0.18); border-style:double; z-index:2; }
.divider-corner-tl{ top:30px; left:30px; border-width:1.5px 0 0 1.5px; }
.divider-corner-tr{ top:30px; right:30px; border-width:1.5px 1.5px 0 0; }
.divider-corner-bl{ bottom:30px; left:30px; border-width:0 0 1.5px 1.5px; }
.divider-corner-br{ bottom:30px; right:30px; border-width:0 1.5px 1.5px 0; }
.divider-content{ position:relative; z-index:3; padding:1in 1.2in; display:flex; flex-direction:column; align-items:center; justify-content:center; transform:translateY(-3%); }
.quote-mark{ font-family:'Playfair Display',serif; font-size:4rem; color:rgba(212,168,67,0.3); line-height:1; margin-bottom:-18px; }
.quote-text{ font-family:'Playfair Display',serif; font-size:1.4rem; line-height:1.5; color:#ddd5c8; font-style:italic; font-weight:400; max-width:82%; margin-bottom:28px; letter-spacing:0.3px; }
.divider-line{ width:100px; height:1px; background:linear-gradient(90deg, transparent, rgba(212,168,67,0.5), transparent); margin-bottom:24px; }
.quote-author{ font-family:'Montserrat',sans-serif; font-size:0.68rem; text-transform:uppercase; letter-spacing:6px; color:rgba(212,168,67,0.75); font-weight:400; }
</style></head><body><div class="divider-page page-container">
<div class="divider-bg"></div><div class="divider-vignette"></div>
<div class="divider-corner divider-corner-tl"></div><div class="divider-corner divider-corner-tr"></div>
<div class="divider-corner divider-corner-bl"></div><div class="divider-corner divider-corner-br"></div>
<div class="divider-content">
<div class="quote-mark">&ldquo;</div>
<div class="quote-text">{{QUOTE_TEXT}}</div>
<div class="divider-line"></div>
<div class="quote-author">{{QUOTE_AUTHOR}}</div>
</div></div></body></html>"""

# Back cover
BACK_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
body,html{ margin:0; padding:0; width:6.25in; height:9.25in; background:#0a0a0a; font-family:'Montserrat',sans-serif; color:#fff; overflow:hidden; }
.back-container{ position:relative; width:100%; height:100%; }
.back-bg{ position:absolute; inset:0; background-image:url('{{BACK_BG_IMAGE}}'); background-size:cover; background-position:center; }
.back-overlay{ position:absolute; inset:0; background:linear-gradient(to bottom, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.75) 50%, rgba(0,0,0,0.9) 100%); z-index:1; }
.back-content{ position:relative; z-index:2; padding:60px 80px; max-width:80%; }
.back-icon{ font-size:2.2rem; margin-bottom:18px; }
.back-book-title{ font-family:'Playfair Display',serif; font-size:1.5rem; color:#d4a843; letter-spacing:4px; text-transform:uppercase; margin-bottom:30px; }
.back-quote{ font-family:'Playfair Display',serif; font-size:1.2rem; font-style:italic; line-height:1.5; color:#f0e6d3; margin-bottom:12px; max-width:500px; }
.back-author{ font-size:0.7rem; letter-spacing:4px; text-transform:uppercase; color:#d4a843; margin-bottom:30px; }
.back-divider{ width:80px; height:2px; background:#d4a843; margin:0 auto 25px; }
.back-desc{ font-size:0.68rem; line-height:1.7; color:#ccc; max-width:450px; margin:0 auto; }
.back-barcode{ margin-top:35px; font-size:0.65rem; color:#888; letter-spacing:2px; }
</style></head><body><div class="back-container page-container" style="background-image:url('{{BACK_BG_IMAGE}}');background-size:cover;background-position:center;">
<div class="back-overlay"></div><div class="back-content">
<div class="back-book-title">Chronicles of the Endangered</div>
<div class="back-icon">&#127807;</div>
<div class="back-quote">"The greatness of a nation and its moral progress can be judged by the way its animals are treated."</div>
<div class="back-author">Mahatma Gandhi</div>
<div class="back-divider"></div>
<div class="back-desc">A stunning visual tribute to the world's most endangered species. Featuring 69 remarkable animals from every corner of the globe, this premium collection raises awareness about the urgent need for wildlife conservation.</div>
<div class="back-barcode">ISBN 978-1-234567-89-0</div>
</div></div></body></html>"""

# === QUOTES ===
QUOTES = [
    ("\"The wildlife and its habitat cannot speak, so we must and we will.\"",
     "Theodore Roosevelt"),
    ("\"We don't own the planet Earth, we belong to it. And we must share it with our wildlife.\"",
     "Steve Irwin"),
    ("\"The question is, are we happy to suppose that our grandchildren may never be able to see an elephant except in a picture book?\"",
     "David Attenborough"),
    ("\"In the end we will conserve only what we love; we will love only what we understand; and we will understand only what we are taught.\"",
     "Baba Dioum"),
    ("\"What we are doing to the forests of the world is but a mirror reflection of what we are doing to ourselves and to one another.\"",
     "Mahatma Gandhi"),
]

# === GENERATE ===
print("Loading animals...")
with open(ROOT / "animals_data_verified.json", "r", encoding="utf-8") as f:
    animals = json.load(f)

# Build sample HTML template with inline CSS
SAMPLE_HTML = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{SAMPLE_CSS}</style></head><body><div class="page-container">
<div class="gradient-blend"></div><div class="gradient-top"></div><div class="gradient-bottom"></div>
<img class="animal-photo" src="{{IMAGE_URL}}" alt="">
<div class="info-box {{BOX_POSITION}} {{IUCN_CLASS}}">
<div class="iucn-badge">{{IUCN_STATUS}}</div>
<div class="animal-name">{{ANIMAL_NAME}}</div>
<div class="divider"></div>
<div class="data-grid">
<div><span class="label">Est. Population</span><span class="value">{{EST_POPULATION}}</span></div>
<div><span class="label">Primary Threat</span><span class="value">{{PRIMARY_THREAT}}</span></div>
<div style="grid-column: 1/-1;"><span class="label">Where to Find</span><span class="value">{{WHERE_FOUND}}</span></div>
</div></div></div></body></html>"""

# Build pages
print("Building HTML draft...")
pages = []

# Cover
bg_img = data_url(IMAGES / "forest_cover_bg.png")
cover_css = """
.cover-page{ width:6.25in; height:9.25in; position:relative; overflow:hidden; background:#0a0a0a; }
.cover-bg{ position:absolute; inset:0; background-size:cover; background-position:center; }
.cover-overlay{ position:absolute; inset:0; background:linear-gradient(to bottom, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0.55) 50%, rgba(0,0,0,0.9) 100%); z-index:1; }
.cover-blur{ position:absolute; top:50%; left:0; right:0; height:160px; transform:translateY(-50%); z-index:2; backdrop-filter:blur(16px); background:rgba(0,0,0,0.6); border-top:1px solid rgba(212,168,67,0.35); border-bottom:1px solid rgba(212,168,67,0.35); }
.cover-content{ position:relative; z-index:3; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; }
.cover-sub{ font-family:'Montserrat',sans-serif; font-size:0.85rem; font-weight:500; letter-spacing:10px; text-transform:uppercase; color:rgba(255,255,255,0.85); margin-bottom:10px; }
.cover-title{ font-family:'Playfair Display',serif; font-size:4rem; font-weight:900; letter-spacing:-2px; background:linear-gradient(180deg, #f5e6a3 0%, #d4a843 35%, #b8860b 65%, #f5e6a3 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; text-transform:uppercase; filter:drop-shadow(3px 3px 15px rgba(0,0,0,0.95)); margin-bottom:6px; }
.cover-div{ width:100px; height:2px; background:#d4a843; margin:0 auto 20px; }
.cover-tag{ font-family:'Montserrat',sans-serif; font-size:0.7rem; letter-spacing:6px; text-transform:uppercase; color:rgba(255,255,255,0.75); }
"""
cover_html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{cover_css}</style></head><body><div class="cover-page page-container">
<div class="cover-bg" style="background-image:url('{bg_img}');"></div><div class="cover-overlay"></div><div class="cover-blur"></div>
<div class="cover-content">
<div class="cover-sub">Chronicles of the</div><div class="cover-title">Endangered</div>
<div class="cover-div"></div><div class="cover-tag">A Premium Wildlife Collection</div>
</div></div></body></html>"""
pages.append(cover_html)
pages.append(COPYRIGHT_HTML)

# TOC
pg = 4
toc_entries = []
qi = 0
for a in animals:
    name = a["name"]
    toc_entries.append(
        f'<div class="toc-item"><span class="toc-name">{name}</span>'
        f'<span class="toc-dots"></span><span class="toc-page">{pg}</span></div>'
    )
    pg += 2  # Every animal is a spread = 2 pages

pages.append(TOC_HTML.replace("{{TOC_ITEMS}}", "\n".join(toc_entries)))

# Animal pages - ALL as spreads
pg = 4
for a in animals:
    img_path = ROOT / a["image_url"]
    if not img_path.exists():
        print(f"  MISSING: {a['name']} -> {a['image_url']}")
    abs_img = f"file:///{img_path.absolute().as_posix()}"
    box = a.get("BOX_POSITION", "pos-bottom-right")
    fx = a.get("focal_x", "center")
    fy = a.get("focal_y", "center")
    iucn_cls = iucn_class(a.get("iucn_status", ""))

    # Spread-L (left page): focal_x="left" (always left portion)
    left = SAMPLE_HTML
    left = left.replace("{IMAGE_URL}", abs_img)
    left = left.replace("{ANIMAL_NAME}", a["name"])
    left = left.replace("{IUCN_STATUS}", a.get("iucn_status", ""))
    left = left.replace("{IUCN_CLASS}", iucn_cls)
    left = left.replace("{EST_POPULATION}", a.get("est_population", ""))
    left = left.replace("{PRIMARY_THREAT}", a.get("primary_threat", ""))
    left = left.replace("{WHERE_FOUND}", a.get("where_found", ""))
    left = left.replace("{BOX_POSITION}", box)
    left = left.replace("{FOCAL_X}", fx)  # JSON per-animal focal
    left = left.replace("{FOCAL_Y}", fy)
    left = left.replace("{IMAGE_FIT}", a.get("image_fit", "cover"))
    left = left.replace('class="info-box', 'class="info-box info-box-minimal')

    # Spread-R (right page): elegant info card — no duplicate photo
    info = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
.spread-info{{ width:6.25in; height:9.25in; background:#080808; position:relative; display:flex; align-items:center; justify-content:center; overflow:hidden; }}
.spread-bg{{ position:absolute; inset:0; opacity:0.03; background-image:radial-gradient(circle at 20% 20%,#d4a843 0.5px,transparent 0.5px),radial-gradient(circle at 80% 80%,#d4a843 0.5px,transparent 0.5px); background-size:80px 80px; z-index:0; }}
.spread-vig{{ position:absolute; inset:0; background:radial-gradient(ellipse at center,transparent 30%,rgba(0,0,0,0.6) 100%); z-index:1; }}
.spread-corner{{ position:absolute; width:40px; height:40px; border-color:rgba(212,168,67,0.2); border-style:double; z-index:2; }}
.sc-tl{{ top:30px; left:30px; border-width:1.5px 0 0 1.5px; }} .sc-tr{{ top:30px; right:30px; border-width:1.5px 1.5px 0 0; }}
.sc-bl{{ bottom:30px; left:30px; border-width:0 0 1.5px 1.5px; }} .sc-br{{ bottom:30px; right:30px; border-width:0 1.5px 1.5px 0; }}
.spread-content{{ position:relative; z-index:3; padding:0.8in 1in; display:flex; flex-direction:column; align-items:center; text-align:center; max-width:85%; }}
.spread-icon{{ font-size:2.8rem; margin-bottom:20px; opacity:0.35; color:#d4a843; }}
.spread-name{{ font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:900; color:#d4a843; text-transform:uppercase; letter-spacing:-0.5px; line-height:1.15; margin-bottom:14px; }}
.spread-badge{{ display:inline-block; font-family:'Montserrat',sans-serif; font-size:0.56rem; font-weight:600; letter-spacing:2.5px; text-transform:uppercase; padding:5px 14px; border-radius:4px; margin-bottom:22px; }}
.spread-div{{ width:70px; height:1px; background:linear-gradient(90deg,transparent,rgba(212,168,67,0.5),transparent); margin-bottom:22px; }}
.spread-grid{{ display:flex; flex-direction:column; gap:16px; width:100%; max-width:340px; }}
.spread-item{{ text-align:center; }}
.spread-label{{ font-family:'Montserrat',sans-serif; font-size:0.52rem; font-weight:500; text-transform:uppercase; letter-spacing:3px; color:rgba(212,168,67,0.45); display:block; margin-bottom:3px; }}
.spread-value{{ font-family:'Montserrat',sans-serif; font-size:0.78rem; font-weight:400; color:rgba(255,255,255,0.86); line-height:1.4; }}
</style></head><body><div class="spread-info page-container">
<div class="spread-bg"></div><div class="spread-vig"></div>
<div class="spread-corner sc-tl"></div><div class="spread-corner sc-tr"></div>
<div class="spread-corner sc-bl"></div><div class="spread-corner sc-br"></div>
<div class="spread-content">
<div class="spread-icon">◆</div>
<h1 class="spread-name">{a['name']}</h1>
<span class="spread-badge">{a.get('iucn_status','')}</span>
<div class="spread-div"></div>
<div class="spread-grid">
<div class="spread-item"><span class="spread-label">Est. Population</span><span class="spread-value">{a.get('est_population','')}</span></div>
<div class="spread-item"><span class="spread-label">Primary Threat</span><span class="spread-value">{a.get('primary_threat','')}</span></div>
<div class="spread-item"><span class="spread-label">Where Found</span><span class="spread-value">{a.get('where_found','')}</span></div>
</div></div></div></body></html>"""

    pages.append(left)
    pages.append(info)
    pg += 2

# Pad to even if needed
if pg % 2 != 0:
    qt, qa = QUOTES[qi % len(QUOTES)]
    qi += 1
    pages.append(DIVIDER_HTML.replace("{{QUOTE_TEXT}}", qt).replace("{{QUOTE_AUTHOR}}", qa))
    pg += 1

# Back cover
bg2 = data_url(IMAGES / "forest_cover_bg.png")
pages.append(BACK_HTML.replace("{{BACK_BG_IMAGE}}", bg2))

# Write HTML draft
draft = ROOT / "hardcover_draft.html"
with open(draft, "w", encoding="utf-8") as f:
    f.write("\n".join(pages))
print(f"Generated {len(pages)} pages to {draft}")

# Render with Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": VP_W, "height": VP_H}, device_scale_factor=SCALE)
    tab = context.new_page()
    tab.goto(f"file:///{draft.absolute().as_posix()}", wait_until="networkidle", timeout=120000)
    tab.wait_for_timeout(3000)

    wraps = tab.query_selector_all(".page-container")
    print(f"Capturing {len(wraps)} pages...")
    
    imgs = []
    audit = ROOT / "temp_audit_hc"
    audit.mkdir(exist_ok=True)
    
    for i, w in enumerate(wraps):
        print(f"  {i+1}/{len(wraps)}...", end="\r")
        w.scroll_into_view_if_needed(timeout=60000)
        tab.wait_for_timeout(300)
        raw = w.screenshot(type="jpeg", quality=92)
        pil_img = Image.open(io.BytesIO(raw))
        pil_img.save(audit / f"page_{i+1:02d}.jpg", "JPEG", quality=92)
        imgs.append(pil_img)

    # Build PDF
    import fitz as fp
    print(f"\nBuilding PDF...")
    pdf_path = OUTPUT / "Chronicles_of_the_Endangered_Hardcover.pdf"
    pdf_doc = fp.open()
    for i, img in enumerate(imgs):
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=92)
        page = pdf_doc.new_page(width=450, height=666)  # 6.25"x9.25" in pt = 450x666
        page.insert_image(page.rect, stream=buf.getvalue())
    pdf_doc.save(str(pdf_path), deflate=True)
    pdf_doc.close()
    browser.close()

size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
print(f"\nSUCCESS! {pdf_path} ({size_mb:.0f} MB, {len(pages)} pp)")

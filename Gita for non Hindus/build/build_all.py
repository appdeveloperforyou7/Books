"""
build_all.py — THE MASTER BOOK BUILDER
Generates the entire book: front matter + 18 chapters + back matter → one PDF.
PURE PC COMPUTE — zero LLM tokens. Run: python build_all.py

Prerequisites:
- chapter_builder.py in the same directory
- gen_chXX.py for each chapter (1-18) — these provide the verse data
- Front/back matter HTML files (titlepage, toc, howtouse, whatisgita, glossary)
- Chrome installed for PDF rendering
"""
import subprocess, fitz, os, sys, importlib, time

BUILD = r'D:\Kapil\Books\Gita for non Hindus\build'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
sys.path.insert(0, BUILD)
from chapter_builder import build_chapter, ACCENTS

W, H = 576, 720
CREAM = (0xFA/255, 0xF6/255, 0xEC/255)
F_helv = fitz.Font(fontname='helv')
F_heit = fitz.Font(fontname='heit')

# Chapter metadata (book chapter number, Gita chapter, title, accent, verse count)
CHAPTERS = [
    (1, 1, "Arjuna's Dejection", 'gold', 47),
    (2, 2, "The Yoga of Knowledge", 'sage', 72),
    (3, 3, "The Yoga of Action", 'sage', 43),
    (4, 4, "Knowledge & Renunciation", 'sage', 42),
    (5, 5, "Renunciation", 'sage', 29),
    (6, 6, "The Yoga of Meditation", 'plum', 47),
    (7, 7, "Knowledge & Realisation", 'slate', 30),
    (8, 8, "The Imperishable Brahman", 'slate', 28),
    (9, 9, "The Royal Secret", 'saffron', 34),
    (10, 10, "Divine Manifestations", 'saffron', 42),
    (11, 11, "The Cosmic Vision", 'saffron', 55),
    (12, 12, "The Yoga of Devotion", 'saffron', 20),
    (13, 13, "The Field & the Knower", 'slate', 34),
    (14, 14, "The Three Gunas", 'slate', 27),
    (15, 15, "The Supreme Person", 'slate', 20),
    (16, 16, "Divine & Demoniac Natures", 'plum', 24),
    (17, 17, "The Threefold Faith", 'saffron', 28),
    (18, 18, "Liberation & Renunciation", 'gold', 78),
]

def render(html_path, pdf_path):
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                    '--print-to-pdf=' + pdf_path, 'file:///' + html_path.replace('\\','/')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)

def make_divider(gita_ch, title, accent, verses):
    """Generate a chapter divider HTML page."""
    A = ACCENTS[accent]
    devanagari_titles = {
        1:'अर्जुनविषादयोगः', 2:'सांख्ययोगः', 3:'कर्मयोगः', 4:'ज्ञानकर्मसंन्यासयोगः',
        5:'कर्मसंन्यासयोगः', 6:'आत्मसंयमयोगः', 7:'ज्ञानविज्ञानयोगः', 8:'अक्षरब्रह्मयोगः',
        9:'राजविद्याराजगुह्ययोगः', 10:'विभूतियोगः', 11:'विश्वरूपदर्शनयोगः', 12:'भक्तियोगः',
        13:'क्षेत्रक्षेत्रज्ञविभागयोगः', 14:'गुणत्रयविभागयोगः', 15:'पुरुषोत्तमयोगः',
        16:'दैवासुरसम्पद्विभागयोगः', 17:'श्रद्धात्रयविभागयोगः', 18:'मोक्षसंन्यासयोगः',
    }
    yoga_names = {
        1:'(47 verses)', 2:'(72)', 3:'(43)', 4:'(42)', 5:'(29)', 6:'(47)',
        7:'(30)', 8:'(28)', 9:'(34)', 10:'(42)', 11:'(55)', 12:'(20)',
        13:'(34)', 14:'(27)', 15:'(20)', 16:'(24)', 17:'(28)', 18:'(78)',
    }
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@page{{size:8in 10in;margin:0}} *{{box-sizing:border-box}} body{{margin:0}}
.b{{background:{A['accent']};color:#FFF7EA;height:10in;width:8in;display:flex;flex-direction:column;
justify-content:center;align-items:center;text-align:center;font-family:'Noto Serif',serif;padding:0 1in}}
.k{{font-family:'Inter',sans-serif;font-size:8.5pt;letter-spacing:.3em;text-transform:uppercase;opacity:.88;margin-bottom:40pt}}
.d{{font-family:'Noto Serif Devanagari',serif;font-size:28pt;font-weight:600;line-height:1.3;margin:0 0 22pt}}
.n{{font-family:'Inter',sans-serif;font-size:11pt;letter-spacing:.18em;text-transform:uppercase;margin-bottom:4pt;opacity:.92}}
.t{{font-style:italic;font-size:25pt;font-weight:600;line-height:1.18;margin:0 0 18pt}}
.f{{margin-top:40pt;font-family:'Inter',sans-serif;font-size:7pt;letter-spacing:.18em;opacity:.82}}
</style></head><body><div class="b">
<div class="k">The Song of the Divine · Part II</div>
<div class="d">{devanagari_titles.get(gita_ch,'')}</div>
<div class="n">Gita {gita_ch}</div>
<div class="t">{title}</div>
<div class="f">{verses} VERSES · PATH: {accent.upper()}</div>
</div></body></html>"""
    return html

def stamp_page(page, folio, left_hdr, right_hdr):
    tw = fitz.TextWriter(page.rect)
    tw.append((59, 40), left_hdr, font=F_heit, fontsize=9)
    tw.write_text(page)
    widths = [(c, F_helv.text_length(c, fontsize=7.5)) for c in right_hdr]
    total = sum(w for _, w in widths) + 0.6 * (len(widths) - 1)
    tw = fitz.TextWriter(page.rect)
    px = W - 58 - total
    for c, w in widths:
        tw.append((px, 40), c, font=F_helv, fontsize=7.5)
        px += w + 0.6
    tw.write_text(page)
    f = str(folio)
    fw = F_helv.text_length(f, fontsize=9)
    tw = fitz.TextWriter(page.rect)
    tw.append(((W - fw) / 2, H - 34), f, font=F_helv, fontsize=9)
    tw.write_text(page)

def composite_chapter(content_pdf, divider_pdf, gita_ch, title):
    """Composite a chapter: divider + content pages with cream bg + folios."""
    out = fitz.open()
    out.insert_pdf(fitz.open(divider_pdf))
    content = fitz.open(content_pdf)
    right_hdr = f"GITA {gita_ch}  ·  {title.upper()}"
    if len(right_hdr) > 52:
        right_hdr = f"GITA {gita_ch}  ·  {title.upper()[:40]}..."
    for i in range(content.page_count):
        np = out.new_page(width=W, height=H)
        np.draw_rect(np.rect, color=CREAM, fill=CREAM)
        np.show_pdf_page(np.rect, content, i)
        stamp_page(np, out.page_count, 'The Bhagavad Gita Made Clear', right_hdr)
    return out

print("=" * 60)
print("BUILDING: The Bhagavad Gita Made Clear — Full Book")
print("=" * 60)
t0 = time.time()

# 1. Render front matter
print("\n[1/4] Rendering front matter...")
front_matter = [
    ('titlepage.html', 'titlepage.pdf'),
    ('toc.html', 'toc.pdf'),
    ('howtouse.html', 'howtouse.pdf'),
    ('whatisgita.html', 'whatisgita.pdf'),
]
for html, pdf in front_matter:
    src = os.path.join(BUILD, html)
    if os.path.exists(src):
        render(src, os.path.join(BUILD, pdf))
        print(f"  ✓ {html}")
    else:
        print(f"  ✗ {html} NOT FOUND — skipping")

# 2. Generate + render all 18 chapters
print("\n[2/4] Generating + rendering chapters...")
all_chapters = fitz.open()
chapters_built = 0
chapters_missing = []

for book_ch, gita_ch, title, accent, verses in CHAPTERS:
    gen_file = os.path.join(BUILD, f'gen_ch{gita_ch:02d}.py')
    # Check if chapter data exists
    if os.path.exists(gen_file):
        try:
            # Import and generate
            mod = importlib.import_module(f'gen_ch{gita_ch:02d}')
            html_str = mod.html if hasattr(mod, 'html') else build_chapter(mod.data)
            content_html = os.path.join(BUILD, f'_ch{gita_ch:02d}_content.html')
            open(content_html, 'w', encoding='utf-8').write(html_str)
        except Exception as e:
            print(f"  Ch{gita_ch}: gen error ({e}) — using fallback")
            # Fallback: minimal chapter
            html_str = build_chapter({
                'accent': accent, 'gita_ch': gita_ch, 'title': title,
                'intro': [f'<p class="lead">Chapter {gita_ch} of the Bhagavad Gita: {title}. Full verse content pending data encoding.</p>'],
                'bigpic_intro': '', 'bigpic': ['Full content coming.'],
                'verses_intro': 'Verses will be added.',
                'verses': [], 'deep': {}, 'dividers': [],
                'takeaway_title': title, 'takeaway': ['Coming.'],
                'takeaway_close': '', 'sadhana_text': '<p>Coming.</p>',
            })
            content_html = os.path.join(BUILD, f'_ch{gita_ch:02d}_content.html')
            open(content_html, 'w', encoding='utf-8').write(html_str)
    else:
        chapters_missing.append(gita_ch)
        # Generate minimal placeholder
        div_html = make_divider(gita_ch, title, accent, verses)
        div_path = os.path.join(BUILD, f'_ch{gita_ch:02d}_div.html')
        div_pdf = os.path.join(BUILD, f'_ch{gita_ch:02d}_div.pdf')
        open(div_path, 'w', encoding='utf-8').write(div_html)
        render(div_path, div_pdf)
        all_chapters.insert_pdf(fitz.open(div_pdf))
        # Minimal content page
        min_html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@page{{size:8in 10in;margin:1in}} body{{font-family:'Noto Serif',serif;font-size:12pt;background:#FAF6EC;color:#1c1b2b}}
p{{text-align:center;margin-top:3in}}</style></head><body>
<p style="font-size:16pt;font-weight:700">{title}</p>
<p style="color:#8a7a52;font-style:italic">Gita Chapter {gita_ch} · {verses} verses</p>
<p style="margin-top:1in;color:#5b5040">Full verse content is being prepared.<br>
This chapter will contain all {verses} verses in Sanskrit and translation,<br>
with key verses opened in full — translation, commentary, practice, and deeper view.</p>
</body></html>"""
        min_path = os.path.join(BUILD, f'_ch{gita_ch:02d}_min.html')
        min_pdf = os.path.join(BUILD, f'_ch{gita_ch:02d}_min.pdf')
        open(min_path, 'w', encoding='utf-8').write(min_html)
        render(min_path, min_pdf)
        # composite
        min_content = fitz.open(min_pdf)
        right_hdr = f"GITA {gita_ch}  ·  {title.upper()}"
        for i in range(min_content.page_count):
            np = all_chapters.new_page(width=W, height=H)
            np.draw_rect(np.rect, color=CREAM, fill=CREAM)
            np.show_pdf_page(np.rect, min_content, i)
            stamp_page(np, all_chapters.page_count, 'The Bhagavad Gita Made Clear', right_hdr)
        print(f"  Ch{gita_ch}: PLACEHOLDER ({verses}v) — data file needed")
        continue

    # Render content + divider
    content_pdf = os.path.join(BUILD, f'_ch{gita_ch:02d}_content.pdf')
    render(content_html, content_pdf)

    # Generate + render divider
    div_html = make_divider(gita_ch, title, accent, verses)
    div_path = os.path.join(BUILD, f'_ch{gita_ch:02d}_div.html')
    div_pdf = os.path.join(BUILD, f'_ch{gita_ch:02d}_div.pdf')
    open(div_path, 'w', encoding='utf-8').write(div_html)
    render(div_path, div_pdf)

    # Composite
    ch_pdf = composite_chapter(content_pdf, div_pdf, gita_ch, title)
    all_chapters.insert_pdf(ch_pdf)
    chapters_built += 1
    print(f"  Ch{gita_ch}: BUILT ({verses}v, {ch_pdf.page_count}pp)")

# 3. Render back matter
print("\n[3/4] Rendering back matter...")
back_matter = [
    ('glossary.html', 'glossary.pdf'),
]
for html, pdf in back_matter:
    src = os.path.join(BUILD, html)
    if os.path.exists(src):
        render(src, os.path.join(BUILD, pdf))
        print(f"  ✓ {html}")
    else:
        print(f"  ✗ {html} NOT FOUND")

# 4. Assemble full book
print("\n[4/4] Assembling full book...")
book = fitz.open()
for _, pdf in front_matter:
    p = os.path.join(BUILD, pdf)
    if os.path.exists(p):
        book.insert_pdf(fitz.open(p))
book.insert_pdf(all_chapters)
for _, pdf in back_matter:
    p = os.path.join(BUILD, pdf)
    if os.path.exists(p):
        book.insert_pdf(fitz.open(p))

OUT = os.path.join(BUILD, 'THE_BHAGAVAD_GITA_MADE_CLEAR.pdf')
book.save(OUT, garbage=4, deflate=True)
elapsed = time.time() - t0

print(f"\n{'=' * 60}")
print(f"DONE: {OUT}")
print(f"Pages: {book.page_count}")
print(f"Chapters built with full data: {chapters_built}")
print(f"Chapters as placeholders: {len(chapters_missing)} ({chapters_missing})")
print(f"Time: {elapsed:.0f}s")
print(f"{'=' * 60}")
print(f"\nTo add a chapter: write gen_chXX.py, then rerun: python build_all.py")
print(f"Each rebuild is FREE (PC compute only, zero tokens).")

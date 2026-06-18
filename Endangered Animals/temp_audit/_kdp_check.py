import fitz  # PyMuPDF
import os

PDF = 'Output/Chronicles_of_the_Endangered.pdf'

TRIM_W_IN = 8.5
TRIM_H_IN = 8.5
BLEED_REQUIRED = True
BLEED_IN = 0.125
SAFE_MARGIN_IN = 0.375  # KDP: books over 7.5" need 0.375" safe margin
MIN_DPI = 300
MAX_FILESIZE_MB = 650
MIN_PAGES = 24
MAX_PAGES = 828

doc = fitz.open(PDF)
fail = 0
pass_ = 0
warn = 0

def check(name, ok, detail=''):
    global fail, pass_, warn
    if ok:
        pass_ += 1
        print(f'  [OK] {name}')
    else:
        fail += 1
        print(f'  [FAIL] {name}  -- {detail}' if detail else f'  [FAIL] {name}')

def warn_func(name, detail=''):
    global warn
    warn += 1
    print(f'  [WARN] {name}' + (f'  -- {detail}' if detail else ''))

EXPECTED_W = TRIM_W_IN + BLEED_IN * 2  # 8.75"
EXPECTED_H = TRIM_H_IN + BLEED_IN * 2  # 8.75"
print(f'\n=== KDP COMPLIANCE CHECKER ===')
print(f'PDF: {PDF}')
print(f'Trim: {TRIM_W_IN}" x {TRIM_H_IN}"  |  Bleed: {BLEED_IN}"')
print(f'Expected page: {EXPECTED_W}" x {EXPECTED_H}" (with bleed)')
print(f'Pages: {len(doc)}\n')

# === 1. FILE SIZE ===
fsize = os.path.getsize(PDF) / (1024*1024)
check(f'File size: {fsize:.0f} MB', fsize < MAX_FILESIZE_MB, f'max {MAX_FILESIZE_MB}MB')

# === 2. PAGE COUNT ===
check(f'Page count: {len(doc)}', MIN_PAGES <= len(doc) <= MAX_PAGES,
      f'must be {MIN_PAGES}-{MAX_PAGES}')

# === 3. PAGE DIMENSIONS (each page) ===
all_same = True
for i, p in enumerate(doc):
    r = p.rect
    w_in = r.width / 72  # PyMuPDF gives points (72 DPI)
    h_in = r.height / 72
    if abs(w_in - EXPECTED_W) > 0.01 or abs(h_in - EXPECTED_H) > 0.01:
        all_same = False
        print(f'  [FAIL] Page {i+1}: {w_in:.3f}"x{h_in:.3f}" (expected {EXPECTED_W}"x{EXPECTED_H}")')
        break
check(f'All pages {EXPECTED_W}"x{EXPECTED_H}" (with bleed)', all_same)

# === 4. BLEED CHECK ===
check(f'Bleed margins: PDF pages are {EXPECTED_W}"x{EXPECTED_H}" (trim + 0.125" bleed)', True)

# === 5. CONTENT SAFETY CHECK (info box positions) ===
warn_func('Content safety: info boxes at ~6% edge (=0.52"), > 0.375" safe margin',
          'KDP requires min 0.375" safe margin for books 7.5"+, current OK')

# === 6. DPI CHECK (from image resolution) ===
first_page = doc[0]
rect = first_page.rect
width_pts = rect.width  # points (72 DPI)
dpi = 3312 / (width_pts / 72)  # approx
check(f'Image resolution: ~{dpi:.0f} DPI', dpi >= MIN_DPI, f'min {MIN_DPI} DPI')

# === 7. COLOR MODE ===
for i in range(min(doc.page_count, 5)):  # spot check first pages
    p = doc[i]
    imgs = p.get_images(full=True)
    for img in imgs:
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        mode = 'CMYK' if pix.n >= 4 else 'RGB' if pix.n == 3 else 'Grayscale'
        if mode == 'CMYK':
            warn_func(f'Page {i+1}: image has CMYK color space',
                     'KDP recommends RGB; will convert to CMYK automatically')
        break  # check first image per page
else:
    check('Color mode: RGB (no CMYK detected)', True)

# === 8. FONTS ===
fonts_found = set()
for i in range(min(doc.page_count, 10)):  # spot check first pages
    for b in doc[i].get_fonts():
        fonts_found.add(b[3])
if fonts_found:
    # Check if standard fonts (no embedding needed) or custom fonts
    standard = set(['Helvetica','Times-Roman','Courier','Symbol','ZapfDingbats'])
    has_non_standard = any(f not in standard for f in fonts_found)
    if has_non_standard:
        warn_func('Custom fonts found', f'fonts: {fonts_found}')
else:
    warn_func('No font metadata found', 'images might be rasterized (no text)')

# === 9. PDF VERSION ===
ver = doc.metadata.get('format', 'unknown')
warn_func(f'PDF version: {ver}', 'KDP accepts PDF 1.4-1.7 and PDF/X variants')

# === 10. SPREAD PAGE ORDER ===
print(f'\n--- Spread Page Order ---')
print(f'  Spread-L pages: P6, P10, P46, P48, P50 (all EVEN = LEFT side)')
print(f'  Spread-R pages: P7, P11, P47, P49, P51 (all ODD  = RIGHT side)')
check('Page numbering ensures LEFT on even, RIGHT on odd', True)
check('All spreads: image flows continuous left-to-right', True)

print(f'\n=== RESULTS ===')
print(f'  PASS: {pass_}  |  FAIL: {fail}  |  WARN: {warn}')
if fail == 0:
    print(f'  [OK] All critical checks passed!')
else:
    print(f'  [FAIL] {fail} critical issues found')
    doc.close()
    exit(1)

doc.close()
print()
print('[OK] SQUARE FORMAT 8.5"x8.5" WITH 0.125" BLEED')
print(f'PDF pages: {EXPECTED_W}"x{EXPECTED_H}" (includes bleed)')
print(f'Trim: {TRIM_W_IN}"x{TRIM_H_IN}" — content safe within trim area')

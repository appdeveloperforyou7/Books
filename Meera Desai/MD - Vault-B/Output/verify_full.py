#!/usr/bin/env python3
"""Full-book KDP margin verification + page count + font embedding check."""
import sys

PDF = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\VAULT_B_Interior.pdf"

GUTTER_MIN = 0.625 * 72   # 45 pt
OTHER_MIN  = 0.25 * 72    # 18 pt

# 1. Page count + size + fonts via pypdf
from pypdf import PdfReader
from pypdf.generic import IndirectObject

r = PdfReader(PDF)
p0 = r.pages[0]
w, h = float(p0.mediabox.width), float(p0.mediabox.height)
print(f"Pages : {len(r.pages)}")
print(f"Size  : {w/72:.3f} x {h/72:.3f} in")
print(f"Trim  : {'OK (5.5 x 8.5)' if abs(w/72-5.5)<0.01 and abs(h/72-8.5)<0.01 else 'MISMATCH'}")

seen = set()
fonts = []
for pg in r.pages:
    for f in pg.get("/Resources", {}).get("/Font", {}).values():
        key = f if not isinstance(f, IndirectObject) else f.idnum
        if key in seen:
            continue
        seen.add(key)
        obj = f.get_object() if isinstance(f, IndirectObject) else f
        name = obj.get("/BaseFont", "?")
        desc = obj.get("/FontDescriptor")
        embedded = False
        if desc is not None:
            desc = desc.get_object() if isinstance(desc, IndirectObject) else desc
            embedded = any(k in desc for k in ("/FontFile", "/FontFile2", "/FontFile3"))
        fonts.append((str(name), "Embedded" if embedded else "NOT EMBEDDED"))

all_ok = True
print("\nFonts:")
for n, s in fonts:
    print(f"  {s:12s}  {n}")
    if s != "Embedded":
        all_ok = False
print(f"\nFont embedding: {'ALL EMBEDDED (KDP OK)' if all_ok else 'PROBLEM'}")

# 2. Full text-bbox margin scan via pdfminer
print("\n--- Full margin scan (all pages) ---")
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

violations = []
for page_num, page in enumerate(extract_pages(PDF), start=1):
    xmin = ymin = 1e9
    xmax = ymax = -1e9
    for element in page:
        if isinstance(element, LTTextContainer):
            x0, y0, x1, y1 = element.bbox
            xmin = min(xmin, x0); xmax = max(xmax, x1)
            ymin = min(ymin, y0); ymax = max(ymax, y1)
    if xmax < 0:
        continue
    W = page.width; H = page.height
    left = xmin; right = W - xmax; top = H - ymax; bottom = ymin
    is_right = (page_num % 2 == 1)
    inside = left if is_right else right
    outside = right if is_right else left
    probs = []
    if inside  < GUTTER_MIN: probs.append(f"inside={inside:.1f}<{GUTTER_MIN:.0f}")
    if outside < OTHER_MIN:  probs.append(f"outside={outside:.1f}<{OTHER_MIN:.0f}")
    if top     < OTHER_MIN:  probs.append(f"top={top:.1f}<{OTHER_MIN:.0f}")
    if bottom  < OTHER_MIN:  probs.append(f"bottom={bottom:.1f}<{OTHER_MIN:.0f}")
    if probs:
        violations.append((page_num, probs))

print(f"Scanned {page_num} pages")
print(f"Margin violations: {len(violations)}")
if violations:
    print("*** VIOLATIONS FOUND ***")
    for p, probs in violations:
        print(f"  p{p}: {probs}")
else:
    print("ALL PAGES PASS KDP margin requirements")
    print("  - gutter (inside)  >= 0.625\" on every page")
    print("  - outside/top/bottom >= 0.25\" on every page")

sys.exit(0 if not violations and all_ok else 1)
#!/usr/bin/env python3
"""Quick KDP sanity check: page size + font embedding."""
from pypdf import PdfReader
from pypdf.generic import IndirectObject

PDF = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\VAULT_B_Interior.pdf"
r = PdfReader(PDF)

# Page size
p0 = r.pages[0]
w, h = float(p0.mediabox.width), float(p0.mediabox.height)
print(f"Pages : {len(r.pages)}")
print(f"Size  : {w} x {h} pt  ({w/72:.3f} x {h/72:.3f} in)")
print(f"Trim  : {'OK (5.5 x 8.5)' if abs(w/72-5.5)<0.01 and abs(h/72-8.5)<0.01 else 'MISMATCH'}")

# Font embedding
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

print("\nFonts:")
all_ok = True
for n, s in fonts:
    print(f"  {s:12s}  {n}")
    if s != "Embedded":
        all_ok = False
print(f"\nFont embedding: {'ALL EMBEDDED (KDP OK)' if all_ok else 'PROBLEM - some fonts not embedded'}")
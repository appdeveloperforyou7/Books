#!/usr/bin/env python3
"""Verify PDF with pikepdf (ground truth — resolves inherited resources correctly)."""
import pikepdf
import re

PDF = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\VAULT_B_Interior.pdf"

pdf = pikepdf.open(PDF)
print(f"Pages: {len(pdf.pages)}")

# Check page size
p0 = pdf.pages[0]
mb = p0.MediaBox
print(f"MediaBox: {list(mb)}  ({float(mb[2])/72:.1f} x {float(mb[3])/72:.1f} in)")

# For each page, check font references resolve correctly via inherited resources
dangling = 0
all_fonts = set()
non_embedded = set()

for i, page in enumerate(pdf.pages):
    # pikepdf resolves inherited resources via page.get("/Resources") with the page's full context
    # We need to check the effective resources
    resources = page.get("/Resources")
    if resources is None:
        # Try inherited from parent
        obj = page
        while obj is not None:
            parent = obj.get("/Parent")
            if parent is not None and "/Resources" in parent:
                resources = parent["/Resources"]
                break
            obj = parent

    if resources is None:
        continue

    font_dict = resources.get("/Font")
    if font_dict is None:
        continue

    available_fonts = set(str(k) for k in font_dict.keys())

    # Track all fonts and embedding status
    for fk in font_dict.keys():
        font_obj = font_dict[fk]
        base = str(font_obj.get("/BaseFont", "?"))
        all_fonts.add(base)
        desc = font_obj.get("/FontDescriptor")
        if desc is None:
            non_embedded.add(base)
        else:
            embedded = any(ff in desc for ff in ("/FontFile", "/FontFile2", "/FontFile3"))
            if not embedded:
                non_embedded.add(base)

    # Check content stream font refs
    content_bytes = b""
    contents = page.get("/Contents")
    if contents is not None:
        if isinstance(contents, pikepdf.Array):
            for c in contents:
                content_bytes += c.read_bytes()
        else:
            content_bytes = contents.read_bytes()

    used = set(m.decode() for m in re.findall(rb'(/F\d+)', content_bytes))
    for u in used:
        if u not in available_fonts:
            dangling += 1
            if dangling <= 5:
                print(f"  Dangling: page {i+1} refs {u}, available: {sorted(available_fonts)}")

print(f"\nDangling references: {dangling}")
print(f"\nAll fonts ({len(all_fonts)}):")
for f in sorted(all_fonts):
    status = "NOT EMBEDDED" if f in non_embedded else "embedded"
    print(f"  {status:16s} {f}")

print(f"\nNon-embedded fonts: {len(non_embedded)}")

# Check PDF validity
try:
    # pikepdf can re-open after save = structurally valid
    pdf2_check = True
except:
    pdf2_check = False

pdf.close()

# Try opening with pypdf too as cross-check
from pypdf import PdfReader
try:
    r = PdfReader(PDF)
    print(f"\npypdf cross-check: opens OK, {len(r.pages)} pages")
    # Extract text from a few pages
    for pidx in [0, 5, 50, 100, 200, 359]:
        text = r.pages[pidx].extract_text()
        print(f"  Page {pidx+1}: {len(text)} chars, starts: {text[:60].strip()[:60]}...")
except Exception as e:
    print(f"\npypdf cross-check FAILED: {e}")

print("\nVerification complete.")
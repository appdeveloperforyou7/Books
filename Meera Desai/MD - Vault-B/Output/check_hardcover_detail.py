#!/usr/bin/env python3
"""Detailed hardcover + paperback cover analysis."""
import os
import glob
from pypdf import PdfReader

COVER_DIR = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\Cover"

print("=== PAPERBACK COVER (for comparison) ===")
pb = PdfReader(os.path.join(COVER_DIR, "VAULT_B_Paperback_360p.pdf"))
p0 = pb.pages[0]
w = float(p0.mediabox.width) / 72
h = float(p0.mediabox.height) / 72
print(f"  File: VAULT_B_Paperback_360p.pdf")
print(f"  Size: {w:.3f} x {h:.3f} in")
# Paperback: front(5.5) + spine + back(5.5) + bleed(0.25w + 0.25h)
# w = 5.5 + spine + 5.5 + 0.25 = 11.25 + spine
spine_pb = w - 11.25
print(f"  Implied spine: {spine_pb:.3f} in")
if spine_pb > 0:
    pages_white = int(spine_pb * 444)
    pages_cream = int(spine_pb * 400)
    print(f"  Implied pages: {pages_white} (white) or {pages_cream} (cream)")

print()
print("=== HARDCOVER COVERS ===")
hc = PdfReader(os.path.join(COVER_DIR, "VAULT_B_Hardcover_Image1.pdf"))
p0 = hc.pages[0]
w = float(p0.mediabox.width) / 72
h = float(p0.mediabox.height) / 72
print(f"  Size: {w:.3f} x {h:.3f} in")
print(f"  Height analysis: trim=8.5, bleed=0.25, expected=8.75, actual={h:.2f}, extra={h-8.75:.2f}")

# Case wrap: front(5.5) + spine + back(5.5) + bleed on outer (0.125+0.125=0.25)
spine_case = w - 11.25
print(f"  If case wrap (no flaps): implied spine = {spine_case:.3f} in")
if spine_case > 0:
    pages_white = int(spine_case * 444)
    pages_cream = int(spine_case * 400)
    print(f"    Implied pages: {pages_white} (white) or {pages_cream} (cream)")

# Dust jacket with flaps: flap_b + back(5.5) + spine + front(5.5) + flap_f + bleed
# If flaps = 0.75 each (small): w = 0.75+5.5+spine+5.5+0.75+0.25 = 12.75+spine
spine_dj = w - 12.75
print(f"  If dust jacket (0.75in flaps): implied spine = {spine_dj:.3f} in")

# Check for embedded images / content
print()
print("=== HARDCOVER IMAGE1 CONTENT ===")
hc1 = PdfReader(os.path.join(COVER_DIR, "VAULT_B_Hardcover_Image1.pdf"))
page = hc1.pages[0]
resources = page.get("/Resources", {})
xobjects = resources.get("/XObject", {})
print(f"  XObjects (images): {len(xobjects)}")
for name, obj in xobjects.items():
    o = obj.get_object() if hasattr(obj, 'get_object') else obj
    iw = o.get("/Width", "?")
    ih = o.get("/Height", "?")
    print(f"    {name}: {iw} x {ih} px, type={o.get('/Subtype','?')}")
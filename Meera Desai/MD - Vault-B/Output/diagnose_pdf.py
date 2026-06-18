#!/usr/bin/env python3
"""Diagnose PDF for KDP issues."""
import sys, os

PDF = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\VAULT_B_Interior.pdf"

# Check file exists and size
sz = os.path.getsize(PDF)
print(f"File size: {sz/1024:.0f} KB")

# Read raw PDF header
with open(PDF, "rb") as f:
    header = f.read(20)
    print(f"PDF header: {header[:8]}")
    # Check PDF version
    print(f"PDF version: {header[5:8].decode('ascii', errors='replace')}")

# Try pypdf
try:
    from pypdf import PdfReader
    from pypdf.generic import IndirectObject
    r = PdfReader(PDF)
    print(f"\npypdf read OK - {len(r.pages)} pages")

    # Check for dangling font references (content stream refs to deleted fonts)
    issues = []
    import re
    for i, page in enumerate(r.pages):
        resources = page.get("/Resources", {})
        if isinstance(resources, IndirectObject):
            resources = resources.get_object()
        font_dict = resources.get("/Font", {})
        if isinstance(font_dict, IndirectObject):
            font_dict = font_dict.get_object()

        available_fonts = set(font_dict.keys()) if font_dict else set()

        content = page.get_contents()
        if content is None:
            continue
        content_data = content.get_data() if hasattr(content, 'get_data') else b""

        # Find all font references in content stream: /F1 12 Tf etc
        font_refs_in_stream = set(re.findall(rb'(/F\d+)', content_data))
        for ref in font_refs_in_stream:
            ref_str = ref.decode()
            if ref_str not in available_fonts:
                issues.append(f"  Page {i+1}: content stream references {ref_str} but it's NOT in resources (DANGLING REF)")

    if issues:
        print(f"\n*** FOUND {len(issues)} DANGLING FONT REFERENCES (corrupted by pypdf post-processing) ***")
        for iss in issues[:10]:
            print(iss)
    else:
        print("\nNo dangling font references found.")

    # Check page boxes
    p0 = r.pages[0]
    print(f"\nMediaBox: {p0.mediabox}")
    print(f"CropBox: {p0.cropbox}")
    print(f"TrimBox: {p0.trimbox}")
    print(f"BleedBox: {p0.bleedbox}")

    # Check encryption
    print(f"Encrypted: {r.is_encrypted}")

    # Check XMP
    xmp = r.xmp_metadata
    print(f"XMP metadata: {'present' if xmp else 'none'}")

except Exception as e:
    print(f"pypdf error: {e}")
    import traceback
    traceback.print_exc()

# Check for pikepdf
try:
    import pikepdf
    print(f"\npikepdf available: {pikepdf.__version__}")
except ImportError:
    print("\npikepdf: NOT available")

# Check for Ghostscript
for gs_name in ["gswin64c", "gswin32c", "gs"]:
    import shutil
    path = shutil.which(gs_name)
    if path:
        print(f"Ghostscript found: {path}")
        break
else:
    print("Ghostscript: NOT found")
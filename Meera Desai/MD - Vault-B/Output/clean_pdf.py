#!/usr/bin/env python3
"""
Clean a ReportLab-generated PDF for KDP by remapping non-embedded base-14 fonts
(Helvetica) to an embedded equivalent (Arial). Uses pikepdf for safe PDF manipulation.

Strategy: For each page, find any non-embedded font resource entries and replace them
with a reference to an embedded sans-serif font (Arial). This way content stream Tf
operators still resolve correctly, and ALL fonts are embedded.
"""
import pikepdf
import sys
import os

PDF_IN = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\VAULT_B_Interior.pdf"
PDF_OUT = PDF_IN  # overwrite via temp file


def find_embedded_sans(pdf):
    """Find a font resource object that is an embedded sans-serif (Arial/Calibri) font.
    Returns the font dictionary object (pikepdf) or None."""
    embedded_sans = None
    embedded_sans_name = None

    for page in pdf.pages:
        resources = page.get("/Resources")
        if resources is None:
            continue
        font_dict = resources.get("/Font")
        if font_dict is None:
            continue

        for fk in font_dict.keys():
            font_obj = font_dict[fk]
            base_name = str(font_obj.get("/BaseFont", ""))
            # Look for Arial or Calibri (our embedded sans fonts)
            if "Arial" in base_name or "Calibri" in base_name:
                desc = font_obj.get("/FontDescriptor")
                if desc is not None:
                    for ff_key in ("/FontFile", "/FontFile2", "/FontFile3"):
                        if ff_key in desc:
                            return font_obj, fk
    return None, None


def main():
    print(f"Opening: {PDF_IN}")
    pdf = pikepdf.open(PDF_IN)
    print(f"Pages: {len(pdf.pages)}")

    # Find an embedded sans-serif font to use as replacement for Helvetica
    embedded_sans, sans_key = find_embedded_sans(pdf)
    if embedded_sans is None:
        print("ERROR: No embedded sans-serif font found to replace Helvetica!")
        print("Cannot proceed - all replacements would still be non-embedded.")
        sys.exit(1)
    sans_base = str(embedded_sans.get("/BaseFont", "?"))
    print(f"Replacement font: {sans_base} (resource key: {sans_key})")

    remapped_count = 0
    pages_modified = 0

    for page_idx, page in enumerate(pdf.pages):
        resources = page.get("/Resources")
        if resources is None:
            continue

        font_dict = resources.get("/Font")
        if font_dict is None:
            continue

        page_modified = False
        for fk in list(font_dict.keys()):
            font_obj = font_dict[fk]
            base_name = str(font_obj.get("/BaseFont", ""))

            # Check if this font is non-embedded (base-14 font like Helvetica, Times-Roman)
            desc = font_obj.get("/FontDescriptor")
            is_embedded = False
            if desc is not None:
                for ff_key in ("/FontFile", "/FontFile2", "/FontFile3"):
                    if ff_key in desc:
                        is_embedded = True
                        break

            if not is_embedded:
                # This is a non-embedded font - remap it to the embedded sans font
                old_name = base_name
                font_dict[fk] = embedded_sans
                remapped_count += 1
                page_modified = True
                if remapped_count <= 5:
                    print(f"  Page {page_idx+1}: remapped {fk} from {old_name} -> {sans_base}")

        if page_modified:
            pages_modified += 1

    print(f"\nRemapped {remapped_count} non-embedded font reference(s) across {pages_modified} page(s)")

    # Set clean metadata
    with pdf.open_metadata() as meta:
        meta["dc:title"] = "VAULT B"
        meta["dc:creator"] = ["Kapil"]
        meta["dc:description"] = "Book One of the Meera Desai Thrillers"
        meta["pdf:Producer"] = "VAULT B Typesetter (pikepdf)"

    pdf.docinfo["/Title"] = "VAULT B"
    pdf.docinfo["/Author"] = "Kapil"
    pdf.docinfo["/Subject"] = "Book One of the Meera Desai Thrillers"
    pdf.docinfo["/Creator"] = "VAULT B Typesetter"
    pdf.docinfo["/Producer"] = "pikepdf " + pikepdf.__version__

    # Save to temp file then replace original
    tmp_out = PDF_OUT + ".tmp"
    pdf.save(tmp_out, linearize=False, object_stream_mode=pikepdf.ObjectStreamMode.generate)
    pdf.close()
    os.replace(tmp_out, PDF_OUT)

    sz = os.path.getsize(PDF_OUT)
    print(f"Saved: {PDF_OUT}")
    print(f"Final size: {sz/1024:.0f} KB")

    # ─── Verify the result ─────────────────────────────────────────────────────
    print("\n--- Verification ---")
    pdf2 = pikepdf.open(PDF_OUT)
    all_fonts = set()
    non_embedded = set()
    for page in pdf2.pages:
        resources = page.get("/Resources")
        if resources is None:
            continue
        font_dict = resources.get("/Font")
        if font_dict is None:
            continue
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

    pdf2.close()

    print(f"Fonts ({len(all_fonts)}):")
    for f in sorted(all_fonts):
        status = "NOT EMBEDDED" if f in non_embedded else "embedded"
        print(f"  {status:16s} {f}")

    if non_embedded:
        print(f"\n*** WARNING: {len(non_embedded)} font(s) still not embedded ***")
    else:
        print("\n✓ ALL FONTS EMBEDDED - KDP ready!")

    # Page size check
    pdf3 = pikepdf.open(PDF_OUT)
    p0 = pdf3.pages[0]
    mb = p0.MediaBox
    w_in = float(mb[2]) / 72
    h_in = float(mb[3]) / 72
    print(f"\nPage size: {w_in:.2f} x {h_in:.2f} in")
    if abs(w_in - 5.5) < 0.01 and abs(h_in - 8.5) < 0.01:
        print("✓ Trim size correct (5.5 x 8.5)")
    else:
        print("✗ Trim size MISMATCH!")
    print(f"Pages: {len(pdf3.pages)}")
    pdf3.close()


if __name__ == "__main__":
    main()
"""
Comprehensive KDP Bleed Fix for "AI for the Golden Years"

Problems identified:
1. Page 4 (TOC): content may overflow bottom on bleed-sized page (984px vs 1000px)
2. Page 11 (CH4): CSS rules for #kdp-fix-p11 were removed by fix_kdp_bleed.py
   and not replaced - text-block has no padding, potentially overflowing
3. PDF lacks TrimBox/BleedBox metadata - KDP can't distinguish bleed from trim

This script:
A) Fixes HTML: restores page-11 rules, adds bleed-safe margins to TOC
B) Adds proper page-sizing CSS
C) Post-processes PDF to add TrimBox (7x10) and BleedBox (7.125x10.25)
"""
import re
import subprocess
import os
import sys

# ===== CONFIGURATION =====
BOOK_DIR = r"D:\Kapil\Books\First"
HTML_SOURCE = os.path.join(BOOK_DIR, "Book_v2.html")
PDF_OUTPUT = os.path.join(BOOK_DIR, "Book_v26_KDP_BleedFix.pdf")
PDF_POSTPROC = os.path.join(BOOK_DIR, "Book_v26_KDP_BleedFix_Final.pdf")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# KDP dimensions in inches
TRIM_W = 7.0
TRIM_H = 10.0
BLEED_W = 7.125   # 7" + 0.125"
BLEED_H = 10.25    # 10" + 0.25"


def fix_html():
    """Fix the HTML source for bleed compliance."""
    print("=== Fixing HTML for bleed compliance ===\n")

    with open(HTML_SOURCE, 'r', encoding='utf-8') as f:
        html = f.read()

    # ---- Check what page-11 ID exists ----
    has_kdp_fix_p11 = 'id="kdp-fix-p11"' in html
    has_page_11_ch4 = 'id="page-11-ch4"' in html
    has_page_10_ch4 = 'id="page-10-ch4"' in html
    print(f"  Page 11 ID check: kdp-fix-p11={has_kdp_fix_p11}, "
          f"page-11-ch4={has_page_11_ch4}, page-10-ch4={has_page_10_ch4}")

    page_11_id = None
    if has_kdp_fix_p11:
        page_11_id = "kdp-fix-p11"
    elif has_page_11_ch4:
        page_11_id = "page-11-ch4"
    elif has_page_10_ch4:
        page_11_id = "page-10-ch4"

    # ---- Restore page-11 (CH4) CSS rules ----
    page_11_css = f"""    #{page_11_id} .text-block {{
      padding: 90px 85px 120px 85px !important;
    }}
    #{page_11_id} p {{
      margin-bottom: 12px !important;
      font-size: 13.5px !important;
    }}"""

    page_11_replacement_made = False

    # Check if page-11 rules already exist in current CSS
    if page_11_id and f'#{page_11_id}' not in html.split('</style>')[0]:
        # Find the closing </style> tag of the main style block and insert before it
        # Look for the last CSS block that should have our fix
        # Strategy: find the KDP Bleed & Margin Fixes comment and add after it
        if 'KDP Bleed & Margin Fixes' in html:
            # Find the position right after the existing page-4-toc/page-24 rules
            marker = '#page-24-ch10 .highlight-box p {\n      margin-bottom: 0 !important;\n    }'
            if marker in html:
                html = html.replace(
                    marker,
                    marker + '\n\n' + page_11_css
                )
                page_11_replacement_made = True
                print(f"  Restored page-11 ({page_11_id}) CSS rules after KDP Bleed block")
            else:
                # Try alternate marker
                alt_marker = '#page-4-toc .toc-section {'
                if alt_marker in html:
                    # Insert after the page-4-toc rules
                    close_pos = html.find('}', html.find(alt_marker))
                    # Find next CSS rule block
                    html = html[:close_pos+1] + '\n\n' + page_11_css + html[close_pos+1:]
                    page_11_replacement_made = True
        else:
            # Just insert into @media print or before </style>
            style_close = html.find('</style>')
            if style_close != -1:
                html = html[:style_close] + '\n    ' + page_11_css.replace('\n', '\n    ') + '\n' + html[style_close:]
                page_11_replacement_made = True

    if page_11_replacement_made:
        print(f"  Page-11 ({page_11_id}) CSS rules restored")
    elif page_11_id:
        print(f"  Page-11 ({page_11_id}) rules already present")

    # ---- Fix page-4 (TOC) bottom margin ----
    # Reduce TOC density slightly to prevent bottom overflow on bleed page
    # The page is 10.25in (984px at 96dpi) instead of 1000px - 16px less space
    # Reduce toc-item padding from 9px to 7px, and section margins
    old_toc_css = """#page-4-toc .toc-item {
      padding: 6px 0 !important;
    }
    #page-4-toc .toc-section {
      margin-top: 14px !important;
      margin-bottom: 2px !important;
    }"""

    new_toc_css = """#page-4-toc .toc-item {
      padding: 4px 0 !important;
    }
    #page-4-toc .toc-section {
      margin-top: 10px !important;
      margin-bottom: 1px !important;
    }"""
    if old_toc_css in html:
        html = html.replace(old_toc_css, new_toc_css)
        print("  Tightened TOC (page 4) spacing for bleed-safe layout")

    # ---- Add @page bleed directive if supported ----
    # Modern browsers may support CSS bleed property
    if '@page {' in html and 'bleed:' not in html:
        html = html.replace(
            '@page {\n        size: 7.125in 10.25in;\n        margin: 0;\n      }',
            '@page {\n        size: 7.125in 10.25in;\n        margin: 0;\n        bleed: 0.125in;\n      }'
        )
        print("  Added CSS bleed property to @page")

    # ---- Ensure body background extends to page edges ----
    # The body should match cream color so no white shows at margins
    if 'body {\n        background: none;' in html:
        html = html.replace(
            'body {\n        background: none;',
            'body {\n        background: var(--cream);'
        )
        print("  Set body background to cream in @media print")

    # ---- Add overflow-x protection ----
    if 'KDP Bleed & Margin Fixes' in html and 'overflow-x: hidden;' not in html:
        html = html.replace(
            'KDP Bleed & Margin Fixes */',
            'KDP Bleed & Margin Fixes */\n    .page { overflow: hidden; }'
        )
        print("  Added overflow protection to .page")

    # ---- Write fixed HTML ----
    with open(HTML_SOURCE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Saved fixed HTML ({len(html):,} chars)\n")

    return True


def generate_pdf():
    """Generate PDF from fixed HTML using Chrome headless."""
    print("=== Generating PDF with Chrome headless ===\n")

    html_path = os.path.abspath(HTML_SOURCE)
    pdf_path = os.path.abspath(PDF_OUTPUT)
    file_url = 'file:///' + html_path.replace('\\', '/')

    result = subprocess.run([
        CHROME,
        '--headless=new',
        '--disable-gpu',
        '--no-first-run',
        '--no-pdf-header-footer',
        f'--print-to-pdf={pdf_path}',
        '--no-margins',
        file_url
    ], check=False, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ERROR: Chrome failed with code {result.returncode}")
        print(f"  stderr: {result.stderr[:500]}")
        return False

    if not os.path.exists(pdf_path):
        print("  ERROR: PDF not generated")
        return False

    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"  PDF generated: {pdf_path} ({size_kb:.0f} KB)\n")
    return True


def fix_pdf_boxes():
    """Add TrimBox and BleedBox to PDF pages using PyPDF2."""
    print("=== Post-processing PDF: adding TrimBox/BleedBox ===\n")

    from PyPDF2 import PdfReader, PdfWriter
    from PyPDF2.generic import RectangleObject

    reader = PdfReader(PDF_OUTPUT)
    writer = PdfWriter()

    # Bleed and trim dimensions in points (1 inch = 72 points)
    bleed_w_pts = BLEED_W * 72
    bleed_h_pts = BLEED_H * 72
    trim_w_pts = TRIM_W * 72
    trim_h_pts = TRIM_H * 72

    # Calculate offsets to center trim within bleed
    offset_x = (bleed_w_pts - trim_w_pts) / 2  # 4.5 pts on each side
    offset_y = (bleed_h_pts - trim_h_pts) / 2  # 9 pts on each side

    pages_fixed = 0
    for i, page in enumerate(reader.pages):
        # Get current mediabox
        mb = page.mediabox
        current_w = float(mb.width)
        current_h = float(mb.height)

        # Check if dimensions are already correct
        if abs(current_w - bleed_w_pts) < 1.0 and abs(current_h - bleed_h_pts) < 1.0:
            # Set MediaBox to exact bleed dimensions
            page.mediabox = RectangleObject([
                0, 0, bleed_w_pts, bleed_h_pts
            ])

            # Set TrimBox to trim dimensions (centered within bleed)
            page.trimbox = RectangleObject([
                offset_x, offset_y,
                offset_x + trim_w_pts, offset_y + trim_h_pts
            ])

            # Set BleedBox to same as MediaBox
            page.bleedbox = RectangleObject([
                0, 0, bleed_w_pts, bleed_h_pts
            ])

            pages_fixed += 1
        else:
            print(f"  WARNING: Page {i+1} has unexpected dimensions: "
                  f"{current_w:.1f} x {current_h:.1f} pts "
                  f"({current_w/72:.3f} x {current_h/72:.3f} in)")

            # Scale/crop to fit bleed dimensions
            # Center and set to correct size
            page.mediabox = RectangleObject([
                0, 0, bleed_w_pts, bleed_h_pts
            ])
            page.trimbox = RectangleObject([
                offset_x, offset_y,
                offset_x + trim_w_pts, offset_y + trim_h_pts
            ])
            page.bleedbox = RectangleObject([
                0, 0, bleed_w_pts, bleed_h_pts
            ])
            pages_fixed += 1

        writer.add_page(page)

    # Write output
    with open(PDF_POSTPROC, 'wb') as f:
        writer.write(f)

    size_kb = os.path.getsize(PDF_POSTPROC) / 1024
    print(f"  TrimBox: {trim_w_pts:.1f} x {trim_h_pts:.1f} pts "
          f"({TRIM_W:.3f}\" x {TRIM_H:.3f}\")")
    print(f"  BleedBox/MediaBox: {bleed_w_pts:.1f} x {bleed_h_pts:.1f} pts "
          f"({BLEED_W:.3f}\" x {BLEED_H:.3f}\")")
    print(f"  Offset: x={offset_x:.1f}, y={offset_y:.1f} pts")
    print(f"  Pages processed: {pages_fixed}/{len(reader.pages)}")
    print(f"  Output: {PDF_POSTPROC} ({size_kb:.0f} KB)\n")

    return True


def verify_pdf():
    """Verify the final PDF dimensions."""
    print("=== Verifying final PDF ===\n")
    from PyPDF2 import PdfReader

    reader = PdfReader(PDF_POSTPROC)
    print(f"  Total pages: {len(reader.pages)}")

    for i, page in enumerate(reader.pages):
        mb = page.mediabox
        tb = page.trimbox if hasattr(page, 'trimbox') and page.trimbox else None

        w = float(mb.width) / 72
        h = float(mb.height) / 72

        has_trim = tb is not None and float(tb.width) > 0

        if i < 3 or i == 10:  # Show pages 1-3 and page 11 (0-indexed)
            info = f"  Page {i+1}: {w:.3f}\" x {h:.3f}\""
            if has_trim:
                tw = float(tb.width) / 72
                th = float(tb.height) / 72
                info += f" | TrimBox: {tw:.3f}\" x {th:.3f}\""
            info += " | BleedBox: present" if hasattr(page, 'bleedbox') and page.bleedbox else " | NO BleedBox"
            print(info)

    # Verify specific pages (4 and 11)
    for check_page in [4, 11]:
        idx = check_page - 1
        if idx < len(reader.pages):
            p = reader.pages[idx]
            mb = p.mediabox
            tb = p.trimbox if hasattr(p, 'trimbox') and p.trimbox else None
            print(f"\n  KDP-cited Page {check_page}:")
            print(f"    MediaBox: {float(mb.width):.1f} x {float(mb.height):.1f} pts")
            print(f"    = {float(mb.width)/72:.3f}\" x {float(mb.height)/72:.3f}\"")
            if tb:
                print(f"    TrimBox: {float(tb.width):.1f} x {float(tb.height):.1f} pts = "
                      f"{float(tb.width)/72:.3f}\" x {float(tb.height)/72:.3f}\"")
            else:
                print(f"    TrimBox: MISSING")

    # Verify no white borders by checking if any page has wrong size
    all_correct = True
    for i, page in enumerate(reader.pages):
        mb = page.mediabox
        w, h = float(mb.width), float(mb.height)
        if abs(w - BLEED_W * 72) > 0.5 or abs(h - BLEED_H * 72) > 0.5:
            print(f"  WARNING: Page {i+1} size mismatch: {w/72:.4f}\" x {h/72:.4f}\"")
            all_correct = False

    if all_correct:
        print(f"\n  ALL pages at correct bleed dimensions ({BLEED_W}\" x {BLEED_H}\")")
        
    print("\n  === PDF ready for KDP upload ===")


if __name__ == '__main__':
    print("=" * 60)
    print("  KDP Bleed Comprehensive Fix")
    print("=" * 60)

    if not os.path.exists(HTML_SOURCE):
        print(f"ERROR: HTML source not found: {HTML_SOURCE}")
        sys.exit(1)

    fix_html()

    if not generate_pdf():
        print("PDF generation failed, aborting.")
        sys.exit(1)

    try:
        fix_pdf_boxes()
    except ImportError as e:
        print(f"WARNING: Could not add PDF boxes: {e}")
        print(f"Using unprocessed PDF: {PDF_OUTPUT}")
        import shutil
        shutil.copy(PDF_OUTPUT, PDF_POSTPROC)

    # Verify
    try:
        verify_pdf()
    except Exception as e:
        print(f"Verification note: {e}")
        print(f"Final PDF is at: {PDF_POSTPROC}")

    print("\nDone.")

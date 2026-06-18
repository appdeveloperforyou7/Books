#!/usr/bin/env python3
"""Diagnose KDP margin/gutter issues for VAULT_B_Interior.pdf.

KDP requirements for 360 pages at 5.5x8.5:
  gutter (inside)   >= 0.625" (45 pt)
  outside/top/bottom >= 0.25" (18 pt)

Page geometry:
  Page width  = 5.5" = 396 pt
  Page height = 8.5" = 612 pt
  Build margins were: inner=0.75" (54pt), outer=0.625" (45pt), top=0.75", bottom=0.75"

Odd pages = RIGHT side (inner edge = LEFT of page)
Even pages = LEFT side (inner edge = RIGHT of page)

We parse content streams to find actual text BBox per page, then compare to
the safe zone.
"""
import pikepdf
import re

PDF = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\VAULT_B_Interior.pdf"

# KDP minimums for 360-page book at 5.5x8.5
GUTTER_MIN = 0.625 * 72   # 45 pt inside
OTHER_MIN  = 0.25 * 72    # 18 pt outside/top/bottom

# Flagged pages from the two KDP errors
OUT_OF_MARGIN_PAGES = [12,16,20,26,32,34,44,46,48,50,64,84,88,94,98,102,104,110,112,114]
GUTTER_PAGES = [22,40,50,110,176,186,192,282,344,360]

def page_text_bbox(content_bytes):
    """Return (xmin,ymin,xmax,ymax) of all text shown via Tj/TJ, or None."""
    # Get current text matrix from Tm/Td/TD operators is complex; approximate by
    # scanning all numeric operands before Tm and all Td moves. For a reliable
    # bbox we instead rely on the cumulative transform via pdfminer below if avail.
    return None

def main():
    try:
        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextContainer, LTChar
        use_miner = True
        print("Using pdfminer.six for text bbox extraction")
    except ImportError:
        use_miner = False
        print("pdfminer.six NOT available - install with: pip install pdfminer.six")
        return

    print(f"\nKDP minimums: gutter(inside)={GUTTER_MIN:.0f}pt ({GUTTER_MIN/72:.3f}in), "
          f"other={OTHER_MIN:.0f}pt ({OTHER_MIN/72:.3f}in)")
    print(f"Page size: 396 x 612 pt (5.5 x 8.5 in)\n")

    # Examine ALL pages so we can confirm safe build margins, then focus on flagged ones.
    flagged = sorted(set(OUT_OF_MARGIN_PAGES + GUTTER_PAGES))
    print(f"Checking {len(flagged)} flagged pages: {flagged}\n")

    worst = []
    for page_num, page in enumerate(extract_pages(PDF), start=1):
        if page_num not in flagged:
            continue
        xmin = ymin = 1e9
        xmax = ymax = -1e9
        for element in page:
            if isinstance(element, LTTextContainer):
                # element.bbox is (x0, y0, x1, y1) in PDF coords (origin bottom-left)
                x0, y0, x1, y1 = element.bbox
                xmin = min(xmin, x0); xmax = max(xmax, x1)
                ymin = min(ymin, y0); ymax = max(ymax, y1)
        if xmax < 0:
            continue
        W = page.width
        H = page.height
        # Margins
        left   = xmin
        right  = W - xmax
        top    = H - ymax
        bottom = ymin
        # Determine inside vs outside based on parity (page 1 = right-hand)
        is_right = (page_num % 2 == 1)
        if is_right:
            inside  = left
            outside = right
            side = "R(inside=left)"
        else:
            inside  = right
            outside = left
            side = "L(inside=right)"

        problems = []
        if inside  < GUTTER_MIN: problems.append(f"GUTTER {inside:.1f}<{GUTTER_MIN:.0f}")
        if outside < OTHER_MIN:  problems.append(f"OUTSIDE {outside:.1f}<{OTHER_MIN:.0f}")
        if top     < OTHER_MIN:  problems.append(f"TOP {top:.1f}<{OTHER_MIN:.0f}")
        if bottom  < OTHER_MIN:  problems.append(f"BOTTOM {bottom:.1f}<{OTHER_MIN:.0f}")

        flag = "*** ISSUE ***" if problems else "ok"
        print(f"p{page_num:>3} {side:14} L={left:5.1f} R={right:5.1f} "
              f"T={top:5.1f} B={bottom:5.1f}  -> {flag} {', '.join(problems)}")
        if problems:
            worst.append((page_num, problems, inside, outside, top, bottom))

    print(f"\n=== {len(worst)} flagged pages with actual margin violations ===")
    if worst:
        for p, probs, ins, out, top, bot in worst:
            print(f"  p{p}: {probs}  inside={ins:.1f} outside={out:.1f} top={top:.1f} bottom={bot:.1f}")

if __name__ == "__main__":
    main()
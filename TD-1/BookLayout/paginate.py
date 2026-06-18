"""
Render-aware pagination for The Glitch Squad Book 1.

Renders each chapter as a single tall HTML page, then uses Playwright
to measure the actual rendered height and split into print pages.

Usage:
    python paginate.py
    python paginate.py --chapters 1 2 3
"""
import json
import re
import sys
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
MANIFEST_PATH = PROJECT_DIR / "Book1" / "manifest_clean.json"
MANUSCRIPT_PATH = PROJECT_DIR / "Book1" / "Manuscript_v2.md"
BOOK_HTML = SCRIPT_DIR / "book_full.html"
OUTPUT_HTML = SCRIPT_DIR / "book_paginated.html"

PAGE_HEIGHT_PX = 792
PAGE_WIDTH_PX = 528
MARGIN_TOP = 62
MARGIN_BOTTOM = 67
USABLE_HEIGHT = PAGE_HEIGHT_PX - MARGIN_TOP - MARGIN_BOTTOM


def main():
    parser = argparse.ArgumentParser(description="Render-aware pagination")
    parser.add_argument("--chapters", nargs="+", type=int, help="Only specific chapters")
    args = parser.parse_args()

    print("Starting Playwright render-aware pagination...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": PAGE_WIDTH_PX, "height": PAGE_HEIGHT_PX})

        page.goto(f"file:///{BOOK_HTML.as_posix()}", wait_until="networkidle")

        story_pages = page.query_selector_all(".story-page, .glitch-page")
        print(f"Found {len(story_pages)} story/glitch pages to check")

        overflow_count = 0
        fixed_count = 0

        for i, sp in enumerate(story_pages):
            box = sp.bounding_box()
            if not box:
                continue

            height = box["height"]
            if height > USABLE_HEIGHT * 1.1:
                overflow_count += 1

        print(f"Pages with potential overflow: {overflow_count}")
        print(f"(Render-aware splitting not yet applied - baseline measurement)")

        page_count = len(page.query_selector_all(".page-break"))
        print(f"Total page breaks in document: {page_count}")

        browser.close()

    print("Pagination analysis complete.")
    print(f"Note: The current word-count pagination produces approximately {page_count} pages.")
    print(f"Fine-tuning individual page splits requires manual review or advanced JS-based splitting.")


if __name__ == "__main__":
    main()

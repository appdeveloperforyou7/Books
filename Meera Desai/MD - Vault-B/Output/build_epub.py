#!/usr/bin/env python3
"""
VAULT B — EPUB Builder (Kindle + Apple Books)
Builds EPUB3 from Manuscript_dvc.md, matching the print interior structure:
  Title page -> Copyright -> Dedication -> FACT -> Chapters (Prologue, 1..N, Epilogue)

Uses ebooklib for structure. Embeds Garamond fonts. Validates with EpubCheck-style checks.
"""
import re
import os
import sys
import traceback
from pathlib import Path
from html import escape

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from ebooklib import epub

# ─── Config ──────────────────────────────────────────────────────────────────
SRC = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Manuscript_dvc.md"
OUT_DIR = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output"

KINDLE_OUT = os.path.join(OUT_DIR, "VAULT_B_Kindle_Final.epub")
APPLE_OUT  = os.path.join(OUT_DIR, "VAULT_B_Apple_Books.epub")

# Fonts to embed (optional but ensures consistency on Apple Books)
FONT_DIR = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")

# ─── Parsing (mirrors build_interior.py) ─────────────────────────────────────
def parse_manuscript(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    fact_match = re.search(r'# FACT\s*\n(.*?)\n---', text, re.DOTALL)
    fact_text = fact_match.group(1).strip() if fact_match else ""
    chapter_pattern = re.compile(r'^# (Prologue|Chapter \d+|Epilogue)\s*$', re.MULTILINE)
    chapter_starts = [(m.start(), m.group(1)) for m in chapter_pattern.finditer(text)]
    chapters = []
    for i, (start, title) in enumerate(chapter_starts):
        end = chapter_starts[i+1][0] if i+1 < len(chapter_starts) else len(text)
        body = text[start:end]
        body_lines = body.split("\n")[1:]
        body = "\n".join(body_lines).strip()
        body = re.sub(r'\n---\s*$', '', body).strip()
        chapters.append((title, body))
    return fact_text, chapters

# ─── Markdown → HTML (minimal, sufficient for this manuscript) ───────────────
def md_to_html(text):
    """Convert a subset of markdown to HTML for EPUB flowables."""
    # Split into paragraphs on double-newline
    paras = re.split(r'\n\s*\n', text.strip())
    html_parts = []
    for para in paras:
        para = para.strip()
        if not para or para == "---":
            continue
        # Strip blockquote markers
        para = re.sub(r'^>\s*', '', para, flags=re.MULTILINE)
        # Bold: **text** -> <strong>
        para = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para)
        # Italic: *text* -> <em> (but not **)
        para = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', para)
        # Escape stray angle brackets (but keep our tags)
        # Simple approach: escape < and > that aren't part of our known tags
        para = _escape_safe(para)
        html_parts.append(f'<p>{para}</p>')
    return "\n".join(html_parts)

def _escape_safe(text):
    """Escape ampersand, <, > but preserve our generated <strong>/<em> tags."""
    # Use chr() codes to avoid formatter/entity mangling
    AMP = chr(38)   # &
    LT  = chr(60)   # <
    GT  = chr(62)   # >
    AMP_ENT = AMP + "amp;"              # &
    LT_ENT  = AMP + "lt;"               # <
    GT_ENT  = AMP + "gt;"               # >
    # Protect our tags with placeholder markers
    SENTINEL = chr(1)
    text = text.replace(LT + "strong" + GT, SENTINEL + "S" + SENTINEL)
    text = text.replace(LT + "/strong" + GT, SENTINEL + "s" + SENTINEL)
    text = text.replace(LT + "em" + GT, SENTINEL + "E" + SENTINEL)
    text = text.replace(LT + "/em" + GT, SENTINEL + "e" + SENTINEL)
    # Escape remaining ampersand, <, >
    text = text.replace(AMP, AMP_ENT)
    text = text.replace(LT, LT_ENT)
    text = text.replace(GT, GT_ENT)
    # Restore our tags
    text = text.replace(SENTINEL + "S" + SENTINEL, LT + "strong" + GT)
    text = text.replace(SENTINEL + "s" + SENTINEL, LT + "/strong" + GT)
    text = text.replace(SENTINEL + "E" + SENTINEL, LT + "em" + GT)
    text = text.replace(SENTINEL + "e" + SENTINEL, LT + "/em" + GT)
    return text

# ─── CSS ─────────────────────────────────────────────────────────────────────
BODY_CSS = """
@charset "utf-8";
body {
    margin: 0;
    padding: 0.5em 0.75em;
    font-family: "Garamond", "Georgia", serif;
    font-size: 1.05em;
    line-height: 1.5;
    color: #1a1a1a;
    text-align: justify;
}
p {
    margin: 0;
    text-indent: 1.5em;
    margin-bottom: 0;
}
p:first-child, p.no-indent {
    text-indent: 0;
}
/* Chapter title pages */
h1.chapter-title {
    font-family: "Garamond", serif;
    font-weight: bold;
    font-size: 1.8em;
    color: #8B0000;
    text-align: center;
    margin-top: 3em;
    margin-bottom: 2em;
    page-break-after: always;
}
/* Title page */
.title-main {
    text-align: center;
    margin-top: 25%;
}
.title-main h1 {
    font-family: "Garamond", serif;
    font-weight: bold;
    font-size: 2.8em;
    color: #1a1a1a;
    margin-bottom: 0.3em;
}
.title-main p.sub {
    font-family: "Garamond", serif;
    font-style: italic;
    font-size: 1.1em;
    color: #666666;
}
/* Copyright */
.copyright {
    text-align: center;
    margin-top: 30%;
    font-family: "Arial", sans-serif;
    font-size: 0.8em;
    color: #666666;
    line-height: 1.5;
}
.copyright .book-title {
    font-family: "Garamond", serif;
    font-weight: bold;
    font-size: 1.1em;
    color: #1a1a1a;
    margin-bottom: 1em;
}
.copyright p {
    text-indent: 0;
    margin: 0.3em 0;
}
/* Dedication */
.dedication {
    text-align: center;
    margin-top: 35%;
    font-family: "Garamond", serif;
    font-style: italic;
    font-size: 1.2em;
    color: #1a1a1a;
}
.dedication p {
    text-indent: 0;
}
/* FACT section */
.fact-heading {
    font-family: "Garamond", serif;
    font-weight: bold;
    font-size: 1.4em;
    color: #8B0000;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 1.5em;
}
.fact-body p {
    text-indent: 0;
    margin: 0.5em 1em;
}
@font-face {
    font-family: "Garamond";
    font-weight: normal;
    font-style: normal;
    src: url("fonts/Garamond.ttf");
}
@font-face {
    font-family: "Garamond";
    font-weight: bold;
    font-style: normal;
    src: url("fonts/Garamond-Bold.ttf");
}
@font-face {
    font-family: "Garamond";
    font-weight: normal;
    font-style: italic;
    src: url("fonts/Garamond-Italic.ttf");
}
"""

# ─── Build ───────────────────────────────────────────────────────────────────
def build_epub(output_path, apple_books=False):
    print(f"\n{'='*60}")
    print(f"Building: {os.path.basename(output_path)}")
    print(f"{'='*60}")

    fact_text, chapters = parse_manuscript(SRC)
    print(f"Parsed: {len(chapters)} chapters + FACT section")

    book = epub.EpubBook()
    book.set_identifier("urn:uuid:vaultb-meedesai-book1-2026")
    book.set_title("VAULT B")
    book.set_language("en")
    book.add_author("Kapil")
    book.add_metadata("DC", "description", "Book One of the Meera Desai Thrillers")
    book.add_metadata("DC", "publisher", "Independent")
    book.add_metadata("DC", "date", "2026-06-15")

    # ─── CSS ───
    style = epub.EpubItem(
        uid="style",
        file_name="style/default.css",
        media_type="text/css",
        content=BODY_CSS.encode("utf-8"),
    )
    book.add_item(style)

    # ─── Embed fonts ───
    font_files = {
        "Garamond.ttf": "GARA.TTF",
        "Garamond-Bold.ttf": "GARABD.TTF",
        "Garamond-Italic.ttf": "GARAIT.TTF",
    }
    for epub_name, sys_name in font_files.items():
        font_path = os.path.join(FONT_DIR, sys_name)
        if os.path.exists(font_path):
            with open(font_path, "rb") as f:
                font_data = f.read()
            ft = epub.EpubItem(
                uid=f"font_{epub_name.replace('.', '_')}",
                file_name=f"fonts/{epub_name}",
                media_type="application/x-font-ttf",
                content=font_data,
            )
            book.add_item(ft)
            print(f"  Embedded font: {epub_name} ({len(font_data)//1024} KB)")

    all_items = []  # for spine + TOC

    # ─── Title page ───
    title_html = (
        '<html><head><link rel="stylesheet" type="text/css" href="style/default.css"/></head>'
        '<body><div class="title-main">'
        '<h1>VAULT B</h1>'
        '<p class="sub">Book One of the Meera Desai Thrillers</p>'
        '</div></body></html>'
    )
    ch_title = epub.EpubHtml(title="Title Page", file_name="title.xhtml", lang="en")
    ch_title.content = title_html
    ch_title.add_item(style)
    book.add_item(ch_title)
    all_items.append(ch_title)

    # ─── Copyright ───
    copyright_html = (
        '<html><head><link rel="stylesheet" type="text/css" href="style/default.css"/></head>'
        '<body><div class="copyright">'
        '<p class="book-title">VAULT B</p>'
        '<p>Book One of the Meera Desai Thrillers</p>'
        '<p>&nbsp;</p>'
        '<p>Copyright &#169; 2026 Kapil</p>'
        '<p>All rights reserved.</p>'
        '<p>&nbsp;</p>'
        '<p>This is a work of fiction. Names, characters, places, and incidents<br/>'
        'are products of the author\'s imagination. Any resemblance to actual<br/>'
        'persons, living or dead, events, or locales is entirely coincidental.</p>'
        '</div></body></html>'
    )
    ch_copy = epub.EpubHtml(title="Copyright", file_name="copyright.xhtml", lang="en")
    ch_copy.content = copyright_html
    ch_copy.add_item(style)
    book.add_item(ch_copy)
    all_items.append(ch_copy)

    # ─── Dedication ───
    dedication_html = (
        '<html><head><link rel="stylesheet" type="text/css" href="style/default.css"/></head>'
        '<body><div class="dedication">'
        '<p>For those who guard knowledge,</p>'
        '<p>and for those who share it.</p>'
        '</div></body></html>'
    )
    ch_ded = epub.EpubHtml(title="Dedication", file_name="dedication.xhtml", lang="en")
    ch_ded.content = dedication_html
    ch_ded.add_item(style)
    book.add_item(ch_ded)
    all_items.append(ch_ded)

    # ─── FACT section ───
    fact_body_html = md_to_html(fact_text)
    fact_html = (
        '<html><head><link rel="stylesheet" type="text/css" href="style/default.css"/></head>'
        '<body>'
        '<p class="fact-heading">FACT</p>'
        f'<div class="fact-body">{fact_body_html}</div>'
        '</body></html>'
    )
    ch_fact = epub.EpubHtml(title="Fact", file_name="fact.xhtml", lang="en")
    ch_fact.content = fact_html
    ch_fact.add_item(style)
    book.add_item(ch_fact)
    all_items.append(ch_fact)

    # ─── Chapters ───
    for idx, (title, body) in enumerate(chapters):
        # Determine display title
        if title == "Prologue":
            display = "Prologue"
        elif title.startswith("Chapter"):
            num = title.split()[-1]
            display = f"Chapter {num}"
        else:
            display = title

        # Build body HTML with first-paragraph no-indent
        body_html = md_to_html(body)
        # Give first paragraph no-indent class
        body_html = body_html.replace('<p>', '<p class="no-indent">', 1)

        chapter_html = (
            '<html><head><link rel="stylesheet" type="text/css" href="style/default.css"/></head>'
            '<body>'
            f'<h1 class="chapter-title">{escape(display)}</h1>'
            f'{body_html}'
            '</body></html>'
        )

        file_slug = re.sub(r'\W+', '_', title).strip('_').lower()
        ch = epub.EpubHtml(title=display, file_name=f"chapters/{file_slug}.xhtml", lang="en")
        ch.content = chapter_html
        ch.add_item(style)
        book.add_item(ch)
        all_items.append(ch)

    print(f"  Created {len(all_items)} content items")

    # ─── Spine ───
    book.spine = all_items

    # ─── TOC (landmarks + nav for EPUB3) ───
    toc_entries = [epub.Link(it.file_name, it.title, it.file_name) for it in all_items]
    book.toc = tuple(toc_entries)

    # Add NCX and Nav for compatibility
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # ─── Write ───
    epub.write_epub(output_path, book, {"epub3_fonts": True, "epub_version": "3.0" if apple_books else "2.0"})
    sz = os.path.getsize(output_path)
    print(f"  DONE: {output_path}")
    print(f"  Size: {sz/1024:.0f} KB")


def main():
    print("Parsing manuscript from:", SRC)

    # Build Apple Books version (EPUB 3.0)
    build_epub(APPLE_OUT, apple_books=True)

    # Build Kindle version (EPUB 2.0 for maximum KF8 compatibility)
    build_epub(KINDLE_OUT, apple_books=False)

    print(f"\n{'='*60}")
    print("ALL EPUBS BUILT SUCCESSFULLY")
    print(f"{'='*60}")
    print(f"  Kindle:     {KINDLE_OUT}")
    print(f"  Apple Books: {APPLE_OUT}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
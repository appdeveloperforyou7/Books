import os
import re
from ebooklib import epub

BASE = r"D:\Kapil\Books\The Fourth Step"
CHAPTERS_DIR = os.path.join(BASE, "Chapters")
OUTPUT_PATH = os.path.join(BASE, "Output", "The_Fourth_Step_Kindle.epub")

PARTS = [
    {"title": "THE ARRIVAL", "range": (0, 8), "number": "ONE"},
    {"title": "THE MEMORY", "range": (8, 17), "number": "TWO"},
    {"title": "THE CONFESSION", "range": (17, 25), "number": "THREE"},
    {"title": "THE STEP", "range": (25, 31), "number": "FOUR"},
]

CHAPTER_ORDER = [
    "prologue.md",
    "chapter-01-neve.md", "chapter-02-saskia.md", "chapter-03-imogen.md",
    "chapter-04-rowan.md", "chapter-05-neve.md", "chapter-06-saskia.md",
    "chapter-07-imogen.md", "chapter-08-rowan.md", "chapter-09-neve.md",
    "chapter-10-saskia.md", "chapter-11-imogen.md", "chapter-12-rowan.md",
    "chapter-13-neve.md", "chapter-14-saskia.md", "chapter-15-imogen.md",
    "chapter-16-neve.md", "chapter-17-saskia.md", "chapter-18-imogen.md",
    "chapter-19-rowan.md", "chapter-20-saskia.md", "chapter-21-aisling.md",
    "chapter-22-neve.md", "chapter-23-saskia.md", "chapter-24-neve.md",
    "chapter-25-neve.md", "chapter-26-neve.md", "chapter-27-saskia.md",
    "chapter-28-neve.md", "chapter-29-neve.md",
    "epilogue-neve.md",
]

CSS = """
body {
    font-family: Georgia, 'Times New Roman', serif;
    line-height: 1.5;
    margin: 1em;
    color: #1a1a1a;
}
h1 {
    font-size: 1.4em;
    text-align: center;
    margin-top: 2.5em;
    margin-bottom: 0.3em;
    letter-spacing: 0.15em;
    color: #333;
    page-break-before: always;
}
h1.part-title {
    font-size: 1.6em;
    margin-top: 35%;
    color: #333;
}
h1.part-number {
    font-size: 0.9em;
    letter-spacing: 0.2em;
    color: #888;
    margin-bottom: 0.5em;
    page-break-before: always;
}
h2 {
    font-size: 1.1em;
    font-style: italic;
    color: #888;
    margin-top: 2em;
    margin-bottom: 1.5em;
    letter-spacing: 0.1em;
}
h3 {
    font-size: 0.95em;
    font-style: italic;
    color: #555;
    margin-top: 1.8em;
    margin-bottom: 1em;
    text-align: center;
}
p {
    text-indent: 1.5em;
    margin: 0;
}
p.no-indent {
    text-indent: 0;
}
p.tagline {
    text-indent: 0;
    text-align: center;
    font-style: italic;
    font-size: 0.95em;
    color: #555;
    margin: 1em 0;
}
p.dedication {
    text-indent: 0;
    text-align: center;
    font-style: italic;
    margin-top: 30%;
    color: #444;
}
p.copyright {
    text-indent: 0;
    font-size: 0.8em;
    color: #666;
    margin: 0.3em 0;
    text-align: center;
}
blockquote {
    font-style: italic;
    margin: 0.8em 2em;
    color: #444;
}
blockquote p {
    text-indent: 0;
    margin: 0.3em 0;
}
.scene-break {
    text-align: center;
    margin: 1.5em 0;
    color: #999;
}
.title-page-title {
    text-align: center;
    font-size: 2em;
    font-weight: bold;
    margin-top: 25%;
    margin-bottom: 0.3em;
    page-break-before: avoid;
}
.title-page-author {
    text-align: center;
    font-size: 1em;
    letter-spacing: 0.15em;
    color: #555;
    margin-top: 1em;
}
"""


def format_text(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text


def parse_chapter(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    header_line = lines[0].strip() if lines else ""
    is_prologue = "Prologue" in header_line
    is_epilogue = "Epilogue" in header_line
    is_chapter = not is_prologue and not is_epilogue

    chapter_info = {"prologue": is_prologue, "epilogue": is_epilogue}
    if is_chapter:
        m = re.match(r"# THE FOURTH STEP — Chapter (\d+): (.+)", header_line)
        if m:
            chapter_info["number"] = int(m.group(1))
            chapter_info["pov"] = m.group(2)

    content_lines = lines[1:]
    elements = []
    current_para = []

    i = 0
    while i < len(content_lines):
        line = content_lines[i].rstrip("\n").rstrip("\r")
        stripped = line.strip()

        if stripped.startswith("## "):
            if current_para:
                text = " ".join(current_para)
                if text.strip():
                    elements.append(("paragraph", text))
                current_para = []
            elements.append(("scene", stripped[3:].strip()))
            i += 1
            continue

        if stripped == "---":
            if current_para:
                text = " ".join(current_para)
                if text.strip():
                    elements.append(("paragraph", text))
                current_para = []
            elements.append(("break",))
            i += 1
            continue

        if stripped.startswith("*") and not stripped.startswith("**") and "\u2014" in stripped and len(stripped) > 40:
            if current_para:
                text = " ".join(current_para)
                if text.strip():
                    elements.append(("paragraph", text))
                current_para = []
            block_lines = [stripped]
            i += 1
            while i < len(content_lines):
                next_line = content_lines[i].strip()
                if next_line.startswith("*") and not next_line.startswith("**"):
                    block_lines.append(next_line)
                    i += 1
                else:
                    break
            for bl in block_lines:
                if bl.startswith("*") and bl.endswith("*") and len(bl) > 2:
                    clean = bl[1:-1]
                else:
                    clean = bl
                elements.append(("blockquote", clean.strip()))
            continue

        if stripped.startswith("*") and stripped.endswith("*") and len(stripped) > 2 and not stripped.startswith("**"):
            if current_para:
                text = " ".join(current_para)
                if text.strip():
                    elements.append(("paragraph", text))
                current_para = []
            clean = stripped[1:-1]
            elements.append(("blockquote", clean.strip()))
            i += 1
            continue

        if stripped == "":
            if current_para:
                text = " ".join(current_para)
                if text.strip():
                    elements.append(("paragraph", text))
                current_para = []
            i += 1
            continue

        current_para.append(stripped)
        i += 1

    if current_para:
        text = " ".join(current_para)
        if text.strip():
            elements.append(("paragraph", text))

    return chapter_info, elements


def elements_to_html(elements, chapter_info):
    html_parts = []
    is_prologue = chapter_info.get("prologue", False)
    is_epilogue = chapter_info.get("epilogue", False)

    if is_prologue:
        html_parts.append('<h1>PROLOGUE</h1>')
    elif is_epilogue:
        html_parts.append('<h1>EPILOGUE</h1>')
    else:
        num = chapter_info.get("number", "")
        pov = chapter_info.get("pov", "")
        html_parts.append(f'<h2>Chapter {num} — {pov}</h2>')

    for el in elements:
        if el[0] == "scene":
            html_parts.append(f'<h3>{format_text(el[1])}</h3>')
        elif el[0] == "break":
            html_parts.append('<p class="scene-break">* * *</p>')
        elif el[0] == "blockquote":
            html_parts.append(f'<blockquote><p>{format_text(el[1])}</p></blockquote>')
        elif el[0] == "paragraph":
            html_parts.append(f'<p>{format_text(el[1])}</p>')

    return "\n".join(html_parts)


def get_part_for_chapter_index(idx):
    for part in PARTS:
        if part["range"][0] <= idx < part["range"][1]:
            return part
    return None


def main():
    print("=" * 60)
    print("THE FOURTH STEP — EPUB Generator")
    print("=" * 60)

    book = epub.EpubBook()
    book.set_identifier("the-fourth-step-kapil-gupta-2026")
    book.set_title("The Fourth Step")
    book.set_language("en")
    book.add_author("Kapil Gupta")
    book.add_metadata("DC", "description", "Some houses don't forget. They wait.")
    book.add_metadata("DC", "subject", "Fiction")
    book.add_metadata("DC", "subject", "Psychological Thriller")
    book.add_metadata("DC", "publisher", "Kapil Gupta")
    book.add_metadata("DC", "rights", "Copyright 2026 Kapil Gupta. All rights reserved.")

    style = epub.EpubItem(
        uid="style",
        file_name="style/default.css",
        media_type="text/css",
        content=CSS.encode("utf-8"),
    )
    book.add_item(style)

    toc = []
    spine = ["nav"]

    title_chapter = epub.EpubHtml(
        title="Title Page",
        file_name="title.xhtml",
        lang="en",
    )
    title_chapter.content = """<html><body>
<p class="title-page-title">THE FOURTH STEP</p>
<p class="title-page-author">KAPIL GUPTA</p>
</body></html>"""
    title_chapter.add_item(style)
    book.add_item(title_chapter)
    spine.append(title_chapter)

    copyright_chapter = epub.EpubHtml(
        title="Copyright",
        file_name="copyright.xhtml",
        lang="en",
    )
    copyright_chapter.content = """<html><body>
<p class="copyright">The Fourth Step</p>
<p class="copyright">Copyright &copy; 2026 Kapil Gupta. All rights reserved.</p>
<p class="copyright">All rights reserved. No part of this publication may be reproduced,</p>
<p class="copyright">distributed, or transmitted in any form or by any means</p>
<p class="copyright">without the prior written permission of the publisher,</p>
<p class="copyright">except in the case of brief quotations embodied in critical reviews.</p>
<p class="copyright">This is a work of fiction. Names, characters, places, and incidents</p>
<p class="copyright">are the product of the author's imagination or are used fictitiously.</p>
<p class="copyright">Any resemblance to actual persons, living or dead, events, or locales</p>
<p class="copyright">is entirely coincidental.</p>
<p class="copyright">First Edition</p>
<p class="copyright">Published in Australia</p>
</body></html>"""
    copyright_chapter.add_item(style)
    book.add_item(copyright_chapter)
    spine.append(copyright_chapter)

    dedication_chapter = epub.EpubHtml(
        title="Dedication",
        file_name="dedication.xhtml",
        lang="en",
    )
    dedication_chapter.content = """<html><body>
<p class="dedication">For those who remember what they'd rather forget.</p>
</body></html>"""
    dedication_chapter.add_item(style)
    book.add_item(dedication_chapter)
    spine.append(dedication_chapter)

    epigraph_chapter = epub.EpubHtml(
        title="Epigraph",
        file_name="epigraph.xhtml",
        lang="en",
    )
    epigraph_chapter.content = """<html><body>
<blockquote>
<p><em>The truth is rarely pure and never simple.</em></p>
<p>&#8212; Oscar Wilde, The Importance of Being Earnest</p>
</blockquote>
</body></html>"""
    epigraph_chapter.add_item(style)
    book.add_item(epigraph_chapter)
    spine.append(epigraph_chapter)

    current_part = None
    part_counter = 0
    part_chapters = []

    for idx, chapter_file in enumerate(CHAPTER_ORDER):
        filepath = os.path.join(CHAPTERS_DIR, chapter_file)
        if not os.path.isfile(filepath):
            print(f"  WARNING: {chapter_file} not found")
            continue

        part = get_part_for_chapter_index(idx)
        if part and part is not current_part:
            current_part = part
            part_counter += 1

            part_ch = epub.EpubHtml(
                title=f"Part {part['number']}: {part['title']}",
                file_name=f"part_{part_counter}.xhtml",
                lang="en",
            )
            part_ch.content = f"""<html><body>
<h1 class="part-number">PART {part['number']}</h1>
<h1 class="part-title">{part['title']}</h1>
</body></html>"""
            part_ch.add_item(style)
            book.add_item(part_ch)
            spine.append(part_ch)

        chapter_info, elements = parse_chapter(filepath)
        is_prologue = chapter_info.get("prologue", False)
        is_epilogue = chapter_info.get("epilogue", False)

        if is_prologue:
            ch_title = "Prologue"
            fname = "prologue.xhtml"
        elif is_epilogue:
            ch_title = "Epilogue"
            fname = "epilogue_chapter.xhtml"
        else:
            num = chapter_info.get("number", idx)
            ch_title = f"Chapter {num}"
            fname = f"chapter_{num:02d}.xhtml"

        chapter_html = elements_to_html(elements, chapter_info)
        epub_chapter = epub.EpubHtml(
            title=ch_title,
            file_name=fname,
            lang="en",
        )
        epub_chapter.content = f"<html><body>\n{chapter_html}\n</body></html>"
        epub_chapter.add_item(style)
        book.add_item(epub_chapter)
        spine.append(epub_chapter)
        part_chapters.append(epub_chapter)

    if part_chapters:
        toc.extend(part_chapters)

    book.toc = toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine

    epub.write_epub(OUTPUT_PATH, book, {})
    fsize = os.path.getsize(OUTPUT_PATH)
    print(f"  Output: {OUTPUT_PATH}")
    print(f"  Size: {fsize / 1024:.0f} KB")
    print("  Done.")


if __name__ == "__main__":
    main()

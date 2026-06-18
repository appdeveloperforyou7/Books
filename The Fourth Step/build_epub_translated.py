import os
import re
from ebooklib import epub

BASE = r"D:\Kapil\Books\The Fourth Step"

LANGUAGES = [
    {
        "name": "Spanish",
        "lang_code": "es",
        "chapters_dir": os.path.join(BASE, "Spanish", "Chapters"),
        "output_path": os.path.join(BASE, "Spanish", "El_Cuarto_Escalon_Spanish_Kindle.epub"),
        "title": "El Cuarto Escalón",
        "subtitle": "Una novela",
        "author": "Kapil Gupta",
        "identifier": "el-cuarto-escalon-kapil-gupta-2026-es",
        "description": "Algunas casas no olvidan. Esperan.",
        "chapter_order": [
            "prologo.md",
            "capitulo-01-neve.md", "capitulo-02-saskia.md", "capitulo-03-imogen.md",
            "capitulo-04-rowan.md", "capitulo-05-neve.md", "capitulo-06-saskia.md",
            "capitulo-07-imogen.md", "capitulo-08-rowan.md", "capitulo-09-neve.md",
            "capitulo-10-saskia.md", "capitulo-11-imogen.md", "capitulo-12-rowan.md",
            "capitulo-13-neve.md", "capitulo-14-saskia.md", "capitulo-15-imogen.md",
            "capitulo-16-neve.md", "capitulo-17-saskia.md", "capitulo-18-imogen.md",
            "capitulo-19-rowan.md", "capitulo-20-saskia.md", "capitulo-21-aisling.md",
            "capitulo-22-neve.md", "capitulo-23-saskia.md", "capitulo-24-neve.md",
            "capitulo-25-neve.md", "capitulo-26-neve.md", "capitulo-27-saskia.md",
            "capitulo-28-neve.md", "capitulo-29-neve.md",
            "epilogo-neve.md",
        ],
        "parts": [
            {"title": "LA LLEGADA", "range": (0, 8), "number": "UNO"},
            {"title": "EL RECUERDO", "range": (8, 17), "number": "DOS"},
            {"title": "LA CONFESIÓN", "range": (17, 25), "number": "TRES"},
            {"title": "EL ESCALÓN", "range": (25, 31), "number": "CUATRO"},
        ],
        "front_matter": {
            "title_page": '<p class="title-page-title">EL CUARTO ESCALÓN</p>\n<p class="title-page-author">KAPIL GUPTA</p>',
            "copyright": [
                "El Cuarto Escalón",
                "Copyright © 2026 Kapil Gupta. Todos los derechos reservados.",
                "Ninguna parte de esta publicación puede ser reproducida, distribuida o transmitida",
                "de cualquier forma o por cualquier medio sin el permiso previo por escrito del editor.",
                "Esta es una obra de ficción. Los nombres, personajes, lugares e incidentes son",
                "producto de la imaginación del autor o se utilizan de forma ficticia.",
                "Cualquier parecido con personas reales es enteramente coincidental.",
                "Primera edición",
                "Publicado en Australia",
            ],
            "dedication": "Para los que recuerdan.",
        },
        "header_re": r"# .+? — Capítulo (\d+):?\s*(.+)",
        "prologue_label": "PRÓLOGO",
        "epilogue_label": "EPÍLOGO",
        "chapter_label": "Capítulo",
        "part_label": "PARTE",
    },
    {
        "name": "French",
        "lang_code": "fr",
        "chapters_dir": os.path.join(BASE, "French", "Chapters"),
        "output_path": os.path.join(BASE, "French", "Le_Quatrieme_Marcher_French_Kindle.epub"),
        "title": "Le Quatrième Marcher",
        "subtitle": "Un roman",
        "author": "Kapil Gupta",
        "identifier": "le-quatrieme-marcher-kapil-gupta-2026-fr",
        "description": "Certaines maisons n'oublient pas. Elles attendent.",
        "chapter_order": [
            "prologue.md",
            "chapitre-01-neve.md", "chapitre-02-saskia.md", "chapitre-03-imogen.md",
            "chapitre-04-rowan.md", "chapitre-05-neve.md", "chapitre-06-saskia.md",
            "chapitre-07-imogen.md", "chapitre-08-rowan.md", "chapitre-09-neve.md",
            "chapitre-10-saskia.md", "chapitre-11-imogen.md", "chapitre-12-rowan.md",
            "chapitre-13-neve.md", "chapitre-14-saskia.md", "chapitre-15-imogen.md",
            "chapitre-16-neve.md", "chapitre-17-saskia.md", "chapitre-18-imogen.md",
            "chapitre-19-rowan.md", "chapitre-20-saskia.md", "chapitre-21-aisling.md",
            "chapitre-22-neve.md", "chapitre-23-saskia.md", "chapitre-24-neve.md",
            "chapitre-25-neve.md", "chapitre-26-neve.md", "chapitre-27-saskia.md",
            "chapitre-28-neve.md", "chapitre-29-neve.md",
            "epilogue-neve.md",
        ],
        "parts": [
            {"title": "L'ARRIVÉE", "range": (0, 8), "number": "UN"},
            {"title": "LE SOUVENIR", "range": (8, 17), "number": "DEUX"},
            {"title": "LA CONFESSION", "range": (17, 25), "number": "TROIS"},
            {"title": "LA MARCHE", "range": (25, 31), "number": "QUATRE"},
        ],
        "front_matter": {
            "title_page": '<p class="title-page-title">LE QUATRIÈME MARCHER</p>\n<p class="title-page-author">KAPIL GUPTA</p>',
            "copyright": [
                "Le Quatrième Marcher",
                "Copyright © 2026 Kapil Gupta. Tous droits réservés.",
                "Aucune partie de cette publication ne peut être reproduite, distribuée ou transmise",
                "sans l'autorisation écrite préalable de l'éditeur.",
                "Ceci est une œuvre de fiction. Les noms, personnages, lieux et incidents sont",
                "soit le produit de l'imagination de l'auteur, soit utilisés de manière fictive.",
                "Toute ressemblance avec des personnes réelles est entièrement coïncidentale.",
                "Première édition",
                "Publié en Australie",
            ],
            "dedication": "Pour ceux qui se souviennent.",
        },
        "header_re": r"# .+? — Chapitre (\d+)\s*:?\s*(.+)",
        "prologue_label": "PROLOGUE",
        "epilogue_label": "ÉPILOGUE",
        "chapter_label": "Chapitre",
        "part_label": "PARTIE",
    },
    {
        "name": "German",
        "lang_code": "de",
        "chapters_dir": os.path.join(BASE, "German", "Chapters"),
        "output_path": os.path.join(BASE, "German", "Die_Vierte_Stufe_German_Kindle.epub"),
        "title": "Die Vierte Stufe",
        "subtitle": "Ein Roman",
        "author": "Kapil Gupta",
        "identifier": "die-vierte-stufe-kapil-gupta-2026-de",
        "description": "Manche Häuser vergessen nicht. Sie warten.",
        "chapter_order": [
            "prolog.md",
            "kapitel-01-neve.md", "kapitel-02-saskia.md", "kapitel-03-imogen.md",
            "kapitel-04-rowan.md", "kapitel-05-neve.md", "kapitel-06-saskia.md",
            "kapitel-07-imogen.md", "kapitel-08-rowan.md", "kapitel-09-neve.md",
            "kapitel-10-saskia.md", "kapitel-11-imogen.md", "kapitel-12-rowan.md",
            "kapitel-13-neve.md", "kapitel-14-saskia.md", "kapitel-15-imogen.md",
            "kapitel-16-neve.md", "kapitel-17-saskia.md", "kapitel-18-imogen.md",
            "kapitel-19-rowan.md", "kapitel-20-saskia.md", "kapitel-21-aisling.md",
            "kapitel-22-neve.md", "kapitel-23-saskia.md", "kapitel-24-neve.md",
            "kapitel-25-neve.md", "kapitel-26-neve.md", "kapitel-27-saskia.md",
            "kapitel-28-neve.md", "kapitel-29-neve.md",
            "epilog-neve.md",
        ],
        "parts": [
            {"title": "DIE ANKUNFT", "range": (0, 8), "number": "EINS"},
            {"title": "DIE ERINNERUNG", "range": (8, 17), "number": "ZWEI"},
            {"title": "DAS GESTÄNDNIS", "range": (17, 25), "number": "DREI"},
            {"title": "DIE STUFE", "range": (25, 31), "number": "VIER"},
        ],
        "front_matter": {
            "title_page": '<p class="title-page-title">DIE VIERTE STUFE</p>\n<p class="title-page-author">KAPIL GUPTA</p>',
            "copyright": [
                "Die Vierte Stufe",
                "Copyright © 2026 Kapil Gupta. Alle Rechte vorbehalten.",
                "Kein Teil dieser Veröffentlichung darf ohne vorherige schriftliche Genehmigung",
                "des Verlages in irgendeiner Form reproduziert oder übertragen werden.",
                "Dies ist ein Werk der Fiktion. Namen, Figuren, Orte und Vorfälle sind",
                "Produkt der Einbildungskraft des Autors oder fiktiv verwendet.",
                "Jede Ähnlichkeit mit tatsächlichen Personen ist völlig zufällig.",
                "Erste Auflage",
                "Veröffentlicht in Australien",
            ],
            "dedication": "Für diejenigen, die sich erinnern.",
        },
        "header_re": r"# .+? — Kapitel (\d+)\s*:?\s*(.+)",
        "prologue_label": "PROLOG",
        "epilogue_label": "EPILOG",
        "chapter_label": "Kapitel",
        "part_label": "TEIL",
    },
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


def parse_chapter(filepath, lang):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    header_line = lines[0].strip() if lines else ""
    is_prologue = "prologo" in filepath.lower() or "prologue" in filepath.lower() or "prolog" in filepath.lower() or "Prólogo" in header_line or "Prologue" in header_line or "Prolog" in header_line
    is_epilogue = "epilogo" in filepath.lower() or "epilogue" in filepath.lower() or "epilog" in filepath.lower() or "Epílogo" in header_line or "Épilogue" in header_line or "Epilog" in header_line
    is_chapter = not is_prologue and not is_epilogue

    chapter_info = {"prologue": is_prologue, "epilogue": is_epilogue}
    if is_chapter:
        m = re.match(lang["header_re"], header_line)
        if m:
            chapter_info["number"] = int(m.group(1))
            chapter_info["pov"] = m.group(2).strip()

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


def elements_to_html(elements, chapter_info, lang):
    html_parts = []
    is_prologue = chapter_info.get("prologue", False)
    is_epilogue = chapter_info.get("epilogue", False)

    if is_prologue:
        html_parts.append(f'<h1>{lang["prologue_label"]}</h1>')
    elif is_epilogue:
        html_parts.append(f'<h1>{lang["epilogue_label"]}</h1>')
    else:
        num = chapter_info.get("number", "")
        pov = chapter_info.get("pov", "")
        html_parts.append(f'<h2>{lang["chapter_label"]} {num} — {pov}</h2>')

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


def get_part_for_chapter_index(idx, parts):
    for part in parts:
        if part["range"][0] <= idx < part["range"][1]:
            return part
    return None


def build_epub(lang):
    name = lang["name"]
    print(f"\n{'='*50}")
    print(f"  {name} — EPUB Generator")
    print(f"{'='*50}")

    chapters_dir = lang["chapters_dir"]
    output_path = lang["output_path"]

    book = epub.EpubBook()
    book.set_identifier(lang["identifier"])
    book.set_title(lang["title"])
    book.set_language(lang["lang_code"])
    book.add_author(lang["author"])
    book.add_metadata("DC", "description", lang["description"])
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

    title_ch = epub.EpubHtml(title=lang["title"], file_name="title.xhtml", lang=lang["lang_code"])
    title_ch.content = f'<html><body>\n{lang["front_matter"]["title_page"]}\n</body></html>'
    title_ch.add_item(style)
    book.add_item(title_ch)
    spine.append(title_ch)

    copyright_lines = "\n".join(f'<p class="copyright">{line}</p>' for line in lang["front_matter"]["copyright"])
    copyright_ch = epub.EpubHtml(title="Copyright", file_name="copyright.xhtml", lang=lang["lang_code"])
    copyright_ch.content = f'<html><body>\n{copyright_lines}\n</body></html>'
    copyright_ch.add_item(style)
    book.add_item(copyright_ch)
    spine.append(copyright_ch)

    dedication_ch = epub.EpubHtml(title="Dedication", file_name="dedication.xhtml", lang=lang["lang_code"])
    dedication_ch.content = f'<html><body>\n<p class="dedication">{lang["front_matter"]["dedication"]}</p>\n</body></html>'
    dedication_ch.add_item(style)
    book.add_item(dedication_ch)
    spine.append(dedication_ch)

    current_part = None
    part_counter = 0
    part_chapters = []

    for idx, chapter_file in enumerate(lang["chapter_order"]):
        filepath = os.path.join(chapters_dir, chapter_file)
        if not os.path.isfile(filepath):
            print(f"  WARNING: {chapter_file} not found")
            continue

        part = get_part_for_chapter_index(idx, lang["parts"])
        if part and part is not current_part:
            current_part = part
            part_counter += 1
            part_ch = epub.EpubHtml(
                title=f"{lang['part_label']} {part['number']}: {part['title']}",
                file_name=f"part_{part_counter}.xhtml",
                lang=lang["lang_code"],
            )
            part_ch.content = f"""<html><body>
<h1 class="part-number">{lang['part_label']} {part['number']}</h1>
<h1 class="part-title">{part['title']}</h1>
</body></html>"""
            part_ch.add_item(style)
            book.add_item(part_ch)
            spine.append(part_ch)

        chapter_info, elements = parse_chapter(filepath, lang)
        is_prologue = chapter_info.get("prologue", False)
        is_epilogue = chapter_info.get("epilogue", False)

        if is_prologue:
            ch_title = lang["prologue_label"].capitalize()
            fname = "prologue.xhtml"
        elif is_epilogue:
            ch_title = lang["epilogue_label"].capitalize()
            fname = "epilogue_chapter.xhtml"
        else:
            num = chapter_info.get("number", idx)
            ch_title = f"{lang['chapter_label']} {num}"
            fname = f"chapter_{num:02d}.xhtml"

        chapter_html = elements_to_html(elements, chapter_info, lang)
        epub_chapter = epub.EpubHtml(title=ch_title, file_name=fname, lang=lang["lang_code"])
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

    epub.write_epub(output_path, book, {})
    fsize = os.path.getsize(output_path)
    print(f"  Chapters: {len(lang['chapter_order'])}")
    print(f"  Output: {output_path}")
    print(f"  Size: {fsize / 1024:.0f} KB")


def main():
    print("=" * 50)
    print("  Translated EPUB Generator")
    print("=" * 50)

    for lang in LANGUAGES:
        build_epub(lang)

    print(f"\n{'='*50}")
    print("  ALL EPUBS GENERATED")
    print(f"{'='*50}")
    for lang in LANGUAGES:
        if os.path.isfile(lang["output_path"]):
            fsize = os.path.getsize(lang["output_path"])
            print(f"  {lang['name']}: {lang['output_path']} ({fsize/1024:.0f} KB)")
    print("Done.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
Build script for THE THIRD CHAIN - KDP-compliant PDF, EPUB, and Cover.
Book 3 of the Meera Desai Thrillers by Kapil.
"""

import os
import re
import sys
import subprocess
import textwrap
from pathlib import Path

BASE_DIR = Path(r"D:\Kapil\Books\Meera Desai\MD -The Third Chain")
MANUSCRIPT = BASE_DIR / "Manuscript_v6.md"
OUTPUT_DIR = BASE_DIR / "Output"
PDF_DIR = OUTPUT_DIR
EPUB_DIR = OUTPUT_DIR
COVER_DIR = OUTPUT_DIR
TEMP_DIR = Path(r"E:\Temp\kilo")

TITLE = "THE THIRD CHAIN"
SUBTITLE = "Book Three of the Meera Desai Thrillers"
SERIES_LINE = "The Meera Desai Thrillers --- Series Finale"
AUTHOR = "Kapil"
DEDICATION = "For my father, who taught me to love numbers."
PREV_BOOKS = ["VAULT B", "TWO CHAINS"]

TRIM_W = 5.5
TRIM_H = 8.5
INNER_MARGIN = 0.75
OUTER_MARGIN = 0.625
TOP_MARGIN = 0.625
BOTTOM_MARGIN = 0.85
PAGE_COUNT = 261
PAPER_THICKNESS = 0.0025
HARDCOVER_PAPER_THICKNESS = 0.00306
BOARD_THICKNESS = 0.100
HARDCOVER_WRAP = 0.708
PAPERBACK_BLEED = 0.125


def read_manuscript():
    with open(MANUSCRIPT, "r", encoding="utf-8") as f:
        return f.read()


def parse_parts_and_chapters(md_text):
    lines = md_text.split("\n")
    parts = []
    current_part = None
    chapters = []
    fact_text = None
    in_fact = False
    fact_lines = []
    epilogue = None

    i = 0
    while i < len(lines):
        line = lines[i]

        if re.match(r"^>\s*\*?\*?\*?FACT\*?\*?\*?\s*$", line, re.IGNORECASE):
            in_fact = True
            i += 1
            continue

        if in_fact:
            if line.startswith(">"):
                cleaned = re.sub(r"^>\s*", "", line).strip()
                if cleaned:
                    fact_lines.append(cleaned)
            elif line.strip() == "---":
                if fact_lines:
                    fact_text = "\n".join(fact_lines)
                in_fact = False
            i += 1
            continue

        part_match = re.match(r"^#\s+(PART\s+\w+)", line)
        if part_match:
            current_part = part_match.group(1)
            parts.append(current_part)
            i += 1
            continue

        part_title_match = re.match(r"^#\s+(THE\s+.+)", line)
        if part_title_match and "CHAIN" not in part_title_match.group(1):
            current_part = part_title_match.group(1)
            parts.append(current_part)
            i += 1
            continue

        ch_match = re.match(r"^##\s+(Chapter\s+\d+)", line, re.IGNORECASE)
        if ch_match:
            ch_title = ch_match.group(1)
            ch_lines = []
            i += 1
            while i < len(lines):
                if re.match(r"^##\s+(Chapter\s+\d+|Epilogue)", lines[i], re.IGNORECASE):
                    break
                if re.match(r"^#\s+PART\s+", lines[i]):
                    break
                if re.match(r"^#\s+THE\s+END", lines[i]):
                    break
                ch_lines.append(lines[i])
                i += 1
            chapters.append({"title": ch_title, "part": current_part, "body": "\n".join(ch_lines)})
            continue

        ep_match = re.match(r"^##\s+Epilogue", line, re.IGNORECASE)
        if ep_match:
            ep_lines = []
            i += 1
            while i < len(lines):
                if re.match(r"^#\s+THE\s+END", lines[i]):
                    break
                ep_lines.append(lines[i])
                i += 1
            epilogue = {"title": "Epilogue", "part": current_part, "body": "\n".join(ep_lines)}
            continue

        if re.match(r"^#\s+THE\s+END", line):
            i += 1
            continue

        i += 1

    return fact_text, parts, chapters, epilogue


# =============================================================================
# PDF GENERATION
# =============================================================================

def escape_latex(text):
    text = text.replace("\\", "\\textbackslash{}")
    text = text.replace("&", "\\&")
    text = text.replace("%", "\\%")
    text = text.replace("$", "\\$")
    text = text.replace("#", "\\#")
    text = text.replace("_", "\\_")
    text = text.replace("{", "\\{")
    text = text.replace("}", "\\}")
    text = text.replace("~", "\\textasciitilde{}")
    text = text.replace("^", "\\textasciicircum{}")
    return text


def md_to_latex_body(md_text):
    lines = md_text.split("\n")
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if re.match(r"^###\s+", line):
            heading = re.sub(r"^###\s+", "", line).strip()
            result.append(f"\\subsection*{{{escape_latex(heading)}}}")
            result.append("")
            i += 1
            continue

        if line.strip() == "---":
            result.append("")
            result.append("\\secediv")
            result.append("")
            i += 1
            continue

        if line.startswith(">"):
            block_lines = []
            while i < len(lines) and lines[i].startswith(">"):
                cleaned = re.sub(r"^>\s*", "", lines[i]).strip()
                if cleaned:
                    block_lines.append(cleaned)
                i += 1
            if block_lines:
                result.append("\\begin{quote}")
                for bl in block_lines:
                    result.append(f"  \\textit{{{escape_latex(bl)}}}")
                result.append("\\end{quote}")
                result.append("")
            continue

        if re.match(r"^\*\*.+\*\*$", line.strip()):
            bold_text = re.sub(r"^\*\*", "", line.strip())
            bold_text = re.sub(r"\*\*$", "", bold_text)
            result.append(f"\\textbf{{{escape_latex(bold_text)}}}")
            result.append("")
            i += 1
            continue

        if line.strip() == "":
            result.append("")
            i += 1
            continue

        text = line
        text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
        text = re.sub(r"\*(.+?)\*", r"\\textit{\1}", text)
        text = escape_latex(text)
        text = text.replace("\\textbackslash\\{\\}", "\\textbackslash{}")
        text = re.sub(r"\\textbf\{([^}]*)\}", lambda m: f"\\textbf{{{escape_latex(m.group(1))}}}", text)
        text = re.sub(r"\\textit\{([^}]*)\}", lambda m: f"\\textit{{{escape_latex(m.group(1))}}}", text)
        result.append(text)
        i += 1

    return "\n".join(result)


def generate_latex(fact_text, parts, chapters, epilogue):
    tex = []

    tex.append(r"""\documentclass[10pt,twoside,openany]{book}

% Page size - trade paperback (KDP: 5.5 x 8.5)
\usepackage[paperwidth=5.5in,paperheight=8.5in,
  inner=0.75in, outer=0.625in,
  top=0.75in, bottom=0.85in]{geometry}

% Fonts - embedded via XeLaTeX/fontspec
\usepackage{fontspec}
\setmainfont{Palatino Linotype}
\setmonofont{Courier New}

% Typography - prevent overfull boxes for KDP compliance
\usepackage{microtype}
\emergencystretch=5em
\tolerance=500
\hfuzz=0pt
\vfuzz=0pt
\raggedbottom
\widowpenalty=10000
\clubpenalty=10000

% Paragraph indentation
\setlength{\parindent}{0.3in}
\setlength{\parskip}{0pt}

% Headers and footers
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[CE,CO]{\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Chapter opening pages
\fancypagestyle{plain}{
  \fancyhf{}
  \fancyfoot[CE,CO]{\thepage}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
}

\fancypagestyle{empty}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
}

% Chapter formatting - title at TOP of page
\usepackage{titlesec}
\titleformat{\chapter}[display]
  {\normalfont\centering}
  {}
  {0pt}
  {\normalfont\Large\bfseries\MakeUppercase}
\titlespacing*{\chapter}
  {0pt}
  {0pt}
  {0.4in}

% Section divider
\newcommand{\secediv}{\begin{center}\textcolor{gray}{\textbullet\quad\textbullet\quad\textbullet}\end{center}}

% Pandoc compatibility
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

% Colors
\usepackage{xcolor}

% Hyperlinks - draft mode for print
\usepackage{hyperref}
\hypersetup{
  draft=true,
  hidelinks,
  pdftitle={THE THIRD CHAIN},
  pdfauthor={Kapil},
  pdfsubject={Fiction - Thriller}
}

% No section numbers
\setcounter{secnumdepth}{-1}
\setcounter{tocdepth}{1}

% Front matter roman numerals
\frontmatter

\begin{document}

%==============================================================================
% FRONT MATTER
%==============================================================================

%--- Also by page ---
\thispagestyle{empty}
\begin{center}
\vspace*{2in}
{\normalfont Also by Kapil\par}
\vspace{0.5in}
""")

    for book in PREV_BOOKS:
        tex.append(f"{{\\normalfont {book}\\par}}")
        tex.append("\\vspace{0.15in}")

    tex.append(r"""\end{center}
\clearpage

%--- Title page ---
\thispagestyle{empty}
\begin{center}
\vspace*{1.5in}
{\LARGE\bfseries THE THIRD CHAIN\par}
\vspace{0.4in}
{\normalfont Book Three of the Meera Desai Thrillers --- Series Finale\par}
\vspace{1in}
{\normalfont Kapil\par}
\end{center}
\clearpage

%--- Copyright page ---
\thispagestyle{empty}
\begin{footnotesize}
\noindent THE THIRD CHAIN\\
Book Three of the Meera Desai Thrillers --- Series Finale\\[0.5em]
\textcopyright\ 2026 Kapil. All rights reserved.\\[0.5em]
This is a work of fiction. Names, characters, organizations, places, events, and incidents are either products of the author's imagination or are used fictitiously. Any resemblance to actual persons, living or dead, or actual events is purely coincidental.\\[0.5em]
Historical entities note: Emperor Ashoka, the Padmanabhaswamy Temple, the Newport Tower, Sarnath, Brahmi script, RSA encryption, the Icelandic Modern Media Initiative, wootz/Damascus steel, Nalanda University, the Silk Road, and other historical entities are real. The story built around them is fiction.\\[0.5em]
First Edition
\end{footnotesize}
\clearpage

%--- Dedication ---
\thispagestyle{empty}
\begin{center}
\vspace*{2.5in}
\textit{For my father, who taught me to love numbers.}
\end{center}
\clearpage

%--- Table of Contents ---
\begingroup
\titlespacing*{\chapter}{0pt}{0pt}{0.3in}
\tableofcontents
\endgroup
\clearpage
""")

    # FACT page
    if fact_text:
        tex.append(r"%--- FACT page ---")
        tex.append(r"\thispagestyle{plain}")
        tex.append(r"\begin{quote}")
        tex.append(r"\textbf{\textit{FACT}}")
        tex.append(r"\end{quote}")

        fact_paragraphs = fact_text.split("\n")
        for para in fact_paragraphs:
            para = para.strip()
            if para:
                para_escaped = escape_latex(para)
                para_escaped = re.sub(r"\\textbf\{([^}]*)\}", lambda m: f"\\textbf{{{escape_latex(m.group(1))}}}", para_escaped)
                tex.append(r"\begin{quote}")
                tex.append(f"  \\textit{{{para_escaped}}}")
                tex.append(r"\end{quote}")

        tex.append(r"\clearpage")

    tex.append(r"""
%==============================================================================
% MAIN MATTER
%==============================================================================
\mainmatter
""")

    current_part_name = None
    for ch in chapters:
        if ch["part"] and ch["part"] != current_part_name:
            current_part_name = ch["part"]
            tex.append(f"\\part*{{{escape_latex(current_part_name)}}}")
            tex.append("")

        tex.append(f"\\chapter{{{escape_latex(ch['title'])}}}")
        tex.append("")
        body_latex = md_to_latex_body(ch["body"])
        tex.append(body_latex)
        tex.append("")

    if epilogue:
        tex.append(f"\\chapter{{Epilogue}}")
        tex.append("")
        body_latex = md_to_latex_body(epilogue["body"])
        tex.append(body_latex)
        tex.append("")

    tex.append(r"""
%==============================================================================
% BACK MATTER
%==============================================================================
\backmatter

%--- Also by ---
\thispagestyle{empty}
\begin{center}
\vspace*{2in}
{\normalfont Also by Kapil\par}
\vspace{0.5in}
""")

    for book in PREV_BOOKS:
        tex.append(f"{{\\normalfont {book}\\par}}")
        tex.append("\\vspace{0.15in}")

    tex.append(r"""{\normalfont\textbf{THE THIRD CHAIN}\par}
\end{center}
\clearpage

\end{document}
""")

    return "\n".join(tex)


def build_pdf():
    print("=" * 60)
    print("BUILDING KDP-COMPLIANT PDF")
    print("=" * 60)

    md_text = read_manuscript()
    fact_text, parts, chapters, epilogue = parse_parts_and_chapters(md_text)

    print(f"  Parsed {len(chapters)} chapters + epilogue")
    print(f"  Parts: {parts}")
    print(f"  Fact page: {'found' if fact_text else 'not found'}")

    latex_content = generate_latex(fact_text, parts, chapters, epilogue)

    tex_path = TEMP_DIR / "the_third_chain.tex"
    tex_path.write_text(latex_content, encoding="utf-8")
    print(f"  LaTeX written to {tex_path}")

    env = os.environ.copy()
    env["TEXINPUTS"] = str(TEMP_DIR) + os.pathsep + env.get("TEXINPUTS", "")

    for pass_num in range(1, 4):
        print(f"  XeLaTeX pass {pass_num}/3...")
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode",
             f"-output-directory={TEMP_DIR}",
             str(tex_path)],
            capture_output=True, cwd=str(TEMP_DIR),
            timeout=300, env=env
        )
        if result.returncode != 0:
            print(f"  XeLaTeX pass {pass_num} had warnings (return code {result.returncode})")
            stdout_text = result.stdout.decode("utf-8", errors="replace")
            errors = [l for l in stdout_text.split("\n") if "!" in l]
            if errors:
                for e in errors[:5]:
                    print(f"    {e}")

    pdf_out = PDF_DIR / "THE_THIRD_CHAIN_Interior.pdf"
    pdf_temp = TEMP_DIR / "the_third_chain.pdf"
    if pdf_temp.exists():
        import shutil
        shutil.copy2(pdf_temp, pdf_out)
        print(f"  PDF written to {pdf_out}")
        size_kb = pdf_out.stat().st_size / 1024
        print(f"  PDF size: {size_kb:.0f} KB")
    else:
        print("  ERROR: PDF was not generated!")
        return False

    return True


# =============================================================================
# EPUB GENERATION
# =============================================================================

def md_to_html_body(md_text):
    text = md_text

    text = re.sub(r"^###\s+(.+)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
    text = re.sub(r"^##\s+(.+)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
    text = re.sub(r"^#\s+(.+)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)

    blockquotes = re.findall(r'((?:^>.*\n?)+)', text, flags=re.MULTILINE)
    for bq in blockquotes:
        inner = re.sub(r'^>\s*', '', bq, flags=re.MULTILINE).strip()
        inner = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', inner)
        inner = re.sub(r'\*(.+?)\*', r'<em>\1</em>', inner)
        text = text.replace(bq, f"<blockquote><p>{inner}</p></blockquote>\n")

    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    text = re.sub(r"^---$", "<hr/>", text, flags=re.MULTILINE)

    paragraphs = text.split("\n\n")
    processed = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith("<") or p.startswith("<h") or p.startswith("<hr") or p.startswith("<block"):
            processed.append(p)
        else:
            lines = p.split("\n")
            lines = [l.strip() for l in lines if l.strip()]
            processed.append("<p>" + " ".join(lines) + "</p>")

    return "\n\n".join(processed)


def build_epub():
    print("=" * 60)
    print("BUILDING KDP-COMPLIANT EPUB")
    print("=" * 60)

    md_text = read_manuscript()
    fact_text, parts, chapters, epilogue = parse_parts_and_chapters(md_text)

    src_dir = TEMP_DIR / "epub_src"
    src_dir.mkdir(parents=True, exist_ok=True)

    metadata = textwrap.dedent(f"""\
    ---
    title: "{TITLE}"
    subtitle: "{SUBTITLE}"
    creator:
    - role: author
      text: {AUTHOR}
    date: 2026-01-01
    lang: en-US
    cover-image: cover.jpg
    stylesheet: style.css
    epub-metadata: |
      <meta property="dcterms:modified">2026-01-01T00:00:00Z</meta>
      <meta name="cover" content="cover.jpg" />
    ---
    """)

    style_css = textwrap.dedent("""\
    @page {
      margin: 0.5em;
    }
    body {
      font-family: "Georgia", "Palatino Linotype", "Book Antiqua", serif;
      line-height: 1.6;
      text-align: justify;
      color: #000;
    }
    h1 {
      font-size: 1.8em;
      font-weight: bold;
      text-align: center;
      margin-top: 2em;
      margin-bottom: 1em;
      page-break-before: always;
    }
    h2 {
      font-size: 1.3em;
      font-weight: bold;
      text-align: center;
      margin-top: 1.5em;
      margin-bottom: 0.8em;
    }
    h3 {
      font-size: 1.1em;
      font-weight: bold;
      margin-top: 1em;
      margin-bottom: 0.5em;
    }
    p {
      text-indent: 1.5em;
      margin: 0;
      margin-bottom: 0;
    }
    p:first-of-type {
      text-indent: 0;
    }
    blockquote {
      margin: 1em 2em;
      font-style: italic;
    }
    blockquote p {
      text-indent: 0;
    }
    hr {
      border: none;
      border-top: 1px solid #ccc;
      margin: 2em auto;
      width: 30%;
      text-align: center;
    }
    .chapter-title {
      font-size: 1.8em;
      font-weight: bold;
      text-align: center;
      margin-top: 3em;
      margin-bottom: 2em;
      page-break-before: always;
    }
    .part-title {
      font-size: 1.5em;
      font-weight: bold;
      text-align: center;
      margin-top: 4em;
      margin-bottom: 3em;
      page-break-before: always;
    }
    .dedication {
      text-align: center;
      font-style: italic;
      margin-top: 5em;
    }
    .fact-label {
      font-weight: bold;
      font-style: italic;
    }
    .front-matter {
      page-break-after: always;
    }
    """)

    (src_dir / "style.css").write_text(style_css, encoding="utf-8")

    cover_src = OUTPUT_DIR / "THE_THIRD_CHAIN_Cover_Front.jpg"
    if cover_src.exists():
        import shutil
        shutil.copy2(cover_src, src_dir / "cover.jpg")
        print("  Cover image copied for EPUB")

    epub_md = metadata + "\n\n"

    epub_md += '<div class="front-matter dedicat' + 'ion">\n\n'
    epub_md += f"*{DEDICATION}*\n\n"
    epub_md += '</div>\n\n'

    if fact_text:
        epub_md += '<div class="front-matter">\n\n'
        epub_md += "> **FACT**\n>\n"
        for line in fact_text.split("\n"):
            epub_md += f"> {line}\n"
        epub_md += "\n</div>\n\n"

    current_part = None
    for ch in chapters:
        if ch["part"] and ch["part"] != current_part:
            current_part = ch["part"]
            epub_md += f'<div class="part-title">{current_part}</div>\n\n'

        epub_md += f"## {ch['title']}\n\n"
        epub_md += ch["body"] + "\n\n"

    if epilogue:
        epub_md += "## Epilogue\n\n"
        epub_md += epilogue["body"] + "\n\n"

    epub_md_path = src_dir / "the_third_chain.md"
    epub_md_path.write_text(epub_md, encoding="utf-8")

    epub_out = EPUB_DIR / "THE_THIRD_CHAIN.epub"

    cmd = [
        "pandoc",
        str(epub_md_path),
        "-o", str(epub_out),
        "--toc",
        "--toc-depth=1",
        "--css=style.css",
        "--metadata", f"title={TITLE}",
        "--metadata", f"author={AUTHOR}",
        "--metadata", "language=en-US",
    ]
    if (src_dir / "cover.jpg").exists():
        cmd.append(f"--epub-cover-image={src_dir / 'cover.jpg'}")
    cmd = [c for c in cmd if c]

    print("  Running pandoc...")
    result = subprocess.run(cmd, capture_output=True, cwd=str(src_dir), timeout=120)
    if result.returncode != 0:
        stderr_text = result.stderr.decode("utf-8", errors="replace")
        print(f"  Pandoc error: {stderr_text}")
        return False

    if epub_out.exists():
        size_kb = epub_out.stat().st_size / 1024
        print(f"  EPUB written to {epub_out}")
        print(f"  EPUB size: {size_kb:.0f} KB")
        return True
    else:
        print("  ERROR: EPUB was not generated!")
        return False


# =============================================================================
# COVER GENERATION
# =============================================================================

def _render_cover(cover_type, spine_w_inches, margin_inches, out_pdf_name, target_w_inches=None, target_h_inches=None):
    import tempfile
    import img2pdf
    from PIL import Image, ImageDraw, ImageFont

    dpi = 300
    spine_w = int(spine_w_inches * dpi)
    cover_w = int(TRIM_W * dpi)
    cover_h = int(TRIM_H * dpi)
    margin_px = int(margin_inches * dpi)

    total_w = margin_px + cover_w + spine_w + cover_w + margin_px
    total_h = margin_px + cover_h + margin_px

    if target_w_inches and target_h_inches:
        target_w_px = int(target_w_inches * dpi + 0.5)
        target_h_px = int(target_h_inches * dpi + 0.5)
        total_w = target_w_px
        total_h = target_h_px
        margin_px = (total_h - cover_h) // 2
        spine_w = total_w - 2 * margin_px - 2 * cover_w

    print(f"  [{cover_type}] Spine: {spine_w_inches:.3f}\" | Margin: {margin_inches:.3f}\"")
    print(f"  [{cover_type}] Full dimensions: {total_w/dpi:.2f}\" x {total_h/dpi:.2f}\" ({total_w}x{total_h}px)")

    img = Image.new("RGB", (total_w, total_h), "#0a0a12")
    draw = ImageDraw.Draw(img)

    front_x = margin_px + cover_w + spine_w
    back_x = margin_px

    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/constanb.ttf", 110)
    except Exception:
        font_title = ImageFont.truetype("arialbd.ttf", 110)
    try:
        font_subtitle = ImageFont.truetype("C:/Windows/Fonts/constan.ttf", 42)
    except Exception:
        font_subtitle = ImageFont.truetype("arial.ttf", 42)
    try:
        font_author = ImageFont.truetype("C:/Windows/Fonts/constanb.ttf", 60)
    except Exception:
        font_author = ImageFont.truetype("arialbd.ttf", 60)
    try:
        font_spine = ImageFont.truetype("C:/Windows/Fonts/constan.ttf", 32)
    except Exception:
        font_spine = ImageFont.truetype("arial.ttf", 32)
    try:
        font_spine_author = ImageFont.truetype("C:/Windows/Fonts/constanb.ttf", 28)
    except Exception:
        font_spine_author = ImageFont.truetype("arialbd.ttf", 28)
    try:
        font_blurb = ImageFont.truetype("C:/Windows/Fonts/constan.ttf", 30)
    except Exception:
        font_blurb = ImageFont.truetype("arial.ttf", 30)
    try:
        font_back_title = ImageFont.truetype("C:/Windows/Fonts/constanb.ttf", 36)
    except Exception:
        font_back_title = ImageFont.truetype("arialbd.ttf", 36)

    dark_bg = "#0a0a12"
    gold_accent = "#c9a84c"
    cream_text = "#e8e0d0"
    muted_text = "#8a8070"

    draw.rectangle([0, 0, total_w, total_h], fill=dark_bg)

    for y in range(0, total_h, 4):
        alpha = int(15 * (y / total_h))
        draw.line([(front_x, y), (front_x + cover_w, y)], fill=f"#{alpha:02x}{alpha:02x}{int(alpha*1.5):02x}")

    spine_left = margin_px + cover_w
    spine_right = margin_px + cover_w + spine_w
    draw.rectangle([spine_left, 0, spine_right, total_h], fill="#08080f")
    draw.line([(spine_left, 0), (spine_left, total_h)], fill=gold_accent, width=2)
    draw.line([(spine_right, 0), (spine_right, total_h)], fill=gold_accent, width=2)

    def draw_text_centered(draw_obj, text, font, fill, cx, cy):
        bbox = draw_obj.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw_obj.text((cx - tw // 2, cy - th // 2), text, font=font, fill=fill)

    title_lines = ["THE", "THIRD", "CHAIN"]
    start_y = int(total_h * 0.30)
    line_spacing = 120
    for i, line in enumerate(title_lines):
        cy = start_y + i * line_spacing
        draw_text_centered(draw, line, font_title, gold_accent, front_x + cover_w // 2, cy)

    deco_y = start_y + len(title_lines) * line_spacing + 40
    deco_w = 200
    deco_cx = front_x + cover_w // 2
    draw.line([(deco_cx - deco_w, deco_y), (deco_cx + deco_w, deco_y)], fill=gold_accent, width=2)
    draw.ellipse([deco_cx - 6, deco_y - 6, deco_cx + 6, deco_y + 6], fill=gold_accent)

    sub_y = deco_y + 60
    draw_text_centered(draw, "Book Three of the Meera Desai Thrillers", font_subtitle, cream_text,
                       front_x + cover_w // 2, sub_y)

    author_y = int(total_h * 0.78)
    draw_text_centered(draw, "KAPIL", font_author, cream_text, front_x + cover_w // 2, author_y)

    prev_y = author_y + 80
    draw_text_centered(draw, "Author of VAULT B and TWO CHAINS", font_subtitle, muted_text,
                       front_x + cover_w // 2, prev_y)

    tagline_y = int(total_h * 0.90)
    draw_text_centered(draw, '"The vault is open. The knowledge is loose.', font_blurb, muted_text,
                       front_x + cover_w // 2, tagline_y)
    draw_text_centered(draw, 'And the world isn\'t ready."', font_blurb, muted_text,
                       front_x + cover_w // 2, tagline_y + 40)

    spine_cx = spine_left + spine_w // 2
    spine_title = "THE THIRD CHAIN"
    bbox = draw.textbbox((0, 0), spine_title, font=font_spine)
    st_w = bbox[2] - bbox[0]
    rotated = Image.new("RGB", (st_w + 40, 50), dark_bg)
    r_draw = ImageDraw.Draw(rotated)
    r_draw.text((20, 5), spine_title, font=font_spine, fill=gold_accent)
    rotated = rotated.rotate(90, expand=True)
    ry = total_h // 2 - rotated.height // 2 - 60
    if spine_w >= rotated.height:
        rx = spine_cx - rotated.width // 2
        img.paste(rotated, (rx, ry))

    spine_author = "KAPIL"
    bbox = draw.textbbox((0, 0), spine_author, font=font_spine_author)
    sa_w = bbox[2] - bbox[0]
    rotated_a = Image.new("RGB", (sa_w + 40, 45), dark_bg)
    ra_draw = ImageDraw.Draw(rotated_a)
    ra_draw.text((20, 10), spine_author, font=font_spine_author, fill=cream_text)
    rotated_a = rotated_a.rotate(90, expand=True)
    ry_a = total_h // 2 + 80
    if spine_w >= rotated_a.height:
        rx_a = spine_cx - rotated_a.width // 2
        img.paste(rotated_a, (rx_a, ry_a))

    text_margin = int(0.5 * dpi)
    back_cx = back_x + cover_w // 2
    back_top = margin_px + text_margin

    draw_text_centered(draw, "PRAISE FOR THE MEERA DESAI THRILLERS", font_back_title, gold_accent,
                       back_cx, back_top + 30)

    draw.line([(back_cx - 150, back_top + 70), (back_cx + 150, back_top + 70)], fill=gold_accent, width=1)

    blurb_y = back_top + 120
    blurbs = [
        '"A pulse-pounding thriller that weaves',
        "ancient mystery with modern suspense.\"",
        "",
        '"Meera Desai is the hero the thriller',
        "genre has been waiting for.\"",
        "",
        '"Fans of Dan Brown and James Rollins',
        "will devour this series.\"",
    ]
    for line in blurbs:
        if line:
            draw_text_centered(draw, line, font_blurb, cream_text, back_cx, blurb_y)
        blurb_y += 45

    synopsis_y = int(total_h * 0.50)
    synopsis_lines = [
        "Eighteen months after becoming the unified",
        "guardian of both chains, ex-FBI agent Meera",
        "Desai discovers that Ashoka's ancient knowledge",
        "has been scattering along the Silk Road for",
        "two thousand years --- and a rogue guardian",
        "from a forgotten lineage is assembling every",
        "fragment for simultaneous global release.",
        "",
        "To stop her, Meera must race across four",
        "continents, confront the moral limits of",
        "secrecy, and make the hardest choice of",
        "her career.",
    ]
    for line in synopsis_lines:
        if line:
            draw_text_centered(draw, line, font_blurb, cream_text, back_cx, synopsis_y)
        synopsis_y += 40

    draw.line([(back_cx - 100, synopsis_y + 20), (back_cx + 100, synopsis_y + 20)], fill=gold_accent, width=1)

    barcode_edge_margin = int(0.25 * dpi)
    barcode_w = int(2.0 * dpi)
    barcode_h = int(1.2 * dpi)
    back_right = margin_px + cover_w
    back_bottom = margin_px + cover_h
    barcode_x = back_right - barcode_edge_margin - barcode_w
    barcode_y = back_bottom - barcode_edge_margin - barcode_h
    draw.rectangle([barcode_x, barcode_y, barcode_x + barcode_w, barcode_y + barcode_h],
                   fill="white", outline="#cccccc")

    temp_jpg = TEMP_DIR / f"_cover_temp_{cover_type.lower()}.jpg"
    img.save(str(temp_jpg), "JPEG", quality=95, dpi=(dpi, dpi))

    pdf_path = COVER_DIR / out_pdf_name
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(str(temp_jpg)))

    size_kb = pdf_path.stat().st_size / 1024
    print(f"  [{cover_type}] PDF written to {pdf_path.name} ({size_kb:.0f} KB)")

    return img, front_x, margin_px, cover_w, cover_h


def build_cover():
    import shutil
    print("=" * 60)
    print("BUILDING KDP-COMPLIANT COVERS (PDF: PAPERBACK + HARDCOVER)")
    print("=" * 60)

    pb_spine = PAPER_THICKNESS * PAGE_COUNT
    hc_spine = HARDCOVER_PAPER_THICKNESS * PAGE_COUNT + 2 * BOARD_THICKNESS

    print(f"  Page count: {PAGE_COUNT}")
    print(f"  Paperback spine: {pb_spine:.3f}\" (paper only)")
    print(f"  Hardcover spine: {hc_spine:.3f}\" (paper + 2x{BOARD_THICKNESS}\" boards)")
    print(f"  Hardcover wrap: {HARDCOVER_WRAP}\" | Expected total: {2*HARDCOVER_WRAP + 2*5.5 + hc_spine:.3f}\" x {2*HARDCOVER_WRAP + 8.5:.3f}\"")

    pb_img, pb_front_x, pb_margin, cw, ch = _render_cover(
        "PAPERBACK", pb_spine, PAPERBACK_BLEED, "THE_THIRD_CHAIN_Cover_Paperback.pdf")

    hc_img, hc_front_x, hc_margin, _, _ = _render_cover(
        "HARDCOVER", hc_spine, HARDCOVER_WRAP, "THE_THIRD_CHAIN_Cover_Hardcover.pdf",
        target_w_inches=13.416, target_h_inches=9.917)

    from PIL import Image
    front_path = COVER_DIR / "THE_THIRD_CHAIN_Cover_Front.jpg"
    front_img = pb_img.crop((pb_front_x, pb_margin, pb_front_x + cw, pb_margin + ch))
    front_img.save(str(front_path), "JPEG", quality=95, dpi=(300, 300))
    print(f"  [FRONT] Written to {front_path.name} (cropped from paperback, for ebook)")

    return True


# =============================================================================
# MAIN
# =============================================================================

def main():
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    tasks = []
    if "--pdf" in sys.argv:
        tasks.append("pdf")
    elif "--epub" in sys.argv:
        tasks.append("epub")
    elif "--cover" in sys.argv:
        tasks.append("cover")
    else:
        tasks = ["cover", "pdf", "epub"]

    success = True
    for task in tasks:
        if task == "cover":
            if not build_cover():
                success = False
        elif task == "pdf":
            if not build_pdf():
                success = False
        elif task == "epub":
            if not build_epub():
                success = False

    print("\n" + "=" * 60)
    if success:
        print("BUILD COMPLETE - All outputs generated successfully")
    else:
        print("BUILD COMPLETE - Some outputs had errors")
    print("=" * 60)

    print("\nOutput files:")
    for f in OUTPUT_DIR.iterdir():
        if f.is_file() and not f.name.startswith("."):
            size = f.stat().st_size
            if size > 1024 * 1024:
                print(f"  {f.name}: {size / (1024*1024):.1f} MB")
            else:
                print(f"  {f.name}: {size / 1024:.0f} KB")

    print("\nKDP Specifications:")
    pb_spine = PAPER_THICKNESS * PAGE_COUNT
    hc_spine = PAPER_THICKNESS * PAGE_COUNT + 2 * BOARD_THICKNESS
    print(f"  Trim Size: {TRIM_W}\" x {TRIM_H}\" (Trade)")
    print(f"  Interior: Black & White, Cream paper recommended")
    print(f"  PDF: 300 DPI, embedded fonts, no bleed")
    print(f"  EPUB: EPUB3, reflowable, cover embedded")
    print(f"  Paperback Cover: wrap, {pb_spine:.3f}\" spine, {PAPERBACK_BLEED}\" bleed")
    print(f"  Hardcover Cover: wrap, {hc_spine:.3f}\" spine, {HARDCOVER_WRAP}\" fold-over")


if __name__ == "__main__":
    main()

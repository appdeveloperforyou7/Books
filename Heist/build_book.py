#!/usr/bin/env python3
"""Build THE MERIDIAN -> EPUB + interior PDF into Output/."""
import os, glob, subprocess, sys

ROOT = r"D:\Kapil\Books\Heist"
CH   = os.path.join(ROOT, "Chapters")
OUT  = os.path.join(ROOT, "Output")
PANDOC = r"E:\Users\Rishabh\AppData\Local\Pandoc\pandoc.exe"
WEASY  = r"E:\Users\Rishabh\AppData\Roaming\Python\Python314\Scripts\weasyprint.exe"
CSS    = os.path.join(ROOT, "book.css")

TITLE    = "THE MERIDIAN"
SUBTITLE = "A Heist Thriller"
AUTHOR   = "Kapil Gupta"
TAGLINE  = ("Ocean's Eleven meets Murder on the Orient Express "
            "at six hundred kilometres an hour \u2014 with codes you "
            "can solve before the thief does.")

os.makedirs(OUT, exist_ok=True)

# 1. Assemble a clean build-source markdown (title page metadata + chapters, NO draft note)
files = sorted(glob.glob(os.path.join(CH, "*.md")))
if not files:
    sys.exit("No chapter files found in " + CH)
body = []
for f in files:
    with open(f, encoding="utf-8") as fh:
        body.append(fh.read().strip())
body_text = "\n\n".join(body)

meta = (
    "---\n"
    f'title: "{TITLE}"\n'
    f'subtitle: "{SUBTITLE}"\n'
    f'author: "{AUTHOR}"\n'
    'lang: en-GB\n'
    "---\n\n"
    f"> *{TAGLINE}*\n\n"
)
build_md = os.path.join(OUT, "_manuscript_build.md")
with open(build_md, "w", encoding="utf-8") as fh:
    fh.write(meta + body_text)

epub_path = os.path.join(OUT, "TheMeridian.epub")
pdf_path  = os.path.join(OUT, "TheMeridian.pdf")
html_tmp  = os.path.join(OUT, "_book.html")

def run(cmd):
    print(">>", " ".join('"%s"' % c if " " in c else c for c in cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("STDERR:", r.stderr[-2000:])
        raise SystemExit("Command failed: " + cmd[0])
    if r.stderr.strip():
        print("  (warn)", r.stderr.strip()[-400:])

# 2. EPUB (pandoc embeds the CSS, splits chapters on H1)
run([PANDOC, build_md, "-o", epub_path,
     "--toc", "--toc-depth=1",
     "--css", CSS,
     "--epub-chapter-level=1"])

# 3. PDF — pandoc -> standalone HTML, then weasyprint with the stylesheet (reliable CSS application)
run([PANDOC, build_md, "-o", html_tmp, "-s", "--toc", "--toc-depth=1"])
run([WEASY, html_tmp, pdf_path, "-s", CSS])

# 4. Cleanup intermediates
for tmp in (build_md, html_tmp):
    try: os.remove(tmp)
    except OSError: pass

print("\n=== BUILD COMPLETE ===")
for p in (epub_path, pdf_path):
    print(f"{os.path.basename(p):24} {os.path.getsize(p):>10,} bytes")

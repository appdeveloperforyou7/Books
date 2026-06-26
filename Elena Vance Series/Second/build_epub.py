# -*- coding: utf-8 -*-
"""Build EPUB3 for THE DEVOTED — English edition (Kindle colour)."""
import subprocess, os

PANDOC = r"C:\Program Files\Pandoc\pandoc.exe"
ASSETS = r"E:\Temp\kilo\epub_assets"
CSS    = ASSETS + r"\stylesheet1.css"
COVER  = ASSETS + r"\cover.jpg"
SRC    = r"D:\Kapil\Books\Elena Vance Series\Second\manuscript.md"
OUT    = r"D:\Kapil\Books\Elena Vance Series\Second\TheDevoted.epub"

META = """---
title: "The Devoted"
author: "Rishabh"
lang: en
publisher: "Self-published"
rights: "All rights reserved"
subject: "Fiction, Thriller, Psychological"
description: "Elena Vance reads people. Her new partner, Joss Navarro, reads crime scenes. When a philanthropist's apparent suicide is ruled a tragic end to a 'sad' life, Elena and Joss must combine their skills to dismantle a perfectly staged room and a perfectly rehearsed household. But to catch a killer who hides behind love, Elena must weaponize the one thing she swore never to use: her own coaching practice."
---
"""

metafile = ASSETS + r"\meta_en_devoted.yaml"
with open(metafile, "w", encoding="utf-8") as f:
    f.write(META)

cmd = [PANDOC, SRC,
       "--metadata-file=" + metafile,
       "--epub-cover-image=" + COVER,
       "--css=" + CSS,
       "--toc", "--toc-depth=2",
       "--epub-chapter-level=2",
       "-f", "markdown", "-t", "epub3",
       "-o", OUT]

r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
if r.returncode != 0:
    print("FAIL", r.stderr)
else:
    print("EPUB written:", OUT, os.path.getsize(OUT), "bytes")

# -*- coding: utf-8 -*-
"""Build EPUB3 editions for The Quiet Wife — DE/ES/FR, same pipeline as the English epub (pandoc)."""
import subprocess, os, sys

PANDOC = r"C:\Program Files\Pandoc\pandoc.exe"
ASSETS = r"E:\Temp\kilo\epub_assets"
CSS    = ASSETS + r"\stylesheet1.css"
COVER  = ASSETS + r"\cover.jpg"
BASE   = r"D:\Kapil\Books\Elena Vance Series\The Quiet Wife"

LANG = {
 "de": {
   "src": BASE + r"\German\manuscript.md",
   "out": BASE + r"\German\DieStilleFrau.epub",
   "title": "Die stille Frau",
   "author": "Rishabh",
   "lang": "de",
   "subtitle": "Die Elena-Vance-Reihe \u00b7 Band 1",
   "subject": "Fiction, Thriller, Psychologisch",
   "desc": "Elena Vance liest Menschen, als w\u00e4re es ihr Beruf. Sie hat nie vers\u00e4umt, es kommen zu sehen. Bis ihr Mann in kleinen, allt\u00e4glichen Dingen an ihr abzugleiten beginnt.",
 },
 "es": {
   "src": BASE + r"\Spanish\manuscript.md",
   "out": BASE + r"\Spanish\LaEsposaSilenciosa.epub",
   "title": "La esposa silenciosa",
   "author": "Rishabh",
   "lang": "es",
   "subtitle": "La serie de Elena Vance \u00b7 Libro 1",
   "subject": "Ficci\u00f3n, Thriller, Psicol\u00f3gico",
   "desc": "Elena Vance lee a la gente para ganarse la vida. Nunca ha dejado de ver venir las cosas. Hasta que su marido empieza a escabullirse de ella en peque\u00f1as formas cotidianas.",
 },
 "fr": {
   "src": BASE + r"\French\manuscript.md",
   "out": BASE + r"\French\LEpouseSilencieuse.epub",
   "title": "L\u2019\u00e9pouse silencieuse",
   "author": "Rishabh",
   "lang": "fr",
   "subtitle": "La s\u00e9rie d\u2019Elena Vance \u00b7 Livre 1",
   "subject": "Fiction, Thriller, Psychologique",
   "desc": "Elena Vance lit les gens pour vivre. Elle n\u2019a jamais manqu\u00e9 de voir venir les choses. Jusqu\u2019\u00e0 ce que son mari commence \u00e0 lui \u00e9chapper par petites fa\u00e7ons ordinaires.",
 },
}

META_TMPL = """---
title: "{title}"
author: "{author}"
lang: {lang}
publisher: "Self-published"
rights: "All rights reserved"
subject: "{subject}"
description: "{desc}"
---
"""

def build(code):
    L = LANG[code]
    metafile = ASSETS + r"\meta_" + code + ".yaml"
    with open(metafile, "w", encoding="utf-8") as f:
        f.write(META_TMPL.format(**L))
    cmd = [PANDOC, L["src"],
           "--metadata-file=" + metafile,
           "--epub-cover-image=" + COVER,
           "--css=" + CSS,
           "--toc", "--toc-depth=2",
           "--epub-chapter-level=2",
           "-f", "markdown", "-t", "epub3",
           "-o", L["out"]]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print("FAIL", code, r.stderr); sys.exit(1)
    print("EPUB written:", L["out"], os.path.getsize(L["out"]), "bytes")

for code in ("de","es","fr"):
    build(code)

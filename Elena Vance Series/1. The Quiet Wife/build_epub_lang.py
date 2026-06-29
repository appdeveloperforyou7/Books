# -*- coding: utf-8 -*-
"""Build EPUB3 editions for The Quiet Wife — DE/ES/FR, same pipeline as the English epub (pandoc)."""
import subprocess, os, sys

PANDOC = r"C:\Program Files\Pandoc\pandoc.exe"
ASSETS = r"E:\Temp\kilo\epub_assets"
CSS    = ASSETS + r"\stylesheet1.css"
COVER  = ASSETS + r"\cover.jpg"
BASE   = r"D:\Kapil\Books\Elena Vance Series\1. The Quiet Wife"

LANG = {
 "de": {
   "src": BASE + r"\German\manuscript.md",
   "out": BASE + r"\German\DieStilleFrau.epub",
   "title": "Die stille Frau",
   "author": "Rishabh",
   "lang": "de",
   "subtitle": "Die Elena Vance Reihe \u00b7 Band 1",
   "subject": "Fiction, Thriller, Psychologisch",
   "desc": "Elena Vance liest Menschen, als w\u00e4re es ihr Beruf. Sie hat nie vers\u00e4umt, es kommen zu sehen. Bis ihr Mann in kleinen, allt\u00e4glichen Dingen an ihr abzugleiten beginnt.",
   "cover": BASE + r"\German\Kindle cover.png",
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
   "cover": COVER,
 },
 "fr": {
   "src": BASE + r"\French\manuscript.md",
   "out": BASE + r"\French\LEpouseSilencieuse.epub",
   "title": "L\u2019épouse silencieuse",
   "author": "Rishabh",
   "lang": "fr",
   "subtitle": "Série Elena Vance \u00b7 Livre 1",
   "subject": "Fiction, Thriller, Psychologique",
   "desc": "Elena Vance lit les gens pour vivre. Elle n\u2019a jamais manqué de voir venir les choses. Jusqu\u2019à ce que son mari commence à lui échapper par petites façons ordinaires.",
   "cover": BASE + r"\French\Kindle cover.png",
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
           "--epub-cover-image=" + L.get("cover", COVER),
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

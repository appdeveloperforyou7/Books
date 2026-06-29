# Visual Audit — chapter9_FINAL.pdf (WeasyPrint) vs chapter9.pdf (Chrome)
*Method: every page described factually via vision model (zai MCP) + Sanskrit verified against the
**PDF text layer** (ground truth). Vision/OCR is unreliable for Devanagari, so all Sanskrit conclusions below
come from the text layer, not the image description.*

## 🔴 CRITICAL FINDING — Sanskrit is corrupted throughout (WeasyPrint)
Every Devanagari verse line AND the divider title in the **WeasyPrint** PDF contains junk Latin glyphs
(ȫ Ȭ Ȫ Ȩ ȱ Ȱ ȴ ă ȳ ȭ ɂ) replacing conjuncts. Verified from the text layer:

| Page | Rendered (corrupt) | Should be (correct, per file 20) |
|---|---|---|
| 1 | राज**ȫ**विद्याराजगुह्ययोगः | राजविद्याराजगुह्ययोगः |
| 3 | प्रकृ**Ȭ**तिः सूयतिे … हेतिुनानेन … जग**Ȫ**द्विप**Ȩ**रवितिर्तिे | प्रकृतिः सूयते … हेतुनानेन कौन्तेय जगद्विपरिवर्तते |
| 5 | अनन्या**ȱ**श्चिन्तियन्तिो … पयुर्तपासतिे | अनन्याश्चिन्तयन्तो मां ये जनाः पर्युपासते |
| 7 | … प्रयच्छ**Ȭ**ति … अश्ना**ȭ**म | … प्रयच्छति … अश्नामि |
| 8 | … द्विेष्योऽ**ȴă**ति न **ȫ**प्रयः … | … द्वेष्योऽस्ति न प्रियः … |
| 9 | अ**ȫ**प चेत् … **Ȫ**ह सः … **ȱ**क्षप्रं … | अपि चेत् … हि सः … क्षिप्रं … |
| 10 | मां नम**ă**कुरु … युक्त्विैवि…ैष्य**Ȱ**स | मां नमस्कुरु … ऐष्यसि |

**The Chrome-rendered PDF is CLEAN** — 0 corrupt verse lines; all conjuncts correct.
→ **Conclusion: WeasyPrint cannot be used (Devanagari shaping/subset bug). Chrome is the required renderer.**

## 🟠 LAYOUT FINDING — White margins around the cream page (all content pp. 2–11)
On every content page the cream "paper" fills only the **content box**; the `@page` margin area stays **white**.
Every page therefore reads as a **beige block sitting on white paper**, not as a uniformly cream page — and it
clashes with the full-bleed saffron divider (p1) and diagram (p12), which bleed edge-to-edge.

## 🟡 PAGINATION FINDING — boxes orphaned from their verse
- 9.22 verse sits on p5 but its Bridge / Sādhana / "What it is NOT" boxes spill onto **p6**.
- 9.26's Sādhana ("leaf practice") box is orphaned to the **top of p8**, separated from the 9.26 verse on p7.
→ Verse blocks break across pages; boxes detach from their verse.

## 🟢 STRUCTURE (what renders correctly)
- Trim **8.0 × 10.0 in** on all 12 pages. Running head (italic title L / small-caps chapter R) + centred folio present on pp. 2–11.
- Full-bleed saffron divider (p1) and diagram (p12) bleed correctly; the OM (ॐ) renders.
- Path-coded callout boxes (saffron Bridge / plum Sādhana / slate Adept / amber "What it is NOT") render with correct fills + left borders on pp. 4,6,8,9.
- IAST accented Roman (ṣ ṛ ṃ ḥ ā ī) renders correctly (Noto Serif).
- Real embedded fonts confirmed (Source Serif 4, Noto Serif, Inter, Noto Serif Devanagari).

## ⚠ METHODOLOGY NOTE
The vision model **cannot reliably read Devanagari** — it read corrupt 9.10 as "fine" on p5, hallucinated an
extra ॐ on p9, and misread the divider title. **Sanskrit must be QA'd from the PDF text layer, never from the image.**

## RECOMMENDED FIX PATH
1. **Switch renderer to headless Chrome** (proven correct Devanagari) — render at `@page{margin:0}` so cream
   fills the whole sheet (kills the white-margin issue).
2. **Stamp running heads + folios in post** with PyMuPDF (Chrome can't emit `@page` margin boxes), skipping
   the full-bleed divider/diagram pages.
3. **Group each verse + its boxes** in a `break-inside:avoid` wrapper so a verse never detaches from its
   Bridge/Sādhana/Adept boxes.
4. **Re-run the text-layer Devanagari integrity check** on every verse of the new PDF before sign-off.

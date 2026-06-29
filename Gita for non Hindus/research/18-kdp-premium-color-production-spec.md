# 18 — KDP Premium Full-Color Production Specification

> *This book ships as a **premium, full-color, illustrated hardcover & paperback via Amazon KDP**. Full color
> is not an extravagance here — it is a functional element (the path color-coding of file 17 only works in
> color, and the diagrams/Sanskrit-art demand it). This file is the print-ready engineering spec.*

## 1. Edition line-up (the KDP product family)

| Edition | Format | Trim | Interior | Purpose |
|---|---|---|---|---|
| **Flagship** | **Hardcover, case laminate (or cloth + jacket)** | **8" × 10"** | Premium Color, 60# white | the gift/artifact object |
| **Mass** | **Paperback** | **8" × 10"** | Premium Color, 60# white | the everyday reader copy |
| **Digital** | Kindle (KFX/Print Replica + reflowable) | n/a | full color (RGB) | audio-linked enhanced e-book |
| **Companion** | App / microsite | n/a | n/a | sādhana tracker + chanting audio |

*Note: KDP supports **8" × 10"** for **both paperback and hardcover**, and **Premium Color** on both. Print
Replica preserves the designed color layout on Kindle.*

## 2. Trim size — 8" × 10" (LOCKED)
- The extra width vs. 7×10 is absorbed by the **Adept outer margin rail** (Layer 3) and breathing room —
  *not* by longer text lines, so readability stays optimal (45–66 char measure).
- Tall enough for **Devanagari hero type** above each verse and for **full-color diagrams** to breathe.
- Reads as a **coffee-table keepsake / illustrated classic** — matches the premium, once-in-a-century intent.
- Holds comfortably in lap/two-handed; this is a practice companion, not a commuter paperback.
- KDP-supported for hardcover + paperback, Premium Color.

## 3. Color & paper
- **Interior color:** **Premium Color** (better ink saturation, richer photos/art than Standard Color).
- **Paper:** **60# (90 GSM) white** (the only KDP paper for Premium Color). Slightly thicker → more pages,
  fuller spine → a more substantial, premium object.
- **Cover (paperback):** choose **matte** (premium, calm, fingerprint-resistant; suits the "sacred-modern"
  aesthetic better than gloss).
- **Cover (hardcover):** **case-laminate matte** (durable, modern) — or cloth-wrapped spine + dust jacket for
  the ultra-premium collector edition.
- **Page-count budget:** design for **~440–480 pp** at 60# white; recompute spine width for the cover
  template (KDP computes it: page count × paper thickness + cover).

## 4. Color profile (designing for predictable print)
- **Work in CMYK** for the print editions. Embed the profile: **FOGRA39 / Coated FOGRA39 (ISO 12647-2:2004)**
  (KDP's EU press baseline) or **U.S. Web Coated SWOP v2**.
- Keep critical text **100% K** (pure black) for crispness; use **rich black** (C60 M40 Y40 K100) only for
  large dark backgrounds.
- Total ink coverage **≤ 300%** (KDP limit) to avoid set-off.
- The e-book/app uses the **sRGB** versions of the same palette.
- **Lock the palette's exact CMYK values early** and proof a physical KDP proof before mass printing.

## 5. Path color-coding — exact palette (CMYK + HEX), now production-locked
*(These four colors are the book's navigation system — they must print consistently.)*

| Path | Accent | CMYK | HEX | Used for |
|---|---|---|---|---|
| **Karma** (action) | Sage/jade | C70 M15 Y45 K10 | `#3E9C73` | verse tags, chapter tabs, diagrams |
| **Bhakti** (devotion) | Saffron-amber | C10 M65 Y95 K0 | `#D98A1E` | verse tags, pull-quotes, the sacred |
| **Jñāna** (knowledge) | Slate blue | C80 M45 Y15 K10 | `#335A8C` | verse tags, philosophical notes |
| **Dhyāna** (meditation) | Plum/maroon | C40 M85 Y30 K20 | `#8C3A55` | Sādhana boxes, meditation verses |
| Base ink | Indigo-black | C70 M60 Y50 K90 | `#1B1A2A` | body text |
| Base paper | Warm cream | C5 M5 Y12 K0 | `#FAF6EC` | page background (full-bleed tint) |

*Page background = a subtle full-bleed warm-cream tint (uses color, but creates the calm, tactile, premium
feel — worth the cost on a premium book).*

## 6. Bleed, margins, gutters (KDP rules) — 8" × 10"
- **Bleed ON** (because of full-bleed page tints, chapter dividers, and edge art).
  - Add **0.125" (3.2 mm) bleed** to top, bottom, and outer edge.
  - Export trim size **8.25" × 10.25"** with bleed (8 + 0.125×2 = 8.25).
- **Gutter** by page count (KDP recommendation): at **~460 pp → use 0.625"** gutter (inner margin).
- **Outer margin:** keep **≥0.5"** and design the **Adept margin rail** within it; no critical content within
  0.25" of trim edge.
- **Safe zone:** all text inside **0.375"** of trim on non-bleed sides.
- Set **facing-page (spread) layout**; mirror margins (gutter alternates L/R).

## 7. Typography — embeddable, open-licensed (KDP-safe, zero licensing cost)
KDP requires all fonts **embedded** in the print PDF with embedding allowed. Use SIL Open Font License fonts:
- **English body serif:** **Source Serif 4** (or **Spectral**).
- **English UI/heads sans:** **Inter** (or **IBM Plex Sans**).
- **Devanagari (hero + body):** **Noto Serif Devanagari** + **Noto Sans Devanagari** (Google, OFL, gorgeous,
  full conjunct support).
- **IAST transliteration:** Source Serif italic (with combining diacritics verified).
- Embed 100% of glyphs; subset allowed but include all Devanagari + IAST combos used.

## 8. Interior layout chassis (the designed spread) — full-color version
Per facing spread, the zones are color-defined:
- **Page background:** warm-cream full-bleed tint.
- **Verse block:** a softly tinted panel keyed to the verse's **path color** (10–12% tint) — so the reader
  *sees* at a glance whether they're in a karma/bhakti/jñāna/dhyāna verse.
- **◎ Sādhana box (Layer 2):** plum-tinted panel with a distinct rule.
- **Adept rail (Layer 3):** narrow outer column, charcoal text, slate-blue rules.
- **Pull-quotes / famous verses:** set in saffron at display size — the "photograph this" moments.
- **Chapter openers:** full-bleed color divider page (one of the four path colors), large Devanagari chapter
  title as art.
- **Diagram pages:** full-color, full-bleed-optional spreads.

## 9. Covers (KDP cover templates) — paperback + hardcover
- Download **two** KDP cover templates for **8" × 10", Premium Color, with bleed**:
  one **paperback**, one **hardcover** (different spine widths/board thickness). Both bake in spine width +
  bleed + barcode zone.
- **Paperback finish:** **matte** (premium, calm, fingerprint-resistant — suits the sacred-modern aesthetic).
- **Hardcover:** **case-laminate matte** for the durable modern look (recommended); optionally a
  **cloth-wrapped spine + dust jacket** ultra-premium collector variant.
- Spine text only if **≥ 100 pages** (we are — fine).
- Design front/spine/back as one continuous wrap; barcode zone auto-generated by KDP (leave clear).
- Use the **same cover art** across both bindings for brand consistency; only the template/spine differs.
- ISBN: acquire own ISBNs for the premium/imprint edition (full control, both bindings); KDP free ISBN
  acceptable for the mass paperback.

## 10. KDP compliance checklist (must pass pre-flight)
- [ ] PDF/X-1a:2001 or PDF/X-3 (flatten transparencies) — KDP preferred.
- [ ] All fonts embedded with embedding allowed.
- [ ] CMYK, ink ≤ 300%, pure-K text.
- [ ] Bleed 0.125" on outer edges; correct trim **7.25 × 10.25" (with bleed)** file size.
- [ ] Gutter 0.625" at ~460 pp.
- [ ] No content in bleed area except background/art.
- [ ] Image resolution ≥ 300 DPI (diagrams/art).
- [ ] Page count 24–828 (we're within).
- [ ] Order a **printed proof** before release; check color saturation, gutter readability, Devanagari
  rendering, tint legibility.
- [ ] Print Replica enabled for the Kindle edition to preserve the color layout.

## 11. Cost reality & premium positioning — **$45 paperback / $65 hardcover**
- **KDP printing cost (est., 8"×10" Premium Color, ~460 pp):**
  - **Paperback** ≈ fixed $0.85 + ($0.065 × 460) ≈ **~$30.75/copy**.
  - **Hardcover** ≈ that + case/board premium ≈ **~$35–38/copy**.
- **Royalty (KDP = 60% × (list − print cost)):**
  - **Paperback @ $45** → 0.60 × (45 − 30.75) ≈ **$8.55/copy** — healthy, premium margin.
  - **Hardcover @ $65** → 0.60 × (65 − ~37) ≈ **$16–17/copy** — strong margin, befits the keepsake.
- Both are **profitable** and position the book as a **true premium artifact** — consistent with the
  full-color, layered, "once-in-a-century" intent.
- The enhanced **Print Replica Kindle** (~$14.99–19.99) and the **free companion app** are the low-cost
  digital entry points for younger readers, feeding sales toward the print objects.
- *Re-run the exact KDP cost calculator once final page count is fixed; keep list price above the print cost
  by a comfortable margin so the 60% royalty stays positive.*

## 12. Production sequence (phase plan)
1. **Lock palette + type** (file 17 §4–5 + file 18 §5,7).
2. **Build the master spread template** (file 18 §8) in InDesign (Industry standard; Affinity Publisher is a
   license-free alternative) — one InDesign book file, paragraph/character/object styles for every element.
3. **Commission the diagram suite + Devanagari hero art** (≥300 DPI, CMYK).
4. **Produce one full sample chapter** (Ch 9) end-to-end → **order a KDP printed proof** → iterate.
5. **Build the companion app/audio** in parallel.
6. **Full production** → preflight (§10) → proof → publish across hardcover, paperback, Print Replica Kindle.

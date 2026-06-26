# Layout, Typography & PDF-Tooling Spec — Senior Large-Print Activity Book Series

**Purpose:** (1) document how the best large-print senior activity books are structured — fonts, sizes, spacing, grids, margins, page architecture — so we build to proven parameters; (2) fix the concrete spec we will generate to; (3) evaluate PDF-generation tools for full control and recommend one.

**Standards referenced (established, stable):** KDP print/cover guidelines (trim, bleed, gutter, margins, paper, fonts); large-print standards (AFB / ALA / RNIB: large print ≥ 16 pt, "extra large" ≥ 18 pt); low-vision type design (APH *APHont*, RNIB *Tiresias*, Braille Institute *Atkinson Hyperlegible*); W3C WCAG contrast & legibility principles.

**Companion files:** `PLAN-…`, `CONTENTS-…`, `RESEARCH-…`, `ratings.md`.

---

## Part 1 — How the best books are structured (research synthesis)

### 1.1 The large-print standard
- **"Large print" floor = 16 pt** body (AFB/ALA/RNIB consensus). **"Extra-large / jumbo / XXL" = ≥ 18 pt** — the band our covers claim and our seniors (often low-vision) need.
- Many competitors print at ~16 pt and call it "large"; the winners that earn 4.5★+ for legibility push **body to 18 pt** and **grid letters to 20–24 pt**. That is our target.

### 1.2 Font choice (the single biggest legibility lever)
- For **low-vision / senior** readers, **high-x-height sans-serif** faces read best: larger counters, unambiguous letterforms (no serif "fuzz"), distinguishable I/l/1, O/0.
- **Purpose-designed low-vision faces:** `APHont` (American Printing House), `Tiresias LP` (RNIB), `Atkinson Hyperlegible` (Braille Institute — free, open, explicitly built to increase letter/number distinction for low vision).
- **Safe, broadly-licensed fallbacks (OFL/Apache):** `Open Sans`, `Lato`, `Source Sans 3`, `Verdana` (high x-height; note: Verdana is a system/web face, verify embedding rights).
- Serif faces (e.g., for sustained reading in novels) are **not** preferred for puzzle grids/numbers; keep the whole interior sans-serif for consistency and clarity.
- **Embed all fonts** in the PDF (KDP requirement; also prevents substitution).

### 1.3 Type sizes per element (what winners use → our spec)
| Element | Competitor "large" | Best-in-class | **Our spec** |
|---|---|---|---|
| Body / instructions | 16 pt | 18 pt | **18 pt** (floor 16, never below) |
| Puzzle grid letters (WS / scramble) | 16–18 pt | 20–24 pt | **20–22 pt** |
| Sudoku given/entry numbers | 18–22 pt | 24–28 pt | **24–26 pt** (jumbo) |
| Section / page headings | 20–24 pt | 24–30 pt | **24–28 pt** |
| Captions, word-list headers | 14 pt | 16 pt | **16 pt** (floor 14) |
| Solutions (reference, compact) | 10–12 pt | 12–14 pt | **≥ 12 pt** (legible but compact) |
| Page numbers / running headers | 12 pt | 14 pt | **14 pt** |

### 1.4 Spacing & measure
- **Leading (line spacing):** body **1.5**; word-lists 1.3–1.4; single-line within grid cells.
- **Letter/word spacing:** default tracking for the chosen font; **do not over-condense**. Slight positive tracking (+10–20) on grid letters aids scanning.
- **Measure (line length):** keep body lines ≤ ~60–65 characters for readability.
- **Alignment:** left-aligned body (avoid justified — it creates "rivers" of whitespace that slow low-vision readers). Center puzzle titles.

### 1.5 Grid geometry per activity (8.5×11, ~7.5×9.5 in usable after margins)
- **Word Search** (1 per page): grids sized to ~6.5 in wide.
  - Easy 11×11 → cell ≈ 0.60 in · Medium 13×13 → ≈ 0.50 in · Challenger 15×15 → ≈ 0.43 in. All keep letters ≥ 18 pt (Challenger at the floor; Easy jumbo at 22 pt).
  - Word list in a side/below column, 18 pt, grouped by theme; circle/highlight key in solutions.
- **Sudoku** (2 per page): 9×9 grid ≈ 4.0 in (≈ 0.44 in cell) with thick region borders (1.5–2 pt) and thin cell lines (0.75–1 pt); numbers 24–26 pt. Mini 6×6 grids larger for the Easy on-ramp.
- **Word Scramble** (2 per page): large answer slots with one box per letter (boxes ≈ 0.35–0.45 in), scrambled clue at 20 pt, optional hint line.
- **Trivia / Finish-the-Phrase** (2 per page): 18 pt question, generous write-in lines spaced 0.4 in apart; multiple-choice options clearly separated.
- **Mazes** (1 per page): vector paths, wall thickness 2–3 pt, entrance/exit marked; grid 12×12 (≈0.5 in cell) / 16×16.
- **Coloring** (1 per page): bold vector line art, stroke 2–4 pt, large open shapes.

### 1.6 Page architecture
- **One puzzle per page** for word search and mazes (full-bleed grid feel); **two per page** for sudoku, scramble, trivia (keeps page count sane).
- **Solutions grouped at the back** (compact, ≥12 pt), never inline — winners all do this; it's a strong review-protection signal.
- **Section dividers** before each activity type (large heading + theme accent); **running headers/footers** with book title + page number.
- **Front matter:** title, copyright, welcome/how-to-use (set expectations: large print, difficulty tiers), TOC, series page.
- **Consistent grid placement** (e.g., puzzle always centered in the same safe zone) so flipping through feels premium and predictable.

### 1.7 Margins, gutter, bleed, paper (KDP 8.5×11)
- **Bleed:** 0.125 in on all outer edges (full page = 8.625 × 11.25 in). Backgrounds/full-page art extend to bleed; live content stays inside.
- **Outside margins:** ≥ 0.375 in (KDP minimum); use **0.5–0.75 in** for comfort.
- **Inside (binding) gutter:** sized by KDP page-count calculator; for ~175 pp cream ≈ **0.5–0.625 in**. Keep all live content out of the gutter.
- **Safe zone:** all text/numbers ≥ 0.375 in from the trim on every edge.
- **Paper:** **cream** (reduces glare for older eyes vs white); B&W interior; matte cover.
- **Contrast:** true black (#000) on cream; never grey-on-grey or low-contrast accents for text/numbers.

---

## Part 2 — The concrete spec we will build to
| Parameter | Value |
|---|---|
| Trim | 8.5 × 11 in |
| Bleed | 0.125 in all outer edges |
| Outside margin / gutter | 0.625 in / 0.5–0.625 in (per KDP calc) |
| Safe zone | ≥ 0.375 in from trim |
| Paper / cover | Cream, B&W interior / matte cover |
| Body font | **Atkinson Hyperlegible Next** (SIL OFL 1.1 — free for commercial use + embedding). Asset: `Atkinson_Hyperlegible_Next/static/` → use the **static instances** (Regular / Medium / SemiBold / Bold + italics). Do **not** use the root `*-VariableFont_*.ttf` files — ReportLab cannot embed variable-font axes reliably. |
| Grid/number font | Same family (sans, high x-height) |
| Body size / leading | 18 pt / 1.5 |
| Grid letters | 20–22 pt (WS/scramble), 24–26 pt (sudoku) |
| Headings | 24–28 pt |
| Captions / footers | 16 pt / 14 pt |
| Solutions | ≥ 12 pt, compact, grouped at back |
| Word-search grids | 11×11 / 13×13 / 15×15 (E/M/C) |
| Sudoku grids | 6×6 mini (some Easy) + 9×9; thick region borders |
| Mazes | 12×12 (E) / 16×16 (M) vector, 2–3 pt walls |
| Coloring | bold vector line art, 2–4 pt stroke |
| Layout | WS + maze 1/page; sudoku + scramble + trivia 2/page; solutions at back |
| Font handling | Embed all fonts in PDF; CMYK or high-res RGB accepted by KDP |

---

## Part 3 — PDF-tool evaluation (full control required)

### 3.1 Hard requirements
1. **Exact 8.5×11 geometry** with bleed, margins, gutter, safe zone (KDP-compliant).
2. **Vector drawing** for word-search grids, sudoku regions, mazes, coloring line art (crisp at print; small file).
3. **Font embedding** incl. low-vision TTF/OTF; exact point sizes.
4. **Deterministic, reproducible** output (solver-verified seeds → identical reprints).
5. **Batch automation:** 10 interiors + 10 covers + metadata CSV from one run.
6. **Programmatic** (code-driven, version-controlled) — not a GUI/manual DTP step.
7. **Print-ready PDF** (embedded fonts, 300 DPI any raster, KDP-acceptable color).
8. **Python-friendly** preferred (matches the planned generator; easy solver/puzzle integration).

### 3.2 Candidate comparison
Criteria weighted for our use: geometry control, vector/grid drawing, font embedding, automation/batch, reproducibility, KDP-readiness, ecosystem/maturity, iteration speed, learning curve (lower better).

| Tool | Lang | Geometry control | Vector grids | Font embed | Auto/batch | Reproducible | KDP-ready | Maturity | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| **ReportLab** | Python | ★★★★★ (Canvas coords) | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | **Best fit** |
| **Typst** | Typst | ★★★★☆ | ★★★★☆ (via cetz) | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | Strong modern alt |
| **WeasyPrint** | Python | ★★★☆☆ (CSS paged) | ★★★☆☆ (SVG/CSS) | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★☆ | ★★★★☆ | Good fallback |
| **LaTeX (XeLaTeX)** | TeX | ★★★★☆ | ★★★★☆ (tikz) | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★★ | Powerful, heavy |
| **FPDF2** | Python | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★☆☆ | ★★★☆☆ | Simpler/weaker than RL |
| **Puppeteer/Playwright** | JS | ★★★☆☆ (paged media gaps) | ★★★★☆ (SVG) | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | Weak print geometry |
| **InDesign** | GUI/JSX | ★★★★★ | ★★★★★ | ★★★★★ | ★★☆☆☆ | ★★★☆☆ | ★★★★★ | ★★★★★ | Not code/batch-friendly; cost |
| **Scribus** | Py script | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | Slower DTP loop |

### 3.3 Detail on the top candidates

**ReportLab (Python) — RECOMMENDED.**
- Two layers: **Canvas** (absolute coordinate drawing → perfect for puzzle grids, sudoku region borders, maze paths, page geometry) and **Platypus** (flowables for body text, TOC, solutions pagination).
- Embeds TTF/OTF (Atkinson Hyperlegible/Open Sans), CMYK or RGB, precise point sizes, vector primitives, barcode/badge-free custom drawing for covers.
- Deterministic: feed fixed seeds → byte-stable reprints; trivial to integrate with our Python puzzle generators + solvers.
- Mature (decades), MIT-licensed, huge KDP/print-PDF precedent, no external runtime/binary.
- **Downside:** verbose API; manual pagination for mixed layouts. Acceptable — our layouts are templated and repeated ×10.

**Typst — strongest modern alternative.**
- Fast compile, superb default typography, code-based, reproducible, TTF embedding, vector via the `cetz` package.
- **Downside:** newer ecosystem (2023+); fewer ready puzzle/KDP examples; binary toolchain; would reimplement some puzzle rendering. Keep as the option if we later prioritize typography polish/iteration speed.

**WeasyPrint (Python) — fallback.**
- HTML/CSS → PDF with solid paged-media + SVG support; easy text layout.
- **Downside:** less fine-grained control over exact grid geometry/bleed than Canvas; slower on very large docs. Use only if a text-heavy, CSS-driven approach is preferred.

**Rejected for this project:** InDesign (manual/costly, not batch), Scribus (slower loop), Puppeteer/Playwright (weak precise paged-media/bleed/gutter control for print books), FPDF2 (strictly weaker than ReportLab), LaTeX (powerful but slow compiles, steep curve, overkill).

### 3.4 Recommendation
**Use ReportLab (Python)** as the generation engine. It satisfies every hard requirement, matches the planned Python toolchain and solver integration, gives full Canvas-level control over KDP geometry and vector puzzle grids, embeds our low-vision fonts, and scales cleanly to the 10-book batch + covers + metadata. This aligns with the build plan's existing ReportLab module structure.

- **Fallback path:** if typography/iteration becomes a bottleneck, port layout to **Typst** (keep puzzle generation/solvers in Python, emit Typst). Cover/badge rendering can stay ReportLab or move to Typst.
- **Tooling posture:** keep puzzle *generation + verification* in Python (ReportLab-independent) so the rendering layer is swappable.

---

## Part 4 — Risks & mitigations
| Risk | Mitigation |
|---|---|
| Font license blocks commercial use/embedding | **Cleared:** Atkinson Hyperlegible Next is SIL OFL 1.1 (embed + sell allowed; document use is not bound by the license). Embed the static TTFs (from `static/`) in every PDF; avoid the variable-font files. |
| Gutter eats grid letters | Respect KDP gutter per final page count; add a QA check that no live content enters the gutter zone. |
| Compact solutions become illegible | Keep solutions ≥ 12 pt; 4-up WS grids max; never shrink sudoku keys below 14 pt. |
| Challenger 15×15 grid letters too small | Cap at 18 pt floor; if legibility fails in QA, drop to 14×14 or enlarge page grid area. |
| Bleed/trim drift between books | One shared page-template module used by all 10 books; geometry asserts in QA. |
| Tool lock-in | Keep generation/solvers decoupled from ReportLab (swappable render layer). |

---

## Part 5 — Integration with the build plan
- **PLAN module 1 (Project setup):** config = the Part 2 spec table; theme registry; font embedding.
- **PLAN module 3 (Generators):** emit per-type grids at the Part 2 sizes via ReportLab Canvas.
- **PLAN module 6 (Layout engine):** page templates (1/page for WS+maze; 2/page for sudoku/scramble/trivia), solutions-at-back assembler.
- **CONTENTS doc:** difficulty tiers + counts (unchanged); grid sizes now fixed here.
- **ratings.md:** Legibility (A) and Production (E) scores assume this spec is realized.

---

## Change log
- v1: created. Synthesized large-print/low-vision typography standards into a concrete spec (Atkinson Hyperlegible, 18 pt body, jumbo grids, cream, KDP geometry); evaluated 8 PDF tools; recommended ReportLab with Typst fallback; risks + integration map.

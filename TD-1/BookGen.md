# Book Generation Guide — The Glitch Squad Series (TD-1) — Geronimo Edition

> *"A Geronimo Stilton-style book with circuits. Colored keywords burst from every page. Sound effects CRASH through text. Every spread is an experience."*

---

## 1. Architecture Overview

```
Manuscript_v3.md  +  manifest_clean.json  +  Images/  +  VisualStyleGuide.md
         |                    |                    |              |
         v                    v                    v              |
    parse_manuscript()   load_manifest()     compress_images.py  |
         |                    |                    |              |
         +--------+-----------+--------+-----------+              |
                  |                    |                          |
            build_book.py (Geronimo parser) <--------------------+
                  |      ~M:text~ → colored spans
                  v
         BookN/Output/BOOK.html  +  book-print.css
                  |
           generate_pdf()  (WeasyPrint — native CSS Paged Media)
                  |
                  v
         BookN/Output/BOOK.pdf  (5.5" x 8.25")
```

**Design philosophy (from VisualStyleGuide.md):**
- "Like a kid's desk after a creative explosion — messy, alive, full of personality"
- No page should look like it belongs in a textbook
- Every character has FIXED visual treatments for instant recognition
- The book itself glitches during Gridlord chapters

**Writing philosophy (from VoiceGuide.md):**
- Every character's dialogue must be identifiable without name labels
- Funny-first, adventurous-second — laugh lines in every chapter
- Emotional beats are earned through action, not stated explicitly
- Show, don't tell. Specific, never generic. Trust the reader.

---

## 2. Directory Structure

```
TD-1/
├── BookLayout/
│   ├── build_book.py              # Builder (book-agnostic, --book N flag)
│   ├── compress_images.py         # PNG->JPEG compression
│   ├── generate_sample_images.py  # Sample chapter image generator
│   └── css/
│       ├── book.css               # Full CSS with all clip-paths, voice pages (760 lines)
│       └── book-print.css         # Print-optimized CSS used by builder
├── Images/                        # Shared across ALL books
│   ├── Cards/                     # Character trading cards
│   ├── ChapterHeaders/            # Chapter vignettes
│   ├── Dividers/                  # Section divider images
│   ├── Marginalia/                # Blip emotional marginalia (256x256)
│   ├── Maps/                      # City/map illustrations
│   ├── Blueprints/                # Gadget blueprint diagrams
│   ├── Spots/                     # Extra spot illustrations
│   ├── Strips/                    # Horizontal strip panoramas (1024-1556 x 256)
│   ├── Documents/                 # In-story documents/notes
│   └── *.png                      # Main illustrations
├── Book1/
│   ├── Manuscript_v2.md           # Revised manuscript (24,532 words, 36 chapters)
│   ├── manifest_clean.json        # Valid JSON manifest (171 images)
│   └── Output/
│       ├── THE_LOST_SIGNAL.html   # Generated HTML with external CSS
│       ├── THE_LOST_SIGNAL.pdf    # Final PDF (~12.6 MB, 365 pages)
│       ├── book-print.css         # Copied from BookLayout/css/
│       ├── images/                # Compressed JPEGs (~14 MB)
│       │   ├── strips/            # Compressed strip images
│       │   ├── panels/            # Auto-sliced comic panels (generated at build time)
│       │   └── *.jpg              # Main illustrations
│       └── Archive/               # Reference files
│           ├── sample_final.html  # Self-contained sample (14 pages, inline CSS)
│           └── The_Glitch_Squad_Sample.pdf  # TARGET reference PDF
├── VisualStyleGuide.md            # Design specification (THE authority)
├── ImageGen.md                    # Image generation guide
├── BookGen.md                     # THIS FILE
└── MCPObservations.md             # Cross-book image database
```

---

## 3. Text Treatments (Per VisualStyleGuide Section 6.5)

Every character has a FIXED visual treatment. A child should instantly recognize who's speaking from styling alone.

### Maya (Olive Green #556B2F)
- Name: `MAYA:` in olive green, bold, 11pt
- Text: Standard body font, normal weight
- Catchphrase: `"I can fix that/anything"` — 16pt bold, olive green, faint green background pill
- Page tint: #F5F8F0 (faint green)
- Frame shape: `.frame-gear` (asymmetric border-radius + olive border + padding)

### Leo (Navy Blue #1B1F3B)
- Name: `LEO:` in navy blue, bold, 11pt
- Text: Standard body font, normal weight
- Catchphrase: `"Error 404: ..."` — 16pt bold, navy, faint blue background pill
- Tech explanations: `.leo-tech` class — 11pt, indented, border-left navy, denser
- Page tint: #F0F2F8 (faint blue)
- Frame shape: `.frame-screen` (monitor shape with thick border + box-shadow)

### Zara (Goldenrod #DAA520)
- Name: `ZARA:` in golden yellow, bold, 11pt
- Text: Standard body font, normal weight
- Catchphrase: `"Hold on, let me DRAW the plan."` — 16pt bold, gold, faint yellow background pill
- Page tint: #FFF8E8 (faint warm yellow)
- Frame shape: `.frame-splatter` (dashed gold border + organic border-radius)

### Sam (Crimson Red #E63946)
- Name: `SAM:` in bright red, bold, 11pt
- Text: Standard body font — but Sam's lines are SHORT. One-liners. Punchy.
- Catchphrase: `"CHALLENGE ACCEPTED!"` — 16pt BOLD ALL CAPS, red, faint red background pill
- Sam's excitement shown through ALL CAPS and exclamation marks, never font tricks
- Page tint: #FFF0F0 (faint warm blush)
- Frame shape: `.frame-starburst` (circular with red border + glow shadow)

### Blip (Cyan #00BCD4) — Most Distinctive
- Name: `BLIP:` in cyan, **monospace font** (Fira Code), 10pt
- Text: Wrapped in **【corner brackets】**, **monospace font**, **cyan color**, 12pt
- Background: **faint cyan tint** (rgba(0,188,212,0.06)) behind the entire dialogue block
- LED face: Always shown as emoji-like face in margin next to dialogue
- Blip faces have **varying colors**: cyan (happy), red (scared), orange (confused), purple (thinking), yellow (excited)
- Page tint: #F0FAFB (faint cyan)
- Frame shape: `.frame-blip` (18% border-radius, matches Blip's body)

### The Gridlord — NO Name Label
- Name: **NO "GRIDLORD:" label**. Voice comes from the text itself.
- Text: **Purple (#4B0082), 14pt, bold italic**, with scanline texture behind
- Style: `.gridlord-voice` — pull-quote format, purple left border, faint purple background
- No quotation marks — the Gridlord doesn't "speak," the Gridlord IS the text
- `.glitch-block` highlights specific words (LOCKED, glitch) with purple background, white text
- Detected automatically by keyword matching (well/well, interesting, level one, solve this, locked, watching, made of, little cube)

### Daadi (Brown #8B4513)
- Name: `DAADI:` in warm brown, bold
- Text: Standard body font
- No catchphrase, but her wisdom is often styled as pull-quotes

### Narrator / Body Text
- Standard body text, warm charcoal (#2D2D2D)
- Never colored unless it's a pull-quote
- Pull-quotes: italic, bold, bordered left in relevant character color

---

## 4. Page Types (From VisualStyleGuide Section 2)

| Type | Description | Current Implementation |
|------|-------------|----------------------|
| **TYPE A** Story Text | 150-300 words, Blip marginalia, spot illustrations | DONE Default page type |
| **TYPE B** Half-Illustration | 40-60% illustration, text flows around | DONE `.illustration-half.align-right` |
| **TYPE C** Full-Page | Full bleed, max one line of text | DONE Full-bleed `<img>` |
| **TYPE D** Action Sequence | Sound effects, comic panels, fast action | DONE 2x2 / 3x2 comic grids |
| **TYPE E** Double-Page Spread | Continuous image, minimal text | NOT IMPLEMENTED (single pages only) |
| **TYPE F** Glitch Page | Text warps, scanlines, uncomfortable | DONE `.glitch-page` + `.scanlines` |
| **TYPE G** Data/Blueprint | Found documents, code screens | CSS exists, not auto-generated |
| **TYPE H** Character Voice | Page design shifts per character personality | CSS exists (`.voice-maya`, etc.), not auto-triggered |

---

## 5. Image Frame Shapes (Per VisualStyleGuide Section 3)

Images are NEVER in plain rectangles. Each character has a signature frame shape.

**CRITICAL: Use WeasyPrint's native CSS Paged Media for PDF rendering.**
- WeasyPrint supports `@page`, `@bottom-center`, and margin boxes directly — no need for separate `footer_template`.
- Fonts are embedded from local `fonts/` directory (downloaded once, reused forever).
- Image quality is print-native (300 DPI equivalent) — no Playwright scale workarounds needed.
- The `book-print.css` `@page` rules (`@page { size: 5.5in 8.25in; margin: ... }`) are rendered natively.

### PDF-Safe Frame Implementations

| Character | Frame Class | Visual Effect | CSS Technique |
|-----------|------------|---------------|---------------|
| Maya | `.frame-gear` | Organic blob, olive border | `border-radius: 30% 70% 70% 30%` + olive border + padding + shadow |
| Leo | `.frame-screen` | Monitor/screen | `border-radius: 12px` + thick dark border + double box-shadow |
| Zara | `.frame-splatter` | Paint splatter, gold | `border-radius: 60% 40% 30% 70%` + dashed gold border + padding |
| Sam | `.frame-starburst` | Circle with glow | `border-radius: 50%` + red border + red glow shadow |
| Blip | `.frame-blip` | Rounded square | `border-radius: 18%` + cyan border + cyan shadow |

Frame shapes are auto-assigned per chapter based on `FRAME_FOR_CHAR` dictionary.

---

## 6. Comic Strip Layout System

### The Problem
Strip images are generated as wide horizontal panoramas (1024-1556 x 256 px). If rendered as-is, they appear as thin horizontal bars at the top of a page with most of the page blank.

### The Solution: Panel Slicing
The builder automatically slices strip images into individual panels and arranges them as full-page comic grids.

**Flow:**
1. `slice_strip_panels(strip_file, compressed_dir, output_dir)` — slices strip into N panels
   - Width <= 1100: 4 panels (2x2 grid)
   - Width <= 1400: 5 panels (3x2 grid)
   - Width > 1400: 6 panels (3x2 grid)
2. Panels saved to `Output/images/panels/` as JPEGs at 300 DPI
3. `render_comic_page(panels, char, ...)` — creates full-page HTML grid with:
   - CSS Grid layout (`grid-template-columns` / `grid-template-rows`)
   - Character-colored panel borders (rotating: Maya/Sam/Leo/Blip/Zara/Glitch)
   - Speech bubbles with character-colored names (white bg, rounded, black border)
   - SFX text overlays (large bold red text)
   - "THE GLITCH SQUAD" title bar at bottom with character icon

**Speech Bubble Pool** — 10 pre-written bubbles rotate across comic pages:
- MAYA: "I can fix that!", "Wait -- I see it!"
- BLIP: "Loading enthusiasm...", "Question mark?", "Yay!"
- SAM: "CHALLENGE ACCEPTED!", "BOOM!"
- LEO: "Error 404...", "Signal acquired."
- ZARA: "Hold on, let me draw!"

**SFX Pool** — 4 rotating SFX: KRRRZZZT!, BZZZT!, WHOOSH!, CLICK!

### CSS Classes
- `.comic-grid` — Full-bleed page container, flex column, 8.25in height
- `.comic-grid-inner` — CSS Grid with gap, flex: 1
- `.comic-grid-2x2` — 2 columns, 2 rows
- `.comic-grid-3x2` — 3 columns, 2 rows
- `.comic-panel` — Individual panel with border, relative positioning
- `.bubble` — Speech bubble overlay (white bg, black border, rounded)
- `.bubble-name.*` — Character-colored name inside bubble
- `.sfx` — Sound effect overlay (large bold, red, text-shadow)
- `.comic-title-bar` — Bottom bar with book title

### Verified Results (MCP-confirmed)
- 28 comic grid pages in Book 1
- Each fills the page with properly sized panels
- Speech bubbles with colored character names render correctly
- SFX text overlays visible
- Title bar at bottom with character icon

---

## 7. Sound Effect Colors

| Effect | Color | CSS Variable |
|--------|-------|-------------|
| KRRRRZZZT, BZZZT (electrical/glitch) | Purple | `var(--color-glitch)` |
| CLICK (mechanical/positive) | Cyan | `var(--color-blip)` |
| SPLOOSH, WHOOOOSH, BONK, BANG | Red | `var(--color-sam)` |

---

## 8. Page Background Tinting

Each chapter gets a subtle background tint matching its character owner:

| Character | Background | CSS Variable |
|-----------|-----------|-------------|
| Maya | #F5F8F0 | `--bg-maya` |
| Leo | #F0F2F8 | `--bg-leo` |
| Zara | #FFF8E8 | `--bg-zara` |
| Sam | #FFF0F0 | `--bg-sam` |
| Blip | #F0FAFB | `--bg-blip` |
| Glitch | #E8ECF0 | `--bg-glitch` |

Background is applied as inline `style="background: {bg};"` on each page-break div.

---

## 9. Blip Face Marginalia System

### Context Faces (auto-detected from text)
20+ LED face expressions detected from text content:

| Face | Emotion | Color | Trigger Words |
|------|---------|-------|---------------|
| ■‿■ | Happy | Cyan | "smiley face", "smile" |
| ●?● | Confused | Orange | "confused" |
| ○_○ | Scared | Red | "scared" |
| ●_● | Thinking | Purple | "thinking", "worried" |
| ★‿★ | Excited | Yellow | (default for positive moments) |
| △ | Antenna flat | Blue | "antenna went flat" |
| ▲ | Antenna perked | Cyan | "antenna perk" |
| ◐ ◐ ◐ | Loading | Cyan | "loading" |
| □□ | Went dark | Grey | "went dark", "went blank" |

These render inline as `.blip-context-face` (floated right, smaller, context-specific).

### Page Marginalia (every story page)
Every story text page gets a Blip margin face at the bottom-right via `BLIP_MARGIN_POOL`:
- Pool: `['■‿■', '●‿●', '◔‿◔', '◘_◘', '◎‿◎', '◆_◆', '▲‿▲']`
- Cycles through pool based on page number within chapter
- Rendered as `.blip-margin` (right-aligned, 18pt, cyan, 0.85 opacity)
- Applied in `flush_page()` function — added to EVERY story page div

**LESSON:** Blip margins are placed at the END of the HTML page div. If content overflows, WeasyPrint may place the margin on the next page. Ensure `WORDS_PER_PAGE` threshold keeps pages well-filled without overflow.

---

## 10. Page Number Handling

**LESSON:** Use WeasyPrint's native `@page` margin boxes for footers. Add `@bottom-center` to the CSS `@page` rule — WeasyPrint handles it natively without any separate template. No duplicate page numbers issue.

---

## 11. Build Command Reference

```bash
# Full book with PDF
python BookLayout/build_book.py --book 1 --pdf

# Selected chapters only (useful for testing)
python BookLayout/build_book.py --book 1 --pdf --chapters 1 6 7 13

# HTML only (no PDF)
python BookLayout/build_book.py --book 1

# Image compression (separate)
python BookLayout/compress_images.py --book 1
```

**IMPORTANT:** Running with `--chapters` OVERWRITES the output HTML/PDF. Always do a full build without `--chapters` for the final output.

### Output
```
Book1/Output/
├── THE_LOST_SIGNAL.html     # Generated HTML with external CSS
├── THE_LOST_SIGNAL.pdf      # Final PDF (target ~220-260 pages)
├── book-print.css           # Copied from BookLayout/css/
├── fonts/                   # Copied from BookLayout/fonts/ (local @font-face)
├── images/
│   ├── strips/              # Compressed strip JPEGs
│   ├── panels/              # Auto-sliced panels (generated at build time)
│   └── *.jpg                # Compressed illustrations
└── panels/                  # Sliced comic panels
```

---

## 12. Key Reference Files

| File | Purpose |
|------|---------|
| `VisualStyleGuide.md` | **THE authority** — design specification |
| `VoiceGuide.md` | **Writing authority** — character voice, humor, emotional architecture, AI prompt strategy |
| `Book1/Output/Archive/sample_final.html` | Target layout sample (14 pages, inline CSS) |
| `Book1/Output/Archive/The_Glitch_Squad_Sample.pdf` | Target PDF output (14 pages) |
| `BookLayout/css/book-print.css` | Active print CSS used by builder |
| `BookLayout/css/book.css` | Full reference CSS (760 lines, NOT used by builder) |
| `ImageGen.md` | Bonsai API image generation guide |

---

## 13. Lessons Learned

### PDF Rendering Gotchas
1. **CSS `box-shadows` and `border-radius` are preferred** over `clip-path` for frame shapes — ensure they render correctly in WeasyPrint.
2. **Use WeasyPrint's `@page` margin boxes** for headers/footers — no separate template required.
3. **The word-per-page threshold (currently 170)** controls page density. `HALF_PAGE_COST` and `SPOT_COST` deduct from the budget when images share a text page. Adjust `WORDS_PER_PAGE` in `build_book.py` to tune page count.
4. **HTML div != PDF page** — A single HTML `page-break` div can span multiple PDF pages if content overflows. Blip margins at the end of a div may appear on a different PDF page.

### Image Handling
5. **Strip images need slicing** — Horizontal panoramas (1024+ x 256) render as thin bars if not sliced into panels. Use `slice_strip_panels()` to cut into individual panels.
6. **Panel count from width** — 1024=4 panels, 1036=4 panels, 1296=5 panels, 1556=6 panels.
7. **Compressed images retain dimensions** — `compress_images.py` converts PNG to JPEG but keeps pixel dimensions. Check compressed images, not originals.

### Builder Architecture
8. **`flush_page()` is the core page emitter** — All story text pages go through `flush_page()`. This function adds Blip margin, page background, and glitch overlay.
9. **`render_chapter()` needs `output_dir`** — Required for `slice_strip_panels()` to save panel images.
10. **Chapter title pages and full-bleed images** bypass `flush_page()` — They're added directly to `html[]`.

### Verification
11. **Always build full before verifying** — `--chapters` flag overwrites the output. A test build with 4 chapters looks like the full book is missing content.
12. **MCP verification confirms:** Comic grids fill pages, speech bubbles render, character-colored names visible, Blip marginalia present on story pages, chapter titles show colored dots/divider/title.

---

## 14. Current Status & Remaining Work

### Done
- Comic strip 2x2 / 3x2 grid layout with panel slicing
- Speech bubbles with character-colored names on comic pages
- SFX text overlays on comic panels
- Blip marginalia on every story page (context + pool)
- All character dialogue formatting (names, colors, catchphrase pills)
- Gridlord voice detection and styling
- Page background tinting per chapter character
- Frame shapes (PDF-safe: border-radius + borders + shadows)
- Sound effects with contextual coloring
- Pull quotes with character-colored borders
- Chapter title pages with colored dots/divider/title

### Remaining
- **Character voice pages (TYPE H)** — CSS classes exist (`.voice-maya`, `.voice-leo`, etc.) but builder doesn't detect first-person narration shifts
- **More visual variety on text pages** — Many pages are still plain text. Need more spot illustrations, decorative corner elements, character-themed motifs
- **Page count** — Current build is 365 pages (target 208-240). Word count threshold may need adjustment
- **Book 2-10 builds** — Builder is book-agnostic but only Book 1 has been tested

---

## Book Titles

| Book | Title |
|------|-------|
| 1 | THE LOST SIGNAL |
| 2 | THE PHANTOM NETWORK |
| 3 | THE INVISIBLE MAZE |
| 4 | THE DIGITAL GARDEN |
| 5 | THE MIRROR CODE |
| 6 | THE SILENT FREQUENCY |
| 7 | THE CLOCKWORK KEY |
| 8 | THE PIXEL THIEF |
| 9 | THE LAST BEACON |
| 10 | THE FINAL REBOOT |

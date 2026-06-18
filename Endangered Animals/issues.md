# Chronicles of the Endangered — Visual QA Issues

**Date**: 2026-05-22 (v21 Square) | **Build**: v21 | **Pages**: 82  
**Format**: 8.5" × 8.5" square, 0.125" bleed | **KDP Cover**: 17.442" × 8.750" @ 300 DPI  
**Audit Method**: MCP vision AI expert book critic review of all pages below 9

---

## BUILD v19-v20 CHANGES (This Session)

### Template/Design Fixes (affect all pages)
| # | Change | File |
|---|--------|------|
| 1 | **Spread-R focal fix**: line 168 now uses inverse of JSON `focal_x` instead of hardcoded `"right"` | `generate_book.py:168` |
| 2 | **Info box redesign**: replaced `rgba(10,10,10,0.92)` with gradient `rgba(18,16,14,0.88)`→`rgba(12,10,8,0.94)`, added gold top border, softer shadow | `templates/sample_page.html` |
| 3 | **Info box - minimal variant**: lighter gradient, reduced gold border | `templates/sample_page.html` |
| 4 | **IUCN badge refined**: background fill added, softer border colors (Critical: #ff6b6b, Endangered: #ffaa44, Vulnerable: #d4a843) | `templates/sample_page.html` |
| 5 | **Labels refined**: gold tint `rgba(212,168,67,0.55)` instead of white, font-weight 500 | `templates/sample_page.html` |
| 6 | **TOC redesigned**: wider margins (0.75in×0.9in), larger row-gap (18px), bigger font (0.78rem), more whitespace | `templates/toc_page.html` |
| 7 | **Divider page refined**: `double` border corners instead of solid, lower opacity background, better gold toning | `templates/divider_page.html` |

### Focal Fixes (MCP face cutoff audit)
| # | Animal | Fix |
|---|--------|-----|
| 1-8 | Roloway Monkey, Sunda Pangolin, Chinese Alligator, African Wild Dog, Okapi, Dhole, Hirola, Black-footed Ferret | `focal_x` reversed (wrong direction → 0% face visible → 100%) |
| 9-20 | Malayan Tiger, Radiated Tortoise, Cuban Crocodile, Chinese Giant Salamander, Giant Panda, Red Panda, Axolotl, Bog Turtle, Numbat, Asian Elephant, Malayan Tapir, Amami Rabbit | `focal_x`/`focal_y` adjusted for partial face cutoffs |
| 21 | Pygmy Hog | `focal_x`: left→center→right (snout at right edge) |

### Image Replacements & Animal Swaps
| # | Page | Change | Resolution | New Rating |
|---|------|--------|------------|-------------|
| 1 | P64 | Axolotl replaced with clear close-up portrait | 4272×2848 | 6→9 |
| 2 | P23 | Mountain Gorilla replaced with Sharp mother+baby photo | 3576×3576 | 6.5→8.5 |
| 3 | P9 | **Javan Rhinoceros → California Condor** (swapped) | 3560×2374 | 4→8 |
| 4 | P56 | **Saola → Kakapo** (swapped) | 3968×2232 | 5→9 |

### Page Ratings Summary
| Metric | v18 | v20 | Change |
|--------|-----|-----|--------|
| Average Score | 8.5 | 8.6+ | ↑ |
| 9-10 (Premium) | 46 | 54+ | ↑ |
| 8 (Excellent) | 33 | ~25 | ↓ |
| <8 (Needs Work) | 2 | ~3 | ↑ |

---

## REMAINING ISSUES (v20)

### 🔴 HIGH — Must reach 9
| Page | Animal | Score | Issue | Fix Needed |
|------|--------|-------|-------|-------------|
| P9 | California Condor | **8** | Side profile shot, standard presentation | Find better condor portrait or adjust focal_x=left for face |
| P23 | Mountain Gorilla | **8.5** | Minor softness in shadow areas | Post-process sharpening or better image |
| P41 | Bornean Elephant | **7** | Captive setting visible (fence, metal) | New wild elephant image |
| P50 | Polar Bear spread-L | **7** | Stock photo feel, flat lighting, generic | Better polar bear image or swap |
| P52 | Indian Rhinoceros | **7** | Info box still generic despite redesign | Info box further refinement |
| P68 | Tamaraw | **7** | Museum exhibit with glass reflections | Find wild Tamaraw photo or swap animal |

### 🟠 MEDIUM — Low Resolution Images (<2400px)
| Animal | Resolution | Notes |
|--------|-----------|-------|
| Grevy's Zebra | 900×659 | Must upscale or replace |
| Wild Bactrian Camel | 1024×768 | Must upscale or replace |
| Pygmy Hog | 1040×678 | Illustration, may be acceptable upscaled |
| Siberian Tiger | 1600×1200 | Borderline, needs upscaling |
| Snow Leopard | 1575×1181 | Borderline, needs upscaling |
| Aye-aye | 1280×853 | Borderline, needs upscaling |
| Amami Rabbit | 1280×970 | Borderline, needs upscaling |
| Tapanuli Orangutan | 1920×1280 | Borderline, needs upscaling |

### 🟡 MINOR — Spread page considerations
| Spread | Issue |
|--------|-------|
| P50-51 (Polar Bear) | Spread-L at 7/10, spread-R at 9/10. Uneven quality |
| P6-7 (Amur Leopard) | Already 9/9 ✅ |
| P10-11 (Sumatran Tiger) | Already 9/9 ✅ |
| P46-47 (Snow Leopard) | Already 9/9 ✅ |
| P48-49 (Giant Panda) | Already 9/9 ✅ |

### ⚫ ACCEPTED LIMITATIONS
| Page | Issue | Reason |
|------|-------|--------|
| P39 | Bleeding Toad: newspaper bg concept | Artistic choice, may keep as educational variant |
| P63 | Hainan Gibbon: silhouette | Powerful artistic composition, acceptable at 8 |
| P82 | Back Cover: ISBN placeholder `978-1-234567-89-0` | Needs real ISBN before KDP upload |

---

## ✅ v19-v20 FIXES LOG

| # | Issue | Fix Applied |
|---|-------|-------------|
| 1 | P6 Amur Leopard spread-L | `generate_book.py` now uses JSON `fx` instead of hardcoded `"left"` |
| 2 | P11 Sumatran Tiger spread-R | Spread-R now uses inverse of `fx` (was duplicate of spread-L) |
| 3 | P49 Giant Panda spread-R | Spread-R now uses inverse of `fx` (was duplicate of spread-L) |
| 4 | All 0%-face pages (8 total) | Source images analyzed, face locations identified, `focal_x` reversed |
| 5 | All partial-face pages (12 total) | `focal_x`/`focal_y` adjusted for optimal face visibility |
| 6 | P64 Axolotl | Replaced with 4272×2848px CC BY-SA 3.0 close-up portrait |
| 7 | P9 Javan Rhino | Swapped to California Condor (no good Javan Rhino CC images exist) |
| 8 | P56 Saola | Swapped to Kakapo (no good Saola CC images exist) |
| 9 | P23 Mountain Gorilla | Replaced with 3576×3576px Sharp mother+baby photo |
| 10 | P3 TOC | Wider margins, larger spacing, bigger font |
| 11 | P5,P45 Divider | Double-border corners, refined gold, lower opacity |
| 12 | All pages | Info box redesigned (gold gradient, gold top accent, softer shadow) |

---

## AUTOMATED QA (v21 — Square KDP)

```
82 pages | 3360×3360 uniform | ~150 MB PDF
KDP COVER: Output/KDP_Cover_Chronicles_of_the_Endangered.pdf (17.442" × 8.750")
Format: 8.5" × 8.5" square, 0.125" bleed | 8.75" × 8.75" page with bleed
DPI: 384 (interior) | 300 (cover) | RGB color mode
ISBN: 978-1-234567-89-0 (PLACEHOLDER — must replace before upload)
KDP max file size: 650 MB ✅ | Pages: 82 (min 75 ✅)
Spreads: 5 confirmed L→R continuous | Safe margin: 0.52" (min 0.375" ✅)
```

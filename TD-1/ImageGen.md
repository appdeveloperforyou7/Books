# Image Generation Guide — The Glitch Squad Series (TD-1)

> **Everything we learned generating 171 images for Book 1.** This guide covers the Bonsai server API, prompt engineering, character consistency, text handling, strip generation, MCP verification, and the text overlay pipeline. Follow these rules to get production-quality images from the first attempt.

---

## Table of Contents

1. [Bonsai Server API](#1-bonsai-server-api)
2. [Image Categories & Sizes](#2-image-categories--sizes)
3. [Art Style Specification](#3-art-style-specification)
4. [Character Descriptions for Prompts](#4-character-descriptions-for-prompts)
5. [Clothing Exclusivity Rules](#5-clothing-exclusivity-rules)
6. [Prompt Engineering Rules](#6-prompt-engineering-rules)
7. [Multi-Character Scenes](#7-multi-character-scenes)
8. [Text Handling (Generate + Overlay)](#8-text-handling-generate--overlay)
9. [Strip Generation (Panel Stitching)](#9-strip-generation-panel-stitching)
10. [Seed Management](#10-seed-management)
11. [MCP Verification Protocol](#11-mcp-verification-protocol)
12. [Text Overlay Pipeline (overlay_text.py)](#12-text-overlay-pipeline-overlay_textpy)
13. [Common Failures & Fixes](#13-common-failures--fixes)
14. [File Organization](#14-file-organization)
15. [Quick Reference: Bonsai Technical Specs](#15-quick-reference-bonsai-technical-specs)

---

## 1. Bonsai Server API

### Our Server

| Item | Value |
|------|-------|
| Address | `http://192.168.29.7:8765` |
| Health check | `GET /health` → `{"status":"ok","gpu":true,"version":"2.0-img2img"}` |
| Generate | `POST /generate` |
| **Returns** | **Raw PNG bytes** (content-type: image/png), NOT JSON |

### Python Generation Function

```python
import requests
import numpy as np
import cv2

SERVER = "http://192.168.29.7:8765"

def gen_img(prompt, seed, size=512):
    """Generate image via Bonsai. Returns numpy BGR array or None."""
    r = requests.post(f"{SERVER}/generate", json={
        "prompt": prompt,
        "negative_prompt": "",
        "width": size,
        "height": size,
        "seed": seed,
        "guidance_scale": 3.5,
        "num_inference_steps": 28,
    }, timeout=120)
    if r.status_code == 200:
        arr = np.frombuffer(r.content, dtype=np.uint8)
        return cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return None
```

### Critical: Response Format

The server returns **raw PNG bytes** directly, not JSON with base64:

```python
# WRONG
img = cv2.imdecode(np.frombuffer(r.json()["image"], dtype=np.uint8), cv2.IMREAD_COLOR)

# CORRECT
img = cv2.imdecode(np.frombuffer(r.content, dtype=np.uint8), cv2.IMREAD_COLOR)
```

### Recommended Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| `guidance_scale` | 3.5 | Higher = more prompt-following, but can over-saturate |
| `num_inference_steps` | 28 | Sweet spot for quality vs speed |
| `width`/`height` | 1024 or 512 | See Section 2 for per-category sizes |
| `seed` | Deterministic from ID | See Section 10 |
| `negative_prompt` | `""` (always empty) | Negative prompts backfire with diffusion models |

---

## 2. Image Categories & Sizes

| Category | Count/Book | Size (px) | Notes |
|----------|-----------|-----------|-------|
| Full-page illustrations | ~12 | 1024×1024 | Hero images, action scenes |
| Half-page illustrations | ~14 | 512×512 | Story beats, character intros |
| Strips (comic panels) | ~8 | 256×256 per panel, stitched | Generate per-panel, never as grid |
| Blip marginalia | 36+ | 256×256 | Circular, simple, Blip expressions |
| Chapter vignettes | 36 | 256×256 | Circular, scene-setting objects |
| Character cards | 6 | 512×512 | Character portraits |
| Maps | 2 | 768×768 | Neighborhood maps |
| Gadget blueprints | 4 | 512×512 | Technical diagrams |
| Section dividers | 5 | 768×768 | Decorative banners |
| Glitch art | 6 | 512×512 | Abstract digital corruption |
| Documents | 4 | 512×512 | Screens, memos, diagnostics |
| Endpapers | 2 | 1024×1024 | Book interior covers |

---

## 3. Art Style Specification

### The Target Style

**Vibrant cel-shaded 2D digital illustration** with these characteristics:
- Bold clean black outlines on all shapes
- Flat color fills with minimal soft shading
- Round friendly proportions, large expressive eyes
- Bright candy-color palette (warm oranges, cool blues, vivid greens)
- No photorealism, no 3D render, no watercolor, no sketch lines

### Style Prefix (NOT used in prompts)

The style description is documented here for reference. Do NOT prepend it to every prompt — it wastes tokens and dilutes the subject description. Instead, include key style keywords naturally.

Key style words to sprinkle into prompts:
- "children's book illustration"
- "cel-shaded 2D" or "flat digital cartoon style"
- "bold outlines, bright colors"
- "cheerful" / "warm" / "colorful"

### Style Keywords to AVOID
- "photorealistic" / "photo" / "realistic"
- "3D render" / "CGI" / "blender"
- "watercolor" / "oil painting" / "sketch"
- "dark" / "gritty" / "horror" (even for Gridlord scenes, keep it kid-appropriate)

---

## 4. Character Descriptions for Prompts

These are the **canonical** character descriptions optimized for Bonsai/FLUX. Use these EXACTLY in prompts — do not paraphrase or abbreviate.

### Maya (The Inventor)
```
11-year-old Indian girl, warm brown skin, dark brown messy ponytail with escaped strands and a pencil stuck in it, safety goggles on forehead, olive green utility vest with many pockets full of wires and tools, faded red rocket ship t-shirt, cargo shorts, velcro sneakers with one untied lace, modified digital watch with tiny antenna, gap-toothed grin, curious expression
```

### Leo (The Coder)
```
11-year-old Mexican-American boy, warm tan skin, short dark hair, navy blue knit beanie with pixelated heart design, rectangular black-rimmed reading glasses, oversized gray zip-up hoodie, distressed blue jeans with rips on knee, brown white high-top sneakers, focused serious expression, holding black tablet
```

### Zara (The Artist)
```
12-year-old Nigerian-British girl, rich dark brown skin, voluminous black hair twists with colorful threads woven in, high cheekbones, bright yellow crossbody bag, oversized blue denim jacket with colorful patches, colorful patterned leggings, gold hoop earrings, vintage SLR camera with yellow strap around neck, colorful beaded bracelets, warm confident smile
```

### Sam (The Gamer)
```
10-year-old Japanese-Korean boy, light warm skin, short spiky black hair shaved on sides, mischievous smile with missing front tooth, bright red crimson fingerless gaming gloves, black PLAYER 1 t-shirt, blue athletic shorts with white side stripes, red high-top sneakers with blue accents and LED soles, black over-ear gaming headphones around neck, black knee pads with stickers, energetic jumping pose
```

### Blip (The Robot)
```
small cute white boxy cube robot, rectangular body with rounded edges, square screen face with thin dark border, two large bright blue circular LED eyes with black pupils, dark red curved smile mouth, two thin white rounded stick antennas on top, two white arms with black elbow joints, two white legs with black knee joints and white rounded feet, hovering slightly off the ground, friendly cheerful expression
```

### Gridlord (The Digital Shadow)
> **ALWAYS shown on screens/monitors, never in physical form.**
```
vintage CRT computer monitor displaying a stern angular pixelated face with glowing green eyes, jagged metallic crown symbol embedded in forehead, skin rendered in shifting green-purple digital noise, sharp angular features with prominent metallic scar from forehead to cheek, short slicked-back dark hair, cascading green code text and purple static distortion around the face, retro monitor with beige casing
```

### Daadi
```
68-year-old Indian grandmother, silver white hair in soft neat bun, warm kind face with wrinkles around eyes, soft lavender cotton salwar kameez, thin gold chain necklace with small pendant, reading glasses on beaded chain around neck, standing in a cozy kitchen
```

---

## 5. Clothing Exclusivity Rules

**CRITICAL: These items belong to ONE character ONLY.** The model will bleed clothing between characters in group scenes (accepted as PARTIAL), but individual portraits MUST get these right.

| Item | Character | Notes |
|------|-----------|-------|
| Olive green utility vest | **Maya ONLY** | No other kid wears green vests |
| Blue denim jacket with patches | **Zara ONLY** | Oversized, with sewn-on patches |
| Red/crimson fingerless gaming gloves | **Sam ONLY** | No other kid wears red gloves |
| Navy blue beanie with heart patch | **Leo ONLY** | Pixelated heart design on the beanie |
| Gray zip-up hoodie | **Leo ONLY** | Other kids can wear hoodies but not gray zip-ups |

When generating multi-character scenes, accept that the model may swap clothing items. This is a known limitation (PARTIAL, accepted). For single-character images, reject if exclusivity is violated.

---

## 6. Prompt Engineering Rules

### Rule 1: No Negative Prompts
```
# BAD — negative prompts backfire with diffusion models
"girl with robot, no background, no text, no blur, no watermark"

# GOOD — just describe what you WANT
"girl with robot, white background, sharp focus, clean illustration"
```

### Rule 2: No "Neonville" or World Context
Do NOT include "in Neonville" or "Neonville city" in prompts. The model doesn't know this fictional world and it wastes tokens.

### Rule 3: "No text, no letters, no words" for Text Overlay Images
FLUX.2-Klein-4B **cannot render legible text**. It will always garble any text in the image. For images that need text (signs, labels, screens):
1. Generate the image WITHOUT text using suffix: `"no text, no letters, no words"`
2. Overlay correct text programmatically using `overlay_text.py` (see Section 12)

### Rule 4: Describe the Scene, Not the Chapter
```
# BAD — too abstract
"Maya discovers the hidden lab"

# GOOD — concrete visual description
"young Indian girl in olive green vest holding flashlight, entering small dusty underground laboratory with wooden workbench, old electronic equipment, cobwebs, single exposed lightbulb, concrete walls, warm flashlight beam cutting through dust"
```

### Rule 5: Keep Prompts Under 200 Words
FLUX.2-Klein-4B has a max sequence length of 256 tokens. Long prompts get truncated, losing details at the end. For multi-character scenes, prioritize:
1. Character appearance (most important for recognition)
2. Action/pose
3. Setting
4. Lighting/mood

### Rule 6: Specify the Background When It Matters
- **White background** ONLY for character portraits/cards
- **Scene backgrounds are part of the story** — always describe them for illustrations
- Circular vignettes (marginalia, chapter headers) naturally fade to dark edges

### Rule 7: Kids Must Look Pre-Teen (10-12)
The model sometimes makes kids look like toddlers or teenagers. Include age explicitly:
```
"11-year-old girl" — NOT "little girl" or "young girl" (risks toddler)
```

---

## 7. Multi-Character Scenes

### The #1 Problem: Blip Truncation
When a prompt includes 4 full kid descriptions + Blip, the model truncates and loses Blip's details. Blip becomes a generic white blob or disappears entirely.

**Solutions:**
- For scenes with Blip + 1-2 kids: Include full Blip description
- For scenes with Blip + 3-4 kids: Shorten Blip to `"small white cube robot with blue eyes and red smile, hovering"`
- Accept PARTIAL for Blip in large group scenes

### Character Ordering: Sam Before Leo
The model sometimes conflates the two boys (both dark-haired, similar age). **Always put Sam's description before Leo's** in the prompt to maintain their distinct appearances.

### GROUP_DESC: Eliminated
Do NOT use a shared group description like "four diverse kids standing together." Instead, include each character's FULL individual description in the prompt. Yes, this makes prompts long, but it's the only way to maintain character distinction.

### Multi-Character Template
```
[SETTING DESCRIPTION]. [SAM DESCRIPTION]. [LEO DESCRIPTION]. [ZARA DESCRIPTION]. [MAYA DESCRIPTION]. small white cube robot with blue eyes hovering nearby. [ACTION/POSE]. [LIGHTING/MOOD]. children's book illustration, cel-shaded 2D, bold outlines, bright colors
```

---

## 8. Text Handling (Generate + Overlay)

### The Problem
FLUX.2-Klein-4B **cannot render accurate text**. Any text in prompts (signs, labels, screen text, book titles) will be garbled into meaningless characters.

### The Solution: Generate Without Text + Programmatic Overlay

**Step 1: Generate image without text**
```
"...vintage CRT monitor displaying a pixelated face, no text, no letters, no words"
```

**Step 2: Overlay text using `overlay_text.py`**
```python
from overlay_text import overlay_text, overlay_text_centered

# Centered text (section dividers, titles)
img = overlay_text_centered(img, "PART ONE", y=100, font_size=55, color=(255, 200, 50))

# Positioned text (labels, document text)
img = overlay_text(img, "NEXCORP RESEARCH", x=30, y=40, font_size=24, color=(200, 150, 30))

# Map labels (subtle, with background banner)
from fix_text_maps_glitch import add_subtle_map_label
img = add_subtle_map_label(img, "MAPLE STREET", x=80, y=90, font_size=16)
```

### Text Categories and Treatment

| Category | Font | Effects | Notes |
|----------|------|---------|-------|
| Section dividers | Arial Rounded MT Bold | Glow + Shadow + Stroke | Large, dramatic |
| Map labels | Calibri | Semi-transparent banner background | Small, subtle |
| Glitch documents | Arial Rounded MT Bold | RGB shift + Scanlines + Noise | Must look corrupted |
| Blueprint labels | Arial Rounded MT Bold | Leader line from target | Hand-drawn feel |
| Character card names | Arial Rounded MT Bold | Shadow only | Clean, readable |

### Fonts Available (Windows)
- `ARLRDBD.TTF` — Arial Rounded MT Bold (primary, children's book feel)
- `comic.ttf` — Comic Sans MS (playful, alternative)
- `calibri.ttf` — Calibri (clean, for maps/documents)
- `georgia.ttf` — Georgia (serif, for formal documents)

---

## 9. Strip Generation (Panel Stitching)

### NEVER Generate Strips as a Single Image

Asking for "4-panel comic strip" in one prompt produces: inconsistent panels, wrong panel count, blurry details, unreadable tiny panels.

### Correct Method: Per-Panel Generation + NumPy Stitching

```python
import numpy as np

def generate_strip(panels, panel_size=256):
    """
    panels: list of dicts with 'prompt' and 'seed' keys
    Returns: stitched strip image (numpy BGR array)
    """
    panel_images = []
    for p in panels:
        img = gen_img(p["prompt"], p["seed"], size=panel_size)
        if img is not None:
            panel_images.append(img)
    
    if not panel_images:
        return None
    
    # Stitch horizontally with dark dividers
    divider = np.zeros((panel_size, 4, 3), dtype=np.uint8)
    stitched = panel_images[0]
    for panel in panel_images[1:]:
        stitched = np.hstack([stitched, divider, panel])
    
    return stitched
```

### Per-Panel Prompt Tips
- Each panel gets its OWN focused prompt describing only what happens in THAT panel
- Use 256×256 per panel (stitched strip becomes ~1040×256 for 4 panels)
- Keep panel prompts short and specific — one action, one moment
- Number of panels: 3-6 per strip (4 is most common)

---

## 10. Seed Management

### Deterministic Seeds from IDs

Use MD5 hash of the image ID to generate reproducible seeds:

```python
import hashlib

def seed_for(id_string):
    """Generate deterministic seed from image ID."""
    return int(hashlib.md5(f"{id_string}_notext_v2".encode()).hexdigest()[:8], 16) % 2147483647
```

### Seed Naming Convention
The suffix `_notext_v2` in the seed function ensures:
- Different seeds from the same ID if the prompt changes (`_v2` version)
- Consistency: same ID + same prompt = same image

### When to Re-seed
- If an image is rated FAIL: try 2-3 different seed suffixes before changing the prompt
- If changing prompt significantly: keep same seed to compare style differences
- Always record which seed produced the best result in MCPObservations.md

---

## 11. MCP Verification Protocol

### MCP is EYES ONLY — Never Ask for Verdicts

**Correct usage:** "Describe what you see in this image in detail"
**Wrong usage:** "Is this image good? Rate it. What's wrong with it?"

MCP describes what's actually in the image. The human makes all quality judgments.

### Verification Checklist

For each generated image, use MCP to check:

1. **Character recognition** — Can you identify which character(s) are shown?
2. **Clothing accuracy** — Are exclusive items on the correct character?
3. **Scene accuracy** — Does the setting match what the prompt requested?
4. **Text legibility** — Is any text present? Is it correct or garbled?
5. **Blip presence** — In multi-char scenes, is Blip visible and recognizable?
6. **Age appropriateness** — Do kids look 10-12, not younger?
7. **Art style** — Cel-shaded 2D with bold outlines?

### Quality Ratings

| Rating | Meaning | Action |
|--------|---------|--------|
| **PASS** | All key elements correct | Accept, move to next |
| **PARTIAL** | Mostly correct, minor issues (clothing bleed, Blip simplified) | Accept as best achievable |
| **FAIL** | Major issues (wrong character, missing elements, dark/scary) | Regenerate with different prompt/seed |

### MCPObservations.md Format

Each image entry follows this format:

```markdown
### B1-001 | mayas_workshop.png | PASS
- **Used In:** B1
- **Characters:** [who's visible, appearance details]
- **Background/Setting:** [environment, objects, lighting]
- **Color Palette:** [dominant colors, temperature]
- **Art Style:** [technique, line quality, shading]
- **Composition:** [layout, focal point, framing]
- **Text:** [any visible text, or "No visible text"]
```

---

## 12. Text Overlay Pipeline (`overlay_text.py`)

### Location
`D:\Kapil\Books\TD-1\overlay_text.py`

### Features
- **PIL-based rendering** with TrueType fonts (NOT OpenCV putText)
- **Multi-layer glow** — 3 blur levels for natural falloff
- **Gaussian-blurred drop shadow** — soft, not hard-stamped
- **Stroke/outline** — auto-adapts to background brightness
- **Color sampling** — reads surrounding artwork colors to choose text/glow colors
- **Auto color** — light text on dark bg, dark text on light bg

### Main Functions

```python
from overlay_text import (
    overlay_text,           # Position text at (x, y)
    overlay_text_centered,  # Center text horizontally
    overlay_multiline,      # Multiple lines with spacing
    overlay_label,          # Blueprint-style label with leader line
)
```

### Specialized Functions (in fix_text_maps_glitch.py)

```python
from fix_text_maps_glitch import (
    add_subtle_map_label,   # Semi-transparent banner behind text
    add_glitch_text,        # RGB shift + scanlines + noise
)
```

### When to Use Each

| Function | Use For | Example |
|----------|---------|---------|
| `overlay_text_centered` | Section dividers, titles | "PART ONE", "DISCOVERY" |
| `overlay_text` | Document text, labels, signs | "NEXCORP RESEARCH", "CONFIDENTIAL" |
| `add_subtle_map_label` | Map location names | "MAPLE STREET", "PARK" |
| `add_glitch_text` | Glitchy screen text | "HELP ME.", "THE SIGNAL." |
| `overlay_label` | Blueprint part names | "COAT HANGER", "ANTENNA" |

---

## 13. Common Failures & Fixes

### Failure: Text is Garbled
**Cause:** FLUX.2-Klein-4B cannot render text.
**Fix:** Regenerate with `"no text, no letters, no words"` suffix, then overlay text using `overlay_text.py`.

### Failure: Clothing Bleed Between Characters
**Cause:** Model conflates characters in group scenes.
**Fix:** Include FULL individual character descriptions (not abbreviated). Accept PARTIAL for 3+ character scenes. Use Sam-before-Leo ordering.

### Failure: Blip is Missing/Simplified in Group Scenes
**Cause:** Prompt too long (4 kids + Blip exceeds token limit).
**Fix:** Shorten Blip to `"small white cube robot with blue eyes and red smile"` in large group scenes. Use full Blip description only in solo/small group scenes.

### Failure: Kids Look Like Toddlers
**Cause:** Model interprets "young girl/boy" as very young child.
**Fix:** Always specify exact age: `"11-year-old girl"`, NOT `"young girl"` or `"little girl"`.

### Failure: Dark/Scary Images
**Cause:** Prompt with words like "dark", "shadowy", "ominous" triggers horror aesthetic.
**Fix:** Even for tense scenes, use "dimly lit" instead of "dark", "mysterious" instead of "scary", "dramatic lighting" instead of "horror lighting".

### Failure: Comic Panel Grid When Not Requested
**Cause:** Model defaults to grid layout for "comic strip" or "sequence" prompts.
**Fix:** Generate individual panels separately and stitch with numpy. NEVER ask for multi-panel output in a single prompt.

### Failure: img2img Makes Everything Look Like Reference
**Cause:** img2img mode forces the output toward the reference image regardless of prompt.
**Fix:** img2img has been abandoned. Always use txt2img (no init_image).

### Failure: White Background on Scene Illustrations
**Cause:** Prompt includes "simple background" or "clean background".
**Fix:** Only use "white background" for character portraits/cards. For scene illustrations, always describe the full setting.

---

## 14. File Organization

### Image Storage (Shared Across All Books)
```
TD-1/
├── Images/                    ← SHARED across all books
│   ├── Archive/               ← Old/regenerated versions
│   ├── Blueprints/            ← Gadget diagrams (GB-01 to GB-04)
│   ├── Cards/                 ← Character cards (CC-01 to CC-06)
│   ├── ChapterHeaders/        ← Chapter vignettes (CV-01 to CV-36)
│   ├── Characters/            ← Reference portraits (Maya/, Leo/, etc.)
│   ├── CharacterTemplates/    ← Template images
│   ├── Dividers/              ← Section dividers (SD-01 to SD-05)
│   ├── Documents/             ← Screens, memos (DOC-01 to DOC-04)
│   ├── GlitchArt/             ← Abstract glitch effects
│   ├── Maps/                  ← Neighborhood maps (MAP-01, MAP-02)
│   ├── Marginalia/            ← Blip expressions (BM-01 to BM-12)
│   ├── Spots/                 ← Small spot illustrations
│   └── Strips/                ← Comic strips (B1-S01 to B1-S28)
├── MCPObservations.md         ← Image database with Used In tracking
├── overlay_text.py            ← Text overlay module
├── fix_text.py                ← Text overlay regeneration script
├── fix_text_v2.py             ← Improved text overlay regeneration
├── fix_text_maps_glitch.py    ← Map labels + glitch text
├── fix_strips.py              ← Strip panel stitching
├── manifest_batch_client.py   ← Batch generation from manifest
└── Book1/
    ├── manifest_clean.json    ← Per-book generation manifest
    ├── Manuscript.md          ← Story text
    └── Outline.md             ← Story outline
```

### Image ID Convention
- `B1-XXX` — Book 1 illustrations (B1-001 to B1-040)
- `B1-SXX` — Book 1 strips (B1-S01 to B1-S28)
- `BM-XX` — Blip Marginalia
- `CV-XX` — Chapter Vignettes
- `CC-XX` — Character Cards
- `SD-XX` — Section Dividers
- `GB-XX` — Gadget Blueprints
- `DOC-XX` — Documents
- `MAP-XX` — Maps
- `TP-XX` — Title Pages
- `ES-XX` — Extra Spots
- `GA-XX` — Glitch Art
- `EP-XX` — Endpapers

---

## 15. Quick Reference: Bonsai Technical Specs

| Item | Value |
|------|-------|
| Base architecture | FLUX.2 Klein 4B (MMDiT diffusion transformer) |
| Parameters | ~4.0B (transformer trunk) |
| Transformer size | 1.21 GB (6.4× smaller than 7.75 GB FP16) |
| Compression | Ternary weights {−1, 0, +1} ≈ 1.71 bits/weight |
| Native resolution | 1024×1024 (also supports 512×512, 768×768) |
| Max sequence length | 256 tokens |
| Text rendering | **Cannot render accurate text** — always garbles |
| Negative prompts | **Do not use** — backfires with diffusion models |
| img2img | **Abandoned** — makes everything look like reference |
| License | Apache 2.0 |
| Our server | 192.168.29.7:8765, returns raw PNG bytes |

---

## Appendix A: Resources

- **Prism ML Website**: https://prismml.com
- **White Paper**: https://github.com/PrismML-Eng/Bonsai-Image-Demo/blob/main/bonsai-image-4b-whitepaper.pdf
- **Demo Repo**: https://github.com/PrismML-Eng/Bonsai-Image-Demo
- **HF Spaces Demo**: https://huggingface.co/spaces/prism-ml/Bonsai-Image-Demo
- **MLX Model**: https://huggingface.co/prism-ml/bonsai-image-ternary-4B-mlx-2bit
- **Gemlite Model**: https://huggingface.co/prism-ml/bonsai-image-ternary-4B-gemlite-2bit

## Appendix B: Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU VRAM | 6 GB | 10 GB+ |
| RAM | 8 GB | 16 GB |
| Disk | ~5 GB | ~10 GB |

> Our GTX 1650 SUPER (4 GB VRAM) is below minimum — we use the networked server instead.

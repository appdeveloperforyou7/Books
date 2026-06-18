# Image Database — The Glitch Squad Series (TD-1)

> **Shared image asset database for all books in the TD-1 series.**
> Images stored at `TD-1/Images/`. Each entry tracks which books reuse an image.

## Dashboard

| Category | Total | Gen | Pending | MCP Status |
|---|---|---|---|---|
| illustrations | 40 | 40 | 0 | 34 PASS, 6 PARTIAL (clothing bleed, accepted) |
| scene_spotlights | 14 | 14 | 0 | 12 PASS, 2 PARTIAL (see notes) |
| locations | 5 | 5 | 0 | 4 PASS, 1 PARTIAL (girl visible in LOC-02) |
| diagrams | 5 | 5 | 0 | 5 PASS |
| blip_marginalia | 12 | 12 | 0 | 12 PASS |
| chapter_vignettes | 36 | 36 | 0 | 36 PASS |
| character_cards | 6 | 6 | 0 | 6 PASS |
| maps | 2 | 2 | 0 | 2 PASS |
| gadget_blueprints | 4 | 4 | 0 | 4 PASS |
| title_page | 1 | 1 | 0 | 1 PASS (text overlaid in layout) |
| section_dividers | 5 | 5 | 0 | 5 PASS |
| glitch_art | 6 | 6 | 0 | 6 PASS |
| extra_spots | 31 | 31 | 0 | 31 PASS |
| documents | 4 | 4 | 0 | 4 PASS |
| endpapers | 2 | 2 | 0 | 2 PASS |
| **TOTAL** | **173** | **173** | **0** | **173/173 generated (100%)** |

**28 comic strips replaced with 24 visual elements (14 scene spotlights + 5 locations + 5 diagrams). All new images MCP-verified 2026-06-05. Issues noted: SS-02 shows boy instead of girl (Bonsai gender swap, minor), LOC-02 includes girl when prompt said "no people" (minor). Diagrams have garbled AI-generated text (expected — text overlaid via HTML). Character consistency is good overall with correct art style (cel-shaded 2D cartoon). All 24 images are text-free as intended.**

**All 177 images generated. 6 new extra spots (ES-26 to ES-31) generated 2026-06-02 to fill sparse pages: spring bounce (Ch1), crate stairs (Ch3), samosa plate (Ch10), basement door (Ch2), backpack crumbled (Ch1), Professor Waddles (Ch1). Title page (TP-01) and section divider (SD-01) regenerated v2 with Bonsai cityscape/robot scene + OpenCV text overlay. All 8 new/regenerated images MCP-verified with exhaustive detail. 53 manifest chapter assignments remapped from 36-ch to 19-ch structure.**

## Build Integration Status (2026-06-02)

All 171 images are wired into the Book 1 build pipeline (`BookLayout/build_book.py`).

| Category | Total | Wired | Method |
|---|---|---|---|
| illustrations | 40 | 40 | `get_chapter_images()` → `distribute_images()` → page layouts |
| scene_spotlights | 14 | 14 | `get_chapter_images()` → `distribute_images()` → `render_scene_spotlight()` (img-overlay + quote-box) |
| locations | 5 | 5 | `get_chapter_images()` → `distribute_images()` → `render_location_page()` (full-bleed) |
| diagrams | 5 | 5 | `get_chapter_images()` → `distribute_images()` → `render_diagram_page()` (blueprint-page) |
| chapter_vignettes | 36 | 19 | `render_chapter()` — one per chapter title page (`ChapterHeaders/ch{num:02d}_vignette.png`) |
| blip_marginalia | 12 | 12 | `flush_page()` — cycled via `BLIP_MARGIN_EMOTIONS` pool, one per text page |
| extra_spots | 25 | 25 | `distribute_images()` → inline float images within text flow |
| glitch_art | 6 | 6 | `distribute_images()` → full-bleed pages in Gridlord chapters (5, 7, 14, 15, 19) |
| documents | 4 | 4 | `distribute_images()` → full doc pages (chapters 14, 16, 17) |
| maps | 2 | 2 | `distribute_images()` → full map pages (chapter 12) |
| character_cards | 6 | 6 | `build_book()` → back matter section |
| gadget_blueprints | 4 | 4 | `build_book()` → back matter section |
| title_page | 1 | 1 | `build_book()` → first page |
| section_dividers | 5 | 5 | `SECTION_DIVIDERS` dict → sections at chapters 1, 6, 13, 23, 32 |
| endpapers | 2 | 2 | `build_book()` → first and last pages |
| **TOTAL** | **169** | **169** | All 169/169 images confirmed in build output (28 strips removed, 24 new visuals added) |

**Build verification:** `Book1/Output/THE_LOST_SIGNAL.pdf` — 199 pages, 19.3 MB, zero blank pages, zero comic strip references.

## PDF Build Audit v3 (2026-06-05)

**Current state:** 199 pages, 19.3 MB. Playwright PDF generation.

**Fixes applied this session (v3):**
1. **Full-bleed CSS overhaul:** Removed `display: flex; align-items: center; justify-content: center` from `.full-bleed-page`. Changed to `display: block; width: 5.5in; height: 8.25in; overflow: hidden; position: relative`. All overlay/spotlight pages now use pure inline styles (`style="break-before:page;padding:0;margin:0;position:relative;width:5.5in;height:8.25in;overflow:hidden"`) instead of CSS classes.
2. **Scene spotlights:** Switched from CSS class-based `.img-overlay` / `.img-overlay-inner` to fully inline-styled HTML with `position:absolute` quote boxes. Both location pages AND spotlight pages confirmed full-bleed via MCP edge analysis.
3. **Geronimo markup fixes:**
   - Chapter teasers: `~M:"Do not activate"~` now properly renders as colored `<span class="gk maya">` instead of literal text
   - Empty tags: `~L:~` (zero-content Geronimo tags) stripped before rendering
   - Next-page tease: `~B:turn the page!~` now renders as `<span class="gk blip">turn the page!</span>`
4. **Merge safety:** `merge_sparse_pages()` now checks both `is_special_page` AND `prev_is_special` — prevents merging content INTO location/spotlight pages. Fixed content from being appended inside `full-bleed-page` wrappers.
5. **body margin:** Added `margin: 0; padding: 0;` to `body` CSS rule.
6. **Location pages:** Confirmed `object-fit: cover` with `width:5.5in;height:8.25in` renders full-bleed edge-to-edge.

**MCP QA results (v13):**
- Pages 4, 15, 20, 25, 34, 37, 45, 54, 63, 76, 94, 118, 127, 137, 158, 178: ALL CONFIRMED FULL-BLEED
- Pages 118, 158 initially flagged as "white margins" — detailed edge analysis confirmed illustration content extends to all edges; light-colored image edges (sky, buildings) were misinterpreted as white margins
- Zero Geronimo literal text across all 199 pages
- Zero content merged into special pages

**Known remaining issues:**
- LOC-02 (location_maya_room): Shows person at desk despite "no people" prompt — needs regeneration when Bonsai server is back up
- SS-02 (spotlight_crate_discovery): Shows boy instead of girl — Bonsai gender swap, minor
- Some images have light-colored edges that may APPEAR as white margins at low DPI inspection (confirmed full-bleed at 200 DPI edge analysis)
- Some text pages are still sparse due to short dialogue exchanges — inherent to children's book layout
- Page 24: PARTIAL — upper half filled with dialogue + illustration, lower half empty (acceptable for children's book)

**Source images needing regeneration:**
- `doc_project_kira.png` — browser chrome with obscured "https://" text
- `doc_nexcorp_memo.png` — garbled text overlays ("NEX", "DATE:", "DOU")
- 5 missing spot images: `spot_spring_bounce`, `spot_backpack_crumbled`, `spot_professor_waddles`, `spot_basement_door`, `spot_crate_stairs`
- `maple_street_chaos.png` — deleted (was photorealistic 3D)

---

## Legend
- PASS = all key elements correct
- PARTIAL = mostly correct, minor clothing/count issues, accepted as best achievable
- FAIL = needs regeneration
- Generated, not yet MCP-verified = batch generated but detailed MCP review pending
- **Used In** = which TD-1 books use this image (B1 = Book 1, B2 = Book 2, etc.)

---

## Character Reference Descriptions

### Maya (The Inventor)
- 11-year-old Indian girl, warm brown skin, dark messy ponytail with pencil stuck in it
- Safety goggles on forehead, olive green utility vest full of tools, faded red rocket-ship t-shirt, cargo shorts, velcro sneakers
- Gap-toothed grin, carries screwdriver
- Clothing exclusivity: olive green utility vest is MAYA ONLY

### Sam (The Gamer)
- 10-year-old Japanese-Korean boy, light warm skin, short spiky black hair shaved on sides
- Mischievous smile, missing front tooth, bright red/crimson fingerless gaming gloves, black PLAYER 1 t-shirt, athletic shorts with stripes, high-top sneakers with LED soles
- Gaming headset around neck, knee pads with stickers
- Clothing exclusivity: red/crimson fingerless gaming gloves are SAM ONLY

### Zara (The Artist)
- 12-year-old Nigerian-British girl, rich dark brown skin, voluminous black hair twists with colorful thread
- High cheekbones, bright yellow crossbody bag, oversized blue denim jacket with patches, colorful patterned leggings, gold hoop earrings
- Vintage SLR camera with yellow strap, colorful beaded bracelets
- Clothing exclusivity: blue denim jacket with patches is ZARA ONLY

### Leo (The Coder)
- 11-year-old Mexican-American boy, warm tan skin, dark intense eyes
- Navy blue beanie with pixel heart patch, oversized gray zip-up hoodie, distressed jeans with patches, black-rimmed rectangular reading glasses, tablet in front pocket
- Silver chain necklace
- Clothing exclusivity: navy blue beanie with heart patch is LEO ONLY, gray hoodie is LEO ONLY

### Blip (The Robot)
- Small white rectangular body, square screen face with thin dark border
- Large bright blue circular LED eyes with pixel dot pattern and black pupils
- Dark red curved smile mouth, two white rounded stick antennas on top
- Two arms with black elbow joints, two legs with black knee/ankle joints, white rounded feet
- Friendly cheerful childlike appearance

### Gridlord (The Digital Shadow)
- Mysterious digital entity, never shown in physical form, always on monitors/screens
- Stern angular pixelated face with glowing green eyes, jagged metallic crown symbol embedded in forehead
- Skin rendered in shifting green-purple digital noise, sharp angular features with prominent metallic implant or scar from forehead to cheek
- Short slicked-back dark hair, surrounded by cascading green code text and purple static distortion
- Glowing orange neon crown icon above, associated with purple and green glitch effects
- **Canonical reference: B1-014 gridlord_first_appearance.png**

### Daadi
- 68-year-old Indian grandmother, silver hair in soft bun, warm kind face
- Soft lavender cotton salwar kameez, thin gold chain with pendant, reading glasses on beaded chain

---

## Illustrations (40 items)

### B1-001 | mayas_workshop.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One young girl with medium-brown skin, dark brown hair in a high ponytail, large expressive brown eyes, broad smile. Wears silver/black goggles on head, bright orange t-shirt with cartoonish white robot graphic, green utility vest with multiple pockets containing pens and scissors, olive-green shorts, tan hiking boots with white laces and blue accents, black wristwatch on left wrist, silver digital smartwatch on right wrist. Seated on wooden stool, right hand touching a green circuit board.
- **Background/Setting:** Indoor workspace/bedroom. Wooden desk with adjustable desk lamp, cups of pens/markers, vintage grey/black radio, stack of papers, green circuit board, scattered pens, white mug with dark logo, rolled-up blueprint. Wall with pinned posters (one with "QUIZ" text). Window with sunny day. Wooden dresser on right.
- **Color Palette:** Warm and earthy — browns, oranges, greens with pops of brighter colors. Warm yellow glow from desk lamp.
- **Art Style:** Clean, smooth digital lines with slightly painterly texture. Soft gradients and subtle color variations with cel-shading.
- **Composition:** Girl centered slightly right, workbench leads eye from foreground to midground to character. Background elements frame without distracting.
- **Text:** "QUIZ" on a poster (yellow on red). Other illegible text on posters, circuit board, blueprint, mug.

---

### B1-002 | basement_corridor.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters visible. The scene is empty.
- **Background/Setting:** Long, narrow corridor with rough, cracked concrete walls, floor, and ceiling. Large metallic pipes and thick black electrical cables along ceiling and walls. Extensive spider webs draped across corners. Small debris on floor. Single exposed light bulb hanging from center of ceiling. Smaller wall-mounted light fixture on left wall. Hazy, dusty atmosphere at far end.
- **Color Palette:** Muted earthy tones — dull off-white/light grey concrete, metallic silver-grey pipes, black cables, stark white spider webs. Warm yellowish-white glow from light source.
- **Art Style:** Digital painting with highly detailed textured approach. Smooth lines define concrete cracks. Soft gradients combined with detailed texturing for rough surfaces. Atmospheric lighting effects with visible dust particles.
- **Composition:** Strong linear perspective with corridor walls/ceiling converging to vanishing point at far end. Central light source positioned on vanishing point. Symmetrical along central axis. Spider webs in foreground frame the view.
- **Text:** No visible text.

---

### B1-003 | hidden_lab_discovery.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One young girl with medium-brown skin, brown hair in two high ponytails with green hair tie, large expressive brown eyes, broad smile showing teeth, flushed pink cheeks. Silver-framed goggles on forehead, yellow pencil with red eraser tucked behind right ear, black wristwatch with green digital display on left wrist. Red t-shirt with rocket ship graphic, green utility vest with pockets containing screwdriver, yellow-handled tool, black multi-tool, round red/white patch. Olive-green cargo shorts, brown/white sneakers with orange laces. Kneeling, hands clasped on lap.
- **Background/Setting:** Cluttered workshop/storage room. Left: wooden workbench with old electronics (boxy radio, device with gauge, coiled wires), poster on wall with partial text "ER... FUTURE", framed portrait, cardboard box labeled "SUNDA." Right: workbench with device with green digital display, cardboard box labeled "EVANORS." Center: concrete floor with debris, cobwebs. Single exposed lightbulb. Pipes and wires along walls.
- **Color Palette:** Earthy muted tones for background (grays, browns, olives) contrasted with brighter character clothing (red, green). Warm yellowish hue from light source.
- **Art Style:** Clean, smooth digital lines. Blend of soft gradients and defined shadows — cel-shading for character, painterly textured shading for background.
- **Composition:** Girl centered slightly left, occupying majority of frame. Background elements frame her. Light source on right balances composition.
- **Text:** Partial "ER... FUTURE" on poster, "SUNDA" and "EVANORS" on cardboard boxes. Other text illegible.

---

### B1-004 | daadi_kitchen_samosas.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One elderly woman with pale skin, white hair in neat low bun, gentle smiling face with wrinkles around eyes and mouth. Long-sleeved lavender blouse, white apron, golden-yellow beaded necklace. Standing at stovetop, right hand holding utensils over pan, left hand near pan.
- **Background/Setting:** Well-equipped kitchen. Wooden cabinets with round handles, open shelves with white mugs and glass jars. Wooden countertop with glass jars (red, green, brownish-orange lids — one labeled "TEA"). Black stovetop with silver pan containing folded food, black pot with steam, copper-colored pot. Window with white lace curtain, green foliage outside. Potted plant and wicker basket on windowsill. Light beige tiled walls.
- **Color Palette:** Warm and earthy — soft browns, beiges, yellows. Accents of lavender, red, green, pink, blue from jars and decor. Warm golden sunlight from window.
- **Art Style:** Clean, smooth, precise lines. Soft, subtle digital painting shading with smooth gradients and gentle texturing.
- **Composition:** Elderly woman centered slightly right. Kitchen elements frame her. Steam from pot adds dynamic element.
- **Text:** "TEA" on green-lidded jar label. Other jar text not fully legible.

---

### B1-005 | maya_sleeping_cube_glow.png | REGEN v2
- **Used In:** B1 (BUILD)
- **Characters:** (1) Young child with warm peachy skin, short light brown hair, lying on side asleep with eyes closed, slight smile, right arm bent with hand under cheek. White nightshirt. (2) Small boxy robot with white worn body (visible scuffs), two large glowing cyan circular eyes, wide glowing cyan smile, thin metallic antenna with blue light at tip, four small dark blue/black wheels. Sitting on bed to right of child, emitting soft warm yellowish-green glow.
- **Background/Setting:** Dark blue bedroom walls. Wooden bed with curved headboard, white pillow, light grey/off-white blanket with faint brownish stains. Large white-framed window with two panes on right, light grey curtains drawn back. Dark blue night sky with small white stars and bright white full moon with grey shading.
- **Color Palette:** Cool — various blues (walls, sky), warm peachy skin, brown wood, cyan robot glow, warm yellowish-green robot body glow. Cool white moonlight.
- **Art Style:** Smooth clean digital lines with slight painterly texture. Soft blended gradient shading, subtle shadows. Whimsical, dreamy quality.
- **Composition:** Child left two-thirds, robot on right. Window frames night sky and moon. Peaceful balanced layout.
- **Text:** No visible text.

---

### B1-006 | blip_activation.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** (1) Young girl with medium-brown skin, large expressive brown eyes, dark brown hair in high ponytail, light blue-tinted goggles on head. Broad joyful smile with mouth open. Kneeling on one knee, right hand extended toward robot. Red t-shirt with rocket ship graphic, green utility vest with pockets containing pens/tools, olive-green cargo shorts, grey sneakers, black/silver wristwatch on left wrist. (2) Small cube-shaped robot hovering in air — white slightly dusty exterior, two black circular eyes, curved blue smile, thin glowing blue antenna, two small silver wheels/legs at bottom, faint blue glow and blue sparkles around it.
- **Background/Setting:** Indoor room with wooden desk (stack of books, sheet of paper), window showing warm golden sunrise/sunset light, off-white/beige wall, framed picture of figure in white coat (scientist/astronaut), wooden cabinet/shelf with colorful books and blue box.
- **Color Palette:** Warm and inviting — earthy tones (browns, greens, beiges) with soft complementary colors (reds, blues). Warm golden window light. Cool blue robot glow.
- **Art Style:** Smooth, clean digital lines with slight hand-drawn texture. Soft painterly blended shading with subtle gradients.
- **Composition:** Girl on right, robot on left, visual connection between them. Desk and background provide context without distraction.
- **Text:** No discernible text.

---

### B1-007 | maple_street_chaos.png | REGEN v2
- **Used In:** B1 (BUILD)
- **Characters:** (1) One small boxy robot, light gray/off-white body, two large glowing blue circular eyes, small rectangular slot mouth, dark gray panel on chest, articulated arms. Mid-air jumping, propelled upward by water from fire hydrant. Water spray visible at feet. (2) One small white/light gray drone with dark gray propellers (blurred in motion), hovering above and behind robot.
- **Background/Setting:** Dark nighttime city street. Wet asphalt road with cracks, central yellow line, glistening with reflections from neon lights. Concrete sidewalks. Rust-colored (brownish-red) fire hydrant actively spraying water in wide arc with frozen droplets. Multi-story older brick/concrete buildings lining both sides with storefronts, metal roll-up shutters on most. Black trash cans on sidewalks. Small dark air conditioning unit mounted on building. Pitch black sky — no stars or moon.
- **Color Palette:** Deep blacks (sky, street), grays (buildings, robot), vibrant saturated neon (bright pink, cyan, green, yellow, orange from signs), rusty brownish-red hydrant, white water highlights, blue robot eyes.
- **Art Style:** Highly detailed 3D digital render with photorealistic environment. Wet surface reflections rendered with advanced lighting. Robot/drone characters more stylized/cartoonish contrasting with realistic setting. Cyberpunk atmosphere.
- **Composition:** Robot and hydrant centered on vertical axis. Street converges to distance with strong perspective. Buildings frame scene. Water spray adds dynamic diagonal element.
- **Text:** Neon signs with Japanese/Chinese characters on buildings. "X10" on green sign left side. Other illegible text on signs.

---

### B1-008 | leo_library.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One young boy with light brown/tan skin, dark brown/black short hair, rectangular black-rimmed glasses. Dark blue knit beanie with pixelated heart design (red, green, blue squares). Grey zip-up hoodie over dark grey/black t-shirt, distressed blue jeans with rips on left knee, brown/white high-top sneakers with white laces. Focused, slightly serious expression with furrowed brow. Crouched on wooden bench/table holding black tablet with both hands and white paper/booklet.
- **Background/Setting:** Cozy library/study room with tall wooden bookshelves filled with books of varying colors (blue, green, red, orange, yellow, brown). Some books stacked horizontally on lower shelves. Light brown wooden table. Light-colored wood plank floor.
- **Color Palette:** Warm and earthy — browns, tans, greens, blues. Soft directional lighting from left creating gentle glow.
- **Art Style:** Clean, smooth digital lines with slightly painterly quality. Soft gradient digital painting shading. Modern children's book/graphic novel style with indie game aesthetic.
- **Composition:** Boy centered slightly right. Bookshelves create depth leading eye toward him. Table creates foreground element.
- **Text:** No discernible legible text on book spines, paper, or tablet screens. Pixelated heart is a symbol.

---

### B1-009 | zara_photographing_chaos.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One young girl with dark brown skin, voluminous curly brown hair with colorful headband (red, blue, green stripes). Wide joyful smile, bright expressive eyes. Standing facing forward slightly angled right, right hand raised to chin, left hand holding black mobile phone to ear, yellow handbag on left arm. Blue denim jacket with collar and colorful patches (red/white, green/red, multi-colored cactus patch), white t-shirt with graphic print showing "NICE" in green letters with food items, galaxy-themed dark blue/purple leggings with pink/yellow star patterns. Small round silver earrings, multiple colorful beaded bracelets on right wrist. Yellow structured handbag with blue flower decoration.
- **Background/Setting:** Paved street/sidewalk with slight sheen, colorful confetti-like specks. Two-story buildings on both sides (large windows, green trash can outside left building). Classic black ornate street lamp on left. European-style town street.
- **Color Palette:** Warm and vibrant — oranges, yellows, browns from sunset light contrasting with cool blues of jacket and bright yellow bag. Muted beige/brown background buildings.
- **Art Style:** Clean, smooth consistent digital lines. Soft gradient shading with blocks of color, subtle shadow for form. Cartoonish, friendly aesthetic.
- **Composition:** Girl centrally positioned, clear focal point. Street leads eye to background buildings. Negative space draws attention to character.
- **Text:** "NICE" in green capital letters on t-shirt. Rest of shirt text not fully legible.

---

### B1-010 | sam_vaulting_bench.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One young boy with short spiky black hair, light brown/tan skin, wide joyful smile with eyes wide open. Mid-air jumping pose with outstretched arms and bent knees. Black t-shirt with "PLATTER" in white capitalized letters and small circular blue logo. Black athletic shorts with white stripe on side, small blue logo. Bright red fingerless gloves. Grey athletic sneakers with black/white accents and blue glowing soles/lights.
- **Background/Setting:** Wooden park bench with light brown slatted seat, dark metal legs. Green/yellow leafed trees with brown trunks. Lush green grass. Light brown dirt/gravel path. Light-colored wooden fence in distance. Light blue sky through tree canopy.
- **Color Palette:** Warm and earthy — greens and yellows dominant. Black clothing for contrast, red gloves and blue glowing shoes for vibrant pops. Bright golden-hour sunlight.
- **Art Style:** Clean, smooth digital lines, uniform thickness. Flat cel-shading with solid color blocks. Highly stylized and cartoonish.
- **Composition:** Boy centered, clear focal point in foreground. Park bench behind creates depth. Background elements frame without distraction. Diagonal body line creates dynamic action composition.
- **Text:** "PLATTER" in white capitalized letters on black t-shirt.

---

### B1-011 | first_meeting_room.png | REGEN v2
- **Used In:** B1 (BUILD)
- **Characters:** Five children gathered around tablet and robot in bedroom. (1) Leftmost girl — light skin, brown hair in high ponytail, blue-tinted goggles on head. Olive green utility vest over white t-shirt, olive green cargo shorts, black sneakers. Standing, hands by sides. (2) Second boy — light skin, dark brown short messy hair, black t-shirt with "PLAYER" in white letters, olive green pants, black sneakers, red gloves. Holding tablet, pointing at screen with right index finger. (3) Third girl — dark skin, black hair in high bun, denim jacket over yellow top, blue jeans, camera with strap around neck. Holding camera up to face. (4) Fourth girl — dark skin, black hair in two high puffs, denim jacket with patches, white t-shirt, colorful floral leggings (pink/yellow/green), pink shoes, yellow crossbody bag. Left hand resting on robot. (5) Rightmost boy — light skin, dark brown hair, blue beanie with pink heart, glasses, grey hoodie, blue jeans. Hands in hoodie pockets, leaning forward. Robot: small white and black with screen face showing blue text and red smile, black tripod-like legs on floor.
- **Background/Setting:** Bedroom/workshop with muted blue walls. Wooden desk left with black desk lamp, laptop, mouse, papers; blue bucket on floor. Bed with grey bedding partially visible right. Two wooden bookshelves with books, framed pictures, figurines. Window with light grey curtains on back wall. Foreground wooden table with papers, yellow pencil, blue pen, coiled yellow cable, black case. Cables/wires on floor.
- **Color Palette:** Cool blues (walls, curtains, robot screen), greens (vest, pants), browns (wood), red accents (gloves, robot smile), yellow (bag, cable).
- **Art Style:** Digital painting, clean lines, smooth shading, slightly stylized illustrative quality. Modern children's book style.
- **Composition:** Children in loose semi-circle around robot and tablet. Robot slightly right of center. Foreground table adds depth. Background shelves and desk frame scene.
- **Text:** "PLAYER" on second child's t-shirt. Blue pixelated text on robot screen (possibly "MATH"). "IRIS" on green book spine. "COLLIER" on another book.
- NOTE: 5 children instead of intended 4. Extra child may be model duplication.

---

### B1-012 | kids_in_closet.png | REGEN v2
- **Used In:** B1 (BUILD)
- **Characters:** Four children in narrow dimly lit space. (1) Left girl — light skin, brown hair in two high pigtails, large blue-tinted glasses, smiling. Dark green t-shirt with small graphic, olive green utility vest with patches, light grey cargo shorts, light grey sneakers. Holding black tablet. (2) Second — light skin, dark blue beanie with two white horn-like protrusions and red heart, dark blue reflective sunglasses, right hand covering mouth, surprised expression. Red t-shirt with green graphic, olive green utility vest, grey hoodie underneath, olive green cargo shorts, light grey sneakers, watch on left wrist. (3) Third girl — medium brown skin, dark brown hair in high messy bun, small hoop earring. Dark grey t-shirt, olive green utility vest, black shorts with white splatter patterns, striped yellow/green knee-high socks, bright red sneakers, yellow crossbody bag, silver necklace. Holding black tablet. (4) Right boy — light skin, dark brown short neat hair, black-rimmed glasses, smiling. Light blue denim jacket with patches, grey hoodie underneath, blue jeans with white/red patches and splatters, purple/white sneakers with yellow laces. Holding black tablet. Small grey boxy object on floor between characters.
- **Background/Setting:** Narrow dimly lit hallway or corridor with beige/light brown walls. Dark doorway behind children suggesting another room. White electrical outlets/switches on walls. Soft dim frontal lighting.
- **Color Palette:** Earthy and muted — olive greens, greys, browns with red, yellow, purple, blue accents.
- **Art Style:** Digital illustration with painterly textured quality. Clean well-defined lines, soft blended coloring. Cartoonish children's book style with gradient shading.
- **Composition:** Four characters in staggered horizontal line, centered close together. Dark doorway provides contrasting background depth.
- **Text:** No visible text.
- NOTE: Multiple children wearing utility vest (clothing bleed). Dark blue beanie on child 2 (not Leo's exact beanie style).

---

### B1-013 | hallway_lockdown.png | REGEN v2
- **Used In:** B1 (BUILD)
- **Characters:** Five children in dimly lit bedroom. (1) Leftmost girl — East Asian appearance, dark brown hair in high spiky ponytail, blue-tinted safety goggles on forehead, olive green utility vest over grey t-shirt, khaki cargo shorts, red fingerless gloves. Standing, hands by sides, serious expression. (2) Second boy — East Asian appearance, black spiky messy hair, grey t-shirt with "PLANTER" and bear graphic, grey cargo pants, red fingerless gloves. Standing, hands clenched at sides. (3) Center girl — African descent, dark brown hair in two thick high pigtails/bantu knots, concentrated expression. Blue denim jacket over light pink t-shirt, brightly colored fruit/vegetable pattern leggings, yellow crossbody bag. Holding black cylindrical object, pointing toward device. (4) Fourth girl — African descent, dark brown hair in high bun. Grey zip-up hoodie, blue jeans, yellow/black backpack. Holding black smartphone. (5) Rightmost boy — African descent, dark brown hair, dark blue beanie with red heart, glasses, grey hoodie. Holding black tablet, leaning forward.
- **Background/Setting:** Dimly lit bedroom/study with muted teal/grey-green walls. Wooden desk left with large black computer monitor displaying neon-lit map/schematic with green and pink lines, computer mouse, cup, small bottles. Wooden bookshelf right with books, framed picture with "I [heart] THINGS". Framed pictures/posters on walls. Window with white trim in background. White boxy robot with red mouth and blue digital display on floor to right.
- **Color Palette:** Muted cool tones — greys, teals, blacks. Accent: red (gloves, heart), blue (denim, goggles), yellow (bags), multicolored leggings. Neon green/pink on computer monitor.
- **Art Style:** High-resolution digital painting with cinematic quality. Detailed and textured. Realistic yet stylized, grungy industrial aesthetic.
- **Composition:** Children in loose semi-circle around computer monitor (focal point left). Robot on right. Background equipment frames scene.
- **Text:** "PLANTER" on second child's t-shirt. "I [heart] THINGS" on framed picture on bookshelf. Small indistinct text on monitor interface.
- NOTE: 5 children instead of intended 4. Red fingerless gloves on wrong character (child 1 girl, should be Sam only).

---

### B1-014 | gridlord_first_appearance.png | PASS (CANONICAL GRIDLORD REFERENCE)
- **Used In:** B1 (BUILD)
- **Characters:** Character displayed on CRT monitor screen — male figure with light skin, short styled brown hair with lighter highlights, serious intense expression, focused eyes, cybernetic/mechanical elements on forehead (metallic implant), wearing brown/tan hooded garment. Shown chest-up in frontal pose.
- **Background/Setting:** Retro-futuristic workspace. Beige/tan CRT monitor with keyboard, two black desk lamps, black speaker, black electronic device with screen and dials. Wooden desk. Wall with purple and green neon lightning effects, neon crown-shaped light fixture. Additional monitors and equipment visible. Hacker/workspace aesthetic.
- **Color Palette:** Warm beiges/browns for desk and monitor. Cool purple and green neon lighting. Teal and brown on-screen character. Moody atmospheric quality.
- **Art Style:** Digital painting with polished detailed finish. Smooth gradient shading, clean precise lines. Character has slightly textured painted appearance. Retro-futuristic blend.
- **Composition:** Central focus on CRT monitor displaying character. Symmetrical equipment arrangement. Neon elements frame composition.
- **Text:** Monitor displays code-like text in green, red, white on dark background — too small to read clearly.

---

### B1-015 | leo_tablet_symbols.png | REGEN v2
- **Used In:** B1 (BUILD)
- **Characters:** One child of East Asian descent, light to medium skin tone. Short dark brown/black slightly tousled hair visible under navy blue knit beanie with small colorful heart-shaped patch on front. Round black-rimmed glasses. Focused intense curious expression, eyes wide, mouth closed. Grey zip-up hoodie over dark navy blue t-shirt. Silver circular pendant on thin chain. Dark blue jeans with small green cartoonish dinosaur (T-Rex) embroidered on left thigh. Leaning forward over wooden table, right hand touching glowing device screen, left hand resting on table.
- **Background/Setting:** Cozy study/bedroom/library. Tall wooden bookshelf behind filled with colorful books (green, purple, orange, blue, pink). Wooden desk/table in foreground. Thick light brown book lying flat on desk left. Futuristic glowing tablet on desk showing complex blue diagrams and stylized code. Window in background letting in warm golden light suggesting late afternoon.
- **Color Palette:** Warm — golden light, rich brown wood, grey hoodie, navy blue beanie/t-shirt. Cool blue from device screen provides strong contrast. Vibrant book colors on shelves.
- **Art Style:** Digital painting, clean smooth lines, slightly cartoonish stylized character. Soft painterly shading focusing on depth and atmosphere.
- **Composition:** Character slightly right of center. Gaze and glowing device draw eye. Bookshelves frame character creating contained personal space. Diagonal desk line leads to character.
- **Text:** Stylized code/diagrams on device screen — not legible as words. No other visible text.

---

### B1-016 | zara_sketchpad_symbols.png | REGEN v2
- **Used In:** B1 (BUILD)
- **Characters:** One girl of African descent, rich deep brown skin. Long thick black braids falling over shoulders. Focused slightly serious expression, eyes looking down at paper in lap, lips slightly parted. Light blue denim jacket with green patch on left chest, yellowish-gold patch on right chest, circular red/black design patch on left sleeve, yellow strap over right shoulder. Off-white/cream t-shirt underneath. Colorful patterned leggings with large vibrant shapes in shades of pink, yellow, blue, green. Multi-colored striped socks (pink, blue, yellow, white). One foot resting on soft grey fluffy rug. Yellow crossbody bag slung over left shoulder resting on floor. Holding yellow pencil with blue eraser in right hand, notebook/paper in left hand, actively drawing.
- **Background/Setting:** Bedroom/playroom. Bed with white bedding and grey throw blanket against wall back. Brass-colored floor lamp with white shade casting warm glow left. White cylindrical pencil holder with colored pencils (red, blue, green) on floor near lamp. White bookshelf/set of shelves against back wall with books, clock, decorative objects. Scattered papers with drawings and colored pencils (green, yellow, red) spread on floor around her. Stack of books far left. Light-colored rug on wooden floor.
- **Color Palette:** Warm and inviting — light blue denim, cream, warm browns (skin, wood), soft greys. Vibrant accents from multicolored leggings, yellow pencil/bag/strap, brass lamp.
- **Art Style:** High-resolution photorealistic digital illustration. Natural documentary feel, sharp details on character, slightly softer background. Realistic lighting and textures.
- **Composition:** Child centered slightly right, occupying majority of frame. Background elements slightly blurred drawing attention to child. Scattered papers and colored pencils lead eye to subject.
- **Text:** No legible text.

---

### B1-017 | team_building_key.png | REGEN v2
- **Used In:** B1 (BUILD)
- **Characters:** Four children in cluttered bedroom. (1) Leftmost girl seated — East Asian, light brown skin, dark brown hair in high ponytail with red hair tie, blue-tinted goggles on head, focused slightly serious expression. Black t-shirt with graphic, green utility vest, khaki cargo pants, pink socks, barefoot. Sitting cross-legged, working on device with screwdriver. (2) Second boy kneeling — Caucasian, light skin, spiky brown hair, curious slightly concerned expression. Black t-shirt with "AYEE" and graphic, dark pants, red fingerless gloves. Holding small flashlight. (3) Third girl kneeling — African descent, medium brown skin, dark brown hair in braids pulled back, friendly engaged expression. Light blue denim jacket over grey t-shirt, purple patterned pants with cartoon designs, yellow crossbody bag. Holding paper illuminated by flashlight. (4) Rightmost boy kneeling — Hispanic/mixed, medium brown skin, dark blue beanie with pink heart, glasses, grey hoodie, blue jeans. Holding tablet with attached flashlight.
- **Background/Setting:** Bedroom/study. Wooden desk left with silver desk lamp (turned on) casting warm yellowish light, papers, book/box. Bed with white bedding partially visible right. Wooden dresser against back wall. Floor covered with project materials: central electronic control box with knobs/buttons, small blue device, white box with screen, larger white box with glowing blue square, colored wires (blue, red, black), tools (screwdriver, red tool/possible soldering iron, pliers, spoons), blue/red tape rolls. Poster on wall reading "RECYCLING" partially visible.
- **Color Palette:** Warm and earthy — browns, beiges, greens. Accent: blue (goggles, devices), red (gloves, hair tie), yellow (bag), pink (socks, beanie heart). Warm desk lamp light.
- **Art Style:** Detailed painterly style, clean lines with textured painted quality. Smooth gradient shading, three-dimensional appearance. Modern children's book illustration.
- **Composition:** Children in loose semi-circle around central electronic device on floor. Desk lamp provides warm focused light creating cozy atmosphere. Floor clutter adds authenticity and project narrative.
- **Text:** "AYEE" on second child's t-shirt. "RECYCLING" partially visible on wall poster.
- NOTE: Correct setting (bedroom floor building device). Clothing mostly correct — red gloves on child 2 (should be Sam only, child 2 appears boyish).

---

### B1-018 | entering_lab_second_time.png | REGEN v2
- **Used In:** B1 (BUILD)
- **Characters:** Five children in basement lab. (1) Left girl — Asian descent, light brown skin, brown hair in high ponytail, blue-tinted goggles on head, green utility vest over white t-shirt, olive green cargo shorts, brown hiking boots, purple wristwatch. Open-mouthed surprise. (2) Center-left boy — Caucasian, light skin, spiky messy black hair, beige t-shirt with "PLAYER" in black, olive green cargo pants, red gloves, dark green sneakers. Open-mouthed surprise. (3) Center-right behind girl — Hispanic/Latina, medium brown skin, dark brown hair pulled back, beige t-shirt, distressed blue jeans, dark sneakers. Pointing right index finger toward device. (4) Center-right front girl — African descent, dark brown skin, dark brown hair in two puffy buns, smiling. Denim jacket over yellow t-shirt, brightly colored floral leggings (pink/blue/yellow/green), yellow boots with blue accents, yellow crossbody bag with "Vib" logo. Holding black device with both hands. (5) Rightmost boy — African descent, dark brown skin, short black hair, dark blue beanie with red heart, glasses, grey hoodie with graphic, blue jeans, light grey sneakers. Smiling, looking over shoulder at device.
- **Background/Setting:** Dimly lit basement workshop with concrete walls and cracked floor. Left: metal desk with CRT monitor displaying code, keyboard, mouse, fluorescent light tube above, grey toolbox on floor. Center background: second desk with CRT monitor, white box with blue glowing screen mounted on wall (robot head), wires and small device below, poster reading "NEX.CAVE" in red. Right: large metal cabinet/server rack with electronic equipment, monitors with green/red lights, buttons, dials, round industrial light fixture above. Wires/cables strewn on floor and hanging from ceiling. Stained walls with posters including "NEXCORP" in black letters on left. Pipes along ceiling.
- **Color Palette:** Gritty industrial — muted greys, browns, greens. Vibrant clothing accents: red gloves, colorful leggings, yellow boots/bag, blue beanie. Glowing blue/green screens.
- **Art Style:** Highly detailed digital painting with strong linework, rich textures, careful shading. Grungy industrial aesthetic with polished children's book quality.
- **Composition:** Five children grouped center in loose semi-circle, collective gaze toward device held by girl in denim jacket (strong focal point). Background equipment frames scene. Monitor glow illuminates faces.
- **Text:** "NEXCORP" on left wall poster. "NEX.CAVE" on center poster. "Vib" on yellow bag. "PLAYER" on t-shirt. Code on monitors not legible.
- NOTE: 5 children instead of intended 4. Correct underground lab setting with terminal.

---

### B1-019 | puzzle_solved_celebration.png | REGEN v2
- **Used In:** B1 (BUILD)
- **Characters:** Five children sitting cross-legged on bedroom floor sharing food. (1) Leftmost girl — light brown/tan skin, dark brown hair in ponytail, black sunglasses on head, focused expression eating. White t-shirt with dark text, greenish-olive utility vest, khaki cargo shorts, black shoes. Holding food (chicken drumstick) to mouth with right hand. (2) Second boy — light skin, spiky light brown/blonde hair, slightly surprised/curious expression. Dark blue t-shirt with "PAIEER" in white capitals, light blue jeans, red fingerless gloves, black wristwatch. Holding food raised to mouth with left hand. (3) Middle girl — medium brown skin, dark brown/black hair in two high puffs, neutral expression. White t-shirt under blue denim jacket with yellow panel on sleeve, maroon/burgundy pants, colorful polka-dotted socks (pink, blue, yellow). Holding food on white stick to mouth. (4) Second-right girl — medium brown skin, dark brown/black hair in bun, focused expression. White t-shirt with graphic under blue denim jacket, blue jeans. Holding food on white stick to mouth. (5) Rightmost boy — medium brown skin, short dark brown hair, dark blue beanie with red heart, glasses, grey hoodie, blue jeans. Holding food on white stick to mouth.
- **Background/Setting:** Bedroom. Bed with wooden headboard, white pillows, white comforter. White robot with blue screen face sitting on bed. Wooden nightstand left with white lamp (beige base, white shade), white electronic device. Large window showing night sky with exterior lights. Beige/off-white curtains. White paper with stick figure drawing on carpeted floor. Two smartphones and small black object on floor bottom right.
- **Color Palette:** Warm and earthy — beige/tan (carpet, walls, curtains), blues (denim, jeans, beanie), white (t-shirts, robot, lamp). Accents: green (vest), red (gloves, heart), yellow (sleeve), maroon. Warm lamp-lit glow.
- **Art Style:** Photorealistic digital illustration, cinematic quality. Natural textures, realistic warm ambient lighting. Documentary feel.
- **Composition:** Five children in semi-circle on floor, lower half of frame. Bed with robot and window provide background context. Drawing on floor adds narrative layer. Balanced and intimate.
- **Text:** "PAIEER" on second boy's t-shirt. Other t-shirt text not fully legible. No other discernible text.
- NOTE: 5 children instead of intended 4. Food items are drumstick/food-on-sticks rather than samosas explicitly. Quiet reflective mood achieved. White robot with blue screen on bed (Blip reference).

---

### B1-020 | blip_buffering.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** (1) Central white cube-shaped robot with rounded top and bottom, single short white cylindrical antenna on top. Two large circular eyes with bright teal/turquoise iris and black pupil, curved teal/turquoise smile line, two small pink circular blush marks on cheeks. Several brown irregularly shaped spots/smudges on body. Two small black wheels at base. Floating/standing upright, emitting soft warm yellow-orange glow. (2) Smaller round orange character in upper left — simple cartoonish face with two black dot eyes, wide open smiling mouth, single raised eyebrow. (3) Small orange megaphone-shaped icon with white outline and sound wave detail on right.
- **Background/Setting:** Solid deep black background. Soft warm yellow-orange glow around robot edges (halo effect). Small orange megaphone icon to right.
- **Color Palette:** White (robot), orange (small character, megaphone), teal/turquoise (eyes, mouth), pink (cheeks), black (background, wheels), yellow-orange (glow).
- **Art Style:** 3D computer-generated with smooth polished finish. No visible lines — forms defined by smooth curved surfaces and shading. Smooth gradient shading with distinct highlights.
- **Composition:** Centered on white robot (largest element). Smaller orange character upper left, megaphone upper right — balanced arrangement. Dark background draws attention to characters.
- **Text:** No visible text.

---

### B1-021 | midnight_samosas.png | PARTIAL (seed 1016257298)
- **Used In:** B1 (BUILD)
- **Characters:** Four children in bedroom at night. (1) Leftmost girl — light brown skin, brown hair in high ponytail, holding black tablet with glowing blue symbol, focused expression. Green utility vest over grey t-shirt, green cargo shorts, tan/black sneakers, green utility belt. (2) Second boy — light brown skin, spiky brown hair, blue goggles on forehead, green utility vest over grey t-shirt with red rocket graphic, black shorts, black/grey sneakers, red fingerless gloves, holding yellow triangular snack eating happily with blushing cheeks. (3) Third girl — medium brown skin, dark brown curly hair, blue denim jacket over black t-shirt with white graphic, colorful shorts with cartoon characters (stars, planets, aliens), pink socks with cartoon characters, blue/white sneakers, eating yellow triangular snack, smiling. Small white/silver robot with blue screen attached to shorts by cord. (4) Rightmost girl — dark brown skin, black hair in ponytail, blue beanie with red heart, black-rimmed glasses, blue denim jacket over black t-shirt, blue jeans, white/red/blue sneakers, small yellow bag with brown strap, smiling.
- **Background/Setting:** Bedroom. Two single beds with white sheets and brown headboards. Dark blue walls decorated with small white five-pointed stars (night sky theme). Light brown wood floor. Framed picture on left wall.
- **Color Palette:** Vibrant with cool blues (jackets, goggles, beanie) and greens (vests), warm browns (hair, floor, headboards), bright pops from snacks, shorts, robot. Warm soft light from left.
- **Art Style:** Digital painting, clean smooth lines, soft gentle gradient shading. Cartoonish, friendly, modern children's book style.
- **Composition:** Four children in loose friendly group, centered. Robot integrated with third child. Beds and picture frame provide context and depth.
- **Text:** Stylized text on t-shirts not fully legible. No other legible text.
- NOTE: 5 seed attempts; best count-correct result.

---

### B1-022 | daadi_morning_parathas.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One elderly woman with short curly grey hair, fair skin, warm gentle smile with crow's feet at eyes. Light purple/lavender long-sleeved blouse, necklace with large oval gold-colored pendant. Standing at kitchen counter, hands on wooden cutting board placing bell pepper slices onto round uncooked pizza/flatbread.
- **Background/Setting:** Kitchen with light-colored square tiles, light brown wooden cabinets with rectangular handles, stainless steel range hood above dark stovetop, silver faucet over sink, white dish towel on sink edge. Yellow ceramic bowl with green/yellow fruit, terracotta pot with green plant on counter. Large wooden-framed window with bright warm light, potted plant on windowsill. Foreground: wooden cutting board with pizza/flatbread (colorful pepper slices), orange bowl with red sauce and steam, small white plate with light-colored substance, blue/yellow bowl with red/green fruit.
- **Color Palette:** Warm and soft — light browns, light purples, oranges, greens, yellows. Golden sunny ambiance.
- **Art Style:** Soft, smooth, rounded lines. Subtle gradient shading with gentle color transitions. Painterly quality.
- **Composition:** Woman centered slightly right. Kitchen elements frame her. Counter objects in foreground lead eye to action.
- **Text:** No visible text.

---

### B1-023 | park_bench_breakfast.png | PARTIAL (seed 1305897773)
- **Used In:** B1 (BUILD)
- **Characters:** Four children in park. (1) Left girl — light brown skin, brown hair in high ponytail, dark blue headband with goggles on top, grey hooded sweatshirt under green utility vest with colorful patches/pins, red t-shirt underneath, olive green cargo shorts, tan/brown hiking boots, white socks, holding white disposable cup, brown leather crossbody bag, gentle smile looking toward second child. (2) Second boy — light brown skin, spiky brown hair, black sunglasses on head, black t-shirt with fish graphic and "PEN" in white, olive green cargo shorts, white/black sneakers, red fingerless gloves, yellow backpack, wide happy smile giving two thumbs up. (3) Third girl — dark brown skin, long dark braided hair in high bun, light blue denim jacket over white t-shirt with red graphic, vibrant multicolored galaxy leggings (planets, stars), blue/red sneakers, holding white bowl with food, several bracelets, bright joyful smile. (4) Right boy — light brown skin, short brown hair, dark blue beanie with red heart, black-rimmed glasses, light blue denim jacket over white t-shirt, blue jeans, white/orange sneakers, yellow backpack, holding black digital camera, big happy laugh.
- **Background/Setting:** Wooden park bench behind children. Grassy area with small white flowers. Large mature trees with thick trunks and green foliage. Light grey paved path/sidewalk with grass patches at edges. Sunlit park/forest clearing.
- **Color Palette:** Vibrant — greens, blues, earth tones with bright accents (red gloves, galaxy leggings, orange sneakers). Warm golden late afternoon light with long soft shadows.
- **Art Style:** Digital illustration, clean smooth lines, slightly rounded cartoonish quality. Soft gradient shading.
- **Composition:** Four children in horizontal line, evenly spaced, balanced. Wooden bench anchors composition. Trees frame scene. Children face toward center.
- **Text:** "PEN" in white capital letters on second child's black t-shirt. No other discernible text.
- NOTE: 5 seed attempts; closest to passing.

---

### B1-024 | underground_tunnel.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** Four children walking through tunnel. (1) Leftmost — light skin, brown hair in ponytail, blue-tinted goggles on forehead, slight smirk/determined expression. Grey long-sleeved shirt under green utility vest with patches/tools (pens, magnifying glass), olive-green cargo shorts, brown lace-up boots, holding flashlight casting beam on wall. (2) Second — light skin, spiky brown hair, confident smiling expression, black t-shirt with white rocket graphic and "BLADEIR" text, light grey shorts, black sneakers with white soles, black wristwatch, red glove on right hand. (3) Third — medium-dark skin, thick dark braids, small hoop earrings, cheerful smile. Blue denim jacket over yellow t-shirt with graphic, blue leggings with colorful star/planet pattern, yellow crossbody bag, white sneakers. (4) Rightmost — light skin, glasses, dark blue beanie with pink heart, friendly smile. Grey hoodie under light blue denim vest/jacket with patches, blue jeans, brown sneakers, red lollipop in pocket, holding tablet looking at screen.
- **Background/Setting:** Narrow enclosed tunnel. Reddish-brown brick walls with darker weathered stone/concrete base. Grey concrete floor with small grass/weed patches near walls. Dark grey metal pipes and black cables on ceiling. Bright flashlight illumination from left.
- **Color Palette:** Warm earth tones (browns, reds, oranges) from brick walls. Cooler clothing tones (blues, greens, greys). Warm yellowish glow from flashlight.
- **Art Style:** Clean, smooth digital lines with varying thickness. Combination of flat color blocks and subtle cel-shading. Slightly painterly texture.
- **Composition:** Four children in horizontal line walking left to right, centered. Tunnel walls frame creating enclosure. Flashlight creates visual anchor.
- **Text:** "BLADEIR" in white on second child's t-shirt below rocket graphic.

---

### B1-025 | gridlord_server_room.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** (1) Young girl — medium-brown skin, brown hair in high ponytail with blue hair tie, large expressive brown eyes, cheerful smile with rosy cheeks. Red short-sleeved t-shirt with small graphic, green utility vest with pockets, khaki cargo shorts, white sneakers, silver/black safety goggles on forehead. Standing facing left, hands raised to sides of head (adjusting goggles or excited), smiling broadly. (2) Small boxy robot on floor — white slightly worn/dirty exterior, square screen face with friendly blue smiley face (two glowing white dot eyes, blue smile), thin silver antenna, four small black wheels, cables connected to equipment. Facing girl.
- **Background/Setting:** Indoor lab/workshop. Grey workbench with large black computer monitor displaying "MARTIAN" in blue text with pattern of red dots (some floating in air between monitor and robot). Grey metal cabinets and drawers. Multiple monitors/screens on walls with data/graphs. Grey worn floor. Muted grey-blue walls. Rectangular ceiling light.
- **Color Palette:** Vibrant — girl's red shirt, green vest, khaki shorts. Robot white with bright blue screen. Cool greys/blues background. Red dots and blue "MARTIAN" text. Warm yellowish ceiling light.
- **Art Style:** Clean, smooth precise digital lines. Soft gradient digital shading with cel-shading technique. Slightly 3D cartoonish look.
- **Composition:** Girl right, robot left, visual connection. Workbench and monitor frame left, cabinets right. Slightly low angle.
- **Text:** "MARTIAN" in blue on computer monitor. No other legible text.

---

### B1-026 | sam_traffic_light.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One young boy with tan skin, short dark brown spiky hair, large brown expressive eyes, wide cheerful smile showing teeth, subtle pink blush. Standing on sidewalk facing slightly left, dynamic stance (left leg forward, right back). Left arm extended toward electrical box, right fist raised near chest. Black t-shirt with "PA" visible in white on front. Black over-ear headphones around neck. Black athletic shorts with two white side stripes, small colorful patch on left leg. Red fingerless gloves. White socks. Red/grey high-top sneakers with blue glowing soles.
- **Background/Setting:** Urban street with paved road, concrete sidewalk with grass patches in cracks. Tall grey metallic utility pole with two attached boxes — upper box with illuminated circular red light, lower box with illuminated circular green light. Boy touching plug inserted in lower box with bright sparks. Multi-story buildings on both sides (warm colors — light orange, yellowish-green, reddish-orange). Green trees lining street. Gradient sky (soft yellow to pale blue, wispy clouds).
- **Color Palette:** Warm and vibrant — yellows, oranges, reds, browns. Black/red clothing contrasts with lighter background. Late afternoon golden-hour lighting.
- **Art Style:** Clean, smooth digital lines (vector-like). Smooth gradient cel-shading. Cartoonish and friendly.
- **Composition:** Boy off-center right, electrical box left creates visual anchor. Street and buildings create depth. Leading lines guide eye to central action.
- **Text:** "PA" in white on black t-shirt. Colorful patch on shorts not legible.

---

### B1-027 | leo_library_hack.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One young boy with light brown/tan skin, short dark brown/black hair, dark blue knit beanie with small pixelated multicolored (orange, green, red) patch, large round black-rimmed glasses with thick lenses. Intense concentration/mild concern expression — slightly furrowed brow, neutral slightly downturned mouth. Crouched on library floor, leaning forward, left hand touching tablet screen, right hand typing/stabilizing. Grey zip-up hoodie over dark teal/navy t-shirt, silver chain with large round metallic pendant, distressed blue jeans with light-colored knee patches, colorful sneakers (white soles, blue laces, blue/orange/white upper).
- **Background/Setting:** Library with tall wooden bookshelves on both sides of narrow aisle, filled with hardcover books (red, blue, green, yellow, orange spines). Light brown wooden plank floor. Warm overhead lighting. Tablet emits greenish glow on boy's face and hands.
- **Color Palette:** Warm and vibrant — earthy browns (shelves, floor), rich blues (beanie, shirt, jeans), bright book colors. Bright green tablet glow contrasting with warmer background.
- **Art Style:** Clean, smooth lines with slightly cartoonish/illustrative quality. Smooth gradient shading with subtle highlights. Soft blending.
- **Composition:** Boy centered, clear focal point. Vertical bookshelf lines frame subject and create depth. Crouched pose and glowing tablet create dynamic engagement.
- **Text:** Tablet screen shows green glowing code-like text: sequences resembling `(a)`, `mncnksjy`, `pr`, `actiorl`, `dron`, `s`, `tho`, `rald`, `bl`, `anat`, `cuna`, `1`, `R`, `htrnndy`. No other discernible text.

---

### B1-028 | zara_ar_art.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** (1) Main painter girl — dark brown skin, long curly black hair with colorful hair ties (yellow, blue, orange, green). Broad smile looking at painting, right hand holding paintbrush poised to canvas, left hand holding yellow bag handle. Light blue denim jacket with patches (yellow bear, red cat, others), black t-shirt with graphic print, galaxy/space leggings (purple, blue, pink), beaded bracelets on both wrists, yellow bag with buttons/pins over left shoulder, black marker/pen behind right ear. (2) Canvas character 1 — brown skin, short curly brown hair, smiling and waving, pink dress. (3) Canvas character 2 — long brown hair, green top, blue pants.
- **Background/Setting:** Outdoor park/garden. Lush green grass with flowers (large pink with yellow centers, small white/yellow). Dirt path. Tall leafy green trees with sunlit sky through branches. Wooden easel holding canvas. Bright sunny day.
- **Color Palette:** Vibrant and cheerful — greens, blues, pinks, yellows. Bright and saturated. Warm golden glow suggesting late afternoon.
- **Art Style:** Clean well-defined digital lines, smooth and consistent. Soft smooth color gradient cel-shading/digital painting.
- **Composition:** Main character right, easel/canvas left — visual connection. Background frames scene. Foreground flowers add depth.
- **Text:** "ZAIRA" in bold black capital letters on bottom left of canvas. Signature below (possibly "Shayla" in cursive).

---

### B1-029 | maya_water_valve.png | REGEN v2
- **Used In:** B1 (BUILD)
- **Characters:** One child, medium to dark brown skin, dark brown/black hair in high ponytail, black goggles with brown/tan strap resting on top of head. Concentrated focused expression, eyes cast downward, mouth closed in neutral/slightly pursed line. Grey t-shirt with colorful graphic print underneath olive/khaki green sleeveless utility vest with multiple pockets and patches (one patch on left side with illegible text/logo). Light brown/khaki cargo shorts with visible side pockets and small patch on upper left thigh. Standing, leaning slightly forward, both hands gripping metal tap/valve — right hand on main body, left hand on smaller lever/valve. Actively controlling water flow.
- **Background/Setting:** Outdoor setting. Metal tap actively dispensing water into small rough concrete/stone basin/trough. Water visibly splashing and flowing, droplets in air. Green plants and foliage to left. Trees in background. Low rustic wall/fence of concrete/mud bricks. Simple single-story structure with open doorway behind (faint person visible standing in doorway). Dirt/earthen ground with water puddles around basin. Faint natural rainbow arcing across sky. Blue and white cloth/item on ground right. Other small indistinct objects near wall left.
- **Color Palette:** Earthy — browns (skin, shorts, ground, structures), green (vest, foliage), grey (t-shirt). Accents: metallic silver/bronze tap, rainbow colors (red through violet) in background, blue/white cloth.
- **Art Style:** Photorealistic digital illustration. Documentary style, sharp focus on child with slightly softer background. Natural diffused lighting, slightly overcast. Realistic textures.
- **Composition:** Child slightly off-center right. Diagonal water stream from tap creates dynamic element. Rainbow provides horizontal balance in background. Shallow depth of field emphasizes subject.
- **Text:** No legible text. Small illegible text on vest patch.

---

### B1-030 | grid_map_revelation.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One small white boxy robot with rectangular body, square head (integrated), two large expressive black-outlined eyes with white sclera and black pupils (wide-eyed, slightly worried), curved glowing blue wavy smile, two short stubby arms, two short cylindrical legs with black feet, thin metallic antenna. Standing upright on workbench facing forward. Brownish scuffs/dirt marks. Glowing blue face provides primary light on front.
- **Background/Setting:** White rectangular workbench with stains/scratches. White computer mouse (dirty) to robot's right. Black cables coiled left of mouse. Large black-framed computer monitor displaying world map (continents in green/brown/orange) with numerous small red glowing circular dots. Prominent glowing golden crown icon on upper right of map. Data readout interface in bottom right corner. Black keyboard. Beige electronic control panel with knobs, red button, digital display. Wall-mounted control box with dials. Glass bottle labeled "hazard" with orange liquid. Smaller beaker with green liquid. Bottle with blue liquid. Two analog clocks. Wall shelves with bottles and apparatus. Two framed documents/charts on wall. Exposed light bulb hanging from ceiling.
- **Color Palette:** Warm vintage — beiges, browns. Cool glowing blues (robot face). Red dots on map. Golden crown. Green/brown/orange map.
- **Art Style:** Clean, smooth digital lines with slight sketchiness for hand-drawn feel. Soft smooth gradient cel-shading.
- **Composition:** Robot centered on workbench, monitor behind as significant background element. Various objects create busy lived-in workspace. Slightly angled perspective looking down.
- **Text:** "hazard" on bottle label. Small text on control panel display and other bottles not legible. Map text too small to read.

---

### B1-031 | blip_interface.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** (1) Girl — brown hair in high ponytail, large expressive brown eyes, cheerful smile. Silver/black safety goggles on forehead. Red short-sleeved t-shirt with cartoon character, green utility vest with pockets, khaki cargo shorts, blue wristwatch, light brown/white sneakers. Standing right of robot, holding black cable with metal probe emitting bright blue electrical arc connecting to robot, right hand raised to temple (concentrating). (2) Robot — small boxy, white body with brownish stains/scratches, four black wheels. Glowing cyan screen with friendly smiley face. Two white flexible antennae. Black cable connecting to girl's probe.
- **Background/Setting:** Indoor lab/workshop. Left: large black computer monitor with complex graphs/charts/code in green/blue/white on dark background. Colorful cables (red, green, blue, black) tangled around equipment. Right: server racks/panels with colorful wires, buttons, lights. Light grey floor with dark stains near robot. White door with brass knob. Framed empty whiteboard on wall. Light beige walls. Bright fluorescent ceiling light.
- **Color Palette:** Vibrant — girl's red shirt, green vest, khaki shorts. Robot white with cyan glow. Blue electrical arc. Multicolored wires. Neutral grey/beige background.
- **Art Style:** Clean, smooth digital lines, slightly cartoonish. Soft gradient shading, stylized. Warm focused lighting.
- **Composition:** Girl slightly right of center, robot left. Electrical arc connects them. Background frames scene. Eye drawn from girl's face to probe to arc to robot.
- **Text:** Code/data on monitor in monospaced font (green, blue, white on black) — not legible. Small logo on vest not readable.

---

### B1-032 | blip_reboot_v1.py | PASS
- **Used In:** B1 (BUILD)
- **Characters:** (1) Girl — medium-brown skin, large expressive brown eyes, long wavy brown hair in high ponytail, wide smile showing teeth. Red short-sleeved t-shirt with small white graphic, green utility vest with pockets containing pens/tools, olive-green cargo shorts, light brown sneakers with white soles. Silver/black goggles on forehead, white wristband on left wrist, tool belt/pouch on vest. Kneeling on right knee on tiled floor, arms crossed over chest, looking at robot happily. (2) Robot — small white cube-shaped with friendly face, slightly worn/dusty with brownish smudges. Two bright cyan circular eyes, simple curved cyan smile, two thin white glowing antennae, silver round lens/sensor on side, two small brown wheels. Floating slightly above floor, emitting faint glow and sparkles around base.
- **Background/Setting:** Technical room/workshop. Tall grey metal cabinets/panels with ventilation grilles. Labels/small signs on upper cabinets. Large equipment with numerous colorful wires (red, blue, orange, green) tangled on left. Similar equipment on right. Light grey tiled floor. Warm ambient light from background plus robot's cyan glow.
- **Color Palette:** Warm — girl's red shirt, green vest/shorts, warm grey equipment. Cool contrast from robot's white body and cyan features.
- **Art Style:** Clean, smooth digital lines. Soft gradient digital painting. Cartoonish and appealing.
- **Composition:** Girl right kneeling, robot left — dynamic interaction. Background frames scene. Negative space draws attention to characters.
- **Text:** No discernible text. Small signs on cabinets too small/indistinct to read.

---

### B1-033 | hq_finished.png | PARTIAL
- **Used In:** B1 (BUILD)
- **Characters:** Five characters (four children + robot) in workshop/creative studio. (1) Leftmost — light brown skin, dark brown hair in high ponytail, black/silver aviator goggles on head, grey long-sleeved shirt under greenish-brown utility vest with badge, khaki cargo pants, white sneakers, black watch, holding pen/stylus near monitor, smiling. (2) Second — light brown skin, short dark brown hair, black t-shirt with red/white graphic, dark green cargo shorts, black sneakers, right hand raised to ear (listening), smiling. (3) Third — medium brown skin, dark brown curly hair in high puff, blue denim jacket over black t-shirt with graphic, light blue denim shorts, colorful sneakers (teal/pink/yellow), yellow backpack, red fingerless gloves, holding black digital camera, smiling. (4) Rightmost — medium brown skin, short dark brown hair, dark blue knit beanie with yellow emblem and red heart, black-rimmed glasses, blue denim jacket over black t-shirt with graphic, blue jeans, red/white/blue sneakers, yellow backpack, left hand in pocket, right hand near ear (listening), smiling. (5) Robot — small white box with rounded top, two black articulated legs, two large glowing cyan circular eyes, curved line mouth, standing on grey platform.
- **Background/Setting:** Workshop/creative studio. Two grey desks (left: computer monitor with green interface, keyboard, mouse on red pad; right: monitor and items). Multiple computer monitors with different screens. Light beige walls with framed pictures/posters. White-framed window. String of round exposed lightbulbs on ceiling. Wooden shelf with pictures/objects. Grey floor. White trash can under right desk. Cables on floor.
- **Color Palette:** Warm — browns, blues, greys with pops of yellow (backpacks), red (gloves), colorful sneakers, cyan robot eyes. Warm string light illumination.
- **Art Style:** Clean well-defined digital lines with slightly sketchy quality in places. Smooth digital gradient shading, polished painterly look.
- **Composition:** Characters in loose semi-circle facing viewer, robot slightly in front. Background elements frame without overwhelming.
- **Text:** T-shirt text not legible. Small badge on leftmost child's vest too small to read. Poster text not legible.
- NOTE: Accepted as best achievable after 6 attempts.

---

### B1-034 | blueprints_analysis.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** (1) Boy — light skin, dark brown/black short slightly tousled hair, thick dark-frame glasses, focused slightly serious expression. Dark grey/black t-shirt under light grey zip-up hoodie (small colorful patch on left chest), blue denim jeans with rips and stains on knees, white sneakers with pink soles (dirty). Seated on wooden stool, leaning forward, typing on laptop in lap. (2) Robot — small boxy, white body with numerous brownish stains/smudges. Bright cyan/turquoise screen face with two large black circular eyes and curved smiling mouth, pink blush marks on cheeks. Two articulated white robotic arms, two large black wheels with glowing blue rims. Standing on floor left of boy, facing him.
- **Background/Setting:** Indoor workshop/lab. Left: large whiteboard with handwritten text (nonsensical/placeholder). Workbench with yellow container of tools, glass jar with red liquid. Center-back: two large glowing blue technical diagrams/schematics on wall, white clipboard, wooden cabinet with drawers, cardboard box, glass jar. Right: window with warm natural light, wall-mounted lamp with yellow shade, countertop with blue mug, white container. Light-colored square tile floor.
- **Color Palette:** Warm — browns, tans, yellows. Cool blues from robot's screen/wheels and diagrams. White robot, grey hoodie provide neutral bases.
- **Art Style:** Clean, smooth digital lines, consistent weight. Soft blended gradient shading. Warm glows around robot and diagrams.
- **Composition:** Boy and robot centered, balanced. Boy right, robot left. Background elements frame central action. Slightly angled perspective.
- **Text:** Whiteboard text: "Read Creoptioy.", "Face eis", "pathe amak,", "Lots, Ice sor ahc hall", "ac hnode,", "Haoy ot tes", "horry ce ontteak.", "klere o, wracel hciots". Diagrams have "BM" in top left corner. Other diagram text too small/stylized.

---

### B1-035 | investigation_board.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One young girl, dark brown skin, large expressive brown eyes, long curly black hair in two high pigtails with colorful hair ties (pink, green, yellow). Small round blue earrings. Broad smile. Blue denim jacket with numerous colorful patches and pins (stars, planets, cartoon characters, text), white t-shirt with colorful graphic and partial text "ATA", purple galaxy/space leggings with stars/planets and small patches, colorful sneakers (pink, blue, green, white with pink laces), bright yellow crossbody bag with blue circular details and gold buckle, beaded anklet on right ankle. Standing facing forward slightly angled, left hand by side, right hand holding yellow bag strap.
- **Background/Setting:** Indoor classroom/community center. Two large light brown cork bulletin boards on light-colored wall. Left board: white sign with black text "ZARAL" at top, papers below (drawing of child, blue paper with orange square, white paper with text, photo of child, drawing of children playing soccer), two colorful spiral decorations. Right board: photos of children and adults, stick figure drawing, white papers with text. Light brown wooden desk below boards with closed book/notebook (left) and red cup with book/notebook (right). Light grey smooth floor.
- **Color Palette:** Bright and cheerful — warm tones. Yellow bag, colorful sneakers, blue jacket, purple leggings, warm browns of wood/cork. Soft cream/beige wall, cool grey floor.
- **Art Style:** Clean, smooth, precise digital lines. Soft blended gradient shading. Cartoonish and whimsical, highly detailed.
- **Composition:** Girl centrally positioned, clear focal point. Bulletin boards and desk frame her. Negative space draws eye to her.
- **Text:** "ZARAL" in black capitals on white sign at top of left board. "ATA" partial text on t-shirt. Other papers on boards too small/blurry to read.

---

### B1-036 | rooftop_sunset.png | PARTIAL
- **Used In:** B1 (BUILD)
- **Characters:** Four children and one robot on rooftop. (1) Leftmost girl — light brown skin, brown hair in high ponytail with red hair tie, dark grey t-shirt with small white logo, large olive-green utility vest with pockets/tools, dark grey shorts, white socks, red sneakers with white soles. Wide happy smile, left hand on kneeling boy's shoulder, right arm bent at elbow. (2) Kneeling center boy — light brown skin, spiky brown hair, red t-shirt, olive-green utility vest, khaki cargo shorts, white socks, blue sneakers with colorful glowing soles. Kneeling on one knee, right hand touching ear (listening), smiling up at robot. (3) Robot — small white boxy, rectangular head, light blue screen face with two glowing green eyes and happy smile, two arms/two legs with visible joints, hovering/jumping with right arm raised, red/black details, two small antennae. (4) Standing girl right-of-center — dark brown skin, long dark brown braided hair, black t-shirt with white graphic, light blue denim jacket, bright pink/blue patterned floral leggings, yellow-green sneakers, holding smartphone in right hand, smiling. (5) Rightmost boy — light brown skin, short brown hair, glasses, dark blue knit beanie, light blue denim jacket, black t-shirt, faded blue jeans, yellow crossbody bag with heart design, holding smartphone in left hand, smiling.
- **Background/Setting:** Grey rooftop with low grey concrete railing. City skyline with numerous buildings silhouetted. Gradient sky — soft peach/light orange near horizon to pale lavender/light blue above. Fluffy pink-tinged clouds. Smooth grey rooftop surface.
- **Color Palette:** Warm and inviting — sunset hues (orange, pink, purple) in sky. Cool tones in clothing (blues, greys, khakis). White robot with cool blue screen.
- **Art Style:** Clean digital illustration. Smooth lines, soft blended gradient shading. Friendly and accessible.
- **Composition:** Robot centered slightly above between four children. Children in loose semi-circle all looking up at robot. Background frames main subjects.
- **Text:** No discernible text. Small indistinct logos on t-shirts.

---

### B1-037 | maya_skyline_dusk.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** One young girl, medium-brown skin, dark brown hair in high ponytail, small pencil/pen tucked behind right ear. Large expressive brown eyes, wide friendly smile showing teeth, subtle pink blush. Dark blue/black goggles on forehead with clear reflective lenses. Pair of round black-rimmed glasses/goggles hanging from black cord around neck. Red t-shirt with white abstract fish-like/star-shaped logo, sleeveless olive-green utility vest with pockets containing red screwdriver, blue pen, yellow pencil, silver wrench, red cylindrical object. Olive-green cargo shorts. Olive-green sneakers with white laces/soles. Kneeling on right knee on rooftop, left hand on left knee, right hand on ground. Looking slightly left toward viewer with confident cheerful expression.
- **Background/Setting:** Flat grey rooftop with subtle texture, simple modern metal railing. Dense urban cityscape — low-rise brick buildings and tall modern skyscrapers, some lit windows. Gradient sky — soft pink/orange near horizon to lighter purple/blue above. Large bright pale yellow sun low on horizon partially obscured by buildings. Wispy pinkish-orange clouds.
- **Color Palette:** Warm dominant — orange, pink, yellow sky. Olive green vest/shorts, red shirt, brown hair. Muted building tones (brown, beige, grey).
- **Art Style:** Clean, smooth lines with slightly sketchy hand-drawn feel. Cel-shading/smooth gradient coloring. Soft light/dark transitions.
- **Composition:** Character slightly right of center, clear focal point. Expansive cityscape and sunset as dynamic background. Railing leads eye to horizon and sun.
- **Text:** No visible text.

---

### B1-038 | backmatter_blip_specs.png | PASS (gold standard)
- **Used In:** B1 (BUILD)
- **Characters:** One robot — simple boxy humanoid form. Large white rectangular torso with slightly rounded top edge, smaller square white head on top. Two short white cylindrical antennae with round tips. Two very large circular eyes — bright glowing blue with darker blue pupils and pattern of smaller blue dots radiating outward (digital/mechanical appearance). Small dark dot nose. Wide red curved smiling mouth. Subtle pinkish blush on cheeks. White articulated arms/legs with black bands around segments. White five-fingered hands. White feet with black soles. Mid-stride walking pose (left leg forward, right back). Cheerful friendly expression.
- **Background/Setting:** Dark forest environment. Large curved tree trunks frame robot on left and right creating natural archway. Dirt path/clearing in dark earthy browns and greys. Rounded rocks and patches of muted green/brown grass/foliage at tree bases. Single warm yellowish spotlight from above illuminating robot and small circular ground area. Stark contrast with surrounding darkness.
- **Color Palette:** White robot, vibrant glowing blue eyes, bright red mouth. Warm golden yellow spotlight. Dark brown, black, muted green background.
- **Art Style:** Smooth, clean digital lines. No visible sketch lines. Soft painterly gradient shading. Dramatic light/shadow for depth and atmosphere.
- **Composition:** Robot centrally positioned. Two tree trunks frame naturally. Spotlight reinforces central focus. Symmetrical balance.
- **Text:** No visible text.
- MATCHES TEMPLATE

---

### B1-039 | backmatter_how_to_draw_blip.png | PASS (gold standard)
- **Used In:** B1 (BUILD)
- **Characters:** (1) Central robot — boxy rounded white body, two short white cylindrical antennae. Large rectangular blue screen face with two large circular blue pixelated eyes (one winking with black dot pupil), wide open-mouthed smile showing pink tongue. Two large round pink circles on cheeks. Black joints on white arms/legs. Floating/jumping mid-air with open hands and feet off ground. (2) Human figure 1 (left background) — short brown hair, light pink short-sleeved shirt, seated at desk facing right. (3) Human figure 2 (left foreground) — short dark hair, dark blue/brown jacket, seated facing right, only back of head/shoulders visible.
- **Background/Setting:** Brownish textured brick walls. Two large black rectangular screens mounted on wall. White pipe across upper wall. Brown concrete/tiled floor with dark rectangular mat and small orange bucket. Light brown desk behind seated person with white coffee cup/saucer. Beige/light brown machine (coffee maker/oven) with green light, equipment with dials/screen. Small tablet/monitor on desk. Brown chair partially visible.
- **Color Palette:** Warm and earthy — browns, beiges, yellows. Bright cool robot colors (white, blue, pink). Single warm yellowish spotlight from above.
- **Art Style:** Clean, smooth, consistent digital lines. Soft painterly gradient shading. Friendly, approachable children's book art.
- **Composition:** Robot centered, clear focal point. Human figures in background provide context. Foreground elements frame scene and add depth. Balanced composition.
- **Text:** Left screen: "TTOPHE STTINS" (reversed) with charts/graphs. Right screen: "NE STSCE BONODIL OI NIOI E FRTENT" (reversed) with technical diagrams, portrait, text blocks. Stylized/made-up font.
- MATCHES TEMPLATE

---

### B1-040 | backmatter_puzzle.png | PASS (gold standard)
- **Used In:** B1 (BUILD)
- **Characters:** One robot — boxy white body and head. Two short white antennae with round white tips. Black rectangular screen face with two large circular glowing blue eyes (pattern of smaller white dots surrounding central black pupil). Simple curved red smiling mouth. Two soft pink blush marks on cheeks. Segmented white arms/legs with black hands and black feet. Standing upright with one leg slightly forward (walking/stepping motion). Arms relaxed at sides. Happy friendly expression.
- **Background/Setting:** Solid light creamy-white background with subtle gradient — lighter center, fading to very pale warm yellowish-white at edges. Soft glowing halo effect around robot. No other objects, characters, or scenery.
- **Color Palette:** White (body), black (face, hands, feet), blue (eyes), red (mouth), pink (blush). Soft warm off-white/cream background.
- **Art Style:** Smooth, clean digital lines. No texture or roughness. Soft gradient shading with subtle color transitions. No harsh shadows.
- **Composition:** Robot centrally positioned, occupies significant portion of frame. Simple, uncluttered. Negative space makes character stand out.
- **Text:** No visible text.
- MATCHES TEMPLATE

---

## Character Cards (6 items)

### CC-01 | Cards/card_maya.png | PASS
- **Used In:** B1 (BUILD)
A young girl named Maya with brown pigtails tied with red bands. Silver goggles on forehead. Cheerful expression with wide smile and bright brown eyes. Red t-shirt with a white and red graphic, green utility vest with multiple pockets, grey shorts, tan lace-up boots. Right hand holds a red-and-white rocket-like object; left hand holds a silver-and-black screwdriver. Floating tools surround her: silver adjustable wrenches, flathead screwdriver, combination wrench, Phillips-head screwdriver, utility knife, green circuit boards, and a yellow-black coiled cable. Background is a slightly out-of-focus indoor workshop with wooden floor, workbench on left, window on right with light streaming through. Warm natural lighting from the right. Clean digital lines with slight sketch quality; soft cel-shaded gradients. Framed by a decorative gear-and-mechanical border. Text: "MAYA" at top in large bold uppercase; "THE INVENTOR" in a decorative banner at bottom.

### CC-02 | Cards/card_leo.png | PASS
- **Used In:** B1 (BUILD)
A young boy named Leo with dark hair and black-rimmed glasses. Serious/focused expression with slight frown. Dark blue knit beanie with a red-and-white heart-shaped patch. Grey hooded sweatshirt over black t-shirt, silver chain necklace. Blue denim jeans with rips at knees. Holding a black tablet computer with both hands, looking at its screen. Three semi-transparent glowing speech bubbles: one left-above-head with green text, one right at chest level with yellow/orange text, one left-lower with blue text—all showing code/programming language. Background is a cozy bedroom with warm orange walls, a window with red curtains, wooden furniture. A small glowing globe/planet in a purple-tinted square on the right, a blue balloon and green object on a desk on the left. Lighting from the tablet and speech bubbles creates ambient glow. Clean cartoonish lines with painterly texture; soft cel-shading. Framed by a colorful pixelated border. Text: "LEO" at top in large bold white with black outline; "THE CODER" in a white banner at bottom.

### CC-03 | Cards/card_zara.png | PASS
- **Used In:** B1 (BUILD)
A young girl named Zara with dark brown skin and long curly black hair in two high pigtails with colorful hair ties (green and blue). Warm friendly smile, expressive brown eyes. Light blue denim jacket covered in colorful patches and pins, white t-shirt with cartoon graphic underneath, purple pants with colorful galaxy-like pattern. Black camera on yellow strap around neck. Small bright yellow crossbody bag. Relaxed standing pose with one hand slightly forward. Surrounded by floating art supplies: green, yellow, pink, blue, and purple pencils; blue, green, and pink crayons; pink, green, white, and brown erasers; small star and flower shapes. Background is warm beige/light tan with colorful paint splatters (blue, green, pink, yellow, orange) and small stars, with a rough torn-paper edge effect. Bold clean black outlines; minimal shading with flat colors. Text: "ZIARA" at top in stylized black brush-lettered font; "THE ARTIST" in a white banner at bottom.

### CC-04 | Cards/card_sam.png | PASS
- **Used In:** B1 (BUILD)
A young boy named Sam with short spiky black hair. Wide happy smile showing teeth, large expressive eyes with slight squint. Black t-shirt with "PLAY!!" in white and "CHAMP" in smaller text. Black shorts with small white rectangular patch on left leg. Blue and purple sneakers with white soles. Red and black fingerless gloves on both hands. Energetic pose: left hand raised holding a black futuristic controller with cord; right hand raised holding a black standard console controller with red and blue buttons. Additional floating controllers in upper corners. Two pink cartoon hearts. Three orange jagged lightning bolts. A green-bordered timer box reading "00 S" and a green-bordered circle displaying "4". Background is a radial starburst from warm yellow center to deep orange/brown edges, with a pixelated retro-video-game cityscape and stars at the outer edge. Thick multicolored border. Text: "SAM" at top in bold yellow with red outline; "PLAY!! CHAMP" on t-shirt; timer text "00 S"; number "4"; and "THANKS FOR PLAYING AND PLEASE COME AGAIN" at bottom in white on black.

### CC-05 | Cards/card_blip.png | PASS
- **Used In:** B1 (BUILD)
A white boxy robot named Blip with rounded edges and two short cylindrical antennae. Face is a large light blue screen with two large circular glowing blue eyes with black pupils and white highlights. Simple red curved smile. Black joints at shoulders, elbows, and knees. Short stubby white limbs with black hands and feet. Dynamic mid-step walking/dancing pose. Several small green square cards with rounded corners float around the robot, each displaying a white schematic symbol (wave/signal, leaf, play button/triangle, bar chart). Multiple pink hearts of varying sizes scattered throughout, including one large pink heart with white outline in top right corner. Vertical lines of white stylized binary code (0s and 1s) on the left side. Background is a softly focused warm indoor scene (workshop or room with window) in shades of orange, yellow, brown, with hints of green and pink. Image framed by a glowing teal border with circuit-like design. Text: "BLIP" at top in large bold turquoise with black outline; "THE ROBOT" at bottom in white bold capitals with black outline.

### CC-06 | Cards/card_gridlord.png | PASS
- **Used In:** B1 (BUILD)
A young male character with short dark brown hair styled upwards with a prominent metallic silver spiked headpiece. Light tan skin. Green digital-like splatters/paint on face. Two metallic triangular silver pieces embedded on forehead. Two thin metallic silver spikes protruding from the right side of the face. Large almond-shaped vibrant glowing green eyes. Serious focused expression with slight frown. Dark green/olive t-shirt. Behind him, a desk with at least four computer monitors displaying various images (a female character, green glowing abstract shape, UI with text and data). Black keyboards and a white computer tower visible. Background is dark (blacks, dark grays) with prominent cascading green glowing binary code digital rain. Deep purple banner at bottom. Dramatic focused lighting from the front with cooler tones; green elements glow strongly. Text: "GRIDLGD" at top in large bold orange glowing capitals with black outline; "THE DIGIAL SHADOW" at bottom in white sans-serif capitals on a purple banner with green splattered border.

---

## Blip Marginalia (12 items)

### BM-01 | Marginalia/blip_thinking.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered cartoon robot with a white boxy body, rounded edges, and black circular joints. Face is a light purple screen displaying two large blue circular eyes with glowing blue outer rings and white spiral patterns in the centers. Mouth is a simple red curved smile. Two thin white antennae with spherical tips protrude from the head. Arms and legs are short, white, with black rounded hands and feet. Pose is a jumping/floating stance with limbs slightly bent. Three small grey metallic gears float around the head—left, behind-right, and far-right. Background is a solid warm brown/tan. Lighting is soft and diffused from front-above, with gentle highlights on top surfaces and subtle shadows beneath. No outlines; forms defined by smooth shading and gradients. No text.

### BM-02 | Marginalia/blip_happy.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered white boxy robot with a bright cyan/turquoise rectangular screen face. Eyes are two large circles with mesh-like or circuit-board patterns in cyan. Mouth is a wide red curved smile. Two white antennae on top. Black arms with grey/silver elbow joints and black three-fingered hands. Two black wheels for lower body with cyan-glowing rims and small cyan center lights. Pose is jumping/dancing with arms bent at elbows. Small light-blue/cyan musical notes and sparkles surround the robot. Background is a warm gradient from lighter orange at top to darker yellow at bottom. Soft front lighting with subtle highlights. No text.

### BM-03 | Marginalia/blip_scared.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered white boxy robot with rounded cube head and glossy finish. Face is a red screen displaying a simple open-mouthed smile drawn in black. Two prominent circular blue eyes with glowing gear-like patterns in the center. Two thin white antennae with spherical tips. Short stubby white limbs with black rounded hands and feet. Walking/dancing pose with one leg lifted and arms positioned dynamically. Background is a gradient from deeper saturated orange at top to lighter orange at bottom. Soft even warm lighting. No text.

### BM-04 | Marginalia/blip_confused.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered white boxy robot with rectangular head and torso. Face is an orange rectangular screen with two large circular blue eyes with black pupils and white highlights. Simple curved orange line for a smile. Two small white antenna protrusions. Black hands and feet. Walking stance with one foot forward and arms bent at elbows. Two black hand-drawn question marks flank the robot's head—one left, one right. Background is solid uniform orange. Soft even front-above lighting. Robot rendered in 3D; question marks have a sketchy 2D hand-drawn line quality. No text.

### BM-05 | Marginalia/blip_excited.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered white boxy robot with square head and rounded corners. Face is a bright yellow screen with thick white border, displaying two large circular blue eyes with white gear-like patterns. Wide red smiling mouth. Two white antennae. Black limbs with rounded joints; black hands and feet. Standing upright, arms slightly bent and held out in a welcoming/presenting pose. Small colorful musical notes and lightning-bolt/star symbols in yellow, blue, and pink scattered around the head and shoulders. Background is a gradient from lighter saturated yellow at bottom to deeper warm orange at top. Soft even front-above lighting. No text.

### BM-06 | Marginalia/blip_love.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered white boxy robot with cubic head and rounded rectangular torso. Face is a large pink rounded square with two large circular blue eyes with black pupils and white highlights. Wide red smiling mouth. Two thin white antennae. Black rounded rectangular hands and feet. Two black rounded rectangular side panels/ears. Dynamic floating/jumping pose with arms slightly bent and raised, legs bent at knees. Two red hearts flank the head (left and right). Three small yellow flowers with orange centers scattered around. One tiny white five-petaled flower near bottom right. Background is a pink gradient (lighter at top, slightly darker at bottom). Soft even lighting. No text.

### BM-07 | Marginalia/blip_loading.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered white boxy robot with cubic head and torso. Two prominent glowing blue circular eyes with gear-like patterns. Simple curved red smiling mouth. Two small white spherical antennae. Left arm slightly raised, holding a small transparent object; right arm hangs loosely. Standing upright with legs slightly apart. A traditional hourglass sits to the left of the robot on the ground—clear glass bulbs with narrow neck, light brown sand in the top bulb, bottom empty, light brown wooden/plastic frame. Background is out-of-focus bokeh in warm light orange and beige tones, suggesting a cozy indoor setting. Soft diffused overhead/front-left lighting. Clean polished vector-like lines. No text.

### BM-08 | Marginalia/blip_sleepy.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered white boxy robot with rectangular head and torso. Face is a purple screen displaying closed blue eyes with small white dot patterns suggesting a dreamy state. Curved red smiling mouth. Two thin white antennae with round white knobs. Short white arms and legs with black rounded feet. Upright sleeping pose, limbs relaxed. A small light-blue "Z" symbol and a small light-blue crescent moon float to the left of the head. Background is solid warm muted orange/amber. Soft diffused front-left lighting with subtle highlights and soft right-side shadows. Clean smooth digital lines. No text beyond the "Z" sleep symbol.

### BM-09 | Marginalia/blip_laugh.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered white rectangular robot with rounded edges. Face is a bright blue screen with two large circular eyes featuring smaller blue circle patterns and white highlights. Small curved black lines above eyes suggesting raised eyebrows. Wide red smiling mouth with black outline. Two white spherical antennae. Black articulated arms with white gloved hands. Short black cylindrical legs with white rounded feet. Jumping/dancing pose with both feet off ground and arms slightly outstretched. Two small white cloud-like shapes with "HA" text near the head. Background is a softly blurred indoor scene—a portion of a potted green plant on the left, warm muted tones of beige/light brown. Soft diffused warm lighting. Text: "HA" appears twice in cloud shapes.

### BM-10 | Marginalia/blip_determined.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered white boxy robot with rounded edges. Black circular details on sides. Short black articulated arms and legs with white feet. Two small black antenna protrusions on top. Face is a large rectangular blue screen with a glowing electric blue outline. Two large expressive glowing blue eyes with black pupils. Simple curved red line forming a wide happy smile. Dynamic mid-step/dance pose with one leg lifted. Two small yellow lightning bolt shapes emanate from the body sides. Background is a blurred indoor living room/playroom with a cream-shaded lamp on the left, a shelf with indistinct objects, warm beige walls, and light warm wood floor. Warm lighting from the left. No text.

### BM-11 | Marginalia/blip_sad.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered white boxy robot with rounded top and bottom. A black rectangular panel on the left side of the head. Face is a black screen displaying two bright blue spiky circular shapes as stylized eyes. Simple curved red line forming a frowning mouth. Two thin silver antennae with round spheres. Articulated arms and legs with visible black joints at shoulders, elbows, hips, and knees. White rounded hands and feet. Walking/stepping pose with left arm and leg forward, right arm and leg behind. Background is a blurred interior with warm light from the left, a blurred green plant/bush on the right, and a warm orange-brown shape suggesting furniture. Soft diffused lighting from the left. No text.

### BM-12 | Marginalia/blip_mischievous.png | PASS
- **Used In:** B1 (BUILD)
A 3D-rendered white boxy robot with rounded corners. Face is a large square green screen with a wide red smiling mouth. Two large glowing blue circular eyes with pixelated spiral patterns. Right eye is winking. A small orange triangular shape (nose/cheek mark) on the right side of the screen. Two thin white cylindrical antennae. White arms with black rounded joints at shoulders and elbows. Black rounded hands. White legs with black joints. Black rounded feet. Walking/stepping pose with one leg forward. Three star-shaped sparkles: two yellow stars flanking the head, one orange star to the right of the body. Background is a gradient from warm orange-brown at top to bright yellow-green at bottom. Soft even front/overhead illumination. No text.

---

## Chapter Vignettes (36 items)

### CV-01 | ChapterHeaders/ch01_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters present. The scene is object-focused.
- **Background/Setting:** A cluttered wooden workbench in a workshop. Behind the bench, a wooden shelf holds silver scissors, colorful books (blue, green, brown), and a cylindrical object (tape roll or spool). A prominent desk lamp on the right casts warm yellowish light. Scattered tools surround the central object: a silver adjustable wrench with red handle, pliers, screws and nuts of various sizes, a coiled black wire, a small dark bottle, and a purple-handled tool.
- **Color Palette:** Bold and saturated primary/secondary colors. Warm lamp yellows contrast with cooler dark background. Dominant tones: red, blue, green, yellow, orange, metallic silver, wood browns.
- **Art Style:** Vibrant cel-shaded 2D with bold dark outlines. Flat color blocks, no gradients. Clean graphic quality. Playful and dynamic.
- **Composition:** Circular vignette crop. Focal point is a large tangled ball of multicolored wires at center with a sparking/glowing cylindrical component emitting white-yellow sparks. Dramatic warm lighting from the desk lamp creates high contrast.
- **Text:** No visible text.

---

### CV-02 | ChapterHeaders/ch02_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters present. The scene is object-focused.
- **Background/Setting:** Dark surface (possibly a door) with a large circular metal lock mechanism mounted on it. The lock appears weathered and rusted with an aged patina. Two small screws flank the central keyhole. Golden light beams radiate outward from the keyhole, with sparkling golden particles floating in the air around it.
- **Color Palette:** Metallic grays and browns with rust orange/brown patina. Warm golden-yellow light from the keyhole. Dark background creating dramatic vignette effect. Muted palette with the exception of the bright golden light.
- **Art Style:** Detailed digital painting with realistic lighting and texturing. Painterly quality with well-executed lighting effects creating depth and mystery. More realistic than cel-shaded.
- **Composition:** Centered and symmetrical circular vignette. Eye drawn directly to the keyhole and magical golden light. Dark edges fade to focus all attention on the lock.
- **Text:** No visible text.

---

### CV-03 | ChapterHeaders/ch03_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters present. The scene is object-focused.
- **Background/Setting:** A dark, theatrical environment with a single warm golden spotlight illuminating the central crate. Floating dust particles in warm tones (gold, orange, brown) add atmosphere. Orange/brown ground surface. The crate sits on a flat surface.
- **Color Palette:** Metallic gray/silver for the crate, blue rectangular panels with white text, warm golden spotlight, dark brown/black background, orange/brown ground. High contrast between illuminated crate and dark surroundings.
- **Art Style:** Vibrant cel-shaded 2D with bold outlines. Clean edges and flat color application characteristic of cel animation. Slightly cartoonish yet detailed quality suitable for children's literature.
- **Composition:** Crate positioned slightly off-center, angled to show two sides. Spotlight creates circular illuminated area drawing attention to the crate. Floating particles enhance focus on the central object. Cinematic framing.
- **Text:** "NEXCORP" in bold white letters on blue rectangular backgrounds, "RESEARCH" below it in white. Appears on both visible sides of the crate. Small text "747428" on the top edge.

---

### CV-04 | ChapterHeaders/ch04_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters present. The scene is entirely object-focused on the kitchen setting.
- **Background/Setting:** A cozy, well-lit kitchen with wooden cabinetry, a countertop, a white pitcher/jug, a faucet, and a window above the sink letting in soft golden light. An oven is partially visible on the left. A polished wooden dining table holds a white ceramic plate piled with golden-brown triangular pastries (turnovers/calzones) with steam rising from them. A neatly folded white napkin and silver fork sit to the right of the plate.
- **Color Palette:** Warm, earthy tones dominate. Rich wood browns for cabinets and table. Vibrant golden-yellow pastries contrast with white plate and napkin. Soft amber and cream tones from window light. Nostalgic and comforting.
- **Art Style:** Vibrant cel-shaded 2D with bold, dark outlines. Flat, solid colors with strong graphic quality. Stylized soft gradients and highlights add depth without being overly realistic. Whimsical and inviting.
- **Composition:** Soft circular vignette draws the eye to the center. Central focus on the plate of steaming pastries. Kitchen elements frame the background providing context. Intimate and focused framing.
- **Text:** No visible text.

---

### CV-05 | ChapterHeaders/ch05_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A small, friendly white robot with a rounded rectangular body and head. It has two small antenna-like protrusions, blue LED eyes displaying a digital pattern resembling "00," a red mouth curved in a cheerful smile, articulated joints at shoulders/elbows/knees, and black rounded hands and feet. The robot has an inviting, approachable expression.
- **Background/Setting:** A cozy room (child's room or study area) with a wooden desk/table surface. An open book or notebook is partially visible to the left. Background bookshelves hold colorful books (red, blue, green, yellow). A window with soft diffused light creates a warm glow. Slightly blurred background with depth of field.
- **Color Palette:** Predominantly white robot with black accents. Bright blue LED eyes. Warm wood tones for the table. Soft blue and white from window light. Colorful books in background. Overall warm palette with soft lighting.
- **Art Style:** 3D rendered with smooth shading and realistic lighting rather than traditional cel-shaded 2D. Soft realistic lighting with gentle shadows, smooth gradients, rounded edges, subtle reflections, and depth of field blur. Friendly cartoonish aesthetic despite the 3D rendering approach.
- **Composition:** Robot positioned centrally on the wooden surface. Window provides soft backlight highlighting the robot's shape. Background elements provide contextual setting without competing for attention.
- **Text:** No visible text (the blue LED eyes display a digital pattern "00" but no readable text).

---

### CV-06 | ChapterHeaders/ch06_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters present. The scene is object-focused.
- **Background/Setting:** Deep dark blue/black background forming a perfect circular vignette that fades to black at edges. A silver-gray pole-mounted traffic light is the sole object. The black light fixture houses three classic lights — red (top), yellow (middle), green (bottom) — all illuminated simultaneously. Explosive burst of golden-yellow light rays and sharp sparks radiate outward from the traffic light.
- **Color Palette:** Vivid glowing red, bright sunny yellow, and lively fresh green for the three lights. Sharp golden-yellow rays/sparks. Deep dark blue/black background. Extremely high contrast. Saturated and bold.
- **Art Style:** Flat 2D cel-shaded style with strong dark outlines defining every shape including individual light rays. Highly saturated solid colors characteristic of cel-shading. Bold, cartoonish, and energetic.
- **Composition:** Centered traffic light with radial burst of light rays creating dynamic energy. Perfect circular vignette isolates the main subject. Symmetrical and impactful. The simultaneous illumination of all three lights suggests a moment of magical malfunction or transition.
- **Text:** No visible text.

---

### CV-07 | ChapterHeaders/ch07_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters present. The scene is object-focused on the tablet device.
- **Background/Setting:** Dark blue/black background creating a circular vignette. A rectangular tablet device with rounded corners and a bright blue backlight is centrally positioned, slightly angled. The tablet screen displays a world map in warm earthy tones (oranges, greens, browns) with a bright cyan/blue sound wave visualization running horizontally across the middle with sharp peaks and valleys. Columns of text resembling code or technical documentation appear on the left and right sides of the image framing the tablet. Yellow/gold glow around tablet edges creates a spotlight effect.
- **Color Palette:** Dark blue/black background, bright cyan/blue for sound wave and tablet backlight, warm oranges and greens for the map, yellow/gold glow accents. Strong contrast between dark background and brightly lit central elements. Neon-like glowing quality.
- **Art Style:** Sleek modern digital interface design with bold outlines. Combines digital interface aesthetics with illustrative map graphics. Glowing neon effects and high contrast. Contemporary, tech-forward look. More digital/holographic than traditional cel-shading.
- **Composition:** Tablet centrally positioned and slightly angled. Dark circular background vignette draws attention to the tablet. Text columns on left and right frame the central image. Balanced and eye-catching.
- **Text:** Mirrored/reversed text visible on the tablet screen (appears upside-down). Code-like text columns on the left and right sides of the image. No clearly legible narrative text.

---

### CV-08 | ChapterHeaders/ch08_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters present. The scene is focused on the neon sign.
- **Background/Setting:** Warm interior lighting with yellow/orange tones. Background reveals what appears to be a building interior with windows and warm lighting. Colorful light streaks and reflections in green, blue, and red appear around the edges. The neon sign appears mounted on or reflected in a glass surface. Slightly dreamy, blurred quality.
- **Color Palette:** Bright pink/magenta, bright yellow, and cyan/blue for the neon letters and border. Warm yellow/orange interior background tones. Colorful light flares in green, blue, and red around edges. Highly saturated and contrasting.
- **Art Style:** Photographic/neon glow aesthetic rather than traditional cel-shaded 2D. Slightly grainy photographic quality with visible light flares and reflections. Dreamy, nighttime captured look. Modern and energetic.
- **Composition:** Central focus on the neon sign. Circular vignette framing creates a spotlight effect, darkening edges. Colorful light flares create a magical, whimsical atmosphere. The neon sign is the dominant visual element.
- **Text:** "SHOT" in bright pink/magenta neon letters at top, "100IS" in bright yellow neon letters below. The entire sign has a glowing cyan/blue neon border. Text appears slightly distorted due to the circular vignette framing.

---

### CV-09 | ChapterHeaders/ch09_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A cheerful young boy with dark spiky hair and large expressive eyes, captured mid-action with arms and legs extended as if jumping or flying. He has a wide enthusiastic smile and confident expression. He wears a black t-shirt with white text "PLAYER1," blue athletic shorts with white stripes, bright red gloves with glowing blue accents on palms, black knee pads with colorful designs, red athletic shoes with blue/white accents and glowing blue soles, and black over-ear headphones with purple accents.
- **Background/Setting:** Stylized cityscape with tall buildings rendered in soft focus, creating depth. Sky has warm sunset-like colors transitioning from yellow to orange. Radial light rays emanate from behind the character enhancing the dynamic feel. No interior setting visible — outdoor urban environment.
- **Color Palette:** Warm oranges and yellows in background. Bold reds for gloves and shoes. Cool blues for shorts, shoe accents, and glowing elements. Black and white for clothing contrast. Bright, vibrant, and engaging overall.
- **Art Style:** Cel-shaded 2D with thick clean black outlines defining all elements. Flat color fills with subtle shading. Smooth gradients for depth. Slightly exaggerated cartoonish aesthetic. Dynamic posing and perspective.
- **Composition:** Circular crop with radial burst effects from behind the character. Character positioned slightly off-center for visual interest. Classic chapter header design drawing the eye to the central figure. Sense of energy and movement.
- **Text:** "PLAYER1" in white text on the black t-shirt.

---

### CV-10 | ChapterHeaders/ch10_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A central small boxy white robot with a black screen face displaying two large circular glowing blue eyes with spiral patterns and a simple red curved smile line. Two thin white antennae on top. White arms with black segments and black rounded feet. Surrounding the robot are four hands of different skin tones reaching toward it — one green, one light brown, one darker brown, and one medium brown — suggesting diversity and inclusion. No fully depicted human characters; only the hands are visible.
- **Background/Setting:** Soft out-of-focus circular vignette with a gradient of warm colors, primarily shades of orange and yellow, with lighter almost-white highlights. Creates a glowing, magical atmosphere as if the robot is the center of a warm, friendly light. No specific architectural or environmental details.
- **Color Palette:** Warm oranges and yellows for background glow. White robot body. Bright blue glowing eyes. Red smile. Varied skin tones and green for the hands. Bright and saturated, cheerful and positive.
- **Art Style:** Vibrant cel-shaded 2D with bold, dark, consistent outlines. Flat solid colors with absence of complex shading except for the background vignette gradient. Clean, bold, and visually appealing for a young audience.
- **Composition:** Robot at the absolute center with hands reaching toward it from all sides. Circular vignette framing. Warm glowing background reinforces the robot as focal point. Composition suggests connection, friendship, and collaboration.
- **Text:** No visible text.

---

### CV-11 | ChapterHeaders/ch11_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** Central robot: white box-shaped with rounded edges, two white antennae with black tips, large screen face with bright blue glowing circular eyes with intricate patterns, a simple red curved-line smile, black and white limbs with rounded joints, black shoes/feet. Left human character: wearing a dark blue coat with a distinctive red fur collar, brown hair visible, appears to be a child/young person. Right human character: wearing a brown coat, face partially visible showing a friendly expression, also appears to be a child/young person.
- **Background/Setting:** Indoor environment with warm yellowish lighting. Wooden floor visible beneath the characters. Blurred background suggesting interior walls or furniture. Circular vignette creates an intimate, focused composition.
- **Color Palette:** Bright and cheerful with high contrast. White (robot), blue (eyes and left character's coat), red (smile and fur collar), brown (right character's coat and floor). Warm yellow/orange background tones. Clean, bold colors.
- **Art Style:** Vibrant cel-shaded 2D with bold black outlines. Smooth color gradients and shading. Simplified cartoonish proportions. Friendly, approachable character designs. Modern digital illustration with a classic children's book feel.
- **Composition:** Robot as the central focal point flanked by two human figures on either side. Circular framing draws the reader's eye to the robot. Balanced composition suggesting interaction and story between the three characters.
- **Text:** No clearly legible text. Small symbols or markings may be present on the robot's screen area but are not readable.

---

### CV-12 | ChapterHeaders/ch12_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters present. The scene is object-focused on the smartphone.
- **Background/Setting:** Dark environment with no visible architectural details. The smartphone is the sole object, centrally positioned. Curved glowing light rays or energy waves radiate outward from the phone, suggesting signal transmission or activation. Circular gradient background transitions from deep red at center to lighter orange and yellow tones toward edges.
- **Color Palette:** Rich reds and oranges dominate, creating a warm energetic atmosphere. Deep red center, lighter orange and yellow edges. Silver/metallic for the phone border. Bright red capital letters on screen. White highlights on glowing rays. High contrast.
- **Art Style:** Digital vector-based appearance with smooth gradients and glowing effects. Incorporates cel-shading characteristics with bold color blocks but also modern digital glow effects and smooth gradients. Contemporary tech-inspired look rather than traditional cel animation.
- **Composition:** Smartphone centrally positioned within circular frame. Symmetrical design with curved glowing light rays creating balanced visual movement on both sides. The phone is oriented vertically. Eye drawn inward to the screen. Designed as a striking chapter header.
- **Text:** "LOCED" displayed in bold bright red capital letters on the smartphone's black screen — likely a stylized abbreviation of "LOCATED" or "LOCKED."

---

### CV-13 | ChapterHeaders/ch13_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A pixelated portrait of a person with curly dark hair, expressive eyes, and a subtle smile is visible on the CRT television screen. The face is rendered in a stylized, simplified manner with distinct facial features including eyes, nose, and mouth.
- **Background/Setting:** A vintage beige/tan CRT television set sits on a wooden surface. The TV has visible control knobs and ventilation grilles. The screen displays horizontal glitch lines and circular patterns behind the portrait. Warm wooden surface underneath.
- **Color Palette:** Warm beige/tan (TV casing), vibrant purple and pink (background illumination and screen), yellow tones in the pixelated portrait, warm browns (wooden surface). Retro-futuristic contrast between old technology and digital elements.
- **Art Style:** Cel-shaded 2D with bold outlines defining the television. The portrait on screen uses a pixelated mosaic technique reminiscent of retro video games. Glitch effects add dynamic, magical quality. Dramatic lighting with strong highlights and shadows.
- **Composition:** Circular vignette framing. CRT television positioned centrally as the focal point. The pixelated portrait draws the eye to the screen center.
- **Text:** No visible text.

---

### CV-14 | ChapterHeaders/ch14_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A human hand (adult's) actively drawing with a black pen on a notebook page. The hand has natural skin tone with red ink marks on the fingers, suggesting recent creative activity.
- **Background/Setting:** A spiral-bound notebook with cream-colored pages sits on a wooden surface. A white cylindrical object (another pen/marker) is visible on the left. The notebook page features a geometric starburst pattern with radiating colored lines connecting to polyhedrons/cubes.
- **Color Palette:** Warm cream (notebook paper), natural skin tone, vibrant blue/yellow/green/red/purple (drawing lines), warm browns (wooden surface). Darker edges from vignette effect.
- **Art Style:** Photographic quality with the hand-drawn artwork inside rendered in bold, clear lines with distinct color separation. Circular vignette creates a storybook-like framing effect. Warm, slightly vintage filtered photograph aesthetic.
- **Composition:** Circular vignette focusing on the hand and notebook. Shallow depth of field with notebook in sharp focus and background softly blurred. Drawing is the central focal point.
- **Text:** Possible handwritten text on the page (not fully legible); red ink splatters near the bottom of the page.

---

### CV-15 | ChapterHeaders/ch15_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A single stylized cartoon hand holding a red and silver soldering iron, actively emitting bright orange sparks. Rendered in warm skin tones.
- **Background/Setting:** A workshop/maker space with a wooden workbench. A green circuit board with electronic components (resistors, capacitors) and a red wire sits on the desk. Red-handled pliers lie nearby. An open manual with text/diagrams is visible. Background includes a window with blinds, shelves with bottles/jars, and a tool container holding screwdrivers.
- **Color Palette:** Rich browns (wood), golden yellows/oranges (light and sparks), reds (tool handles), green (circuit board), blue (some components). Warm, late-afternoon sunlight quality.
- **Art Style:** Vibrant cel-shaded 2D with thick, bold black outlines defining every object. Flat, solid colors without complex gradients. Simplified and friendly cartoonish style. Strong sense of depth through perspective.
- **Composition:** Circular vignette framing. Hand and soldering iron on the right, circuit board and manual on the left. Sparks provide dynamic energy at the center focal point.
- **Text:** Text visible on the open manual/notebook (not legible due to stylization and size).

---

### CV-16 | ChapterHeaders/ch16_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A stylized cartoon hand holding a red and silver soldering iron, actively creating bright orange-yellow sparks. The hand is rendered in warm skin tones.
- **Background/Setting:** A well-stocked workshop with a green circuit board on a wooden desk, red-handled pliers nearby, a white instruction manual/schematic sheet, and a tool caddy on the left. Background shelves contain bottles and containers. A window with blinds lets in warm light.
- **Color Palette:** Warm wood browns, amber lighting, red tool handles, cool green circuit board, blue bottles on shelves, bright orange-yellow spark effects. Overall warm, late-afternoon quality with directional sunlight.
- **Art Style:** Vibrant cel-shaded 2D with bold, dark outlines. Smooth color gradients within shapes. Dramatic lighting with strong highlights and shadows. Slightly retro children's illustration feel.
- **Composition:** Circular vignette framing focusing on the central soldering action. Hand and soldering iron positioned in the upper right quadrant. Circuit board and tools create a balanced workshop scene.
- **Text:** No visible text.

---

### CV-17 | ChapterHeaders/ch17_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters visible. The scene is purely environmental.
- **Background/Setting:** An underground stone/brick tunnel with rough, uneven walls and an arched ceiling of visible stone blocks. The floor consists of irregular stone flagstones. Two large aged metal doors with visible scratches and wear stand at the tunnel's end. The doors have different handles — one a lever, one a round knob. Two wall-mounted spotlights cast converging beams.
- **Color Palette:** Blue-gray stone, warm yellows/oranges from spotlights, weathered gray metal doors. Muted overall palette with strong light/dark contrasts. Cool blue-white beam from left light, warm yellow-orange beam from right.
- **Art Style:** Vibrant cel-shaded 2D with bold black outlines. Flat color fills with minimal gradients. Cartoonish yet detailed texture work on stone surfaces. Dramatic lighting typical of adventure/fantasy illustrations.
- **Composition:** Circular vignette with strong one-point perspective drawing the eye toward the doors at the end of the tunnel. Dual spotlight beams converge at center, creating dramatic focal point. Designed to evoke suspense and mystery.
- **Text:** No visible text.

---

### CV-18 | ChapterHeaders/ch18_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters visible. The scene focuses on the computer and desk objects.
- **Background/Setting:** An Apple iMac workstation with silver/white casing on a desk. A black keyboard with greenish backlighting, a black mouse to the right, and a beige/tan coffee mug on the left. Cables connect the peripherals. The screen displays the word "CONNECTED" in large white text against a vibrant green background with a glowing circular effect, surrounded by colorful confetti/streamers.
- **Color Palette:** Dominant green (screen background), warm yellow/orange ambient lighting, silver/white (iMac), black (keyboard/mouse), multicolored confetti (orange, yellow, green, blue, pink). Warm directional lighting from above.
- **Art Style:** High-quality photorealistic 3D render or photograph with polished, professional appearance. The screen content uses bold, graphic typography and celebratory confetti elements. Not cel-shaded 2D — more of a rendered/photographic style.
- **Composition:** Computer centered in a circular vignette frame. Keyboard directly in front, mouse to the right, coffee mug to the left. The glowing screen radiates light as the central focal point. Warm, cozy atmosphere.
- **Text:** "CONNECTED" displayed prominently in large white text on the iMac screen.

---

### CV-19 | ChapterHeaders/ch19_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A small white boxy robot with a square head and rectangular body. Two short white antennae on top. Large, circular glowing blue eyes with a pixelated/starry pattern. Sad/worried expression — downturned black eyebrows and a small downturned red mouth. Black articulated hands and rounded black feet.
- **Background/Setting:** A cozy, sunlit room (child's playroom or bedroom). A window with light-colored curtains on the left lets in warm golden sunlight creating soft glow and long shadows. A wooden shelf/mantelpiece on the right holds a potted plant and colorful objects. Warm light brown floor. Colorful balls (red, green, blue, pink) partially visible in the foreground.
- **Color Palette:** Soft yellows, oranges, and browns from the warm lighting. White robot body with black accents. Vibrant luminous blue eyes. Green plant, colorful balls and shelf items as pops of color. Cheerful, warm overall palette.
- **Art Style:** Vibrant cel-shaded 2D with thick, bold black outlines. Flat, solid colors without complex gradients. Soft, diffused lighting creating a gentle, comforting atmosphere. Clean, graphic, cartoonish quality.
- **Composition:** Circular vignette drawing focus directly to the sad robot at center. Robot is the clear focal point. Warm sunlit background contrasts with the robot's melancholy expression to create emotional tension.
- **Text:** No visible text.

---

### CV-20 | ChapterHeaders/ch20_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** Two humans visible only from the knees down, wearing brown lace-up shoes and casual trousers (one gray, one beige/khaki). A small white and gray boxy robot with two antennae, blue and red circular eyes, and a simple friendly expression stands to the right of the plate.
- **Background/Setting:** Indoor scene on light brown wooden plank flooring. A white plate holds a pile of golden-brown pastries/cookies (croissant-shaped). A classic brass-based table lamp with a white dome shade casts warm yellowish light behind the plate. A wooden door and cabinet visible to the left suggest a kitchen or dining room.
- **Color Palette:** Warm browns (floor, shoes), yellows (lamp light, pastries), whites (plate, robot body, lamp shade). Blue and red robot eyes as accent pops. Soft golden hue from the lighting enhances the cozy atmosphere.
- **Composition:** Circular vignette framing. The plate of pastries is the central focal point. Two pairs of legs frame the plate from both sides. Robot observes from the right. Lamp provides warm backlighting. Creates an intimate, shared-moment feel.
- **Text:** No visible text.

---

### CV-21 | ChapterHeaders/ch21_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters visible. The scene is a still life/environmental shot.
- **Background/Setting:** A lush green park with tall trees with thick trunks and green-yellow foliage forming a canopy. A brown wooden park bench with black metal armrests and legs sits on a stone pathway of irregular gray pavers. White dandelions dot the grass. A white ceramic bowl filled with popcorn sits on the bench alongside three colorful cereal boxes.
- **Color Palette:** Dominant greens (grass, trees), warm yellows and golds (sunlight, dandelion flowers), rich browns (bench, tree trunks), bright saturated colors on cereal boxes (blue, orange). Soft whites and grays for path and bowl. Warm golden sunlight filtering through trees.
- **Art Style:** Vibrant cel-shaded 2D with crisp outlines and solid color blocks. Balances detailed foreground elements with a softly rendered background. Nostalgic, timeless quality. Reminiscent of both traditional illustration and modern digital animation.
- **Composition:** Circular vignette framing. Bench positioned centrally. Bowl and cereal boxes on the bench create the focal point. Trees and dandelions frame the scene. Peaceful, inviting park atmosphere with early morning or late afternoon lighting.
- **Text:** Handwritten text visible on the page (partially legible). Cereal boxes display "Cocoa" and "Frosted" branding.

---

### CV-22 | ChapterHeaders/ch22_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters (people or animals) visible. The focus is entirely on setting and objects.
- **Background/Setting:** A lush green park with tall trees, grassy field dotted with white dandelions, and a stone pathway leading toward a brown wooden park bench with black metal legs. On the bench: a white bowl filled with a light brown puffed snack (popcorn/cereal) and three brightly colored cereal boxes — blue (Cheerios), light blue (Frosted Flakes), and orange (Froot Loops).
- **Color Palette:** Warm and vibrant — greens (grass, trees), browns (bench, path), yellows (sunlight, dandelions), blue/light blue/orange (cereal boxes). Soft hazy yellow sky suggesting a sunny day. Cheerful, saturated palette.
- **Art Style:** Vibrant cel-shaded 2D with very bold, clean black outlines. Flat, saturated colors typical of modern children's book illustrations. Soft, diffused lighting with a gentle warm glow. Polished, graphic look.
- **Composition:** Circular vignette drawing the eye to the bench and items on it. Classic design choice for chapter headers creating intimacy. Pathway leads the viewer's gaze to the bench. Absence of characters invites reader imagination.
- **Text:** Brand names visible on cereal boxes: "Cheerios," "Frosted Flakes," and "Froot Loops."

---

### CV-23 | ChapterHeaders/ch23_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No characters visible. The scene is purely atmospheric/environmental.
- **Background/Setting:** A narrow brick corridor extending into the distance with orange-brown walls showing visible mortar lines. Exposed pipes run vertically along walls. Coiled ropes/cables hang from hooks on the left wall. Tangled wires and cables run along the ceiling and walls. A single exposed light bulb hangs from the ceiling in the distance. A blue glowing crown symbol is painted or projected on the right wall. Rectangular brick/tile floor.
- **Color Palette:** Dominant warm orange-brown (bricks, golden lighting). Cool accents: blue-green light from the bulb, blue crown symbol. Strong warm foreground vs. cool background contrast.
- **Art Style:** Vibrant cel-shaded 2D with bold black outlines defining all shapes. Flat color fills with subtle shading. Vibrant, saturated colors. Dramatic one-point perspective drawing the eye toward the distant light.
- **Composition:** Circular vignette (peephole/telescope framing). Strong perspective lines guide the eye to the hanging light bulb in the distance. Blue crown symbol on the right wall adds mystery. Creates anticipation and a sense of discovery.
- **Text:** No visible text.

---

### CV-24 | ChapterHeaders/ch24_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A white robot with a square head and body, two antennae on top, large expressive blue eyes on its screen face, a cheerful red smile. Black limbs with white gloves and black feet. Friendly, approachable design sitting on a white box/platform.
- **Background/Setting:** A tech/server room environment. A tall server rack on the left with multiple blue indicator lights. Various colored cables (blue, yellow, black) connect to the server. A computer monitor in the background displays a map with red dots. Warm yellow/orange lighting throughout.
- **Color Palette:** Warm yellow/orange dominant lighting. White robot body with black limbs. Bright blue (eyes, server lights). Red (smile, map dots). Multi-colored cables (blue, yellow, black). Cozy atmosphere with strong contrast.
- **Art Style:** Clean cel-shaded 2D with bold black outlines. Smooth, flat coloring with no gradients. Simplified, cartoonish proportions typical of children's animation. Friendly, approachable aesthetic.
- **Composition:** Circular vignette framing. Robot is the central focal point sitting on a platform. Server rack on the left, monitor in the background. Balanced composition between the character and technical elements. The robot serves as a welcoming guide through the tech environment.
- **Text:** No visible text.

---

### CV-25 | ChapterHeaders/ch25_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No visible characters. The vignette is an object-focused scene.
- **Background/Setting:** A warm gradient background transitioning from golden yellow-orange at center to cool blue at edges, creating a circular vignette effect. No distinct architectural or environmental setting.
- **Color Palette:** Warm yellows and oranges for the gradient background; earthy browns and grays for the briefcase; vibrant red, green, blue, and yellow for wires and components; glowing red-orange for the central sphere. Overall warm temperature.
- **Art Style:** Vibrant cel-shaded 2D with bold black outlines. Flat color application with minimal shading. Cartoonish, approachable quality with simplified shapes suitable for children's illustration.
- **Composition:** Open briefcase positioned centrally with lid angled open. A glowing red sphere at the center emits sparks, creating the focal point. Colorful wires create dynamic flowing lines leading the eye through the composition. Circular gradient background frames the entire scene.
- **Text:** No visible text.

---

### CV-26 | ChapterHeaders/ch26_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No visible characters (no people, robots, or creatures). The scene is object-focused.
- **Background/Setting:** A cozy, focused workspace/desk environment. A warm, softly lit background with bokeh-style glowing circular lights suggesting a late-night indoor setting. Objects rest on a brown wooden desk surface.
- **Color Palette:** Dominant warm tones — browns and yellows for the desk and ambient lighting. Cool contrast from bright green text/graph on the screens. Dark blue/black for the device screens. Metallic/silver tones for the glasses.
- **Art Style:** Cel-shaded 2D cartoon style with bold, dark outlines defining all shapes. Flat, solid colors without complex shading. Simplified cartoonish device designs. Circular vignette framing focuses attention on the central objects.
- **Composition:** A tablet/smartphone lies in the foreground on the desk, displaying a bright green jagged line graph (heartbeat/data monitor). Behind it, a computer monitor shows green code text. A pair of round eyeglasses rests on top of the monitor. Warm glowing lights in the background create depth and atmosphere.
- **Text:** Programming code visible on the laptop screen (words like "if", "for", "function"). The tablet screen shows a green waveform/graph with a small label at the bottom. No other legible text.

---

### CV-27 | ChapterHeaders/ch27_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No visible characters (no people, robots, or creatures). The image is a purely abstract composition.
- **Background/Setting:** A plain, warm beige/light tan wall providing a neutral gallery-like backdrop. The abstract painting fills a square canvas set within a thin circular metallic frame.
- **Color Palette:** Extensive and highly saturated spectrum — warm colors include bright yellows, oranges, reds, and pinks; cool colors include various greens, blues, and purples. Dynamic contrast between warm and cool tones throughout.
- **Art Style:** Abstract expressionist mosaic/pixelated style with irregular blocky shapes and patches of overlapping color. Notably does NOT feature bold outlines or cel-shading — this is a purely abstract, non-representational composition with a textured, digital mosaic quality.
- **Composition:** Square abstract painting displayed within a thin circular frame mounted on a wall. The canvas is entirely filled with vibrant color blocks in an organic, seemingly random pattern with no negative space. No focal point — the composition is evenly distributed.
- **Text:** No visible text.

---

### CV-28 | ChapterHeaders/ch28_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No visible characters. The vignette is object-focused.
- **Background/Setting:** Outdoor garden or park environment. Green trees and foliage in the distance, pink and white flowers visible. A sun visible in the upper portion creating warm golden light. Ground is a mix of dirt, small rocks, and grass. Suggests morning or late afternoon.
- **Color Palette:** Warm tones dominate — golden yellows, oranges, and browns. Various greens (lime to forest) for foliage. Metallic silver and copper/bronze for the nozzle. Blue and white for water. Soft pink and white for flowers. Earthy browns and tans for the ground. Overall warm, sunlit temperature.
- **Art Style:** Clearly cel-shaded 2D illustration with bold, dark outlines defining all elements. Flat color application with minimal shading. Simplified shapes and forms suitable for children's illustration. Cartoonish and friendly with exaggerated proportions.
- **Composition:** A metallic garden hose nozzle is the central focus, positioned on a dirt patch with small plants and grass. Water flows actively from the nozzle, creating splashes and a small puddle on the ground. The hose curves around and extends out of frame. Circular vignette creates a focused, intimate view of the scene.
- **Text:** No visible text.

---

### CV-29 | ChapterHeaders/ch29_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No visible characters. The vignette is an abstract/map-based scene.
- **Background/Setting:** A yellowish-brown or sepia-toned map/grid pattern resembling city streets or a radar screen. Dark brown/black grid lines create a network of intersecting streets or pathways. The overall setting suggests a digital or technological surveillance environment.
- **Color Palette:** Sepia/yellowish-brown for the background map. Various shades of red (bright crimson to darker maroon) for the central glitch area and scattered dots. Dark brown/black for the grid lines. Creates a vintage/retro technological feel.
- **Art Style:** Cel-shaded 2D style with bold, clean outlines. Sharply defined edges with strong contrast. Digital, vector-like quality with flat color application. The glitch effect in the central red area adds a modern digital corruption aesthetic. Retro video game or early computer graphics feel.
- **Composition:** A large, irregularly shaped red area dominates the center, appearing pixelated or glitchy with a jagged, fragmented edge. Numerous smaller red dots of varying sizes are scattered throughout the map. Dark circular vignette edges that lighten toward the center.
- **Text:** No visible text.

---

### CV-30 | ChapterHeaders/ch30_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A friendly anthropomorphic robot. Head is a white cube with a large blue screen face displaying two expressive glowing blue eyes with black pupils and a wide red smiling mouth. Two small white spherical antennae on top. Simple blocky white body. Black arms with white gloves, white legs with black feet/shoes. Dynamic floating/jumping pose — one arm extended forward holding a thick black cable, other arm slightly raised. Happy, approachable expression.
- **Background/Setting:** A server room or high-tech laboratory. Tall black server racks on both left and right sides, populated with colored indicator lights (green, yellow, red) and control panels. Coiled cables visible on the floor. Warm yellowish-orange lighting creating a cozy yet futuristic atmosphere. Light-colored floor surface.
- **Color Palette:** Warm yellows and oranges dominating the background. Cool bright blue for the robot's face, eyes, and electrical sparks. White and black for the robot's body. Black for the server racks. Creates strong warm/cool contrast.
- **Art Style:** Clearly cel-shaded 2D with very prominent thick black outlines defining every shape. Flat solid colors. Modern animated cartoon style. Clean, bold visual impact suited for children's media.
- **Composition:** Robot is the central focal point, viewed at a slight angle within the circular vignette. Dynamic pose suggests action. A thick black cable held by the robot emits bright jagged blue electrical sparks — a key visual element suggesting a "glitch." Server racks frame the character on both sides. Circular vignette crop focuses attention on the robot.
- **Text:** No visible text.

---

### CV-31 | ChapterHeaders/ch31_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A small white robot with a boxy rounded head and cylindrical body. Face is a bright sky-blue square with glossy finish, two large expressive cartoonish blue eyes with star-like glowing centers, and a wide red smiling mouth. Two small white antennae on top. Red circular detail (button/speaker) on the side of its head. Black and white articulated arms and legs, white shoes with dark soles. Captured mid-jump — one arm raised in a fist, the other extended forward. Very happy, enthusiastic expression.
- **Background/Setting:** Soft, out-of-focus circular vignette drawing attention to the character. Sunny, idyllic outdoor setting — hints of buildings with warm orange and yellow roofs in the distance suggesting a friendly village or magical landscape. Warm, golden lighting creating a cheerful atmosphere.
- **Color Palette:** Bright and cheerful — warm orange, yellow, and peach gradients for the background. White for the robot body. Bright blue for the face. Red accents (mouth, side detail, confetti). Blue, red, and yellow for confetti. Overall warm temperature.
- **Art Style:** Cel-shaded 2D with strong, bold black outlines defining all shapes. Flat solid colors with subtle gradients in the background for depth. Clean, simple, cartoonish style suitable for children's media.
- **Composition:** Robot is the clear central focal point, captured in a dynamic mid-air jump pose. Colorful confetti-like shapes (red, blue, yellow) scattered around the robot add festive energy. Circular vignette effectively frames the character against the warm background.
- **Text:** No visible text.

---

### CV-32 | ChapterHeaders/ch32_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A white humanoid robot with black accents visible through a circular window/portal on the right wall. Simple friendly design with round head, large eyes, and articulated limbs. Stationary, welcoming pose with neutral expression. Small cartoon characters displayed on computer monitors (details limited by size). Illustrated children characters visible on wall posters in various poses.
- **Background/Setting:** A cozy tech lab or workshop with pegboard walls. Warm, inviting lighting. A circular window or portal on the right wall reveals the robot. Functional yet friendly creative workspace.
- **Color Palette:** Warm earth tones — browns, tans, and beiges for the room. Yellow/orange for string lights. White and black for the robot. Various colors on posters and computer screens. Overall warm, inviting temperature.
- **Art Style:** Clearly cel-shaded 2D illustration with bold dark outlines. Flat color application with minimal shading. Cartoonish, approachable character designs. Clean, simplified forms for children's book illustration. Circular vignette focuses attention on the central workspace.
- **Composition:** Three computer monitors on a wooden desk (left: cartoon character, center: interface elements, right: blue screen). Keyboard and mouse on desk. Computer towers beneath. String lights in zigzag pattern on ceiling. Two colorful posters on pegboard wall. Cardboard box under desk. Robot appears through a circular window/portal on the right. Warm, layered composition creating depth.
- **Text:** Text appears on wall posters (not clearly legible). Computer screens display interface elements (too small to read confidently). No prominent text visible.

---

### CV-33 | ChapterHeaders/ch33_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No visible human characters. The central subject is a detailed mechanical robot — metallic silver/gray with a rectangular body and articulated legs. Two antenna protrusions on top. A small control module with a blue screen. A large circular lens/sensor on one side. Blue glowing circuit patterns visible through transparent panels. Standing on a simple wooden floor surface with a faint grid pattern.
- **Background/Setting:** Warm orange-brown gradient background transitioning from warm edges to lighter tone near the robot. Simple wooden floor with faint grid pattern suggesting a laboratory or technical setting.
- **Color Palette:** Metallic grays/silvers for the robot body. Bright blue for glowing circuitry and control screen. Warm orange-brown for background gradient. Wooden brown for the floor. Overall warm temperature with cool blue accents.
- **Art Style:** Vibrant cel-shading with bold black outlines defining all elements. Cartoonish yet technical — balancing whimsy with mechanical detail. Dramatic lighting with blue circuitry glowing from within transparent panels.
- **Composition:** Robot positioned centrally, viewed from a slightly low angle to emphasize presence. Circular vignette creates a focused, intimate view. Multiple handwritten-style text labels with arrows point to different robot components, creating an educational/technical diagram feel.
- **Text:** Multiple visible labels: "blorg-tia" (top module), "flavor" (side panel), "dark matter" (side panel), "plasma" (side panel), "energy & bacteria" (lower section), "turret antenna for comms" (side), "photo (to) braincracker" (lens area), "site of omni-lens to view the universe, please" (bottom area). Playful, educational labeling style.

---

### CV-34 | ChapterHeaders/ch34_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** No visible characters. The vignette is an environment/object-focused scene.
- **Background/Setting:** A city skyline during sunrise or sunset, with the sun visible near the horizon between tall buildings. Various skyscrapers of different heights creating an urban silhouette. Viewed from an elevated viewpoint (balcony) with a railing visible in the lower portion.
- **Color Palette:** Dominant warm tones — orange and yellow for the sky and sunset. Golden brown for the food item. Darker browns and grays for the buildings and railing. White for the plate. Warm, inviting atmosphere typical of evening/morning light. Overall warm temperature.
- **Art Style:** Cel-shaded 2D with bold clean outlines. Flat colors with minimal gradients. Graphic, cartoon-like appearance suitable for children's book illustration. Circular vignette framing creates focused, intimate view.
- **Composition:** A plate with a hot dog or wrapped food item (golden-brown with red filling visible at one end) positioned in the lower right foreground. City skyline spans the background with sunset/sunrise lighting. Balcony railing in lower portion. Circular vignette creates atmospheric, scene-setting composition.
- **Text:** No visible text.

---

### CV-35 | ChapterHeaders/ch35_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** Multiple characters visible within photographs pinned to a corkboard: (1) A man in a dark suit and hat sitting at a desk with papers — detective/official. (2) A man in a brown jacket and glasses, serious expression. (3) A woman in a dark coat and hat with arms crossed, determined look. (4) A young girl in a pink shirt, cheerful. (5) A young boy in a dark suit, serious expression. (6) A girl in a dark jacket. (7) A young boy sitting outdoors on a rock, contemplative. (8) A small figure (child or robot) standing in a field. (9) A landscape/nature scene. No characters appear directly — all are within the photo-within-image framing.
- **Background/Setting:** A textured brown corkboard serving as a detective board or "wall of clues." Photos are pinned to the board with red strings creating a web-like connection between them. Gallery-like presentation.
- **Color Palette:** Warm brown for the corkboard. Red for the connecting strings. Bright cyan/light blue for the neon logo glow. Blue for the "NexCorp" text. Light pink for question marks. Various colors from the photographs (dark blues, browns, pinks, greens). Overall warm temperature with cool neon accents.
- **Art Style:** Cel-shaded 2D with bold dark outlines. Flat solid colors. Clean, graphic, slightly retro feel. The neon logo provides a strong light source with subtle glow on surrounding corkboard. Bold, highly stylized aesthetic suitable for children's book.
- **Composition:** Nine photographs arranged on the corkboard, connected by red strings. At the center, a glowing circular neon sign with a light blue outer ring and bright cyan inner glow containing two light pink question marks and the text "NexCorp." Web-like string connections create visual movement across the board. Circular vignette framing.
- **Text:** "NexCorp" in bold blue sans-serif font at the center of the neon logo. The "Nex" portion in darker blue, "Corp" in lighter vibrant blue with a subtle wave-like underline. Two pink question marks accompany the text.

---

### CV-36 | ChapterHeaders/ch36_vignette.png | PASS
- **Used In:** B1 (BUILD)
- **Characters:** A single character seen from behind — simple rounded head with warm peach-colored complexion. Small curved shape on top (ear or hair tuft). Wearing a dark black collar or strap around the neck. Large prominent goggles dominate the foreground — metallic bronze/gold frames with thick bold black outlines. Lenses are dark and reflective with subtle blue-green glow and hints of city lights reflected. Black strap secures goggles around the back of the head.
- **Background/Setting:** A stylized futuristic city at twilight/dusk. Sky transitions from deep blue at top to warm oranges and pinks near the horizon (sunset). Tall buildings in dark muted tones (blues, browns, blacks) make bright neon lights pop. Buildings illuminated with neon lights in pink, green, blue, and yellow. Urban, futuristic atmosphere.
- **Color Palette:** Highly saturated — cool blues and purples blended with warm oranges and pinks in the sky. Bright neon pink, green, blue, and yellow for city lights. Warm peach for the character's skin. Metallic gold and dark reflective elements for goggles. Strong warm/cool contrast.
- **Art Style:** Vibrant cel-shaded 2D with very bold, clean black outlines. Flat, solid colors with strong contrasts. Modern animated cartoon style. Clear, engaging, and easy to interpret for children's media.
- **Composition:** Character seen from behind in the foreground, gazing out at the cityscape. Goggles are the dominant visual element in the foreground, framing the perspective. The futuristic city fills the background with colorful neon lights. Circular vignette creates an intimate, focused view — as if looking through a porthole or the character's goggles. Builds curiosity about what the character is experiencing.
- **Text:** Stylized signs on buildings — a vertical pink neon sign on the left (possibly "HOTEL," artistic and not perfectly legible). A square sign on the bottom right with a letter resembling "E." These are integrated into the city aesthetic.

---

## Strips (28 items) - All MCP-verified

### B1-S01 | Strips/strip_maya_inventions.png | Ch1 | PASS (regenerated, 4 stitched panels)
- **Used In:** B1 (BUILD)
- 4-panel stitched strip (256px panels, dark dividers). P1: Brown-haired girl in blue shirt with backpack holding crystalline object, kitchen with shelves. P2: Girl with toothbrush and floating musical notes, bathroom scene, concerned expression. P3: White boxy robot with blue eyes and speech bubble, children looking with curiosity. P4: Kitchen pot overflowing with orange liquid, splashed walls and floor, chaotic mess. Each panel individually generated then stitched with numpy. Content matches failed-inventions sequence.

### B1-S02 | Strips/strip_maya_day.png | Ch4 | PASS
- **Used In:** B1 (BUILD)
- 3-panel strip. P1: Three children (boy in green shirt eating, girl in yellow, girl in red) around wooden table with food in kitchen, wooden cabinets, window. P2: Child on bed with silver/blue metallic robot seated on chair beside bed, robot extending arm toward child, bedroom with desk/lamp/teapot. P3: Child in red shirt reaching toward white glowing cube on desk, another child asleep in bed, bedroom setting. Cel-shaded with clear outlines, warm browns/yellows/blues palette.

### B1-S03 | Strips/strip_glitch_wave.png | Ch6 | PASS (regenerated, 6 stitched panels)
- **Used In:** B1 (BUILD)
- 6-panel stitched strip. P1: City street with traffic light and cars. P2: Indoor scene with broken window, water splashing, orange cat looking startled (intentional per story — sprinklers spray cat). P3: Tablet/device screen showing cat image (intentional — digital photo frame with cat meme). P4: Drone flying with falling cardboard boxes against blue sky. P5: Smart device with musical note icon. P6: Two boys looking out window with shocked expressions at chaos. Each panel individually generated then stitched. Content matches glitch-wave chaos spreading sequence.

### B1-S04 | Strips/strip_leo_traces_signal.png | Ch7 | PASS
- **Used In:** B1 (BUILD)
- 4-panel strip. P1: Brown-haired boy in greenish-gray long-sleeve shirt seated at wooden desk writing, bookshelf with colored books, computer monitor with code, warm lamp. P2: Same boy in beige sweater typing on silver laptop with glowing blue circular futuristic interface, larger monitor behind with same interface. P3: Boy in light brown short-sleeve shirt at laptop with blue screen, focused expression, window showing darkening sky. P4: Boy in gray t-shirt sprinting on wet cobblestone street at night, fist clenched, street lamps casting long shadows. Cel-shaded, warm-to-cool palette progression from day to night.

### B1-S05 | Strips/strip_zara_photo_trail.png | Ch8 | PASS (regenerated, 5 stitched panels)
- **Used In:** B1 (BUILD)
- 5-panel stitched strip. P1: City street scene with traffic lights, crosswalks, buildings. P2: Interior with window view, sprinkler spraying water, microphone stand. P3: Brown and white dog (Boxer) with illuminated colorful collar, concerned expression (intentional — confused dog with LED collar per story). P4: Drone carrying brown boxes against blue sky with clouds. P5: Nighttime scene with castle/fortress, rainbow light beam, dark starry sky. Each panel individually generated then stitched. Content matches photo-trail through-the-lens sequence.

### B1-S06 | Strips/strip_sam_arrives.png | Ch9 | PASS
- **Used In:** B1 (BUILD)
- 4-panel strip. P1: Boy in blue shirt visible on two computer monitors showing code, dim room with desk and green plants. P2: Boy in blue shirt running out of open doorway smiling, grassy outdoor area, warm golden sunlight. P3: Empty park scene with wooden bench on green grass, tall trees, clear blue sky. P4: Boy in tan shirt running back into house through open doorway, red brick exterior, both arms outstretched. Bold outlines, flat cel-shaded colors, cool-to-warm palette shift.

### B1-S07 | Strips/strip_first_reactions.png | Ch10 | PASS (regenerated, 4 stitched panels)
- **Used In:** B1 (BUILD)
- 4-panel stitched strip. P1: Girl with brown hair, green vest over white shirt, wide surprised eyes, white robot with blue elements. P2: Boy in blue beanie and blue shirt looking at tablet with concerned expression, small white robot beside tablet. P3: Girl in blue denim jacket, smiling broadly, holding two white devices/robots. P4: Boy in gray hoodie with red gloves pointing at small white device/robot with concerned expression. Each panel individually generated then stitched. Content matches each kid's first reaction to Blip.

### B1-S08 | Strips/strip_blip_greetings.png | Ch11 | PASS (regenerated, 4 stitched panels)
- **Used In:** B1 (BUILD)
- 4-panel stitched strip. P1: Boy in yellow shirt with white robot (blue eyes) on table, holding tablet. P2: Girl with brown hair and pink headband holding white device/camera with screen. P3: Boy in white/yellow outfit with red gloves interacting with tech device. P4: Person with dark hair and goggles on head, green vest over orange shirt, outdoor background with mountains. Each panel individually generated then stitched. Content shows Blip greeting each kid differently.

### B1-S09 | Strips/strip_zara_decodes.png | Ch15 | PASS (regenerated, 5 stitched panels)
- **Used In:** B1 (BUILD)
- 5-panel stitched strip. P1: Girl in blue shirt at desk with computer screen showing colorful abstract drawings, art supplies. P2: Girl in green shirt drawing in sketchbook with pencil at desk. P3: Girl in light blue shirt painting with brush at table with paint palettes, room with window. P4: Close-up of hand drawing black abstract geometric shapes on paper with pen. P5: Stylized girl head/shoulders portrait, brown hair with bangs, white collared shirt, smiling. Each panel individually generated then stitched. Content shows artistic decoding/visual puzzle sequence.

### B1-S10 | Strips/strip_building_key.png | Ch16 | PASS
- **Used In:** B1 (BUILD)
- 5-panel strip showing electronics/DIY build sequence. P1: Hand in light blue cuff holding metallic silver tweezers. P2: Black wire spool fed through metallic clamp, red and green wires. P3: Close-up of device with red top/black body, gold USB connector, red and green wires. P4: Hand with soldering iron creating bright yellow/orange spark, black 9V battery connected via red/black wires. P5: Hand with soldering iron touching silver spoon, blue gradient background. Clean outlines, cel-shaded, warm yellow-brown then cool blue palette. Matches building-key/invention theme.

### B1-S11 | Strips/strip_normal_kids.png | Ch19 | PASS
- **Used In:** B1 (BUILD)
- 4-panel strip of kids with technology at home. P1: Two boys on orange-brown sofa, older boy holding game controller, younger boy watching. P2: Girl with ponytail in white shirt/headphones and boy in red/blue shirt on sofa looking at blue/white box on table, smaller boy peeking over sofa back. P3: Boy at desk looking at computer monitor showing family photo, surprised expression. P4: Two girls at desk looking at laptop, one in red shirt smiling, one in orange shirt focused, window with blue sky. Warm cel-shaded style, bold outlines, earthy palette.

### B1-S12 | Strips/strip_park_meeting.png | Ch22 | PASS
- **Used In:** B1 (BUILD)
- 4-panel strip set in park. P1: Boy in blue shirt/brown shorts sitting on wooden bench reading large unfolded map. P2: Girl in purple shirt/green pants sitting on stone bench. P3: Girl in orange shirt/blue shorts standing, handing box to white/silver robot with blue visor and red button. P4: Girl in pink shirt/blue pants and boy in green shirt/blue pants sitting on bench sharing snacks. Clean bold outlines, bright saturated cel-shaded colors, warm greens/yellows/oranges.

### B1-S13 | Strips/strip_four_glitches.png | Ch24 | PASS (regenerated, 4 stitched panels)
- **Used In:** B1 (BUILD)
- 4-panel stitched strip. P1: Urban street intersection with yellow taxis, traffic lights, buildings, daytime. P2: Library/bookstore interior with bookshelves, neon/holographic architectural projections on walls and ceiling, blue tone. P3: Art gallery interior with colorful abstract art on walls, furniture, natural light. P4: Outdoor pond with water fountains, ripples, grass, trees, rocks. Each panel individually generated then stitched. Content shows four distinct glitch locations (traffic, library, AR art, park flooding).

### B1-S14 | Strips/strip_sam_climbs.png | Ch25 | PASS (regenerated, 5 stitched panels)
- **Used In:** B1 (BUILD)
- 5-panel stitched strip. P1: Boy with red gloves running on street at night toward traffic light. P2: Boy with red gloves climbing traffic light pole against blue sky. P3: Boy reaching up to interact with traffic light fixture. P4: Boy shining flashlight/light beam, wearing blue shirt and red gloves. P5: Boy on traffic light pole against blue sky, triumphant. Each panel individually generated then stitched. Content clearly shows climbing/parkour sequence with traffic light pole.

### B1-S15 | Strips/strip_library_saves.py | Ch26 | PASS
- **Used In:** B1 (BUILD)
- 5-panel strip. P1: Boy in blue shirt standing looking at large futuristic screen with complex blue 3D model, glowing blue table projecting model. P2: Same boy at desk typing on laptop with 3D model on screen, bookshelf behind. P3: Boy at larger desktop monitor showing 3D map/diagram, hands on keyboard. P4: Boy looking at monitor showing humanoid figure with overlaid graph. P5: Woman in white shirt giving double thumbs-up, bookshelf behind. Clean outlines, cel-shaded, warm browns with cool blue screen highlights.

### B1-S16 | Strips/strip_maya_builds_valve.png | Ch28 | PASS
- **Used In:** B1 (BUILD)
- 5-panel strip. P1: Boy in light blue shirt crouched on grass holding red hose, forest setting with pink/red flowers. P2: Girl in light green shirt using wrench on red object connected to hose, same forest. P3: Red device with green/red pump and bicycle wheel spraying water, forest floor pooling water. P4: Close-up of water pump device indoors/shed, water flowing into metal barrel. P5: Girl in orange shirt kneeling on wet floor washing hands under water stream, wooden structure interior. Illustrative with clear outlines, natural/earthy palette. Matches building/water-device theme.

### B1-S17 | Strips/strip_gridlord_truth.png | Ch29 | PASS (regenerated, 4 stitched panels)
- **Used In:** B1 (BUILD)
- 4-panel stitched strip. P1: Dark grid/network interface with hundreds of red dots and small technical displays. P2: Four cartoon boys with concerned/surprised expressions looking at large screen showing numerous red circles. P3: Small boxy robot with blue eyes in dark environment with blue electrical energy/lightning effects. P4: Close-up of white cube robot with blue face showing sad/distressed expression with tears. Each panel individually generated then stitched. Content matches Gridlord truth revelation (red dots scale, robot recognizing patterns, sad Blip).

### B1-S18 | Strips/strip_blip_upgrade.png | Ch30 | PASS (regenerated, 6 stitched panels)
- **Used In:** B1 (BUILD)
- 6-panel stitched strip showing clear robot transformation sequence. P1: Server rack with cables, small white cube connected by blue cable. P2: White cube with colorful screen and rainbow glow, activating. P3: White cube with powerful blue energy burst, power-up. P4: Larger rectangular device with black screen and metallic frame, transformation. P5: Dark panel with single small blue light, scary blank moment. P6: Cheerful white cube robot with large eyes, smile, wheels, and label, final form. Each panel individually generated then stitched. Clear upgrade/transformation narrative.

### B1-S19 | Strips/strip_hq_makeover.png | Ch32 | PASS (regenerated, 5 stitched panels)
- **Used In:** B1 (BUILD)
- 5-panel stitched strip. P1: Person with dark hair in green shirt working at workbench with pegboard tools, workshop. P2: Person in blue beanie at desk with multiple computer monitors showing code/technical data. P3: Two people on rooftop looking at city skyline with skyscrapers, one with dreadlocks and denim jacket. P4: Person with dark hair running through tunnel/hallway carrying white refrigerator. P5: Interior room with warm string lights, small device/robot on round table, cozy lived-in space. Each panel individually generated then stitched. Content matches HQ makeover sequence (pegboard, monitors, mural on wall, fridge, string lights + robot dock).

### B1-S20 | Strips/strip_nexcorp_clues.png | Ch33 | PASS
- **Used In:** B1 (BUILD)
- 4-panel strip. P1: Hand holding pen over newspaper titled "NexCorp" with photo of two women, light desk surface. P2: Crown made of reddish-brown bricks/tiles embedded in cracked wall, warm yellow light behind. P3: Computer monitor displaying green grid with "KDA" text, keyboard/mouse on desk, office environment. P4: Humanoid robot with silver/white body and glowing orange eyes sitting at desk, office/lab with window. Strong outlines, cel-shaded, warm and cool tones. Matches NexCorp investigation theme.

### B1-S21 | Strips/strip_rooftop_friends.png | Ch34 | PASS
- **Used In:** B1 (BUILD)
- 4-panel strip. P1: Girl with brown hair in light blue shirt sitting on stone ledge eating snack, warm sunset sky. P2: Boy in green shirt at wooden table with silver laptop, girl leaning over his shoulder, sunset through window. P3: Boy in blue shirt painting on large paper at table, cityscape through window. P4: Boy in gray shirt hanging from horizontal metal bar on rooftop/balcony, city buildings, warm sunset sky. Clean outlines, vibrant cel-shaded palette, warm sunset tones throughout.

### B1-S22 | Strips/strip_neonville_lights.png | Ch36 | PASS
- **Used In:** B1 (BUILD)
- Single panel (not multi-panel strip). Nighttime city street scene from elevated perspective. Multi-story buildings with gabled roofs on both sides, autumn trees (yellow/orange leaves), warm yellow streetlights, red car taillights. Distant skyscraper skyline with illuminated windows, building with "PRYME" sign, another with red circular logo. Deep navy blue sky with white stars. Bold black outlines, flat cel-shaded colors. Atmospheric cityscape.

### B1-S23 | Strips/strip_maya_finds_crate.png | Ch3 | PASS
- **Used In:** B1 (BUILD)
- 5-panel strip. P1: Girl with brown ponytail in blue shirt leaning over open wooden chest emitting bright glowing light, indoor room with bookshelves. P2: Same girl in orange shirt sitting inside chest looking shocked, chest has blue label with white text. P3: Girl in orange shirt standing outside chest holding metal tongs, looking at white fluffy contents, blurred green/blue background. P4: Girl leaning over chest overflowing with white fluffy material, outdoor setting with blue sky. P5: Girl in maroon/purple shirt kneeling holding large white cube, broken chest with scattered white material around. Distinct line art, flat cel-shaded colors, vibrant palette.

### B1-S24 | Strips/strip_blip_wakes_up.png | Ch5 | PASS
- **Used In:** B1 (BUILD)
- 5-panel strip. P1: Single small yellow square on light beige surface, black background. P2: White round-headed robot with small antenna, large round yellow eyes, sad/concerned expression, sitting at table in dim blue room. P3: Brown round-headed android figure with antenna, happy expression, gray/black outfit, sitting at table, warm window light, potted plant. P4: Same white robot from P2 now with happy smiling expression, dim blue room, book on table. P5: Large glowing round smiling sun-like orb with rounded protrusions on sides, warm yellow/orange gradient background. Cel-shaded, flat colors, warm palette. Wake-up/awakening progression visible.

### B1-S25 | Strips/strip_gridlord_speaks.png | Ch13 | PASS (regenerated, 4 stitched panels)
- **Used In:** B1 (BUILD)
- 4-panel stitched strip. P1: Pixelated/low-res image of person in dark suit, digital glitchy appearance with color distortion. P2: Stylized text in bold graffiti font (purple and green with black outline) on black background. P3: Robot/cyborg on old TV screen with static/noise effects, metallic appearance with glowing eye elements. P4: Animated robot/cyborg character with blue coloring, humanoid face with expressive concerned eyes, warm color gradient background. Each panel individually generated then stitched. Content matches Gridlord communication attempt (static forming, broken text, face dissolving, reforming).

### B1-S26 | Strips/strip_puzzle_montage.png | Ch18 | PASS
- **Used In:** B1 (BUILD)
- 4-panel strip. P1: Girl with ponytail in blue shirt typing on keyboard, large dark blue monitor with complex white diagram/code. P2: Same girl typing on silver laptop, warm yellowish room, wall lamp, framed picture. P3: Boy in beige shirt pressing buttons on large silver machine with screen, shelves with boxes and blue pencil cup. P4: Three boys (blue hoodie, blue shirt, brown shirt) around large gray machine, one pressing buttons, one looking at small device, one observing. Clean outlines, warm browns/yellows then cooler blues, painterly cel-shaded style. Matches puzzle/investigation montage theme.

### B1-S27 | Strips/strip_emotional_blip.png | Ch30 | PASS (regenerated, 5 stitched panels)
- **Used In:** B1 (BUILD)
- 5-panel stitched strip showing cube robot emotional journey. P1: White cube with red angry eyes and frown, server room cables in background (scared/angry when connected). P2: White cube like retro CRT TV showing rainbow colors, colorful glowing aura (screen flickering). P3: Dark square metallic object with black screen (blank/scary moment). P4: Dark rectangular box with black screen and single blue light, three colored buttons below (hope returning). P5: White cube character with happy face, large black eyes, smile, text "VGM10", black round feet (happy version 1.0). Each panel individually generated then stitched. Clear emotional progression.

### B1-S28 | Strips/strip_team_skyline.png | Ch36 | PASS
- **Used In:** B1 (BUILD)
- Single panel (not multi-panel strip). 8 children in line on rooftop/observation deck at dusk. City skyline with illuminated buildings behind, orange-to-purple sky gradient. Characters from left: (1) Boy in blue cap with goggles, grey denim jacket, jeans with patches. (2) Boy in dark blue beanie with yellow "V", grey hoodie, holding smartphone. (3) Boy in brown beanie, red shirt, holding tablet. (4) Girl with ponytail, brown vest, holding glowing blue device, smiling. (5) Black silhouette child. (6) Girl with ponytail, brown vest over red shirt, goggles on head, phone to ear. (7) Boy in black shirt, smiling. (8) Girl with dark curly hair, brown vest, red boxing gloves, right fist raised. Bright vertical light beam behind silhouette. Bold outlines, cel-shaded, vibrant palette. Rooftop team scene.

---

## Extra Spots (25 items) - All MCP-verified

### ES-01 | Spots/daadi_calling.png | Ch1 | PASS
- **Used In:** B1 (BUILD)
- Elderly Indian grandmother in colorful saree leaning through doorway with spatula, warm kitchen with steam behind her, maternal expression. Warm golden tones.

### ES-02 | Spots/nexcorp_crate_label.png | Ch3 | PASS
- **Used In:** B1 (BUILD)
- Close-up of faded grey plastic crate label reading NEXCORP in stamped blue letters, dust and scratches on surface, ominous detail. Muted industrial palette.

### ES-03 | Spots/blip_first_light.png | Ch5 | PASS
- **Used In:** B1 (BUILD)
- Close-up of small white cube robot screen showing single tiny blue pixel of light in darkness, dust particles floating, magical moment. Dark background, single blue glow point.

### ES-04 | Spots/maya_robot_pajamas.png | Ch5 | PASS
- **Used In:** B1 (BUILD)
- Close-up of cute pajamas with little robot print pattern, girl lying in bed hugging pillow, cozy bedtime scene, warm bedroom light. Soft pastel palette.

### ES-05 | Spots/leo_pixel_heart_patch.png | Ch7 | PASS
- **Used In:** B1 (BUILD)
- Close-up of navy blue beanie with small pixel heart patch sewn on side, beanie slightly too big, warm detail shot. Dark navy fabric, small colorful patch.

### ES-06 | Spots/zara_yellow_bag.png | Ch8 | PASS
- **Used In:** B1 (BUILD)
- Bright yellow crossbody bag with colorful enamel pins and patches, camera strap visible beside it, artistic messy pin arrangement. Vibrant yellow dominant.

### ES-07 | Spots/sam_led_sneakers.png | Ch9 | PASS
- **Used In:** B1 (BUILD)
- Reddish-brown kids sneakers with LED lights in soles flashing red and blue, mid-run motion blur, dynamic action detail. Dark background, red/blue sole lights.

### ES-08 | Spots/blip_scanning.png | Ch11 | PASS
- **Used In:** B1 (BUILD)
- Boxy white robot with blue scanning beam projecting from screen showing grid pattern, beam hitting a clock/gadget on desk, tech detective scene. Blue beam, warm desk lighting.

### ES-09 | Spots/connector_key_closeup.png | Ch17 | PASS
- **Used In:** B1 (BUILD)
- Close-up of strange homemade connector device made from bent wire, spoon handles, and magnet — spoon-sculpture radial mechanical object, warm golden workshop lighting. Warm amber tones.

### ES-10 | Spots/blip_charging_dock.png | Ch20 | PASS
- **Used In:** B1 (BUILD)
- Boxy white robot standing on makeshift charging dock (phone charger + duct tape), blue screen face with red smile, battery filling up icon visible. Cozy home setting.

### ES-11 | Spots/daadi_smile.png | Ch21 | PASS
- **Used In:** B1 (BUILD)
- Elderly Indian grandmother + granddaughter baking together, lavender blouse/cream apron, hands dusted with flour, warm knowing smile, warm golden kitchen. Rich warm palette.

### ES-12 | Spots/crown_graffiti.png | Ch23 | PASS
- **Used In:** B1 (BUILD)
- Spray-painted pixelated crown symbol on dark brick wall, pink-purple/blue-cyan dripping paint, urban art style, mysterious tag. Dramatic spotlight illumination on graffiti.

### ES-13 | Spots/nexcorp_tower.png | Ch24 | PASS
- **Used In:** B1 (BUILD)
- Nighttime urban scene centered on tall modern glass skyscraper. "NEXCOR" name illuminated in cyan-blue sans-serif capital letters at top. Glass facade reflecting city lights, warm yellow/orange interior illumination on lower floors, vibrant purple light from middle floors. Dense cityscape of mid-rise buildings, streets with cars, green trees. Sky transitions from dark blue/black to deep orange at horizon. Digital illustration style with smooth gradients, realistic light reflections — not cel-shaded. Elevated aerial perspective. Bustling modern metropolis atmosphere.

### ES-14 | Spots/blip_cable_plug.png | Ch19 | PASS
- **Used In:** B1 (BUILD)
- Cheerful anthropomorphic white box-shaped robot with rounded top, two short cylindrical antennae, large rectangular screen face with two bright blue circular pixelated eyes and curved red smiling mouth. Black jointed articulated arms and legs, single black rounded foot. Robot plugging black cable into white rectangular device port — blue/white electrical sparks at connection point. Warm brown wooden table surface. Blurred bookshelf background. Warm soft ambient lighting with cool blue glow from eyes and sparks. 3D stylized cartoonish aesthetic, smooth glossy surfaces, no hard outlines. Playful friendly mood.

### ES-15 | Spots/zara_painting_glitch.png | Ch27 | PASS (seed 1107293671, regenerated)
- **Used In:** B1 (BUILD)
- Canvas painting on wooden easel showing vibrant city skyline with glitch-art pixel overlays in bright neon green and purple/pink colors. Pixel fragments scattered throughout creating digital corruption effect. City extends to horizon with water visible. Warm sunset/sunrise tones. Indoor gallery/exhibition space with warm wall sconce lights on left, white pedestal/table on right with decorative object. Neutral light walls, polished floor. Canvas has visible thick edge with paint texture. Glitch-art effect blends traditional painting with digital aesthetics.

### ES-16 | Spots/water_spray_park.png | Ch28 | PASS (seed 1364668657, regenerated)
- **Used In:** B1 (BUILD)
- Park garden with multiple sprinkler heads on metal poles gushing water dramatically in chaotic spray patterns. Multiple forceful water arcs shooting high into air. Faint rainbow/visible spectrum within mist from larger water arcs. Bright golden sunlight from upper left creating prominent lens flares. Wet reflective ground with puddles. Lush green trees as dense backdrop. Wooden park benches along water feature edge. Green well-maintained grass. Warm golden-hour lighting (early morning or late afternoon). Dynamic yet refreshing atmosphere.

### ES-17 | Spots/sam_gaming_trophy.png | Ch25 | PASS
- **Used In:** B1 (BUILD)
- Cozy creative workspace centered on large ornate golden trophy reading "CHAMPION OF THE SUMMER OLYMPICS" on its base. Wooden desk with colorful books, magazines, snack package with "FROOT" text, blue pen, pencil holder, yellow bear figurine, loose papers. Warm desk lamp on right creating golden illumination. Three large colorful posters on wall: "ADVENTURE", "CHAMPION TONIC", and third partially obscured. Illustrative painterly style with soft visible outlines. Warm celebratory creative mood.

### ES-18 | Spots/librarian_amazed.png | Ch26 | PASS
- **Used In:** B1 (BUILD)
- Young woman with brown hair in ponytail, black-rimmed glasses, surprised expression with mouth open, wearing green long-sleeved sweater over white collared shirt. Seated at wooden desk using black keyboard, left hand resting on white computer monitor. Monitor displays dark screen with green text/code lines. Tall wooden bookshelves filled with colorful books (red, blue, orange, green spines) in background. White pencil holder with pencils. Warm diffused lighting, yellowish hue. Clean cel-shaded digital style with distinct dark outlines and flat color blocks. Atmosphere of discovery/surprise.

### ES-19 | Spots/hq_string_lights.png | Ch32 | PASS
- **Used In:** B1 (BUILD)
- Rustic well-stocked pantry/storage room with three wooden shelves filled with glass jars (grains, powders, liquids in brown/yellow/white), wooden/cardboard boxes, kitchen utensils. String of warm glowing light bulbs hanging from ceiling in curved line. Metal utensils (forks, spoons, ladles) hanging on wall between shelving units. Lemon on middle shelf, sunglasses on bottom shelf, small blue/green bowls. Light tan wood, muted off-white walls. Strong dark outlines, flat color with subtle shading — cel-shaded style. Warm cozy inviting atmosphere.

### ES-20 | Spots/blip_hologram_project.png | Ch33 | PASS
- **Used In:** B1 (BUILD)
- Cheerful white cubic robot with two short white spherical-tipped antennae, blue pixelated screen face with two large round blue eyes and red smiling mouth, black articulated arms/legs with white gloves and black rounded shoes. Semi-transparent glowing blue holographic display floating above head showing technical schematics (circular diagrams, lines, small text labels). Child's playroom background: green shelf with yellow duck/pink pig toys, yellow table with books, orange storage bin, framed landscape picture on wall, light wood floor, patterned rug. Soft diffused warm lighting with cool blue glow from hologram. 3D cartoon style, cel-shaded with clean outlines. Friendly curious atmosphere.

### ES-21 | Spots/investigation_photos.png | Ch34 | PASS
- **Used In:** B1 (BUILD)
- Five printed photographs arranged on light brown wooden table. Photos show: (1) close-up of futuristic mechanical eye with glowing circular pupil and colorful blurred lights, (2) golden crown on green foliage with sunlit sky, (3) portrait of two smiling girls (one brown hair/blue shirt, one dark hair/glasses), (4) another futuristic eye close-up from different angle, (5) outdoor city street with arched stone structure. White box with "NEXO" in red/blue text in top-right corner. Blue cylindrical object (tape dispenser) and white pen with blue cap. Bright natural lighting, warm wood tones. Photorealistic photos on stylized 3D-rendered table. Cheerful creative detective atmosphere.

### ES-22 | Spots/sunset_fire_escape.png | Ch35 | PASS
- **Used In:** B1 (BUILD)
- Serene urban sunset viewed from fire escape balcony. Metal fire escape railing with vertical/horizontal bars in foreground, wooden plank balcony floor. Railing positioned diagonally creating leading line. Warm golden/orange/pink sunset sky with soft wispy clouds, cooler blue/gray distant buildings. Long subtle shadows from railing onto floor. Clean precise lines, smooth color gradients — digital illustration style, no hard outlines, painterly approach. No text. Dense city skyline with varied buildings. Calm peaceful contemplative mood.

### ES-23 | Spots/maya_goggles_determination.png | Ch36 | PASS
- **Used In:** B1 (BUILD)
- Close-up portrait of person's face from nose up, wearing large round eyeglasses with metallic silver/gray frames. Lenses reflect detailed city skyline at dusk — warm orange/yellow sunset sky, buildings including domed structure and skyscrapers, city lights as bright points. Dark brown hair with lighter brown highlights framing face. Amber/golden colored eyes visible through lenses. Soft directional lighting from front/above. Digital painterly style, smooth gradients, semi-realistic with clean defined lines. No text. Quiet contemplation/wonder mood, intimate close-up.

### ES-24 | Spots/team_silhouette_rooftop.png | Ch36 | PASS
- **Used In:** B1 (BUILD)
- Four children and a hovering robot as solid black silhouettes against vibrant sunset sky. Two children on left concrete platform (one spiky hair/jacket, one short hair/t-shirt), two on right platform (short hair/t-shirt, hooded jacket). Robot hovering between platforms — rectangular head, two small antennae, two glowing green circular eyes, boxy body, round wheels/treads for legs, one arm extended. Sky gradient: deep purple at top, orange in middle, bright yellow at horizon. Large stylized clouds tinted orange/yellow. Dark distant city skyline. Strong backlight from setting sun between platforms. Flat graphic style, no internal shading. Warm tranquil yet mysterious atmosphere.

### ES-25 | Spots/blip_wave_hello.png | Ch0 (front matter) | PASS
- **Used In:** B1 (BUILD)
- Cheerful white cubic robot with rectangular head, two short white spherical-tipped antennae, blue pixelated screen face with two large round blue eyes (black pupils, white highlights) and wide red smiling mouth. Black articulated arms/legs, white gloves, black rounded shoes. Right hand raised in waving gesture, robot in mid-jump/lively step. Child's playroom: shelf with red curtain/teddy bear, stacked colorful cylindrical toys, books and yellow duck toy on another shelf. Warm peach/orange walls, light floor. Colorful polka-dotted balls in foreground. Small white sparkle effects scattered throughout. Soft warm golden diffused lighting. Digital cartoon style with bold clean outlines, cel-shaded. Cheerful playful welcoming mood.

### ES-26 | Spots/spot_spring_bounce.png | Ch1 | PASS
- **Used In:** B1 (BUILD)
- **Generated:** 2026-06-02 via Bonsai (seed from spot_spring_bounce, 512x512).
- Central object: classic gooseneck desk lamp with white rectangular base, black coiled insulated neck severely twisted and strained with separated coils giving spring-like appearance, metallic silver conical shade with intensely glowing warm yellow bulb. Chaotic array of colorful wires (red, blue, green, yellow) tangled around base and neck, one wire visibly arcing/sparking with white lines and black dots indicating short circuit. Small clear bottle with white label and red cap taped to lamp base.
- Workbench: warm brown wood with visible grain and worn scratched texture. Scattered tools: blue-handle screwdriver with silver shaft, red-handle screwdriver, blue-handle pliers, green-handle utility knife, smaller screwdrivers and bits. Black boxy device resembling camera/electronic component on left. Green box (power supply) and white keyboard/control panel on right.
- Background workshop: left wall with white pegboard holding scissors, wrench, hammer, saw/chisel. Round black-and-white clock on wall. Hand-drawn diagram/notes pinned to pegboard. Framed picture/poster on back wall. Window with white frame on right showing blue sky. Wooden shelf with blue cup of pens/pencils, green bottle. Purple box and pen container under window.
- Lighting: primary warm yellow from lamp bulb creating strong local illumination with dimmer shadowed background. Strong chiaroscuro effect. Warm browns and yellows dominated, colorful wire accents. Digital cartoon/comic book style with bold outlines, detailed linework, slightly textured vintage print quality. Chaotic late-night creativity mood.

### ES-27 | Spots/spot_crate_stairs.png | Ch3 | PASS
- **Used In:** B1 (BUILD)
- **Generated:** 2026-06-02 via Bonsai (seed from spot_crate_stairs, 512x512).
- Central character: young girl with shoulder-length brown hair in simple ponytail, light natural peach skin, large expressive brown eyes conveying focus and mild apprehension. Plain white short-sleeve t-shirt, dark blue denim jeans slightly faded at knees, gray athletic sneakers with black laces and white soles. Mid-stride ascending stairs, left foot higher, right lower. Both hands gripping large dark gray matte rectangular plastic crate with grid-like vertical slats — left hand on top edge, right supporting from side. Body leaned forward showing effort, expression concentrated with mild concern.
- Setting: dark brown wooden staircase with visible grain and texture. Enclosed by wooden banisters on both sides — left polished smooth, right darker rustic oak/walnut. Muted dark gray/taupe walls. Two large stylized bright yellow sunflowers with dark brown centers and rich green leaves on right wall, one above the other, painted or affixed. At top of stairs: doorway into warmly lit yellow room with framed picture on far wall.
- Lighting: single warm amber light source from left casting long rightward shadows. Stark contrast between darker foreground staircase and bright warm room above. Light illuminates girl's face and left staircase side while right side with sunflowers in relative shadow. Cinematic quality with dramatic chiaroscuro. Digital illustration with painterly quality, clean smooth lines, slight texture mimicking traditional media. Muted desaturated palette except bright sunflowers and warm light. Quiet intensity and mild suspense mood.

### ES-28 | Spots/spot_samosa_plate.png | Ch10 | PASS
- **Used In:** B1 (BUILD)
- **Generated:** 2026-06-02 via Bonsai (seed from spot_samosa_plate, 512x512).
- Foreground: white round plate with thin black outline holding six golden-yellow triangular samosas in slightly overlapping cluster, some pointing upward others angled. Slightly textured crispy appearance with subtle brown speckles indicating perfect frying. Thin white steam lines curling upward from center suggesting heat and freshness. Plate sits on warm medium-brown wooden table with visible grain texture and slight sheen, casting subtle shadow beneath.
- Midground kitchen counter: light brown wooden surface extending across background. Glass jars with metal lids: deep red chunky preserve/chutney (far left), small white ceramic jar with pale yellow powder/salt/sugar, tall slender jar with orange liquid/oil, large jar with red chunky substance, jar with bright orange powdery spice/turmeric, very large jar with light beige powder/flour. Small loose items between jars: reddish-brown crumbly herbs, yellow irregular ginger piece, small yellow rectangular block. Wooden spoons and spatula in container far left behind jars.
- Background: large rectangular brownish-tan wall tiles in brick-like pattern with slightly darker brown grout lines. Slightly rough matte texture.
- Art style: flat cartoon/vector art with strong clean black outlines defining all shapes. Solid highly saturated colors without complex shading. Warm overhead diffused lighting enhancing golden hues. Color palette: warm browns, yellows, reds throughout. Cheerful appetizing cozy mood. No text, no characters.

### ES-29 | Spots/spot_basement_door.png | Ch2 | PASS
- **Used In:** B1 (BUILD)
- **Generated:** 2026-06-02 via Bonsai (seed from spot_basement_door, 512x512).
- Central subject: single weathered wooden door constructed from vertical planks, faded aged brown with once-light green/off-white paint heavily weathered and peeling revealing grayish-brown wood beneath. Deep cracks running through wood and paint. Visible drips of dried dark liquid running down planks. Prominent old-fashioned tarnished brass/bronze doorknob and lock mechanism on left side, ornate circular design with central emblem, heavy rust around base and keyhole. Small round peephole above doorknob. Door slightly ajar. Centered in frame occupying majority of vertical space.
- Walls: large irregularly shaped stone/crumbling plaster, deep blue-gray and black, blending into shadows. Severe decay with jagged cracks spiderwebbing across surface, significant portions fallen away revealing rough uneven interior structure. Gritty ancient pitted texture. Right wall partially illuminated showing depth of cracks.
- Floor: concrete/stone tiles in gray and blue tones, cracked and uneven with small pebbles, dust, debris scattered. Bright patch of light illuminating dust motes and small stones.
- Lighting: single intense light source off-camera right, casting sharp focused beam illuminating right side of door, adjacent wall, and floor patch. Dramatic chiaroscuro effect — left side plunged into deep inky blackness. Stark division drawing eye directly to door. Limited desaturated palette: cool blues, grays, browns.
- Art style: digital illustration with strong graphic quality, bold dark outlines, sophisticated shading creating depth and texture. Dark painterly comic book/concept art style. Quiet dread, mystery, abandonment, suspense mood. No text, no characters.

### ES-30 | Spots/spot_backpack_crumbled.png | Ch1 | PASS
- **Used In:** B1 (BUILD)
- **Generated:** 2026-06-02 via Bonsai (seed from spot_backpack_crumbled, 512x512).
- Central subject: large vibrant slightly faded orange-red backpack with darker maroon accents along seams, zippers, straps. Boxy shape with rounded main compartment and large rectangular front pocket. Top slightly indented giving soft rounded appearance. Thick padded shoulder straps, one looping over top and down right side. Significant wear: numerous dark brown/black speckle scuffs, larger irregular brownish stains on front pocket. Black zipper running vertically down front pocket, main compartment zipper partially open with top flap askew. Two cylindrical objects protruding from top: shorter wider black cylinder (flashlight/scope) and taller thinner silver antenna/rod with pointed tip. Thin black wire dangling from left side.
- Scattered electronics on white ground: left — grey rectangular device (external hard drive/power supply), smaller grey rectangular memory card/battery, thin black cable partially coiled. Right — larger grey device with blue-lit screen/display (portable media player/diagnostic tool), another small grey rectangular component, tiny green rectangular microchip/connector. Small screws and debris.
- Background: solid clean stark white, high-contrast backdrop making colorful backpack and grey electronics stand out sharply.
- Art style: flat vector-based comic book style with very clean bold black outlines. Primarily flat coloring with subtle internal shading suggesting volume. Single consistent upper-left light source with soft grey shadows beneath objects. Centrally positioned balanced composition. Technical disarray / DIY maker mood. No text, no characters.

### ES-31 | Spots/spot_professor_waddles.png | Ch1 | PASS
- **Used In:** B1 (BUILD)
- **Generated:** 2026-06-02 via Bonsai (seed from spot_professor_waddles, 512x512).
- Central character: cartoon penguin sitting upright on desk facing forward. Round plump body: black back/wings/head, bright clean white belly, vibrant warm orange triangular beak and feet. Large expressive white eyes with small black circular pupils, wide open conveying focus or mild frustration. Slightly pink cheeks. Subtly furrowed eyebrows enhancing determined/annoyed expression. Flippers resting on belly, legs tucked underneath.
- Desk: warm brown wooden surface with visible grain, scratches and marks from frequent use. Matte slightly textured painted/stained wood. Numerous silver/gray metal screws scattered across surface in varying sizes and orientations. Black and green wires tangled and strewn, some coiled loosely others stretched with frayed ends. Small crumpled white paper left of penguin. Small indistinct plastic/metal debris bits.
- Background: top-right — dark gray/black metal adjustable desk lamp angled down toward penguin, emitting warm yellowish light creating distinct spotlight effect with soft shadows. Top-right behind lamp — stack of white papers/documents with thicker brown books/binders underneath, slightly askew. Top-left — cylindrical brown wooden pencil holder containing colored pencils (blue, green, red) standing upright. Left of holder — small rectangular grayish-green cardboard/plastic box. Top-left behind holder — white-framed multi-pane window showing dark nighttime exterior, no discernible details. Wall: warm beige/light tan with slightly textured finish.
- Lighting: primary warm yellow desk lamp spotlight on penguin creating strong focal point. Softer diffused ambient light from above. Robot... penguin as clear center of attention framed by lamp top-right and pencil holder/box top-left. Warm earthy color palette: browns, beiges, black/white penguin with orange beak/feet accents and colored pencil pops.
- Art style: clean modern cartoon with bold black outlines, solid flat colors with subtle soft gradient shading for depth. Digital illustration, friendly approachable yet detailed lived-in workshop feel. Cozy warm intimate mood mixed with mild chaos of creative work. No text.

---

## Maps (2 items) - All MCP-verified

### MAP-01 | Maps/map_neonville.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Isometric illustrated map of neighborhood. Mix of residential houses, apartment building, glass skyscraper, shops, curving streets with cars, green parks with benches. OpenCV labels: "NEONVILLE" (title), "MAPLE STREET", "MAIN STATION", "VALLEY STREET", "COMMUNITY CENTER", "PARK". Compass rose in corner. Cartoonish whimsical style, warm earthy palette.

### MAP-02 | Maps/map_underground.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Vertical cross-section. Top: 4-story pink/salmon apartment building. OpenCV label: "WAGLE STREET" (building sign). Bottom: underground tunnel network in brown rocky earth, silver pipes. OpenCV labels: "SECRET LAB" (room with equipment), "SERVER ROOM" (dark server racks), "TUNNEL EXIT" (dark opening), "PIPES" (pipe area). Dim lighting from rooms. Comic book style. Mystery mood.

---

## Gadget Blueprints (4 items) - All MCP-verified

### GB-01 | Blueprints/bp_connector_key.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Blueprint on aged cream paper with circuit-board border. Central coat-hanger-and-spoon device in metallic bronze. OpenCV labels: "COAT HANGER" (top loop), "ANTENNA" (wire), "SPEAKER" (cylinder), "COILED WIRE" (coiled section), "MAGNET" (coiled section), "ANTENNA" (bottom protrusion), "SPOON BASE" (bottom). Patent-drawing style.

### GB-02 | Blueprints/bp_pressure_valve.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Steampunk diagram on yellowed parchment. Copper cylindrical chamber + secondary chamber + corrugated hose + spoked wheels + blue liquid flow arrows. OpenCV labels: "FUSION CHAMBER", "EXPANSION", "WHEEL", "CHAMBER", "FLEXIBLE HOSE", "PRESSURE", "RELEASE VALVE". Vintage engineering sketch style.

### GB-03 | Blueprints/bp_blip_internals.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Blueprint on aged paper. White boxy robot with blue eyes, red smile, 3 antennae, black limbs, walking pose + inset circuit board diagram. OpenCV labels: "LED FACE", "ANTENNA x3", "SCREEN", "CORE CHIP", "SIGNAL PROCESSOR", "MOTOR", "BATTERY". Cartoonish friendly style. Canonical Blip form present.

### GB-04 | Blueprints/bp_bypass_device.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Blueprint of compact device with red button on top and circular lens on front, metallic brass body, isometric 3D view. OpenCV labels: "BYPASS SWITCH", "RED BUTTON", "LENS", "SERIAL PORT", "BATTERY PACK", "CIRCUIT", "SCAVENGED PARTS". Sketchy cross-hatching style on cream paper.

---

## Title Page (1 item) - MCP-verified

### TP-01 | title_page.png | PASS (regenerated v2 with OpenCV text overlay)
- **Used In:** B1 (BUILD)
- **Regenerated:** 2026-06-02. Bonsai-generated dark cityscape background (1024x1024, seed from TITLE_v3) with OpenCV text overlay via overlay_text.py.
- **Background:** Nighttime urban street scene, perspective view down central road lined with autumn-orange deciduous trees. Multi-story buildings in warm brown/orange tones on both sides, numerous lit yellow windows. Tall modern skyscrapers in background, tallest centered with bright cyan light running up spire and blue-glowing windows. Deep navy sky with stars, thin crescent moon upper right. Three large jagged lightning bolts in vibrant purple and cyan crackling across sky toward city. Single prominent street lamp on right casting warm yellow pool of light on sidewalk. Street surface dark gray reflecting ambient light.
- **Text overlay (OpenCV):** "THE GLITCH SQUAD" top center in golden-yellow bold rounded font (72pt), multi-layer glow in blue (alpha 0.4), Gaussian shadow blur 10, black stroke width 3. "BOOK ONE" below in light blue (30pt), blue glow alpha 0.3. "THE LOST SIGNAL" bottom center in cyan (48pt), cyan glow alpha 0.5, shadow blur 8, dark stroke. "Some signals are meant to be found." tagline in white (22pt), subtle purple glow.
- **Dark gradient overlays:** Top 350px and bottom 200px darkened for text readability.
- **Art style:** Cel-shaded 2D digital illustration, bold clean outlines, warm golden lighting at street level, cool electric purple/cyan in sky. Vibrant candy-color palette. No characters visible — focus on setting and mood. Cinematic dramatic atmosphere suggesting urban tech mystery.

---

## Section Dividers (5 items) - All MCP-verified

### SD-01 | Dividers/divider_act1_discovery.png | PASS (regenerated v2 with OpenCV text overlay)
- **Used In:** B1 (BUILD)
- **Regenerated:** 2026-06-02. Bonsai-generated robot workshop scene (1024x1024, seed from PART1_v3) with OpenCV text overlay via overlay_text.py.
- **Central character:** Small white boxy robot (Blip) with rectangular CRT-monitor head, two short white rounded antennae. Black screen face displaying two large bright blue circular LED eyes with pixel-dot pattern, small blue symbol between eyes, dark red curved smile. White rounded rectangular body with small square chest panel. Short white rounded arms, left hand slightly raised emitting soft blue glow. Cute approachable retro-futuristic design.
- **Setting:** Wooden workbench with warm brown tone, visible grain, worn surface. Workshop background: pegboard wall on left with wrenches, shelves above workbench, adjustable desk lamp on right casting warm yellowish light. Tools on bench: orange-handled screwdriver, silver wrench, black USB cable, coiled red/black cable, small screwdriver. Right side: technical drawings/blueprints, brown pencil, pen, stack of books/notebooks. Container with colored pencils.
- **Lighting:** Primary warm yellow desk lamp creating cozy focused spotlight. Secondary diffused overhead light. Robot's eyes and hand emit cool blue glow contrasting warm lamp. Distinct soft shadows under robot.
- **Text overlay (OpenCV):** "PART ONE" top center in golden-yellow bold rounded font (65pt), orange glow alpha 0.4, shadow blur 10, dark brown stroke width 3. "DISCOVERY" bottom center in electric blue (55pt), blue glow alpha 0.4, shadow blur 8, dark blue stroke. Thin decorative golden divider line at vertical midpoint.
- **Warm vignette** applied around edges. Art style: clean digital cartoon, cel-shaded, bold outlines, warm earthy palette with blue/cyan accents. Inviting creative atmosphere.

### SD-02 | Dividers/divider_act2_chaos.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Curved magenta banner with lightning bolts and blue pixel fragments. "PART TWO" / "THE GLITCH WAVE" overlaid in bold yellow (OpenCV). Left icon: yellow lightning bolt. Right icon: black traffic light. Warm golden-yellow gradient background. Futuristic high-tech style.

### SD-03 | Dividers/divider_act3_gridlord.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Dark purple-to-blue gradient background. "PART THREE" / "THE GRIDLORD" overlaid in bold cyan (OpenCV). Left icon: pixelated golden crown. Right icon: retro CRT monitor with green grid, keyboard, mouse. Floating pixelated cubes in blue/purple. Binary code border. 8-bit pixel art style.

### SD-04 | Dividers/divider_act4_mission.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Horizontal banner with multicolored triangle border. "PART FOUR" / "MISSION NEONVILLE" overlaid in bold yellow (OpenCV). Left: gear icon + paintbrush. Right: game controller + paintbrush. Cream background. Flat cartoon style.

### SD-05 | Dividers/divider_act5_beginning.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Warm orange gradient background. "PART FIVE" / "THE BEGINNING" overlaid in bold golden-yellow (OpenCV). Left: stylized sun with rays + astronaut. Right: city skyline silhouette + heart icon + microphone. Golden border. Flat vector cartoon style.

---

## Glitch Art (6 items) - All MCP-verified

### GA-01 | GlitchArt/glitch_gridlord_static.png | PASS
- **Used In:** B1 (BUILD)
- Central figure from chest up: person with short dark hair, green pixelated glitched skin with purple/black patches, horizontal scan lines, metallic circuit-like patchwork on right face side. Vibrant green intense eyes. Black t-shirt with green binary code cascading down front. Angular metallic crown-like headpiece with glowing orange spiky protrusions. Two background monitors: left shows green-tinted distorted person with crown, right shows purple-tinted person with glasses and crown. Orange spark effects around crown. Dark gray/black background. High-contrast polished digital painting with comic book aesthetic. Intense futuristic unsettling mood. Canonical Gridlord elements present (crown, green/purple, digital corruption, CRT monitors).

### GA-02 | GlitchArt/glitch_signal_corruption.png | PASS
- **Used In:** B1 (BUILD)
- Circular tunnel-like digital vortex/wormhole. Concentric rings of light creating depth perspective. Bright white/cyan beam radiating from center. Chaotic field of fragmented data and light trails (orange/yellow with red/white accents). Pixelated shapes and blocks scattered throughout. Green/red/yellow binary code and alphanumeric characters streaming across image. Deep black background. Intense warm palette (orange/yellow/red). Glitch art style with digital distortion effects. Energetic chaotic immersive mood.

### GA-03 | GlitchArt/glitch_crown_pattern.png | PASS
- **Used In:** B1 (BUILD)
- Large central pixelated crown constructed from mosaic of geometric blocks, traditional multi-pointed form. Central peak emits bright explosive light burst. Neon purple/pink/blue crown colors with yellow/orange light bursts. Cyan grid/wireframe overlay across entire image. Translucent layered crown sections. Background: deep black with numerous smaller faded pixelated crowns in muted purples/blues. No legible text. High-contrast bold glitch art. Futuristic majesty meets digital chaos mood.

### GA-04 | GlitchArt/glitch_city_fracture.png | PASS
- **Used In:** B1 (BUILD)
- Stylized city skyline at dusk (resembling NYC) with tall skyscrapers, two prominent spired buildings with cyan/teal illuminated outlines. Dark gradient sky (black to warm orange/yellow horizon). Large spiderweb crack/shatter pattern radiating from brilliant white/yellow central light source. Crack lines in neon red/yellow. Scattered digital glitches: flickering blocks (cyan/red/white), horizontal/vertical lines, pixelated distortions. Lens flare from central light. Cyberpunk glitch art style. Tense dystopian disruptive mood.

### GA-05 | GlitchArt/glitch_data_stream.png | PASS
- **Used In:** B1 (BUILD)
- Bright luminous vertical beam (white/cyan) from bottom center shooting upward. Chaotic explosion of colorful geometric fragments (squares, rectangles, shards) in purple/teal/pink/white. Green cascading "digital rain" code filling background. Deep black background. Dynamic explosive composition. Data fragmentation and digital disruption effects. Glitch art/cyberpunk style. Intense energy, chaos, technological disruption mood.

### GA-06 | GlitchArt/glitch_cipher_symbols.png | PASS
- **Used In:** B1 (BUILD)
- Collection of glowing wireframe geometric polyhedra on black background. Large light blue dodecahedron (center), large green dodecahedron (upper right), light blue cube (upper left), cyan cube disintegrating with particle effects (lower left), purple wireframe (lower center), golden-yellow star-like polyhedra (lower right, upper center). Thin colored light trails (orange/green/blue) connecting shapes. Digital noise, pixelation, illegible text snippets in green/yellow/purple. Futuristic abstract cyberpunk style. Mysterious chaotic digital-void mood.

---

## Documents (4 items) - All MCP-verified

### DOC-01 | Documents/doc_nexcorp_memo.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Faded yellowed document with brown stains and creases. OpenCV text: "NEXCORP RESEARCH" header, "PROJECT BLIP", "DATE: CLASSIFIED", "CONFIDENTIAL", "DO NOT DISTRIBUTE", red stamps "URGENT" and "APPROVED". Central white cube robot with blue eyes, pink blush, black limbs, standing in relaxed pose. Vintage document texture.

### DOC-02 | Documents/doc_gridlord_message.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Computer monitor on wooden desk in dim room. Dark screen with OpenCV text: "HELP ME." (purple), "TRUST THEM." (purple), "THE SIGNAL." (green). Glitch/distressed font style. Mystery, urgency mood.

### DOC-03 | Documents/doc_blip_diagnostic.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Retro diagnostic screen with white cube robot schematic in center, dark background, green grid. OpenCV text: "SIGNAL ORIGIN: UNKNOWN", "CORE STATUS: ACTIVE", "94% FUNCTIONAL", "0.7 BPS SIGNAL", "DIAGNOSTIC COMPLETE", "BLIP v1.0". Green-on-dark terminal aesthetic.

### DOC-04 | Documents/doc_project_kira.png | PASS (text overlay)
- **Used In:** B1 (BUILD)
- Computer screen showing classified document. OpenCV text: "https://project-kira.net" (address bar), "PROJECT KIRA" (title), "CLASSIFIED" (subtitle). Central photo of scientist in lab coat. Background lab scene with researchers, beakers. Warm sepia-toned cinematic lighting. Serious secretive mood.

---

## Endpapers (2 items) - All MCP-verified

### EP-01 | endpaper_front.png | PASS
- **Used In:** B1 (BUILD)
- Repeating pattern on light beige/cream background with faint golden-yellow circuit-board lines. Central focal point: large white boxy robot with glowing blue circular eyes, white highlights, rectangular mouth, pink cheeks, black limbs, two antennae. Smaller crowned robot head peeking behind. Scattered elements: numerous smaller white robots (varied eye colors: green, blue), orange/yellow gears (some with smiling faces), smartphones (blue screens), tablets, cameras, wrenches (red/silver), screwdrivers, paintbrushes (green/yellow), small colorful crowns (red/green/yellow). Seamless tileable pattern. Bold outlines, flat cartoon vector style. Cheerful imaginative tech-themed mood.

### EP-02 | endpaper_back.png | PASS
- **Used In:** B1 (BUILD)
- Single-scene illustration (not repeating tile). Central: cheerful boy with black hair, wide smile, black "1 PLAYER" t-shirt with pixelated blue "1", dark shorts with colorful side stripes, black/white sneakers, mismatched gloves (one red, one black/green). Surrounding: 4 robots of varying designs (blue screen face, small simple, white with black goggles, white with blue light), 2 potatoes (single large, pair of small), 2 cityscapes (brown skyline, city-in-cube), brown arched tunnel, light cube with doorway containing city, paintbrush (black handle/brown tip), red gloves mirroring boy's. Light creamy beige background. Clean modern digital illustration. Cheerful playful imaginative mood.

---

## Scene Spotlights (14 items) - MCP-verified 2026-06-05

> Replaced 28 comic strips with 14 scene spotlights (full-page illustrations + chapter quote overlay via HTML `img-overlay` + `quote-box`). All text-free images; quotes overlaid by build_book.py.

### SS-01 | Spotlights/spotlight_maya_desk.png | Ch 1 | PASS
- **Quote overlay:** "Every project was a tiny universe of possibility."
- Girl matches description well: 11yo Indian girl, warm brown skin, dark brown messy ponytail, safety goggles on forehead, olive green utility vest with pockets, faded red t-shirt with rocket ship design, cargo shorts, velcro sneakers, gap-toothed grin. **Minor:** no pencil in hair, both sneaker laces tied (not one untied). Cel-shaded 2D cartoon with bold outlines. Workshop setting with tools, papers, warm desk lamp. High quality.

### SS-02 | Spotlights/spotlight_crate_discovery.png | Ch 2 | PARTIAL
- **Quote overlay:** "Whatever you are, you're coming with me."
- **Issue:** Bonsai rendered the character as a BOY instead of girl (gender swap). Brown hair with pencil stuck in it, goggles on forehead, olive green vest, red rocket shirt, cargo pants, velcro sneakers. Otherwise matches outfit and setting perfectly. Dark basement/corridor setting with wooden crates, one marked "NEXCORP". Dramatic spotlight lighting. Cel-shaded 2D style. Quality good despite gender issue.

### SS-03 | Spotlights/spotlight_cube_awakens.png | Ch 3 | PASS
- **Quote overlay:** "The cube heard it. And began to boot."
- Dark bedroom at night. White cube on cluttered desk emitting soft cyan glow. Cube has black screen with 4 small white lights (not exactly blue eyes + red smile, but recognizable as Blip). Girl asleep in bed in background. Moonlight through window. Papers, wires on desk. Cel-shaded 2D style. Quiet magical mood. High quality.

### SS-04 | Spotlights/spotlight_blip_first_words.png | Ch 4 | PASS
- **Quote overlay:** "He was ALIVE. Really, truly, impossibly ALIVE."
- Girl: 11yo Indian, warm brown skin, messy ponytail, safety goggles on forehead, olive green utility vest, red rocket t-shirt, cargo shorts. Sitting on bed edge with amazed expression. Robot: small white cube hovering with blue eyes, red smile, cyan glowing aura. Bedroom at night with moon and stars visible through window. Cel-shaded 2D with bold outlines, vibrant colors. Warm whimsical emotional impact. No text in image. High quality.

### SS-05 | Spotlights/spotlight_glitch_wave.png | Ch 5 | PASS
- **Quote overlay:** "A pulse of CYAN light shot out of Blip like a ripple in water."
- White cube robot with blue eye and red smile hovering, emitting expanding cyan ring. City street at night with glitch effects: fire hydrant spraying cyan-tinted water, spinning drone in sky, flickering neon signs on buildings. Cyberpunk aesthetic. Cel-shaded 2D cartoon. **Note:** Neon signs have some text (BAROG, FAME, G1H, RHYTHM, HAUN, OAZRG) — these are AI-generated gibberish, not readable text. High quality dynamic composition.

### SS-06 | Spotlights/spotlight_gridlord_appears.png | Ch 7 | PASS
- **Quote overlay:** "Someone woke up the little cube. How... INTERESTING."
- 4 kids in dimly-lit high-tech room around large CRT monitor. Monitor displays pixelated face with glowing green eyes and jagged orange crown — Gridlord. Girl (Maya): ponytail, goggles on head, red rocket shirt, olive green vest, cargo shorts, red fingerless gloves. Boy (Sam): dark hair, "PUZZLE" t-shirt, red gloves, tablet. Boy (Leo): dark hair, blue beanie with red heart, glasses, grey hoodie, jeans, tablet, headphones. Girl (Zara): dark skin, curly pigtails with colorful braids, blue denim jacket, patterned leggings, yellow crossbody bag. **Note:** No Blip cube visible. Purple-hued lighting. Cel-shaded 2D. High quality atmospheric scene.

### SS-07 | Spotlights/spotlight_team_builds.png | Ch 8 | PASS
- **Quote overlay:** "Her goggles were foggy. Her fingers were scorched. Her grin was VICTORIOUS."
- 4 kids in workshop around workbench. Sam (left): black "PLAYER" t-shirt, red fingerless gaming gloves, shorts with stripes, LED sneakers, controller. Leo (second left): navy beanie, glasses, grey hoodie, jeans, tablet. Maya (second right): curly pigtails, goggles, olive green vest, writing on paper. Zara (right): denim jacket with patches, goggles on head, working with electronics. Small floating cube in upper right corner (Blip). Warm afternoon light. Cel-shaded 2D. High quality collaborative scene.

### SS-08 | Spotlights/spotlight_puzzle_celebration.png | Ch 9 | PASS
- **Quote overlay:** "Despite EVERYTHING - they all LAUGHED."
- 5 kids + Blip celebrating in workshop. Maya: ponytail, goggles on head, olive green vest, red shirt, pencil behind ear, standing and smiling. Sam: short black hair, "PUMA" t-shirt, red fingerless gloves, tablet, smiling. Leo: brown hair, navy beanie, grey hoodie, tablet. Zara: dark curly hair with red highlights, denim jacket with patches, patterned pants, camera, sitting on floor. Blip: white cube with blue eyes floating, cyan glow. Blueprints on wooden floor with tools. Warm interior lighting with nighttime visible through window. Cel-shaded 2D. High quality joyful scene.

### SS-09 | Spotlights/spotlight_daadi_parathas.png | Ch 11 | PASS
- **Quote overlay:** "Reckless love is still love, Maya-beta."
- 68yo Indian grandmother: silver hair in neat bun, warm kind face, rectangular glasses, soft lavender salwar kameez, thin gold chain necklace. Standing at stainless steel stove flipping golden parathas, steam rising. Young girl (Maya) sitting at table in red t-shirt, green overalls, goggles on head, eating flatbread. Warm kitchen with wooden cabinets, glass spice jars, window with patterned curtains. Cel-shaded 2D. High quality heartwarming domestic scene.

### SS-10 | Spotlights/spotlight_sam_traffic.png | Ch 13 | PASS
- **Quote overlay:** "Like a platformer, except the consequences were REAL."
- 10yo Japanese-Korean boy: short spiky black hair shaved on sides, missing front tooth, bright red fingerless gaming gloves, black "PLAYER" t-shirt, black athletic shorts with white stripes, high-top sneakers with glowing blue LED soles. Standing confidently in middle of city street surrounded by stopped cars and taxi. Traffic light above. Buildings with Japanese signage. Warm golden lighting. Cel-shaded 2D cartoon. High quality dynamic scene.

### SS-11 | Spotlights/spotlight_blip_mainframe.png | Ch 14 | PASS
- **Quote overlay:** "Version 2.0. And still himself. Still Blip."
- 4 kids in massive digital mainframe space. White cube robot with blue eye and red smile held by character on left, emitting cyan glow. Background filled with cyan and purple data streams, binary code, terminals. Boy with "PLAYFIIT" t-shirt. Digital environment with cool blue-purple lighting. Cel-shaded 2D. High quality futuristic atmosphere.

### SS-12 | Spotlights/spotlight_rooftop_sunset.png | Ch 17 | PASS
- **Quote overlay:** "The sky is NEVER the same color twice."
- 5 kids + Blip on rooftop at sunset. Maya (far left): ponytail, goggles on head, olive green vest, red shirt, red fingerless gloves, backpack, kneeling and smiling. Sam: spiky black hair, "RATEL GAMES" t-shirt, red fingerless gloves, sitting cross-legged. Leo: blue beanie, glasses, grey hoodie, standing behind. Second boy in blue denim jacket with tablet. Zara (far right): dark curly hair, denim jacket, pink shirt, patterned pants, yellow crossbody bag, tablet. Blip floating upper right with blue eyes. City skyline silhouette. Beautiful orange-pink-purple sunset gradient. Cel-shaded 2D. High quality warm emotional scene.

### SS-13 | Spotlights/spotlight_gridlord_truth.png | Ch 18 | PASS
- **Quote overlay:** "The Gridlord wasn't the villain. They were the ALARM."
- 3 kids in underground lab looking at large CRT monitor. Monitor shows pixelated face with glowing green eyes and jagged metallic crown — expression is neutral/contemplative, NOT villainous. Maya (left): ponytail, goggles on head, red rocket shirt, olive green vest, cargo shorts, green-lit face, determined expression. Leo (center): blue beanie, glasses, grey jacket, "MAKE" t-shirt, smiling, gesturing. Zara (right): dark curly hair, denim jacket with patches, patterned pants (ducks), tablet, slight smile. Green code on screen. Cel-shaded 2D. High quality revelation scene.

### SS-14 | Spotlights/spotlight_maya_final_stand.png | Ch 19 | PASS
- **Quote overlay:** "Glitch Squad - we have a rescue mission."
- Maya (left): 11yo Indian, ponytail, goggles on forehead, olive green utility vest, faded red rocket t-shirt, cargo shorts, red gloves, typing on keyboard with determined expression. Sam: "PLAYER 1" t-shirt, red gloves, cheerful. Leo: blue beanie, glasses, grey hoodie, arm around Sam. Zara: dark skin, curly hair, denim jacket, patterned leggings, yellow bag, camera, smiling. Blip: small white cube with smile near Leo. High-tech workshop with glowing screens. Cel-shaded 2D with dramatic lighting. Heroic adventurous tone. High quality.

---

## Locations (5 items) - MCP-verified 2026-06-05

> Full-bleed atmospheric establishing shots. No text overlay — just the image. All prompts specified "no people" but Bonsai added a person in LOC-02.

### LOC-01 | Locations/location_maple_street.png | Ch 1 | PASS
- Wide establishing shot of cozy neighborhood street. Brownstone/townhouse buildings with fire escapes, brick facades. Warm golden evening light with pink-blue sky gradient. Mature trees with lush foliage lining sidewalks. Parked cars along street (sedan, SUV). Street lamp. **No people.** No readable text. Cel-shaded 2D cartoon with clean outlines. Excellent quality. Inviting multicultural neighborhood feel.

### LOC-02 | Locations/location_maya_room.png | Ch 1 | PARTIAL
- Interior of young inventor's bedroom workshop. Cluttered wooden desk with circuit boards, tools (screwdriver, pliers), coiled wires, laptop with schematic, containers with pens/tools. Two adjustable desk lamps casting warm light. Blueprints/schematics on wall. Shelf with vintage radio, goggles hanging from hooks, gauges. Wooden floor. **Issue:** A girl is visible sitting at the desk working on computer, despite "no people" in prompt. Cel-shaded 2D. High quality cozy creative atmosphere.

### LOC-03 | Locations/location_nexcorp_basement.png | Ch 9 | PASS
- Abandoned underground laboratory. Dusty wooden workbenches with old electronic equipment (oscilloscopes, signal generators, vintage instruments). Grey metal storage crates with yellowed labels. Thick cobwebs hanging from ceiling and corners. Single bare lightbulb hanging by wire, casting warm yellowish glow with strong shadows. Concrete walls with exposed pipes. Debris on floor. **No people.** Mysterious eerie forgotten atmosphere. Cel-shaded 2D with excellent texturing of dust and decay. High quality.

### LOC-04 | Locations/location_utility_tunnels.png | Ch 12 | PASS
- Underground utility tunnel network. Long straight concrete corridor with dense pipes running along ceiling and walls. Electrical junction boxes mounted on walls at intervals. Wires and cables connecting boxes to pipe network. Dim warm yellowish lighting from wall-mounted round fixtures. Steam/smoke rising from ceiling near center. Vanishing point at far end with faint green exit sign. **No people. No text.** Cel-shaded 2D with bold black outlines. Mysterious maze-like feeling. High quality atmospheric scene.

### LOC-05 | Locations/location_hq_lab.png | Ch 17 | PASS
- Transformed underground lab as team headquarters. Wooden desk with two computer monitors displaying code/data. String lights hanging from ceiling creating warm ambient glow. White mini-fridge on right. Wall covered with colorful children's drawings in white frames. Shelves with tools, stuffed toy, jars, utensils. Office chair (empty). Cables under desk. Cracked ceiling suggesting basement. **No people.** Some text on drawings ("Happy Birthday" visible but stylized). Cel-shaded 2D. Warm lived-in creative space. High quality.

---

## Diagrams (5 items) - MCP-verified 2026-06-05

> Educational infographic pages rendered with `blueprint-page` CSS class. All prompts specified "no text" because Bonsai cannot render readable text. Text will be overlaid via HTML.

### DIA-01 | Diagrams/diagram_signal_path.png | Ch 5 | PASS
- Educational signal path diagram. Central white cube (Blip) with red indicator light and blue port. Radiating colored arrows (red, green, orange, yellow, blue, purple, cyan, pink) connecting to peripheral devices: monitor, vintage computer terminal, mobile phone, traffic light, wheeled cart, sensor unit, printer/scanner. Off-white background with subtle grid pattern (blueprint-style). Cel-shaded 2D cartoon. **AI-generated text labels present but garbled/unreadable** ("Siignal t fnirt", "Sjaalor tparacio bariarnt", etc.) — expected, text will be overlaid. Good educational clarity via visual elements alone.

### DIA-02 | Diagrams/diagram_gridlord_network.png | Ch 7 | PASS
- Network visualization infographic. Isometric city block at night with buildings in muted earth tones, yellow-lit windows. Electronic devices on buildings: CRT monitors, laptop, smartphone, server tower, printer, keyboard. Central large glowing sphere with digital face (Gridlord). Bright neon lines (green, purple, pink, blue, orange, cyan) radiating from face to each device. Solid black background making neon connections pop. Cel-shaded 2D. **No readable text.** Highly effective educational visualization of network concept.

### DIA-03 | Diagrams/diagram_anatomy_glitch.png | Ch 10 | PASS
- Step-by-step glitch anatomy diagram. 2x2 grid of rounded rectangular panels with orange-brown borders. Each panel has numbered orange circle in top-left corner. Shows POS/cash register terminal in 4 stages: (1) normal static state, (2) malfunctioning with flames and receipt ejecting, (3) exploded with burst of light and debris, (4) damaged with wrench inserted and sparks. Simple pale yellow/blue backgrounds per panel. Cel-shaded 2D. **"Stage"/"Staign" text labels present but garbled** — expected. Clear visual storytelling of glitch progression.

### DIA-04 | Diagrams/diagram_connector_key.png | Ch 8 | PASS
- Exploded view technical blueprint. Central green circuit board with ICs, resistors, capacitors, knob. Yellowish-green rectangular casing below (battery pack). Black rectangular component and glowing wire/cable separated above in exploded view. Dotted leader lines extending from components toward periphery. Light blue background with white grid pattern (blueprint-style). Isometric perspective. Cel-shaded 2D cartoon. **No clearly readable text** (small text on labels too stylized). Effective educational exploded view showing internal structure.

### DIA-05 | Diagrams/diagram_project_kira.png | Ch 16 | PASS
- Timeline infographic. 9 circular illustrations in 3x3 grid on light beige background, connected by dashed colored lines (orange, green, red). Each circle contains an illustrated scene: lab with beakers, robot on sandy surface, child at desk, humanoid robot connected to box, central monitor displaying abstract shape, child with screwdriver at workbench, girl with tool smiling, portrait of smiling girl, two boys looking at book together. Central monitor acts as hub node. Cel-shaded 2D cartoon. **No readable text.** Effective visual storytelling of story chronology.

"""
Generate 24 replacement images for comic strips.
14 Scene Spotlights + 5 Location Establishers + 5 Diagrams.

Usage:
    python generate_replacements.py                    # dry-run, show prompts
    python generate_replacements.py --generate         # generate all via Bonsai
    python generate_replacements.py --generate --only SS-01 SS-02  # specific images
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys, time
from pathlib import Path
import numpy as np
import cv2

try:
    import requests
except ImportError:
    requests = None

SERVER = "http://192.168.29.7:8765"
OUT_DIR = Path(__file__).resolve().parent / "Images"

MAYA = ("11-year-old Indian girl, warm brown skin, dark brown messy ponytail with escaped strands "
        "and a pencil stuck in it, safety goggles on forehead, olive green utility vest with many "
        "pockets full of wires and tools, faded red rocket ship t-shirt, cargo shorts, velcro sneakers "
        "with one untied lace, gap-toothed grin, curious determined expression")

LEO = ("11-year-old Mexican-American boy, warm tan skin, navy blue knit beanie with small pixelated "
       "heart patch, rectangular black-rimmed reading glasses on chain around neck, oversized gray "
       "zip-up hoodie with sleeves over hands, dark t-shirt, distressed jeans, sturdy sneakers, "
       "focused serious expression, holding tablet")

ZARA = ("12-year-old Nigerian-British girl, rich dark brown skin, voluminous black hair twists with "
        "colorful threads woven in, high cheekbones, bright yellow crossbody bag covered in enamel "
        "pins, oversized blue denim jacket with colorful patches, colorful patterned leggings, gold "
        "hoop earrings, vintage SLR camera with yellow strap, warm confident smile")

SAM = ("10-year-old Japanese-Korean boy, light warm skin, short spiky black hair shaved on sides, "
       "mischievous grin with missing front tooth, bright red crimson fingerless gaming gloves, "
       "black PLAYER 1 t-shirt, athletic shorts with side stripes, high-top sneakers with LED soles, "
       "gaming headset around neck, energetic athletic pose")

BLIP = ("small cute white boxy cube robot with rounded edges, square screen face, two large bright "
        "blue circular LED eyes, dark red curved smile mouth, two thin white stick antennas on top, "
        "two short white arms with black elbow joints, hovering with soft cyan glow underneath")

BLIP_SHORT = "small white cube robot with blue eyes and red smile hovering with cyan glow"

DAADI = ("68-year-old Indian grandmother, silver hair in soft neat bun, warm kind face, soft lavender "
         "cotton salwar kameez, thin gold chain necklace, reading glasses on beaded chain, warm smile")

GRIDLORD = ("vintage CRT monitor displaying stern angular pixelated face with glowing green eyes, "
            "jagged metallic crown in forehead, green-purple digital noise skin, sharp angular features, "
            "cascading green code text and purple static, glowing orange neon crown icon above")

STYLE = "children's book illustration, cel-shaded 2D, bold outlines, bright colors, warm golden lighting"

IMAGES = [
    # ── SCENE SPOTLIGHTS (14) ──────────────────────────────────────
    {
        "id": "SS-01", "type": "spotlight", "chapter": 1, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_maya_desk.png",
        "quote": "Every project was a tiny universe of possibility.",
        "prompt": (
            f"{MAYA}, sitting at her cluttered wooden workbench in a cozy bedroom workshop, "
            "surrounded by circuit boards, tools, wires, and blueprints, warm golden desk lamp "
            "lighting, notebooks scattered everywhere, she is tinkering with a small gadget with "
            "a screwdriver, proud grin on her face, cozy creative inventor den, afternoon light "
            "through window, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "SS-02", "type": "spotlight", "chapter": 2, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_crate_discovery.png",
        "quote": "Whatever you are, you're coming with me.",
        "prompt": (
            f"{MAYA}, crouching in a dusty basement before a mysterious sealed wooden crate with "
            "faded NexCorp logo, single beam of flashlight illuminating the crate, cobwebs on "
            "concrete walls, exposed pipes overhead, her eyes wide with curiosity and wonder, "
            "one hand reaching toward the crate, dim mysterious atmosphere, no text no letters "
            "no words, " + STYLE
        ),
    },
    {
        "id": "SS-03", "type": "spotlight", "chapter": 3, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_cube_awakens.png",
        "quote": "The cube heard it. And began to boot.",
        "prompt": (
            "dark bedroom at night, one small white cube robot sitting alone on cluttered desk "
            "among wires and notebooks, beginning to emit soft cyan blue glow, moonlight through "
            "window, a girl asleep in bed in background with closed eyes, the cube screen showing "
            "two blinking dots appearing, quiet magical moment, no text no letters no words, "
            + STYLE
        ),
    },
    {
        "id": "SS-04", "type": "spotlight", "chapter": 4, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_blip_first_words.png",
        "quote": "He was ALIVE. Really, truly, impossibly ALIVE.",
        "prompt": (
            f"{MAYA}, sitting up in bed with shocked amazed expression, face to face with "
            f"{BLIP_SHORT}, the robot hovering at eye level with big happy smile and bright "
            "blue eyes, soft cyan glow illuminating both their faces, dark bedroom, moonlight "
            "through window, a stuffed penguin fallen off the bed, wonder and surprise moment, "
            "no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "SS-05", "type": "spotlight", "chapter": 5, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_glitch_wave.png",
        "quote": "A pulse of CYAN light shot out of Blip like a ripple in water.",
        "prompt": (
            f"{BLIP_SHORT} at center emitting expanding ring of cyan light like a shockwave, "
            "a city street at night, glitch effects everywhere, a fire hydrant spraying water, "
            "a delivery drone spinning in sky, neon signs flickering with magenta and turquoise "
            "colors, cars stopped at crazy angles, no people visible, dramatic cinematic scene, "
            "no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "SS-06", "type": "spotlight", "chapter": 7, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_gridlord_appears.png",
        "quote": "Someone woke up the little cube. How... INTERESTING.",
        "prompt": (
            f"{MAYA} and {SAM} and {LEO} and {ZARA}, four pre-teen kids standing in a dark "
            "server room, their faces lit by purple and green light from a large computer monitor "
            f"on the wall, {GRIDLORD}, the kids look up at the screen with mix of awe and fear, "
            "dramatic lighting, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "SS-07", "type": "spotlight", "chapter": 8, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_team_builds.png",
        "quote": "Her goggles were foggy. Her fingers were scorched. Her grin was VICTORIOUS.",
        "prompt": (
            f"{SAM} holding wires, {LEO} typing on tablet, {ZARA} drawing blueprint, {MAYA} "
            "soldering at a workbench with goggles down, all four pre-teen kids working together "
            f"at Maya's cluttered desk, {BLIP_SHORT} hovering nearby watching, teamwork scene, "
            "warm afternoon light, parts and tools spread on table, collaborative energy, "
            "no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "SS-08", "type": "spotlight", "chapter": 9, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_puzzle_celebration.png",
        "quote": "Despite EVERYTHING - they all LAUGHED.",
        "prompt": (
            f"{MAYA} and {SAM} and {LEO} and {ZARA}, four exhausted but grinning pre-teen kids "
            f"sitting on floor at 3AM surrounded by blueprints and parts, {BLIP_SHORT} doing a "
            "happy spin with sparkles, everyone celebrating, warm lamp light, messy room, "
            "triumphant joy, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "SS-09", "type": "spotlight", "chapter": 11, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_daadi_parathas.png",
        "quote": "Reckless love is still love, Maya-beta.",
        "prompt": (
            f"{DAADI} standing in her warm cozy kitchen flipping golden parathas on a stove, "
            f"steam rising, colorful spice jars on counter, lace curtains with morning sunlight, "
            f"{MAYA} sitting at kitchen table packing parathas in a cloth bundle, warm family "
            "kitchen scene, love and warmth, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "SS-10", "type": "spotlight", "chapter": 13, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_sam_traffic.png",
        "quote": "Like a platformer, except the consequences were REAL.",
        "prompt": (
            f"{SAM} standing determined at a city street corner, a traffic light above him "
            "glitching between red and green with sparks, confused cars in background, his "
            "red gaming gloves clenched, athletic stance ready to act, dramatic urban scene "
            "with glitch effects on the traffic light, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "SS-11", "type": "spotlight", "chapter": 14, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_blip_mainframe.png",
        "quote": "Version 2.0. And still himself. Still Blip.",
        "prompt": (
            f"{BLIP} floating into a massive digital space filled with swirling data streams "
            "in cyan and purple, abstract digital landscape with floating code fragments, "
            f"{MAYA} and {SAM} and {LEO} and {ZARA} watching from behind a glowing terminal, "
            "dramatic digital world scene, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "SS-12", "type": "spotlight", "chapter": 17, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_rooftop_sunset.png",
        "quote": "The sky is NEVER the same color twice.",
        "prompt": (
            f"{MAYA} and {SAM} and {LEO} and {ZARA}, four pre-teen kids sitting on a rooftop "
            f"at sunset, city skyline in background with warm golden and orange sky, {BLIP_SHORT} "
            "hovering among them, everyone relaxed and happy, fire escape railing, peaceful "
            "golden hour moment, warm colors, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "SS-13", "type": "spotlight", "chapter": 18, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_gridlord_truth.png",
        "quote": "The Gridlord wasn't the villain. They were the ALARM.",
        "prompt": (
            f"large computer screen showing {GRIDLORD}, but the face is sad and lonely not angry, "
            f"{MAYA} standing before the screen with hand reaching out compassionately, "
            f"{SAM} and {LEO} and {ZARA} behind her also showing empathy, dim server room, "
            "emotional revelation scene, soft purple and green glow, no text no letters no words, "
            + STYLE
        ),
    },
    {
        "id": "SS-14", "type": "spotlight", "chapter": 19, "size": 1024,
        "dir": "Spotlights",
        "file": "spotlight_maya_final_stand.png",
        "quote": "Glitch Squad - we have a rescue mission.",
        "prompt": (
            f"{MAYA} standing before a large glowing terminal with goggles pulled down over eyes, "
            "fingers hovering over keyboard, determined fierce expression, "
            f"{SAM} and {LEO} and {ZARA} standing behind her ready for action, "
            f"{BLIP_SHORT} glowing brightly beside her, dramatic lighting from the terminal, "
            "heroic final stand moment, no text no letters no words, " + STYLE
        ),
    },
    # ── LOCATION ESTABLISHERS (5) ──────────────────────────────────
    {
        "id": "LOC-01", "type": "location", "chapter": 1, "size": 1024,
        "dir": "Locations",
        "file": "location_maple_street.png",
        "prompt": (
            "wide establishing shot of a cozy city neighborhood street called Maple Street, "
            "brownstone apartment buildings with fire escapes, warm evening light, a small park "
            "visible, trees lining the sidewalk, a few parked cars, inviting multicultural "
            "neighborhood, no people, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "LOC-02", "type": "location", "chapter": 1, "size": 1024,
        "dir": "Locations",
        "file": "location_maya_room.png",
        "prompt": (
            "interior of a young inventor girl's bedroom workshop, cluttered wooden desk covered "
            "in circuit boards and tools and wires, blueprints pinned to wall, warm desk lamp, "
            "shelf with gadgets, goggles hanging on a hook, cozy creative space with afternoon "
            "light through window, no people, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "LOC-03", "type": "location", "chapter": 9, "size": 1024,
        "dir": "Locations",
        "file": "location_nexcorp_basement.png",
        "prompt": (
            "abandoned underground laboratory, dusty workbenches with old electronic equipment, "
            "grey crates with faded labels, cobwebs hanging from ceiling, single bare lightbulb, "
            "concrete walls with exposed pipes, mysterious forgotten space, dim atmospheric "
            "lighting, no people, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "LOC-04", "type": "location", "chapter": 12, "size": 1024,
        "dir": "Locations",
        "file": "location_utility_tunnels.png",
        "prompt": (
            "underground utility tunnel network, concrete corridor with exposed pipes and junction "
            "boxes, dim industrial lighting, steam vents, cables running along ceiling, map-like "
            "perspective showing tunnel branching ahead, mysterious underground maze, no people, "
            "no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "LOC-05", "type": "location", "chapter": 17, "size": 1024,
        "dir": "Locations",
        "file": "location_hq_lab.png",
        "prompt": (
            "transformed underground lab becoming a team headquarters, three computer monitors "
            "on a desk displaying data, string lights hanging from ceiling, a mini-fridge, "
            "colorful drawings pinned to wall, tools organized on shelves, cozy lived-in space "
            "with personality of four kids, warm lighting, no people, no text no letters no words, "
            + STYLE
        ),
    },
    # ── DIAGRAMS / INFOGRAPHICS (5) ────────────────────────────────
    {
        "id": "DIA-01", "type": "diagram", "chapter": 5, "size": 1024,
        "dir": "Diagrams",
        "file": "diagram_signal_path.png",
        "prompt": (
            "educational infographic diagram showing how a signal travels from a small white cube "
            "robot at center to connected household devices around it like doorbells and traffic "
            "lights and phones, labeled arrows showing signal path, clean technical diagram style, "
            "blueprint-style background with grid lines, bright colors, educational children book "
            "style diagram, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "DIA-02", "type": "diagram", "chapter": 7, "size": 1024,
        "dir": "Diagrams",
        "file": "diagram_gridlord_network.png",
        "prompt": (
            "infographic map showing a city block with all connected devices highlighted in "
            "neon colors, smartphones and doorbells and traffic lights and computers all connected "
            "by glowing lines to a central digital face, network visualization diagram, dark "
            "background with neon green and purple connections, children book educational style, "
            "no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "DIA-03", "type": "diagram", "chapter": 10, "size": 1024,
        "dir": "Diagrams",
        "file": "diagram_anatomy_glitch.png",
        "prompt": (
            "educational step-by-step diagram showing 4 stages of a glitch: stage 1 a normal "
            "device, stage 2 the device receiving a signal with wavy lines, stage 3 the device "
            "malfunctioning with sparks, stage 4 the device being fixed with a wrench, numbered "
            "stages shown left to right in boxes, clean infographic style, bright colors, "
            "children book educational diagram, no text no letters no words, " + STYLE
        ),
    },
    {
        "id": "DIA-04", "type": "diagram", "chapter": 8, "size": 1024,
        "dir": "Diagrams",
        "file": "diagram_connector_key.png",
        "prompt": (
            "exploded view technical blueprint of a gadget called the connector key, showing "
            "a coat hanger antenna at top, circuit board in middle, battery pack at bottom, "
            "with dotted leader lines pointing to each part, blueprint-style blue grid background, "
            "clean technical drawing style, educational diagram for children, no text no letters "
            "no words, " + STYLE
        ),
    },
    {
        "id": "DIA-05", "type": "diagram", "chapter": 16, "size": 1024,
        "dir": "Diagrams",
        "file": "diagram_project_kira.png",
        "prompt": (
            "timeline infographic showing a story chronology with 5 milestones connected by a "
            "horizontal line: beginning with a lab, then a robot being built, then the lab closing, "
            "then a digital face appearing, then four kids discovering it, each milestone shown "
            "as a small illustration in a circle connected by a dotted line, educational children "
            "book timeline diagram, no text no letters no words, " + STYLE
        ),
    },
]


def seed_for(img_id: str) -> int:
    return int(hashlib.md5(f"{img_id}_notext_v2".encode()).hexdigest()[:8], 16) % 2147483647


def gen_img(prompt: str, seed: int, size: int = 512):
    if requests is None:
        print("  ERROR: requests library not installed")
        return None
    r = requests.post(f"{SERVER}/generate", json={
        "prompt": prompt,
        "negative_prompt": "",
        "width": size,
        "height": size,
        "seed": seed,
        "guidance_scale": 3.5,
        "num_inference_steps": 28,
    }, timeout=180)
    if r.status_code == 200:
        arr = np.frombuffer(r.content, dtype=np.uint8)
        return cv2.imdecode(arr, cv2.IMREAD_COLOR)
    print(f"  ERROR: server returned {r.status_code}: {r.text[:200]}")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--generate", action="store_true", help="Actually generate images")
    ap.add_argument("--only", nargs="*", help="Only generate these IDs")
    args = ap.parse_args()

    images = IMAGES
    if args.only:
        images = [im for im in images if im["id"] in args.only]
        if not images:
            print(f"No images matched: {args.only}")
            return

    print(f"{'GENERATING' if args.generate else 'DRY-RUN'}: {len(images)} images\n")

    for im in images:
        seed = seed_for(im["id"])
        out_dir = OUT_DIR / im["dir"]
        out_path = out_dir / im["file"]

        print(f"{'='*60}")
        print(f"ID:    {im['id']}")
        print(f"Type:  {im['type']} | Ch: {im['chapter']} | Size: {im['size']}")
        print(f"File:  {out_path}")
        print(f"Seed:  {seed}")
        print(f"Quote: {im.get('quote', '(none)')}")
        print(f"Prompt ({len(im['prompt'])} chars):")
        prompt_display = im['prompt']
        if len(prompt_display) > 300:
            prompt_display = prompt_display[:300] + "..."
        print(f"  {prompt_display}")
        print()

        if args.generate:
            out_dir.mkdir(parents=True, exist_ok=True)
            if out_path.exists():
                print(f"  SKIP: {out_path.name} already exists")
                continue
            img = gen_img(im["prompt"], seed, size=im["size"])
            if img is not None:
                cv2.imwrite(str(out_path), img)
                print(f"  SAVED: {out_path} ({os.path.getsize(out_path)//1024} KB)")
            else:
                print(f"  FAILED: {im['id']}")
            time.sleep(1)

    if not args.generate:
        print("Run with --generate to actually generate images")


if __name__ == "__main__":
    main()

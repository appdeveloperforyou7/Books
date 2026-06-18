"""
Manifest Batch Client v4 - Character-Consistent Image Generation with img2img.

Strategy for character consistency with Bonsai:
  1. Each character has a REFERENCE IMAGE (best portrait from Characters/ folder)
  2. When a character appears, their reference image is sent as init_image (img2img)
  3. image_strength controls how much Bonsai follows the reference (0.3-0.5 recommended)
  4. Each character has a DETAILED description injected into every prompt
  5. Fixed seed per character for additional consistency
  6. Falls back to txt2img when server doesn't support img2img

Usage:
    python manifest_batch_client.py --server 192.168.29.7
    python manifest_batch_client.py --server 192.168.29.7 --dry-run --show-prompt
    python manifest_batch_client.py --server 192.168.29.7 --strength 0.4
    python manifest_batch_client.py --server 192.168.29.7 --no-img2img
    python manifest_batch_client.py --server 192.168.29.7 --type strip,marginalia
    python manifest_batch_client.py --server 192.168.29.7 --only B1-006 B1-007
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import secrets
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SCRIPT_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = SCRIPT_DIR / "Book1" / "manifest_clean.json"
OUTPUT_DIR = SCRIPT_DIR / "Images"

# ── STYLE ──────────────────────────────────────────────────────────────
STYLE_PREFIX = (
    "Clean polished digital illustration for a premium children's chapter book, "
    "vibrant warm rich colors, soft cinematic golden lighting, "
    "perfectly smooth clear skin on every character in the scene, "
    "clear expressive faces, round friendly childlike proportions, "
    "large expressive eyes, bright candy-color palette, "
    "professional storybook quality art, "
    "clean smooth rendering without grain"
)

STYLE_SUFFIX = (
    "premium children's book illustration quality, clean smooth polished digital art, "
    "warm golden lighting, perfectly smooth clear skin, "
    "vibrant colors, professional storybook art, "
    "clean sharp rendering"
)

SCENE_STYLE = (
    "Clean polished digital illustration for a premium children's chapter book, "
    "vibrant warm rich colors, soft cinematic golden lighting, "
    "professional storybook quality art rendered in a clean style, "
    "sharp focus on the scene, every object clearly visible"
)

SCENE_SUFFIX = (
    "premium children's book scene illustration, "
    "warm golden lighting, vibrant colors, "
    "clean sharp rendering, professional storybook art"
)

# ── CHARACTER DESCRIPTIONS (injected into every prompt featuring them) ──
CHARACTER_DESCRIPTIONS = {
    "maya": (
        "an 11-year-old Indian girl named Maya with warm brown skin, dark brown thick "
        "messy ponytail with escaped strands and a pencil stuck in it, safety goggles "
        "pushed up on forehead, oversized olive green utility vest with many pockets "
        "full of wires and tools, faded red rocket ship t-shirt underneath, cargo shorts, "
        "velcro sneakers with one untied lace, modified digital watch with tiny antenna "
        "on left wrist, gap-toothed grin, lean wiry build, "
        "curious determined expression with wide dark brown eyes, "
        "no gloves on her hands, bare hands only"
    ),
    "leo": (
        "an 11-year-old Mexican-American boy named Leo with warm tan golden-brown skin, "
        "compact stocky build with broad shoulders for a kid, black thick slightly "
        "grown-out fade haircut under a navy blue beanie with a small pixelated heart "
        "patch, very dark intense eyes with thick eyebrows, "
        "focused expression, oversized gray hoodie with sleeves pulled over hands and "
        "tablet in front pocket, dark t-shirt underneath, jeans with grass-stained knees, "
        "sturdy double-knotted sneakers, reading glasses on a chain around neck, "
        "no gloves on his hands, bare hands only"
    ),
    "zara": (
        "a 12-year-old Nigerian-British girl named Zara with rich dark brown skin, "
        "tall long-limbed graceful build, voluminous black natural hair in chunky twists "
        "with colorful thread woven in, bright expressive dark brown eyes, high "
        "cheekbones, wide smile with gap in front teeth, small 3D-printed stud earrings, "
        "bright yellow crossbody bag covered in enamel pins, oversized denim jacket with "
        "patches and doodles on sleeves, graphic art tee underneath, colorful patterned "
        "leggings, bright galaxy-painted sneakers, beaded bracelets on both wrists, "
        "stylus behind ear, no gloves on her hands, bare hands only"
    ),
    "sam": (
        "a 10-year-old Japanese-Korean boy named Sam with light-medium warm skin, compact "
        "athletic muscular build, shortest in group, black spiky messy hair gel-styled "
        "on top shaved close on sides, almond-shaped dark brown eyes with mischievous "
        "sparkle, round face with pointed chin, missing bottom front baby tooth, impish "
        "grin, bright red fingerless gaming gloves, black PLAYER 1 t-shirt, athletic "
        "shorts with side stripes, high-top sneakers with LED lights in soles, gaming "
        "headset around neck, knee pads with stickers"
    ),
    "blip": (
        "a small cute white boxy robot named Blip with a rectangular head and body as one unit, "
        "clean matte white casing, front square screen face with thin dark border, "
        "large bright blue circular LED eyes with pixel dot pattern and black pupils, "
        "dark red curved smile mouth, two small white rounded stick antennas on top of head, "
        "two short arms with black elbow joints and rounded hands, "
        "two legs with black knee and ankle joints and rounded feet, "
        "walks on its two legs, friendly cheerful childlike appearance"
    ),
    "daadi": (
        "a 68-year-old Indian grandmother named Daadi with silver hair, warm kind "
        "face with gentle smile, short round build, wearing soft lavender or cream "
        "cotton salwar kameez, thin gold chain with small pendant, reading glasses on a "
        "beaded chain around neck, warm loving maternal presence"
    ),
    "gridlord": (
        "a mysterious digital entity named Gridlord appearing as a stern angular "
        "pixelated face on computer screens with glowing green eyes, jagged metallic "
        "crown symbol embedded in forehead, skin rendered in shifting green-purple "
        "digital noise, sharp angular features with prominent metallic implant or scar "
        "running from forehead to cheek, short slicked-back dark hair, surrounded by "
        "cascading green code text and purple static distortion, glowing orange neon "
        "crown icon above, never shown in physical form always on monitors or displays"
    ),
}

# ── CHARACTER KEYWORDS for auto-detection ──
CHARACTER_KEYWORDS = {
    "maya": [
        "maya", "indian girl", "inventor girl", "girl with goggles", "olive vest",
        "girl with ponytail", "girl with messy ponytail",
        "11-year-old indian", "brown skin girl",
        "girl with warm brown skin", "messy ponytail",
    ],
    "leo": [
        "leo", "mexican-american boy", "coder boy", "boy with tablet",
        "boy with beanie", "navy blue beanie", "pixel heart patch",
        "11-year-old mexican-american",
    ],
    "zara": [
        "zara", "nigerian-british girl", "artist girl", "girl with camera",
        "yellow crossbody bag", "denim jacket with patches",
        "girl with sketchpad", "12-year-old nigerian",
        "black hair twists", "colorful leggings",
    ],
    "sam": [
        "sam", "japanese-korean boy", "gaming gloves", "red fingerless",
        "boy vaulting", "boy with gloves", "led sneakers",
        "10-year-old japanese-korean", "fingerless gaming gloves",
    ],
    "blip": [
        "blip", "white cube robot", "cube robot", "small white cube",
        "cute white cube", "floating white cube", "glowing white cube",
        "small cube robot",
    ],
    "daadi": [
        "daadi", "indian grandmother", "elderly indian grandmother",
        "indian grandma", "saree", "salwar kameez",
    ],
    "gridlord": [
        "gridlord", "grid lord", "digital entity", "pixelated face on screen",
        "crown icon", "digital villain", "glitch face",
    ],
}

# ── FIXED SEEDS PER CHARACTER ──────────────────────────────────────────
# Each character gets a unique seed. When multiple characters appear,
# the seeds are combined deterministically. This ensures the same
# visual "DNA" for a character across all images.
CHARACTER_SEEDS = {
    "maya": 10101,
    "leo": 20202,
    "zara": 30303,
    "sam": 40404,
    "blip": 50505,
    "daadi": 60606,
    "gridlord": 70707,
}

# ── REFERENCE IMAGES for img2img character consistency ─────────────────
# Best character portrait from the Characters/ folder. Used as init_image
# so Bonsai "sees" the character and reproduces them consistently.
CHAR_REF_DIR = OUTPUT_DIR / "Characters"
CHARACTER_REF_IMAGES = {
    "maya": CHAR_REF_DIR / "Maya" / "template_reference.png",
    "leo": CHAR_REF_DIR / "Leo" / "template_reference.png",
    "zara": CHAR_REF_DIR / "Zara" / "template_reference.png",
    "sam": CHAR_REF_DIR / "Sam" / "template_reference.png",
    "blip": CHAR_REF_DIR / "Blip" / "template_reference.png",
    "daadi": None,
}

# ── CATEGORY CONFIG ────────────────────────────────────────────────────
CATEGORY_DIRS = {
    "strip": "Strips",
    "marginalia": "Marginalia",
    "chapter-vignette": "ChapterHeaders",
    "character-card": "Cards",
    "map": "Maps",
    "blueprint": "Blueprints",
    "title-page": "",
    "section-divider": "Dividers",
    "glitch-art": "GlitchArt",
    "document": "Documents",
    "endpaper": "",
    "spot": "Spots",
    "full-page": "",
    "half-page": "",
    "back-matter": "",
}

STEPS_BY_TYPE = {
    "full-page": 12,
    "half-page": 10,
    "spot": 8,
    "strip": 10,
    "back-matter": 10,
    "marginalia": 6,
    "chapter-vignette": 6,
    "character-card": 12,
    "map": 12,
    "blueprint": 6,
    "title-page": 16,
    "section-divider": 6,
    "glitch-art": 10,
    "document": 6,
    "endpaper": 10,
}


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        print(f"ERROR: {MANIFEST_PATH} not found")
        sys.exit(1)
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(manifest: dict):
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def detect_characters(prompt: str) -> list[str]:
    import re
    prompt_lower = prompt.lower()
    found = []
    for char_id, keywords in CHARACTER_KEYWORDS.items():
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, prompt_lower):
                found.append(char_id)
                break
    return sorted(found)


def compute_seed(characters: list[str], fallback_seed: int = 0) -> int:
    if not characters:
        return fallback_seed
    combined = "_".join(characters)
    h = hashlib.md5(combined.encode()).hexdigest()
    return int(h[:8], 16) % 2147483647


CHARACTER_ACTIONS = {
    "maya": [
        "Maya adjusts her safety goggles as she examines the gadget closely",
        "Maya studies the object with intense concentration, her ponytail swinging",
        "Maya points excitedly at her discovery, her gap-toothed grin showing",
        "Maya kneels down for a closer look, her olive vest pockets jingling with tools",
        "Maya traces the circuit path with her finger, deep in thought",
    ],
    "leo": [
        "Leo types rapidly on his tablet, code reflecting in his reading glasses",
        "Leo studies the data with narrowed eyes, his beanie slightly askew",
        "Leo shows his analysis to the others, pointing at his screen",
        "Leo paces while thinking, his gray hoodie sleeves pulled over his hands",
    ],
    "zara": [
        "Zara composes the perfect photograph, her camera held steady",
        "Zara sketches in her notebook with quick confident strokes",
        "Zara observes the scene with her artist's eye, a warm smile on her face",
        "Zara adjusts her yellow crossbody bag as she leans in for a better view",
    ],
    "sam": [
        "Sam bounces excitedly, his red gaming gloves gesturing wildly",
        "Sam grins his gap-toothed smile, always ready for action",
        "Sam darts around to see everything at once, his LED sneakers flashing",
        "Sam pumps his fist in excitement, full of youthful energy",
    ],
    "blip": [
        "Blip floats nearby, its cyan LED screen showing a curious expression",
        "Blip bobs in the air, its face cycling through emoji reactions",
        "Blip hovers at eye level, projecting a soft glow onto the scene",
        "Blip's antenna wiggles as it processes the situation",
    ],
    "daadi": [
        "Daadi watches with warm loving eyes, a gentle smile on her kind face",
        "Daadi bustles around the kitchen with practiced efficiency",
        "Daadi wipes her hands and turns to face them with a grandmotherly warmth",
    ],
}

CHARACTER_SHORT = {
    "maya": "Maya, 11-year-old Indian girl inventor with warm brown skin, dark messy ponytail with pencil stuck in it, safety goggles on forehead, olive green utility vest full of tools, red t-shirt, cargo shorts, velcro sneakers, gap-toothed grin",
    "leo": "Leo, 11-year-old Mexican-American boy coder with warm tan skin, navy blue beanie with pixel heart patch, dark intense eyes, oversized gray hoodie, tablet in front pocket, reading glasses on chain around neck",
    "zara": "Zara, 12-year-old Nigerian-British girl artist with rich dark brown skin, voluminous black hair twists with colorful thread, high cheekbones, bright yellow crossbody bag, oversized denim jacket with patches, colorful leggings",
    "sam": "Sam, 10-year-old Japanese-Korean boy gamer with light warm skin, short spiky black hair shaved on sides, mischievous smile, missing front tooth, bright red fingerless gaming gloves, black PLAYER 1 t-shirt, LED sneakers",
    "blip": "Blip, small cute white cube robot with matte white rounded body, cyan LED screen showing happy dot eyes and smile, small antenna on top that wiggles, hover thrusters underneath, floating 2 feet off ground",
    "daadi": "Daadi, 68-year-old Indian grandmother with silver hair in soft bun, warm kind face, soft lavender cotton salwar kameez, thin gold chain, reading glasses on beaded chain around neck",
    "gridlord": "Gridlord, mysterious digital entity appearing as stern angular pixelated face on screens with glowing green eyes, jagged metallic crown symbol in forehead, green-purple digital noise skin, metallic implant scar on face, surrounded by green code and purple static, orange neon crown icon",
}

CHARACTER_SHORT_ALT = {
    "maya": "Maya, 11-year-old Indian girl inventor with warm brown skin, dark messy ponytail, safety goggles on forehead, olive green utility vest, red t-shirt, cargo shorts, gap-toothed grin",
    "leo": "Leo, 11-year-old Mexican-American boy coder with warm tan skin, navy beanie with pixel heart patch, dark intense eyes, gray hoodie, tablet, reading glasses",
    "zara": "Zara, 12-year-old Nigerian-British girl artist with rich dark brown skin, black hair twists with colorful thread, high cheekbones, yellow crossbody bag, denim jacket with patches",
    "sam": "Sam, 10-year-old Japanese-Korean boy gamer with light warm skin, spiky black hair, red gaming gloves, black PLAYER 1 t-shirt, LED sneakers",
    "blip": "Blip, small cute white cube robot with cyan LED smile face, antenna on top, hover thrusters, floating 2 feet off ground",
    "daadi": "Daadi, 68-year-old Indian grandmother with silver hair, warm kind face, lavender salwar kameez, reading glasses on chain",
    "gridlord": "Gridlord, digital entity as stern pixelated face on screens, green eyes, crown symbol in forehead, green-purple noise skin, green code and purple static, orange neon crown icon",
}

GROUP_DESC = "A diverse group of four children of different ethnicities - an Indian girl inventor with ponytail and goggles, a Mexican-American boy coder with beanie and glasses, a Nigerian-British girl artist with hair twists and yellow bag, a Japanese-Korean boy gamer with red gloves - plus a small floating white cube robot with a glowing cyan screen"

def _count_kids(characters: list[str]) -> int:
    kids = {"maya", "leo", "zara", "sam"}
    return sum(1 for c in characters if c in kids)


def _count_robots(characters: list[str]) -> int:
    bots = {"blip"}
    return sum(1 for c in characters if c in bots)


def build_full_prompt(raw_prompt: str) -> str:
    characters = detect_characters(raw_prompt)
    char_parts = []
    n_kids = _count_kids(characters)
    n_robots = _count_robots(characters)

    for c in characters:
        if c in CHARACTER_DESCRIPTIONS:
            char_parts.append(CHARACTER_DESCRIPTIONS[c])

    import random
    action_parts = []
    for c in characters:
        if c in CHARACTER_ACTIONS:
            action = random.choice(CHARACTER_ACTIONS[c])
            action_parts.append(action)

    count_constraints = []
    if n_kids >= 2:
        count_constraints.append(
            f"CRITICAL: exactly {n_kids} children visible in the entire image, "
            f"no extra kids, no duplicate children, absolutely no additional people beyond these {n_kids}"
        )
    elif n_kids == 1:
        count_constraints.append(
            "CRITICAL: exactly one person visible in the entire image, "
            "no other people in background or foreground, no extra figures"
        )
    if n_robots >= 1 and n_kids >= 1:
        count_constraints.append(
            f"exactly {n_robots} small white cube robot, no other robots or machines"
        )

    count_block = ". ".join(count_constraints)

    if char_parts:
        char_block = ". ".join(char_parts)
        action_block = " ".join(action_parts) if action_parts else ""

        result = (
            f"THE SCENE: {raw_prompt}. "
            f"{STYLE_PREFIX}. "
            f"CHARACTERS IN THIS SCENE: {char_block}. "
            f"WHAT THEY ARE DOING: {action_block}. "
        )
        if count_block:
            result += f"{count_block}. "
        result += (
            f"{STYLE_SUFFIX}. "
            f"Art direction: children's book illustration, every character has smooth clear skin, "
            f"the scene and setting are fully visible in the background."
        )
        return result
    else:
        return (
            f"THE SCENE: {raw_prompt}. "
            f"{SCENE_STYLE}. "
            f"{SCENE_SUFFIX}. "
            f"Art direction: children's book scene illustration, the scene is fully visible."
        )


def get_output_path(item: dict) -> Path:
    filename = item["file"]
    if "/" in filename or "\\" in filename:
        return OUTPUT_DIR / filename
    item_type = item.get("type", "")
    subdir = CATEGORY_DIRS.get(item_type, "")
    if subdir:
        return OUTPUT_DIR / subdir / filename
    return OUTPUT_DIR / filename


def parse_size(size_val, default_dim: int = 1024) -> tuple[int, int]:
    if isinstance(size_val, int):
        return (size_val, size_val)
    if isinstance(size_val, str) and "x" in size_val:
        w, h = size_val.split("x")
        return (int(w), int(h))
    return (default_dim, default_dim)


def get_primary_character_ref(characters: list[str]) -> Path | None:
    """Pick the PRIMARY character's reference image for img2img."""
    priority = ["maya", "leo", "zara", "sam", "blip", "daadi"]
    for c in priority:
        if c in characters:
            ref = CHARACTER_REF_IMAGES.get(c)
            if ref and ref.exists():
                return ref
    return None


def encode_image_to_b64(image_path: Path) -> str:
    """Read an image file and return base64-encoded PNG string."""
    data = image_path.read_bytes()
    return base64.b64encode(data).decode("ascii")


def check_server(server_url: str) -> bool:
    try:
        req = Request(f"{server_url}/health")
        with urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read())
                print(f"Server OK - GPU: {data.get('gpu', '?')}")
                return True
    except Exception as e:
        print(f"ERROR: Cannot reach server at {server_url}: {e}")
    return False


def generate_one(server_url: str, prompt: str, width: int, height: int,
                 steps: int, seed: int, retries: int,
                 init_image_b64: str | None = None,
                 image_strength: float = 0.4,
                 max_seq: int = 1024) -> bytes:
    payload_dict = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "seed": seed,
        "max_sequence_length": max_seq,
    }
    endpoint = "/generate"

    if init_image_b64:
        payload_dict["init_image"] = init_image_b64
        payload_dict["image_strength"] = image_strength
        endpoint = "/generate_unified"

    payload = json.dumps(payload_dict).encode("utf-8")
    req = Request(
        f"{server_url}{endpoint}", data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )

    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with urlopen(req, timeout=300) as resp:
                if resp.status == 200:
                    return resp.read()
                body = resp.read().decode("utf-8", errors="replace")
                print(f"    HTTP {resp.status}: {body[:200]}")
                if resp.status == 507:
                    return b""
                if resp.status == 422 and init_image_b64:
                    print("    img2img not supported, retrying as txt2img...")
                    payload_dict.pop("init_image", None)
                    payload_dict.pop("image_strength", None)
                    payload = json.dumps(payload_dict).encode("utf-8")
                    req = Request(
                        f"{server_url}/generate", data=payload,
                        headers={"Content-Type": "application/json"}, method="POST",
                    )
                    continue
        except HTTPError as e:
            print(f"    HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}")
            if e.code == 507:
                return b""
            if e.code == 422 and init_image_b64:
                print("    img2img not supported, retrying as txt2img...")
                payload_dict.pop("init_image", None)
                payload_dict.pop("image_strength", None)
                payload = json.dumps(payload_dict).encode("utf-8")
                req = Request(
                    f"{server_url}/generate", data=payload,
                    headers={"Content-Type": "application/json"}, method="POST",
                )
                continue
        except (URLError, ConnectionError, TimeoutError) as e:
            last_err = e
            print(f"    Attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(attempt * 5)
        except Exception as e:
            last_err = e
            print(f"    Unexpected: {e}")
            if attempt < retries:
                time.sleep(5)

    print(f"    FAILED after {retries} attempts: {last_err}")
    return b""


def collect_all_items(manifest: dict) -> list[dict]:
    arrays = [
        "illustrations", "strips", "blip_marginalia_images", "chapter_vignettes",
        "character_cards", "maps", "gadget_blueprints", "title_page",
        "section_dividers", "glitch_art", "extra_spots", "documents", "endpapers",
    ]
    items = []
    for key in arrays:
        if key in manifest:
            for item in manifest[key]:
                item["_array"] = key
                items.append(item)
    return items


def main():
    parser = argparse.ArgumentParser(description="Manifest Batch Client v3 - Character Consistent")
    parser.add_argument("--server", required=True)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--delay", type=float, default=1.5)
    parser.add_argument("--steps", type=int, default=None,
                        help="Override steps for ALL images")
    parser.add_argument("--type", dest="filter_types",
                        help="Comma-separated types to generate")
    parser.add_argument("--only", nargs="+",
                        help="Only generate specific IDs (e.g. --only B1-006 B1-007)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--raw-prompts", action="store_true",
                        help="Skip character injection")
    parser.add_argument("--show-prompt", action="store_true",
                        help="Print full enhanced prompt")
    parser.add_argument("--strength", type=float, default=0.65,
                        help="img2img strength (0.1=close to ref, 0.9=mostly new). Default 0.65")
    parser.add_argument("--max-seq", type=int, default=1024,
                        help="max sequence length for text encoder (default 1024)")
    parser.add_argument("--no-img2img", action="store_true",
                        help="Disable img2img, use txt2img only (character descriptions only)")
    args = parser.parse_args()

    server_url = f"http://{args.server}:{args.port}"
    manifest = load_manifest()
    filter_types = set()
    if args.filter_types:
        filter_types = {t.strip() for t in args.filter_types.split(",")}
    only_ids = set(args.only) if args.only else set()

    all_items = collect_all_items(manifest)
    todo = []
    skip = []

    for item in all_items:
        item_type = item.get("type", "")
        item_id = item["id"]
        filename = item["file"]

        if only_ids and item_id not in only_ids:
            skip.append((item_id, filename, "filtered"))
            continue

        if filter_types and item_type not in filter_types:
            skip.append((item_id, filename, "filtered"))
            continue

        out_path = get_output_path(item)
        if not args.overwrite and out_path.exists() and out_path.stat().st_size > 1000:
            skip.append((item_id, filename, "exists"))
            if item.get("status") != "generated":
                item["status"] = "generated"
            continue

        todo.append(item)

    print(f"\n{'=' * 65}")
    print(f"  Manifest Batch Client v3 (Character Consistent)")
    print(f"  Server  : {server_url}")
    print(f"  Total   : {len(all_items)}")
    print(f"  To gen  : {len(todo)}")
    print(f"  Skipped : {len(skip)}")
    print(f"  Steps   : {'auto per type' if args.steps is None else args.steps}")
    print(f"  Char inj: {'OFF (raw)' if args.raw_prompts else 'ON + fixed seeds'}")
    print(f"  img2img : {'DISABLED' if args.no_img2img else f'ENABLED (strength={args.strength})'}")
    print(f"{'=' * 65}\n")

    for item_id, filename, reason in skip[:20]:
        tag = "EXISTS" if reason == "exists" else "SKIP"
        print(f"  [{tag}] {item_id}: {filename}")
    if len(skip) > 20:
        print(f"  ... and {len(skip) - 20} more skipped")

    if args.dry_run:
        print(f"\nDry run - {len(todo)} images:\n")
        for item in todo:
            w, h = parse_size(item.get("size", 1024))
            item_type = item.get("type", "")
            steps = args.steps or STEPS_BY_TYPE.get(item_type, 4)
            raw_prompt = item["prompt"]
            chars = detect_characters(raw_prompt)
            seed = secrets.randbits(31)
            full_prompt = raw_prompt if args.raw_prompts else build_full_prompt(raw_prompt)
            print(f"  {item['id']}: {item['file']} ({w}x{h}, steps={steps}, seed={seed})")
            if chars:
                print(f"    Characters: {', '.join(chars)}")
            if args.show_prompt:
                print(f"    Full: {full_prompt[:250]}...")
            else:
                print(f"    Raw: {raw_prompt[:90]}...")
        return

    if not todo:
        print("\nNothing to generate!")
        save_manifest(manifest)
        return

    if not check_server(server_url):
        sys.exit(1)

    print()
    success = 0
    failed = 0

    for i, item in enumerate(todo, 1):
        item_id = item["id"]
        filename = item["file"]
        item_type = item.get("type", "")
        raw_prompt = item["prompt"]
        w, h = parse_size(item.get("size", 1024))
        steps = args.steps or STEPS_BY_TYPE.get(item_type, 4)
        chars = detect_characters(raw_prompt)
        seed = int(hashlib.md5(item_id.encode()).hexdigest()[:8], 16) % 2147483647 if chars else 0
        full_prompt = raw_prompt if args.raw_prompts else build_full_prompt(raw_prompt)
        out_path = get_output_path(item)

        char_tag = f" [{','.join(chars)}]" if chars else ""
        print(f"[{i}/{len(todo)}] {item_id}: {filename} ({w}x{h}, s={steps}, seed={seed}){char_tag}")
        if args.show_prompt:
            print(f"  Full: {full_prompt[:180]}...")
        else:
            print(f"  Raw: {raw_prompt[:90]}...")

        # img2img: load character reference image
        init_b64 = None
        if not args.no_img2img and chars:
            ref_path = get_primary_character_ref(chars)
            if ref_path:
                init_b64 = encode_image_to_b64(ref_path)
                print(f"  img2img ref: {ref_path.name} (strength={args.strength})")

        out_path.parent.mkdir(parents=True, exist_ok=True)

        png_bytes = generate_one(server_url, full_prompt, w, h, steps, seed, args.retries,
                                 init_image_b64=init_b64, image_strength=args.strength,
                                 max_seq=args.max_seq)

        if png_bytes and len(png_bytes) > 1000:
            out_path.write_bytes(png_bytes)
            kb = len(png_bytes) / 1024
            print(f"  OK: {out_path.name} ({kb:.0f} KB)")
            item["status"] = "generated"
            save_manifest(manifest)
            success += 1
        else:
            print(f"  FAIL: {item_id}")
            item["status"] = "failed"
            save_manifest(manifest)
            failed += 1

        if i < len(todo):
            time.sleep(args.delay)
        print()

    print(f"\n{'=' * 65}")
    print(f"  Done!  Success: {success}  Failed: {failed}")
    print(f"{'=' * 65}\n")


if __name__ == "__main__":
    main()

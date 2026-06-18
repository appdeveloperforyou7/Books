import json
import time
import sys
from urllib.request import Request, urlopen
from pathlib import Path

SERVER = "http://192.168.29.7:8765"
OUT_DIR = Path(r"D:\Kapil\Books\TD-1\BookLayout\images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

STYLE = "THE GLITCH SQUAD children's book art, vibrant cel-shaded 2D digital illustration, bold clean black outlines, flat color fills with minimal soft shading, round friendly proportions, large expressive eyes, bright candy-color palette, no photorealism no 3D render"

images = [
    {
        "file": "blip_activating.png",
        "prompt": f"{STYLE}, A small cute white cube robot activating on a cluttered desk, soft cyan glow emanating from LED screen showing happy face, small antenna wiggling, tiny hover thrusters glowing underneath lifting it slightly off desk, warm golden desk lamp lighting from the left, scattered tools and circuit boards and screws on desk, pencils and blueprints in background, cozy bedroom workshop scene, warm brown skin tone hand of a 10-year-old girl reaching toward the robot with wonder, magical moment of first contact, 8k detail, THE GLITCH SQUAD official art style",
        "size": 1024
    },
    {
        "file": "comic_street_glitch.png",
        "prompt": f"{STYLE}, City neighborhood street in chaos, traffic lights flashing disco colors of pink and green and blue, confused drivers stopped at intersection, dogs with glowing LED collars running in circles, Maple Street neighborhood with old brick buildings and trees, warm summer evening light, funny chaotic scene, no photorealism, THE GLITCH SQUAD official art style",
        "size": 512
    },
    {
        "file": "comic_sprinklers.png",
        "prompt": f"{STYLE}, Interior of a cozy apartment with indoor sprinklers going off spraying water everywhere, a cat leaping off a bookshelf in surprise, grandma with reading glasses looking shocked holding a newspaper getting wet, water puddles on floor, funny chaotic moment, warm home interior with Indian decorations on wall, THE GLITCH SQUAD official art style",
        "size": 512
    },
    {
        "file": "comic_drone.png",
        "prompt": f"{STYLE}, A delivery drone with a small package spinning out of control doing loop-de-loops in the sky over a city neighborhood, packages falling with parachutes, two kids on the sidewalk pointing and cheering, blue sky with fluffy clouds, funny action scene, THE GLITCH SQUAD official art style",
        "size": 512
    },
    {
        "file": "comic_photo_frames.png",
        "prompt": f"{STYLE}, Close-up of three digital photo frames on a mantelpiece showing funny cat memes instead of family photos, a confused family of four staring at them with open mouths, living room interior, warm lighting, comedic scene, THE GLITCH SQUAD official art style",
        "size": 512
    },
    {
        "file": "comic_maya_window.png",
        "prompt": f"{STYLE}, Wide view of a 10-year-old Indian girl with messy ponytail and olive green vest looking out her apartment window in shock at the chaos below, a small cute white cube robot with cyan LED face floating beside her, the street below shows neon lights flickering and water spraying and drones spinning, warm brown skin, safety goggles on forehead, golden evening light from window, THE GLITCH SQUAD official art style",
        "size": 1024
    },
    {
        "file": "sam_portrait.png",
        "prompt": f"{STYLE}, Portrait of a 9-year-old Japanese-Korean boy named Sam, light-medium warm skin, spiky messy black hair on top shaved close on sides, almond-shaped dark brown eyes with mischievous sparkle, round face with pointed chin, missing bottom front tooth goofy grin, bright red fingerless gaming gloves, black game controller t-shirt, compact athletic build, white simple background, THE GLITCH SQUAD official art style, character portrait",
        "size": 512
    },
    {
        "file": "leo_portrait.png",
        "prompt": f"{STYLE}, Portrait of a 10-year-old Mexican-American boy named Leo, warm tan golden-brown skin, compact stocky build, black hair under navy blue beanie with small pixelated heart patch, very dark intense eyes with thick eyebrows, small scar on chin, calm focused expression, gray hoodie, reading glasses on chain around neck, white simple background, THE GLITCH SQUAD official art style, character portrait",
        "size": 512
    },
    {
        "file": "zara_portrait.png",
        "prompt": f"{STYLE}, Portrait of an 11-year-old Nigerian-British girl named Zara, rich dark brown skin, tall graceful build, voluminous black natural hair in chunky twists with colorful thread, bright expressive dark brown eyes, high cheekbones, wide smile with gap in front teeth, bright yellow crossbody bag, oversized denim jacket with patches, colorful leggings, white simple background, THE GLITCH SQUAD official art style, character portrait",
        "size": 512
    },
    {
        "file": "zara_sketching.png",
        "prompt": f"{STYLE}, 11-year-old Nigerian-British girl Zara sketching furiously in a notebook with intense creative focus, rich dark brown skin, voluminous black hair twists with colorful threads, oversized denim jacket with doodles on sleeves, colorful markers scattered around her, bright yellow crossbody bag beside her, stylus behind ear, beaded bracelets on wrists, warm interior lighting, THE GLITCH SQUAD official art style",
        "size": 512
    },
    {
        "file": "hq_discovery.png",
        "prompt": f"{STYLE}, Four diverse kids and a small cute floating white cube robot discovering an abandoned secret lab in a dusty basement, flashlight beams cutting through darkness revealing old workbenches and holographic displays flickering to life with blue light, circuit diagrams pinned to walls, dusty NexCorp equipment, a 10-year-old Indian girl with olive vest looking amazed, a 10-year-old Mexican-American boy with navy beanie already at a terminal, an 11-year-old Nigerian-British girl with yellow bag photographing everything, a 9-year-old Japanese-Korean boy with red gloves doing a victory pose, the cube robot showing a happy cyan face, warm golden flashlight beams mixing with cool blue screen glow, dust particles in the air, sense of wonder and discovery, THE GLITCH SQUAD official art style, cinematic wide shot",
        "size": 1024
    },
]

print(f"Generating {len(images)} images for sample chapter...\n")

success = 0
failed = 0

for i, img in enumerate(images, 1):
    out_path = OUT_DIR / img["file"]
    if out_path.exists() and out_path.stat().st_size > 1000:
        print(f"[{i}/{len(images)}] EXISTS: {img['file']} ({out_path.stat().st_size // 1024} KB)")
        success += 1
        continue

    print(f"[{i}/{len(images)}] {img['file']} ({img['size']}px)...")
    print(f"  Prompt: {img['prompt'][:80]}...")

    payload = json.dumps({
        "prompt": img["prompt"],
        "width": img["size"],
        "height": img["size"],
        "steps": 4,
    }).encode()

    req = Request(
        f"{SERVER}/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    t0 = time.time()
    try:
        with urlopen(req, timeout=300) as resp:
            data = resp.read()
            elapsed = time.time() - t0
            if len(data) > 1000:
                out_path.write_bytes(data)
                print(f"  SAVED: {out_path.name} ({len(data) // 1024} KB, {elapsed:.0f}s)")
                success += 1
            else:
                print(f"  FAILED: response too small ({len(data)} bytes)")
                failed += 1
    except Exception as e:
        print(f"  ERROR: {e}")
        failed += 1

    if i < len(images):
        time.sleep(2)

print(f"\nDone! Success: {success}, Failed: {failed}")

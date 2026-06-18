import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
import os
import hashlib
from overlay_text import (
    overlay_text, overlay_text_centered, overlay_label,
    FONT_ROUNDED, FONT_CALIBRI, FONT_COMIC,
)

SERVER = "http://192.168.29.7:8765"
IMAGES_DIR = r"D:\Kapil\Books\TD-1\Images"


def gen_img(prompt, seed, size=512):
    r = requests.post(f"{SERVER}/generate", json={
        "prompt": prompt,
        "negative_prompt": "",
        "width": size, "height": size,
        "seed": seed,
        "guidance_scale": 3.5,
        "num_inference_steps": 28,
    }, timeout=120)
    if r.status_code == 200:
        arr = np.frombuffer(r.content, dtype=np.uint8)
        return cv2.imdecode(arr, cv2.IMREAD_COLOR)
    print(f"  ERROR: {r.status_code}")
    return None


def seed_for(id_str):
    return int(hashlib.md5(f"{id_str}_notext_v2".encode()).hexdigest()[:8], 16) % 2147483647


def add_scanlines(img, opacity=0.15, thickness=2, gap=3):
    h, w = img.shape[:2]
    overlay = img.copy()
    for y in range(0, h, gap + thickness):
        overlay[y:y + thickness, :] = (overlay[y:y + thickness, :].astype(np.float32) * (1 - opacity)).astype(np.uint8)
    return overlay


def add_glitch_text(img, text, x, y, font_size=28, color=(200, 80, 180),
                    rgb_shift=3, scanlines=True, noise_amount=15):
    result = overlay_text(
        img, text, x, y, font_size=font_size, color=color,
        font_path=FONT_ROUNDED, shadow=True, glow=True, stroke=True,
        glow_alpha=0.2, shadow_blur=4, stroke_width=1,
    )
    h, w = result.shape[:2]
    if rgb_shift > 0:
        b, g, r = cv2.split(result)
        r_shifted = np.roll(r, rgb_shift, axis=1)
        b_shifted = np.roll(b, -rgb_shift, axis=1)
        result = cv2.merge([b_shifted, g, r_shifted])
    if noise_amount > 0:
        noise = np.random.normal(0, noise_amount, result.shape).astype(np.int16)
        text_region = result[y:y + font_size + 10, max(0, x - 10):min(w, x + len(text) * (font_size // 2) + 10)]
        if text_region.size > 0:
            noisy = np.clip(text_region.astype(np.int16) + noise[:text_region.shape[0], :text_region.shape[1]], 0, 255).astype(np.uint8)
            result[y:y + font_size + 10, max(0, x - 10):min(w, x + len(text) * (font_size // 2) + 10)] = noisy
    if scanlines:
        result = add_scanlines(result, opacity=0.1, thickness=1, gap=2)
    return result


def add_subtle_map_label(img, text, x, y, font_size=16, color=(255, 255, 255)):
    h, w = img.shape[:2]
    font = ImageFont.truetype(FONT_CALIBRI, font_size)
    tmp = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    tmp_draw = ImageDraw.Draw(tmp)
    bbox = tmp_draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    base = Image.fromarray(img_rgb).convert("RGBA")

    banner = Image.new("RGBA", (tw + 10, th + 6), (0, 0, 0, 0))
    banner_draw = ImageDraw.Draw(banner)
    banner_draw.rounded_rectangle([(0, 0), (tw + 9, th + 5)], radius=3, fill=(0, 0, 0, 100))

    banner_pos = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    banner_pos.paste(banner, (x - 5, y - 3))
    composite = Image.alpha_composite(base, banner_pos)

    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    text_draw.text((x, y), text, font=font, fill=(*color, 220))

    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_draw.text((x + 1, y + 1), text, font=font, fill=(0, 0, 0, 120))

    composite = Image.alpha_composite(composite, shadow_layer)
    composite = Image.alpha_composite(composite, text_layer)

    result_rgb = composite.convert("RGB")
    return cv2.cvtColor(np.array(result_rgb), cv2.COLOR_RGB2BGR)


MAPS = [
    {
        "id": "MAP-01", "file": "Maps/map_neonville.png",
        "prompt": "Illustrated children's book isometric map of a neighborhood with apartment buildings, houses, shops, a tall glass skyscraper, curving streets with cars, green parks with benches and trees, rolling hills in background, blue sky with clouds, compass rose in corner, warm earthy palette, cartoonish whimsical style, no text, no labels, no street names, no words, no letters",
        "labels": [
            ("MAPLE STREET", 80, 90, 16),
            ("NEONVILLE", 220, 40, 28),
            ("MAIN STATION", 380, 350, 14),
            ("VALLEY STREET", 500, 120, 14),
            ("COMMUNITY CENTER", 350, 220, 13),
            ("PARK", 150, 300, 15),
        ],
    },
    {
        "id": "MAP-02", "file": "Maps/map_underground.png",
        "prompt": "Illustrated cross-section map showing an apartment building at the top with balconies and trees around it, and an underground tunnel system below carved into brown rocky earth with large silver pipes, multiple rooms with equipment inside, dim lighting from within the rooms, cartoon comic book style, warm surface vs cool underground contrast, no text, no labels, no room names, no words, no letters",
        "labels": [
            ("WAGLE STREET", 180, 55, 18),
            ("SECRET LAB", 250, 380, 16),
            ("SERVER ROOM", 420, 380, 15),
            ("TUNNEL EXIT", 480, 450, 14),
            ("PIPES", 80, 300, 14),
        ],
    },
]

DOCUMENTS_GLITCH = [
    {
        "id": "DOC-02", "file": "Documents/doc_gridlord_message.png",
        "prompt": "A computer monitor screen displaying a glitched message interface with dark background, the screen is on a wooden desk in a dimly lit room, purple and green color scheme, space for text lines, glitch effects and scan lines, no text, no letters, no words",
        "overlays": [
            ("HELP ME.", 140, 200, 30, (200, 80, 180)),
            ("TRUST THEM.", 140, 260, 26, (200, 80, 180)),
            ("THE SIGNAL.", 140, 320, 28, (80, 200, 80)),
        ],
    },
    {
        "id": "DOC-03", "file": "Documents/doc_blip_diagnostic.png",
        "prompt": "A retro-style diagnostic screen with a white cube robot schematic in the center with system readouts around it, dark background with green grid lines, space for text readouts on sides, the robot schematic shows a cute boxy robot with blue eyes, no text, no letters, no words",
        "overlays": [
            ("SIGNAL ORIGIN: UNKNOWN", 20, 30, 15, (80, 200, 80)),
            ("CORE STATUS: ACTIVE", 20, 60, 15, (80, 200, 80)),
            ("94% FUNCTIONAL", 20, 90, 15, (80, 200, 80)),
            ("0.7 BPS SIGNAL", 20, 440, 15, (80, 200, 80)),
            ("DIAGNOSTIC COMPLETE", 20, 470, 15, (80, 200, 80)),
            ("BLIP v1.0", 200, 500, 17, (80, 200, 80)),
        ],
    },
]


print("=== MAPS (subtle labels) ===")
for mp in MAPS:
    s = seed_for(mp["id"])
    print(f"\n{mp['id']} seed={s}...", end=" ", flush=True)
    img = gen_img(mp["prompt"], s, size=768)
    if img is None:
        print("FAILED")
        continue
    for text, px, py, fs in mp["labels"]:
        color = (255, 220, 100) if text == "NEONVILLE" else (255, 255, 255)
        img = add_subtle_map_label(img, text, px, py, font_size=fs, color=color)
    out = os.path.join(IMAGES_DIR, mp["file"])
    cv2.imwrite(out, img)
    print(f"OK -> {out}")


print("\n\n=== GLITCH DOCUMENTS ===")
for doc in DOCUMENTS_GLITCH:
    s = seed_for(doc["id"])
    print(f"\n{doc['id']} seed={s}...", end=" ", flush=True)
    img = gen_img(doc["prompt"], s, size=512)
    if img is None:
        print("FAILED")
        continue
    for text, px, py, fs, color in doc["overlays"]:
        img = add_glitch_text(
            img, text, px, py, font_size=fs, color=color,
            rgb_shift=2, scanlines=True, noise_amount=10,
        )
    out = os.path.join(IMAGES_DIR, doc["file"])
    cv2.imwrite(out, img)
    print(f"OK -> {out}")


print("\n\nDONE!")

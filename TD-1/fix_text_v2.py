import cv2
import numpy as np
import requests
import os
import hashlib
from overlay_text import (
    overlay_text, overlay_text_centered, overlay_multiline, overlay_label,
    FONT_ROUNDED, FONT_COMIC, FONT_CALIBRI,
)

SERVER = "http://192.168.29.7:8765"
IMAGES_DIR = r"D:\Kapil\Books\TD-1\Images"
TEMP = r"E:\Temp\kilo\textfix_v2"
os.makedirs(TEMP, exist_ok=True)


def gen_img(prompt, seed, size=512):
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
    print(f"  ERROR: {r.status_code}")
    return None


def seed_for(id_str):
    return int(hashlib.md5(f"{id_str}_notext_v2".encode()).hexdigest()[:8], 16) % 2147483647


DIVIDERS = [
    {
        "id": "SD-01", "file": "Dividers/divider_act1_discovery.png",
        "prompt": "Decorative section divider banner for a children's book, horizontal banner shape with warm orange-brown gradient background with golden circuit-board line patterns, three icons in a row: a magnifying glass on the left, a cute white boxy robot with blue eyes in the center, a white cube on the right, golden-yellow rounded border, no text, no letters, no words, flat digital cartoon style, cheerful tech-themed",
        "lines": ["PART ONE", "DISCOVERY"],
        "colors": [(255, 200, 50), (255, 180, 30)],
    },
    {
        "id": "SD-02", "file": "Dividers/divider_act2_chaos.png",
        "prompt": "Decorative section divider banner for a children's book, curved magenta banner with dynamic white lightning bolts and blue pixel fragments, left icon of yellow lightning bolt, right icon of black traffic light, warm golden-yellow gradient background, glitch effects, no text, no letters, no words, futuristic digital high-tech style",
        "lines": ["PART TWO", "THE GLITCH WAVE"],
        "colors": [(255, 220, 50), (255, 200, 30)],
    },
    {
        "id": "SD-03", "file": "Dividers/divider_act3_gridlord.png",
        "prompt": "Decorative section divider banner for a children's book, dark purple-to-blue gradient background, pixelated golden crown icon on the left, retro CRT monitor with green grid on the right, floating pixelated cubes and gems in blue and purple, binary code border pattern, 8-bit pixel art style, no text, no letters, no words",
        "lines": ["PART THREE", "THE GRIDLORD"],
        "colors": [(255, 215, 0), (255, 200, 0)],
    },
    {
        "id": "SD-04", "file": "Dividers/divider_act4_mission.png",
        "prompt": "Decorative section divider banner for a children's book, horizontal banner with multicolored triangle border pattern, left side has a gear icon and paintbrush, right side has a game controller and paintbrush, cream yellow background, no text, no letters, no words, flat cartoon style, cheerful creative mood",
        "lines": ["PART FOUR", "MISSION NEONVILLE"],
        "colors": [(255, 200, 50), (255, 180, 30)],
    },
    {
        "id": "SD-05", "file": "Dividers/divider_act5_beginning.png",
        "prompt": "Decorative section divider banner for a children's book, warm orange gradient background, golden rectangular border, left side has large stylized sun with radiating rays and small astronaut below, right side has dark city skyline silhouette and pink heart icon and golden microphone, no text, no letters, no words, flat vector cartoon style",
        "lines": ["PART FIVE", "THE BEGINNING"],
        "colors": [(255, 215, 0), (255, 200, 0)],
    },
]

BLUEPRINTS = [
    {
        "id": "GB-01", "file": "Blueprints/bp_connector_key.png",
        "prompt": "Blueprint-style technical diagram on warm cream aged paper with decorative circuit-board border pattern, a strange homemade connector device in the center made from bent coat hanger wire forming a large top loop, a central cylindrical component, coiled wire around it, a spoon attached at the bottom, two small antenna protrusions, metallic bronze color, patent drawing style, no text, no labels, no words, no letters",
        "labels": [
            ("COAT HANGER", 0.50, 0.22),
            ("ANTENNA", 0.72, 0.18),
            ("SPEAKER", 0.50, 0.48),
            ("COILED WIRE", 0.28, 0.52),
            ("MAGNET", 0.72, 0.58),
            ("ANTENNA", 0.32, 0.72),
            ("SPOON BASE", 0.50, 0.82),
        ],
    },
    {
        "id": "GB-02", "file": "Blueprints/bp_pressure_valve.png",
        "prompt": "Blueprint-style technical diagram on warm cream aged paper, a steampunk pressure valve device in the center with a large copper cylindrical chamber with rounded top, a smaller secondary chamber with a pipe connecting them, a flexible corrugated hose, two large spoked wheels, blue liquid splash effects showing flow direction with arrows, hand-drawn vintage engineering sketch style, no text, no labels, no words, no letters",
        "labels": [
            ("FUSION CHAMBER", 0.50, 0.08),
            ("EXPANSION", 0.78, 0.28),
            ("WHEEL", 0.22, 0.45),
            ("CHAMBER", 0.78, 0.55),
            ("FLEXIBLE HOSE", 0.50, 0.42),
            ("PRESSURE", 0.30, 0.65),
            ("RELEASE VALVE", 0.50, 0.78),
        ],
    },
    {
        "id": "GB-03", "file": "Blueprints/bp_blip_internals.png",
        "prompt": "Blueprint-style technical diagram on warm cream aged paper showing the internal schematic of a cute white cube robot in the center, the robot has a cubic white body with a rectangular screen face showing two blue eyes and a red smile, three antennae on top, black arms and legs, walking pose, a small inset circuit board diagram to the side, no text, no labels, no words, no letters, cartoonish friendly style",
        "labels": [
            ("LED FACE", 0.50, 0.18),
            ("ANTENNA x3", 0.72, 0.12),
            ("SCREEN", 0.28, 0.32),
            ("CORE CHIP", 0.72, 0.42),
            ("SIGNAL PROCESSOR", 0.28, 0.58),
            ("MOTOR", 0.72, 0.65),
            ("BATTERY", 0.50, 0.82),
        ],
    },
    {
        "id": "GB-04", "file": "Blueprints/bp_bypass_device.png",
        "prompt": "Blueprint-style technical diagram on warm cream aged paper showing a small bypass device in the center with a prominent red circular button on top, a circular lens on the front, metallic brass body with screws, isometric 3D view, small circuit diagrams on the sides, hand-drawn sketchy style with cross-hatching, no text, no labels, no words, no letters",
        "labels": [
            ("BYPASS SWITCH", 0.50, 0.15),
            ("RED BUTTON", 0.72, 0.25),
            ("LENS", 0.28, 0.40),
            ("SERIAL PORT", 0.72, 0.50),
            ("BATTERY PACK", 0.28, 0.62),
            ("CIRCUIT", 0.72, 0.72),
            ("SCAVENGED PARTS", 0.50, 0.85),
        ],
    },
]

DOCUMENTS = [
    {
        "id": "DOC-01", "file": "Documents/doc_nexcorp_memo.png",
        "prompt": "A faded corporate memo document on slightly yellowed paper with coffee stains and creases, NEXCORP RESEARCH logo placeholder at top left, several lines of blank ruled lines for handwritten text, two red rectangular STAMP placeholders, a cute white cube robot with blue eyes standing in the center of the page, vintage document texture, no text, no letters, no words",
        "overlays": [
            ("NEXCORP RESEARCH", 30, 40, 0.45, (200, 150, 30), False),
            ("CONFIDENTIAL", 30, 320, 0.38, (40, 40, 180), True),
            ("DO NOT DISTRIBUTE", 30, 350, 0.30, (40, 40, 180), True),
            ("PROJECT BLIP", 30, 120, 0.35, (50, 50, 50), False),
            ("DATE: CLASSIFIED", 30, 155, 0.28, (80, 80, 80), False),
            ("APPROVED", 350, 380, 0.48, (40, 40, 180), True),
            ("URGENT", 300, 300, 0.42, (40, 40, 180), True),
        ],
    },
    {
        "id": "DOC-02", "file": "Documents/doc_gridlord_message.png",
        "prompt": "A computer monitor screen displaying a glitched message interface with dark background, the screen is on a wooden desk in a dimly lit room, purple and green color scheme, space for text lines, glitch effects and scan lines, no text, no letters, no words",
        "overlays": [
            ("HELP ME.", 140, 200, 0.60, (200, 80, 180), True),
            ("TRUST THEM.", 140, 260, 0.52, (200, 80, 180), True),
            ("THE SIGNAL.", 140, 320, 0.55, (80, 200, 80), True),
        ],
    },
    {
        "id": "DOC-03", "file": "Documents/doc_blip_diagnostic.png",
        "prompt": "A retro-style diagnostic screen with a white cube robot schematic in the center with system readouts around it, dark background with green grid lines, space for text readouts on sides, the robot schematic shows a cute boxy robot with blue eyes, no text, no letters, no words",
        "overlays": [
            ("SIGNAL ORIGIN: UNKNOWN", 20, 30, 0.30, (80, 200, 80), True),
            ("CORE STATUS: ACTIVE", 20, 60, 0.30, (80, 200, 80), True),
            ("94% FUNCTIONAL", 20, 90, 0.30, (80, 200, 80), True),
            ("0.7 BPS SIGNAL", 20, 440, 0.30, (80, 200, 80), True),
            ("DIAGNOSTIC COMPLETE", 20, 470, 0.30, (80, 200, 80), True),
            ("BLIP v1.0", 200, 500, 0.35, (80, 200, 80), True),
        ],
    },
    {
        "id": "DOC-04", "file": "Documents/doc_project_kira.png",
        "prompt": "A computer screen showing a classified document interface with a formal header area at top, a photograph placeholder in the center showing a scientist in lab coat, a faded laboratory scene in the background, warm sepia-toned lighting, browser chrome visible, no text, no letters, no words",
        "overlays": [
            ("PROJECT KIRA", 130, 60, 0.60, (60, 60, 60), True),
            ("CLASSIFIED", 175, 100, 0.48, (60, 60, 60), True),
            ("https://project-kira.net", 90, 30, 0.25, (100, 100, 100), False),
        ],
    },
]

MAPS = [
    {
        "id": "MAP-01", "file": "Maps/map_neonville.png",
        "prompt": "Illustrated children's book isometric map of a neighborhood with apartment buildings, houses, shops, a tall glass skyscraper, curving streets with cars, green parks with benches and trees, rolling hills in background, blue sky with clouds, compass rose in corner, warm earthy palette, cartoonish whimsical style, no text, no labels, no street names, no words, no letters",
        "overlays": [
            ("MAPLE STREET", 80, 90, 0.30, (255, 255, 255), True),
            ("NEONVILLE", 200, 30, 0.45, (255, 220, 100), True),
            ("MAIN STATION", 380, 350, 0.26, (255, 255, 255), True),
            ("VALLEY STREET", 500, 120, 0.26, (255, 255, 255), True),
            ("COMMUNITY CENTER", 350, 220, 0.24, (255, 255, 255), True),
            ("PARK", 150, 300, 0.28, (255, 255, 255), True),
        ],
    },
    {
        "id": "MAP-02", "file": "Maps/map_underground.png",
        "prompt": "Illustrated cross-section map showing an apartment building at the top with balconies and trees around it, and an underground tunnel system below carved into brown rocky earth with large silver pipes, multiple rooms with equipment inside, dim lighting from within the rooms, cartoon comic book style, warm surface vs cool underground contrast, no text, no labels, no room names, no words, no letters",
        "overlays": [
            ("WAGLE STREET", 200, 60, 0.35, (255, 255, 255), True),
            ("SECRET LAB", 250, 380, 0.32, (80, 80, 200), True),
            ("SERVER ROOM", 420, 380, 0.30, (255, 255, 255), True),
            ("TUNNEL EXIT", 480, 450, 0.26, (255, 255, 255), True),
            ("PIPES", 80, 300, 0.26, (180, 180, 180), True),
        ],
    },
]

print("=== SECTION DIVIDERS ===")
for d in DIVIDERS:
    s = seed_for(d["id"])
    print(f"\n{d['id']} seed={s}...", end=" ", flush=True)
    img = gen_img(d["prompt"], s, size=768)
    if img is None:
        print("FAILED")
        continue
    h, w = img.shape[:2]
    fs1 = int(w / 14)
    fs2 = int(w / 10)
    y1 = int(h * 0.15)
    y2 = int(h * 0.85)
    img = overlay_text_centered(
        img, d["lines"][0], y=y1, font_size=fs1, color=d["colors"][0],
        glow=True, stroke=True, shadow_blur=8, glow_alpha=0.3, stroke_width=2,
    )
    img = overlay_text_centered(
        img, d["lines"][1], y=y2, font_size=fs2, color=d["colors"][1],
        glow=True, stroke=True, shadow_blur=8, glow_alpha=0.3, stroke_width=2,
    )
    out = os.path.join(IMAGES_DIR, d["file"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cv2.imwrite(out, img)
    print(f"OK -> {out}")

print("\n\n=== GADGET BLUEPRINTS ===")
for bp in BLUEPRINTS:
    s = seed_for(bp["id"])
    print(f"\n{bp['id']} seed={s}...", end=" ", flush=True)
    img = gen_img(bp["prompt"], s, size=512)
    if img is None:
        print("FAILED")
        continue
    h, w = img.shape[:2]
    fs = max(14, int(w / 28))
    for label, rx, ry in bp["labels"]:
        lx = int(rx * w)
        ly = int(ry * h)
        img = overlay_label(
            img, label, lx, ly, font_size=fs, color=(60, 30, 10),
        )
    out = os.path.join(IMAGES_DIR, bp["file"])
    cv2.imwrite(out, img)
    print(f"OK -> {out}")

print("\n\n=== DOCUMENTS ===")
for doc in DOCUMENTS:
    s = seed_for(doc["id"])
    print(f"\n{doc['id']} seed={s}...", end=" ", flush=True)
    img = gen_img(doc["prompt"], s, size=512)
    if img is None:
        print("FAILED")
        continue
    h, w = img.shape[:2]
    for text, px, py, rel_fs, color, use_glow in doc["overlays"]:
        fs = max(12, int(rel_fs * w))
        img = overlay_text(
            img, text, px, py, font_size=fs, color=color,
            font_path=FONT_ROUNDED, shadow=True, glow=use_glow,
            stroke=use_glow, glow_alpha=0.2 if use_glow else 0,
            shadow_blur=4, stroke_width=1 if use_glow else 0,
        )
    out = os.path.join(IMAGES_DIR, doc["file"])
    cv2.imwrite(out, img)
    print(f"OK -> {out}")

print("\n\n=== MAPS ===")
for mp in MAPS:
    s = seed_for(mp["id"])
    print(f"\n{mp['id']} seed={s}...", end=" ", flush=True)
    img = gen_img(mp["prompt"], s, size=768)
    if img is None:
        print("FAILED")
        continue
    for text, px, py, rel_fs, color, use_glow in mp["overlays"]:
        h, w = img.shape[:2]
        fs = max(14, int(rel_fs * w))
        img = overlay_text(
            img, text, px, py, font_size=fs, color=color,
            font_path=FONT_ROUNDED, shadow=True, glow=use_glow,
            stroke=True, glow_alpha=0.25, shadow_blur=5,
            stroke_width=1,
        )
    out = os.path.join(IMAGES_DIR, mp["file"])
    cv2.imwrite(out, img)
    print(f"OK -> {out}")

print("\n\nALL DONE!")

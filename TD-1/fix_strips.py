import json, hashlib, requests, os, sys, time
import numpy as np

try:
    import cv2
except ImportError:
    print("Installing opencv-python...")
    os.system(f"{sys.executable} -m pip install opencv-python-headless")
    import cv2

MANIFEST = r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json"
IMAGES_DIR = r"D:\Kapil\Books\TD-1\Images\Strips"
SERVER = "http://192.168.29.7:8765"
TEMP_DIR = r"E:\Temp\kilo\strip_panels"
os.makedirs(TEMP_DIR, exist_ok=True)

m = json.load(open(MANIFEST, "r", encoding="utf-8"))

STRIP_PANEL_PROMPTS = {
    "B1-S01": [
        "A brown-haired Indian girl inventor holding a backpack that is crumpling itself into a ball, funny expression, workshop background, cel-shaded cartoon style",
        "A brown-haired Indian girl holding a music toothbrush that is playing wrong notes with musical notes floating away, puzzled expression, bathroom mirror, cel-shaded cartoon style",
        "A small white cube robot with blue eyes and red smile telling a joke with a question mark on its screen, confused audience, cel-shaded cartoon style",
        "A self-stirring soup pot overflowing with soup splashing everywhere in a kitchen, spoon flying out, chaotic scene, cel-shaded cartoon style",
    ],
    "B1-S03": [
        "A traffic light at intersection showing all three colors at once with cars confused and stopped below, glitch effects, cel-shaded cartoon style",
        "Indoor sprinklers spraying water everywhere inside a house with a wet orange cat looking annoyed, cel-shaded cartoon style",
        "A digital photo frame on wall showing a funny cat meme instead of family photo, glitch pixels around edges, cel-shaded cartoon style",
        "A delivery drone spinning out of control with packages falling from the sky, cel-shaded cartoon style",
        "A smart doorbell device on wall playing polka music with colorful musical notes, cel-shaded cartoon style",
        "A boy looking out his window in shock at all the chaos outside, eyes wide, cel-shaded cartoon style",
    ],
    "B1-S05": [
        "Through a camera viewfinder, glitching traffic lights at an intersection, lens framing effect, cel-shaded cartoon style",
        "Through a camera viewfinder, indoor sprinklers spraying through a window, lens framing effect, cel-shaded cartoon style",
        "Through a camera viewfinder, a confused dog wearing an LED collar blinking different colors, lens framing effect, cel-shaded cartoon style",
        "Through a camera viewfinder, a delivery drone spinning with packages falling, lens framing effect, cel-shaded cartoon style",
        "Through a camera viewfinder, a trail of colored lights leading to a mysterious building at night, lens framing effect, cel-shaded cartoon style",
    ],
    "B1-S07": [
        "An Indian girl with brown hair and olive green vest looking with wide fascinated eyes at a small white cube robot with blue glowing eyes, cel-shaded cartoon style",
        "A Mexican-American boy with navy blue beanie analyzing a small white cube robot with a tablet device, curious expression, cel-shaded cartoon style",
        "A Nigerian-British girl with camera and blue denim jacket photographing a small white cube robot with blue eyes, excited expression, cel-shaded cartoon style",
        "A Japanese-Korean boy with red fingerless gaming gloves poking a small white cube robot cautiously, nervous expression, cel-shaded cartoon style",
    ],
    "B1-S08": [
        "A small white cube robot with blue eyes sending a data packet to a boy with a tablet, digital sparkles between them, cel-shaded cartoon style",
        "A small white cube robot displaying a pixel art smiley face on its screen for a girl with a camera, warm expression, cel-shaded cartoon style",
        "A small white cube robot showing a game controller icon on its screen for a boy with red gaming gloves, cheerful scene, cel-shaded cartoon style",
        "A small white cube robot displaying a question mark on its screen for an Indian girl with goggles and vest, curious moment, cel-shaded cartoon style",
    ],
    "B1-S09": [
        "A girl artist with brown hair staring at abstract symbols on a computer screen, focused expression, desk with art supplies, cel-shaded cartoon style",
        "A girl artist with brown hair sketching abstract symbols separately in a notebook with colored pens, concentrated, cel-shaded cartoon style",
        "A girl artist rearranging cut-out abstract symbols by shape on a table, artistic workspace, cel-shaded cartoon style",
        "A girl artist connecting lines between abstract symbols on paper with a pen, discovery moment, cel-shaded cartoon style",
        "The final connected shape revealed as a connector plug drawn on paper, girl looking satisfied, cel-shaded cartoon style",
    ],
    "B1-S13": [
        "A traffic light intersection with cars stopped and lights malfunctioning, city street scene, cel-shaded cartoon style",
        "A library interior with scrambled holographic displays and glitchy floating text, books on shelves, cel-shaded cartoon style",
        "A community center with distorted AR art projections on walls, warped colorful images, cel-shaded cartoon style",
        "A park garden flooding with water from broken sprinklers, puddles everywhere, cel-shaded cartoon style",
    ],
    "B1-S14": [
        "A boy with red fingerless gaming gloves sprinting toward a traffic light pole at night, determined expression, cel-shaded cartoon style",
        "A boy with red fingerless gaming gloves jumping onto the base of a traffic light pole, action pose, cel-shaded cartoon style",
        "A boy with red fingerless gaming gloves climbing a traffic light pole hand over hand, looking up, cel-shaded cartoon style",
        "A boy with red fingerless gaming gloves attaching a small bypass device to a traffic light, white flash effect, cel-shaded cartoon style",
        "A boy with red fingerless gaming gloves sliding down a traffic light pole triumphantly with fist raised, cel-shaded cartoon style",
    ],
    "B1-S17": [
        "A map of a city with hundreds of red glowing dots scattered across it, ominous digital display, cel-shaded cartoon style",
        "Four kids looking concerned at a large screen showing the scale of the red dots, worried expressions, cel-shaded cartoon style",
        "A small white cube robot recognizing patterns inside itself, blue screen flickering, introspective moment, cel-shaded cartoon style",
        "Close-up of a small white cube robot with a sad expression on its blue screen face, single tear pixel, cel-shaded cartoon style",
    ],
    "B1-S18": [
        "A cable connecting a small white cube robot to a server rack, blue data flowing through cable, cel-shaded cartoon style",
        "A small white cube robot screen flickering between multiple bright colors, transition effect, cel-shaded cartoon style",
        "A small white cube robot body glowing brighter with energy, light radiating outward, cel-shaded cartoon style",
        "A small white cube robot screen going completely blank and dark, scary moment, cel-shaded cartoon style",
        "A single tiny pixel of blue light appearing on a dark robot screen, hope moment, cel-shaded cartoon style",
        "A small white cube robot with a big happy face and version 1.0 text display, celebration moment, cel-shaded cartoon style",
    ],
    "B1-S19": [
        "An Indian girl with green vest organizing tools on a pegboard wall in an underground lab, workshop setting, cel-shaded cartoon style",
        "A boy with navy blue beanie setting up computer monitors and terminal on a desk in underground lab, tech setup, cel-shaded cartoon style",
        "A Nigerian-British girl with denim jacket painting a mural of a city skyline on an underground wall, artistic moment, cel-shaded cartoon style",
        "A Japanese-Korean boy carrying a mini-fridge through an underground tunnel, effort expression, cel-shaded cartoon style",
        "A small white cube robot sitting on a custom charging dock with warm string lights around it, cozy headquarters, cel-shaded cartoon style",
    ],
    "B1-S25": [
        "Static noise on a screen slowly forming into a vague face shape, digital corruption, cel-shaded cartoon style",
        "A screen showing broken corrupted text that reads HELP in glitchy letters, green and purple, cel-shaded cartoon style",
        "A robot screen face dissolving into digital noise and static, distress, cel-shaded cartoon style",
        "A robot screen face reforming with clearer eyes looking sad and pleading, emotional moment, cel-shaded cartoon style",
    ],
    "B1-S27": [
        "A small white cube robot with scared red face when connected to a server rack, fear expression, cel-shaded cartoon style",
        "A small white cube robot screen flickering rapidly between many colors, transition effect, cel-shaded cartoon style",
        "A small white cube robot screen going completely blank and dark, scary moment, cel-shaded cartoon style",
        "A single tiny pixel of blue light appearing on a dark robot screen, hope returning, cel-shaded cartoon style",
        "A small white cube robot with a big happy face and version 1.0 display, joyful moment, cel-shaded cartoon style",
    ],
}

def gen_panel(prompt, seed, size=256):
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
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return img
    return None

def stitch_panels(panels, gap=4):
    h, w = panels[0].shape[:2]
    gap_color = np.full((h, gap, 3), [40, 40, 40], dtype=np.uint8)
    result = panels[0]
    for p in panels[1:]:
        result = np.hstack([result, gap_color, p])
    return result

total = sum(len(v) for v in STRIP_PANEL_PROMPTS.values())
done = 0

for strip_id, panel_prompts in STRIP_PANEL_PROMPTS.items():
    print(f"\n=== {strip_id} ({len(panel_prompts)} panels) ===")
    
    panels = []
    for pi, prompt in enumerate(panel_prompts):
        seed = int(hashlib.md5(f"{strip_id}_panel_{pi}_v2".encode()).hexdigest()[:8], 16) % 2147483647
        print(f"  Panel {pi+1} seed={seed}...", end=" ", flush=True)
        
        for attempt in range(2):
            img = gen_panel(prompt, seed if attempt == 0 else seed + attempt * 1000)
            if img is not None:
                panels.append(img)
                print(f"OK ({img.shape[1]}x{img.shape[0]})")
                done += 1
                break
            print(f"RETRY...", end=" ", flush=True)
        else:
            print("FAILED")
    
    if len(panels) == len(panel_prompts):
        stitched = stitch_panels(panels)
        out_path = os.path.join(IMAGES_DIR, f"{strip_id.lower().replace('-','_')}_stitched.png")
        # Find the original filename from manifest
        for s in m["strips"]:
            if s["id"] == strip_id:
                out_path = os.path.join(IMAGES_DIR, s["file"])
                break
        cv2.imwrite(out_path, stitched)
        print(f"  -> Stitched {len(panels)} panels -> {out_path} ({stitched.shape[1]}x{stitched.shape[0]})")
    else:
        print(f"  INCOMPLETE: got {len(panels)}/{len(panel_prompts)} panels")

print(f"\nDone! Generated {done}/{total} panels for {len(STRIP_PANEL_PROMPTS)} strips")

import json, hashlib, requests, time, os, sys

MANIFEST = r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json"
IMAGES_DIR = r"D:\Kapil\Books\TD-1\Images"
SERVER = "http://192.168.29.7:8765"
CATEGORY_DIRS = {
    "title_page": "",
    "extra_spots": "Spots",
    "strips": "Strips",
}

m = json.load(open(MANIFEST, "r", encoding="utf-8"))

FIXES = {
    "TP-01": "Title page illustration for a children's chapter book titled THE GLITCH SQUAD in large bold playful yellow letters at the top, five diverse pre-teen kids standing together on a rooftop at night facing a glittering city skyline with lit windows and neon signs, a small cute white cube robot with blue glowing eyes floating above them, starry deep blue sky with orange horizon, vibrant cel-shaded 2D illustration style with bold outlines and bright candy colors",
    "ES-15": "A canvas painting on an easel showing an abstract city scene with beautiful glitch-art pixel overlays appearing on the painting as if it is coming alive with digital energy, colorful paint mixing with digital pixel squares in green and purple, warm golden gallery lighting, the painting transforming from analog to digital before your eyes",
    "ES-16": "A park garden with multiple water sprinklers broken and gushing dramatically in chaotic spray patterns shooting water high into the air, rainbows forming in the mist between the water sprays, wet grass and puddles on ground, trees and park benches visible, chaotic fun water scene, bright warm daylight with lens flare",
}

def get_output_path(item):
    f = item["file"]
    arr = item["_array"]
    d = CATEGORY_DIRS.get(arr, "")
    if "/" in f or "\\" in f:
        return os.path.join(IMAGES_DIR, f)
    if d:
        return os.path.join(IMAGES_DIR, d, f)
    return os.path.join(IMAGES_DIR, f)

def gen_one(item, seed=None, prompt_override=None):
    prompt = prompt_override or item["prompt"]
    if seed is None:
        seed = int(hashlib.md5(item["id"].encode()).hexdigest()[:8], 16) % 2147483647
    payload = {
        "prompt": prompt,
        "negative_prompt": "",
        "width": item.get("size", 512),
        "height": item.get("size", 512),
        "seed": seed,
        "guidance_scale": 3.5,
        "num_inference_steps": 28,
    }
    r = requests.post(f"{SERVER}/generate", json=payload, timeout=120)
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}"
    content_type = r.headers.get("content-type", "")
    out = get_output_path(item)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if "json" in content_type:
        data = r.json()
        if "image" not in data:
            return None, data.get("error", "no image key")
        img_bytes = base64.b64decode(data["image"])
        with open(out, "wb") as f:
            f.write(img_bytes)
    else:
        with open(out, "wb") as f:
            f.write(r.content)
    return out, None

# Find items to fix
items_to_fix = []
for arr_name in ["title_page", "extra_spots"]:
    for s in m[arr_name]:
        if s["id"] in FIXES:
            items_to_fix.append(s)

if not items_to_fix:
    print("No items to fix found in manifest")
    sys.exit(1)

print(f"Fixing {len(items_to_fix)} items with new prompts + new seeds...")

for item in items_to_fix:
    fid = item["id"]
    new_prompt = FIXES[fid]
    print(f"\n--- {fid} ---")
    print(f"  File: {item['file']}")
    print(f"  New prompt: {new_prompt[:100]}...")
    
    # Try up to 3 seeds
    for attempt in range(3):
        seed = int(hashlib.md5(f"{fid}_fix_v2_{attempt}".encode()).hexdigest()[:8], 16) % 2147483647
        print(f"  Attempt {attempt+1}, seed={seed}...", end=" ", flush=True)
        try:
            path, err = gen_one(item, seed=seed, prompt_override=new_prompt)
            if err:
                print(f"ERROR: {err}")
                continue
            print(f"OK -> {path}")
            break
        except Exception as e:
            print(f"EXCEPTION: {e}")
            time.sleep(2)

print("\nDone!")

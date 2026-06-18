import requests, os, hashlib

SERVER = "http://192.168.29.7:8765"
OUT_DIR = r"E:\Temp\kilo"

# Generate title page WITHOUT text - just the scene
PROMPT = (
    "Epic children's book illustration, five diverse pre-teen kids standing together "
    "on a rooftop at night facing a glittering city skyline with lit windows and neon signs, "
    "Indian girl with goggles and olive green utility vest in center, "
    "Mexican-American boy with navy blue beanie and tablet to the left, "
    "Nigerian-British girl with blue denim jacket and camera to the right, "
    "Japanese-Korean boy with red fingerless gaming gloves, "
    "small cute white cube robot with blue glowing eyes floating above them, "
    "starry deep blue sky with orange horizon, "
    "vibrant cel-shaded 2D illustration style with bold outlines and bright candy colors, "
    "no text, no letters, no words"
)

os.makedirs(OUT_DIR, exist_ok=True)

for i in range(4):
    seed = int(hashlib.md5(f"TP01_notext_{i}".encode()).hexdigest()[:8], 16) % 2147483647
    print(f"Seed {seed}...", end=" ", flush=True)
    try:
        r = requests.post(f"{SERVER}/generate", json={
            "prompt": PROMPT,
            "negative_prompt": "",
            "width": 768,
            "height": 512,
            "seed": seed,
            "guidance_scale": 3.5,
            "num_inference_steps": 28,
        }, timeout=120)
        if r.status_code == 200:
            tmp = os.path.join(OUT_DIR, f"tp01_notext_{seed}.png")
            with open(tmp, "wb") as f:
                f.write(r.content)
            print(f"OK -> {tmp}")
        else:
            print(f"FAIL HTTP {r.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

print("Done!")

import sys
sys.path.insert(0, r"D:\Kapil\Books\TD-1")
import json, pathlib, random, time
from manifest_batch_client import (
    build_full_prompt, detect_characters, parse_size,
    STEPS_BY_TYPE, OUTPUT_DIR, generate_one
)

SERVER = "http://192.168.29.7:8765"
MAX_TRIES = 8

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text("utf-8"))

item_id = sys.argv[1]
target_count = int(sys.argv[2]) if len(sys.argv) > 2 else 4

item = None
for arr in ["illustrations"]:
    for x in m.get(arr, []):
        if x.get("id") == item_id:
            item = x
            break

if not item:
    print(f"Item {item_id} not found")
    sys.exit(1)

raw = item["prompt"]
chars = detect_characters(raw)
full = build_full_prompt(raw)
w, h = parse_size(item.get("size", 1024))
steps = STEPS_BY_TYPE.get(item.get("type", ""), 10)
out_path = OUTPUT_DIR / item["file"]

for attempt in range(MAX_TRIES):
    seed = random.randint(100000, 2147483647)
    print(f"Attempt {attempt+1}/{MAX_TRIES} seed={seed}")
    
    png_bytes = generate_one(SERVER, full, w, h, steps, seed, retries=2, max_seq=1024)
    if not png_bytes or len(png_bytes) < 1000:
        print(f"  Generation failed")
        time.sleep(2)
        continue
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(png_bytes)
    
    print(f"  Generated {len(png_bytes)//1024}KB - saved to {out_path.name}")
    print(f"  CHECK WITH MCP - if wrong, will retry")
    print(f"  SEED_USED={seed}")
    break

item["seed_override"] = seed
item["status"] = "generated"
p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")

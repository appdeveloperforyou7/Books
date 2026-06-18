import sys, json, pathlib, base64, hashlib, time
from urllib.request import Request, urlopen

sys.path.insert(0, r"D:\Kapil\Books\TD-1")
from manifest_batch_client import (
    build_full_prompt, detect_characters, parse_size,
    STEPS_BY_TYPE, OUTPUT_DIR, generate_one
)

SERVER = "http://192.168.29.7:8765"
item_id = sys.argv[1]

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text("utf-8"))
item = None
for arr_name in ["illustrations", "strips", "blip_marginalia_images", "chapter_vignettes",
                  "character_cards", "maps", "gadget_blueprints", "title_page",
                  "section_dividers", "glitch_art", "extra_spots", "documents", "endpapers"]:
    for x in m.get(arr_name, []):
        if x.get("id") == item_id:
            item = x
            break
    if item:
        break

if not item:
    print(f"Item {item_id} not found")
    sys.exit(1)

raw = item["prompt"]
chars = detect_characters(raw)
full = build_full_prompt(raw)
w, h = parse_size(item.get("size", 1024))
steps = STEPS_BY_TYPE.get(item.get("type", ""), 10)
seed = item.get("seed_override") or (int(hashlib.md5(item["id"].encode()).hexdigest()[:8], 16) % 2147483647 if chars else 0)

print(f"Generating {item_id}: {item['file']} ({w}x{h}, steps={steps}, seed={seed})")
print(f"Chars: {chars}")

out_path = OUTPUT_DIR / item["file"]
out_path.parent.mkdir(parents=True, exist_ok=True)

png_bytes = generate_one(SERVER, full, w, h, steps, seed, retries=3, max_seq=1024)

if png_bytes and len(png_bytes) > 1000:
    out_path.write_bytes(png_bytes)
    print(f"OK: {out_path} ({len(png_bytes)//1024} KB)")
    item["status"] = "generated"
    p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
else:
    print(f"FAILED: {item_id}")
    item["status"] = "failed"
    p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")

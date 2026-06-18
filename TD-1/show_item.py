import sys
sys.path.insert(0, r"D:\Kapil\Books\TD-1")
import json, pathlib, base64, hashlib
from manifest_batch_client import (
    build_full_prompt, detect_characters, parse_size,
    STEPS_BY_TYPE, OUTPUT_DIR, compute_seed
)

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text("utf-8"))
item = [x for x in m["illustrations"] if x["id"] == sys.argv[1]][0]

raw = item["prompt"]
chars = detect_characters(raw)
full = build_full_prompt(raw)
w, h = parse_size(item.get("size", 1024))
steps = STEPS_BY_TYPE.get(item.get("type", ""), 10)
seed = int(hashlib.md5(item["id"].encode()).hexdigest()[:8], 16) % 2147483647 if chars else 0

print(f"ID: {item['id']}")
print(f"File: {item['file']}")
print(f"Type: {item['type']}")
print(f"Size: {w}x{h}")
print(f"Steps: {steps}")
print(f"Chars: {chars}")
print(f"Seed: {seed}")
print(f"Raw prompt: {raw}")
print(f"Full prompt ({len(full)} chars): {full[:300]}...")

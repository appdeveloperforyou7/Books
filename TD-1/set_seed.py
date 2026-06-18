import json
import pathlib
import random
import hashlib

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text("utf-8"))

for item in m["illustrations"]:
    if item["id"] == "B1-033":
        new_seed = random.randint(100000, 2147483647)
        item["seed_override"] = new_seed
        print(f"Set seed to {new_seed}")
        break

p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")

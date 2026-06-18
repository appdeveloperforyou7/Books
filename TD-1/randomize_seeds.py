import json
import pathlib
import random

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text("utf-8"))

seeds = {}
for item in m["illustrations"]:
    if item["id"] in ["B1-011","B1-012","B1-017","B1-018","B1-019","B1-021","B1-023","B1-029"]:
        s = random.randint(100000, 2147483647)
        item["seed_override"] = s
        item["status"] = "pending"
        seeds[item["id"]] = s

p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
for k, v in seeds.items():
    print(f"  {k}: seed={v}")

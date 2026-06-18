import json
import re
import pathlib

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text(encoding="utf-8"))

fixed = 0
for arr_name in ["documents", "endpapers", "extra_spots"]:
    for item in m.get(arr_name, []):
        if item.get("status") == "generated":
            continue
        raw = item.get("prompt", "")
        match = re.search(r"Scene:\s*(.+?)\.\s*(?:THE LOCATION|Blip is)", raw)
        if match:
            clean = match.group(1).strip()
            if len(clean) > 30:
                item["prompt"] = clean
                fixed += 1
                print(f"  Fixed {item['id']}: {clean[:80]}...")
            else:
                print(f"  SKIP {item['id']}: too short ({len(clean)})")
        else:
            print(f"  WARN {item['id']}: no match")

p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nFixed {fixed} prompts")

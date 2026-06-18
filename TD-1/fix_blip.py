import json
import pathlib

BLIP_FIX = "one small white boxy robot with rectangular head, square screen face with thin dark border, large bright blue LED eyes with pixel pattern, dark red curved smile, two white rounded antennas, two short arms with black joints, two legs with black joints, walks on feet"

MULTI_IDS = ["B1-011","B1-012","B1-017","B1-018","B1-019","B1-021","B1-023","B1-024","B1-033","B1-036"]

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text("utf-8"))

updated = 0
for item in m["illustrations"]:
    if item["id"] in MULTI_IDS:
        old = item["prompt"]
        import re
        old = re.sub(r'One small white cube robot[^.]*\.?', f'{BLIP_FIX}.', old)
        old = re.sub(r'One white cube robot[^.]*\.?', f'{BLIP_FIX}.', old)
        old = re.sub(r'one white cube robot[^.]*\.?', f'{BLIP_FIX}.', old)
        item["prompt"] = old
        updated += 1
        print(f"  Updated {item['id']}")

p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nUpdated {updated} prompts with corrected Blip description")

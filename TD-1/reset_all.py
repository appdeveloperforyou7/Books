import json
import pathlib

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text(encoding="utf-8"))

reset = 0
for key in list(m.keys()):
    val = m[key]
    if isinstance(val, list):
        for item in val:
            if isinstance(item, dict) and item.get("status") == "generated":
                if item.get("file") and item["file"].endswith(".png"):
                    item["status"] = "pending"
                    reset += 1

p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Reset {reset} items to pending status")

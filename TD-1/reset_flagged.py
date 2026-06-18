import json
import pathlib

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text(encoding="utf-8"))

FLAGGED = {
    "B1-004", "B1-005", "B1-006", "B1-007", "B1-009", "B1-010",
    "B1-011", "B1-012", "B1-017", "B1-018", "B1-019", "B1-021",
    "B1-023", "B1-024", "B1-025", "B1-029", "B1-033", "B1-035",
}

reset = 0
for item in m["illustrations"]:
    if item["id"] in FLAGGED and item.get("status") == "generated":
        item["status"] = "pending"
        reset += 1
        print(f"  Reset {item['id']}: {item['file']}")

p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nReset {reset} items to pending")

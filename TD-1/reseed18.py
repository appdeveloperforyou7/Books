import json, pathlib, random
p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text("utf-8"))
for item in m["illustrations"]:
    if item["id"] == "B1-018":
        s = random.randint(100000, 2147483647)
        item["seed_override"] = s
        print("B1-018: " + str(s))
p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")

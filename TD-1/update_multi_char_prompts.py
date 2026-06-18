import json
import pathlib

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text("utf-8"))

MULTI_CHAR = {
    "B1-017": "Four children sitting in a circle on living room floor. From left: a brown-skinned girl with ponytail and green utility vest, a tan-skinned boy with beanie and glasses in gray hoodie, a dark-skinned girl with curly hair and yellow bag, a light-skinned boy with spiky hair and red fingerless gloves. One small white cube robot floating above them. Notebooks and gadgets on floor between them. Building a strange device from bent wire and magnets. No other people.",

    "B1-018": "Four children standing at a dark tunnel entrance behind a basement wall. From left: a brown-skinned girl with ponytail goggles and green vest holding flashlight, a tan-skinned boy with beanie and glasses peering into darkness, a dark-skinned girl with curly hair and yellow bag looking nervous, a light-skinned boy with spiky hair and red gloves leading the way. One small white cube robot hovering near flashlight beam. Dusty narrow space with cables along walls. No other people.",

    "B1-019": "Four children celebrating excitedly around an underground lab workbench. From left: a brown-skinned girl with ponytail and green vest jumping with joy, a tan-skinned boy with beanie and glasses pumping fist in air, a dark-skinned girl with curly hair clapping enthusiastically, a light-skinned boy with spiky hair and red gloves cheering loudly. One small white cube robot with happy glowing face floating above. Device connected to terminal. No other people.",

    "B1-021": "Four children sitting on bedroom floor at midnight sharing samosas. From left: a brown-skinned girl with ponytail and green vest eating a samosa, a tan-skinned boy with beanie and glasses whispering excitedly, a dark-skinned girl with curly hair and yellow bag reaching for another samosa, a light-skinned boy with spiky hair and red gloves stuffing his face. One small white cube robot watching curiously nearby. Moonlight through window. Plate of samosas between them. No other children.",

    "B1-023": "Four children on a park bench in morning sunshine sharing breakfast. From left: a brown-skinned girl with ponytail and green vest holding a cup, a tan-skinned boy with beanie and glasses eating from a bowl, a dark-skinned girl with curly hair and denim jacket holding a plate, a light-skinned boy with spiky hair and red gloves with a snack. One small white cube robot hovering nearby. Dappled light through leafy trees. No other people on the bench.",

    "B1-024": "Four children walking cautiously through narrow underground tunnel. From left: a brown-skinned girl with ponytail goggles and green vest in front, a tan-skinned boy with beanie and glasses scanning walls with tablet, a dark-skinned girl with curly hair and yellow bag in middle, a light-skinned boy with spiky hair and red gloves at rear. Brick walls with bundled cables along ceiling. Flashlights cutting through dust. No other people in the tunnel.",

    "B1-033": "Four children in their cozy underground lab headquarters. From left: a brown-skinned girl with ponytail goggles and green vest at workbench, a tan-skinned boy with beanie and glasses studying monitor, a dark-skinned girl with curly hair and yellow bag sketching at desk, a light-skinned boy with spiky hair and red gloves testing gadget. One small white cube robot on charging dock. String lights across ceiling. Monitors and blueprints. Secret base atmosphere. No other people.",

    "B1-035": "One dark-skinned girl with curly black hair and denim jacket pinning a photograph to a cork investigation board. Red string connecting pinned photos. Newspaper clippings about glitches. A small holographic logo glowing nearby. Solo detective moment. No other people in the room.",

    "B1-029": "One brown-skinned girl with ponytail goggles and green utility vest operating a makeshift water valve. Water spraying everywhere from sprinklers. Rainbows in the mist. Determined action pose. Solo action scene. No other people visible anywhere.",
}

updated = 0
for item in m["illustrations"]:
    if item["id"] in MULTI_CHAR:
        item["prompt"] = MULTI_CHAR[item["id"]]
        updated += 1
        print(f"Updated {item['id']}")

p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nUpdated {updated} prompts")

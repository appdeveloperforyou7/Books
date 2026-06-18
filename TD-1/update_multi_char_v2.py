import json
import pathlib

MAYA = "an 11-year-old Indian girl with warm brown skin, dark brown thick messy ponytail with a pencil stuck in it, safety goggles on forehead, olive green utility vest full of tool pockets, faded red rocket t-shirt, cargo shorts"
LEO = "an 11-year-old Mexican-American boy with warm tan golden-brown skin, black fade haircut, navy blue beanie with pixel heart patch, reading glasses, gray hoodie with tablet, jeans with grass-stained knees"
ZARA = "a 12-year-old Nigerian-British girl with rich dark brown skin, voluminous black hair in chunky twists with colorful thread, bright yellow crossbody bag, denim jacket with patches and doodles, colorful patterned leggings"
SAM = "a 10-year-old Japanese-Korean boy with light-medium warm skin, black spiky messy hair gel-styled on top, bright red fingerless gaming gloves, black PLAYER 1 t-shirt, athletic shorts, LED sneakers"
BLIP = "one small white cube robot with front LED screen showing simple cyan smiley face, small antenna on top, floating on tiny hover thrusters"
AGE = "All children are pre-teens aged 10-12, not toddlers or babies. Each child looks distinctly different in skin tone, hair, and clothing."

MULTI_CHAR = {
    "B1-011": f"Exactly four pre-teen children sitting around a table in a bright meeting room. On the left is {MAYA}. Next to her is {LEO}. Across from them is {ZARA}. On the right is {SAM}. {BLIP} floats above the table center. Whiteboard with colorful diagrams on the wall behind them. Warm friendly first meeting. No other children or people. {AGE}",

    "B1-012": f"Exactly four pre-teen children crammed together hiding in a dark narrow janitor closet. On the left is {MAYA} pressing finger to lips shushing. Next is {LEO} crouching low with tablet. Then {ZARA} clutching her yellow bag nervously. On the right is {SAM} peeking through door crack with gloved hand. {BLIP} hovers near ceiling with dim face. Cleaning supplies on shelves. Single sliver of light under the door. No other people. {AGE}",

    "B1-017": f"Exactly four pre-teen children sitting in a tight circle on a living room rug, nobody standing. On the left is {MAYA}. Across is {LEO}. On the right is {ZARA}. At the bottom facing us is {SAM}. {BLIP} floats in the center of their circle. Wires and magnets and a small device between them on the floor. Living room with couch and bookshelf behind them. No other people in the room. {AGE}",

    "B1-018": f"Exactly four pre-teen children standing at a dark tunnel entrance behind a basement wall. Leading from the left is {MAYA} holding a flashlight beam forward. Behind her is {LEO} peering into darkness scanning walls. Next is {ZARA} looking nervous clutching her yellow bag. At the rear is {SAM} with red gloves ready to go. {BLIP} hovers near the flashlight beam. Dusty narrow space with cables along walls. No other people. {AGE}",

    "B1-019": f"Exactly four pre-teen children celebrating excitedly around an underground lab workbench. On the left {MAYA} is jumping with arms raised joyfully. Next to her {LEO} is pumping his fist in the air grinning. On the right {ZARA} is clapping with a huge smile. Beside her {SAM} is cheering with red-gloved hands up. {BLIP} floats above with a happy glowing face. Device connected to terminal on workbench. Only this one robot exists in the scene, no second robot. No other people. {AGE}",

    "B1-021": f"Exactly four pre-teen children sitting on bedroom floor at midnight sharing samosas from a plate between them. On the left {MAYA} is eating a samosa with gap-toothed grin. Next to her {LEO} is whispering excitedly. On the right {ZARA} is reaching for another samosa with her beaded bracelets jingling. Beside her {SAM} is stuffing his face with both gloved hands. {BLIP} watches curiously from nearby, the only robot. Moonlight through window. Cozy secret midnight feast. No other people. {AGE}",

    "B1-023": f"Exactly four pre-teen children sitting on a wooden park bench in morning sunshine sharing breakfast food. On the left {MAYA} holds a cup. Next {LEO} eats from a bowl with his glasses glinting. Then {ZARA} holds a plate with her denim jacket sleeves rolled up. On the right {SAM} gives a thumbs up with his red gaming glove. Dappled golden light through leafy trees above. Peaceful park morning. No other people on the bench, no robots. {AGE}",

    "B1-024": f"Exactly four pre-teen children walking in single file cautiously through a narrow underground tunnel with brick walls. Leading is {MAYA} with flashlight cutting through dust. Behind her {LEO} scans the walls with his tablet showing green code. Next {ZARA} walks carefully with her yellow bag close. At the rear {SAM} glances back with red-gloved hands ready. Bundled cables along the ceiling. Dim distant glow ahead. No other people in the tunnel, no robots. {AGE}",

    "B1-033": f"Exactly four pre-teen children in their cozy underground lab headquarters. On the left at the workbench is {MAYA} tinkering with circuits. At the monitor desk is {LEO} studying data on screen. At the art desk is {ZARA} sketching in her notebook. Testing a gadget on the right is {SAM} with his red gloves. {BLIP} sits on its charging dock, the only robot in the room. String lights across the ceiling. Monitors and blueprints everywhere. Secret base atmosphere. No other people. {AGE}",

    "B1-036": f"Exactly four pre-teen children sitting on the edge of an apartment rooftop at sunset looking at the glowing city skyline. On the left {MAYA} has wind in her ponytail and goggles around her neck. Next {LEO} has his beanie pulled down watching the horizon. Then {ZARA} is taking a photo with her phone in her yellow bag. On the right {SAM} is leaning back on his red-gloved hands with LED sneakers dangling over the edge. {BLIP} floats between them with a peaceful smile face, the only robot. Golden hour warm light. No other people on the rooftop. {AGE}",

    "B1-035": f"One single 12-year-old Nigerian-British girl with rich dark brown skin, voluminous black hair in chunky twists with colorful thread, bright yellow crossbody bag, oversized denim jacket with patches and doodles, colorful patterned leggings. She is pinning a photograph to a cork investigation board. Red string connecting pinned photos. Newspaper clippings about glitches. A small holographic logo glowing nearby. Solo detective moment. No other people in the room. She is a pre-teen, not a toddler.",

    "B1-029": f"One single 11-year-old Indian girl with warm brown skin, dark brown thick messy ponytail with pencil in it, safety goggles on forehead, olive green utility vest, faded red rocket t-shirt, cargo shorts. She is operating a makeshift water valve at a park sprinkler. Water spraying everywhere creating rainbows in the mist. Determined action pose. Solo scene with no other people visible anywhere, not even in the background. She is a pre-teen, not a toddler.",
}

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text("utf-8"))

updated = 0
for item in m["illustrations"]:
    if item["id"] in MULTI_CHAR:
        item["prompt"] = MULTI_CHAR[item["id"]]
        item["status"] = "pending"
        updated += 1
        print(f"  Updated {item['id']}")

p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nUpdated {updated} multi-character prompts with full inline descriptions")

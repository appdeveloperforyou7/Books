import json
import pathlib

SAM = "a 10-year-old Japanese-Korean boy with light-medium warm skin, black spiky messy hair gel-styled pointy on top and shaved close on sides, bright red fingerless gaming gloves on both hands (the only child wearing gloves), black t-shirt with PLAYER printed on it, athletic shorts with side stripes, high-top sneakers with glowing LED lights in the soles"
MAYA = "an 11-year-old Indian girl with warm brown skin, dark brown thick messy ponytail with a pencil stuck in it and escaped strands, safety goggles pushed up on forehead, oversized olive green utility vest with many pockets full of tools, faded red rocket ship t-shirt underneath, cargo shorts, bare hands with no gloves"
LEO = "an 11-year-old Mexican-American boy with warm tan golden-brown skin, compact build, black thick slightly grown-out fade haircut under a navy blue knit beanie with a small pixelated heart patch sewn on it, very dark intense eyes, reading glasses, oversized gray hoodie with sleeves over hands and a tablet in the front pocket, dark t-shirt underneath, jeans with grass-stained knees, bare hands with no gloves"
ZARA = "a 12-year-old Nigerian-British girl with rich dark brown skin, tall long-limbed graceful build, voluminous black natural hair in chunky twists with colorful thread woven through, bright expressive dark brown eyes, bright yellow crossbody bag covered in enamel pins, oversized denim jacket with patches and doodles on the sleeves, colorful patterned leggings, bare hands with no gloves"
BLIP = "one single small white cube robot with a front LED screen showing a simple cyan smiley face, small antenna on top that wiggles, floating on tiny hover thrusters, the only robot in the scene"
AGE = "All children are pre-teens aged 10 to 12 years old, not toddlers or babies. Sam is the only child wearing red gloves, all other children have bare hands."

MULTI = {
    "B1-011": f"Exactly four pre-teen children aged 10-12 sitting around a table in a bright meeting room, no other people. On the left is {MAYA}. Next to her is {SAM}. Across from them is {ZARA}. On the right is {LEO} with his tablet showing green code on screen. {BLIP} floats above the table center. Whiteboard with colorful diagrams on the wall. {AGE}",

    "B1-012": f"Exactly four pre-teen children aged 10-12 crammed together hiding in a dark narrow janitor closet, no other people. On the left is {MAYA} pressing finger to lips shushing. Next to her is {SAM} peeking through the door crack. Then {ZARA} clutching her yellow bag nervously. On the right is {LEO} crouching low with his tablet. {BLIP} hovers near the ceiling. Cleaning supplies on shelves. Single sliver of light under the door. {AGE}",

    "B1-017": f"Exactly four pre-teen children aged 10-12 sitting in a tight circle on a living room rug, nobody standing. Facing us at the bottom is {SAM}. On the left is {MAYA}. Across is {LEO} with tablet beside him. On the right is {ZARA} with her yellow bag. {BLIP} floats in the center of their circle. Wires and magnets and a small device between them. Living room with couch and bookshelf. {AGE}",

    "B1-018": f"Exactly four pre-teen children aged 10-12 at a dark tunnel entrance, no other people. Leading from the left is {MAYA} holding a flashlight. Behind her is {SAM} with red-gloved hands ready. Next is {ZARA} with yellow bag clutched close. At the rear is {LEO} scanning walls with his tablet. {BLIP} hovers near the flashlight beam. Brick walls with bundled cables. {AGE}",

    "B1-019": f"Exactly four pre-teen children aged 10-12 celebrating around an underground lab workbench, no other people. On the left {MAYA} is jumping joyfully. Next to her {SAM} is cheering with red-gloved hands raised. On the right {ZARA} is clapping with a huge smile. Beside her {LEO} is grinning with his glasses glinting. {BLIP} floats above with a happy glowing face, the only robot. Device connected to terminal. {AGE}",

    "B1-021": f"Exactly four pre-teen children aged 10-12 on bedroom floor at midnight sharing samosas, no other people. On the left {MAYA} is eating a samosa. Next to her {SAM} is stuffing his face with red-gloved hands. On the right {ZARA} is reaching for another samosa. Beside her {LEO} is whispering with his reading glasses on. {BLIP} watches curiously, the only robot. Moonlight through window. {AGE}",

    "B1-023": f"Exactly four pre-teen children aged 10-12 on a park bench in morning sunshine sharing breakfast, no other people, no robots. On the left {MAYA} holds a cup. Next {SAM} gives a thumbs up with his red gaming glove. Then {ZARA} holds a plate with her yellow bag on her lap. On the right {LEO} eats from a bowl with beanie and glasses. Dappled golden light through trees. {AGE}",

    "B1-024": f"Exactly four pre-teen children aged 10-12 walking through a narrow underground tunnel, no other people, no robots. Leading is {MAYA} with flashlight and goggles on forehead. Behind her is {SAM} with red-gloved hands ready. Next is {ZARA} walking carefully with yellow bag. At the rear is {LEO} scanning walls with tablet. Brick walls with bundled cables along ceiling. Dim distant glow ahead. {AGE}",

    "B1-033": f"Exactly four pre-teen children aged 10-12 in their cozy underground lab headquarters, no other people. At the workbench is {MAYA} tinkering with circuits. Testing a gadget is {SAM} with red gaming gloves assembling parts. At the art desk is {ZARA} sketching with her yellow bag beside her. At the monitor desk is {LEO} studying data with reading glasses. {BLIP} sits on its charging dock, the only robot. String lights across ceiling. {AGE}",

    "B1-036": f"Exactly four pre-teen children aged 10-12 on an apartment rooftop at sunset, no other people. On the left {MAYA} has wind in her ponytail. Next {SAM} is leaning back on red-gloved hands with LED sneakers dangling. Then {ZARA} is taking a photo with her yellow bag. On the right {LEO} has beanie and glasses watching the horizon. {BLIP} floats between them, the only robot. Golden hour light. {AGE}",

    "B1-035": f"One single 12-year-old Nigerian-British girl with rich dark brown skin, voluminous black hair in chunky twists with colorful thread, bright yellow crossbody bag, oversized denim jacket with patches, colorful patterned leggings, bare hands with no gloves. She is pinning a photograph to a cork investigation board with red string. Solo detective moment. No other people. Pre-teen aged 12, not a toddler.",

    "B1-029": f"One single 11-year-old Indian girl with warm brown skin, dark brown thick messy ponytail with pencil, safety goggles on forehead, olive green utility vest, faded red rocket t-shirt, cargo shorts, bare hands with no gloves. She is operating a makeshift water valve at park sprinklers. Water spraying creating rainbows. Solo scene. No other people anywhere. Pre-teen aged 11, not a toddler.",
}

p = pathlib.Path(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json")
m = json.loads(p.read_text("utf-8"))

updated = 0
for item in m["illustrations"]:
    if item["id"] in MULTI:
        item["prompt"] = MULTI[item["id"]]
        item["status"] = "pending"
        updated += 1
        print(f"  Updated {item['id']}")

p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nUpdated {updated} prompts (red gloves = Sam only, bare hands for others)")

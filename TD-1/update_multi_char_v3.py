import json
import pathlib

SAM = "a 10-year-old Japanese-Korean boy with light-medium warm skin, black spiky messy hair gel-styled pointy on top and shaved close on sides, bright red fingerless gaming gloves on both hands, black t-shirt with PLAYER printed on it, athletic shorts with side stripes, high-top sneakers with glowing LED lights in the soles"
MAYA = "an 11-year-old Indian girl with warm brown skin, dark brown thick messy ponytail with a pencil stuck in it and escaped strands, safety goggles pushed up on forehead, oversized olive green utility vest with many pockets full of tools, faded red rocket ship t-shirt underneath, cargo shorts, velcro sneakers"
LEO = "an 11-year-old Mexican-American boy with warm tan golden-brown skin, compact build, black thick slightly grown-out fade haircut under a navy blue knit beanie with a small pixelated heart patch sewn on it, very dark intense eyes, reading glasses, oversized gray hoodie with sleeves over hands and a tablet in the front pocket, dark t-shirt underneath, jeans with grass-stained knees, sturdy sneakers"
ZARA = "a 12-year-old Nigerian-British girl with rich dark brown skin, tall long-limbed graceful build, voluminous black natural hair in chunky twists with colorful thread woven through, bright expressive dark brown eyes, high cheekbones, bright yellow crossbody bag covered in enamel pins, oversized denim jacket with patches and doodles on the sleeves, graphic art tee underneath, colorful patterned leggings, bright galaxy-painted sneakers, beaded bracelets on both wrists"
BLIP = "one single small white cube robot with a front LED screen showing a simple cyan smiley face, small antenna on top that wiggles, floating on tiny hover thrusters about two feet off the ground, the only robot in the scene"
AGE = "All children are pre-teens aged 10 to 12 years old, not toddlers or babies. Each child has distinctly different skin tone, hair texture, and clothing from the others - four unique individual children."

MULTI = {
    "B1-011": f"Exactly four pre-teen children aged 10-12 sitting around a table in a bright meeting room, no other people. On the left is {MAYA}. Next to her is {SAM} with his red gaming gloves on the table. Across from them is {ZARA} with her yellow crossbody bag beside her. On the right is {LEO} with his tablet showing green code on screen. {BLIP} floats above the table center. Whiteboard with colorful diagrams on the wall. Warm friendly first meeting. {AGE}",

    "B1-012": f"Exactly four pre-teen children aged 10-12 crammed together hiding in a dark narrow janitor closet, no other people. On the left is {MAYA} pressing finger to lips shushing quietly. Next to her is {SAM} peeking through the door crack with his red-gloved hand. Then {ZARA} clutching her yellow bag nervously with her beaded bracelets jingling. On the right is {LEO} crouching low scanning with his tablet. {BLIP} hovers near the ceiling with a dim worried face. Cleaning supplies on shelves. Single sliver of light under the door. {AGE}",

    "B1-018": f"Exactly four pre-teen children aged 10-12 standing at a dark tunnel entrance behind a basement wall, no other people. Leading from the left is {MAYA} holding a flashlight beam forward cutting through dust. Behind her is {SAM} at the ready with his red gaming gloves clenched. Next is {ZARA} walking carefully with her yellow bag clutched close and her denim jacket sleeves rolled up. At the rear is {LEO} peering into darkness scanning the walls with his tablet. {BLIP} hovers near the flashlight beam. Dusty narrow space with bundled cables along brick walls. Adventurous discovery. {AGE}",

    "B1-019": f"Exactly four pre-teen children aged 10-12 celebrating excitedly around an underground lab workbench, no other people. On the left {MAYA} is jumping with arms raised joyfully her ponytail flying. Next to her {SAM} is cheering loudly with his red-gloved hands pumped high in the air. On the right {ZARA} is clapping with a huge smile her hair twists bouncing. Beside her {LEO} is grinning ear to ear with his glasses glinting under the light. {BLIP} floats above the workbench with a happy glowing face, the only robot. Device connected to terminal. Triumphant joyful mood. {AGE}",

    "B1-021": f"Exactly four pre-teen children aged 10-12 sitting on bedroom floor at midnight sharing samosas from a plate between them, no other people. On the left {MAYA} is eating a samosa with a gap-toothed grin. Next to her {SAM} is stuffing his face with both red-gloved hands. On the right {ZARA} is reaching for another samosa with her beaded bracelets jingling and her yellow bag beside her. Beside her {LEO} is whispering excitedly with his reading glasses on. {BLIP} watches curiously from nearby, the only robot. Moonlight through window. Cozy secret midnight feast. {AGE}",

    "B1-023": f"Exactly four pre-teen children aged 10-12 sitting on a wooden park bench in morning sunshine sharing breakfast, no other people, no robots. On the left {MAYA} holds a cup with her utility vest pockets bulging. Next to her {SAM} gives a thumbs up with his red gaming glove while holding a snack. Then {ZARA} holds a plate with her denim jacket sleeves catching the light and her yellow bag on her lap. On the right {LEO} eats from a bowl with his beanie pulled down and his glasses glinting. Dappled golden light through leafy trees. Peaceful park morning. {AGE}",

    "B1-024": f"Exactly four pre-teen children aged 10-12 walking in single file cautiously through a narrow underground tunnel, no other people, no robots. Leading is {MAYA} with her flashlight cutting through dust and her goggles on her forehead. Behind her is {SAM} glancing back with his red-gloved hands ready and his LED sneakers lighting the floor. Next is {ZARA} walking carefully with her yellow bag close and her twists swaying. At the rear is {LEO} scanning the walls with his tablet showing green code. Brick walls with bundled cables along the ceiling. Dim distant glow ahead. {AGE}",

    "B1-033": f"Exactly four pre-teen children aged 10-12 in their cozy underground lab headquarters, no other people. On the left at the workbench is {MAYA} tinkering with circuits and wires, her vest pockets full of tools. At the center testing a gadget is {SAM} with his red gaming gloves carefully assembling parts. At the art desk is {ZARA} sketching in her notebook with her hair twists tied back and her yellow bag on the chair. At the monitor desk is {LEO} studying data on screen with his reading glasses on and tablet beside him. {BLIP} sits on its charging dock in the corner, the only robot. String lights across the ceiling. Monitors and blueprints everywhere. Secret base atmosphere. {AGE}",

    "B1-036": f"Exactly four pre-teen children aged 10-12 sitting on the edge of an apartment rooftop at sunset looking at the glowing city skyline, no other people. On the left {MAYA} has wind in her ponytail and goggles around her neck. Next to her {SAM} is leaning back on his red-gloved hands with his LED sneakers dangling over the edge. Then {ZARA} is holding her phone in her yellow bag taking a photo with her hair twists catching the golden light. On the right {LEO} has his beanie pulled down watching the horizon with his glasses reflecting the sunset. {BLIP} floats between them with a peaceful smile face, the only robot. Golden hour warm light bathing the scene. {AGE}",
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
print(f"\nUpdated {updated} multi-character prompts (Sam before Leo ordering)")

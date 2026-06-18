from gradio_client import Client
import os, base64, time, sys, dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
HF_TOKEN = os.environ.get("HF_TOKEN", None)

print(f"HF token: {'set' if HF_TOKEN else 'NOT SET'}")
print("Connecting to Bonsai Image API...")
client = Client("akhaliq/Bonsai-Image-Demo", token=HF_TOKEN)
print("Connected.")

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Characters")

# ── SHARED STYLE TOKENS ──
# Every single prompt gets this prepended AND appended so all 30 images
# share the same visual DNA regardless of subject or pose.
STYLE_PREFIX = (
    "THE GLITCH SQUAD children's book character art, "
    "vibrant saturated cel-shaded 2D digital illustration, "
    "bold clean black outlines with uniform line weight, "
    "flat color fills with minimal soft shading, "
    "round friendly proportions, large expressive eyes, "
    "warm golden lighting from upper-left, "
    "bright candy-color palette with high saturation, "
    "no gradients no photorealism no 3D render, "
)

STYLE_SUFFIX = (
    ", THE GLITCH SQUAD official art style, "
    "cel-shaded 2D cartoon illustration for kids age 8 to 11, "
    "clean vector-like linework, consistent character design sheet, "
    "bright warm lighting, high saturation colors, "
    "white or simple gradient background, "
    "no shadows on background, crisp edges, "
    "professional children's book illustration quality, 1024px"
)

MAX_RETRIES = 5
RETRY_WAIT = 75  # seconds to wait when quota exhausted

def generate(prompt, output_path, seed=0):
    if os.path.exists(output_path):
        print(f"SKIP (already exists): {output_path}")
        return True

    full_prompt = STYLE_PREFIX + prompt + STYLE_SUFFIX
    print(f"\nGenerating: {prompt[:90]}...")
    print(f"Output: {output_path}")
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"  Attempt {attempt}/{MAX_RETRIES} — sending to cloud (~30-60s)...")
            result = client.predict(
                prompt=full_prompt,
                seed=seed,
                steps=4,
                guidance=1.0,
                backend="bonsai-ternary-gemlite",
                height=1024,
                width=1024,
                max_sequence_length=256,
                api_name="/generate"
            )
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if isinstance(result, dict) and "image_b64" in result:
                img_data = base64.b64decode(result["image_b64"])
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"  SAVED: {output_path}")
                return True
            elif isinstance(result, str) and os.path.exists(result):
                import shutil
                shutil.copy2(result, output_path)
                print(f"  SAVED: {output_path}")
                return True
            else:
                print(f"  ERROR: Unexpected result type: {type(result)}")
                return False
                
        except Exception as e:
            err = str(e)
            if "quota" in err.lower() or "No GPU" in err:
                wait = RETRY_WAIT * attempt
                print(f"  QUOTA EXCEEDED — waiting {wait}s before retry ({attempt}/{MAX_RETRIES})...")
                time.sleep(wait)
            else:
                print(f"  ERROR: {err}")
                if attempt < MAX_RETRIES:
                    time.sleep(10)
    
    print(f"  FAILED after {MAX_RETRIES} attempts: {output_path}")
    return False

PROMPTS = {
    "Maya": [
        ("01_fullbody_front", "Full body character design of a 10-year-old Indian girl named Maya, warm brown skin, dark brown messy ponytail with escaped strands and a pencil stuck in it, safety goggles pushed up on forehead, oversized olive green utility vest covered in pockets with wires and tools sticking out, faded red t-shirt with rocket ship logo underneath, cargo shorts, velcro sneakers with one untied lace, modified digital watch on left wrist with tiny antenna taped on, grease smudge on one cheek, gap-toothed grin, curious squinting expression, lean wiry build, band-aids on fingers, standing pose facing viewer"),
        ("02_action_tinkering", "10-year-old Indian girl Maya building a gadget at a cluttered workbench, soldering wires together with intense concentration, safety goggles pushed up on forehead, olive green utility vest with tools in pockets, messy ponytail, warm brown skin, scattered screws and circuit boards around her, warm yellow desk lamp lighting, detailed workshop background"),
        ("03_closeup_face", "Close-up portrait of 10-year-old Indian girl Maya, warm brown skin, dark brown wide eyes full of curiosity, gap-toothed grin, slight grease smudge on cheek, safety goggles on forehead, messy ponytail with escaped strands and a small screwdriver stuck in hair, round face with slightly upturned nose, curious squinting expression like she is reverse-engineering something"),
        ("04_with_gadget", "10-year-old Indian girl Maya proudly holding up a strange mechanical gadget she just built, olive green utility vest, red t-shirt underneath, messy ponytail, warm brown skin, gap-toothed excited grin, safety goggles on forehead, the gadget is made of junk parts and wires with blinking lights, standing in a cluttered basement workshop"),
        ("05_vest_detail", "10-year-old Indian girl Maya showing off her oversized olive green inventor's vest, the vest has many pockets overflowing with wires batteries screws and small tools, she wears a faded red rocket ship t-shirt underneath, cargo shorts, modified digital watch with tiny antenna, warm brown skin, confident stance with hands on hips, messy ponytail"),
        ("06_team_pose", "10-year-old Indian girl Maya standing confidently with arms crossed, olive green utility vest, red t-shirt, cargo shorts, messy ponytail with pencil in it, safety goggles on forehead, warm brown skin, leader pose with a determined smile, slight grease on cheek, urban neighborhood background with brick buildings"),
    ],
    "Leo": [
        ("01_fullbody_front", "Full body character design of a 10-year-old Mexican-American boy named Leo, warm tan golden-brown skin, compact stocky build, black hair in slightly grown-out fade under a navy blue beanie with a small pixelated heart patch sewn on, very dark intense eyes with thick eyebrows, small scar on chin, calm focused expression with slight frown of concentration, oversized gray hoodie with sleeves pulled over hands, dark t-shirt underneath, jeans with grass stains on knees, sturdy double-knotted sneakers, reading glasses hanging on a chain around neck, standing pose facing viewer"),
        ("02_coding_action", "10-year-old Mexican-American boy Leo coding on a tablet at a desk, navy blue beanie with pixel heart patch, gray hoodie with sleeves over hands, intense focused expression, dark eyes narrowed in concentration, warm tan skin, small chin scar, the tablet screen shows colorful code, desk has a bag of chips and crumpled papers, dim room with screen glow on face"),
        ("03_closeup_face", "Close-up portrait of 10-year-old Mexican-American boy Leo, warm tan golden-brown skin, very dark almost black eyes with thick eyebrows making him look serious, round cheeks contradicting his intense expression, small scar on chin, navy blue beanie with tiny pixelated heart patch, calm focused face, slightly hunched posture visible"),
        ("04_invisible_keyboard", "10-year-old Mexican-American boy Leo standing and typing on an invisible keyboard in the air with his fingers, eyes closed in deep thought, navy blue beanie, gray hoodie, warm tan skin, reading glasses dangling on chain, visual thought bubble showing code and patterns around his head"),
        ("05_hoodie_detail", "10-year-old Mexican-American boy Leo in his signature oversized gray hoodie, navy blue beanie with pixel heart patch, the hoodie front pocket holds his tablet peeking out, grass-stained jeans, double-knotted sneakers, reading glasses on chain, warm tan skin, compact stocky build, relaxed standing pose"),
        ("06_with_tablet", "10-year-old Mexican-American boy Leo sitting cross-legged on floor with tablet on his face, fallen asleep coding, navy blue beanie askew, gray hoodie, warm tan skin, empty chip bag next to him, peaceful sleeping face with tablet balanced on face"),
    ],
    "Zara": [
        ("01_fullbody_front", "Full body character design of an 11-year-old Nigerian-British girl named Zara, rich dark brown skin, tall long-limbed graceful build, voluminous black natural hair in chunky twists with colorful thread woven in, bright expressive dark brown eyes, high cheekbones, wide smile with gap between front teeth, small 3D-printed stud earrings, bright yellow crossbody bag covered in colorful enamel pins, oversized denim jacket with patches and doodles on sleeves, graphic art tee underneath, colorful patterned leggings, bright sneakers, beaded bracelets on both wrists, standing pose facing viewer"),
        ("02_drawing_action", "11-year-old Nigerian-British girl Zara sketching furiously in a notebook, voluminous black hair in chunky twists with colorful threads, rich dark brown skin, oversized denim jacket with doodles, bright yellow bag beside her, colorful markers scattered around, intense creative focus on her face, beaded bracelets jingling on wrists, stylus behind ear, bright art studio background"),
        ("03_closeup_face", "Close-up portrait of 11-year-old Nigerian-British girl Zara, rich dark brown skin, bright expressive dark brown eyes showing warmth and amusement, high cheekbones, wide smile with gap between front teeth, small 3D-printed stud earrings, voluminous black natural hair in chunky twists with colorful thread, long graceful neck, observant expression seeing artistic potential in everything"),
        ("04_with_sketchpad", "11-year-old Nigerian-British girl Zara holding up a sketchpad showing a detailed drawing, proud expression, rich dark brown skin, voluminous twists hair, bright yellow crossbody bag, denim jacket with patches, colorful leggings, the sketchpad shows a robot design that looks like a small cute cube, beaded bracelets, art supplies scattered around her feet"),
        ("05_jacket_detail", "11-year-old Nigerian-British girl Zara showing off her customized denim jacket, the jacket is covered in hand-drawn doodles embroidered patches and small painted designs, rich dark brown skin, bright yellow crossbody bag with enamel pins of robots and flowers, graphic tee underneath, colorful beaded bracelets, voluminous natural hair twists"),
        ("06_team_pose", "11-year-old Nigerian-British girl Zara standing tall and graceful with one hand on hip and sketchpad in other hand, bright yellow crossbody bag, oversized denim jacket with doodles, voluminous black hair twists, rich dark brown skin, warm confident smile, colorful sneakers, beaded bracelets, urban park background"),
    ],
    "Sam": [
        ("01_fullbody_front", "Full body character design of a 9-year-old Japanese-Korean boy named Sam, light-medium warm skin, compact athletic muscular build for a kid, black spiky messy hair on top shaved close on sides styled with gel, almond-shaped dark brown eyes with permanent mischievous sparkle, round face with pointed chin, missing bottom front tooth creating goofy grin, bright red fingerless gaming gloves, black t-shirt with pixelated game controller, athletic shorts with stripes, high-top sneakers with LED lights in soles, gaming headset around neck, small game-cartridge backpack, standing in dynamic action-ready pose facing viewer"),
        ("02_parkour_action", "9-year-old Japanese-Korean boy Sam mid-parkour jump between buildings, dynamic leaping pose with arms spread, bright red fingerless gaming gloves, black game controller t-shirt, athletic shorts, LED sneakers lighting up, gaming headset bouncing around neck, spiky black hair, missing tooth grin of pure joy, fresh scrape on elbow, city rooftop background, action scene with motion lines"),
        ("03_closeup_face", "Close-up portrait of 9-year-old Japanese-Korean boy Sam, light-medium warm skin, almond-shaped dark brown eyes with permanent mischievous sparkle like he is planning something, round face with pointed chin, goofy grin showing missing bottom front tooth, black spiky messy hair on top shaved close on sides, impish eyebrows raised expression"),
        ("04_gaming_pose", "9-year-old Japanese-Korean boy Sam in intense gaming stance, red fingerless gloves gripping an invisible controller, body crouched and focused, LED sneakers glowing, gaming headset on ears, black game controller t-shirt, spiky black hair, missing tooth visible in determined grin, eyes wide with concentration"),
        ("05_gloves_detail", "9-year-old Japanese-Korean boy Sam showing off his signature bright red fingerless gaming gloves, flexing his hands dramatically, black game controller t-shirt, athletic shorts with stripes, high-top LED sneakers, game cartridge backpack, spiky black hair, missing tooth grin, compact athletic build, light-medium warm skin"),
        ("06_victory_dance", "9-year-old Japanese-Korean boy Sam doing a wild victory dance with arms raised, one foot off ground, LED sneakers flashing, bright red fingerless gloves in the air, gaming headset around neck, missing tooth grin of pure triumph, spiky black hair, fresh scrape on knee, confetti or sparkles around him"),
    ],
    "Blip": [
        ("01_fullbody_front", "Full body character design of Blip a small cute AI robot cube, 4 inches per side, matte white casing with rounded edges and slight scuff marks and dirt smudges, front LED screen showing a cute simple emoji face with two dot eyes and a curved smile line in cyan teal color, small antenna on top that wiggles, tiny hover thrusters underneath creating a soft cyan glow, floating 2 feet off the ground, small charging cable compartment on one side, adorable robot companion design, facing viewer"),
        ("02_confused_expression", "Cute small white cube robot Blip with a confused expression, LED screen face showing tilted question-mark-like eyes and a wobbly frown in orange color indicating confusion, antenna drooping slightly, hovering off ground, small sparks around his body from bumping into something, matte white casing with rounded edges and scuff marks"),
        ("03_excited_expression", "Cute small white cube robot Blip with an excited happy expression, LED screen face showing wide bright eyes and a big open smile in yellow color with small star shapes, antenna wiggling wildly like an excited dog tail, hover thrusters glowing brighter, bouncing slightly in the air, matte white casing with scuff marks"),
        ("04_scared_expression", "Cute small white cube robot Blip with a scared worried expression, LED screen face showing small quivering eyes and a wavy frown in dim flickering red color indicating fear, antenna drooping, hovering lower to the ground, hiding behind a pair of kids legs only his antenna and top edge visible, matte white casing"),
        ("05_with_kids", "Cute small white cube robot Blip floating in the center among four diverse kids who are smiling warmly at him, Blip has happy cyan face, antenna wiggling, hover glow underneath, one kid with olive green vest, one with navy beanie, one with yellow bag, one with red gloves, matte white casing with scuff marks, bright cheerful scene"),
        ("06_sleepy_charging", "Cute small white cube robot Blip plugged in and charging, LED screen face showing closed eyes in a sleepy expression with soft purple dim color, small Zzz floating above antenna which is drooping, charging cable connected from the side compartment, cozy warm lighting, sitting on a messy desk with kid's drawings and gadgets"),
    ],
}

character = sys.argv[1] if len(sys.argv) > 1 else None

if character and character in PROMPTS:
    names = [character]
elif character == "all":
    names = list(PROMPTS.keys())
else:
    print("Usage: python generate_characters.py <Maya|Leo|Zara|Sam|Blip|all>")
    print(f"Available: {', '.join(PROMPTS.keys())}, all")
    sys.exit(1)

for char_name in names:
    char_dir = os.path.join(BASE_DIR, char_name)
    os.makedirs(char_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"Generating {len(PROMPTS[char_name])} images for {char_name}...")
    print(f"{'='*60}")
    
    for i, (variant_name, prompt) in enumerate(PROMPTS[char_name]):
        output_path = os.path.join(char_dir, f"{variant_name}.png")
        seed = hash(char_name + variant_name) % 100000
        generate(prompt, output_path, seed=seed)
        if i < len(PROMPTS[char_name]) - 1:
            print(f"  Waiting 10s before next image...")
            time.sleep(10)
    
    print(f"\nDone with {char_name}: {len(PROMPTS[char_name])} images in {char_dir}")

print("\nAll done!")

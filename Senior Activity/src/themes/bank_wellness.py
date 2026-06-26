"""Wellness & Healthy Living - evergreen, all-country content bank."""
from __future__ import annotations
from collections import OrderedDict


def build() -> dict:
    word_pools = OrderedDict([
        ("Healthy Foods", [
            "OATS", "GREENS", "NUTS", "FRUIT", "SEEDS", "LENTILS", "BEANS",
            "YOGURT", "SALAD", "BROTH", "SALMON", "BERRY", "QUINOA", "BARLEY",
            "CITRUS", "GINGER", "TURMERIC", "HONEY", "CINNAMON", "SPINACH",
            "BROCCOLI", "CARROT", "APPLE", "BANANA", "ORANGE", "AVOCADO",
            "PUMPKIN", "CABBAGE", "ALMOND", "WALNUT", "RAISIN", "KALE", "PEAS",
            "RICE", "MILLET", "CORN", "PEAR", "PLUM", "MANGO", "PAPAYA",
            "GUAVA", "FIG", "GRAPE", "MELON", "PEACH", "LEMON", "LIME",
            "BEET", "ONION", "GARLIC", "TOMATO", "PEPPER", "CUCUMBER",
            "ZUCCHINI", "EGGPLANT", "MUSHROOM", "CAULIFLOWER", "RADISH",
            "CELERY", "TURNIP", "OKRA", "OLIVE", "COCONUT",
        ]),
        ("Exercise & Movement", [
            "WALKING", "YOGA", "STRETCH", "SWIM", "DANCE", "CYCLE", "JOG",
            "LIFT", "SQUAT", "LUNGE", "PLANK", "BALANCE", "FLEX", "MOVE",
            "ROUTINE", "WARMUP", "COOLDOWN", "POSTURE", "AGILITY", "STAMINA",
            "STRENGTH", "ENDURANCE", "PACE", "STRIDE", "MARCH", "JOGGING",
            "HIKING", "GARDENING", "TAICHI", "PILATES", "CARDIO", "RUN",
            "ROW", "BEND", "REACH", "TWIST", "LEAP", "HOP", "SKIP", "CLIMB",
            "PEDAL", "PADDLE", "ROLL", "FLEXIBILITY", "MOBILITY", "FITNESS",
            "WORKOUT", "GYM", "TRACK", "TRAIL", "PATH", "AEROBICS", "BOWLING",
            "GOLF", "TENNIS", "BICYCLE", "TREADMILL", "WEIGHTS", "KETTLEBELL",
            "DUMBBELL", "REPS", "SETS", "INTERVAL", "CIRCUIT", "DRILL",
            "SPRINT", "STROLL", "AMBLE",
        ]),
        ("Relaxation & Calm", [
            "CALM", "SERENE", "QUIET", "SOOTHE", "UNWIND", "EASE", "GENTLE",
            "SLOW", "STILL", "PAUSE", "SIGH", "RELEASE", "MELLOW", "COZY",
            "TRANQUIL", "SOFT", "RESTFUL", "PEACEFUL", "MEDITATE", "RELAX",
            "BREATHE", "DEEP", "SETTLE", "DRIFT", "COMFORT", "PLACID", "HUSH",
            "LULL", "BASK", "LOUNGE", "NESTLE", "SNUGGLE", "CRADLE", "SWAY",
            "HUM", "BREEZE", "REPOSE", "LEISURE", "TRANQUILITY", "SERENITY",
            "HARMONY", "CALMNESS", "STILLNESS", "EQUANIMITY", "CONTENTMENT",
            "RETREAT", "OASIS", "SANCTUARY", "HAVEN", "BLISS", "ZEN", "MILD",
            "BALMY",
        ]),
        ("Sleep & Rest", [
            "SLEEP", "NAP", "DREAM", "BED", "PILLOW", "BLANKET", "SLUMBER",
            "NIGHT", "DROWSY", "SNOOZE", "NIGHTCAP", "BEDTIME", "LULLABY",
            "DUVET", "MATTRESS", "CURTAIN", "COTTON", "REST", "RISE", "DAWN",
            "SLEEPY", "TIRED", "WEARY", "DOZE", "YAWN", "SIESTA", "MOON",
            "STAR", "NIGHTIE", "PAJAMAS", "NIGHTGOWN", "ROBE", "SLIPPER",
            "SHEET", "QUILT", "NIGHTFALL", "DUSK", "TWILIGHT", "DREAMLAND",
            "NIGHTSHIRT", "DAYBED", "COT", "BUNK", "BEDFRAME", "HEADBOARD",
            "DREAMY", "NOD", "WINK",
        ]),
        ("Hydration", [
            "WATER", "SIP", "DRINK", "THIRST", "FLUID", "MOISTURE", "REFRESH",
            "GLASS", "BOTTLE", "JUICE", "CLEAR", "COOL", "CUP", "HYDRATE",
            "INFUSE", "STEEP", "TEA", "DEW", "POUR", "SWIG", "GULP",
            "TUMBLER", "MUG", "FLASK", "JUG", "PITCHER", "DRINKS", "BEVERAGE",
            "SMOOTHIE", "ICED", "ICY", "LIQUID", "WET", "SPRING", "STREAM",
            "FOUNTAIN", "TAP", "REFRESHING", "THIRSTY", "LEMONADE",
            "FLAVORED",
        ]),
        ("Mindfulness & Meditation", [
            "AWARE", "PRESENT", "FOCUS", "NOTICE", "OBSERVE", "GRATITUDE",
            "KINDNESS", "BREATH", "MOMENT", "CENTER", "GROUND", "REFLECT",
            "ACCEPT", "SMILE", "ATTENTION", "AWARENESS", "BREATHING",
            "MINDFUL", "INTENT", "CLARITY", "MEDITATION", "MANTRA", "CHANT",
            "LOTUS", "PRANA", "CHAKRA", "BREATHWORK", "CONSCIOUS",
            "CONTEMPLATE", "BEING", "SPIRIT", "SOUL", "INNER", "THANKFUL",
            "APPRECIATE", "COMPASSION", "EMPATHY", "ATTENTIVE", "PRESENCE",
            "NOW", "INSIGHT", "WISDOM", "CONCENTRATION", "REFLECTION",
            "CONTEMPLATION", "CENTERED", "GROUNDED", "MINDFULNESS",
            "ATTENTIVENESS",
        ]),
        ("Body Parts", [
            "HEART", "LUNGS", "MUSCLE", "JOINT", "BONE", "SPINE", "SKIN",
            "BACK", "KNEE", "SHOULDER", "NECK", "ARM", "LEG", "HAND", "FOOT",
            "CORE", "HIP", "WRIST", "ELBOW", "ANKLE", "CHEST", "FINGER",
            "HEAD", "FACE", "EYE", "EAR", "NOSE", "MOUTH", "LIP", "TEETH",
            "TONGUE", "THUMB", "PALM", "FIST", "THIGH", "CALF", "SHIN",
            "TOE", "HEEL", "SOLE", "BELLY", "WAIST", "RIB", "PELVIS",
            "BRAIN", "NERVE", "VEIN", "ARTERY", "TENDON", "LIGAMENT",
            "CARTILAGE", "CELL", "BLOOD", "PULSE", "TEMPLE", "JAW", "CHIN",
            "CHEEK", "FOREHEAD", "SCALP", "HAIR", "NAIL", "COLLARBONE",
            "SHOULDERBLADE", "KNEECAP", "FEMUR",
        ]),
        ("Feelings & Moods", [
            "JOY", "PEACE", "ENERGY", "HAPPY", "HOPE", "GLOW", "VITAL",
            "BRIGHT", "CHEER", "CONTENT", "GLEE", "RELAXED", "REFRESHED",
            "STRONG", "ACTIVE", "ALIVE", "WELL", "HEALTHY", "FRESH", "GLAD",
            "PROUD", "GRATEFUL", "EAGER", "LIVELY", "BOLD", "CONFIDENT",
            "OPTIMISTIC", "POSITIVE", "UPBEAT", "CHEERFUL", "DELIGHT",
            "JOYFUL", "JOLLY", "MERRY", "BLISSFUL", "CONTENTED", "SATISFIED",
            "PLEASED", "EXCITED", "INSPIRED", "MOTIVATED", "ZESTFUL",
            "VIBRANT", "RADIANT", "THRIVING", "FLOURISHING", "RENEWED",
            "ENTHUSED", "SPUNKY", "SMILING", "GLEEFUL", "HAPPINESS",
            "DELIGHTED", "ENCOURAGED", "EMPOWERED",
        ]),
        ("Healthy Habits", [
            "BRUSH", "FLOSS", "WASH", "CHEW", "SAVOR", "PLAN", "COOK",
            "GARDEN", "CLEAN", "TIDY", "ORGANIZE", "SCHEDULE", "HYGIENE",
            "GROOMING", "BATHE", "SHOWER", "SCRUB", "RINSE", "SOAP", "TOWEL",
            "COMB", "TRIM", "EAT", "MEAL", "BREAKFAST", "LUNCH", "DINNER",
            "SNACK", "PORTION", "WAKE", "JOURNAL", "DIARY", "GOAL", "HABIT",
            "PLANNER", "CHECKLIST", "STAND", "SIT", "PREP", "SHOP",
            "NUTRITION", "NOURISH", "FUEL", "SUPPER", "NIBBLE", "MUNCH",
        ]),
        ("Nature & Outdoor Wellness", [
            "SUNSHINE", "SUNLIGHT", "OUTDOOR", "OUTSIDE", "SKY", "CLOUD",
            "BIRD", "TREE", "LEAF", "GRASS", "LAWN", "MEADOW", "FIELD",
            "FOREST", "WOOD", "PARK", "FLOWER", "BLOOM", "BLOSSOM", "PETAL",
            "STEM", "ROOT", "BRANCH", "POND", "LAKE", "RIVER", "SEA", "OCEAN",
            "BEACH", "SAND", "SHELL", "WAVE", "HILL", "MOUNTAIN", "VALLEY",
            "SUN", "BUSH", "SHRUB", "VINE", "FERN", "MOSS", "STONE",
            "PEBBLE", "SOIL", "SUNRISE", "SUNSET", "HORIZON", "DAYLIGHT",
            "GROVE", "CANOPY", "THICKET", "GLADE", "BROOK", "CREEK", "TRUNK",
            "BARK", "BUD",
        ]),
        ("Self-care", [
            "BATH", "SPA", "MASSAGE", "LOTION", "CREAM", "PAMPER", "TREAT",
            "INDULGE", "CARE", "SELF", "MANICURE", "PEDICURE", "FACIAL",
            "SALON", "BARBER", "STYLIST", "HAIRCUT", "SHAVE", "MOISTURIZE",
            "BALM", "SOAK", "STEAM", "SAUNA", "JACUZZI", "POOL", "NURTURE",
            "REJUVENATE", "REVIVE", "RECHARGE", "RESTORE", "RENEW", "CANDLE",
            "AROMA", "PERFUME", "SCENT", "FRAGRANCE", "OIL", "MIST", "RUB",
            "MASK",
        ]),
    ])
    trivia_easy = [
        {"q": "About how many glasses of water a day are often suggested for good hydration?",
         "options": ["8 glasses", "1 glass", "20 glasses"], "answer": "8 glasses"},
        {"q": "Which gentle activity helps keep joints loose and flexible?",
         "options": ["Stretching", "Sprinting", "Lifting heavy boxes"], "answer": "Stretching"},
        {"q": "Which calming practice links slow breathing with gentle poses?",
         "options": ["Yoga", "Boxing", "Sprinting"], "answer": "Yoga"},
        {"q": "About how many hours of sleep do most adults need each night?",
         "options": ["About 8 hours", "About 2 hours", "About 16 hours"], "answer": "About 8 hours"},
        {"q": "Which of these is a healthy whole grain for breakfast?",
         "options": ["Oats", "Candy", "Soda"], "answer": "Oats"},
        {"q": "What is one of the best things you can do to lift a low mood?",
         "options": ["Move and be active", "Complain often", "Skip meals"], "answer": "Move and be active"},
        {"q": "Which part of a meal is packed with vitamins?",
         "options": ["Vegetables", "Sugar", "Salt"], "answer": "Vegetables"},
        {"q": "Which of these helps most to relax before bedtime?",
         "options": ["A warm bath", "Loud music", "Bright screens"], "answer": "A warm bath"},
        {"q": "Which habit helps keep your teeth healthy?",
         "options": ["Brushing twice daily", "Skipping brushing", "Eating lots of sweets"],
         "answer": "Brushing twice daily"},
        {"q": "Which kind of place tends to boost mood and calm the mind?",
         "options": ["A green park", "A busy road", "A dark, stuffy room"], "answer": "A green park"},
        {"q": "What does regular stretching mainly help to improve?",
         "options": ["Flexibility", "Eyesight", "Hearing"], "answer": "Flexibility"},
        {"q": "Which of these is the best way to stay hydrated?",
         "options": ["Drink water through the day", "Drink less water", "Only drink coffee"],
         "answer": "Drink water through the day"},
    ]
    phrase_medium = [
        {"prompt": "Early to bed and early to ____", "answer": "Rise"},
        {"prompt": "A sound mind in a sound ____", "answer": "Body"},
        {"prompt": "Health is ____", "answer": "Wealth"},
        {"prompt": "An ounce of prevention is worth a pound of ____", "answer": "Cure"},
        {"prompt": "Laughter is the best ____", "answer": "Medicine"},
        {"prompt": "A healthy outside starts from the ____", "answer": "Inside"},
        {"prompt": "Take care of your body; it's the only place you have to ____",
         "answer": "Live"},
        {"prompt": "Move it or ____ it", "answer": "Lose"},
        {"prompt": "Early to rise makes a man healthy, wealthy, and ____", "answer": "Wise"},
    ]
    trivia_open = [
        {"q": "Name the calming practice that links body poses with slow breath.",
         "answer": "Yoga"},
        {"q": "Which gentle outdoor activity is often called the best all-round exercise?",
         "answer": "Walking"},
        {"q": "Which warm whole grain is commonly eaten at breakfast for energy?",
         "answer": "Oats"},
        {"q": "What do we call the practice of paying full attention to the present moment?",
         "answer": "Mindfulness"},
        {"q": "Which clear drink is essential for keeping the body hydrated?",
         "answer": "Water"},
        {"q": "About how many hours of sleep do most adults need each night?",
         "answer": "Eight hours"},
        {"q": "Name the bowl of leafy greens eaten for vitamins and fiber.",
         "answer": "Salad"},
        {"q": "What should you do each morning to keep your teeth clean?",
         "answer": "Brush them"},
    ]
    crossword = [
        ("WATER", "Clear drink that keeps the body hydrated"),
        ("YOGA", "Calm practice of poses and breath"),
        ("SLEEP", "Nightly rest for body and mind"),
        ("OATS", "Healthy whole-grain breakfast"),
        ("WALK", "Gentle outdoor exercise, step by step"),
        ("REST", "Time to relax and recover"),
        ("BREATHE", "Take in air, slowly and deeply"),
        ("HEART", "Organ that pumps blood around the body"),
        ("LUNGS", "Pair of organs you breathe with"),
        ("MUSCLE", "Tissue that moves your body"),
        ("STRETCH", "Lengthen your muscles gently"),
        ("ENERGY", "Vigor and zest for activity"),
        ("CALM", "Peaceful and relaxed"),
        ("SMILE", "Happy expression on your face"),
        ("PEACE", "Feeling of quiet calm"),
        ("FRUIT", "Sweet plant food full of vitamins"),
        ("GREENS", "Leafy vegetables like spinach"),
        ("NUTS", "Crunchy healthy snacks"),
        ("HYDRATE", "Take in water to refresh the body"),
        ("POSTURE", "The way you hold and carry your body"),
        ("BALANCE", "Staying steady on your feet"),
        ("RELAX", "Let go of tension"),
        ("VITAL", "Full of life and energy"),
        ("FRESH", "Crisp and new, like morning air"),
        ("GARDEN", "Outdoor patch for plants and calm"),
        ("DREAM", "Picture seen while you sleep"),
        ("PILLOW", "Soft headrest for sleep"),
        ("BROTH", "Warm, soothing drink"),
        ("SALAD", "Bowl of healthy greens"),
    ]
    remedies = [
        {"condition": "Joint & Arthritis Pain",
         "text": "Drink warm turmeric milk, often called golden milk, and massage "
                 "aching joints with warm sesame oil. Fenugreek seeds soaked "
                 "overnight are a traditional daily support for the joints. "
                 "Gentle, regular movement keeps them looser than long still spells."},
        {"condition": "Stiff, Creaky Knees",
         "text": "Massage the knees with warm sesame oil, or apply a warm ginger-"
                 "turmeric paste. Gentle, regular movement keeps stiff joints "
                 "looser than sitting still for long spells. Build up activity "
                 "slowly and stop if it feels sharp."},
        {"condition": "High Blood Pressure",
         "text": "A little garlic daily, less salt, and hibiscus tea are "
                 "traditional supports. Daily walks and slow, deep breathing help "
                 "keep blood pressure steady. Always follow your doctor's plan and "
                 "check it regularly."},
        {"condition": "Blood Sugar Support",
         "text": "Fenugreek seeds soaked overnight, a pinch of cinnamon, and "
                 "Indian gooseberry are old daily aids. Steady, smaller meals and "
                 "a short walk after eating help too. Always follow your doctor's "
                 "plan for sugar control."},
        {"condition": "Daily Constipation",
         "text": "Start the day with a glass of warm water. A teaspoon of "
                 "clarified butter (ghee) in warm milk, or triphala, a traditional "
                 "three-fruit blend, at night are gentle aids. Soaked figs or "
                 "raisins and plenty of fibre keep you regular."},
        {"condition": "Triphala Water",
         "text": "Stir a little triphala, a traditional three-fruit herbal blend, "
                 "into warm water and drink at bedtime. It is a gentle, time-"
                 "honored aid for regularity and gentle cleansing."},
        {"condition": "Ashwagandha Milk",
         "text": "Whisk a small spoon of ashwagandha, a traditional calming herb, "
                 "into warm milk at night. This traditional tonic is used to ease "
                 "stress, build strength, and support sound sleep."},
    ]
    coloring = ["flower", "bird", "butterfly", "sun", "leaf", "teapot"]
    return {
        "word_pools": _dedup_pools(word_pools),
        "trivia_easy": trivia_easy, "phrase_medium": phrase_medium,
        "trivia_open": trivia_open, "crossword": crossword,
        "remedies": remedies, "remedies_title": "Home Remedies & Wellness Wisdom",
        "coloring": coloring,
    }


def _dedup_pools(pools):
    seen, out = set(), OrderedDict()
    for cat, words in pools.items():
        clean = []
        for w in words:
            wu = w.upper()
            if wu.isalpha() and 3 <= len(wu) <= 13 and wu not in seen:
                seen.add(wu); clean.append(wu)
        out[cat] = clean
    return out


BANKS = {"wellness": build}

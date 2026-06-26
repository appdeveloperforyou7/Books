"""Food & Kitchen Favorites - evergreen, all-country content bank."""
from __future__ import annotations
from collections import OrderedDict


def build() -> dict:
    word_pools = OrderedDict([
        ("Fruits", [
            "APPLE", "BANANA", "ORANGE", "MANGO", "GRAPE", "PEACH", "PEAR",
            "PLUM", "CHERRY", "BERRY", "LEMON", "LIME", "MELON", "PAPAYA",
            "PINEAPPLE", "APRICOT", "FIG", "GUAVA", "KIWI", "NECTARINE",
            "POMEGRANATE", "STRAWBERRY", "BLUEBERRY", "RASPBERRY", "COCONUT",
            "AVOCADO", "DATE", "CURRANT", "CRANBERRY", "TANGERINE",
            "BLACKBERRY", "BOYSENBERRY", "GOOSEBERRY", "ELDERBERRY", "MULBERRY",
            "LINGONBERRY", "GRAPEFRUIT", "WATERMELON", "CANTALOUPE", "HONEYDEW",
            "LYCHEE", "JACKFRUIT", "DRAGONFRUIT", "PASSIONFRUIT", "MANGOSTEEN",
            "QUINCE", "PERSIMMON", "KUMQUAT", "RAMBUTAN", "STARFRUIT",
            "CLEMENTINE", "MANDARIN", "SATSUMA", "DAMSON", "LOQUAT",
            "DURIAN", "BREADFRUIT", "SALAK", "ACAI", "NONI",
            "ACKEE", "SAPOTE", "LONGAN", "FEIJOA", "MEDLAR", "ROWAN",
        ]),
        ("Vegetables", [
            "CARROT", "POTATO", "ONION", "TOMATO", "PEPPER", "CABBAGE",
            "LETTUCE", "SPINACH", "BROCCOLI", "CUCUMBER", "PUMPKIN", "BEAN",
            "PEA", "CORN", "CELERY", "RADISH", "BEETROOT", "TURNIP",
            "PARSNIP", "COURGETTE", "AUBERGINE", "CAULIFLOWER", "ASPARAGUS",
            "LEEK", "KALE", "SQUASH", "ARTICHOKE", "MUSHROOM", "GARLIC",
            "SHALLOT", "OKRA", "ZUCCHINI", "EGGPLANT", "YAM", "BEET",
            "SPROUT", "CHARD", "WATERCRESS", "ARUGULA", "ENDIVE", "RADICCHIO",
            "KOHLRABI", "SWEDE", "RUTABAGA", "MANGETOUT", "BOKCHOY",
            "BROCCOLINI", "CAPSICUM", "JICAMA", "TARO", "CASSAVA", "PLANTAIN",
            "SCALLION", "GHERKIN", "EDAMAME", "CHAYOTE", "COLLARD",
            "SWEETCORN", "MAIZE", "LOTUSROOT", "HORSERADISH", "PAKCHOI",
            "GAILAN", "TATSOI", "MIZUNA", "YAMBEAN",
        ]),
        ("Herbs & Spices", [
            "BASIL", "MINT", "SAGE", "THYME", "DILL", "PARSLEY", "OREGANO",
            "ROSEMARY", "CUMIN", "PAPRIKA", "TURMERIC", "GINGER", "CINNAMON",
            "SAFFRON", "VANILLA", "CLOVE", "NUTMEG", "CORIANDER", "CARDAMOM",
            "CHILI", "PEPPER", "BAY", "CHIVES", "TARRAGON", "FENNEL",
            "ALLSPICE", "ANISE", "CARAWAY", "MACE", "MARJORAM", "LAVENDER",
            "LEMONBALM", "LEMONGRASS", "FENUGREEK", "WASABI", "PEPPERCORN",
            "CAYENNE", "ZAATAR", "SUMAC", "CHERVIL", "SORREL", "GALANGAL",
            "PEPPERMINT", "SPEARMINT", "CHAMOMILE", "BERGAMOT", "CURRYLEAF",
            "TAMARIND", "CAPER", "STARANISE", "SAFFLOWER", "AJWAIN",
            "ASAFOETIDA", "GARAMMASALA", "DUKKAH", "BLACKPEPPER", "WHITEPEPPER",
        ]),
        ("Kitchen Tools", [
            "WHISK", "LADLE", "SPATULA", "SPOON", "FORK", "KNIFE", "PAN",
            "POT", "BOWL", "PLATE", "CUP", "MUG", "KETTLE", "TOASTER",
            "BLENDER", "GRATER", "COLANDER", "ROLLINGPIN", "MEASURINGCUP",
            "CUTTINGBOARD", "SIEVE", "TONGS", "TRAY", "OVEN", "STOVE",
            "FRIDGE", "FREEZER", "SAUCEPAN", "FRYINGPAN", "PEELER",
            "MIXER", "MICROWAVE", "SLOWCOOKER", "AIRFRYER", "FOODPROCESSOR",
            "STANDMIXER", "SCALE", "THERMOMETER", "TIMER", "CLEAVER",
            "PARINGKNIFE", "CHEFKNIFE", "CHOPPINGBOARD", "MORTAR", "PESTLE",
            "JUICER", "GARLICPRESS", "CANOPENER", "CORKSCREW", "NUTCRACKER",
            "MANDOLINE", "RICER", "MASHER", "POTATOMASHER", "FUNNEL",
            "PASTRYBRUSH", "BASTER", "SKILLET", "WOK", "GRIDDLE", "DUTCHOVEN",
            "STOCKPOT", "STEAMER", "ROASTINGPAN", "BAKINGSHEET", "MUFFINTIN",
            "SPRINGFORM", "COOLINGRACK", "RAMEKIN", "TEASPOON", "TABLESPOON",
            "CHOPSTICKS", "STRAINER", "TEATOWEL", "OVENMITT", "APRON",
            "TRIVET", "COASTER", "PLATTER", "CUTLERY", "FLASK", "THERMOS",
            "PITCHER", "CARAFE", "TEAPOT", "COOKIECUTTER", "PIPINGBAG",
            "EGGBEATER", "DOUBLEBOILER", "CITRUSPRESS", "SLOTTEDSPOON",
        ]),
        ("Cooking Techniques", [
            "GRILL", "SIMMER", "KNEAD", "FRY", "BOIL", "STEAM", "BROIL",
            "BRAISE", "SAUTE", "SEAR", "POACH", "BLANCH", "DEEPFRY", "PANFRY",
            "TOSS", "BEAT", "MIX", "CHOP", "DICE", "MINCE", "SLICE", "GRATE",
            "PEEL", "MASH", "PUREE", "BLEND", "STUFF", "FOLD", "MARINATE",
            "PICKLE", "CURE", "SMOKE", "BRINE", "GLAZE", "REDUCE", "WHIP",
            "DRIZZLE", "GARNISH", "BASTE", "CARVE", "SCOOP", "SIFT",
            "SCRAMBLE", "ROUX", "FLAMBE", "INFUSE", "STEEP", "CLARIFY",
            "SCALD", "PARBOIL", "CONFIT", "TEMPER", "PROOF", "FERMENT",
            "ZEST", "CORE", "HULL", "SHELL", "DREDGE", "COAT", "SEASON",
            "CARAMELIZE", "DEGLAZE", "EMULSIFY", "JULIENNE", "BRUNOISE",
            "TRUSS", "RENDER", "BROWN", "CHAR", "TORCH", "BAKE",
        ]),
        ("Dishes & Baking", [
            "SOUP", "STEW", "SALAD", "PASTA", "RICE", "BREAD", "PIE", "CAKE",
            "COOKIE", "MUFFIN", "PANCAKE", "OMELETTE", "CASSEROLE", "CURRY",
            "STIRFRY", "ROAST", "GRAVY", "DUMPLING", "QUICHE", "FRITTATA",
            "SANDWICH", "WRAP", "BURGER", "PIZZA", "TART", "PUDDING",
            "BISCUIT", "SCONE", "CRUMBLE", "FLAN", "LASAGNA", "RAVIOLI",
            "GNOCCHI", "RISOTTO", "FONDUE", "CHOWDER", "NOODLES", "TOFU",
            "STEAK", "CUTLET", "CROQUETTE", "FRITTER", "SAUSAGE", "BACON",
            "HAM", "PRAWN", "SHRIMP", "LOBSTER", "CRAB", "CLAM", "MUSSEL",
            "OYSTER", "SQUID", "CALAMARI", "TUNA", "SALMON", "TROUT",
            "HADDOCK", "ANCHOVY", "CAVIAR", "MEATBALL", "MEATLOAF", "HASH",
            "HOTDOG", "RIBS", "WINGS", "PATTY",
        ]),
        ("World Dishes", [
            "PAELLA", "GOULASH", "BORSCHT", "GAZPACHO", "SUSHI", "SASHIMI",
            "RAMEN", "UDON", "SOBA", "KEBAB", "FALAFEL", "SHAWARMA", "TACO",
            "BURRITO", "QUESADILLA", "ENCHILADA", "FAJITA", "NACHOS",
            "KORMA", "BIRYANI", "PILAF", "PULAO", "DAL", "SAMOSA", "PAKORA",
            "BHAJI", "DOSA", "IDLI", "VADA", "MOUSSAKA", "SOUVLAKI", "GYRO",
            "TAGINE", "COUSCOUS", "RENDANG", "SATAY", "LAKSA", "PHO",
            "BIBIMBAP", "KIMCHI", "BANHMI", "PIEROGI", "GOZLEME", "MOLE",
            "CEVICHE", "EMPANADA", "AREPA", "TAMALE", "POUTINE",
            "RATATOUILLE",
        ]),
        ("Baking & Sweets", [
            "FLOUR", "DOUGH", "BATTER", "YEAST", "LOAF", "ROLL", "BUN",
            "CRUST", "CRUMB", "ICING", "FROSTING", "SPRINKLE", "TOPPING",
            "FILLING", "LAYER", "PASTRY", "PUFF", "SHORTCRUST", "PHYLLO",
            "BRIOCHE", "CROISSANT", "BAGEL", "PRETZEL", "DONUT", "DOUGHNUT",
            "CRULLER", "ECLAIR", "TARTLET", "CUPCAKE", "BROWNIE", "BLONDIE",
            "CHEESECAKE", "TIRAMISU", "GATEAU", "COBBLER", "STRUDEL",
            "DANISH", "CRUMPET", "PANETTONE", "STOLLEN", "HOTCROSSBUN",
            "CINNAMONROLL", "BREADSTICK", "GRISSINI", "NAAN", "PITA",
            "TORTILLA", "CHAPATI", "ROTI", "PARATHA", "BAGUETTE",
            "FOCACCIA", "CIABATTA", "CRACKER", "RUSK", "BISCOTTI",
            "MACARON", "MACAROON", "MERINGUE", "WAFFLE", "CREPE",
            "SODABREAD", "CORNBREAD", "RYEBREAD", "BREADCRUMB", "CROUTON",
            "SHORTENING", "MARGARINE", "SUGAR", "HONEY", "SYRUP", "MOLASSES",
            "TREACLE", "AGAVE", "MAPLE", "CHOCOLATE", "CAROB", "BUTTERMILK",
            "EGGWHITE", "EGGYOLK", "BICARB", "BAKINGSODA", "BAKINGPOWDER",
            "CORNFLOUR", "CORNSTARCH", "RAISIN", "SULTANA", "MARZIPAN",
            "PRALINE", "NOUGAT", "FUDGE", "CARAMEL", "TOFFEE", "GANACHE",
            "TRUFFLE", "BONBON",
        ]),
        ("Dairy & Cheese", [
            "CREAM", "BUTTER", "CHEESE", "YOGURT", "YOGHURT", "KEFIR", "WHEY",
            "CURD", "PANEER", "RICOTTA", "MOZZARELLA", "PARMESAN", "CHEDDAR",
            "GOUDA", "BRIE", "CAMEMBERT", "FETA", "GOATCHEESE", "BLUECHEESE",
            "CREAMCHEESE", "COTTAGECHEESE", "MASCARPONE", "PROVOLONE",
            "EMMENTAL", "GRUYERE", "ROQUEFORT", "STILTON", "EDAM", "HAVARTI",
            "PECORINO", "ASIAGO", "MANCHEGO", "HALLOUMI", "BURRATA",
            "TALEGGIO", "FONTINA", "JARLSBERG", "RACLETTE", "CLOTTEDCREAM",
            "SOURCREAM", "GHEE", "LASSI",
        ]),
        ("Condiments & Sauces", [
            "KETCHUP", "MUSTARD", "MAYONNAISE", "RELISH", "CHUTNEY", "SALSA",
            "GUACAMOLE", "HUMMUS", "TAHINI", "TZATZIKI", "TAPENADE", "AIOLI",
            "SRIRACHA", "TABASCO", "SOYSAUCE", "HOISIN", "OYSTERSAUCE",
            "FISHSAUCE", "TERIYAKI", "BARBECUE", "HOLLANDAISE", "BEARNAISE",
            "BECHAMEL", "VINAIGRETTE", "PESTO", "RAGU", "MARINARA", "ALFREDO",
            "PEANUTSAUCE", "PLUMSAUCE", "DUCKSAUCE", "STEAKSAUCE", "HOTSAUCE",
            "CHILISAUCE", "APPLESAUCE", "MINTSAUCE", "TARTARE", "RAITA",
            "PICKLES", "OLIVE", "MARMALADE", "JAM", "JELLY", "PRESERVES",
            "COMPOTE", "LEMONCURD", "NUTELLA", "VEGEMITE", "MARMITE",
        ]),
        ("Grains & Pasta", [
            "OATS", "BARLEY", "RYE", "WHEAT", "QUINOA", "MILLET", "SPELT",
            "BUCKWHEAT", "FARRO", "FREEKEH", "BULGUR", "SEMOLINA", "POLENTA",
            "GRITS", "HOMINY", "AMARANTH", "TEFF", "SORGHUM", "CANE",
            "CEREAL", "MUESLI", "GRANOLA", "PORRIDGE", "OATMEAL",
            "SPAGHETTI", "FETTUCCINE", "LINGUINE", "PENNE", "RIGATONI",
            "FUSILLI", "MACARONI", "ORZO", "VERMICELLI", "FARFALLE",
            "ROTINI", "TORTELLINI", "TAGLIATELLE", "PAPPARDELLE",
            "CANNELLONI", "CAPELLINI",
        ]),
        ("Nuts & Seeds", [
            "ALMOND", "CASHEW", "WALNUT", "PECAN", "PISTACHIO", "HAZELNUT",
            "PEANUT", "BRAZILNUT", "MACADAMIA", "CHESTNUT", "PINENUT",
            "ACORN", "SUNFLOWER", "SESAME", "POPPY", "NIGELLA", "FLAX",
            "LINSEED", "CHIA", "HEMP", "PSYLLIUM", "LOTUS", "PUMPKINSEED",
            "WATERCHESTNUT",
        ]),
        ("Legumes & Beans", [
            "LENTIL", "CHICKPEA", "SOYBEAN", "BLACKBEAN", "REDBEAN", "MUNG",
            "ADZUKI", "LIMA", "NAVY", "PINTO", "KIDNEYBEAN", "CANNELLINI",
            "BUTTERBEAN", "BROADBEAN", "GREENBEAN", "RUNNERBEAN", "FAVA",
            "SPLITPEA", "TEMPEH", "LEGUME", "PULSE", "GRAM", "MOONG",
            "HARICOT",
        ]),
        ("Drinks & Tastes", [
            "WATER", "JUICE", "TEA", "COFFEE", "MILK", "SMOOTHIE", "LEMONADE",
            "COCOA", "CORDIAL", "BROTH", "SWEET", "SOUR", "SALTY", "SPICY",
            "BITTER", "SAVORY", "CREAMY", "CRISPY", "TENDER", "FRESH",
            "ROASTED", "STEAMED", "GRILLED", "BAKED", "FROZEN", "SODA",
            "COLA", "LIMEADE", "PUNCH", "MOCKTAIL", "SHAKE", "MILKSHAKE",
            "HOTCHOCOLATE", "ESPRESSO", "LATTE", "CAPPUCCINO", "MOCHA",
            "AMERICANO", "DECAF", "TISANE", "KOMBUCHA", "CHAI", "ICEDTEA",
            "CIDER", "PERRY", "MEAD", "ALE", "LAGER", "STOUT", "PORTER",
            "TODDY", "UMAMI", "TANGY", "ZESTY", "EARTHY", "NUTTY", "FRUITY",
            "BUTTERY", "GOOEY", "CHEWY", "CRUNCHY", "FLAKY", "MOIST", "RICH",
            "MILD", "PUNGENT", "AROMATIC", "FRAGRANT", "STODGY", "MELLOW",
            "ROBUST", "DELICATE", "SMOOTH", "GRAINY", "VELVETY", "SILKY",
            "JUICY", "SUCCULENT", "ACIDIC", "ZINGY",
        ]),
    ])
    trivia_easy = [
        {"q": "Which fruit is traditionally said to keep the doctor away?",
         "options": ["Apple", "Banana", "Grape"], "answer": "Apple"},
        {"q": "What do we call a person who cooks professionally?",
         "options": ["A chef", "A waiter", "A farmer"], "answer": "A chef"},
        {"q": "Which spice comes from the saffron flower?",
         "options": ["Saffron", "Pepper", "Salt"], "answer": "Saffron"},
        {"q": "Bread is mainly made from which grain?",
         "options": ["Wheat", "Rice", "Corn"], "answer": "Wheat"},
        {"q": "Which drink is made from roasted beans?",
         "options": ["Coffee", "Tea", "Juice"], "answer": "Coffee"},
        {"q": "Which vegetable is known to help you see in the dark?",
         "options": ["Carrot", "Potato", "Onion"], "answer": "Carrot"},
        {"q": "Which dairy product is churned to make butter?",
         "options": ["Cream", "Milk", "Cheese"], "answer": "Cream"},
        {"q": "Pasta is a famous food from which country?",
         "options": ["Italy", "Japan", "Mexico"], "answer": "Italy"},
        {"q": "Which sweet treat is made from cocoa?",
         "options": ["Chocolate", "Honey", "Caramel"], "answer": "Chocolate"},
        {"q": "Which kitchen tool is used to flip eggs?",
         "options": ["A spatula", "A whisk", "A ladle"], "answer": "A spatula"},
    ]
    phrase_medium = [
        {"prompt": "An apple a day keeps the ____ away", "answer": "Doctor"},
        {"prompt": "Too many cooks spoil the ____", "answer": "Broth"},
        {"prompt": "The proof of the pudding is in the ____", "answer": "Eating"},
        {"prompt": "Don't cry over spilt ____", "answer": "Milk"},
        {"prompt": "A piece of ____", "answer": "Cake"},
        {"prompt": "As cool as a ____", "answer": "Cucumber"},
        {"prompt": "Bring home the ____", "answer": "Bacon"},
        {"prompt": "Have your cake and ____ it", "answer": "Eat"},
    ]
    trivia_open = [
        {"q": "Name the Italian dish of flat dough with toppings.", "answer": "Pizza"},
        {"q": "What is the main ingredient in guacamole?", "answer": "Avocado"},
        {"q": "Which spice is the most expensive by weight?", "answer": "Saffron"},
        {"q": "What do you call a person who does not eat meat?", "answer": "A vegetarian"},
        {"q": "Which grain is used to make sushi?", "answer": "Rice"},
        {"q": "Name the hot drink made from leaves and boiling water.", "answer": "Tea"},
    ]
    crossword = [
        ("APPLE", "Round fruit, often red or green"),
        ("BREAD", "Baked food made from flour"),
        ("CHEF", "Professional cook"),
        ("SALT", "White seasoning from the sea"),
        ("MILK", "White drink from cows"),
        ("RICE", "Small white grain eaten across Asia"),
        ("PIZZA", "Italian flat dough with toppings"),
        ("CAKE", "Sweet baked treat for birthdays"),
        ("SOUP", "Hot liquid meal in a bowl"),
        ("EGG", "Oval food laid by hens"),
        ("HONEY", "Sweet golden stuff made by bees"),
        ("LEMON", "Yellow sour citrus fruit"),
        ("PASTA", "Italian noodles"),
        ("BUTTER", "Spread made from cream"),
        ("CHEESE", "Dairy food made from curdled milk"),
        ("SUGAR", "Sweet white grains"),
        ("COFFEE", "Hot drink from roasted beans"),
        ("ONION", "Layered vegetable that may make you cry"),
        ("CARROT", "Orange root vegetable"),
        ("PEPPER", "Hot spice or bell vegetable"),
        ("MANGO", "Sweet tropical orange fruit"),
        ("BASIL", "Fragrant green herb"),
        ("OVEN", "Appliance you bake food in"),
        ("WHEAT", "Grain used to make flour"),
        ("CREAM", "Rich top layer of milk"),
        ("MELON", "Large sweet fruit with seeds inside"),
        ("GRAPE", "Small fruit grown in bunches"),
        ("SALAD", "Cold dish of mixed vegetables"),
        ("CHILI", "Hot spicy pepper"),
        ("BERRY", "Small juicy fruit"),
    ]
    remedies = [
        {"condition": "Indigestion & Bloating",
         "text": "Chew a pinch of roasted cumin, coriander, and carom seeds "
                 "after a heavy meal, or sip warm ginger water. A glass of "
                 "spiced buttermilk with roasted cumin settles a full stomach. "
                 "Take a short, gentle walk and avoid lying down right after "
                 "eating."},
        {"condition": "Acidity & Heartburn",
         "text": "Sip cold milk in small amounts, eat a ripe banana, or chew a "
                 "few holy basil leaves. A small piece of jaggery (unrefined "
                 "cane sugar) and fennel-seed water help soothe the burn. Eat "
                 "smaller, slower meals and ease up on very spicy or fried food."},
        {"condition": "Hiccups",
         "text": "Swallow a spoon of dry sugar, sip cold water slowly, or hold "
                 "your breath for a few seconds. Chewing a couple of cardamom "
                 "pods is an old kitchen trick that often does the job. They "
                 "usually pass on their own within a few minutes."},
        {"condition": "Loss of Appetite",
         "text": "Try a little grated ginger with lemon juice and a pinch of "
                 "salt before meals, or chew some fennel seeds. Warm, freshly "
                 "cooked, smaller meals are easier to enjoy than cold or heavy "
                 "ones. A short walk before eating can also wake up the appetite."},
        {"condition": "Mouth Ulcers",
         "text": "Dab a little honey or a paste of turmeric and water on the "
                 "sore, or rinse with warm salt water. Chewing licorice root or "
                 "a cardamom pod soothes the sting. Avoid very spicy, salty, or "
                 "sour foods until it heals."},
        {"condition": "Golden Milk",
         "text": "Warm a cup of milk with a pinch of turmeric, a crack of black "
                 "pepper, and a little clarified butter (ghee); sip at bedtime. "
                 "This comforting golden nightcap is said to soothe the joints "
                 "and support restful sleep."},
        {"condition": "Digestive Seed Tea (Cumin-Coriander-Fennel)",
         "text": "Boil equal pinches of cumin, coriander, and fennel seeds in "
                 "water for a few minutes, then strain. Sipped warm after meals, "
                 "it settles bloating and helps food digest comfortably."},
    ]
    coloring = ["teapot", "flower", "sun", "leaf", "star", "record"]
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


BANKS = {"food": build}

"""Nature & the Great Outdoors - evergreen, all-country content bank."""
from __future__ import annotations
from collections import OrderedDict


def build() -> dict:
    word_pools = OrderedDict([
        ("Landforms & Terrain", [
            "MOUNTAIN", "VALLEY", "CANYON", "HILL", "CLIFF", "PLATEAU",
            "RIDGE", "DUNE", "MESA", "BUTTE", "PEAK", "SUMMIT", "GORGE",
            "RAVINE", "BLUFF", "ESCARPMENT", "FOOTHILL", "HILLTOP", "KNOLL",
            "BOULDER", "CRAG", "PLAINS", "DESERT", "TUNDRA", "SAVANNA",
            "GRASSLAND", "BADLANDS", "PENINSULA", "DELTA", "BASIN", "CRATER",
            "VOLCANO", "GEYSER", "FJORD", "PRAIRIE", "MEADOW", "MOOR",
            "HEATH", "BOG", "FEN", "GLADE", "VALE", "DELL", "HOLLOW",
            "GLEN", "PASS", "SADDLE", "SLOPE", "LEDGE", "TERRACE", "SCREE",
            "MORAINE", "LOWLAND", "UPLAND", "HIGHLAND", "HEADLAND", "CAPE",
            "PROMONTORY", "ISTHMUS", "ATOLL", "ARCHIPELAGO", "ISLAND",
            "ISLET", "COAST", "SHORE", "BEACH", "OASIS", "WADI", "ARROYO",
            "GULLY", "CHASM", "FLATLAND", "SHINGLE", "BARREN", "WILDERNESS",
            "OUTBACK",
        ]),
        ("Weather & Sky", [
            "THUNDER", "RAINBOW", "BREEZE", "LIGHTNING", "STORM", "CLOUD",
            "SUNSHINE", "RAINDROP", "TORNADO", "HURRICANE", "BLIZZARD",
            "DRIZZLE", "DOWNPOUR", "GUST", "GALE", "MONSOON", "FLURRY",
            "FROST", "MIST", "FOG", "HAIL", "SLEET", "SNOW", "SNOWFLAKE",
            "HUMIDITY", "TEMPERATURE", "BAROMETER", "CLIMATE", "FORECAST",
            "SUNSET", "SUNRISE", "DAWN", "DUSK", "AURORA", "CUMULUS", "WIND",
            "ZEPHYR", "SQUALL", "TEMPEST", "CYCLONE", "TYPHOON", "DROUGHT",
            "HEATWAVE", "ICICLE", "SNOWSTORM", "THUNDERSTORM", "OVERCAST",
            "HAZY", "MUGGY", "CRISP", "CHILLY", "FRIGID", "BALMY",
            "WINDCHILL", "DEW", "DEWDROP", "VAPOUR", "CONDENSATION",
            "ATMOSPHERE", "AIR", "OZONE", "SUNBEAM", "MOONBEAM", "HALO",
            "SUNDOG", "MIRAGE", "METEOROLOGY", "WATERSPOUT", "DUSTDEVIL",
            "HUMID", "ARID", "DAMP", "CLAMMY", "FAHRENHEIT", "CELSIUS",
            "ISOBAR", "ANEMOMETER", "HYGROMETER", "WEATHERVANE", "HORIZON",
            "ZENITH", "RAIN", "SNOWFALL", "SNOWPACK", "PERMAFROST",
        ]),
        ("Bodies of Water", [
            "RIVER", "LAKE", "OCEAN", "SEA", "STREAM", "POND", "WATERFALL",
            "CREEK", "BROOK", "BAY", "COVE", "HARBOR", "LAGOON", "ESTUARY",
            "INLET", "STRAIT", "CHANNEL", "GULF", "BAYOU", "MARSH", "SWAMP",
            "WETLAND", "RESERVOIR", "TIDEPOOL", "ICEBERG", "GLACIER",
            "CURRENT", "WAVE", "SPRING", "RAPIDS", "TRIBUTARY", "WATERSHED",
            "TARN", "LOCH", "PUDDLE", "EDDY", "WHIRLPOOL", "AQUIFER",
            "CASCADE", "CATARACT", "FLOOD", "FLOODPLAIN", "BANK", "BED",
            "MOUTH", "HEADWATER", "WATERFRONT", "PIER", "DOCK", "QUAY",
            "WHARF", "JETTY", "BREAKWATER", "SEAWALL", "TIDE", "BREAKER",
            "SWELL", "SURF", "FOAM", "BRINE", "SALTWATER", "FRESHWATER",
            "KETTLE", "BILLABONG", "SOUND", "BIGHT", "REEF", "SHOAL",
            "SANDBAR",
        ]),
        ("Trees & Forests", [
            "FOREST", "WOODLAND", "JUNGLE", "RAINFOREST", "TIMBER", "CANOPY",
            "GROVE", "THICKET", "UNDERGROWTH", "SAPLING", "EVERGREEN",
            "CONIFER", "BROADLEAF", "REDWOOD", "BAOBAB", "SEQUOIA", "BIRCH",
            "ASPEN", "CEDAR", "SPRUCE", "EUCALYPTUS", "MANGROVE", "BAMBOO",
            "WILLOW", "PINE", "OAK", "MAPLE", "BEECH", "ELM", "ASH", "FIR",
            "CHESTNUT", "SHRUB", "BRAMBLE", "FERN", "MOSS", "LICHEN", "BARK",
            "BRANCH", "TRUNK", "ROOT", "LEAF", "NEEDLE", "ACORN", "PINECONE",
            "RESIN", "LUMBER", "HEARTWOOD", "SAPWOOD", "BURL", "KNOT",
            "STUMP", "LOG", "BRUSH", "SCRUB", "TAIGA", "BOREAL", "COPSE",
            "COPPICE", "UNDERSTORY", "DECIDUOUS", "CONIFEROUS", "LEAFY",
            "TWIG", "SEEDLING", "HEMLOCK", "CYPRESS", "JUNIPER", "LARCH",
            "POPLAR", "ALDER", "HICKORY", "WALNUT", "SYCAMORE",
        ]),
        ("Wild Animals", [
            "BEAR", "DEER", "WOLF", "FOX", "MOOSE", "ELK", "BISON", "COYOTE",
            "BOBCAT", "LYNX", "COUGAR", "BADGER", "OTTER", "BEAVER",
            "RACCOON", "SKUNK", "PORCUPINE", "SQUIRREL", "HARE", "ANTELOPE",
            "PUMA", "JAGUAR", "LEOPARD", "TIGER", "ELEPHANT", "GIRAFFE",
            "ZEBRA", "CAMEL", "KANGAROO", "KOALA", "PANDA", "MONKEY",
            "GORILLA", "BIGHORN", "LION", "CHEETAH", "HYENA", "JACKAL",
            "BABOON", "CHIMP", "ORANGUTAN", "RHINO", "HIPPO", "WARTHOG",
            "BUFFALO", "WILDEBEEST", "OKAPI", "TAPIR", "SLOTH", "ANTEATER",
            "ARMADILLO", "MARMOT", "GROUNDHOG", "PIKA", "VOLE", "LEMMING",
            "WEASEL", "STOAT", "MARTEN", "MINK", "WOLVERINE", "FERRET",
            "MUSKRAT", "NUTRIA", "CAPYBARA", "ALPACA", "LLAMA", "MUSKOX",
            "CARIBOU", "REINDEER", "GAZELLE", "IMPALA", "ELAND", "ORYX",
            "IBEX", "TAHR", "BOAR", "LEMUR", "GIBBON", "MANATEE", "DUGONG",
            "PLATYPUS", "ECHIDNA", "POSSUM", "WALLABY", "WOMBAT", "EAGLE",
            "HAWK", "FALCON", "OWL", "OSPREY", "CONDOR", "VULTURE",
            "KESTREL", "RAVEN", "MAGPIE", "LIZARD", "SNAKE", "VIPER",
            "COBRA", "PYTHON", "GECKO", "IGUANA", "CROCODILE", "ALLIGATOR",
            "TURTLE", "TORTOISE", "FROG", "TOAD", "SALAMANDER", "NEWT",
            "CHAMELEON", "RATTLESNAKE",
        ]),
        ("Outdoor Activities", [
            "HIKING", "CAMPING", "FISHING", "CLIMBING", "KAYAKING",
            "CANOEING", "SAILING", "SURFING", "SWIMMING", "DIVING", "SKIING",
            "TREKKING", "ORIENTEERING", "BIRDWATCHING", "FORAGING",
            "PHOTOGRAPHY", "STARGAZING", "CAMPFIRE", "TENT", "SLEEPINGBAG",
            "COMPASS", "BINOCULARS", "THERMOS", "CANTEEN", "FLASHLIGHT",
            "KNAPSACK", "TARP", "HAMMOCK", "BACKPACKING", "BUSHWHACKING",
            "ROCKCLIMBING", "RAFTING", "TUBING", "PADDLING", "ROWING",
            "BOATING", "SNOWSHOEING", "SNOWBOARDING", "BOULDERING",
            "CYCLING", "BIKING", "JOGGING", "GEOCACHING", "NATUREWALK",
            "HUNTING", "TRAPPING", "ARCHERY", "ANGLING", "FLYFISHING",
            "SNORKELING", "SCUBA", "BODYBOARDING", "WATERSKIING",
            "KITESURFING", "WINDSURFING", "PARAGLIDING", "HANGGLIDING",
            "SKYDIVING", "BALLOONING", "GLIDING", "CAVING", "SPELUNKING",
            "BACKPACK", "RUCKSACK", "DAYPACK", "WATERBOTTLE", "LANTERN",
            "KINDLING", "FIREWOOD", "TINDER", "FLINT", "SLEEPINGPAD", "MAP",
            "WALKIETALKIE", "FIRSTAID", "SUNSCREEN", "REPELLENT", "RAINCOAT",
            "PARKA", "BOOTS", "CAMPSTOVE",
        ]),
        ("Geology & Earth", [
            "ROCK", "MINERAL", "CAVE", "CRYSTAL", "GRANITE", "MARBLE",
            "SANDSTONE", "LIMESTONE", "SHALE", "BASALT", "OBSIDIAN", "QUARTZ",
            "GARNET", "AMETHYST", "AGATE", "STALACTITE", "STALAGMITE",
            "GROTTO", "CREVASSE", "FAULT", "EARTHQUAKE", "LAVA", "MAGMA",
            "BEDROCK", "SEDIMENT", "FOSSIL", "EROSION", "TECTONIC",
            "CONTINENT", "TOPAZ", "DIAMOND", "EMERALD", "RUBY", "SAPPHIRE",
            "OPAL", "JADE", "TURQUOISE", "JASPER", "ONYX", "FLINT", "PUMICE",
            "GNEISS", "SCHIST", "SLATE", "QUARTZITE", "DIORITE", "GABBRO",
            "HALITE", "GYPSUM", "CALCITE", "PYRITE", "CLAY", "GRAVEL",
            "PEBBLE", "COBBLE", "ORE", "VEIN", "LODE", "QUARRY", "SHAFT",
            "TUNNEL", "STRATA", "LAYER", "OUTCROP", "MONOLITH", "HOODOO",
            "GEODE", "ANDESITE", "RHYOLITE", "HEMATITE", "COPPER", "SILVER",
            "IRON", "COAL", "PEAT",
        ]),
        ("Sky & Space", [
            "MOON", "STAR", "PLANET", "COMET", "GALAXY", "CONSTELLATION",
            "METEOR", "ASTEROID", "NEBULA", "SATELLITE", "ECLIPSE", "ORBIT",
            "TWILIGHT", "COSMOS", "UNIVERSE", "JUPITER", "SATURN", "VENUS",
            "MARS", "MERCURY", "NEPTUNE", "URANUS", "SOLAR", "LUNAR",
            "ZODIAC", "TELESCOPE", "STARDUST", "METEORITE", "SUN", "EARTH",
            "SUNSPOT", "SOLARFLARE", "SOLSTICE", "EQUINOX", "NADIR",
            "MERIDIAN", "HEMISPHERE", "ECLIPTIC", "GRAVITY", "LIGHTYEAR",
            "SUPERNOVA", "PULSAR", "QUASAR", "ASTRONOMY", "ASTRONAUT",
            "SPACECRAFT", "ROCKET", "PROBE", "ROVER", "ORBITAL", "MAGNITUDE",
            "PARALLAX", "GALACTIC", "CELESTIAL", "COSMIC", "INTERSTELLAR",
            "ASTEROIDBELT",
        ]),
    ])
    trivia_easy = [
        {"q": "What do we call water that falls from clouds?",
         "options": ["Rain", "Wind", "Sand"], "answer": "Rain"},
        {"q": "Which of these is a large body of salt water?",
         "options": ["An ocean", "A puddle", "A pond"], "answer": "An ocean"},
        {"q": "What is the tallest kind of landform?",
         "options": ["A mountain", "A valley", "A plain"], "answer": "A mountain"},
        {"q": "Which weather event is a spinning funnel of wind?",
         "options": ["A tornado", "A rainbow", "A breeze"], "answer": "A tornado"},
        {"q": "What do trees mostly use to make their food?",
         "options": ["Sunlight", "Soil", "Rocks"], "answer": "Sunlight"},
        {"q": "Which bright arc often appears in the sky after rain?",
         "options": ["A rainbow", "A cloud", "Fog"], "answer": "A rainbow"},
        {"q": "What do we call a scientist who studies rocks?",
         "options": ["A geologist", "A biologist", "A chemist"], "answer": "A geologist"},
        {"q": "Which of these is a slow-moving mass of ice?",
         "options": ["A glacier", "A river", "A desert"], "answer": "A glacier"},
        {"q": "What is the planet we live on called?",
         "options": ["Earth", "Mars", "Venus"], "answer": "Earth"},
        {"q": "Which outdoor activity means walking long trails in nature?",
         "options": ["Hiking", "Fishing", "Skiing"], "answer": "Hiking"},
        {"q": "Which flash of light is usually followed by thunder?",
         "options": ["Lightning", "A rainbow", "Fog"], "answer": "Lightning"},
        {"q": "Which big cat is known as the king of the jungle?",
         "options": ["The lion", "The wolf", "The bear"], "answer": "The lion"},
    ]
    phrase_medium = [
        {"prompt": "Every cloud has a silver ____", "answer": "Lining"},
        {"prompt": "It never rains but it ____", "answer": "Pours"},
        {"prompt": "A bolt from the ____", "answer": "Blue"},
        {"prompt": "The calm before the ____", "answer": "Storm"},
        {"prompt": "Make hay while the sun ____", "answer": "Shines"},
        {"prompt": "A breath of fresh ____", "answer": "Air"},
        {"prompt": "Still waters run ____", "answer": "Deep"},
        {"prompt": "Let nature take its ____", "answer": "Course"},
        {"prompt": "As right as ____", "answer": "Rain"},
        {"prompt": "A mountain to ____", "answer": "Climb"},
    ]
    trivia_open = [
        {"q": "Name the highest mountain on Earth.", "answer": "Mount Everest"},
        {"q": "What do we call a deep, narrow valley with steep rocky sides?",
         "answer": "A canyon"},
        {"q": "Which large mammal is famous for building dams in rivers?",
         "answer": "The beaver"},
        {"q": "What natural process turns liquid water into vapor?",
         "answer": "Evaporation"},
        {"q": "Name the star at the center of our solar system.",
         "answer": "The Sun"},
        {"q": "What do we call a scientist who studies the weather?",
         "answer": "A meteorologist"},
        {"q": "Which slow-moving mass of ice carves out valleys over time?",
         "answer": "A glacier"},
        {"q": "What is the name of the galaxy we live in?",
         "answer": "The Milky Way"},
    ]
    crossword = [
        ("MOUNTAIN", "Towering landform, higher than a hill"),
        ("VALLEY", "Low land between hills or mountains"),
        ("CANYON", "Deep gorge with steep rocky sides"),
        ("RIVER", "Flowing body of fresh water"),
        ("OCEAN", "Huge body of salt water"),
        ("FOREST", "Large area thick with trees"),
        ("THUNDER", "Loud rumble that follows lightning"),
        ("RAINBOW", "Colorful arc seen after rain"),
        ("STORM", "Wild weather with wind and rain"),
        ("BREEZE", "Gentle, light wind"),
        ("GLACIER", "Slow-moving river of ice"),
        ("VOLCANO", "Mountain that can erupt with lava"),
        ("BOULDER", "Very large, rounded rock"),
        ("MOOSE", "Large antlered animal of northern forests"),
        ("EAGLE", "Majestic bird of prey"),
        ("BEAR", "Large furry mammal that hibernates"),
        ("DEER", "Graceful animal, the male grows antlers"),
        ("WOLF", "Wild canine that howls"),
        ("HIKING", "Walking for pleasure on trails"),
        ("CAMPFIRE", "Outdoor fire for warmth and cooking"),
        ("TENT", "Portable shelter used when camping"),
        ("COMPASS", "Tool with a needle that points north"),
        ("MINERAL", "Naturally occurring solid from the earth"),
        ("CRYSTAL", "Sparkling, structured solid like quartz"),
        ("MOON", "Earth's natural satellite"),
        ("COMET", "Icy space object with a glowing tail"),
        ("ECLIPSE", "When one body blocks light from another"),
        ("GEYSER", "Hot spring that erupts with steam"),
        ("WATERFALL", "Where a river plunges over a cliff"),
        ("TUNDRA", "Cold, treeless northern plain"),
        ("DESERT", "Dry, sandy, often hot region"),
        ("SAVANNA", "Grassy plain with scattered trees"),
    ]
    remedies = [
        {"condition": "Sun-Warmed Skin",
         "text": "Cool the skin with damp cloths or a cool shower, then soothe "
                 "with aloe vera gel or cool milk compresses. Sip plenty of water "
                 "and stay in the shade while it settles. Seek help for "
                 "widespread redness, blisters, or feeling unwell."},
        {"condition": "Prickly Heat",
         "text": "Take cool baths with a little neem or rose water, and dust "
                 "lightly with starch powder. Drink cool water and buttermilk, "
                 "and wear loose cotton to let the skin breathe. A cool, airy "
                 "spot brings quick relief."},
        {"condition": "Puffy, Swollen Feet",
         "text": "Rest with your feet raised, then soak them in cool water with "
                 "a little rock salt and massage gently upward. A cup of turmeric-"
                 "ginger tea supports healthy circulation. Comfortable shoes and "
                 "short rest stops help on long days out."},
        {"condition": "Tired Outdoor Eyes",
         "text": "Rest cool cucumber slices or rosewater-soaked cotton pads over "
                 "closed eyes for a few minutes. Gentle palming, warm palms cupped "
                 "over the eyes, and fresh-air breaks refresh tired sight. A hat "
                 "and sunglasses ease the glare."},
        {"condition": "Pollen Sneezing",
         "text": "Rinse your face and hands after being outdoors, and sip warm "
                 "ginger-holy basil tea. Steam with a little eucalyptus clears a "
                 "tickly nose. Airing rooms and a spoon of local honey are old "
                 "folk helps."},
        {"condition": "Roasted Chickpea-Flour Drink (Sattu)",
         "text": "Mix roasted chickpea flour into cool water with lemon, roasted "
                 "cumin, and a pinch of salt. A refreshing summer drink from "
                 "northern India that fills you up and cools you down."},
        {"condition": "Spiced Buttermilk",
         "text": "Blend yogurt with water, roasted cumin, curry leaves, ginger, "
                 "and a pinch of salt. This cooling savory drink aids digestion "
                 "and refreshes you on warm days outdoors."},
    ]
    coloring = ["sun", "star", "leaf", "flower", "butterfly", "bird"]
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


BANKS = {"nature": build}

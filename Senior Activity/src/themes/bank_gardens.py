"""Gardens, Flowers & Birds - FULL-SPEC evergreen, all-country content bank.

Sized for the full 180-puzzle preset: ~540 unique word-search words, 10 MC
trivia, 8 finish-the-phrase, 6 open recall, a 30+ crossword clue bank, 7
detailed remedies, and coloring keys. No decade/era/country-specific refs.
Words are single A-Z tokens (<=13 letters) to fit large-print grids.
"""
from __future__ import annotations
from collections import OrderedDict


def build() -> dict:
    word_pools = OrderedDict([
        ("Flowers", [
            "ROSE", "TULIP", "DAISY", "LILY", "ORCHID", "JASMINE", "LOTUS",
            "SUNFLOWER", "DAFFODIL", "IRIS", "POPPY", "VIOLET", "MARIGOLD",
            "LAVENDER", "HIBISCUS", "CARNATION", "PETUNIA", "PRIMROSE",
            "DAHLIA", "PANSY", "ZINNIA", "SNAPDRAGON", "FOXGLOVE", "HOLLYHOCK",
            "FORSYTHIA", "HYACINTH", "NASTURTIUM", "LUPINE", "PEONY", "BEGONIA",
            "GERANIUM", "FUCHSIA", "AZALEA", "CAMELLIA", "MAGNOLIA",
            "WISTERIA", "GARDENIA", "ANEMONE", "CLEMATIS", "COSMOS", "ASTER",
            "YARROW", "ECHINACEA", "LANTANA", "VERBENA", "DIANTHUS", "STOCK",
            "LOBELIA", "IMPATIENS", "COLEUS", "ALLIUM", "PHLOX", "SALVIA",
            "PENSTEMON", "HELLEBORE", "CALENDULA", "LARKSPUR", "DELPHINIUM",
            "FREESIA", "GAILLARDIA", "GAZANIA", "SWEETPEA", "CORNFLOWER",
            "SNOWDROP", "CROCUS", "BLUEBELL", "DAISY",  # daisy dup guard below
            "PRIMULA", "PANSY", "VIOLA", "AGERATUM", "ALYSSUM", "AMARANTH",
            "BORAGE", "CANDYTUFT", "CLARKIA", "GODETIA", "LINARIA", "NIGELLA",
            "SCABIOUS", "STOCK", "SWEETWILLIAM", "WALLFLOWER", "MONARDA",
            "RUDBECKIA", "COREOPSIS", "GYPSOPHILA", "LIATRIS",
            "VERONICA", "AUBRIETA", "CERASTIUM",
            "LUPIN", "MIMULUS", "TUBEROSE", "VALERIAN", "AGAPANTHUS",
            "ARUM", "BELLFLOWER", "BROOM", "BUGLE", "CATCHFLY", "DICENTRA",
            "EPIMEDIUM", "GENTIAN", "GERBERA", "HEUCHERA", "HOLLY", "HOSTA",
            "ICEPLANT", "JACOBEAN", "KNAUTIA", "LADY", "LUNGWORT",
            "MALLOW", "MEXICAN", "MONTBRETIA", "NEMOPHILA", "OREGANO",
            "PENNYCRESS", "PYRETHRUM", "QUINCE", "ROCKROSE", "SEAHOLLY",
            "TORCHLILY", "VINCA", "WANDFLOWER",
        ]),
        ("Birds", [
            "ROBIN", "SPARROW", "EAGLE", "OWL", "PIGEON", "SWAN", "CROW",
            "PEACOCK", "PARROT", "FLAMINGO", "FALCON", "HAWK", "DUCK",
            "SWALLOW", "FINCH", "WREN", "HERON", "SEAGULL", "GOLDFINCH",
            "BLUEBIRD", "CARDINAL", "MAGPIE", "RAVEN", "BLACKBIRD", "CUCKOO",
            "WOODPECKER", "NIGHTINGALE", "KINGFISHER", "HUMMINGBIRD", "ORIOLE",
            "STARLING", "THRUSH", "LARK", "MEADOWLARK", "JAY", "BLUEJAY",
            "NUTHATCH", "TITMOUSE", "CATBIRD", "CHAT",
            "CROSSBILL", "DIPPER", "FLYCATCHER", "GOLDCREST", "GREBE",
            "GROUSE", "GULL", "HARRIER", "HOBBY", "IBIS", "JUNCO",
            "KESTREL", "KITE", "KIWI", "LAPWING", "LONGSPUR", "LOON",
            "MARTIN", "MERLIN", "MOORHEN", "NODDY", "OSPREY", "OYSTERCATCHER",
            "PARAKEET", "PARTRIDGE", "PHOEBE", "PIPIT", "PLOVER", "PUFFIN",
            "QUAIL", "REDSTART", "SANDPIPER", "SHRIKE", "SISKIN", "SNIPE",
            "STORK", "SWIFT", "TEAL", "TERN", "TOUCAN", "TURNSTONE",
            "VULTURE", "WAGTAIL", "WARBLER", "WAXWING", "WHEATEAR",
            "WOODCOCK", "YELLOWHAMMER",
        ]),
        ("Trees & Shrubs", [
            "OAK", "PINE", "MAPLE", "WILLOW", "BAMBOO", "PALM", "CEDAR",
            "BIRCH", "SPRUCE", "POPLAR", "ASH", "BEECH", "ELM", "FIR",
            "CHESTNUT", "WALNUT", "ALMOND", "HAZEL", "ROWAN", "HAWTHORN",
            "JUNIPER", "YEW", "LARCH", "REDWOOD", "SYCAMORE", "EUCALYPTUS",
            "CACTUS", "FIG", "OLIVE", "PECAN", "PLUM", "APPLE",
            "PEAR", "CHERRY", "LEMON", "ORANGE", "PEACH", "MULBERRY",
            "POMEGRANATE", "BUCKTHORN", "BUCKEYE", "CASHEW", "CYPRESS",
            "DOGWOOD", "ELDER", "GINKGO", "HICKORY", "HORSECHESTNUT",
            "LABURNUM", "LAUREL", "LILAC", "LOCUST", "MACADAMIA", "MANGO",
            "MESQUITE", "PAPAYA", "PISTACHIO", "PLANE", "POINCIANA",
            "SOURWOOD", "SWEETGUM", "TAMARIND", "TEAK", "TULIPTREE",
            "WALNUT", "WATTLE",
        ]),
        ("Herbs", [
            "BASIL", "MINT", "ROSEMARY", "THYME", "SAGE", "PARSLEY", "DILL",
            "CORIANDER", "OREGANO", "CHIVES", "TARRAGON", "BAY", "MARJORAM",
            "LEMONGRASS", "FENNEL", "CHAMOMILE", "CILANTRO", "SORREL",
            "BURDOCK", "CATNIP", "COMFREY", "ECHINACEA", "FEVERFEW",
            "GARLIC", "HYSSOP", "LAVENDER", "LEMONBALM", "LOVAGE",
            "MELISSA", "PENNYROYAL", "ROOIBOS", "RUE", "SAFFRON", "SALMONBERRY",
            "SUMAC", "SWEETCICELY", "VALERIAN", "VERVAIN", "WATERCRESS",
            "WORMWOOD", "YARROW",
        ]),
        ("Fruits & Vegetables", [
            "TOMATO", "CARROT", "POTATO", "ONION", "GARLIC", "LETTUCE",
            "CABBAGE", "BROCCOLI", "CAULIFLOWER", "SPINACH", "BEAN", "PEA",
            "CUCUMBER", "PUMPKIN", "SQUASH", "ZUCCHINI", "PEPPER", "RADISH",
            "TURNIP", "BEETROOT", "CELERY", "LEEK", "KALE", "COURGETTE",
            "ASPARAGUS", "ARTICHOKE", "AUBERGINE", "RHUBARB", "SWEETCORN",
            "SCALLION", "SHALLOT", "PARSNIP", "SWEDE", "OKRA", "MELON",
            "STRAWBERRY", "BLUEBERRY", "RASPBERRY", "BLACKBERRY", "CURRANT",
            "GOOSEBERRY", "CRANBERRY", "GRAPE", "APPLE", "PEAR", "PLUM",
            "CHERRY", "PEACH", "APRICOT", "FIG", "QUINCE", "MANGO",
            "PINEAPPLE", "PAPAYA", "POMEGRANATE", "BLACKCURRANT",
            "STONEFRUIT", "BROADBEAN", "MANGETOUT", "WATERCRESS",
        ]),
        ("In the Garden (tools, parts, actions)", [
            "SHOVEL", "RAKE", "SPADE", "HOE", "SHEARS", "WHEELBARROW",
            "WATERINGCAN", "COMPOST", "MULCH", "TRELLIS", "SEEDS", "SOIL",
            "ROOT", "LEAF", "STEM", "BUD", "LAWN", "HEDGE", "GREENHOUSE",
            "HOSE", "PRUNER", "TROWEL", "FORK", "SECATEURS", "WATERBUTT",
            "POTS", "TRAY", "CAN", "GLOVES", "BOOTS", "HAT", "APRON",
            "WHEELHOE", "EDGER", "AERATOR", "CULTIVATOR", "DIBBER",
            "PLANTER", "WINDOWBOX", "CLIMBER", "PERENNIAL", "ANNUAL",
            "BIENNIAL", "BULB", "CORM", "TUBER", "RHIZOME", "STOLON",
            "TENDRIL", "THORN", "PRICKLE", "PETAL", "SEPAL", "STAMEN",
            "PISTIL", "POLLEN", "NECTAR", "BLOSSOM", "SHOOT", "RUNNER",
            "SUCKER", "DEADHEAD", "TRANSPLANT", "PROPAGATE", "PRUNE",
            "WATER", "WEED", "DIG", "SOW", "HARVEST", "MULCH", "AERATE",
            "COMPOST", "FERTILIZE", "REPOT", "GRAFT", "LAYERING",
        ]),
        ("Garden Creatures", [
            "BUTTERFLY", "BEE", "LADYBUG", "DRAGONFLY", "ANT", "CRICKET",
            "GRASSHOPPER", "CATERPILLAR", "BEETLE", "MOTH", "SPIDER", "FROG",
            "TOAD", "HEDGEHOG", "WORM", "SNAIL", "SLUG", "CENTIPEDE",
            "EARTHWORM", "LADYBIRD", "WASP", "HOVERFLY", "LACEWING",
            "MASONBEE", "BUMBLEBEE", "LEAFHOPPER", "SHIELDBUG", "STINKBUG",
            "FIREFLY", "CICADA", "MANTIS", "APHID", "WHITEFLY", "EARWIG",
            "WOODLOUSE", "MILLIPEDE", "BEETLE", "GRUB", "MAGGOT", "PUPA",
            "COCOON", "CHRYSALIS", "HIVE", "NEST", "WEB", "HONEY",
            "WAX", "COMB", "QUEEN", "DRONE", "WORKER", "FORAGER",
        ]),
        ("Nature & Weather", [
            "SUNSHINE", "RAINBOW", "BREEZE", "DEW", "BLOSSOM", "MEADOW",
            "POND", "STREAM", "RIVER", "LAKE", "HILL", "VALLEY", "FOREST",
            "WOODLAND", "FIELD", "HEDGEROW", "ORCHARD", "PRAIRIE", "MARSH",
            "BOG", "FEN", "MOOR", "GROVE", "COPSE", "THICKET", "GLADE",
            "CLEARING", "TRAIL", "PATH", "GATE", "STILE", "FENCE", "WALL",
            "STONE", "ROCK", "PEBBLE", "SAND", "CLAY", "LOAM", "CHALK",
            "PEAT", "GRIT", "MULCH", "COMPOST", "HUMUS", "WORMCAST",
            "RAINDROP", "MIST", "FOG", "FROST", "SNOW", "HAIL", "SLEET",
            "THUNDER", "LIGHTNING", "SUNSET", "SUNRISE", "DAWN", "DUSK",
            "SHADE", "SHADOW", "SEASON", "SPRING", "SUMMER", "AUTUMN",
            "WINTER", "BLOOM", "GROWTH", "HARVEST", "BUDDING",
        ]),
    ])

    trivia_easy = [
        {"q": "What do bees collect from flowers?",
         "options": ["Nectar", "Pollen dust", "Rain water"], "answer": "Nectar"},
        {"q": "Which flower is the classic symbol of love?",
         "options": ["Rose", "Cactus", "Tulip"], "answer": "Rose"},
        {"q": "What is a young butterfly called before it has wings?",
         "options": ["Caterpillar", "Tadpole", "Chick"], "answer": "Caterpillar"},
        {"q": "Which bird is famous for copying human speech?",
         "options": ["Parrot", "Owl", "Eagle"], "answer": "Parrot"},
        {"q": "Which tree produces acorns?",
         "options": ["Oak", "Pine", "Palm"], "answer": "Oak"},
        {"q": "Which part of a plant draws water up from the soil?",
         "options": ["The root", "The petal", "The thorn"], "answer": "The root"},
        {"q": "Which insect makes honey?",
         "options": ["Bee", "Ant", "Fly"], "answer": "Bee"},
        {"q": "What do we call a group of bees living together?",
         "options": ["A hive", "A flock", "A pod"], "answer": "A hive"},
        {"q": "Which part of a plant catches sunlight to make food?",
         "options": ["The leaf", "The root", "The bark"], "answer": "The leaf"},
        {"q": "What is the sweet liquid flowers make to attract bees?",
         "options": ["Nectar", "Sap", "Resin"], "answer": "Nectar"},
    ]

    phrase_medium = [
        {"prompt": "Stop and smell the ____", "answer": "Roses"},
        {"prompt": "As busy as a ____", "answer": "Bee"},
        {"prompt": "Birds of a feather ____ together", "answer": "Flock"},
        {"prompt": "Every rose has its ____", "answer": "Thorn"},
        {"prompt": "The early bird catches the ____", "answer": "Worm"},
        {"prompt": "April showers bring May ____", "answer": "Flowers"},
        {"prompt": "As free as a ____", "answer": "Bird"},
        {"prompt": "A thing of beauty is a ____ forever", "answer": "Joy"},
    ]

    trivia_open = [
        {"q": "Name the tall flower that turns to face the sun.",
         "answer": "Sunflower"},
        {"q": "Which spring bulb flower is strongly linked to the Netherlands?",
         "answer": "Tulip"},
        {"q": "What do you call a scientist who studies plants?",
         "answer": "A botanist"},
        {"q": "Which tiny bird can fly backwards?",
         "answer": "Hummingbird"},
        {"q": "What is the process by which plants make food using sunlight?",
         "answer": "Photosynthesis"},
        {"q": "Which creature spins a web to catch insects?",
         "answer": "Spider"},
    ]

    crossword = [
        ("ROSE", "Romantic flower, usually red"),
        ("TULIP", "Cup-shaped spring flower tied to the Netherlands"),
        ("DAISY", "White petals around a yellow center"),
        ("LILY", "Trumpet-shaped, often fragrant flower"),
        ("SUNFLOWER", "Tall bloom that faces the sun"),
        ("ROBIN", "Red-breasted garden bird"),
        ("SPARROW", "Small, common brown bird"),
        ("OWL", "Nocturnal bird that hoots"),
        ("PARROT", "Colorful bird that can mimic speech"),
        ("EAGLE", "Large, powerful bird of prey"),
        ("BEE", "Honey-making insect"),
        ("OAK", "Tree that bears acorns"),
        ("PINE", "Conifer with needle-shaped leaves"),
        ("SEED", "A plant's starting point"),
        ("SOIL", "Earth that plants grow in"),
        ("ROOT", "Part that anchors a plant and drinks water"),
        ("LEAF", "Green organ that catches sunlight"),
        ("BUD", "Young shoot that opens into a flower"),
        ("LAWN", "Mown grass area"),
        ("HOSE", "Flexible tube for watering"),
        ("POND", "Small body of water in a garden"),
        ("HEDGE", "Line of shrubs forming a boundary"),
        ("WEED", "Unwanted plant"),
        ("MULCH", "Layer spread on soil to keep it moist"),
        ("COMPOST", "Rotting plant matter that feeds the soil"),
        ("FERN", "Leafy, shade-loving plant"),
        ("FROG", "Hopping creature often found by a pond"),
        ("WORM", "Wriggling helper that airs the soil"),
        ("WREN", "Tiny garden bird with a loud voice"),
        ("IVY", "Climbing evergreen vine"),
        ("MOSS", "Soft green growth on damp ground"),
        ("BARK", "A tree's outer covering"),
        ("THORN", "Sharp point on a rose stem"),
        ("PETAL", "Colorful leaf of a flower"),
        ("NECTAR", "Sweet liquid flowers make for bees"),
        ("POD", "Case that holds peas or beans"),
        ("ACORN", "The oak tree's seed"),
        ("FROST", "Thin white ice on a cold morning"),
        ("RAIN", "Water that falls from clouds"),
        ("BIRD", "Feathered animal that lays eggs"),
    ]

    remedies = [
        {"condition": "Minor Burns",
         "text": "Right away, hold the spot under cool (not ice-cold) running "
                 "water for several minutes, then smooth on fresh aloe vera gel "
                 "from the leaf. A light coating of honey also soothes the skin. "
                 "Keep it clean and dry, and see a professional for any "
                 "blistering or large burns."},
        {"condition": "Itchy Skin & Rashes",
         "text": "Apply a paste of neem leaves or a cool compress of coriander-"
                 "seed water to calm the irritation. Aloe vera gel or a little "
                 "coconut oil also brings relief. Try not to scratch, and keep "
                 "the skin cool and clean."},
        {"condition": "Minor Cuts & Grazes",
         "text": "Rinse the little cut with clean water to wash away grit, then "
                 "pat dry. A dab of turmeric paste, an old wound-care habit, and "
                 "a clean cover help it heal. Check each day for redness, heat, "
                 "or pus, which mean it needs more care."},
        {"condition": "Insect Bites",
         "text": "Wash the spot with cool water and soap, then apply a paste of "
                 "neem or holy basil leaves, or rest a slice of raw onion on it. "
                 "A cold, damp cloth eases the swelling. Try not to scratch so "
                 "it can heal cleanly."},
        {"condition": "Gardener's Back Ache",
         "text": "Massage the lower back with warm sesame oil, then rest with a "
                 "warm compress on the sore area. A cup of turmeric milk at "
                 "bedtime eases stiff muscles. Bend at the knees when lifting "
                 "and pace the gardening through the day."},
        {"condition": "Holy Basil (Tulsi) Tea",
         "text": "Steep a few holy basil leaves in hot water for a few minutes, "
                 "then add honey to taste. This gentle golden-green tea is a "
                 "daily support for calm and a steady sense of wellbeing."},
        {"condition": "Soft Rice-and-Lentil Porridge (Khichdi)",
         "text": "Cook rice and mung lentils soft with clarified butter, cumin, "
                 "and turmeric. This light, warming meal is easy to digest and "
                 "just right when the body needs gentle nourishment."},
    ]

    coloring = ["flower", "bird", "butterfly", "wateringcan", "sun", "leaf"]

    return {
        "word_pools": _dedup_pools(word_pools),
        "trivia_easy": trivia_easy,
        "phrase_medium": phrase_medium,
        "trivia_open": trivia_open,
        "crossword": crossword,
        "remedies": remedies,
        "remedies_title": "Home Remedies & Wellness Wisdom",
        "coloring": coloring,
    }


# de-duplicate helper used at build time; guarantees no repeated tokens within
# the word-search pool (the assembler also enforces this across the book).
def _dedup_pools(pools):
    seen, out = set(), OrderedDict()
    for cat, words in pools.items():
        clean = []
        for w in words:
            wu = w.upper()
            if wu.isalpha() and 3 <= len(wu) <= 13 and wu not in seen:
                seen.add(wu)
                clean.append(wu)
        out[cat] = clean
    return out


BANKS = {"gardens": build}

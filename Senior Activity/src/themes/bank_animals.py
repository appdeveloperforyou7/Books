"""Animals & Pets - evergreen, all-country content bank."""
from __future__ import annotations
from collections import OrderedDict


def build() -> dict:
    word_pools = OrderedDict([
        ("Pets & Companions", [
            "DOG", "CAT", "RABBIT", "HAMSTER", "GUINEAPIG", "PARROT",
            "GOLDFISH", "KITTEN", "PUPPY", "CANARY", "TURTLE", "FERRET",
            "GERBIL", "CHINCHILLA", "POODLE", "TERRIER", "SPANIEL", "COLLIE",
            "TABBY", "PARAKEET", "COCKATIEL", "GUPPY", "FINCH", "BUDGIE",
            "HOUND", "RETRIEEVER", "SETTER", "BEAGLE", "MASTIFF", "SHEPHERD",
            "DACHSHUND", "DALMATIAN", "PUG", "POMERANIAN", "GREYHOUND",
            "POOCH", "MUTT", "LAPDOG",
            "SIAMESE", "PERSIAN", "MANX", "RAGDOLL", "SPHYNX", "BENGAL",
            "LOVEBIRD", "COCKATOO", "MACAW", "LORIKEET", "CONURE",
            "KOI", "ANGELFISH", "MOLLY", "PLATY", "SWORDTAIL", "TETRA",
            "BARB", "DISCUS", "BETTA", "GOURAMI", "CARP",
        ]),
        ("Farm Animals", [
            "COW", "PIG", "HORSE", "SHEEP", "GOAT", "CHICKEN", "DUCK",
            "GOOSE", "TURKEY", "DONKEY", "MULE", "BULL", "CALF", "LAMB",
            "ROOSTER", "HEN", "PONY", "LLAMA", "ALPACA", "RAM", "OX",
            "MARE", "STALLION", "COLT", "FILLY", "FOAL", "GELDING",
            "HEIFER", "EWE", "PIGLET", "CHICK", "DUCKLING", "GOSLING",
            "POULT", "QUAIL", "PHEASANT", "BANTAM", "PEAFOWL",
        ]),
        ("Wild Animals", [
            "LION", "TIGER", "ELEPHANT", "BEAR", "WOLF", "FOX", "DEER",
            "MONKEY", "ZEBRA", "GIRAFFE", "HIPPO", "RHINO", "LEOPARD",
            "CHEETAH", "GORILLA", "CHIMP", "KANGAROO", "KOALA", "PANDA",
            "SQUIRREL", "HARE", "RACCOON", "SKUNK", "MOOSE", "BISON",
            "HYENA", "JAGUAR", "PANTHER", "BABOON", "ANTELOPE", "BEAVER",
            "OTTER", "BADGER", "HEDGEHOG", "PORCUPINE", "GAZELLE", "FROG",
            "SNAKE",
            "APE", "GIBBON", "ORANGUTAN", "LEMUR", "SLOTH", "AARDVARK",
            "ARMADILLO", "PLATYPUS", "WOMBAT", "POSSUM", "OPOSSUM",
            "WALLABY", "EMU", "RHEA", "COYOTE", "JACKAL", "DINGO", "LYNX",
            "BOBCAT", "COUGAR", "PUMA", "OCELOT", "SERVAL", "CARACAL",
            "MONGOOSE", "MEERKAT", "BOAR", "WARTHOG", "TAPIR", "PECCARY",
            "CAPYBARA", "AGOUTI", "ELK", "CARIBOU", "REINDEER", "MUSKOX",
            "IBEX", "CHAMOIS", "BIGHORN", "OKAPI", "TARSIER", "MACAQUE",
            "MANDRILL", "BAT", "MOLE", "SHREW", "PIKA", "MARMOT",
            "CHIPMUNK", "GROUNDHOG", "WOODCHUCK", "NUTRIA",
        ]),
        ("Sea & Water Life", [
            "FISH", "SHARK", "WHALE", "DOLPHIN", "OCTOPUS", "SQUID", "CRAB",
            "LOBSTER", "SHRIMP", "JELLYFISH", "SEAHORSE", "STARFISH",
            "STINGRAY", "EEL", "CORAL", "URCHIN", "CLAM", "OYSTER", "MUSSEL",
            "SNAIL", "SALMON", "TUNA", "COD", "RAY", "SEAL", "WALRUS",
            "MANATEE", "ORCA", "BARRACUDA", "PUFFERFISH", "TADPOLE",
            "PLANKTON", "ANEMONE",
            "TROUT", "BASS", "PIKE", "HALIBUT", "MACKEREL", "HERRING",
            "SARDINE", "ANCHOVY", "CATFISH", "SWORDFISH", "MARLIN",
            "SAILFISH", "GROUPER", "SNAPPER", "PERCH", "CONCH", "WHELK",
            "ABALONE", "SCALLOP", "LIMPET", "BARNACLE", "PRAWN", "KRILL",
            "NAUTILUS", "CUTTLEFISH", "CUTTLE", "PARROTFISH", "PIRANHA",
            "DUGONG", "NARWHAL", "BELUGA", "PORPOISE", "SPONGE", "MORAY",
            "CLOWNFISH", "GOBY", "WRASSE", "TANG", "BLENNY",
        ]),
        ("Birds", [
            "EAGLE", "HAWK", "OWL", "SPARROW", "PIGEON", "CROW", "ROBIN",
            "SWAN", "FLAMINGO", "PEACOCK", "PENGUIN", "OSTRICH", "SEAGULL",
            "WOODPECKER", "HUMMINGBIRD", "KINGFISHER", "VULTURE", "HERON",
            "STORK", "CRANE", "DOVE", "NIGHTINGALE", "CUCKOO", "MAGPIE",
            "RAVEN", "FALCON",
            "LARK", "SWALLOW", "MARTIN", "STARLING", "BLACKBIRD",
            "BLUEBIRD", "CARDINAL", "ORIOLE", "TANAGER", "BUNTING", "JAY",
            "TITMOUSE", "CHICKADEE", "NUTHATCH", "CREEPER", "WREN",
            "WARBLER", "THRUSH", "KINGLET", "COOT", "MOORHEN", "RAIL",
            "BITTERN", "IBIS", "SPOONBILL", "AVOCET", "STILT", "PLOVER",
            "SANDPIPER", "CURLEW", "DUNLIN", "KNOT", "TURNSTONE",
            "PHALAROPE", "GULL", "TERN", "SKIMMER", "AUK", "PUFFIN",
            "MURRE", "ALBATROSS", "PETREL", "SHEARWATER", "FULMAR",
            "PELICAN", "CORMORANT", "ANHINGA", "BOOBY", "GANNET",
            "TROPICBIRD", "KITE", "OSPREY", "HARRIER", "BUZZARD",
            "KESTREL", "MERLIN", "GOSHAWK", "CONDOR", "CARACARA",
            "PARTRIDGE", "GROUSE", "PTARMIGAN", "ROADRUNNER", "TOUCAN",
            "HORNBILL", "BARBET", "HOOPOE", "KOOKABURRA", "LYREBIRD",
            "BOWERBIRD", "QUETZAL", "TROGON",
        ]),
        ("Insects & Bugs", [
            "ANT", "BEE", "WASP", "FLY", "MOSQUITO", "BUTTERFLY", "MOTH",
            "BEETLE", "LADYBUG", "DRAGONFLY", "GRASSHOPPER", "CATERPILLAR",
            "SPIDER", "CRICKET", "FLEA", "TICK", "TERMITE", "CENTIPEDE",
            "SCORPION", "LOCUST", "FIREFLY", "COCKROACH", "APHID", "WORM",
            "HORNET", "YELLOWJACKET", "BUMBLEBEE", "HONEYBEE", "SILVERFISH",
            "EARWIG", "MAYFLY", "STONEFLY", "CADDISFLY", "DAMSELFLY",
            "LOUSE", "CHIGGER", "MITE", "BEDBUG", "MANTIS", "MILLIPEDE",
            "SILKWORM", "MEALWORM", "GLOWWORM", "GRUB", "MAGGOT", "PUPA",
            "LARVA", "NYMPH", "CHRYSALIS", "COCOON", "PILLBUG", "WOODLOUSE",
            "SOWBUG",
        ]),
        ("Body Parts & Sounds", [
            "PAW", "TAIL", "FUR", "CLAW", "HORN", "HOOF", "TUSK", "MANE",
            "BEAK", "WING", "FEATHER", "FIN", "SCALE", "GILL", "SNOUT",
            "WHISKER", "SHELL", "TENTACLE", "ANTLER", "POUCH", "STINGER",
            "VENOM", "BLUBBER", "FANG", "CREST", "SPINE", "TALON", "BARK",
            "MEOW", "PURR", "CHIRP", "BUZZ", "ROAR", "HOWL", "NEIGH", "MOO",
            "BAA", "OINK", "QUACK", "HISS", "GROWL", "CROAK", "SQUEAK",
            "GRUNT", "BLEAT", "SNORT", "HOOT", "SQUAWK",
            "NAIL", "PELT", "HIDE", "SKIN", "MUZZLE", "TOOTH", "TEETH",
            "TONGUE", "GIZZARD", "PLUME", "COMB", "WATTLE", "SPUR",
            "PINION", "PLUMAGE", "DOWN", "SCUTE", "CARAPACE", "PLASTRON",
            "FLIPPER", "BLOWHOLE", "PAD", "HAIR", "QUILL", "BRISTLE",
            "TRILL", "WARBLE", "CLICK", "SNAP", "CHATTER", "CHITTER",
            "SQUALL", "WHINNY", "BRAY", "BELLOW", "BUGLE", "COO",
            "TRUMPET", "SNORE", "SQUEAL", "WHIMPER", "YELP", "YIP", "BAY",
            "WHINE", "MOAN", "HUM", "SING", "SONG", "CAW", "HONK",
            "SCREECH", "SHRIEK",
        ]),
        ("Habitats & Homes", [
            "JUNGLE", "OCEAN", "DESERT", "FOREST", "RIVER", "POND", "LAKE",
            "MOUNTAIN", "MEADOW", "SAVANNA", "GRASSLAND", "WETLAND", "REEF",
            "CAVE", "TUNDRA", "MARSH", "STREAM", "VALLEY", "BURROW", "DEN",
            "HIVE", "STABLE", "BARN", "KENNEL", "AVIARY", "ZOO", "FARM",
            "WOODS", "PRAIRIE", "NEST", "TREE",
            "SEA", "COAST", "SHORE", "BEACH", "DUNE", "CLIFF", "ISLAND",
            "ATOLL", "LAGOON", "ESTUARY", "DELTA", "BAYOU", "SWAMP", "BOG",
            "FEN", "MOOR", "HEATH", "GLADE", "THICKET", "BRUSH", "SCRUB",
            "CANOPY", "GROVE", "ORCHARD", "FIELD", "PASTURE", "PLAIN",
            "PLATEAU", "CANYON", "GORGE", "RAVINE", "GLEN", "DELL", "HILL",
            "RANGE", "OUTBACK", "TAIGA", "STEPPE", "PAMPAS", "VELD",
            "FJORD", "GLACIER", "ICEBERG", "FLOE", "TIDEPOOL", "LAIR",
            "ROOST", "FORM", "SETT", "EYRIE", "AERIE", "DREY", "LODGE",
            "WARREN", "BOWER", "DOME", "TUNNEL", "TERRARIUM", "AQUARIUM",
            "VIVARIUM", "PADDOCK", "CORRAL", "PEN", "STY", "COOP", "COTE",
            "HUTCH", "TANK", "TROUGH", "WATERHOLE", "OASIS",
        ]),
        ("Reptiles & Amphibians", [
            "LIZARD", "CROCODILE", "ALLIGATOR", "GATOR", "CAIMAN",
            "TUATARA", "TORTOISE", "TERRAPIN", "COBRA", "VIPER", "PYTHON",
            "BOA", "MAMBA", "ADDER", "RATTLESNAKE", "COPPERHEAD",
            "MOCCASIN", "GARTER", "KRAIT", "TOAD", "CHAMELEON", "MONITOR",
            "SKINK", "ANACONDA", "BULLFROG", "TREEFROG", "AGAMID",
            "NATTERJACK",
        ]),
        ("Animal Groups & Behaviors", [
            "PACK", "HERD", "FLOCK", "SWARM", "POD", "PRIDE", "TROOP",
            "COLONY", "SCHOOL", "SHOAL", "DROVE", "GAGGLE", "SKEIN",
            "MURDER", "PARLIAMENT", "KETTLE", "BUSINESS", "CAST", "COVEY",
            "BEVY", "LABOR", "TRIP", "TRIBE", "BAND", "RAFT", "ROMP",
            "SKULK", "LEAP", "CRY", "TOWER", "CRASH", "STAMPEDE",
            "HERDING", "GRAZING", "BROWSING", "MIGRATION", "FORAGE",
            "ROAM", "PROWL", "STALK", "HUNT", "HUNTING", "PREDATOR",
            "PREY", "CARNIVORE", "HERBIVORE", "OMNIVORE", "ALPHA",
            "NOCTURNAL", "HIBERNATE", "CAMOUFLAGE", "MIMIC", "VENOMOUS",
            "POISONOUS", "DIURNAL", "DOMINANT",
        ]),
    ])
    trivia_easy = [
        {"q": "Which animal is often called man's best friend?",
         "options": ["Dog", "Cat", "Horse"], "answer": "Dog"},
        {"q": "Which big cat has black stripes?",
         "options": ["Tiger", "Lion", "Leopard"], "answer": "Tiger"},
        {"q": "Which bird is famous for copying human speech?",
         "options": ["Parrot", "Eagle", "Owl"], "answer": "Parrot"},
        {"q": "Which sea mammal is clever, friendly, and playful?",
         "options": ["Dolphin", "Shark", "Crab"], "answer": "Dolphin"},
        {"q": "Which animal is the largest that lives on land?",
         "options": ["Elephant", "Whale", "Bear"], "answer": "Elephant"},
        {"q": "Which insect makes honey?",
         "options": ["Bee", "Ant", "Fly"], "answer": "Bee"},
        {"q": "Which bird cannot fly but swims very well?",
         "options": ["Penguin", "Eagle", "Sparrow"], "answer": "Penguin"},
        {"q": "Which animal carries its shell home and moves slowly?",
         "options": ["Snail", "Rabbit", "Cat"], "answer": "Snail"},
        {"q": "Which tall animal has a very long neck?",
         "options": ["Giraffe", "Zebra", "Hippo"], "answer": "Giraffe"},
        {"q": "A baby dog is called a what?",
         "options": ["Puppy", "Kitten", "Calf"], "answer": "Puppy"},
        {"q": "Which animal hops and carries its baby in a pouch?",
         "options": ["Kangaroo", "Monkey", "Bear"], "answer": "Kangaroo"},
        {"q": "What sound does a cow make?",
         "options": ["Moo", "Baa", "Quack"], "answer": "Moo"},
    ]
    phrase_medium = [
        {"prompt": "The early bird catches the ____", "answer": "Worm"},
        {"prompt": "Let the cat out of the ____", "answer": "Bag"},
        {"prompt": "When the cat's away, the ____ will play", "answer": "Mice"},
        {"prompt": "Busy as a ____", "answer": "Bee"},
        {"prompt": "Quiet as a ____", "answer": "Mouse"},
        {"prompt": "Hold your ____", "answer": "Horses"},
        {"prompt": "Curiosity killed the ____", "answer": "Cat"},
        {"prompt": "Barking up the wrong ____", "answer": "Tree"},
        {"prompt": "Don't count your chickens before they ____", "answer": "Hatch"},
        {"prompt": "When pigs ____", "answer": "Fly"},
    ]
    trivia_open = [
        {"q": "Name the big cat known as the king of the jungle.",
         "answer": "Lion"},
        {"q": "Which pet is said to have nine lives?", "answer": "A cat"},
        {"q": "What do you call a baby dog?", "answer": "A puppy"},
        {"q": "Which is the largest mammal in the ocean?",
         "answer": "The blue whale"},
        {"q": "What is the fastest land animal?", "answer": "The cheetah"},
        {"q": "Which black-and-white bear eats bamboo?",
         "answer": "The giant panda"},
        {"q": "What is a group of wolves called?", "answer": "A pack"},
    ]
    crossword = [
        ("DOG", "Loyal pet that barks"),
        ("CAT", "Feline that chases mice"),
        ("LION", "Big cat called king of the jungle"),
        ("TIGER", "Striped big cat"),
        ("ELEPHANT", "Large animal with a trunk"),
        ("GIRAFFE", "Tallest animal with a long neck"),
        ("HORSE", "Animal you can ride and gallop"),
        ("COW", "Farm animal that gives milk"),
        ("SHEEP", "Woolly farm animal"),
        ("MONKEY", "Tree-swinging primate"),
        ("ZEBRA", "Black-and-white striped horse"),
        ("KANGAROO", "Hopping animal with a pouch"),
        ("PENGUIN", "Flightless bird that swims"),
        ("EAGLE", "Powerful bird of prey"),
        ("OWL", "Bird that hoots at night"),
        ("SHARK", "Fierce ocean predator"),
        ("WHALE", "Giant mammal of the sea"),
        ("DOLPHIN", "Clever friendly sea mammal"),
        ("RABBIT", "Hopping pet with long ears"),
        ("BEE", "Insect that makes honey"),
        ("FISH", "Animal that lives in water"),
        ("CRAB", "Shellfish that walks sideways"),
        ("DUCK", "Bird that quacks and swims"),
        ("GOAT", "Farm animal that climbs and butts"),
        ("TURTLE", "Reptile that carries a shell"),
        ("PARROT", "Bird that can mimic words"),
        ("FROG", "Green animal that croaks and hops"),
        ("SNAKE", "Long animal with no legs"),
        ("DEER", "Forest animal with antlers"),
        ("FOX", "Sly wild animal with a bushy tail"),
        ("SEAL", "Sea mammal that barks on rocks"),
    ]
    remedies = [
        {"condition": "Pet Scratch or Minor Bite",
         "text": "Wash the spot with cool water and soap, then dab a little "
                 "turmeric paste and keep it clean. Check that the pet's shots "
                 "are up to date. See a professional if it becomes red, swollen, "
                 "or warm."},
        {"condition": "Insect Bite or Sting",
         "text": "Wash the area with cool water and soap, then apply a paste of "
                 "neem or holy basil leaves, or rest a slice of onion on it. A "
                 "cold, damp cloth eases the sting and swelling. Get help right "
                 "away for trouble breathing or a lot of swelling."},
        {"condition": "Dust & Fur Sneezing",
         "text": "Rinse your face and hands after being around animals, and "
                 "step into fresh air. Sip warm ginger-holy basil tea and steam "
                 "with a little eucalyptus to clear a tickly nose. Keeping rooms "
                 "aired and brushed-down often lowers the sneezes."},
        {"condition": "Yard & Pet Back Ache",
         "text": "Massage the lower back with warm sesame oil, then rest with a "
                 "warm compress. A cup of turmeric milk at bedtime eases stiff "
                 "muscles. Bend at the knees when lifting and pace the chores "
                 "through the day."},
        {"condition": "Outdoor Dehydration",
         "text": "Sit in the shade and sip water slowly with a pinch of salt and "
                 "lemon, or drink coconut water. Rest in cooler air and let the "
                 "body recover. Keep drinks close by before you head back out."},
        {"condition": "Indian Gooseberry (Amla)",
         "text": "Eat it fresh, drink its juice, or enjoy it as a sweet syrup "
                 "preserve. Rich in vitamin C, it is a daily tonic for immunity, "
                 "hair, and digestion."},
        {"condition": "Fennel Seed Water",
         "text": "Soak a spoon of fennel seeds overnight, then sip the cool "
                 "water in the morning. It is refreshing, aids digestion, and is "
                 "a gentle traditional help for tired eyes."},
    ]
    coloring = ["bird", "butterfly", "flower", "leaf", "sun", "star"]
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


BANKS = {"animals": build}

"""Holidays & Family Celebrations - evergreen, all-country content bank."""
from __future__ import annotations
from collections import OrderedDict


def build() -> dict:
    word_pools = OrderedDict([
        ("Celebrations & Feasts", [
            "CHRISTMAS", "EASTER", "DIWALI", "EID", "HANUKKAH", "KWANZAA",
            "HALLOWEEN", "NEWYEAR", "THANKSGIVING", "BIRTHDAY", "WEDDING",
            "ANNIVERSARY", "GRADUATION", "FESTIVAL", "FIESTA", "CARNIVAL",
            "PARADE", "CEREMONY", "JUBILEE", "GALA", "REUNION", "FEAST",
            "HOLIDAY", "PAGEANT", "RAMADAN", "VESAK", "OBON", "SONGKRAN",
            "PURIM", "PESACH", "PASSOVER", "ONAM", "PONGAL", "HOLI",
            "NAVRATRI", "DUSSEHRA", "JANMASHTAMI", "GANESH", "TET",
            "KRATHONG", "MIDAUTUMN", "ADVENT", "LENT", "EPIPHANY",
            "PENTECOST", "VALENTINE", "MARDIGRAS", "HOGMANAY",
            "OKTOBERFEST", "BOXING", "BASTILLE", "INDEPENDENCE", "MAYDAY",
            "SHROVE", "SEDER", "SHABBAT", "SABBATH", "WHITSUN",
            "CANDLEMAS", "BONFIRE", "GUYFAWKES", "LAMMAS", "PALMSUNDAY",
            "COMMUNION", "BAPTISM", "BARMITZVAH", "BATMITZVAH",
            "ENGAGEMENT", "NAMING", "BRIDE", "GROOM", "BRIDAL",
            "CHRISTENING", "BABYSHOWER", "RECEPTION", "BANQUET", "DINNER",
            "SUPPER", "BRUNCH", "LUNCHEON", "PILGRIMAGE",
        ]),
        ("Decorations", [
            "LIGHTS", "WREATH", "LANTERN", "GARLAND", "BANNER", "RIBBON",
            "BOW", "TINSEL", "BALLOON", "BUNTING", "ORNAMENT", "CANDLE",
            "BAUBLE", "STREAMER", "CONFETTI", "BELLS", "STAR", "PINECONE",
            "MISTLETOE", "HOLLY", "BLOSSOM", "TASSEL", "CREPE", "POMPOM",
            "GLITTER", "IVY", "TEALIGHT", "VOTIVE", "CRIB", "NATIVITY",
            "MANGER", "ANGEL", "CHIMNEY", "STOCKING", "FIREPLACE",
            "NUTCRACKER", "SNOWGLOBE", "LAMP", "DIYA", "RANGOLI", "KOLAM",
            "FAIRY", "STRING", "BEAD", "SEQUIN", "SPANGLE", "FLAG",
            "PENNANT", "ROSETTE", "DOILY", "RUNNER", "SWAG", "TOPIARY",
            "PUMPKIN", "GHOST", "CROWN", "TIARA", "SASH", "CHAIN",
            "PAPER", "LUMINARY", "LIGHT", "BULB", "SPIDER", "BAT",
        ]),
        ("Festive Food", [
            "CAKE", "PUDDING", "COOKIE", "TURKEY", "PIE", "CANDY",
            "CHOCOLATE", "ROAST", "GINGERBREAD", "MINCEPIE", "STOLLEN",
            "FUDGE", "NOG", "MARZIPAN", "STUFFING", "GRAVY", "TRIFLE",
            "PAVLOVA", "PANETTONE", "BISCUIT", "TART", "WAFER", "NOUGAT",
            "PRETZEL", "MULLED", "CIDER", "PUNCH", "LOAF", "HAM", "NUTS",
            "EGNOG", "GOOSE", "DUCK", "LAMB", "SALAD", "POTATO", "YAM",
            "CRANBERRY", "SAUCE", "JELLY", "CUSTARD", "CREAM", "ICECREAM",
            "SORBET", "SUGAR", "SULTANA", "RAISIN", "ALMOND", "PECAN",
            "WALNUT", "CASHEW", "PISTACHIO", "MACAROON", "MERINGUE",
            "CHEESECAKE", "BROWNIE", "CUPCAKE", "MUFFIN", "SCONE",
            "PANCAKE", "WAFFLE", "CROISSANT", "DOUGHNUT", "BAGEL",
            "BRIOCHE", "BUN", "ROLL", "BREAD", "TAMALE", "TURRON", "SOUP",
            "BROTH", "STEW", "CURRY", "RICE", "NOODLE", "DUMPLING",
            "SAGE", "THYME", "ROSEMARY", "NUTMEG", "CINNAMON", "GINGER",
            "CLOVE", "VANILLA", "HONEY", "SYRUP", "BUTTER", "CHEESE",
            "COCOA",
        ]),
        ("Gifts & Surprises", [
            "GIFT", "PRESENT", "CARD", "PARCEL", "SURPRISE", "BOUQUET",
            "TOY", "TOKEN", "HAMPER", "TREAT", "WRAPPING", "ENVELOPE",
            "PACKAGE", "GIFTBAG", "BASKET", "GOODIES", "SWEETS", "FAVORS",
            "NOVELTY", "PRIZE", "WRAP", "TAG", "LABEL", "STICKER", "SEAL",
            "STAMP", "TISSUE", "BOX", "SACK", "CRACKER", "POPPER",
            "TROPHY", "MEDAL", "GIFTTAG", "FAVOUR", "DONATION", "CHARITY",
            "ALMS", "TIP", "GRATUITY", "KEEPSAKE", "SOUVENIR", "MEMENTO",
        ]),
        ("Family & Guests", [
            "FAMILY", "MOTHER", "FATHER", "SISTER", "BROTHER", "COUSIN",
            "AUNT", "UNCLE", "GRANDMA", "GRANDPA", "NIECE", "NEPHEW",
            "RELATIVE", "CLAN", "KIN", "GUEST", "HOST", "FRIEND",
            "PARTNER", "HUSBAND", "WIFE", "PARENT", "CHILD", "TODDLER",
            "ELDERS", "NEIGHBOR", "GRANNY", "NANA", "PAPA", "GRANDMOTHER",
            "GRANDFATHER", "DAUGHTER", "SON", "BABY", "INFANT", "TEEN",
            "YOUTH", "ADULT", "SENIOR", "SIBLING", "TWINS", "INLAWS",
            "GODPARENT", "GODCHILD", "SPOUSE", "COMPANION", "VISITOR",
            "COMPANY", "COMMUNITY", "CROWD", "BESTMAN", "BRIDESMAID",
            "USHER", "PAGEBOY",
        ]),
        ("Music & Carols", [
            "CAROL", "SONG", "HYMN", "ANTHEM", "MELODY", "CHORUS", "TUNE",
            "JINGLE", "BAND", "CHOIR", "DRUM", "WHISTLE", "ORCHESTRA",
            "CONCERT", "GUITAR", "HARP", "FLUTE", "LYRICS", "VERSE",
            "RHYTHM", "TRUMPET", "CAROLER", "BALLAD", "PIANO", "VIOLIN",
            "CELLO", "CLARINET", "SAXOPHONE", "TROMBONE", "CYMBAL",
            "TAMBOURINE", "MARACA", "BANJO", "MANDOLIN", "ACCORDION",
            "KEYBOARD", "ORGAN", "XYLOPHONE", "FIDDLE", "RECORDER",
            "HARMONICA", "BASS", "UKULELE", "OBOE", "PICCOLO", "CORNET",
            "BUGLE", "TUBA", "TIMPANI", "CHIMES", "GONG", "CASTANET",
            "TRIANGLE", "SINGER", "VOCAL", "HARMONY", "DUET", "TRIO",
            "QUARTET", "CHORD", "TEMPO", "BEAT", "NOTE", "SCALE",
            "OCTAVE", "REFRAIN", "SERENADE", "LULLABY", "ARIA",
            "OVERTURE", "SONATA", "SYMPHONY", "CONCERTO", "CADENCE",
            "CRESCENDO",
        ]),
        ("Seasons & Nature", [
            "WINTER", "SPRING", "SUMMER", "AUTUMN", "FALL", "SNOW",
            "FROST", "SUNSHINE", "HARVEST", "SEASON", "SOLSTICE", "SUNNY",
            "SNOWFLAKE", "FLOWER", "LEAF", "RAINBOW", "BREEZE", "CLOUD",
            "SLEET", "ICICLE", "PETAL", "EVERGREEN", "SNOWMAN",
            "SNOWBALL", "BLIZZARD", "FLURRY", "DRIFT", "POWDER", "FROZEN",
            "ICE", "RIVER", "LAKE", "MOUNTAIN", "FOREST", "MEADOW",
            "GARDEN", "ORCHARD", "TULIP", "DAFFODIL", "ROSE", "LILY",
            "JASMINE", "MARIGOLD", "LOTUS", "PINE", "FIR", "CEDAR",
            "SPRUCE", "BIRCH", "OAK", "MAPLE", "WILLOW", "ACORN", "CONE",
            "TWIG", "BRANCH", "ROOT", "MOSS", "FERN", "THISTLE", "BUD",
            "STEM", "BARK", "POND", "HILL", "VALLEY", "FIELD", "DEW",
            "MIST", "RAIN", "WIND", "SUN", "MOON", "STORM", "THUNDER",
            "LIGHTNING", "EQUINOX", "THAW", "BLOOM", "POLLEN", "SEED",
            "KERNEL", "GRAIN", "STALK", "REED", "VINE", "GLADE", "GROVE",
            "CANOPY",
        ]),
        ("Party & Greetings", [
            "CHEERS", "WELCOME", "JOY", "PEACE", "LOVE", "BLESSING",
            "WISHES", "CONGRATS", "HAPPY", "MERRY", "FESTIVE", "TOAST",
            "DANCE", "GAMES", "NAPKIN", "PLATE", "MUSIC", "HAT",
            "BLOWOUT", "PARTY", "GATHER", "CELEBRATE", "LAUGH", "SMILE",
            "HUG", "KISS", "GREETING", "SALUTE", "BLESS", "PRAY", "HOPE",
            "FAITH", "GRACE", "CHEER", "GLAD", "BLISS", "JOLLY", "HEALTH",
            "WEALTH", "PROSPER", "LUCKY", "FORTUNE", "PROSPERITY",
            "INVITE", "INVITATION", "MENU", "RECIPE", "TABLE", "CHAIR",
            "GLASS", "MUG", "CUP", "FORK", "SPOON", "KNIFE",
            "TABLECLOTH", "HORN", "BLOWER", "RAFFLE", "BINGO", "QUIZ",
            "FAVOR", "FUN", "GIGGLE", "GLOW", "CHEERFUL", "DELIGHT",
            "ENJOY", "REJOICE", "CLAP", "JUBILATION", "FESTIVITY",
            "MERRYMAKING", "REVELRY", "GAIETY", "MIRTH", "JOLLITY",
            "GLEE", "ELATION", "ECSTASY", "RAPTURE",
        ]),
    ])
    trivia_easy = [
        {"q": "Which festival is widely known as the Festival of Lights?",
         "options": ["Diwali", "Easter", "Eid"], "answer": "Diwali"},
        {"q": "What green plant do people kiss beneath at Christmas?",
         "options": ["Mistletoe", "Holly", "Ivy"], "answer": "Mistletoe"},
        {"q": "Which bird is the traditional centerpiece of Thanksgiving?",
         "options": ["Turkey", "Duck", "Goose"], "answer": "Turkey"},
        {"q": "Which holiday is famous for carved pumpkins?",
         "options": ["Halloween", "Easter", "Diwali"], "answer": "Halloween"},
        {"q": "What drops in many city squares at New Year?",
         "options": ["A giant ball", "A bell", "A star"], "answer": "A giant ball"},
        {"q": "Which festival honours African heritage with seven candles?",
         "options": ["Kwanzaa", "Hanukkah", "Christmas"], "answer": "Kwanzaa"},
        {"q": "What sweet treat is usually cut at a birthday party?",
         "options": ["Cake", "Soup", "Pie"], "answer": "Cake"},
        {"q": "What do people exchange at many festivals?",
         "options": ["Gifts", "Snowballs", "Garlands"], "answer": "Gifts"},
        {"q": "What is sung door to door at Christmas?",
         "options": ["Carols", "Lullabies", "Ballads"], "answer": "Carols"},
        {"q": "Which Jewish festival lasts eight nights and uses a menorah?",
         "options": ["Hanukkah", "Kwanzaa", "Eid"], "answer": "Hanukkah"},
        {"q": "Why are lamps and candles lit during Diwali?",
         "options": ["To celebrate light over darkness", "To scare birds",
                     "To dry clothes"],
         "answer": "To celebrate light over darkness"},
        {"q": "What do guests often bring when visiting for a holiday meal?",
         "options": ["A small gift", "A ladder", "A map"], "answer": "A small gift"},
    ]
    phrase_medium = [
        {"prompt": "Happy New ____", "answer": "Year"},
        {"prompt": "Merry Christmas and a Happy New ____", "answer": "Year"},
        {"prompt": "Eat, drink, and be ____", "answer": "Merry"},
        {"prompt": "Home for the ____", "answer": "Holidays"},
        {"prompt": "It's the most wonderful time of the ____", "answer": "Year"},
        {"prompt": "Many happy ____", "answer": "Returns"},
        {"prompt": "Good things come in small ____", "answer": "Packages"},
        {"prompt": "Family is where the ____ is", "answer": "Heart"},
        {"prompt": "The more the ____", "answer": "Merrier"},
        {"prompt": "Make yourself at ____", "answer": "Home"},
    ]
    trivia_open = [
        {"q": "Name the Hindu festival known as the Festival of Lights.",
         "answer": "Diwali"},
        {"q": "Which flower is most often given on Valentine's Day?",
         "answer": "A rose"},
        {"q": "What is the Jewish eight-night festival of lights called?",
         "answer": "Hanukkah"},
        {"q": "Name the African heritage festival that lights seven candles.",
         "answer": "Kwanzaa"},
        {"q": "What spiced treat is shaped into houses and people at Christmas?",
         "answer": "Gingerbread"},
        {"q": "What do people make by clinking glasses and wishing good health?",
         "answer": "A toast"},
        {"q": "Name the paper tubes that pop with a small toy at a party.",
         "answer": "Christmas crackers"},
        {"q": "What is the Italian sweet bread loaf eaten at Christmas?",
         "answer": "Panettone"},
    ]
    crossword = [
        ("STAR", "Bright shape on top of many trees"),
        ("WREATH", "Circular evergreen door decoration"),
        ("GIFT", "Present given at celebrations"),
        ("EASTER", "Spring festival with eggs and bunnies"),
        ("DIWALI", "Hindu festival of lights"),
        ("PARADE", "Marching procession down a street"),
        ("CANDLE", "Waxed light for a celebration"),
        ("PARTY", "Gathering of guests for fun"),
        ("CAROL", "Festive song sung at Christmas"),
        ("TURKEY", "Roasted bird of Thanksgiving"),
        ("CAKE", "Sweet baked treat for birthdays"),
        ("LANTERN", "Portable light for festivals"),
        ("RIBBON", "Decorative band tied on gifts"),
        ("GARLAND", "Loop of flowers or leaves hung up"),
        ("BALLOON", "Inflated party decoration"),
        ("HOLLY", "Prickly green plant with red berries"),
        ("CONFETTI", "Tiny paper bits thrown at celebrations"),
        ("FAMILY", "Loved ones gathered together"),
        ("HOST", "Person who welcomes guests"),
        ("TOAST", "Raising a glass to wish well"),
        ("ORCHESTRA", "Large group playing music together"),
        ("FIREWORK", "Explosive light show in the sky"),
        ("BANNER", "Long sign hung at a party"),
        ("WINTER", "Snowy season of Christmas"),
        ("HOLIDAY", "Day of celebration or rest"),
        ("BELLS", "Ringing metal instruments of cheer"),
        ("MISTLETOE", "Plant kissed under at Christmas"),
        ("PRESENT", "Another word for a gift"),
        ("BIRTHDAY", "Anniversary of being born"),
        ("CHEERS", "Cry said when clinking glasses"),
    ]
    remedies = [
        {"condition": "Festive Indigestion",
         "text": "After a big meal, chew a pinch of roasted fennel, cumin, and "
                 "carom seeds, and sip warm ginger water. A gentle stroll and a "
                 "small piece of jaggery help settle a rich feast. Next time, "
                 "keep portions modest and eat slowly."},
        {"condition": "Sore Throat",
         "text": "Gargle with warm salt water and a pinch of turmeric two or "
                 "three times a day. Sip ginger-honey tea or warm turmeric milk, "
                 "and rest your voice. Staying warm and hydrated helps it heal."},
        {"condition": "Seasonal Stress",
         "text": "Make a simple list and do one task at a time, accepting help "
                 "from family. A cup of holy basil tea, a few slow breaths, and "
                 "a short step outside reset a busy mind. It is fine to rest "
                 "between preparations."},
        {"condition": "Late-Night Sleep Trouble",
         "text": "Keep late nights short and dim the lights well before bed. "
                 "Warm milk with nutmeg or chamomile, a calm routine, and slow "
                 "breathing help you wind down. Skip heavy food and caffeine in "
                 "the evening."},
        {"condition": "Rich-Food Nausea & Head",
         "text": "Sip ginger-lemon water, eat a ripe banana, and rest. Light, "
                 "plain food and plenty of water help after a heavy feast. A "
                 "cool cloth on the forehead eases the head."},
        {"condition": "Immunity Herbal Decoction (Kadha)",
         "text": "Boil holy basil, ginger, black pepper, cinnamon, and a clove "
                 "in water until fragrant, then strain. Sip warm through the "
                 "winter to soothe colds and build resistance."},
        {"condition": "Sesame-Jaggery Balls",
         "text": "Roll roasted sesame seeds and chopped nuts in melted jaggery "
                 "(unrefined cane sugar) into small balls. A winter favourite "
                 "that gives warmth, energy, and a little iron."},
    ]
    coloring = ["star", "flower", "butterfly", "sun", "bird", "guitar"]
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


BANKS = {"holidays": build}

"""Faith, Hope & Inspiration - evergreen, all-country interfaith content bank."""
from __future__ import annotations
from collections import OrderedDict


def build() -> dict:
    word_pools = OrderedDict([
        ("Virtues", [
            "HOPE", "PEACE", "GRACE", "JOY", "LOVE", "FAITH", "KINDNESS",
            "PATIENCE", "COURAGE", "WISDOM", "CHARITY", "MERCY", "HONESTY",
            "HUMILITY", "GENEROSITY", "COMPASSION", "FORGIVENESS", "GRATITUDE",
            "TRUST", "HARMONY", "SERENITY", "TENDERNESS", "GENTLENESS",
            "GOODNESS", "FAIRNESS", "LOYALTY", "VIRTUE", "DEVOTION",
            "REVERENCE", "INTEGRITY", "PRUDENCE", "TEMPERANCE", "FORTITUDE",
            "JUSTICE", "TOLERANCE", "RESPECT", "DILIGENCE", "NOBILITY",
            "PURITY", "MODESTY", "PIETY", "SINCERITY", "DUTY", "GOODWILL",
            "ALTRUISM", "BENEVOLENCE", "HOSPITALITY", "CONTENTMENT",
            "OPTIMISM", "FAITHFULNESS", "HOPEFULNESS", "KINDHEARTED",
            "WARMHEARTED", "GOODHEARTED", "TENDERHEARTED", "PHILANTHROPY",
            "VIRTUOUS", "GRACIOUS", "MERCIFUL", "CHARITABLE", "GENEROUS",
            "HONEST", "HUMBLE", "REVERENT", "DEVOUT", "PIOUS", "SINCERE",
            "NOBLE", "BRAVE", "VALIANT", "GALLANT", "HEROIC", "ETHICAL",
            "RIGHTEOUS", "UPRIGHT", "TRUSTWORTHY", "DEPENDABLE", "RELIABLE",
            "STEADFAST", "RESOLUTE", "TENACIOUS", "CONSTANT", "FAITHFUL",
            "FAIR", "PURE", "KIND", "MEEK", "MILD", "BENEVOLENT",
            "AFFECTIONATE",
        ]),
        ("Comfort Words", [
            "COMFORT", "SOLACE", "WARMTH", "SHELTER", "REFUGE", "HAVEN",
            "EMBRACE", "BLESSING", "BLESSED", "HEALING", "REST", "CALM",
            "QUIET", "GENTLE", "TENDER", "SOOTHING", "CRADLE", "NURTURE",
            "BLISS", "EASE", "RELIEF", "CHEER", "SMILE", "HUG", "HEART",
            "CARE", "FRIEND", "CHEERFUL", "CONSOLE", "CONSOLATION", "SOOTHE",
            "COMFORTING", "PEACEFUL", "TRANQUIL", "RESTFUL", "SOFT", "MELLOW",
            "COZY", "SNUG", "BLANKET", "PILLOW", "HEARTH", "CUDDLE",
            "SNUGGLE", "LULLABY", "SAFE", "SAFETY", "SHELTERED", "GUARDIAN",
            "PROTECT", "PROTECTION", "OASIS", "SANCTUARY", "RETREAT",
            "ASYLUM", "KINDLY", "FRIENDLY", "AMIABLE", "GENIAL", "AFFECTION",
            "FOND", "DEAR", "DARLING", "BELOVED", "CHERISH", "ADORE",
            "VALUE", "ESTEEM", "ADMIRE", "REVERE", "RELIEVED", "CALMING",
            "SOOTHED", "COSY", "RELAX", "RELAXED", "COMFORTED", "SHELTERING",
            "NURTURING", "CARESSED", "PRAYER", "PRAY", "BLESS",
            "BENEDICTION", "INVOCATION",
        ]),
        ("Nature & Light", [
            "SUNRISE", "DAWN", "DUSK", "SUNSET", "MORNING", "STAR", "MOON",
            "RAINBOW", "DOVE", "OLIVE", "BLOSSOM", "PETAL", "GARDEN",
            "MEADOW", "RIVER", "BROOK", "MOUNTAIN", "VALLEY", "OCEAN", "SEA",
            "CLOUD", "BREEZE", "SUNSHINE", "SUNBEAM", "HORIZON", "HARVEST",
            "CEDAR", "OAK", "WILLOW", "MAPLE", "SUN", "SKY", "MOONBEAM",
            "MOONLIGHT", "STARLIGHT", "STARLIT", "STARRY", "TWILIGHT",
            "NIGHTFALL", "EVENING", "DAYBREAK", "AURORA", "FIRMAMENT",
            "HEAVENS", "ZENITH", "GLIMMER", "GLEAM", "GLINT", "SHIMMER",
            "GLISTEN", "RADIANCE", "RADIANT", "LUMINOUS", "LUSTER", "GLOW",
            "GLOWING", "ILLUMINE", "BEAM", "RAY", "FLICKER", "BLAZE",
            "BLAZING", "KINDLE", "SPARKLE", "TWINKLE", "DAZZLE", "BRIGHT",
            "BRIGHTNESS", "LILY", "ROSE", "TULIP", "DAISY", "LOTUS",
            "JASMINE", "LAVENDER", "ROSEMARY", "SAGE", "FERN", "MOSS",
            "IVY", "VINE", "BIRCH", "PINE", "PALM", "PRAIRIE", "ORCHARD",
            "FOREST", "WOODS", "GROVE", "GLADE", "POND", "LAKE", "STREAM",
            "CREEK", "CASCADE", "WATERFALL", "BAY", "COVE", "HARBOR",
            "SHORE", "BEACH", "CLIFF", "HILL", "PEAK", "SUMMIT", "RIDGE",
            "PLAIN", "DESERT", "ISLAND",
        ]),
        ("Music & Hymns", [
            "HYMN", "ANTHEM", "CHORUS", "MELODY", "CAROL", "PSALM", "CHANT",
            "SONG", "VOICE", "CHIME", "BELL", "ORGAN", "CHOIR", "TEMPO",
            "RHYTHM", "TUNE", "LYRIC", "BALLAD", "REJOICE", "PRAISE",
            "GLORY", "HALLELUJAH", "INSTRUMENT", "SING", "REVERIE", "SINGER",
            "SINGING", "SONGWRITER", "MUSIC", "MUSICAL", "MUSICIAN",
            "MELODIOUS", "TUNEFUL", "HARMONIZE", "HARMONIOUS", "DUET",
            "TRIO", "QUARTET", "ENSEMBLE", "ORCHESTRA", "SYMPHONY",
            "CONCERT", "RECITAL", "OVERTURE", "INTERLUDE", "ARIA", "SOLO",
            "REFRAIN", "VERSE", "STANZA", "COUPLET", "CADENCE", "PITCH",
            "SCALE", "NOTE", "BEAT", "DRUM", "CYMBAL", "HARP", "VIOLIN",
            "FLUTE", "TRUMPET", "OBOE", "CLARINET", "LYRE", "LUTE",
            "GUITAR", "PIANO", "KEYBOARD", "ACCORDION", "SITAR", "BANJO",
            "MANDOLIN", "UKULELE", "SAXOPHONE", "GOSPEL", "SPIRITUAL",
            "ORATORIO", "CANTATA", "NOCTURNE", "SERENADE", "HYMNAL",
            "LITANY", "MOTET", "REQUIEM", "DOXOLOGY", "JUBILATE", "CAROLER",
            "SINGALONG", "ELEVATE",
        ]),
        ("Symbols of Peace", [
            "CANDLE", "LAMP", "LANTERN", "FLAME", "BEACON", "TORCH", "EMBER",
            "SPARK", "AURA", "HALO", "BANNER", "PLEDGE", "TRUCE", "UNITY",
            "BRIDGE", "EMBLEM", "TOKEN", "BOND", "AMITY", "CONCORD",
            "WREATH", "LAUREL", "GARLAND", "RING", "CIRCLE", "GLOBE",
            "WORLD", "FLAG", "HANDSHAKE", "AMULET", "TALISMAN", "CHARM",
            "MEDALLION", "KEEPSAKE", "MEMENTO", "COMPASS", "ANCHOR", "KNOT",
            "CRANE", "ORIGAMI", "STANDARD", "INSIGNIA", "BADGE", "CREST",
            "SEAL", "SIGN", "RIBBON",
        ]),
        ("Gratitude", [
            "THANKS", "APPRECIATE", "GIFT", "PRESENT", "OFFERING",
            "THANKSGIVING", "GRATEFUL", "BOON", "BOUNTY", "FAVOR",
            "TREASURE", "THANKFUL", "GIVING", "SHARING", "WELCOME",
            "ACKNOWLEDGE", "REWARD", "PRIZE", "THANK", "THANKING",
            "GRATIFY", "GRATIFIED", "GRATEFULNESS", "APPRECIATIVE",
            "RECIPROCATE", "RECIPROCITY", "RECOGNITION", "COMMENDATION",
            "COMMEND", "TRIBUTE", "SALUTE", "OVATION", "ACCOLADE",
            "BOUNTIFUL", "LARGESSE", "ENDOWMENT", "DONATION", "ALMS",
            "TITHE", "TITHING", "CONTRIBUTION", "BEQUEST", "LEGACY",
            "ENDOW", "BESTOW", "BESTOWAL", "DONATE", "DONOR", "BENEFACTOR",
            "PATRON", "SPONSOR", "SUPPORTER", "GIVER", "CONTRIBUTOR",
            "VOLUNTEER", "SHARE", "SHARED", "ACKNOWLEDGED", "GRACIOUSLY",
            "APPRECIATED", "HONORING", "SALUTING", "BENEFICENT",
        ]),
        ("Universal Proverbs", [
            "PROVERB", "PARABLE", "LESSON", "MORAL", "STORY", "TALE",
            "COUNSEL", "ADVICE", "GUIDANCE", "MENTOR", "ELDER", "TRADITION",
            "LEGEND", "SAYING", "MAXIM", "TRUTH", "SECRET", "PROMISE",
            "BEGINNING", "JOURNEY", "PATH", "DESTINY", "PURPOSE", "MEANING",
            "WONDER", "FABLE", "ALLEGORY", "ANALOGY", "METAPHOR", "EPIGRAM",
            "APHORISM", "ADAGE", "AXIOM", "BYWORD", "EPIGRAPH", "MOTTO",
            "CREED", "BELIEF", "TENET", "DOCTRINE", "PRECEPT", "EDICT",
            "LORE", "FOLKLORE", "MYTH", "SAGA", "EPIC", "ODYSSEY",
            "NARRATIVE", "CHRONICLE", "ANECDOTE", "INSIGHT", "REVELATION",
            "EPIPHANY", "AWAKENING", "ENLIGHTENMENT", "DISCERNMENT",
            "UNDERSTANDING", "KNOWLEDGE", "LEARNING", "APPRENTICE",
            "DISCIPLE", "SEEKER", "PILGRIM", "WANDERER", "EXPLORER",
            "PIONEER", "WAYFARER", "TRAVELER", "SOJOURNER", "VOYAGER",
            "NAVIGATOR", "DESTINATION", "MILESTONE", "LANDMARK",
            "CROSSROADS",
        ]),
        ("Mindfulness", [
            "BREATH", "BREATHE", "MEDITATE", "REFLECT", "STILLNESS",
            "AWARENESS", "PRESENCE", "FOCUS", "CLARITY", "BALANCE", "CENTER",
            "GROUND", "PAUSE", "SILENCE", "MINDFUL", "AWARE", "ATTENTION",
            "OBSERVE", "NOTICE", "ACCEPTANCE", "OPENNESS", "TRANQUILITY",
            "CALMNESS", "COMPOSURE", "EQUANIMITY", "EQUILIBRIUM",
            "PEACEFULNESS", "PLACID", "CONTEMPLATION", "CONTEMPLATE",
            "MEDITATION", "MUSING", "REFLECTION", "INTROSPECTION",
            "INTROSPECT", "MINDSET", "SOUL", "SPIRIT", "ESSENCE", "BEING",
            "EXISTENCE", "MOMENT", "INSTANT", "INHALE", "EXHALE", "RESPIRE",
            "SIGH", "SERENE", "CENTERED", "GROUNDED", "ROOTED", "ANCHORED",
            "ATTENTIVE", "CONCENTRATE", "CONCENTRATION", "ABSORBED",
            "IMMERSED", "ENGAGED", "ALERT", "VIGILANT", "WATCHFUL",
            "OBSERVANT", "PERCEIVE", "PERCEPTION", "SENSATION", "AWAKEN",
            "AWAKE", "CONSCIOUS", "CONSCIOUSNESS", "LUCID", "LUCIDITY",
        ]),
    ])
    trivia_easy = [
        {"q": "Which bird is widely used as a symbol of peace?",
         "options": ["Dove", "Owl", "Crow"], "answer": "Dove"},
        {"q": "After a storm, a colorful arc in the sky is a?",
         "options": ["Rainbow", "Comet", "Cloud"], "answer": "Rainbow"},
        {"q": "What word means a deep feeling of thankfulness?",
         "options": ["Gratitude", "Anger", "Hunger"], "answer": "Gratitude"},
        {"q": "A small flame on a candle is often a symbol of?",
         "options": ["Hope", "Fear", "Cold"], "answer": "Hope"},
        {"q": "Which color is most often linked with calm and quiet?",
         "options": ["Blue", "Red", "Black"], "answer": "Blue"},
        {"q": "A gentle, kind way of treating others is called?",
         "options": ["Compassion", "Greed", "Rivalry"], "answer": "Compassion"},
        {"q": "What do we call a song sung in praise or worship?",
         "options": ["A hymn", "A march", "A chant"], "answer": "A hymn"},
        {"q": "Complete it: 'Every cloud has a silver ___'",
         "options": ["Lining", "Button", "Edge"], "answer": "Lining"},
        {"q": "The morning light as the sun comes up is called?",
         "options": ["Sunrise", "Sunset", "Moonlight"], "answer": "Sunrise"},
        {"q": "Which of these best describes a quiet, peaceful mind?",
         "options": ["Calm", "Rushed", "Noisy"], "answer": "Calm"},
        {"q": "An olive branch is an old, universal symbol of?",
         "options": ["Peace", "War", "Hunger"], "answer": "Peace"},
        {"q": "To say 'thank you' is to show?",
         "options": ["Gratitude", "Pity", "Doubt"], "answer": "Gratitude"},
    ]
    phrase_medium = [
        {"prompt": "Every cloud has a silver ____", "answer": "Lining"},
        {"prompt": "Where there is life, there is ____", "answer": "Hope"},
        {"prompt": "Good things come to those who ____", "answer": "Wait"},
        {"prompt": "A journey of a thousand miles begins with a single ____",
         "answer": "Step"},
        {"prompt": "It is better to light a candle than curse the ____",
         "answer": "Darkness"},
        {"prompt": "When one door closes, another ____", "answer": "Opens"},
        {"prompt": "The best time to plant a tree was years ago; the next best time is ____",
         "answer": "Now"},
        {"prompt": "Smooth seas do not make skillful ____", "answer": "Sailors"},
        {"prompt": "Kindness is a language the blind can see and the deaf can ____",
         "answer": "Hear"},
        {"prompt": "After the darkest night comes the ____", "answer": "Dawn"},
    ]
    trivia_open = [
        {"q": "Name the bird most often drawn carrying an olive branch as a sign of peace.",
         "answer": "Dove"},
        {"q": "What colorful arc appears in the sky after rain?", "answer": "Rainbow"},
        {"q": "What word beginning with G means being thankful?", "answer": "Gratitude"},
        {"q": "What quiet practice focuses on the breath to find calm?",
         "answer": "Meditation"},
        {"q": "Which feeling is described as 'a deep, peaceful stillness'?",
         "answer": "Serenity"},
        {"q": "Name the first light of day as the sun rises.", "answer": "Sunrise"},
        {"q": "What universal virtue means caring about the suffering of others?",
         "answer": "Compassion"},
        {"q": "What does a candle's flame commonly symbolize at vigils of remembrance?",
         "answer": "Hope"},
    ]
    crossword = [
        ("HOPE", "Feeling that good things will come"),
        ("PEACE", "Calm and absence of conflict"),
        ("DOVE", "White bird of peace"),
        ("RAINBOW", "Colorful arc after rain"),
        ("GRACE", "Simple elegance or a blessing"),
        ("JOY", "Great happiness"),
        ("FAITH", "Complete trust or belief"),
        ("CANDLE", "Wax stick with a flame"),
        ("DAWN", "First light of day"),
        ("PRAYER", "Words spoken to the heavens"),
        ("PSALM", "Sacred song or poem"),
        ("CHOIR", "Group that sings together"),
        ("HALO", "Ring of light around a head"),
        ("MERCY", "Kindness shown to someone in your power"),
        ("CHARITY", "Giving help to those in need"),
        ("HARMONY", "Pleasing agreement of sounds or people"),
        ("SERENITY", "Deep, calm peacefulness"),
        ("GRATITUDE", "Thankfulness"),
        ("SUNRISE", "When the sun first appears"),
        ("OLIVE", "Branch of this tree is a peace symbol"),
        ("HYMN", "Song of praise"),
        ("CALM", "Quiet and still"),
        ("LIGHT", "Opposite of darkness"),
        ("STAR", "Shines in the night sky"),
        ("TRUST", "Firm belief in reliability"),
        ("WISDOM", "Deep knowledge and good judgment"),
        ("ANGEL", "Kind messenger from above"),
        ("SMILE", "Friendly curve of the lips"),
    ]
    remedies = [
        {"condition": "Restless, Anxious Mind",
         "text": "Sit quietly and take a few slow, deep breaths, in through the "
                 "nose and out through the mouth. A cup of holy basil tea calms "
                 "the nerves. Ashwagandha, a traditional calming herb, in warm "
                 "milk is a gentle evening support."},
        {"condition": "Trouble Sleeping",
         "text": "Keep evenings calm and dim the lights an hour before bed. Warm "
                 "milk with a pinch of nutmeg or cinnamon, and a warm sesame-oil "
                 "massage on the soles, are soothing old habits. Slow breathing "
                 "helps quiet a busy mind."},
        {"condition": "Low Mood",
         "text": "A little morning sunlight, a short walk, and kind company "
                 "often lift the spirits. Holy basil tea and the herbs brahmi "
                 "and ashwagandha are traditional daily supports for steadier "
                 "spirits. Speak with someone you trust if low feelings linger."},
        {"condition": "Worrying, Racing Thoughts",
         "text": "Write down what is on your mind, then set the page aside for a "
                 "while. Slow breathing, quiet meditation, and a calming herbal "
                 "tea ease a busy head. Sharing big worries with someone you "
                 "trust lightens the load."},
        {"condition": "Mental Clarity & Focus",
         "text": "Soak a few almonds overnight and eat them in the morning, and "
                 "add a pinch of turmeric to daily meals. The herb brahmi is a "
                 "traditional support for clear thinking. A few calm breaths "
                 "before a task help sharpen the mind."},
        {"condition": "Cardamom-Cinnamon Milk",
         "text": "Warm milk with a crushed cardamom pod and a small cinnamon "
                 "stick makes a fragrant bedtime cup. This calming drink aids "
                 "digestion and helps settle the mind for sleep."},
        {"condition": "Sweet Rose-Petal Preserve (Gulkand)",
         "text": "Stir a spoonful of sweetened rose petals into milk or water. "
                 "Cooling and gentle, it is a traditional soother for acidity "
                 "and overheating."},
    ]
    coloring = ["sun", "star", "flower", "bird", "butterfly", "leaf"]
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


BANKS = {"faith": build}

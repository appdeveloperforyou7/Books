"""Music & Movies - evergreen, all-country content bank."""
from __future__ import annotations
from collections import OrderedDict


def build() -> dict:
    word_pools = OrderedDict([
        ("Instruments", [
            "PIANO", "GUITAR", "VIOLIN", "FLUTE", "DRUM", "CELLO", "HARP",
            "CLARINET", "TRUMPET", "SAXOPHONE", "TROMBONE", "KEYBOARD",
            "ORGAN", "BANJO", "MANDOLIN", "ACCORDION", "HARMONICA",
            "XYLOPHONE", "TAMBOURINE", "OBOE", "BASS", "RECORDER", "UKULELE",
            "CORNET", "BAGPIPES", "CONCERTINA", "VIOLA", "CYMBALS", "MARACAS",
            "CASTANETS", "GONG", "OCARINA", "TUBA", "TRIANGLE", "PICCOLO",
            "SITAR", "LUTE", "ZITHER", "KOTO", "BONGO", "CONGA", "TIMPANI",
            "GLOCKENSPIEL", "COWBELL", "WOODBLOCK", "SNARE", "KAZOO",
            "PANPIPES", "FIDDLE", "HARPSICHORD", "DIDGERIDOO", "STEELPAN",
            "THEREMIN", "EUPHONIUM", "BANDONEON", "GUITARRON", "FRENCHHORN",
            "CONTRABASS", "DULCIMER",
        ]),
        ("Musical Genres", [
            "JAZZ", "BLUES", "ROCK", "POP", "CLASSICAL", "OPERA", "FOLK",
            "COUNTRY", "DISCO", "SOUL", "FUNK", "REGGAE", "SALSA", "SWING",
            "WALTZ", "TANGO", "MARCH", "GOSPEL", "CHORAL", "BAROQUE",
            "BALLAD", "SYMPHONY", "ANTHEM", "LULLABY", "CONCERTO", "SONATA",
            "HYMN", "POLKA", "RAP", "BOLERO", "FANDANGO", "MAMBO", "MERENGUE",
            "CUMBIA", "BOSSANOVA", "RAGTIME", "RAGA", "NOCTURNE", "PRELUDE",
            "RHAPSODY", "OVERTURE", "ARIA", "DUET", "TRIO", "QUARTET",
            "QUINTET", "SERENADE", "ETUDE", "CANTATA", "ORATORIO", "SUITE",
            "FUGUE", "IMPROMPTU", "INTERMEZZO", "MAZURKA", "TARANTELLA",
            "CHACONNE", "REQUIEM", "MEDLEY", "MOTET",
        ]),
        ("Film & Cinema Terms", [
            "MOVIE", "CINEMA", "ACTOR", "ACTRESS", "DIRECTOR", "SCRIPT",
            "SCENE", "CAMERA", "SCREEN", "TICKET", "POPCORN", "STUDIO",
            "TRAILER", "SEQUEL", "REMAKE", "COMEDY", "DRAMA", "THRILLER",
            "HORROR", "ROMANCE", "WESTERN", "CARTOON", "FANTASY", "MUSICAL",
            "PRODUCER", "EDITOR", "SCREENPLAY", "SOUNDTRACK", "CREDITS",
            "PREMIERE", "BLOCKBUSTER", "CAST", "PROJECTOR", "FILM", "FRAME",
            "CLIP", "FOOTAGE", "DUBBING", "SUBTITLES", "MATINEE", "FEATURE",
            "MONTAGE", "FLASHBACK", "NARRATIVE", "PLOT", "ACTION",
            "ADVENTURE", "ANIMATION", "BIOGRAPHY", "DOCUMENTARY", "EPIC",
            "CRIME", "MYSTERY", "HISTORICAL", "ROMCOM", "SATIRE",
            "WHODUNNIT", "SLAPSTICK", "CLIFFHANGER", "BLOOPERS", "CAMEO",
            "STUNTMAN", "REEL", "EPISODE", "SERIAL",
        ]),
        ("The Stage & Theatre", [
            "STAGE", "CURTAIN", "AUDIENCE", "BALCONY", "SPOTLIGHT", "PROPS",
            "COSTUME", "REHEARSAL", "MONOLOGUE", "DIALOGUE", "ENTRANCE",
            "EXIT", "PLAY", "THEATRE", "AUDITORIUM", "BACKSTAGE", "APPLAUSE",
            "ENCORE", "USHER", "PROLOGUE", "EPILOGUE", "SOLILOQUY",
            "INTERMISSION", "SCENERY", "ORCHESTRA", "WINGS", "FOYER",
            "STALLS", "AISLE", "RIGGING", "FLYTOWER", "GREASEPAINT",
            "FOOTLIGHTS", "PROMPTER", "UNDERSTUDY", "GREENROOM", "CABARET",
            "REVUE", "PANTOMIME", "FARCE", "TRAGEDY", "PLAYWRIGHT",
            "AUDITION", "STAGECRAFT", "TABLEAU", "LOBBY", "CANOPY",
            "PORTICO", "MIRROR",
        ]),
        ("Dance", [
            "DANCE", "BALLET", "FOXTROT", "RUMBA", "SAMBA", "CHACHA",
            "FLAMENCO", "TAP", "JIVE", "QUICKSTEP", "BALLROOM",
            "CHOREOGRAPHY", "DANCER", "STEP", "TWIRL", "LEAP", "SPIN",
            "SWAY", "SLIDE", "SHUFFLE", "PRANCE", "GLIDE", "BOUNCE", "SKIP",
            "JITTERBUG", "PARTNER", "ROUTINE", "FORMATION", "TURN", "DIP",
            "LIFT", "KICK", "ARABESQUE", "PIROUETTE", "POINTE", "SLIPPERS",
            "BARRE", "TROUPE", "RECITAL", "CHOREOGRAPHER", "PRINCIPAL",
            "SOLOIST", "MODERN", "CONTEMPORARY", "FREESTYLE", "LINDY",
            "PLIE", "SAUTE", "TENDU", "GRANDJETE",
        ]),
        ("Notes & Rhythm & Harmony", [
            "MELODY", "TEMPO", "CHORD", "RHYTHM", "HARMONY", "NOTE", "BEAT",
            "TUNE", "SCALE", "PITCH", "OCTAVE", "SHARP", "FLAT", "REST",
            "KEY", "CLEF", "STAVE", "BAR", "VERSE", "CHORUS", "BRIDGE",
            "RIFF", "ARPEGGIO", "CRESCENDO", "FORTISSIMO", "LEGATO",
            "STACCATO", "DYNAMICS", "COMPOSER", "LYRICS", "MINIM",
            "CROTCHET", "QUAVER", "SEMIBREVE", "SEMIQUAVER", "CADENCE",
            "MODULATION", "TRANSPOSITION", "INTERVAL", "TRIAD", "ACCENT",
            "RITARDANDO", "ACCELERANDO", "DIMINUENDO", "FORTE", "PIANISSIMO",
            "ANDANTE", "ALLEGRO", "PRESTO", "LENTO", "ADAGIO", "MODERATO",
            "VIVACE", "LARGO", "TRILL", "MOTIF", "THEME", "LEITMOTIF",
            "COUNTERPOINT", "POLYPHONY", "DISSONANCE", "CONSONANCE",
            "TONIC", "DOMINANT",
        ]),
        ("Music & Film Equipment", [
            "MICROPHONE", "SPEAKER", "AMPLIFIER", "HEADPHONES", "TURNTABLE",
            "MIXER", "CONSOLE", "CABLE", "JACK", "PLUG", "STAND", "BOOM",
            "SLATE", "CLAPPER", "LENS", "FILTER", "TRIPOD", "DOLLY", "CRANE",
            "JIB", "WINDSCREEN", "PICKUP", "STRINGS", "PICK", "BOW", "ROSIN",
            "REED", "MOUTHPIECE", "VALVE", "PEDAL", "FOOTSWITCH",
            "SYNTHESIZER", "SEQUENCER", "SAMPLER", "MULTITRACK", "GAFFER",
            "LIGHTING", "CASSETTE", "VINYL", "DISC", "TAPE", "GRAMOPHONE",
            "PHONOGRAPH", "PLAYBACK", "EARPHONES", "SUBWOOFER", "TWEETER",
            "WOOFER", "EQUALIZER", "REVERB", "DELAY", "TREBLE",
        ]),
        ("Awards & Roles", [
            "OSCAR", "GRAMMY", "TROPHY", "MEDAL", "NOMINEE", "WINNER",
            "AWARD", "STATUETTE", "CEREMONY", "RIBBON", "LAUREL", "HONOR",
            "PRIZE", "VOTE", "JUDGE", "GOLDENGLOBE", "EMMY", "PLATINUM",
            "DIAMOND", "ACCOLADE", "TONY", "BAFTA", "CANNES", "SUNDANCE",
            "PALME", "OVATION", "HOST", "PRESENTER", "ANNOUNCER", "CRITIC",
            "REVIEWER", "STAR", "CELEBRITY", "IDOL", "ICON", "LEGEND",
            "VETERAN", "MAESTRO", "VIRTUOSO", "PRODIGY", "TALENT",
            "ARTISTE", "PERFORMER", "ENTERTAINER", "MUSICIAN", "CONDUCTOR",
            "ARRANGER", "SONGWRITER", "LYRICIST", "LIBRETTIST",
            "IMPRESARIO", "NOVICE", "AMATEUR", "PROFESSIONAL", "COMPERE",
            "FAN", "CROWD", "CHEER",
        ]),
        ("Story & Characters", [
            "HERO", "VILLAIN", "PRINCESS", "KNIGHT", "DRAGON", "WIZARD",
            "FAIRY", "GENIE", "ROBOT", "ALIEN", "PIRATE", "CLOWN", "KING",
            "QUEEN", "PRINCE", "WITCH", "GHOST", "MONSTER", "GIANT", "DWARF",
            "ELF", "SIREN", "MERMAID", "UNICORN", "NARRATOR", "MENTOR",
            "OUTLAW", "DETECTIVE", "EXPLORER", "CAPTAIN", "GOBLIN", "TROLL",
            "OGRE", "SORCERER", "MAGICIAN", "SQUIRE", "BARON", "LORD",
            "LADY", "DUKE", "DUCHESS", "EMPEROR", "EMPRESS", "PEASANT",
            "MERCHANT", "SAILOR", "SOLDIER", "GUARD", "ARCHER", "HUNTER",
            "BAKER", "JESTER", "THIEF", "BANDIT", "ROBBER", "SHERIFF",
            "MAYOR", "PRIEST", "MONK", "PHOENIX", "GRIFFIN", "CENTAUR",
            "VAMPIRE", "WEREWOLF", "ZOMBIE", "GOLEM", "DEMON", "ANGEL",
            "SPIRIT", "PHANTOM", "SKELETON",
        ]),
        ("Singing & Voice", [
            "SONG", "SING", "SINGER", "VOICE", "VOCAL", "CHOIR", "CHANT",
            "HUM", "WHISTLE", "CROON", "BELT", "WAIL", "SHOUT", "WHISPER",
            "SHRIEK", "BELLOW", "YODEL", "CHORALE", "ALTO", "SOPRANO",
            "TENOR", "BARITONE", "CONTRALTO", "MEZZO", "VOCALIST", "SOLO",
            "HARMONIZE", "MELODIC", "TUNEFUL", "WARBLE", "CAROL", "REFRAIN",
            "CHORISTER", "CANTOR", "VOCALS", "RECITATIVE", "COLORATURA",
            "VIBRATO", "PORTAMENTO", "GLISSANDO", "VOCALISE", "BELTING",
            "FALSETTO", "BREATH", "PHRASING", "DICTION", "ENUNCIATE",
            "ARTICULATE", "DUO", "ECHO",
        ]),
    ])
    trivia_easy = [
        {"q": "Which instrument has black and white keys?",
         "options": ["Piano", "Drum", "Flute"], "answer": "Piano"},
        {"q": "Who stands in front of an orchestra and leads it?",
         "options": ["The conductor", "The drummer", "The usher"],
         "answer": "The conductor"},
        {"q": "Which string instrument is played with a bow?",
         "options": ["Violin", "Piano", "Trumpet"], "answer": "Violin"},
        {"q": "What do we call a person who acts in a film?",
         "options": ["An actor", "A doctor", "A baker"], "answer": "An actor"},
        {"q": "Which snack is most famous at the cinema?",
         "options": ["Popcorn", "Soup", "Salad"], "answer": "Popcorn"},
        {"q": "What is the name of the golden statue for films?",
         "options": ["Oscar", "Grammy", "Emmy"], "answer": "Oscar"},
        {"q": "Which award honours the best music recordings?",
         "options": ["Grammy", "Oscar", "Tony"], "answer": "Grammy"},
        {"q": "Who guides the actors and the making of a movie?",
         "options": ["The director", "The usher", "The composer"],
         "answer": "The director"},
        {"q": "How many strings does a standard guitar have?",
         "options": ["Six", "Two", "Ten"], "answer": "Six"},
        {"q": "Which of these is a slow, graceful ballroom dance?",
         "options": ["Waltz", "March", "Disco"], "answer": "Waltz"},
        {"q": "What do you call the words of a song?",
         "options": ["Lyrics", "Script", "Tune"], "answer": "Lyrics"},
        {"q": "Which part of a film rolls at the very end?",
         "options": ["The credits", "The trailer", "The poster"],
         "answer": "The credits"},
    ]
    phrase_medium = [
        {"prompt": "That idea is music to my ____", "answer": "Ears"},
        {"prompt": "It's time to face the ____", "answer": "Music"},
        {"prompt": "I don't need sheet music, I'll play it by ____",
         "answer": "Ear"},
        {"prompt": "He keeps repeating himself, like a broken ____",
         "answer": "Record"},
        {"prompt": "No matter what, the show must go ____", "answer": "On"},
        {"prompt": "In dancing, it takes two to ____", "answer": "Tango"},
        {"prompt": "Before going on stage, actors wish each other: break a ____",
         "answer": "Leg"},
        {"prompt": "She likes to march to the beat of her own ____",
         "answer": "Drum"},
        {"prompt": "It was a grand show, all singing, all ____",
         "answer": "Dancing"},
        {"prompt": "A picture is worth a thousand ____", "answer": "Words"},
    ]
    trivia_open = [
        {"q": "Name the instrument with 88 black and white keys.",
         "answer": "Piano"},
        {"q": "What do you call the music specially written for a film?",
         "answer": "A soundtrack"},
        {"q": "Which passionate dance is famous in Argentina?",
         "answer": "Tango"},
        {"q": "What is a person who writes music called?",
         "answer": "A composer"},
        {"q": "Name the wooden string instrument played with a bow.",
         "answer": "A violin"},
        {"q": "What is the grand Hollywood ceremony that hands out the Oscars?",
         "answer": "The Academy Awards"},
        {"q": "Which hand drum has small metal jingles around its rim?",
         "answer": "A tambourine"},
        {"q": "What word describes how high or low a musical sound is?",
         "answer": "Pitch"},
    ]
    crossword = [
        ("PIANO", "Instrument with 88 keys"),
        ("GUITAR", "Six-stringed instrument"),
        ("VIOLIN", "Bowed string instrument"),
        ("FLUTE", "High woodwind instrument"),
        ("DRUM", "You beat it with sticks"),
        ("MOVIE", "A film shown in cinemas"),
        ("OSCAR", "Famous golden film award"),
        ("GRAMMY", "Top music award"),
        ("POPCORN", "Favourite cinema snack"),
        ("ACTOR", "Person who plays a role"),
        ("DIRECTOR", "Person who guides a film"),
        ("MELODY", "The main tune of a song"),
        ("TEMPO", "The speed of the music"),
        ("CHORD", "Three or more notes together"),
        ("BALLET", "Graceful dance on pointe"),
        ("TANGO", "Passionate ballroom dance"),
        ("HERO", "The main good character"),
        ("VILLAIN", "The bad character in a story"),
        ("LYRICS", "The words of a song"),
        ("COMPOSER", "Person who writes music"),
        ("STAGE", "Where actors perform"),
        ("CURTAIN", "It rises and falls in a theatre"),
        ("SCRIPT", "Written text of a play or film"),
        ("JAZZ", "Music style with swing and blues"),
        ("OPERA", "Drama sung on stage"),
        ("COMEDY", "Film genre that makes you laugh"),
        ("DRAMA", "Serious film or play"),
        ("CINEMA", "Place where films are shown"),
        ("ROCK", "Loud guitar-driven music"),
        ("WALTZ", "Smooth dance in three time"),
    ]
    remedies = [
        {"condition": "Hoarse Voice",
         "text": "Rest your voice and sip warm, not hot, water with a little "
                 "honey and a pinch of turmeric. Chew licorice root to soothe the "
                 "throat. Avoid throat-clearing and dry, smoky rooms until your "
                 "voice feels easy again."},
        {"condition": "Dry Cough",
         "text": "A spoon of honey with a pinch of black pepper and turmeric "
                 "soothes the throat and calms the cough reflex. Warm ginger tea "
                 "and steam with a little mint or eucalyptus add moisture. Keep "
                 "the room air from getting too dry."},
        {"condition": "Screen Eye Strain",
         "text": "Follow the 20-20-20 rule: every 20 minutes look at something 20 "
                 "feet away for 20 seconds. Blink often, rest cool cucumber or "
                 "rosewater pads over closed eyes, and try gentle palming. Soft "
                 "room lighting eases tired sight."},
        {"condition": "Tension Headache",
         "text": "Sip ginger tea, rest in a dim, quiet room, and press a cool "
                 "cloth on your forehead. A drop of eucalyptus oil on the temples "
                 "eases the tightness. Headaches often follow long screen time, "
                 "noise, or missed meals."},
        {"condition": "Stiff Neck From Sitting",
         "text": "Loosen the shoulders and roll the neck gently, then massage "
                 "with warm sesame oil. A warm cloth on the back of the neck "
                 "softens tight muscles. Good posture and a supportive chair help "
                 "prevent it."},
        {"condition": "Ginger Tea",
         "text": "Simmer a few slices of fresh ginger in water for a few minutes, "
                 "strain, and add honey or lemon. A warm cup eases indigestion, "
                 "chills, and clears the voice."},
        {"condition": "Pomegranate Juice",
         "text": "Sip a glass of fresh pomegranate juice. It is refreshing, "
                 "gentle on the stomach, and a traditional heart-friendly drink "
                 "with a little natural iron."},
    ]
    coloring = ["guitar", "record", "star", "bird", "butterfly", "sun"]
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


BANKS = {"musicmovies": build}

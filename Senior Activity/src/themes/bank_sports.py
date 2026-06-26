"""Sports, Games & Hobbies - evergreen, all-country content bank."""
from __future__ import annotations
from collections import OrderedDict


def build() -> dict:
    word_pools = OrderedDict([
        ("Sports", [
            "SOCCER", "TENNIS", "GOLF", "CRICKET", "BASKETBALL", "BASEBALL",
            "VOLLEYBALL", "HOCKEY", "RUGBY", "BADMINTON", "SWIMMING", "BOXING",
            "CYCLING", "SKATING", "SKIING", "ARCHERY", "FENCING", "WRESTLING",
            "JUDO", "KARATE", "ROWING", "SAILING", "SURFING", "DIVING",
            "RUNNING", "JOGGING", "HIKING", "CLIMBING", "GYMNASTICS", "BOWLING",
            "SQUASH", "NETBALL", "HANDBALL", "POLO", "LACROSSE", "FOOTBALL",
            "BILLIARDS", "SNOOKER", "DARTS", "MARATHON", "SPRINTING", "HURDLES",
            "TRIATHLON", "DECATHLON", "WEIGHTLIFTING", "AEROBICS", "YOGA",
            "PILATES", "SKATEBOARDING", "SNOWBOARDING", "BUNGEE", "PARAGLIDING",
            "HANGLIDING", "SKYDIVING", "BALLET", "TAEKWONDO", "AIKIDO", "SUMO",
            "PINGPONG", "RACQUETBALL", "PADDLEBALL", "KICKBOXING", "CURLING",
            "BOBSLEIGH", "LUGE", "TOBOGGAN", "BIATHLON", "SLALOM", "CANOEING",
            "KAYAKING", "RAFTING", "PADDLING", "PARKOUR", "CALISTHENICS",
            "TRAMPOLINE", "PENTATHLON", "HEPTATHLON", "EQUESTRIAN",
        ]),
        ("Equipment & Gear", [
            "RACKET", "BAT", "BALL", "GLOVES", "STICK", "PUCK", "HELMET", "NET",
            "SHUTTLECOCK", "PAD", "GUARD", "CLEAT", "WHISTLE", "CONE", "JERSEY",
            "BOOT", "SNEAKER", "GOGGLES", "PADDLE", "OAR", "SADDLE", "BATON",
            "DUMBBELL", "TREADMILL", "MAT", "ROPE", "FRISBEE", "RIBBON",
            "DARTBOARD", "TARGET", "CLUB", "CUE", "SHINGUARD", "KNEEPAD",
            "ELBOWPAD", "MOUTHGUARD", "FACEGUARD", "CHESTPAD", "GLOVE", "SHOE",
            "SPIKE", "FLAG", "POST", "CROSSBAR", "GOALPOST", "STOPWATCH",
            "SCOREPAD", "CHALK", "HARNESS", "CARABINER", "GRIP", "SOCK", "CAP",
            "VISOR", "STRAP", "TEE", "BASE", "WICKET", "STUMP", "BAIL",
            "WATERBOTTLE", "TOWEL", "TIMER", "HORN", "BELL", "HALTER", "BRIDLE",
            "REIN", "STIRRUP", "HOOP", "PUTTER", "GLOVEBAG", "BALLBAG",
            "CARRIER", "BAG", "PUMP", "NEEDLE", "PINS", "BATGRIP", "GRIPWRAP",
        ]),
        ("Board & Card Games", [
            "CHESS", "DICE", "PUZZLE", "CHECKERS", "BACKGAMMON", "CARDS",
            "DOMINO", "SCRABBLE", "MONOPOLY", "SUDOKU", "BRIDGE", "SOLITAIRE",
            "JOKER", "PAWN", "KING", "QUEEN", "BISHOP", "KNIGHT", "ROOK", "ACE",
            "JACK", "SPADE", "HEART", "DIAMOND", "TOKEN", "TILE", "DECK",
            "RUMMY", "POKER", "WHIST", "EUCHRE", "CANASTA", "PINOCHLE", "BINGO",
            "CLUEDO", "RISK", "DRAUGHTS", "SHOGI", "MANCALA", "LUDO",
            "PICTIONARY", "MEMORY", "SNAP", "WAR", "CRIBBAGE", "HEARTS",
            "SPADES", "TAROT", "BANKER", "ROLL", "DEAL", "SHUFFLE", "GAMBIT",
            "CASTLE", "CHECKMATE", "STALEMATE", "TRUMP", "SUIT", "FOLD", "RAISE",
            "ANTE", "POT", "BET", "HAND", "PILE", "DRAWPILE", "BOARD", "SPINNER",
            "MOVE", "TURN", "HOP", "TOKENS", "MEEPLE", "CUBE", "PROMPT", "BUZZER",
        ]),
        ("Outdoor Games", [
            "HOPSCOTCH", "KITE", "MARBLE", "YOYO", "TOP", "SLINGSHOT", "RACE",
            "RELAY", "TUGOFWAR", "SACKRACE", "SKIPPING", "HOPPING", "JUMPING",
            "LEAP", "THROW", "CATCH", "TAG", "BALANCE", "SWING", "SLIDE",
            "ROUNDERS", "BOWLS", "CROQUET", "QUOITS", "TETHERBALL", "KICKBALL",
            "HIDESEEK", "BLINDMAN", "REDROVER", "PIGGYBACK", "SEESAW",
            "FOURSQUARE", "KICKTHECAN", "DODGEBALL", "SPUD", "JACKS", "MARBLES",
            "STILTS", "HULAHOOP", "SKIPPINGROPE", "CONKER", "BOULES", "PETANQUE",
            "SKITTLES", "BEANBAG", "CORNHOLE", "LADDER", "RINGTOSS", "EGGRACE",
            "WHEELBARROW", "THREELEGGED", "OBSTACLE", "PARACHUTE", "TUNNEL",
            "BALANCEBEAM", "STEPPINGSTONE", "NATURE", "SCAVENGER", "TRAIL",
        ]),
        ("Hobbies & Crafts", [
            "KNITTING", "PAINTING", "GARDENING", "READING", "DRAWING", "SEWING",
            "EMBROIDERY", "QUILTING", "POTTERY", "SCULPTURE", "PHOTOGRAPHY",
            "STAMPING", "CALLIGRAPHY", "ORIGAMI", "WOODWORK", "CARVING",
            "WEAVING", "CROCHET", "CROSSSTITCH", "BEADING", "SCRAPBOOK",
            "JOURNAL", "COOKING", "BAKING", "WRITING", "SINGING", "DANCING",
            "PLAYING", "COLLECTING", "BIRDWATCHING", "FISHING", "WALKING",
            "SKETCHING", "DOODLING", "COLORING", "COLLAGE", "DECOUPAGE",
            "MOSAIC", "ENGRAVING", "PRINTMAKING", "BONSAI", "ARRANGING",
            "IKEBANA", "LACEMAKING", "SPINNING", "DYEING", "SOAPMAKING",
            "CANDLEMAKING", "BREWING", "FERMENTING", "PICKLING", "PRESERVING",
            "FORAGING", "CAMPING", "ORIENTEERING", "GEOCACHING", "STARGAZING",
            "ASTRONOMY", "TELESCOPE", "MICROSCOPE", "COLLECTIBLE", "PHILATELY",
            "NUMISMATICS", "ANTIQUING", "DIORAMA", "MODELMAKING", "RAILWAY",
            "DRONE", "STAMP", "COIN", "BUTTON", "POSTCARD", "SHELL", "ROCK",
            "BUTTONS", "MAGNET", "BADGE", "PIN", "FABRIC", "THREAD", "NEEDLE",
            "YARN", "WOOL", "COTTON", "BRUSH", "PALETTE", "EASEL", "CANVAS",
            "CLAY", "GLAZE", "KILN", "WHEEL", "LOOM", "SPINDLE", "CHISEL",
            "GOUGE", "MALLET",
        ]),
        ("Playing Terms", [
            "TEAM", "SCORE", "GOAL", "MATCH", "WIN", "LOSS", "TIE", "DRAW",
            "FOUL", "PENALTY", "REFEREE", "UMPIRE", "CAPTAIN", "COACH",
            "PLAYER", "RIVAL", "CHAMPION", "TROPHY", "MEDAL", "RECORD",
            "TITLE", "LEAGUE", "TOURNAMENT", "SEASON", "ROUND", "HEAT",
            "INNING", "QUARTER", "HALFTIME", "TIMEOUT", "SUBSTITUTION",
            "ASSIST", "DRIBBLE", "TACKLE", "PASS", "SHOT", "SAVE", "BLOCK",
            "INTERCEPT", "STEAL", "REBOUND", "TURN", "OVERTIME", "PLAYOFF",
            "FINALS", "SEMIFINAL", "QUARTERFINAL", "ELIMINATE", "UPSET",
            "UNDERDOG", "FAVORITE", "SEED", "BYE", "RANKING", "STANDING",
            "SCORER", "LINEUP", "ROSTER", "SQUAD", "SUB", "BENCH", "FIXTURE",
            "DERBY", "CHAMPIONSHIP", "HATTRICK", "CLEANSHEET", "STREAK",
            "SLUMP", "RALLY", "COMEBACK", "BLANKS", "SHUTOUT", "DRAWN",
            "LEVEL", "DEUCE", "ADVANTAGE", "LEAD", "DEFICIT", "MARGIN",
            "UPSETTER", "TIEBREAK", "SUDDENDEATH", "WALKOVER", "FORFEIT",
        ]),
        ("Venues", [
            "STADIUM", "COURT", "FIELD", "ARENA", "TRACK", "POOL", "RINK", "GYM",
            "PITCH", "GREEN", "RANGE", "COURSE", "RING", "FAIRWAY", "BULLPEN",
            "DUGOUT", "GRANDSTAND", "PAVILION", "CLUBHOUSE", "SCOREBOARD",
            "TURF", "LAWN", "SAND", "TRAP", "BUNKER", "RIDGE", "BLEACHER",
            "TERRACE", "BOX", "SUITE", "TURNSTILE", "SLOPE", "TRAIL", "CIRCUIT",
            "VELODROME", "LANES", "BULLRING", "MARINA", "HARBOR", "LAKE",
            "RIVER", "BASECAMP", "HALL", "FIELDHOUSE", "SPORTSCENTER",
            "RECREATION", "STAND", "BLEACHERS", "VIEWING", "LODGE", "CHALET",
            "PARK", "RESERVE", "GROUNDS", "OVAL", "DIAMOND", "GRIDIRON",
            "BACKCOURT", "FORECOURT", "SIDELINE", "BASELINE", "BOUNDARY",
            "FENCE", "WALL", "ROOF", "DOME",
        ]),
        ("Positions & Moves", [
            "STRIKER", "KEEPER", "DEFENDER", "FORWARD", "MIDFIELDER", "BATTER",
            "BOWLER", "SERVER", "RECEIVER", "SETTER", "LIBERO", "GOALIE",
            "POINT", "RUN", "BIRDIE", "EAGLE", "STROKE", "SERVE", "VOLLEY",
            "SMASH", "ALLROUNDER", "SLIP", "GULLY", "COVER", "SWEEPER",
            "STOPPER", "WING", "CENTER", "PIVOT", "BLOCKER", "TACKLER",
            "CHASER", "RIDER", "DRIVER", "PITCHER", "CATCHER", "FIELDER",
            "RUNNER", "JUMPER", "THROWER", "LIFTER", "SKIER", "DIVER",
            "SWIMMER", "CLIMBER", "ROWER", "PADDLER", "CYCLIST", "ATHLETE",
            "OLYMPIAN", "AMATEUR", "ROOKIE", "SPECIALIST", "UTILITY", "RESERVE",
            "VETERAN", "CAPTAINED", "LEADER", "ANCHOR", "LINKMAN", "MARKER",
            "SWEEPER", "HOOPER", "CADDIE", "GOLFERS", "BOXER", "GRAPPLER",
            "STRIKER", "FASTBOWLER", "SPINNER", "WICKETKEEPER", "OPEN",
        ]),
        ("Water & Winter Sports", [
            "SNORKELING", "SCUBA", "WATERSKIING", "WAKEBOARDING", "PARASAILING",
            "JETSKI", "BODYBOARD", "KITEBOARDING", "WINDSURFING", "PADDLESURF",
            "SLEDDING", "MOGUL", "CROSSCOUNTRY", "HALFPIPE", "AXEL", "LUTZ",
            "TOELOOP", "SALCHOW", "FIGURESKATING", "SPEEDSKATING", "ICEHOCKEY",
            "SNOWBALL", "SNOWMAN", "SNOWSHOE", "SKIJUMPING", "SNOWBOARD",
            "GLACIER", "ALPINE", "NORDIC", "ICEDANCE", "WATERPOLO", "BUTTERFLY",
            "BACKSTROKE", "BREASTSTROKE", "SIDESTROKE", "FLOAT", "SPLASH",
            "TREADING", "REGATTA", "BOATING", "ANCHOR",
            "BUOY", "LIFEGUARD", "FLIPPER", "AIRTANK", "MASK", "FINS",
            "PADDLEBOARD", "SURFBOARD", "BODYBOARD", "WAKE", "TOW", "LAUNCH",
            "BOATRAMP", "MARINE", "REEF", "LAGOON", "BAY", "COVE", "INLET",
            "SLIPWAY", "DECKHAND", "SKIPPER", "CAPTAIN", "CREW",
        ]),
        ("Athletics", [
            "SPRINT", "JAVELIN", "DISCUS", "SHOTPUT", "HAMMER", "POLEVAULT",
            "HIGHJUMP", "LONGJUMP", "TRIPLEJUMP", "BLOCKS", "STARTER",
            "FINISHER", "LAP", "PACE", "STRIDE", "ENDURANCE", "STAMINA",
            "AGILITY", "SPEED", "STRENGTH", "FLEXIBILITY", "COORDINATION",
            "REFLEX", "WARMUP", "COOLDOWN", "STRETCH", "TRAINER", "ATHLETICS",
            "EVENT", "ROADRACE", "STEEPLECHASE", "RACEWALK", "ULTRAMARATHON",
            "TIMETRIAL", "BARBELL", "KETTLEBELL", "MEDICINEBALL", "BOXJUMP",
            "BURPEE", "PLANK", "SQUAT", "LUNGE", "CRUNCH", "PRESSUP", "PUSHUP",
            "SITUP", "CHINUP", "PULLUP", "SHUTTLE", "SHUTTLERUN", "JOG",
            "WALKING", "STRIDER", "JUMPER", "VAULTER", "THROWERS", "RUNNERS",
            "HURDLER", "SPRINTER", "DISTANCE", "MIDDLE", "RELAY", "BATON",
            "EXCHANGE", "ZONE", "STARTLINE", "FINISHLINE", "TIMER", "STAND",
            "FORM", "TECHNIQUE", "DRILL", "REPS", "SETS", "REST", "RECOVERY",
        ]),
    ])
    trivia_easy = [
        {"q": "How many players from one team are on the field in a soccer "
              "match?",
         "options": ["11", "9", "7"], "answer": "11"},
        {"q": "Wimbledon is famous for which sport?",
         "options": ["Tennis", "Golf", "Cricket"], "answer": "Tennis"},
        {"q": "Which chess piece moves only in an L-shape?",
         "options": ["Knight", "Bishop", "Rook"], "answer": "Knight"},
        {"q": "How many colored rings are on the Olympic flag?",
         "options": ["Five", "Four", "Six"], "answer": "Five"},
        {"q": "Which racket sport uses a shuttlecock (birdie)?",
         "options": ["Badminton", "Tennis", "Squash"], "answer": "Badminton"},
        {"q": "Which sport is played over 18 holes with clubs?",
         "options": ["Golf", "Baseball", "Hockey"], "answer": "Golf"},
        {"q": "How many pins stand in a game of ten-pin bowling?",
         "options": ["Ten", "Eight", "Twelve"], "answer": "Ten"},
        {"q": "Which board game makes words with letter tiles?",
         "options": ["Scrabble", "Chess", "Dominoes"], "answer": "Scrabble"},
        {"q": "Which card game tries to reach a total of twenty-one?",
         "options": ["Blackjack", "Bridge", "Solitaire"], "answer": "Blackjack"},
        {"q": "Which gym machine has a moving belt you walk or run on?",
         "options": ["A treadmill", "A rower", "A stepper"],
         "answer": "A treadmill"},
        {"q": "Which hobby uses needles and yarn to make fabric?",
         "options": ["Knitting", "Pottery", "Carving"], "answer": "Knitting"},
        {"q": "What do you call the person who runs a soccer match?",
         "options": ["A referee", "A coach", "A captain"], "answer": "A referee"},
    ]
    phrase_medium = [
        {"prompt": "Practice makes ____", "answer": "Perfect"},
        {"prompt": "It's not whether you win or lose, it's how you play the ____",
         "answer": "Game"},
        {"prompt": "Win some, ____ some", "answer": "Lose"},
        {"prompt": "On your marks, get set, ____", "answer": "Go"},
        {"prompt": "Throw in the ____", "answer": "Towel"},
        {"prompt": "Hit it out of the ____", "answer": "Park"},
        {"prompt": "Level the playing ____", "answer": "Field"},
        {"prompt": "Drop the ____", "answer": "Ball"},
        {"prompt": "A good sport plays by the ____", "answer": "Rules"},
        {"prompt": "That was a home ____", "answer": "Run"},
    ]
    trivia_open = [
        {"q": "Name the board game where you checkmate the opponent's king.",
         "answer": "Chess"},
        {"q": "Which sport is played on ice with a puck and sticks?",
         "answer": "Ice hockey"},
        {"q": "Name the shiny prize given to the winner of a competition.",
         "answer": "A trophy"},
        {"q": "What do you call the hobby of folding paper into shapes?",
         "answer": "Origami"},
        {"q": "Which indoor game is played on a table with cues and balls?",
         "answer": "Billiards"},
        {"q": "Name the official who watches for fouls in a match.",
         "answer": "Referee"},
        {"q": "What do you call a list of the players in a team?",
         "answer": "A roster"},
        {"q": "Name the Olympic event of running, jumping, and throwing.",
         "answer": "Athletics"},
    ]
    crossword = [
        ("SOCCER", "Sport played with a round ball and two nets"),
        ("TENNIS", "Racket sport played across a net"),
        ("GOLF", "Sport played over 18 holes with clubs"),
        ("CRICKET", "Bat-and-ball sport loved in England and India"),
        ("CHESS", "Board game of kings and queens"),
        ("DICE", "Cubes with dots used in many games"),
        ("PUZZLE", "Brain teaser made of pieces"),
        ("RACKET", "Stringed tool used to hit a ball"),
        ("BALL", "Round object you throw, kick, or hit"),
        ("BAT", "Wooden stick used to strike a ball"),
        ("GLOVES", "Hand cover worn by boxers and goalkeepers"),
        ("HELMET", "Hard hat worn to protect the head"),
        ("GOAL", "The net a striker aims the ball into"),
        ("SCORE", "The number of points a team has"),
        ("TEAM", "A group of players on one side"),
        ("MATCH", "A single game between two sides"),
        ("TROPHY", "Shiny prize given to the winner"),
        ("MEDAL", "Award hung around a champion's neck"),
        ("STADIUM", "Large arena where thousands watch sport"),
        ("COURT", "Marked surface for tennis or basketball"),
        ("FIELD", "Grassy ground where games are played"),
        ("REFEREE", "Official who enforces the rules"),
        ("COACH", "Person who trains and guides a team"),
        ("KNITTING", "Hobby using needles and yarn"),
        ("GARDENING", "Hobby of growing plants and flowers"),
        ("PAINTING", "Art hobby using brushes and colors"),
        ("MARBLE", "Small glass ball used in a playground game"),
        ("KITE", "Toy flown in the wind on a string"),
        ("YOYO", "Toy that climbs back up its string"),
        ("CARD", "Rectangular piece used in games like bridge"),
    ]
    remedies = [
        {"condition": "Muscle Ache After Activity",
         "text": "Rest the sore area and massage it with warm sesame or mustard "
                 "oil. A cup of turmeric milk and a warm compress ease the "
                 "stiffness. Gentle stretching and a short walk the next day "
                 "help you feel limber again."},
        {"condition": "Minor Sprain",
         "text": "First rest the limb, keep it raised, and apply a cool compress "
                 "to reduce swelling. Later, a warm ginger or turmeric paste and "
                 "sesame-oil massage support recovery. Move it gently as the "
                 "soreness fades, and seek help if it will not bear weight."},
        {"condition": "Stiff Calf Cramp",
         "text": "Gently stretch the calf and massage it with warm mustard oil. "
                 "A glass of water with a pinch of salt and lemon, and steady "
                 "hydration, help prevent cramps. Building up activity slowly "
                 "also makes a difference."},
        {"condition": "Low Energy & Midday Slump",
         "text": "Drink a glass of water, eat a few soaked almonds or dates, and "
                 "take a short walk in fresh air. A spoon of honey in warm water "
                 "is a traditional quick lift. Regular sleep and small meals "
                 "keep energy steadier through the day."},
        {"condition": "Tired, Aching Feet",
         "text": "Soak your feet in warm water with a little rock salt and "
                 "ginger, then massage with sesame oil. Rest with your feet "
                 "raised for a while. Comfortable, well-cushioned shoes ease the "
                 "next ache."},
        {"condition": "Soaked Dates & Almonds",
         "text": "Soak a few dates and almonds overnight, then eat them in the "
                 "morning. This simple habit gives steady energy, a little iron, "
                 "and lasting strength for an active day."},
        {"condition": "Clarified Butter (Ghee) in Warm Milk",
         "text": "Stir a teaspoon of clarified butter (ghee) into warm milk at "
                 "night. It is said to lubricate the joints, ease constipation, "
                 "and nourish the body after an active day."},
    ]
    coloring = ["flower", "butterfly", "wateringcan", "sun", "guitar", "star"]
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


BANKS = {"sports": build}

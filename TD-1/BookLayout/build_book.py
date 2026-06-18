"""
Build Book - The Glitch Squad series (Geronimo Edition)
Images integrated with scene spotlights, locations, and diagrams replacing comic strips.
Usage:
    python build_book.py --book 1 --pdf
    python build_book.py --book 1 --pdf --chapters 1 2 3
"""
import json, re, shutil, argparse
from pathlib import Path
from PIL import Image

SERIES_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = SERIES_DIR / "Images"
CSS_DIR = Path(__file__).resolve().parent / "css"
FONTS_DIR = Path(__file__).resolve().parent / "fonts"

BOOK_TITLES = {
    1: "THE LOST SIGNAL", 2: "THE PHANTOM NETWORK", 3: "THE INVISIBLE MAZE",
    4: "THE DIGITAL GARDEN", 5: "THE MIRROR CODE", 6: "THE SILENT FREQUENCY",
    7: "THE CLOCKWORK KEY", 8: "THE PIXEL THIEF", 9: "THE LAST BEACON",
    10: "THE FINAL REBOOT",
}

SECTION_DIVIDERS = {
    1: ("PART ONE", "DISCOVERY", "SD-01"),
    6: ("PART TWO", "THE GLITCH WAVE", "SD-02"),
    13: ("PART THREE", "THE GRIDLORD", "SD-03"),
    23: ("PART FOUR", "MISSION NEONVILLE", "SD-04"),
    32: ("PART FIVE", "THE BEGINNING", "SD-05"),
}

CHAPTER_CHARACTERS = {
    1: "maya", 2: "maya", 3: "maya", 4: "blip", 5: "blip",
    6: "blip", 7: "blip", 8: "blip", 9: "maya", 10: "blip",
    11: "maya", 12: "blip", 13: "sam", 14: "blip", 15: "blip",
    16: "maya", 17: "leo", 18: "zara", 19: "maya",
}

GLITCH_CHAPTERS = {7, 14, 15}

DIVIDER_ICONS = {"maya": "\u2699", "leo": "\u2605", "zara": "\u2726", "sam": "\u2605", "blip": "\u25A0"}

FRAME_FOR_CHAR = {"maya": "frame-gear", "leo": "frame-screen", "zara": "frame-splatter", "sam": "frame-starburst", "blip": "frame-blip"}

SPOT_FRAMES = ['frame-rounded', 'frame-blob', 'frame-slash', 'frame-wave', 'frame-starburst', 'frame-splatter',
                'frame-circle', 'frame-gear', 'frame-blip', 'frame-screen']

PAGE_BG = {"maya": "#F5F8F0", "leo": "#F0F2F8", "zara": "#FFF8E8", "sam": "#FFF0F0", "blip": "#F0FAFB"}

WORDS_PER_PAGE = 160
HALF_PAGE_COST = 80
SPOT_COST = 30
MIN_WORDS_FLUSH = 80
MIN_WORDS_FLUSH_IMAGE = 90
MIN_WORDS_MERGE = 70



CHARS_INTRODUCED_BY_CH = {
    1: {"MAYA"}, 2: {"MAYA"}, 3: {"MAYA"}, 4: {"MAYA", "BLIP"},
    5: {"MAYA", "BLIP"}, 6: {"MAYA", "BLIP", "LEO", "ZARA", "SAM"},
    7: {"MAYA", "BLIP", "LEO", "ZARA", "SAM", "GRIDLORD"},
    8: {"MAYA", "BLIP", "LEO", "ZARA", "SAM", "GRIDLORD"},
    9: {"MAYA", "BLIP", "LEO", "ZARA", "SAM", "GRIDLORD"},
    10: {"MAYA", "BLIP", "LEO", "ZARA", "SAM", "GRIDLORD"},
    11: {"MAYA", "BLIP", "LEO", "ZARA", "SAM", "GRIDLORD", "DAADI"},
}

GERONIMO_CODES = {
    'M': 'maya', 'Z': 'leo', 'S': 'zara', 'L': 'sam',
    'B': 'blip', 'G': 'gridlord', 'D': 'daadi', 'F': 'sfx',
}

BLIP_MARGIN_IMAGES = {
    'happy': 'Marginalia/blip_happy.png', 'scared': 'Marginalia/blip_scared.png',
    'confused': 'Marginalia/blip_confused.png', 'excited': 'Marginalia/blip_excited.png',
    'thinking': 'Marginalia/blip_thinking.png', 'love': 'Marginalia/blip_love.png',
    'loading': 'Marginalia/blip_loading.png', 'sleepy': 'Marginalia/blip_sleepy.png',
    'laugh': 'Marginalia/blip_laugh.png', 'determined': 'Marginalia/blip_determined.png',
    'sad': 'Marginalia/blip_sad.png', 'mischievous': 'Marginalia/blip_mischievous.png',
}
BLIP_MARGIN_EMOTIONS = list(BLIP_MARGIN_IMAGES.keys())

NAME_PATTERNS = [
    (r'\bDaadi\b', 'daadi'), (r'\bGridlord\b', 'gridlord'), (r'\bKira\b', 'kira'),
    (r'\bMaya\b', 'maya'), (r'\bLeo\b', 'leo'), (r'\bZara\b', 'zara'),
    (r'\bSam\b', 'sam'), (r'\bBlip\b', 'blip'),
    (r'\bthe cube\b', 'blip'), (r'\bthe robot\b', 'blip'),
]

CATCHPHRASES = {
    "i can fix that": "maya", "i can fix anything": "maya",
    "i'm innovating": "maya", "innovating": "maya",
    "challenge accepted": "sam", "error 404": "leo",
    "hold on, let me draw": "zara", "hold on. let me draw": "zara",
    "maya-beta": "daadi", "just some junk": "maya",
    "yes please": "maya", "...yes": "maya",
    "waste not, want not": "daadi", "regular junk": "daadi",
    "then tell me": "daadi", "innovate less": "daadi",
}

BLIP_INTERACTIVE_QUESTIONS = {
    1: "Can YOU find all three inventions Maya has broken this week?",
    2: "How many places in YOUR neighborhood have secret basements?",
    3: "Can YOU spot the moment Blip first wakes up?",
    4: "What would YOU say to a robot that just learned what 'hungry' means?",
    5: "How many glitches can YOU spot on Maple Street?",
    6: "If YOUR backpack could do ONE thing, what would it be?",
    7: "Can YOU decode the symbol puzzle before the Squad does?",
    8: "What's the WEIRDEST thing YOU'VE ever found in a basement?",
    9: "Count the Blip faces in this chapter. How many emotions does he show?",
    10: "What would YOU name the team?",
    11: "Can YOU draw what YOU think the Gridlord looks like?",
    12: "What gadget would YOU build to find a hidden signal?",
    13: "Which glitch would YOU fix first — and HOW?",
    14: "Find the THREE hidden clues the Gridlord left in this chapter!",
    15: "If YOU were Blip, would YOU make the same choice?",
    16: "What's YOUR Daadi's best advice? Write it down!",
    17: "Can YOU spot the code pattern before Leo does?",
    18: "What does YOUR squad do at sunset?",
    19: "What was YOUR favorite moment in the whole adventure?",
}

FIND_OBJECTS = {
    2: ("Find the HIDDEN DOOR in the basement illustration!", "Marginalia/blip_thinking.png"),
    5: ("Count ALL the glitched objects on Maple Street. How many can YOU find?", "Marginalia/blip_confused.png"),
    7: ("The Gridlord hid THREE symbols in this chapter. Can YOU find them all?", "Marginalia/blip_mischievous.png"),
    9: ("Blip's screen shows different faces. Count how many DIFFERENT emotions you see!", "Marginalia/blip_excited.png"),
    14: ("The Gridlord's message has a SECRET CODE hidden in it. Can YOU crack it?", "Marginalia/blip_determined.png"),
    17: ("Leo's code has a pattern. Can YOU spot what comes NEXT in the sequence?", "Marginalia/blip_thinking.png"),
}

PULL_QUOTES = {
    1: "~M:I can fix that!~", 2: "~G:Old buildings have old secrets.~",
    3: "~M:We were the only ones who could hear it.~",
    4: "~B:【Hello. Why does everything smell like old soup?】~",
    5: "~S:FIRST GLITCH — CLEARED!~",
    6: "~L:CHALLENGE ACCEPTED!~", 8: "~B:【I contain MULTITUDES, Zara!】~",
    9: "~S:That was TWELVE STARS!~",
    10: "~M:We're the GLITCH SQUAD!~",
    11: "~Z:Hold on, let me draw the plan.~",
    12: "~L:Error 404: Normal Not Found.~",
    13: "~S:CHALLENGE ACCEPTED!~",
    14: "~G:I didn't CAUSE the glitches. I FOUND them.~",
    15: "~B:【Processing... I choose THIS.】~",
    16: "~D:Maya-beta, the broken wire carries no current. Find where it disconnected.~",
    17: "~L:The signal isn't random. It's a pattern.~",
    18: "~M:This is the most beautiful normal anyone has ever seen.~",
    19: "~B:【I do not know. But I am learning.】~",
}

SFX_WORDS = frozenset([
    'KRRRRZZZT', 'KRRRRZZZZT', 'BZZZT', 'CRUNCH', 'WHIRRRRRR', 'WHIRRRRRRRRR',
    'SPLOOSH', 'SPLOOOOSH', 'SNICK', 'SNAP', 'POP', 'CLUNK', 'CLICK',
    'CLICK-CLICK', 'BOOM', 'ZZZT', 'BANG', 'WHOOOOSH', 'WHOOSH',
    'SPROING', 'FWOOOOOOSH', 'THUMP', 'KSSSSSHHHHHHT', 'SNIP',
    'DRIP-DRIP-DRIP', 'VRROOOOM', 'CLOP-CLOP-CLOP', 'WEEEEEEOOOOOOO',
    'CLICK-CLICK-CLICK-CLICK', 'ZZZZZT',
])
SFX_PREFIXES = ('KRRR', 'WHIRR', 'SPLOO', 'BZZZ', 'CLUN', 'SNIC', 'CLIC',
                'FWOO', 'KSSS', 'DRIP', 'VRRO', 'CLOP', 'WEEE', 'SNAP', 'SPRO', 'THUM', 'ZZZT', 'ZZZZ')

SFX_STYLES = {
    'KRRR': 'sfx-electric', 'BZZZ': 'sfx-electric', 'ZZZT': 'sfx-electric', 'ZZZZ': 'sfx-electric',
    'KSSS': 'sfx-electric', 'WEEE': 'sfx-electric',
    'SPLOO': 'sfx-splash', 'DRIP': 'sfx-splash', 'FWOO': 'sfx-splash',
    'CLIC': 'sfx-click', 'SNIC': 'sfx-click', 'SNAP': 'sfx-click', 'SNIP': 'sfx-click',
    'WHIRR': 'sfx-crash', 'WHOOO': 'sfx-whoosh', 'CRUNCH': 'sfx-crash', 'CLUN': 'sfx-crash',
    'THUM': 'sfx-big', 'VRRO': 'sfx-big', 'BOOM': 'sfx-big', 'BANG': 'sfx-big',
    'SPRO': 'sfx-whoosh', 'CLOP': 'sfx-click',
}
SPOT_SHAPES = ['star-shape', 'gear-shape', 'splatter-shape']

BLIP_FACE_COLORS = {
    '■‿■': 'var(--color-blip)', '●‿●': 'var(--color-blip)', '▲': 'var(--color-blip)',
    '▽': 'var(--color-glitch)', '●_●': '#e67e22', '□□': '#888',
    '○_○': '#e74c3c', '⏴‿⏴': 'var(--color-blip)', '⏴_⏴': 'var(--color-blip)',
    '●?●': '#9b59b6', '○□○': '#e74c3c',
}

PULL_QUOTE_TRIGGERS = [
    (r'felt something she hadn\'t expected', 'maya'), (r'changed everything', 'glitch'),
    (r'real game hasn\'t started', 'glitch'), (r'will be watching', 'glitch'),
    (r'never been so', 'glitch'), (r'entire history of sandwiches', 'blip'),
    (r'you\'re made of', 'glitch-blue'), (r'didn\'t see code.*saw\b', 'zara'),
    (r'never NOT fixed', 'maya'), (r'exactly the right shape', 'maya'),
    (r'creeps.*do not enjoy', 'blip'), (r'twelve stars', 'sam'),
    (r'old buildings have old secrets', 'maya'),
]
def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

MAX_IMG_LONG_EDGE = 1650
JPEG_QUALITY = 85

def _compress_image(src_path, dest_path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    jpg_dest = dest_path.with_suffix('.jpg')
    if jpg_dest.exists():
        return jpg_dest
    try:
        img = Image.open(src_path)
        if img.mode in ('RGBA', 'LA', 'P'):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            bg.paste(img, mask=img.split()[-1] if 'A' in img.mode else None)
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        w, h = img.size
        long_edge = max(w, h)
        if long_edge > MAX_IMG_LONG_EDGE:
            scale = MAX_IMG_LONG_EDGE / long_edge
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        img.save(jpg_dest, 'JPEG', quality=JPEG_QUALITY, dpi=(300, 300))
        return jpg_dest
    except Exception as e:
        print(f"  WARN: compress failed for {src_path}: {e}")
        shutil.copy2(src_path, dest_path)
        return dest_path

def img_rel(file_ref, compressed_dir):
    filename = Path(file_ref)
    orig = IMAGES_DIR / filename
    if orig.exists():
        dest = compressed_dir / filename
        result = _compress_image(orig, dest)
        return "images/" + result.relative_to(compressed_dir).as_posix()
    for suffix in ['.jpg', '.png']:
        check = filename.with_suffix(suffix)
        dest = compressed_dir / check
        if dest.exists():
            return "images/" + check.as_posix()
        orig_check = IMAGES_DIR / check
        if orig_check.exists():
            result = _compress_image(orig_check, compressed_dir / check)
            return "images/" + result.relative_to(compressed_dir).as_posix()
    return "images/" + filename.with_suffix('.jpg').as_posix()

def load_manifest(path):
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

def parse_manuscript(path, only_chapters=None):
    with open(path, "r", encoding="utf-8") as f: text = f.read()
    parts = re.split(r'^## Chapter (\d+) \u2014 (.+)$', text, flags=re.M)
    chapters = []
    for i in range(1, len(parts) - 1, 3):
        num, title, body = int(parts[i]), parts[i + 1].strip(), parts[i + 2].strip()
        if only_chapters is None or num in only_chapters:
            chapters.append({"num": num, "title": title, "body": body})
    return chapters

def get_chapter_images(manifest, ch):
    items = []
    for key in ["illustrations", "extra_spots", "glitch_art", "documents"]:
        for item in manifest.get(key, []):
            ic = item.get("chapter", item.get("chapters", None))
            if ic == ch or (isinstance(ic, list) and ch in ic): items.append(item)
    for item in manifest.get("scene_spotlights", []):
        cs = item.get("chapter", None)
        if cs == ch or (isinstance(cs, list) and ch in cs): items.append({**item, "type": "scene_spotlight"})
    for item in manifest.get("locations", []):
        cs = item.get("chapter", None)
        if cs == ch or (isinstance(cs, list) and ch in cs): items.append({**item, "type": "location"})
    for item in manifest.get("diagrams", []):
        cs = item.get("chapter", None)
        if cs == ch or (isinstance(cs, list) and ch in cs): items.append({**item, "type": "diagram"})
    for item in manifest.get("maps", []):
        ic = item.get("chapter", item.get("chapters", None))
        if ic == ch or (isinstance(ic, list) and ch in ic): items.append({**item, "type": "map"})
    return items

def get_section_divider(manifest, div_id):
    for item in manifest.get("section_dividers", []):
        if item.get("id") == div_id: return item
    return None

def is_catchphrase(para):
    for cp, char in CATCHPHRASES.items():
        if cp in para.lower(): return cp, char
    return None, None

def blip_face_for(para):
    for pat, face in {'smiley face|smile': '\u25A0\u203F\u25A0', 'hopeful': '\u25CF\u203F\u25CF',
        'antenna.*flat': '\u25BD', 'antenna.*perk': '\u25B2', 'worried': '\u25CF_\u25CF',
        'went dark': '\u25A1\u25A1', 'went blank': '\u25A1\u25A1',
        'scared': '\u25CB_\u25CB', 'happy': '\u25F4\u203F\u25F4', 'sad': '\u25F4_\u25F4',
        'confused': '\u25CF?\u25CF', 'determined': '\u25B6_\u25C0', 'shocked': '\u25CB\u25A1\u25CB'}.items():
        if re.search(pat, para, re.I): return face
    return None

def check_pull_quote(para):
    for pat, char in PULL_QUOTE_TRIGGERS:
        if re.search(pat, para, re.I):
            clean = para.strip().strip('"')
            if 40 < len(clean) < 300: return clean, char
    return None, None

def detect_speaker(para, prev=None):
    in_q, outside, inside = False, [], []
    for ch in para:
        if ch == '"': in_q = not in_q
        elif not in_q: outside.append(ch)
        else: inside.append(ch)
    outside_text, inside_text = "".join(outside), "".join(inside)
    speech_verb = re.compile(r'\b(said|asked|shouted|whispered|called|muttered|grinned|agreed|added|continued|replied|announced|cried|yelled|murmured|told|explained|exclaimed|offered|suggested|began|finished|declared|insisted|argued|whined|complained|sighed|laughed|chuckled)\b', re.I)
    name_bv = re.compile('(' + '|'.join(n[1] for n in NAME_PATTERNS) + ')', re.I)
    matches = list(speech_verb.finditer(outside_text))
    if matches:
        closest = outside_text[:matches[0].start()]
        nm = name_bv.search(closest)
        if nm: return nm.group(0).lower()
    for pat, char in NAME_PATTERNS:
        if re.search(pat, outside_text, re.I): return char
    for cp, char in CATCHPHRASES.items():
        if cp in para.lower(): return char
    if para.startswith('"') and not outside_text.strip():
        ql = inside_text.lower()
        if prev == 'daadi' and ('daadi' in ql or "you're" in ql or "your" in ql): return 'maya'
        if prev == 'maya' and 'daadi' in ql: return 'maya'
    pronouns = {'she': ['maya', 'zara', 'daadi'], 'he': ['sam', 'leo']}
    for pron, cands in pronouns.items():
        if re.search(r'\b' + pron + r'\b', outside_text, re.I):
            return prev if prev in cands else cands[0]
    if re.search(r'\bit\b', outside_text, re.I): return 'blip'
    return prev

def is_gridlord_speaking(para):
    gl_cues = ['well, well', 'interesting', 'level one', 'solve this', 'locked', 'watching', "i'll be", 'made of', 'little cube']
    return sum(1 for cue in gl_cues if cue in para.lower()) >= 2 and para.startswith('"')

def fmt(text):
    text = esc(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = text.replace('\u2014', '&mdash;').replace(' \u2013 ', ' &ndash; ')
    text = re.sub(r'~([A-Z]):([^~]+(?:~~[^~]*)*)~',
        lambda m: f'<span class="gk {GERONIMO_CODES.get(m.group(1), "default")}">{m.group(2)}</span>', text)
    return text

def is_leo_tech(para):
    tech_cues = ['ghz', 'mhz', 'frequency', 'algorithm', 'protocol', 'bandwidth', 'omnidirectional', 'latency', 'firmware', 'hexadecimal', 'binary', 'encryption']
    return any(cue in para.lower() for cue in tech_cues) and len(para) < 300

def _is_sfx(text):
    s = text.strip().rstrip('.!-\u2014')
    su = s.upper()
    if su in SFX_WORDS or any(su.startswith(p) for p in SFX_PREFIXES):
        for prefix, style in SFX_STYLES.items():
            if su.startswith(prefix):
                return style
        return ''
    return None

def render_paragraph(para, is_glitch, prev_speaker):
    para = re.sub(r'~([A-Z]):~', '', para)
    parts, geronimo_speaker = [], None
    
    gk_tags = list(re.finditer(r'~([A-Z]):([^~]+)~', para))
    sfx_tags = []
    for m in gk_tags:
        code, text = m.group(1), m.group(2)
        style = _is_sfx(text)
        if style is not None:
            sfx_tags.append((m.start(), m.end(), text, style))
    
    gk_wrap = re.match(r'^~([A-Z]):([^~]+)~$', para.strip())
    if gk_wrap:
        code, wrapped = gk_wrap.group(1), gk_wrap.group(2)
        style = _is_sfx(wrapped)
        if style is not None:
            cls = f'sfx-burst {style}' if style else 'sfx-burst'
            return f'<div class="{cls}">{esc(wrapped)}</div>', prev_speaker
        geronimo_speaker = GERONIMO_CODES.get(code)
        if geronimo_speaker == 'sfx':
            return f'<div class="sfx-burst">{esc(wrapped)}</div>', prev_speaker
        para = wrapped
    
    if sfx_tags and not (gk_wrap and len(sfx_tags) == 1 and sfx_tags[0][0] == 0 and sfx_tags[0][1] == len(para.strip())):
        result = []
        last_end = 0
        for start, end, text, style in sfx_tags:
            before = para[last_end:start].strip()
            if before:
                result.append(f'<p>{fmt(before)}</p>')
            cls = f'sfx-burst {style}' if style else 'sfx-burst'
            result.append(f'<div class="{cls}">{esc(text)}</div>')
            last_end = end
        after = para[last_end:].strip()
        if after:
            result.append(f'<p>{fmt(after)}</p>')
        return '\n'.join(result), prev_speaker

    if para == "---":
        return f'<div class="text-divider">&mdash; {DIVIDER_ICONS.get("maya", "\u2726")} &mdash;</div>', prev_speaker

    if is_glitch:
        for kw in ['glitched', 'glitches', 'glitching', 'glitch']:
            para = re.sub(r'\b(' + kw + r')\b', r'GLITCH_KW:\1:END', para, flags=re.I)

    if is_gridlord_speaking(para):
        text = para.strip().strip('"')
        formatted = fmt(text).replace('GLITCH_KW:', '<span class="glitch-block">').replace(':END', '</span>')
        return f'<div class="gridlord-voice">{formatted}</div>', prev_speaker

    if para.startswith('"'):
        speaker = geronimo_speaker or detect_speaker(para, prev_speaker)
        if speaker:
            prev_speaker = speaker
            name = speaker.upper()
            cp_text, cp_char = is_catchphrase(para)
            formatted = fmt(para)
            if geronimo_speaker and geronimo_speaker != 'sfx':
                formatted = f'<span class="gk {geronimo_speaker}">{formatted}</span>'
            if speaker == 'blip':
                text = para.strip().strip('"')
                inner = fmt(text).replace('GLITCH_KW:', '<span class="glitch-block">').replace(':END', '</span>')
                if geronimo_speaker:
                    inner = f'<span class="gk blip">{inner}</span>'
                bf = blip_face_for(para)
                face_html = f' <span class="blip-inline-face">{bf}</span>' if bf else ''
                return f'<div class="dialogue dialogue-blip"><div class="dialogue-name blip">BLIP:</div><p class="blip-text">\u3010{inner}\u3011{face_html}</p></div>', prev_speaker
            elif cp_text:
                pattern = re.compile(re.escape(esc(cp_text)), re.I)
                formatted = pattern.sub(f'<span class="catchphrase {cp_char}">\\g<0></span>', formatted, count=1)
                return f'<div class="dialogue"><div class="dialogue-name {speaker}">{name}:</div><p>{formatted.replace("GLITCH_KW:", "<span class=\"glitch-block\">").replace(":END", "</span>")}</p></div>', prev_speaker
            else:
                return f'<div class="dialogue"><div class="dialogue-name {speaker}">{name}:</div><p>{formatted.replace("GLITCH_KW:", "<span class=\"glitch-block\">").replace(":END", "</span>")}</p></div>', prev_speaker

    if para.startswith('\u3010') or para.startswith('['):
        speaker = geronimo_speaker or 'blip'
        text = para.strip().strip('\u3010\u3011[]')
        inner = fmt(text).replace('GLITCH_KW:', '<span class="glitch-block">').replace(':END', '</span>')
        if geronimo_speaker and geronimo_speaker != 'sfx':
            inner = f'<span class="gk {geronimo_speaker}">{inner}</span>'
        bf = blip_face_for(para)
        face_html = f' <span class="blip-inline-face">{bf}</span>' if bf else ''
        return f'<div class="dialogue dialogue-blip"><div class="dialogue-name blip">BLIP:</div><p class="blip-text">\u3010{inner}\u3011{face_html}</p></div>', speaker

    # Secondary SFX detection (for unwrapped all-caps lines)
    stripped = para.strip()
    if stripped.isupper() and len(stripped) < 40:
        su = stripped.upper().replace('\u2014', '-').replace('&MDASH;', '-')
        style = None
        for prefix, s in SFX_STYLES.items():
            if su.startswith(prefix):
                style = s; break
        if style is None and any(w in su for w in SFX_WORDS):
            style = ''
        if style is not None:
            cls = f'sfx-burst {style}' if style else 'sfx-burst'
            return f'<div class="{cls}">{esc(stripped)}</div>', prev_speaker

    pq_text, pq_char = check_pull_quote(para)
    if pq_text: return f'<div class="pull-quote {pq_char}">{fmt(pq_text)}</div>', prev_speaker

    return f'<p>{fmt(para).replace("GLITCH_KW:", "<span class=\"glitch-block\">").replace(":END", "</span>")}</p>', prev_speaker


def render_scene_spotlight(item, compressed_dir):
    src = img_rel(item["file"], compressed_dir)
    quote = item.get("quote", "")
    if quote:
        formatted_q = fmt(quote)
        return (f'<div style="break-before:page;padding:0;margin:0;position:relative;width:5.5in;height:8.25in;overflow:hidden;">'
                f'<img src="{src}" alt="Illustration" style="width:5.5in;height:8.25in;object-fit:cover;display:block;">'
                f'<div style="position:absolute;bottom:0.5in;left:15%;right:15%;background:rgba(255,255,255,0.90);border-radius:10px;padding:0.25in 0.3in;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,0.15);"><p style="font-size:11pt;font-weight:700;margin:0;line-height:1.5;">{formatted_q}</p></div>'
                f'</div>')
    return f'<div style="break-before:page;padding:0;margin:0;"><img src="{src}" alt="" style="width:5.5in;height:8.25in;object-fit:cover;display:block;"></div>'

def render_location_page(item, compressed_dir):
    src = img_rel(item["file"], compressed_dir)
    return f'<div style="break-before:page;padding:0;margin:0;"><img src="{src}" alt="" style="width:5.5in;height:8.25in;object-fit:cover;display:block;"></div>'

def render_diagram_page(item, compressed_dir):
    src = img_rel(item["file"], compressed_dir)
    return f'<div class="blueprint-page"><img src="{src}" alt="" style="max-width:90%;max-height:6in;display:block;margin:0 auto;"></div>'

def distribute_images(images, num_paragraphs):
    typed = {'full-page': [], 'half-page': [], 'spot': [], 'scene_spotlight': [], 'location': [], 'diagram': [], 'glitch_art': [], 'document': [], 'map': [], 'other': []}
    for img in images:
        t = img.get('type', 'other')
        if t in typed: typed[t].append(img)
        elif t == 'extra_spot': typed['spot'].append(img)
        else: typed['other'].append(img)
    assignments = {}
    for fp in typed['full-page']:
        assignments['full-page'] = assignments.get('full-page', [])
        assignments['full-page'].append(fp)
    if typed['scene_spotlight']:
        sp = max(1, num_paragraphs // 3)
        for s in typed['scene_spotlight']:
            assignments[sp] = assignments.get(sp, [])
            assignments[sp].append(('scene_spotlight', s))
    if typed['location']:
        sp = max(1, num_paragraphs // 4)
        for s in typed['location']:
            assignments[sp] = assignments.get(sp, [])
            assignments[sp].append(('location', s))
    if typed['diagram']:
        sp = max(1, num_paragraphs // 3)
        for s in typed['diagram']:
            assignments[sp] = assignments.get(sp, [])
            assignments[sp].append(('diagram', s))
    if typed['glitch_art']:
        for ga in typed['glitch_art']:
            mp = num_paragraphs // 2
            assignments[mp] = assignments.get(mp, [])
            assignments[mp].append(('glitch_art', ga))
    if typed['document']:
        for d in typed['document']:
            dp = max(1, num_paragraphs // 3)
            assignments[dp] = assignments.get(dp, [])
            assignments[dp].append(('document', d))
    if typed['map']:
        for mp in typed['map']:
            mpp = max(1, num_paragraphs // 4)
            assignments[mpp] = assignments.get(mpp, [])
            assignments[mpp].append(('map', mp))
    if typed['half-page']:
        n = len(typed['half-page'])
        spacing = max(1, num_paragraphs // (n + 1))
        for idx, hp in enumerate(typed['half-page']):
            pos = min(spacing * (idx + 1), num_paragraphs - 1)
            assignments[pos] = assignments.get(pos, [])
            assignments[pos].append(('half-page', hp))
    if typed['spot']:
        for idx, sp in enumerate(typed['spot']):
            pos = min(3 + idx * 5, num_paragraphs - 1)
            if pos not in assignments: assignments[pos] = []
            assignments[pos].append(('spot', sp))
    return assignments

def render_chapter(manifest, ch, compressed_dir, output_dir):
    ch_num, ch_title, char = ch["num"], ch["title"], CHAPTER_CHARACTERS.get(ch["num"], "maya")
    html, ch_offset = [], ch_num * 7

    if ch_num in SECTION_DIVIDERS:
        title, subtitle, div_id = SECTION_DIVIDERS[ch_num]
        div = get_section_divider(manifest, div_id)
        if div:
            src = img_rel(div["file"], compressed_dir)
            html.append(f'''<div class="section-divider-page" style="background-image:url('{src}');">
<div class="divider-text"><div class="divider-title">{esc(title)}</div><div class="divider-subtitle">{esc(subtitle)}</div></div>
</div>''')

    teaser = ""
    fs = re.search(r'^(.+?[.!?])\s', ch["body"][:400])
    if fs:
        teaser_raw = esc(fs.group(1))
        teaser_raw = re.sub(
            r'~([A-Z]):([^~]+)~',
            lambda m: f'<span class="gk {GERONIMO_CODES.get(m.group(1), "maya")}">{m.group(2)}</span>',
            teaser_raw)
        teaser = f'\n    <p class="chapter-teaser">{teaser_raw}</p>'

    th = esc(ch_title)
    if len(th) > 28:
        ws = th.split(); mid = len(ws) // 2
        th = esc(" ".join(ws[:mid])) + "<br>" + esc(" ".join(ws[mid:]))

    html.append(f'''<div class="chapter-title-page chapter-{char}">
    <div class="chapter-dots"><span></span><span></span><span></span></div>
    <div class="chapter-number">Chapter {ch_num}</div>
    <h1 class="chapter-title">{th}</h1>
    <div class="chapter-divider"></div>{teaser}
    <div class="chapter-vignette"><img src="{img_rel(f'ChapterHeaders/ch{ch_num:02d}_vignette.png', compressed_dir)}" alt="" style="border-radius:0 60% 0 60%;"></div>
</div>''')

    all_images = get_chapter_images(manifest, ch_num)
    is_glitch = ch_num in GLITCH_CHAPTERS
    full_pages = [i for i in all_images if i.get("type") == "full-page"]
    other_images = [i for i in all_images if i.get("type") != "full-page"]

    for fp in full_pages:
        src = img_rel(fp["file"], compressed_dir)
        pq = PULL_QUOTES.get(ch_num, "")
        if pq:
            formatted_pq = fmt(pq)
            html.append((f'<div style="break-before:page;padding:0;margin:0;position:relative;width:5.5in;height:8.25in;overflow:hidden;">'
                         f'<img src="{src}" alt="Illustration" style="width:5.5in;height:8.25in;object-fit:cover;display:block;">'
                         f'<div style="position:absolute;bottom:0.5in;left:15%;right:15%;background:rgba(255,255,255,0.90);border-radius:10px;padding:0.25in 0.3in;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,0.15);"><p style="font-size:11pt;font-weight:700;margin:0;line-height:1.5;">{formatted_pq}</p></div>'
                         f'</div>'))
        else:
            html.append(f'<div style="break-before:page;padding:0;margin:0;"><img src="{src}" alt="" style="width:5.5in;height:8.25in;object-fit:cover;display:block;"></div>')

    paragraphs = [p.strip() for p in re.split(r'\n\n+', ch["body"]) if p.strip()]
    assignments = distribute_images(other_images, len(paragraphs))
    current_page, word_count, image_cost = [], 0, 0
    prev_speaker, page_num_in_chapter = None, 0

    def flush_page(force=False):
        nonlocal current_page, word_count, image_cost, page_num_in_chapter
        if not current_page: return
        if not force and word_count < 40 and image_cost == 0 and page_num_in_chapter > 0:
            return
        pc = 'glitch-page' if is_glitch else ''
        go = '<div class="scanlines"></div>' if is_glitch else ''
        bg = PAGE_BG.get(char, "#FFF8F0") if is_glitch or word_count >= 80 else "white"
        mi = (ch_num * 3 + page_num_in_chapter) % len(BLIP_MARGIN_EMOTIONS)
        bm = ''
        if page_num_in_chapter % 3 == 0:
            bm = f'<div class="blip-margin"><img src="{img_rel(BLIP_MARGIN_IMAGES[BLIP_MARGIN_EMOTIONS[mi]], compressed_dir)}" alt="Blip" style="width:45px;height:auto;"></div>'
        npt = ''
        if page_num_in_chapter % 4 == 3 and word_count >= 80:
            npt = '<div class="next-page-tease"><span class="gk blip">turn the page!</span></div>'
        html.append(f'<div class="page-break {pc}" style="background: {bg};">{go}' + "\n".join(current_page) + npt + bm + '</div>')
        current_page, word_count, image_cost = [], 0, 0
        page_num_in_chapter += 1

    for pi, para in enumerate(paragraphs):
        pw = len(para.split())
        para_visual_cost = 0
        if re.match(r'^~?[A-Z]:', para) or para.startswith('"') or '"\u3010' in para[:5]:
            para_visual_cost = 55
        elif any(kw in para.upper() for kw in ['SPROING', 'WHIRRR', 'CRASH', 'THUMP', 'BOOM', 'DRIP', 'ZZZZ']):
            para_visual_cost = 50
        elif re.search(r'~[A-Z]:[^~]+~', para):
            para_visual_cost = 40
        if len(para) > 300:
            para_visual_cost += 15
        pb = WORDS_PER_PAGE - image_cost
        if pb < 60: pb = 60
        min_words_before_flush = MIN_WORDS_FLUSH_IMAGE if image_cost > 0 else MIN_WORDS_FLUSH
        remaining_paras = len(paragraphs) - pi - 1
        remaining_words = sum(len(p.split()) for p in paragraphs[pi+1:])
        has_upcoming_special = any(
            it in ('scene_spotlight', 'location', 'diagram', 'document', 'map')
            for pj in range(pi+1, len(paragraphs))
            if pj in assignments
            for it, _ in assignments[pj]
        )
        if (remaining_paras <= 1 or remaining_words < 25) and not has_upcoming_special:
            min_words_before_flush = 9999

        if pi in assignments:
            for it, idata in assignments[pi]:
                if it == 'spot-row':
                    para_visual_cost += SPOT_COST * len(idata)
                elif it == 'half-page':
                    para_visual_cost += HALF_PAGE_COST
                elif it == 'spot':
                    para_visual_cost += SPOT_COST

        if word_count + pw + para_visual_cost > pb and current_page and word_count >= min_words_before_flush:
            flush_page()

        if pi in assignments:
            for it, idata in assignments[pi]:
                if it == 'spot-row':
                    spots_html = []
                    for i, sp in enumerate(idata):
                        shape = SPOT_SHAPES[(ch_offset + i) % len(SPOT_SHAPES)]
                        sps = img_rel(sp["file"], compressed_dir)
                        spots_html.append(f'<div class="spot {shape}"><img src="{sps}" alt="" style="width:100%;display:block;"></div>')
                    current_page.append('<div class="spot-cluster">' + ''.join(spots_html) + '</div>')
                    image_cost += SPOT_COST * len(idata)
                elif it == 'scene_spotlight':
                    flush_page()
                    html.append(render_scene_spotlight(idata, compressed_dir))
                    page_num_in_chapter += 1
                elif it == 'location':
                    flush_page()
                    html.append(render_location_page(idata, compressed_dir))
                    page_num_in_chapter += 1
                elif it == 'diagram':
                    flush_page()
                    html.append(render_diagram_page(idata, compressed_dir))
                    page_num_in_chapter += 1
                elif it == 'half-page':
                    src = img_rel(idata["file"], compressed_dir)
                    frame = FRAME_FOR_CHAR.get(char, "frame-blip")
                    side = 'align-right' if pi % 2 == 0 else 'align-left'
                    current_page.append(f'<div class="illustration-half {side}"><div class="{frame}"><img src="{src}" alt=""></div></div>')
                    image_cost += HALF_PAGE_COST
                elif it == 'spot':
                    src = img_rel(idata["file"], compressed_dir)
                    side = 'ill-float-right' if pi % 2 == 0 else 'ill-float-left'
                    frame = SPOT_FRAMES[(ch_offset + pi) % len(SPOT_FRAMES)]
                    current_page.append(f'<div class="{side}"><div class="{frame}"><img src="{src}" alt=""></div></div>')
                    image_cost += SPOT_COST
                elif it == 'glitch_art':
                    src = img_rel(idata["file"], compressed_dir)
                    html.append(f'<div class="glitch-art-page"><img src="{src}" alt=""></div>')
                    page_num_in_chapter += 1
                elif it == 'document':
                    flush_page()
                    src = img_rel(idata["file"], compressed_dir)
                    html.append(f'<div class="doc-page"><img src="{src}" alt=""></div>')
                    page_num_in_chapter += 1
                elif it == 'map':
                    flush_page()
                    src = img_rel(idata["file"], compressed_dir)
                    html.append(f'<div class="map-page you-are-here"><img src="{src}" alt=""></div>')
                    page_num_in_chapter += 1

        ph, prev_speaker = render_paragraph(para, is_glitch, prev_speaker)
        current_page.append(ph)
        word_count += pw
        if 'class="dialogue' in ph:
            word_count += 55
        elif 'class="sfx-burst' in ph:
            word_count += 50
        elif 'class="pull-quote' in ph or 'class="gridlord-voice' in ph:
            word_count += 40
        elif 'class="text-divider' in ph:
            word_count += 20
        if 'class="blip-corner' in ph or 'class="find-object' in ph:
            word_count += 15

        bf = blip_face_for(para)
        if bf and not para.startswith('"') and not para.startswith('\u3010'):
            color = BLIP_FACE_COLORS.get(bf, 'var(--color-blip)')
            current_page.append(f'<div class="blip-context-face" style="color: {color};">{bf}</div>')
            word_count += 5

    # Add interactive elements to the last page before flushing
    if ch_num in BLIP_INTERACTIVE_QUESTIONS:
        bq = BLIP_INTERACTIVE_QUESTIONS[ch_num]
        blip_img = img_rel("Marginalia/blip_thinking.png", compressed_dir)
        current_page.append(f'<div class="blip-corner"><div class="blip-emoji"><img src="{blip_img}" alt="Blip"></div><p>{esc(bq)}</p></div>')
        word_count += 15

    if ch_num in FIND_OBJECTS:
        challenge, blip_img_name = FIND_OBJECTS[ch_num]
        blip_img = img_rel(blip_img_name, compressed_dir)
        current_page.append(f'<div class="find-object"><span class="find-icon">\U0001F50D</span><p>{esc(challenge)}</p></div>')
        word_count += 15

    # If current page is too sparse, merge with previous page
    if current_page and word_count < MIN_WORDS_MERGE and len(html) > 0:
        prev = html[-1]
        closing = prev.rfind('</div>')
        if closing > 0:
            html[-1] = prev[:closing] + "\n".join(current_page) + '</div>'
            current_page, word_count, image_cost = [], 0, 0
        else:
            current_page, word_count, image_cost = [], 0, 0

    flush_page(force=True)

    html = merge_sparse_pages(html)

    return "\n".join(html)

def merge_sparse_pages(pages):
    merged = []
    for idx, page in enumerate(pages):
        text = re.sub(r'<[^>]+>', '', page).strip()
        words = len(text.split())
        is_content_page = 'page-break ' in page or 'page-break"' in page
        is_special_page = any(cls in page for cls in [
            'chapter-title-page', 'section-divider-page', 'glitch-art-page',
            'doc-page', 'map-page', 'blueprint-page', 'quote-box',
            'object-fit:cover', 'char-card-page', 'endpaper-page',
            'char-squad-title',
        ])
        prev_is_special = merged and any(cls in merged[-1] for cls in [
            'chapter-title-page', 'section-divider-page', 'glitch-art-page',
            'doc-page', 'map-page', 'blueprint-page', 'quote-box',
            'object-fit:cover', 'char-card-page', 'endpaper-page',
            'char-squad-title',
        ])
        if is_content_page and not is_special_page and not prev_is_special and words < 80:
            inner_clean = re.sub(r'<div class="blip-margin">.*?</div>', '', page, flags=re.DOTALL)
            inner_clean = re.sub(r'<div class="scanlines"></div>', '', inner_clean)
            inner_clean = re.sub(r'<div class="next-page-tease">.*?</div>', '', inner_clean, flags=re.DOTALL)
            inner_text = re.sub(r'<[^>]+>', '', inner_clean).strip()
            has_images = '<img ' in inner_clean
            if len(inner_text.split()) < 15 and merged:
                prev = merged[-1]
                closing = prev.rfind('</div>')
                if closing > 0 and has_images:
                    img_start = inner_clean.find('>', inner_clean.find('page-break')) + 1
                    img_content = inner_clean[img_start:].strip()
                    img_content = re.sub(r'<div class="blip-margin">.*?</div>', '', img_content, flags=re.DOTALL).strip()
                    img_content = re.sub(r'<div class="scanlines"></div>', '', img_content)
                    if img_content and img_content != '</div>':
                        merged[-1] = prev[:closing] + img_content + '</div>'
                continue
            elif len(inner_text.split()) < 15:
                if merged:
                    continue
            elif merged:
                prev = merged[-1]
                closing = prev.rfind('</div>')
                if closing > 0:
                    inner = page[page.find('>', page.find('page-break')) + 1:]
                    inner = re.sub(r'<div class="blip-margin">.*?</div>', '', inner, flags=re.DOTALL).strip()
                    inner = re.sub(r'<div class="scanlines"></div>', '', inner)
                    if inner and inner != '</div>':
                        merged[-1] = prev[:closing] + inner + '</div>'
                    continue
            elif len(inner_text.split()) < 15:
                if merged:
                    continue
            elif merged:
                prev = merged[-1]
                closing = prev.rfind('</div>')
                if closing > 0:
                    inner = page[page.find('>', page.find('page-break')) + 1:]
                    inner = re.sub(r'<div class="blip-margin">.*?</div>', '', inner, flags=re.DOTALL).strip()
                    inner = re.sub(r'<div class="scanlines"></div>', '', inner)
                    if inner and inner != '</div>':
                        merged[-1] = prev[:closing] + inner + '</div>'
                    continue
        merged.append(page)
    return merged

def build_book(manifest, chapters, book_title, compressed_dir, output_dir):
    css_file = CSS_DIR / "book-print.css"
    shutil.copy2(css_file, output_dir / "book-print.css")
    fonts_out = output_dir / "fonts"
    fonts_out.mkdir(parents=True, exist_ok=True)
    if FONTS_DIR.exists():
        for ff in FONTS_DIR.iterdir():
            if ff.is_file(): shutil.copy2(ff, fonts_out / ff.name)

    parts = [f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>The Glitch Squad &mdash; {esc(book_title)}</title>
<link rel="stylesheet" href="book-print.css"></head><body>''']

    tp = manifest.get("title_page")
    if tp:
        src = img_rel(tp.get("file", "title_page.png"), compressed_dir)
        parts.append(f'<div class="endpaper-page"><img src="{src}" alt="Title Page"></div>')

    for ch in chapters: parts.append(render_chapter(manifest, ch, compressed_dir, output_dir))

    char_cards = manifest.get("character_cards", [])
    if char_cards:
        parts.append('<div class="char-squad-title"><div class="char-squad-title-inner"><h2>Meet the Squad</h2><p>Turn the page to meet everyone!</p></div></div>')
        for card in char_cards:
            src = img_rel(card["file"], compressed_dir)
            name = card.get("prompt", "").split("name", 1)[-1].split("at top", 1)[0].strip().rstrip(",").strip() if "name" in card.get("prompt", "") else "???"
            role = card.get("prompt", "").split("subtitle", 1)[-1].split(",")[0].strip() if "subtitle" in card.get("prompt", "") else ""
            parts.append(f'<div class="char-card-page" style="background-image:url(\'{src}\');"><div class="char-card-banner-top"><div class="char-name">{esc(name)}</div></div><div class="char-card-banner-bottom"><div class="char-role">{esc(role)}</div></div></div>')

    blueprints = manifest.get("gadget_blueprints", [])
    if blueprints:
        parts.append('<div class="page-break" style="padding-top:0.3in;text-align:center;">')
        parts.append('<p style="font-size:14pt;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:var(--color-leo);">Gadget Blueprints</p>')
        for bp in blueprints:
            src = img_rel(bp["file"], compressed_dir)
            parts.append(f'<div class="blueprint-page"><img src="{src}" alt="Blueprint"></div>')
        parts.append('</div>')

    back_matter = [i for i in manifest.get("illustrations", []) if i.get("type") == "back-matter"]
    for bm in back_matter:
        src = img_rel(bm["file"], compressed_dir)
        parts.append(f'<div class="page-break full-bleed-page"><img src="{src}" alt="" style="max-width:100%;max-height:8.25in;object-fit:contain;display:block;"></div>')

    for ep in manifest.get("endpapers", []):
        src = img_rel(ep["file"], compressed_dir)
        parts.append(f'<div class="endpaper-page"><img src="{src}" alt="Endpaper" style="width:5.5in;height:8.25in;object-fit:cover;display:block;"></div>')

    parts.append("</body></html>")
    return "\n".join(parts)

def generate_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    print(f"Generating PDF with Playwright: {pdf_path}")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(1000)
        page.pdf(
            path=str(pdf_path),
            width="5.5in",
            height="8.25in",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()
    print(f"PDF saved: {pdf_path} ({pdf_path.stat().st_size / 1024 / 1024:.1f} MB)")

def main():
    parser = argparse.ArgumentParser(description="Build Glitch Squad book")
    parser.add_argument("--book", type=int, default=1)
    parser.add_argument("--pdf", action="store_true")
    parser.add_argument("--chapters", nargs="+", type=int)
    args = parser.parse_args()

    book_dir = SERIES_DIR / f"Book{args.book}"
    output_dir = book_dir / "Output"
    output_dir.mkdir(parents=True, exist_ok=True)

    mp, msp = None, None
    for c in ["manifest_clean.json", "manifest.json"]:
        if (book_dir / c).exists(): mp = book_dir / c; break
    for c in ["Manuscript_v3.md", "Manuscript_v2.md", "Manuscript.md"]:
        if (book_dir / c).exists(): msp = book_dir / c; break
    if not mp or not msp: print(f"ERROR: Missing files in {book_dir}"); return

    title = BOOK_TITLES.get(args.book, f"Book {args.book}")
    safe, comp_dir = title.replace(" ", "_"), output_dir / "images"
    comp_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(mp)
    chapters = parse_manuscript(msp, args.chapters)
    print(f"Book {args.book}: {title}")
    print(f"  {len(chapters)} chapters, {len(manifest.get('illustrations', []))} illustrations")

    html = build_book(manifest, chapters, title, comp_dir, output_dir)
    html_path = output_dir / f"{safe}.html"
    with open(html_path, "w", encoding="utf-8") as f: f.write(html)
    print(f"  HTML: {html_path.name} ({html_path.stat().st_size / 1024:.0f} KB)")

    if args.pdf: generate_pdf(html_path, output_dir / f"{safe}.pdf")

if __name__ == "__main__": main()

import re

html_path = r"d:\Kapil\Books\First\Book_v1.html"
with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

replacements = [
    (r'<div style="font-size:48px; margin-bottom: 16px;">\?\?</div>\s*<div style="font-family: \'Playfair Display\', serif; font-size: 22px; color: #C9913D;">GPS',
     r'<div style="font-size:48px; margin-bottom: 16px;">🗺️ 📺 📧</div>\n        <div style="font-family: \'Playfair Display\', serif; font-size: 22px; color: #C9913D;">GPS'),
    
    (r'<div style="font-size:52px; margin-bottom: 16px;">\?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Chapter Three',
     r'<div style="font-size:52px; margin-bottom: 16px;">🎓</div>\n      <div class="text-block">\n        <div class="chapter-label">Chapter Three'),

    (r'<div style="font-size:52px; margin-bottom: 16px;">\?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Chapter Four',
     r'<div style="font-size:52px; margin-bottom: 16px;">🤖</div>\n      <div class="text-block">\n        <div class="chapter-label">Chapter Four'),

    (r'<div style="font-size:40px; margin-bottom:20px; letter-spacing:8px;">\?\? \?\? \?\?</div>',
     r'<div style="font-size:40px; margin-bottom:20px; letter-spacing:8px;">📱 💻 ⌚</div>'),

    (r'<div class="box-title">\?\? Tip</div>',
     r'<div class="box-title">💡 Tip</div>'),

    (r'<div style="font-size:64px; margin-bottom:20px;">\?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Chapter Seven',
     r'<div style="font-size:64px; margin-bottom:20px;">🗣️</div>\n      <div class="text-block">\n        <div class="chapter-label">Chapter Seven'),

    (r'<div style="font-size:52px; margin-bottom:20px;">\?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Chapter Eight',
     r'<div style="font-size:52px; margin-bottom:20px;">❓</div>\n      <div class="text-block">\n        <div class="chapter-label">Chapter Eight'),

    (r'<div class="box-title">\?\? Music', r'<div class="box-title">🎵 Music'),
    (r'<div class="box-title">\?\? Video', r'<div class="box-title">🎬 Video'),
    
    (r'<div style="font-size:48px; margin-bottom:18px; letter-spacing:6px;">\?\? \?\? \?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Chapter Nine',
     r'<div style="font-size:48px; margin-bottom:18px; letter-spacing:6px;">🎵 📸 🎥</div>\n      <div class="text-block">\n        <div class="chapter-label">Chapter Nine'),

    (r'<div class="box-title">\?\? Medical Jargon', r'<div class="box-title">🩺 Medical Jargon'),
    (r'<div class="box-title">\?\? Real-Time Translation', r'<div class="box-title">🌍 Real-Time Translation'),
    (r'<div class="box-title">\?\? Fitness', r'<div class="box-title">🥗 Fitness'),

    (r'<div style="font-size:48px; margin-bottom:18px; letter-spacing:6px;">\?\? \?\? \?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Chapter Ten',
     r'<div style="font-size:48px; margin-bottom:18px; letter-spacing:6px;">🩺 🌍 🥗</div>\n      <div class="text-block">\n        <div class="chapter-label">Chapter Ten'),

    (r'<div class="box-title">\?\? The Master Gardener', r'<div class="box-title">🪴 The Master Gardener'),
    (r'<div class="box-title">\?\? The Family Historian', r'<div class="box-title">🕰️ The Family Historian'),
    (r'<div class="box-title">\?\? The Handyman', r'<div class="box-title">🛠️ The Handyman'),
    (r'<div class="box-title">\?\? The Golden Rule: Trust, But Verify', r'<div class="box-title">🛑 The Golden Rule: Trust, But Verify'),

    (r'<div style="font-size:52px; margin-bottom:18px;">\?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Chapter Twelve',
     r'<div style="font-size:52px; margin-bottom:18px;">🛑</div>\n      <div class="text-block">\n        <div class="chapter-label">Chapter Twelve'),

    (r'<div class="box-title">\?\? Red Flag 1', r'<div class="box-title">🚩 Red Flag 1'),
    (r'<div class="box-title">\?\? Red Flag 2', r'<div class="box-title">🚩 Red Flag 2'),
    (r'<div class="box-title">\?\? Red Flag 3', r'<div class="box-title">🚩 Red Flag 3'),

    (r'<div style="font-size:52px; margin-bottom:18px;">\?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Chapter Thirteen',
     r'<div style="font-size:52px; margin-bottom:18px;">🎭</div>\n      <div class="text-block">\n        <div class="chapter-label">Chapter Thirteen'),

    (r'<div class="box-title">\?\? The "Grandma', r'<div class="box-title">📞 The "Grandma'),

    (r'<div style="font-size:52px; margin-bottom:18px;">\?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Chapter Fourteen',
     r'<div style="font-size:52px; margin-bottom:18px;">🎙️</div>\n      <div class="text-block">\n        <div class="chapter-label">Chapter Fourteen'),

    (r'<div class="box-title">\?\? Rule 1:', r'<div class="box-title">🗝️ Rule 1:'),
    (r'<div class="box-title">\?\? Rule 2:', r'<div class="box-title">☎️ Rule 2:'),
    (r'<div class="box-title">\?\? Rule 3:', r'<div class="box-title">⏱️ Rule 3:'),
    (r'<div class="box-title">\?\? Rule 4:', r'<div class="box-title">🚫 Rule 4:'),

    (r'<div style="font-size:48px; margin-bottom:18px; letter-spacing:6px;">\?\? \?\? \?\? \?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Chapter Fifteen',
     r'<div style="font-size:48px; margin-bottom:18px; letter-spacing:6px;">🛡️ ☎️ 🛑 🗝️</div>\n      <div class="text-block">\n        <div class="chapter-label">Chapter Fifteen'),

    (r'<div class="box-title">\?\? The Golden Rule of AI Privacy', r'<div class="box-title">🔒 The Golden Rule of AI Privacy'),

    (r'<div style="font-size:52px; margin-bottom:18px;">\?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Chapter Sixteen',
     r'<div style="font-size:52px; margin-bottom:18px;">🔒</div>\n      <div class="text-block">\n        <div class="chapter-label">Chapter Sixteen'),

    (r'<div style="font-size:52px; margin-bottom:18px;">\?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Conclusion',
     r'<div style="font-size:52px; margin-bottom:18px;">📖</div>\n      <div class="text-block">\n        <div class="chapter-label">Conclusion'),

    (r'<div style="font-size:52px; margin-bottom:18px;">\?\?</div>\s*<div class="text-block">\s*<div class="chapter-label">Reference',
     r'<div style="font-size:52px; margin-bottom:18px;">📚</div>\n      <div class="text-block">\n        <div class="chapter-label">Reference'),
]

for old, new in replacements:
    text = re.sub(old, new, text)

# Also fix smart quotes and em-dashes that were corrupted to ?
text = text.replace(" don?t ", " don't ")
text = text.replace(" AI?s ", " AI's ")
text = text.replace(" ? ", " — ")
text = text.replace("?that's", "—that's")
text = text.replace("re?s ", "re's ")
text = text.replace("you?re", "you're")
text = text.replace("you?ve", "you've")
text = text.replace("didn?t", "didn't")
text = text.replace("can?t", "can't")
text = text.replace("It?s", "It's")
text = text.replace("it?s", "it's")
text = text.replace("Let?s", "Let's")
text = text.replace("You?ll", "You'll")
text = text.replace("you?ll", "you'll")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Icons restored!")

html_path = r"d:\Kapil\Books\First\Book_v1.html"
with open(html_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

def replace_icon(idx, icon):
    if "??" in lines[idx]:
        lines[idx] = lines[idx].replace("??", icon)

# Let's target the exact line numbers output by Select-String
replace_icon(703, "🎓") # line 704
replace_icon(741, "🤖")
replace_icon(829, "🗣️")
replace_icon(870, "❓")
replace_icon(908, "🎵 📸 🎥")
replace_icon(947, "🩺 🌍 🥗")
replace_icon(1018, "🛑")
replace_icon(1060, "🎭")
replace_icon(1094, "🎙️")
replace_icon(1136, "🛡️ ☎️ 🛑 🗝️") # Line 1137
replace_icon(1175, "🔒")
replace_icon(1256, "📖")
replace_icon(1296, "📚")

with open(html_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Remaining emojis restored!")

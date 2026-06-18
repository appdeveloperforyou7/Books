import re

html_path = r"d:\Kapil\Books\First\Book_v1.html"
with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# Fix Page 21 Question Mark
text = text.replace('<div style="font-size:52px; margin-bottom:20px;">❓</div>', '<div style="font-size:52px; margin-bottom:20px;"></div>')

# Fix Chapter 4 "Meet the AI Agents" (Page 11) to be text-over-image like Page 2-3
# Strategy: Replace the entire PAGE 11 / PAGE 12 block with a unified style-b-photo + gradient overlay.

ch4_pattern = re.compile(
    r'(<!-- ======= PAGE 11: CH4 TEXT ======= -->\n.*?)(<!-- ======= PAGE 12: CH4 PLACEHOLDER ======= -->\n.*?</div>\n    </div>)',
    re.DOTALL
)

ch4_replacement = """<!-- ======= PAGE 11: CH4 TEXT & BACKGROUND ======= -->
    <div class="page style-b-photo" style="background-image: url('data:image/png;base64,{ch4_b64_placeholder}');">
      <div style="background: linear-gradient(to top, rgba(15, 25, 45, 0.95) 0%, rgba(15, 25, 45, 0.8) 60%, transparent 100%); width: 100%; height: 100%; display:flex; flex-direction:column; justify-content:flex-end; padding:110px 85px; box-sizing: border-box;">
        <div class="text-block" style="color: #ffffff;">
          <div class="chapter-label" style="color: var(--gold);">Chapter Four</div>
          <div class="chapter-title" style="color: #ffffff;">Meet the AI &ldquo;Agents&rdquo;</div>
          <div class="rule" style="background: var(--gold);"></div>
          <p>A regular search engine is like a phone book - it tells you <span class="italic-word">where</span> to find
            information, but you have to do the calling, talking, and booking yourself.</p>
          <p>An <span class="bold-word">AI Agent</span> is like a top-tier hotel concierge. You don't just ask Agent <span
              class="italic-word">how</span> to do things - you ask an Agent to <span class="bold-word">do it for
              you.</span></p>
          <p>Instead of searching "how to book a flight to Florida," you could tell an AI Agent: <span
              class="italic-word">"Find me the cheapest morning flight to Florida next Tuesday and book the aisle
              seat."</span> The Agent researches, compares, fills forms, and presents you with the ticket.</p>
          <p>AI Agents handle multi-step tasks - summarizing 100-page documents, checking your calendar, automatically
            sending invitations. They are transforming computers from passive libraries into <span
              class="bold-word">active, helpful partners.</span></p>
        </div>
        <span class="page-number right" style="color: #ffffff;">11</span>
      </div>
    </div><!-- ======= PAGE 12 REMOVED (MERGED INTO 11) ======= -->"""

text = re.sub(ch4_pattern, ch4_replacement, text)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Page 11 and 21 fixed!")

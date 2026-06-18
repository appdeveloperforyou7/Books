import re

html_path = r"d:\Kapil\Books\First\Book_v1.html"
with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

ch4_merged = """<!-- ======= PAGE 11: CH4 TEXT & BACKGROUND ======= -->
    <div class="page style-a" style="background-image: url('data:image/png;base64,{CH4_BASE64}');">
      <div class="text-block">
        <div class="chapter-label">Chapter Four</div>
        <div class="chapter-title">Meet the AI &ldquo;Agents&rdquo;</div>
        <div class="rule"></div>
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
      <span class="page-number right">11</span>
    </div>

    <!-- ======= PAGE 13:"""

# Regex replacing everything between PAGE 11: CH4 and PAGE 13:
text = re.sub(r'<!-- ======= PAGE 11: CH4(.*?)<!-- ======= PAGE 13:', ch4_merged, text, flags=re.DOTALL)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

print("regex sub complete")

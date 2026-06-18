import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'D:\Kapil\Books\TD-1\Book1\Output\THE_LOST_SIGNAL.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find "But something else caught her eye" in the HTML
idx = content.find('But something else caught her eye')
if idx > 0:
    # Get surrounding context
    start = max(0, idx - 500)
    end = min(len(content), idx + 500)
    print("=== Context around 'But something else caught her eye' ===")
    print(content[start:end])

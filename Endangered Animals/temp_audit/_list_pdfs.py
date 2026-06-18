import os

out = 'Output'
files = sorted(f for f in os.listdir(out) if f.endswith('.pdf'))

print("=" * 75)
print(f"{'PDF File':50s} {'Size':>8s}  Status")
print("=" * 75)

for f in files:
    path = os.path.join(out, f)
    size_mb = os.path.getsize(path) / (1024 * 1024)
    if size_mb > 50:
        status = "READY"
    elif size_mb > 0.5:
        status = "READY"
    else:
        status = "INCOMPLETE"
    print(f"{f:50s} {size_mb:7.1f} MB  {status}")

print()
print("READY for publishing:")
print("-" * 75)
for f in sorted(files):
    path = os.path.join(out, f)
    size_mb = os.path.getsize(path) / (1024 * 1024)
    if size_mb > 0.5:
        if 'Hardcover' in f or 'hardcover' in f:
            fmt = "HARDCOVER"
        elif 'Cover' in f and 'Hardcover' in f:
            fmt = "HARDCOVER COVER"
        elif 'Cover' in f:
            fmt = "PAPERBACK COVER"
        else:
            fmt = "PAPERBACK"
        print(f"  [{fmt:15s}] {f}")

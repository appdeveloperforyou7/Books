import os
for f in os.listdir('Output'):
    path = os.path.join('Output', f)
    size = os.path.getsize(path)
    unit = 'MB' if size > 1000000 else 'KB'
    val = size // 1024 // 1024 if size > 1000000 else size // 1024
    print(f'{f}: {val}{unit}')

"""Try image generation via Z.AI API."""
from openai import OpenAI
import base64, os

ASSETS = r"D:\Kapil\Books\First\Assets"

client = OpenAI(
    api_key='f45f1d12fa5b487b81d987d8bb54b10e.44lOxbQvxUDwLHW1',
    base_url='https://api.z.ai/api/coding/paas/v4'
)

models_to_try = [
    'cogview-3', 'cogview-3-flash', 'cogview-4',
    'cogview-3-plus', 'cogview', 'cogvideo',
]

for model in models_to_try:
    try:
        print(f"Trying {model}...")
        resp = client.images.generate(
            model=model,
            prompt='A warm, golden sunset over a peaceful garden, photorealistic, cinematic lighting',
            n=1,
            size='1024x1024'
        )
        print(f"  {model}: SUCCESS!")
        if resp.data and resp.data[0].url:
            print(f"  URL: {resp.data[0].url[:80]}...")
        elif resp.data and resp.data[0].b64_json:
            data = base64.b64decode(resp.data[0].b64_json)
            path = os.path.join(ASSETS, f"test_{model}.png")
            with open(path, 'wb') as f:
                f.write(data)
            print(f"  Saved: {path} ({len(data)} bytes)")
        break
    except Exception as e:
        err = str(e)
        if '1211' in err or 'Unknown Model' in err:
            print(f"  {model}: model not found")
        elif '401' in err or 'auth' in err.lower():
            print(f"  {model}: auth error")
        else:
            print(f"  {model}: {err[:120]}")

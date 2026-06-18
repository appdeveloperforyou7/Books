from gradio_client import Client
import sys, os, base64

client = Client("akhaliq/Bonsai-Image-Demo")

prompt = sys.argv[1] if len(sys.argv) > 1 else "A bonsai tree in a quiet ceramic studio, soft morning light, detailed, 8k"

print(f"Generating: {prompt}")
print("Sending to Bonsai Image (cloud)... This may take 30-60s.")

result = client.predict(
    prompt=prompt,
    seed=0,
    steps=4,
    guidance=1.0,
    backend="bonsai-ternary-gemlite",
    height=1024,
    width=1024,
    max_sequence_length=256,
    api_name="/generate"
)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bonsai_output.png")

if isinstance(result, dict) and "image_b64" in result:
    img_data = base64.b64decode(result["image_b64"])
    with open(output_path, "wb") as f:
        f.write(img_data)
    print(f"Saved to: {output_path}")
elif isinstance(result, str) and os.path.exists(result):
    import shutil
    shutil.copy2(result, output_path)
    print(f"Saved to: {output_path}")
else:
    print(f"Unexpected result type: {type(result)}")

import io
import base64
import os
from PIL import Image
import requests

def get_encoded_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read())
            return 'data:image/png;base64,' + str(encoded, encoding='utf-8')
    else:
        return None

def send_prompt_to_stable_diffusion(prompt, steps=5):
    snapshot_path = r"C:\tmp\snapshot.png"
    EncodedImage = get_encoded_image(snapshot_path)

    if EncodedImage is None:
        print("Snapshot image not found.")
        return  # Or handle the absence of the image as needed

    url = "http://127.0.0.1:7860"
    payload = {
        "init_images": [EncodedImage],
        "prompt": prompt,
        "steps": steps
    }

    response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    r = response.json()

    output_dir = "C:\\tmp"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "output.png")

    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    image.save(output_path)

    return output_path
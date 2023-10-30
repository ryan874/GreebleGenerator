import requests
import io
import base64
from PIL import Image

def send_prompt_to_stable_diffusion(prompt, steps=5):
    url = "http://127.0.0.1:7860"
    payload = {
        "prompt": prompt,
        "steps": steps
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()

    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    image.save('output.png')

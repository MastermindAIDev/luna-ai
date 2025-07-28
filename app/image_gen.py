import os
import json
import base64
import uuid
import requests

GENERATED_DIR = "generated"
PROMPT_DIR = "prompts"


def load_prompt_config(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_luna_image(config_name):
    try:
        config_path = os.path.join(PROMPT_DIR, f"{config_name}.json")
        payload = load_prompt_config(config_path)

        response = requests.post(
            "http://127.0.0.1:7860/sdapi/v1/txt2img",
            json=payload
        )
        result = response.json()
        image_data = result["images"][0]
        image_bytes = base64.b64decode(image_data)

        os.makedirs(GENERATED_DIR, exist_ok=True)
        filename = os.path.join(GENERATED_DIR, f"luna_{uuid.uuid4().hex}.png")
        with open(filename, "wb") as f:
            f.write(image_bytes)

        print("✅ Luna image saved at:", filename)
        return None

    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return None


def get_all_generated_images():
    if not os.path.exists(GENERATED_DIR):
        os.makedirs(GENERATED_DIR)
    files = sorted(
        [os.path.join(GENERATED_DIR, f) for f in os.listdir(GENERATED_DIR)
         if f.lower().endswith((".png", ".jpg", ".jpeg"))],
        key=os.path.getmtime,
        reverse=True
    )
    return files
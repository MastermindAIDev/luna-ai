import os
import json
import base64
import uuid
import requests

GENERATED_DIR = "generated"
PROMPT_DIR = "prompts"

# Automatically applied tags
BASE_TAGS = [
    "earrings", "black hair", "blunt bangs", "blue eyes", "medium hair",
    "anime woman", "anime screencap", "anime style", "choker"
]

NEGATIVE_TAGS = [
    "nsfw", "poorly drawn", "bad anatomy"
]


def load_prompt_config(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_luna_image(config_or_prompt, custom_prompt=None):
    try:
        if custom_prompt and custom_prompt.strip():
            # User typed a prompt manually
            user_prompt = custom_prompt.strip()
            full_prompt = ", ".join(BASE_TAGS + [user_prompt])
            full_negative = ", ".join(NEGATIVE_TAGS)

            payload = {
                "prompt": full_prompt,
                "negative_prompt": full_negative,
                "steps": 25,
                "sampler_name": "Default",
                "cfg_scale": 7.0,
                "width": 720,
                "height": 1280,
                "seed": -1,
                "enable_hr": False,
                "override_settings": {
                    "sd_model_checkpoint": "hsUltrahdCG_IllEpic.safetensors [860f6430d8]",
                    "CLIP_stop_at_last_layers": 2,
                    "sd_vae": "Automatic"
                }
            }

        else:
            # Load saved config file
            config_path = os.path.join(PROMPT_DIR, f"{config_or_prompt}.json")
            payload = load_prompt_config(config_path)

            base_prompt = payload.get("prompt", "")
            full_prompt = ", ".join(BASE_TAGS + [base_prompt.strip()])
            full_negative = ", ".join(
                set(NEGATIVE_TAGS + payload.get("negative_prompt", "").split(","))
            )

            payload["prompt"] = full_prompt
            payload["negative_prompt"] = full_negative

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

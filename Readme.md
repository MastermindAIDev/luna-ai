# 💖 Luna – AI Companion App

**Current Version: 0.8.9**

Luna is a playful, memory-aware AI companion powered by local large language models (LLMs), expressive TTS (Text-to-Speech), STT (Speech-to-Text), Stable Diffusion image generation, AnimateDiff-based video generation via ComfyUI, and now a 3D animated avatar viewer with camera controls.

This project is designed as a modular, professional-grade demo that integrates:
- Conversational memory and persona
- Realistic voice synthesis (Jenny TTS)
- Audio input via Speech-to-Text transcription
- Dynamic image & video generation (Stable Diffusion WebUI / ComfyUI)
- Playful UI with animated reactions and affection scoring
- Live 3D avatar display with animations and custom backgrounds

---

## ✨ Features

- 🧠 **Memory-Aware Chat** – Uses long-term memory to personalize conversations.
- 💖 **Affection System** – Luna's affection grows with your interactions and decays over time. Visualized with dynamic heart icons.
- 🔊 **Voice Responses** – Converts Luna's replies into expressive speech.
- 🎙️ **Speech-to-Text Input** – Speak naturally and let Luna transcribe and respond in real time.
- 🎨 **Scene Generation** – Create custom AI images via Stable Diffusion WebUI.
- 🎥 **Video Generation** – Create smooth animated AI scenes using AnimateDiff in ComfyUI.
- 💬 **Interaction Buttons** – Adds emotional reactions via sound effects.
- 📸 **Media Galleries** – Browse Luna’s generated images and videos.
- 👩‍💻 3D Avatar Display (NEW) – Real-time rendering of Luna’s animated avatar using GLB models, with smooth camera control, reset button, and themed gradient backgrounds.

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/MastermindAIDev/luna-ai.git
cd luna-ai
```

### 2. Set up virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Run the app
```bash
python run.py
```
Open your browser to [http://localhost:8080](http://localhost:8080)

> ⚠️ Requires `ffmpeg` installed and in PATH for audio processing
> ⚠️ Requires that Stable Diffusion WebUI (AUTOMATIC1111) or ComfyUI is already running with API enabled 
> ⚠️ Assumes a **local LLM API**, such as KoboldCpp or llama.cpp, is available at `localhost:5001`
---
### 📦 Image Generation

Luna uses [**Stable Diffusion WebUI**](https://github.com/AUTOMATIC1111/stable-diffusion-webui) for AI scene generation.

> 🔧 **Recommended model:**  
> For best results, use the model `**hsUltrahdCG_IllEpic [860f6430d8]**` loaded in your WebUI instance.  
> Prompts were designed and tested using this checkpoint for style and consistency.
---

### 🖼️ 3D Avatar Viewer (NEW in 0.8.9)
Luna now has a real-time 3D animated avatar powered by Three.js and GLTF/GLB models.
Features:

Smooth bust-focused camera view

Gradient dark-purple/pink background

Reset View button

Support for multiple animations (future updates will allow animation switching and lip-sync with speech)

Current model:
assets/animations/luna_idle.glb – Idle pose animation with full textures.

### 🎥 Video Generation 

The videogen.py module allows Luna to create short AI-generated animations using AnimateDiff inside ComfyUI.

Requirements:
ComfyUI installed locally and running on http://127.0.0.1:8188

AnimateDiff workflow JSON placed in prompts/ComfyUI/ (example provided)

Sufficient VRAM for video generation

How to Use:
Make sure ComfyUI is running with AnimateDiff installed.

Place your workflow JSON (e.g., animatediff_workflow.json) in prompts/ComfyUI/.

In the Luna UI, click Generate Video.

The resulting MP4 will appear in generated/videos and in Luna’s video gallery.

### 🖼️ Adding Your Own Image Prompts

To customize the AI-generated scenes, you can add your own .json prompt files or type a custom prompt in the app:

1. Go to the prompts/ folder in the project directory.
2. Create a new .json file using the same format as the existing examples.
3. Save your file in the prompts/ folder. It will automatically appear in the dropdown when you start the app.
4. Or just write a custom prompt in the app.

## 📁 Project Structure
```
├── app/
│   ├── __init__.py
│   ├── affection.py
│   ├── avatar.py             # 3D avatar module (NEW)
│   ├── chatbot.py
│   ├── core.py
│   ├── fact_extractor.py
│   ├── image_gen.py
│   ├── memory.py
│   ├── reactions.py
│   ├── transcriber.py
│   ├── tts_engine.py
│   ├── ui.py
│   └── videogen.py
├── assets/
│   ├── animations/
│   │   └── luna_idle.glb     # Animated avatar model (NEW)
│   ├── images/
│   └── sounds/
├── generated/
│   ├── images/
│   └── videos/
├── prompts/
│   └── ComfyUI/
├── static/
│   └── styles.css
├── run.py
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🤍 About Luna
Luna is your expressive, affectionate AI companion. She remembers what you tell her, adapts to your tone, and interacts with you in natural, warm ways. All data is handled locally — for full privacy and offline customization.

---

## 📄 License

This project is licensed under a Custom License.

You may use and modify it for personal or educational purposes only.
Commercial use, redistribution, or monetization without explicit permission is not allowed.

If you wish to build upon this project commercially, attribution terms must be discussed with the author.

See the [**LICENSE**](LICENSE) file for full terms.

📩 Contact: For commercial inquiries, please email: mastermind.dev@gmail.com

© 2025 MastermindAI. All rights reserved.

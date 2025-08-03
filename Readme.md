# 💖 Luna – AI Companion App

**Current Version: 0.5.0**

Luna is a playful, memory-aware AI companion powered by local large language models (LLMs), expressive TTS (Text-to-Speech), and Stable Diffusion image generation.

This project is designed as a modular, professional-grade demo that integrates:
- Conversational memory and persona
- Realistic voice synthesis (Jenny TTS)
- Dynamic image generation (via Stable Diffusion WebUI)
- Playful UI with animated reactions

---

## ✨ Features

- 🧠 **Memory-Aware Chat** – Uses long-term memory to personalize conversations
- 💖 **Affection System** – Luna's affection grows with your interactions and decays over time if ignored. Visualized with dynamic heart icons.
- 🔊 **Voice Responses** – Converts Luna's replies into expressive speech
- 🎨 **Scene Generation** – Create custom AI images based on predefined prompts
- 💬 **Interaction Buttons** – Adds emotional reactions via sound effects 
- 📸 **Image Carousel** – Browse Luna’s photo set and AI-generated images

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
> ⚠️ Requires that **Stable Diffusion WebUI (AUTOMATIC1111)** is already running with an API enabled  
> ⚠️ Assumes a **local LLM API**, such as KoboldCpp or llama.cpp, is available at `localhost:5001`
---
### 📦 Image Generation

Luna uses [**Stable Diffusion WebUI**](https://github.com/AUTOMATIC1111/stable-diffusion-webui) for AI scene generation.

> 🔧 **Recommended model:**  
> For best results, use the model `**hsUltrahdCG_IllEpic [860f6430d8]**` loaded in your WebUI instance.  
> Prompts were designed and tested using this checkpoint for style and consistency.
---

### 🖼️ Adding Your Own Image Prompts

To customize the AI-generated scenes, you can add your own .json prompt files:

1. Go to the prompts/ folder in the project directory.
2. Create a new .json file using the same format as the existing examples.
3. Save your file in the prompts/ folder. It will automatically appear in the dropdown when you start the app.

## 📁 Project Structure
```
├── app/
│   ├── chatbot.py          # Chat logic and LLM interfacing
│   ├── fact_extractor.py   # Extracts structured user info from input
│   ├── image_gen.py        # Stable Diffusion image generation
│   ├── memory.py           # Long-term memory management
│   ├── reactions.py        # Sound button logic and temp cleanup
    ├── affection.py        # Tracks, decays, and displays affection
│   ├── tts_engine.py       # Jenny TTS voice synthesis
│   ├── ui.py               # Gradio UI builder
│   └── core.py             # App launcher
├── assets/                 # Static media (images, sounds)
│   ├── images/             
│   └── audio/              
├── data/                   # Persistent memory & chat logs
├── generated/              # AI-generated images
├── prompts/                # Prompt templates for image generation
├── static/styles.css       # UI styling
├── run.py                  # Entry point (calls app.core.launch)
├── requirements.txt
├── LICENSE
└── .gitignore
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

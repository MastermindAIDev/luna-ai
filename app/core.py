from app.ui import build_interface
from app.videogen import COMFY_VIDEOS_DIR  # <-- reuse the exact folder your gallery lists

__version__ = "0.8.9"

def launch():
    interface = build_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=8080,
        share=True,
        allowed_paths=[COMFY_VIDEOS_DIR],  # ✅ let Gradio serve files from Comfy’s folder
    )


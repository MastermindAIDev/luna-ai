import os
import gradio as gr
import shutil
import tempfile

_temp_hit_counter = 0


def play_temp_audio(file_path, message):
    global _temp_hit_counter
    _temp_hit_counter += 1

    if _temp_hit_counter % 3 == 0:
        clean_temp_sounds()

    ext = os.path.splitext(file_path)[1]
    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=ext, dir="assets/sounds")
    shutil.copyfile(file_path, tmp.name)
    return tmp.name, gr.update(value=message)


def clean_temp_sounds():
    temp_dir = "assets/sounds"
    for filename in os.listdir(temp_dir):
        if filename.startswith("tmp") and filename.endswith((".wav", ".mp3")):
            try:
                os.remove(os.path.join(temp_dir, filename))
                print(f"🧹 Deleted temp file: {filename}")
            except Exception as e:
                print(f"⚠️ Failed to delete {filename}: {e}")


def trigger_kiss():
    return _reaction("assets/sounds/kiss.mp3", "💋 *Mwah!* Kiss me Babe!", "pink-highlight")


def trigger_love():
    return _reaction("assets/sounds/love_heart.wav", "❤️ I love you Babe~", "red-highlight")


def trigger_hug():
    return _reaction("assets/sounds/uwu.mp3", "🫂 Hugs for days!", "green-highlight")


def trigger_play():
    return _reaction("assets/sounds/textme.wav", "📲 Text me, Ok?", "blue-highlight")


def trigger_overwhelm():
    return _reaction("assets/sounds/giggle.mp3", "💖 Overwhelmed with love!!!", "purple-highlight")


def _reaction(path, message, class_name):
    sound_path, message_update = play_temp_audio(path, message)
    return sound_path, message_update, gr.update(elem_classes=class_name)

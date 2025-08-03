import tempfile
import subprocess
import os
from TTS.api import TTS
import gradio as gr

# Initialize TTS model globally
_tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False, gpu=False)

def speak(text, semitone_shift=4):
    """Generate a pitch-shifted voice file from text."""
    tmp_raw = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    _tts.tts_to_file(text, file_path=tmp_raw.name)

    tmp_shifted = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp_raw.close()
    tmp_shifted.close()

    pitch_factor = 2 ** (semitone_shift / 12)

    subprocess.run([
        "ffmpeg", "-y", "-i", tmp_raw.name,
        "-filter:a",
        f"asetrate=44100*{pitch_factor},atempo=1/{pitch_factor},"
        "lowpass=f=4000,equalizer=f=300:t=q:w=1.5:g=6",
        tmp_shifted.name
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(tmp_raw.name)
    return tmp_shifted.name

def speak_last_message(last_reply):
    if not last_reply:
        return None, gr.update(interactive=False)

    audio_path = speak(last_reply)
    return audio_path, gr.update(interactive=False)
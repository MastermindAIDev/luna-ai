# app/transcriber.py
import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import warnings

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

model = whisper.load_model("base")


def transcribe_unified(audio_path, chat_state):
    if audio_path is None:
        return chat_state, "", chat_state
    result = model.transcribe(audio_path)
    text = result["text"].strip()
    if chat_state is None:
        chat_state = []
    return chat_state, text, chat_state


def record_audio(duration=5, sample_rate=16000):
    print("🎙️ Recording...")
    audio = sd.rec(int(duration * sample_rate),
                   samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    return sample_rate, audio


def transcribe_audio(duration=5):
    sample_rate, audio = record_audio(duration)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        tmp_path = tmpfile.name

    wav.write(tmp_path, sample_rate, audio)
    print(f"[DEBUG] Temp WAV written to: {tmp_path}")

    result = model.transcribe(tmp_path)

    try:
        os.remove(tmp_path)
    except Exception as e:
        print(f"[WARN] Failed to delete temp file: {e}")

    print(f"[DEBUG] Transcription: '{result['text']}'")
    return result["text"].strip()


def transcribe_and_send(chat_state):
    text = transcribe_audio()
    print(f"[DEBUG] Transcription: '{text}'")

    if not text.strip():
        return chat_state, ""  # Nothing to send

    chat_state.append({"role": "user", "content": text})
    return chat_state, text

# For mobile compatibility


def transcribe_and_send_file(audio_path, chat_state):
    result = model.transcribe(audio_path)
    text = result["text"].strip()
    if chat_state is None:
        chat_state = []
    if not text:
        return chat_state, "", chat_state
    chat_state.append({"role": "user", "content": text})
    return chat_state, text, chat_state

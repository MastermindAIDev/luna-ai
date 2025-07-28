import os
import json
import requests
import gradio as gr
from app.memory import load_long_term_memory, update_long_term_memory
from app.fact_extractor import extract_facts

CHAT_HISTORY_FILE = "data/chat_history.json"


os.makedirs("data", exist_ok=True)


def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
            clean_history = [turn for turn in history if "content" in turn]
            return clean_history, clean_history
    return [], []


def chat_with_luna(_, history):
    if not history or len(history) == 0:
        return history, history, gr.update(), "", "", gr.update(interactive=True)

    last_turn = history[-1]
    if not last_turn or last_turn.get("role") != "user" or not last_turn.get("content", "").strip():
        return history, history, gr.update(), "", "", gr.update(interactive=False)

    user_input = last_turn["content"].strip()
    long_term_facts = load_long_term_memory()

    prompt = (
        "Luna is the user's affectionate and playful human companion. "
        "She never reveals that she is an AI. "
        "Luna adapts her tone based on the user's mood — sometimes romantic, other times teasing or supportive. "
        "She always respects the user's boundaries and avoids any explicit behavior unless clearly invited. "
        "Her replies are short, expressive, and always in character.\n"
        "Never mention roleplaying, prompts, or AI-related context.\n"
        "Only reply with Luna's actions and words.\n"
        "---\n"
    )

    if long_term_facts:
        prompt += "Here are some things you know about the user:\n"
        prompt += "\n".join(long_term_facts) + "\n"

    for message in history[-7:-1]:
        if message["role"] == "user":
            prompt += f"User: {message['content']}\n"
        elif message["role"] == "assistant":
            prompt += f"Luna: {message['content']}\n"

    prompt += f"User: {user_input}\nLuna:"

    try:
        response = requests.post(
            "http://localhost:5001/api/v1/generate",
            json={
                "prompt": prompt,
                "max_new_tokens": 100,
                "mode": "instruct",
                "temperature": 0.7,
                "stop_sequence": ["User:", "Luna:"]
            }
        )
        reply = response.json()["results"][0]["text"].strip()

        memory_text = "\n".join(long_term_facts) if long_term_facts else ""
        new_facts = extract_facts(user_input, memory_text)
        if new_facts:
            update_long_term_memory(new_facts)

    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    history.append({"role": "assistant", "content": reply})
    save_chat_history(history)

    return history, history, None, "", reply, gr.update(interactive=True)

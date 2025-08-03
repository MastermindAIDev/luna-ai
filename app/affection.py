import json
import os
import time

AFFECTION_FILE = "data/affection_score.json"
DEFAULT_AFFECTION = 0
DECAY_RATE_PER_HOUR = 120  # affection points lost per hour of inactivity
MAX_AFFECTION = 100
MIN_AFFECTION = 0


def load_affection():
    if os.path.exists(AFFECTION_FILE):
        with open(AFFECTION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            affection = data.get("affection", DEFAULT_AFFECTION)
            last_updated = data.get("last_updated", time.time())
            elapsed = time.time() - last_updated
            decay = DECAY_RATE_PER_HOUR * (elapsed / 3600)
            decayed = max(MIN_AFFECTION, affection - decay)
            return decayed
    return DEFAULT_AFFECTION


def decay_affection():
    decayed = load_affection()
    save_affection(decayed)
    # print(f"[Decay] Updated affection: {decayed}")


def format_affection_display():
    hearts = render_affection_hearts()
    return f"""
        <div class="affection-title">Affection Level:</div>
        <div class="affection-hearts">{hearts}</div>
        """


def load_affection_display():
    return f"""<div align="center"><strong>Affection Level:</strong><br>{render_affection_hearts()}</div>"""


def save_affection(score):
    os.makedirs("data", exist_ok=True)
    with open(AFFECTION_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "affection": score,
            "last_updated": time.time()
        }, f, indent=2)


def get_affection():
    return load_affection()


def adjust_affection(change):
    score = load_affection()
    score = max(MIN_AFFECTION, min(MAX_AFFECTION, score + change))
    save_affection(score)
    return score


def reset_affection():
    save_affection(DEFAULT_AFFECTION)
    return DEFAULT_AFFECTION


def render_affection_hearts():
    score = get_affection()
    total_hearts = 10
    fill_per_heart = 100 / total_hearts
    full_hearts = int(score // fill_per_heart)
    remainder = score % fill_per_heart
    fractional = remainder / fill_per_heart

    gradient_steps = {
        "💓": 0.8,
        "💖": 0.6,
        "💗": 0.4,
        "🩷": 0.2,
        "🤍": 0.0
    }

    html = '<div class="affection-hearts">'

    # Full red hearts — pulse
    for _ in range(full_hearts):
        html += '<span class="filled-heart">❤️</span>'

    # Fractional heart
    for emoji, threshold in gradient_steps.items():
        if fractional > threshold:
            html += f'<span>{emoji}</span>'
            break

    # Remaining empty hearts
    total_drawn = full_hearts + (1 if fractional > 0 else 0)
    for _ in range(total_hearts - total_drawn):
        html += '<span>🤍</span>'

    html += '</div>'
    return html


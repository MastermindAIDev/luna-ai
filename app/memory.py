import os
import json

LONG_TERM_MEMORY_FILE = "data/long_term_memory.json"


def update_long_term_memory(new_facts):
    if os.path.exists(LONG_TERM_MEMORY_FILE):
        with open(LONG_TERM_MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = set(json.load(f))
    else:
        memory = set()

    memory.update(new_facts)

    with open(LONG_TERM_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(list(memory), f, indent=2, ensure_ascii=False)


def load_long_term_memory():
    if os.path.exists(LONG_TERM_MEMORY_FILE):
        with open(LONG_TERM_MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

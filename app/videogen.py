# app/videogen.py
import os
import json
import time
import uuid
import requests
from pathlib import Path

# --- Config
COMFY_API_URL = os.environ.get("COMFY_API_URL", "http://127.0.0.1:8188")

# Where your workflow JSON might live
DEFAULT_WORKFLOW_CANDIDATES = [
    os.path.join("prompts", "ComfyUI", "animatediff_workflow.json")
]
# Comfy output location (used directly by the gallery)
COMFY_OUTPUT_DIR = os.environ.get(
    "COMFY_OUTPUT_DIR",
    r"C:\AI\zluda\ComfyUI\ComfyUI-Zluda\output"  # ✅ fixed: 'output' not 'ouutput'
)
# must match your filename_prefix subdir
COMFY_SUBDIR = "LunaGen"
COMFY_VIDEOS_DIR = str(Path(COMFY_OUTPUT_DIR) / COMFY_SUBDIR)
DEFAULT_NEG = (
    "nsfw, lowres, bad anatomy, extra limbs, missing fingers, distorted face, "
    "worst quality, blurry, watermark, malformed eyes, loli, impossible anatomy, "
    "unnatural head twist, broken neck, twisted torso"
)

BASE_TAGS = [
    "anime woman", "anime screencap", "anime artstyle",
    "black hair", "blue eyes", "blunt bangs", "earrings"
]
FORCE_TRAITS = [
    "short black hair",        # more specific than “medium hair”
    "blunt bangs",
]

# AnimateDiff node assumptions (change if your JSON differs)
POS_NODE_ID = "3"        # CLIPTextEncode (positive)
NEG_NODE_ID = "6"        # CLIPTextEncode (negative)
VIDEO_NODE_ID = "37"     # VHS_VideoCombine (has filename_prefix)

FILENAME_PREFIX = "LunaGen/luna"  # Comfy writes to ComfyUI/output/LunaGen/...
POLL_SECS = 1.5
TIMEOUT_SECS = 900


def _compose_positive(user_text: str, graph_default: str) -> str:
    txt = (user_text or "").strip() or (graph_default or "")
    low = txt.lower()
    # remove conflicts
    for bad in ["long hair", "very long hair", "brown hair", "blonde hair", "red hair"]:
        low = low.replace(bad, "")
    low = low.replace("medium hair", "short black hair")
    pieces = [p.strip(" ,") for p in [low, *BASE_TAGS, *
                                      FORCE_TRAITS] if p and p.strip(" ,")]
    seen, out = set(), []
    for p in pieces:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return ", ".join(out)

# --- Public: list all videos for the gallery (reads directly from Comfy output)


def get_all_videos_from_comfy():
    os.makedirs(COMFY_VIDEOS_DIR, exist_ok=True)
    vids = []
    for f in os.listdir(COMFY_VIDEOS_DIR):
        if f.lower().endswith((".mp4", ".webm", ".mov")):
            vids.append(str(Path(COMFY_VIDEOS_DIR) / f))
    vids.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return vids

# --- Helpers


def _load_workflow_json(workflow_path: str | None = None):
    if workflow_path and os.path.exists(workflow_path):
        path = workflow_path
    else:
        path = next(
            (p for p in DEFAULT_WORKFLOW_CANDIDATES if os.path.exists(p)), None)
        if not path:
            raise FileNotFoundError(
                "animatediff workflow JSON not found in expected locations.")
    with open(path, "r", encoding="utf-8") as f:
        print(f"🎯 Loaded workflow from: {path}")
        return json.load(f)


def _edit_workflow_graph(graph: dict, positive: str | None, negative: str | None, filename_prefix: str):
    # Validate nodes exist (fail fast if IDs don’t match your JSON)
    for nid, label in [(POS_NODE_ID, "POS_NODE_ID"), (NEG_NODE_ID, "NEG_NODE_ID"), (VIDEO_NODE_ID, "VIDEO_NODE_ID")]:
        if nid not in graph:
            raise KeyError(f"{label} '{nid}' not found in workflow JSON")
        if "inputs" not in graph[nid]:
            raise KeyError(
                f"{label} '{nid}' missing 'inputs' in workflow JSON node")

    graph[POS_NODE_ID]["inputs"]["text"] = positive if positive is not None else graph[POS_NODE_ID]["inputs"].get(
        "text", "")
    graph[NEG_NODE_ID]["inputs"]["text"] = negative if negative is not None else graph[NEG_NODE_ID]["inputs"].get(
        "text", "")
    graph[VIDEO_NODE_ID]["inputs"]["filename_prefix"] = filename_prefix

    print(
        f"📝 Using filename_prefix: {graph[VIDEO_NODE_ID]['inputs']['filename_prefix']}")
    return graph


def _submit_to_comfy(graph: dict) -> tuple[str, float]:
    submit_time = time.time()
    client_id = uuid.uuid4().hex
    resp = requests.post(
        f"{COMFY_API_URL}/prompt",
        json={"prompt": graph, "client_id": client_id},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("prompt_id", ""), submit_time


def _wait_for_new_video(since_time: float) -> str | None:
    """Block until a fresh .mp4 appears in ComfyUI/output/LunaGen (or timeout)."""
    target_dir = Path(COMFY_VIDEOS_DIR)
    start = time.time()
    target_dir.mkdir(parents=True, exist_ok=True)

    while time.time() - start < TIMEOUT_SECS:
        candidates = list(target_dir.glob("*.mp4"))
        fresh = [p for p in candidates if p.stat().st_mtime >=
                 since_time - 0.5]
        if fresh:
            newest = max(fresh, key=lambda p: p.stat().st_mtime)
            return str(newest.resolve())
        time.sleep(POLL_SECS)
    return None


def generate_luna_video(config_or_prompt: str | None, custom_prompt: str | None = None,
                        workflow_path: str | None = None):
    try:
        graph = _load_workflow_json(workflow_path)

        pos_default = graph.get(POS_NODE_ID, {}).get(
            "inputs", {}).get("text", "")
        pos = _compose_positive(custom_prompt, pos_default)
        neg = DEFAULT_NEG

        graph = _edit_workflow_graph(
            graph, positive=pos, negative=neg, filename_prefix=FILENAME_PREFIX)

        print(f"▶️ POS:\n{pos}\n\n🚫 NEG:\n{neg}\n")
        prompt_id, submit_time = _submit_to_comfy(graph)
        print(
            f"➡️ Submitted to ComfyUI (prompt_id={prompt_id}). Waiting for video in {COMFY_VIDEOS_DIR} ...")

        _wait_for_new_video(since_time=submit_time)

        # If you picked option A:
        return get_all_videos_from_comfy()
        # If you picked option B:
        # return None

    except Exception as e:
        print(f"❌ Error generating video: {e}")
        # Option A: return current gallery
        # return get_all_videos_from_comfy()
        return None

"""
================================================================================
Node Name   : TA Unified Model Switcher
Created     : 2025
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0


Description:
    Unified model switcher with dynamic slots (up to 3) and browser-based editor.
    Uses ta_model_choices.json for dropdown options. Lazy evaluation loads only
    the selected model's MODEL/CLIP/VAE. Web UI at http://localhost:8188/ta_model_choices/ui
    for editing choices without code changes.
================================================================================
"""

import os
import json
from aiohttp import web
from server import PromptServer

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_DIR = os.path.dirname(os.path.abspath(__file__))
_JSON_PATH = os.path.join(_DIR, "ta_model_choices.json")
_HTML_PATH = os.path.join(_DIR, "web", "js", "ta_model_choices_ui.html")

_DEFAULT_CHOICES = [
    "Z-Image Diffusion",
    "Z-Image GGUF",
    "Qwen Diffusion",
    "FLUX Diffusion",
    "Checkpoint",
]


def _load_choices() -> list:
    """
    Loads model choices from ta_model_choices.json, falls back to defaults.
    """
    if not os.path.exists(_JSON_PATH):
        _save_choices(_DEFAULT_CHOICES.copy())
        return _DEFAULT_CHOICES.copy()
    try:
        with open(_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("choices", _DEFAULT_CHOICES.copy())
    except Exception as e:
        print(f"[TAUnifiedModelSwitcher] Error loading JSON: {e}")
        return _DEFAULT_CHOICES.copy()


def _save_choices(choices: list) -> None:
    """
    Saves model choices to ta_model_choices.json.
    """
    try:
        with open(_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump({"choices": choices}, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[TAUnifiedModelSwitcher] Error saving JSON: {e}")


# ---------------------------------------------------------------------------
# Web Endpoints
# ---------------------------------------------------------------------------

@PromptServer.instance.routes.get("/ta_model_choices/ui")
async def ta_choices_ui(request):
    """
    Serves the browser-based model choices editor HTML.
    """
    if not os.path.exists(_HTML_PATH):
        return web.Response(text="HTML not found.", status=404)
    with open(_HTML_PATH, "r", encoding="utf-8") as f:
        return web.Response(text=f.read(), content_type="text/html")


@PromptServer.instance.routes.get("/ta_model_choices/list")
async def ta_choices_list(request):
    """
    API endpoint to retrieve current model choices.
    """
    return web.json_response({"choices": _load_choices()})


@PromptServer.instance.routes.post("/ta_model_choices/save")
async def ta_choices_save(request):
    """
    API endpoint to save updated model choices.
    """
    try:
        body = await request.json()
        choices = body.get("choices", [])
        choices = [str(c).strip() for c in choices if str(c).strip()]
        if not choices:
            return web.json_response({"ok": False, "error": "List cannot be empty."})
        _save_choices(choices)
        print(f"[TAUnifiedModelSwitcher] Choices saved: {choices}")
        return web.json_response({"ok": True})
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)})


def _build_slot_map() -> dict:
    """
    Dynamically generates SLOT_MAP from JSON choices.
    List position = slot number (1-based).
    """
    choices = _load_choices()
    return {
        choice: [f"model_{i+1}", f"clip_{i+1}", f"vae_{i+1}", f"model_name_{i+1}"]
        for i, choice in enumerate(choices)
    }


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

class TAUnifiedModelSwitcher:
    """
    Unified Model Switcher node supporting up to 3 dynamic slots.

    Features:
    - model_choice: Dropdown populated from ta_model_choices.json
    - Optional lazy inputs for each slot: model/clip/vae/model_name
    - Lazy evaluation: only active slot's upstream nodes execute
    - Dynamic SLOT_MAP generated from JSON choices
    - Browser editor: http://localhost:8188/ta_model_choices/ui

    Usage: Connect model loader groups to slots 1-3. Select via dropdown.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Required Inputs:
        model_choice: Dropdown of choices from JSON (editable via web UI).

        Optional Inputs (lazy):
        model_1/clip_1/vae_1/model_name_1: Slot 1 inputs
        model_2/clip_2/vae_2/model_name_2: Slot 2 inputs  
        model_3/clip_3/vae_3/model_name_3: Slot 3 inputs

        Returns:
        dict: ComfyUI INPUT_TYPES dictionary.
        """
        choices = _load_choices()
        return {
            "required": {
                "model_choice": (choices, {
                    "default": choices[0],
                    "tooltip": "Editor: http://localhost:8188/ta_model_choices/ui",
                }),
            },
            "optional": {
                "model_1": ("MODEL", {"lazy": True}),
                "clip_1": ("CLIP", {"lazy": True}),
                "vae_1": ("VAE", {"lazy": True}),
                "model_name_1": ("TA_MODEL_NAME", {"lazy": True}),

                "model_2": ("MODEL", {"lazy": True}),
                "clip_2": ("CLIP", {"lazy": True}),
                "vae_2": ("VAE", {"lazy": True}),
                "model_name_2": ("TA_MODEL_NAME", {"lazy": True}),

                "model_3": ("MODEL", {"lazy": True}),
                "clip_3": ("CLIP", {"lazy": True}),
                "vae_3": ("VAE", {"lazy": True}),
                "model_name_3": ("TA_MODEL_NAME", {"lazy": True}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "TA_MODEL_NAME")
    RETURN_NAMES = ("model", "clip", "vae", "active_model")
    FUNCTION = "select"
    CATEGORY = "TA Nodes/loaders"

    @classmethod
    def IS_CHANGED(cls, model_choice, **kwargs):
        """
        Triggers re-execution when model_choice changes.
        """
        return model_choice

    def check_lazy_status(self, model_choice, **kwargs):
        """
        Determines which lazy inputs to request for the selected slot.

        Called during graph planning. Returns only the inputs for the active
        slot, enabling lazy evaluation.

        Args:
        model_choice (str): Selected choice from dropdown.

        Returns:
        list: Input names for the active slot.
        """
        slot_map = _build_slot_map()
        needed = slot_map.get(model_choice)
        if needed:
            print(f"[TAUnifiedModelSwitcher] Loading slot: '{model_choice}' → {needed}")
            return needed
        all_inputs = []
        for v in slot_map.values():
            all_inputs.extend(v)
        return all_inputs

    def select(
        self,
        model_choice,
        model_1=None, clip_1=None, vae_1=None, model_name_1=None,
        model_2=None, clip_2=None, vae_2=None, model_name_2=None,
        model_3=None, clip_3=None, vae_3=None, model_name_3=None,
    ):
        """
        Selects and returns MODEL/CLIP/VAE from the active slot.

        Validates connections and slot index. Falls back to model_choice as
        name if model_name input is missing.

        Args:
        model_choice (str): Selected slot identifier.
        model_1..model_name_3: All slot inputs (lazy).

        Returns:
        tuple: (MODEL, CLIP, VAE, active_model_name)
        
        Raises:
        ValueError: Invalid choice, missing connections, or slot overflow.
        """
        all_models = [model_1, model_2, model_3]
        all_clips = [clip_1, clip_2, clip_3]
        all_vaes = [vae_1, vae_2, vae_3]
        all_names = [model_name_1, model_name_2, model_name_3]

        slot_map = _build_slot_map()
        if model_choice not in slot_map:
            raise ValueError(
                f"[TAUnifiedModelSwitcher] Unknown model_choice: '{model_choice}'\n"
                f"Available options: {list(slot_map.keys())}"
            )

        slot_inputs = slot_map[model_choice]
        idx = int(slot_inputs[0].split("_")[1]) - 1

        if idx >= 3:
            raise ValueError(
                f"[TAUnifiedModelSwitcher] Slot index {idx+1} exceeds maximum (3)."
            )

        model = all_models[idx]
        clip = all_clips[idx]
        vae = all_vaes[idx]
        name = all_names[idx]

        if model is None or clip is None or vae is None:
            raise ValueError(
                f"[TAUnifiedModelSwitcher] Slot '{model_choice}' (#{idx+1}) not connected "
                f"(model={model is not None}, clip={clip is not None}, vae={vae is not None})."
            )

        if name is None:
            name = model_choice

        print(f"[TAUnifiedModelSwitcher] Active: '{model_choice}' → '{name}'")
        return (model, clip, vae, name)


NODE_CLASS_MAPPINGS = {
    "TAUnifiedModelSwitcher": TAUnifiedModelSwitcher
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TAUnifiedModelSwitcher": "🧠 TA Unified Model Switcher v2.0"
}

"""
================================================================================
Node Name   : TA Sampler Preset
Created     : 2026-03-07
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Loads sampler presets from ta_sampler_presets.json on every execution.
    All outputs are directly connectable to TA KSampler. Includes a
    browser-based preset editor at:
    http://localhost:8188/ta_sampler_presets/ui
================================================================================
"""

import os
import json
from aiohttp import web
from server import PromptServer

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_DIR       = os.path.dirname(os.path.abspath(__file__))
_JSON_PATH = os.path.join(_DIR, "ta_sampler_presets.json")
_HTML_PATH = os.path.join(_DIR, "web", "js", "ta_sampler_presets_ui.html")

_DEFAULT_PRESETS = {
    "Z-Image Turbo": {
        "steps": 9, "cfg": 1.0,
        "start_at_step": 0, "end_at_step": 9999,
        "sampler_name": "euler", "scheduler": "beta",
    },
}


# ---------------------------------------------------------------------------
# JSON Helpers
# ---------------------------------------------------------------------------

def _load_presets() -> dict:
    """
    Loads presets from ta_sampler_presets.json. If the file does not exist it
    is created with _DEFAULT_PRESETS. Returns _DEFAULT_PRESETS as a fallback
    if the file cannot be read or parsed.

    Returns:
        dict: Mapping of preset name strings to preset parameter dicts.
    """
    if not os.path.exists(_JSON_PATH):
        _save_presets(_DEFAULT_PRESETS)
        return _DEFAULT_PRESETS.copy()
    try:
        with open(_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[TASamplerPreset] Error loading JSON: {e}")
        return _DEFAULT_PRESETS.copy()


def _save_presets(presets: dict) -> None:
    """
    Serializes the given presets dict to ta_sampler_presets.json.

    Args:
        presets (dict): Mapping of preset name strings to preset parameter dicts.
    """
    try:
        with open(_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[TASamplerPreset] Error saving JSON: {e}")


def _preset_names() -> list:
    """
    Returns an ordered list of all preset name strings from the presets file.
    Falls back to ['(empty)'] if no presets are found.

    Returns:
        list[str]: List of preset name strings.
    """
    return list(_load_presets().keys()) or ["(empty)"]


# ---------------------------------------------------------------------------
# Web Endpoints
# ---------------------------------------------------------------------------

@PromptServer.instance.routes.get("/ta_sampler_presets/ui")
async def ta_presets_ui(request):
    """
    Serves the browser-based sampler preset editor HTML page.

    Route: GET /ta_sampler_presets/ui

    Returns:
        web.Response: HTML page content, or a 404 response if the HTML file
                      is not found at the expected path.
    """
    if not os.path.exists(_HTML_PATH):
        return web.Response(text="HTML file not found.", status=404)
    with open(_HTML_PATH, "r", encoding="utf-8") as f:
        return web.Response(text=f.read(), content_type="text/html")


@PromptServer.instance.routes.get("/ta_sampler_presets/options")
async def ta_presets_options(request):
    """
    Returns all available sampler and scheduler names as JSON.
    Used by the browser editor to populate its dropdown menus.

    Route: GET /ta_sampler_presets/options

    Returns:
        web.Response: JSON response with {'samplers': [...], 'schedulers': [...]}.
    """
    import comfy.samplers
    return web.json_response({
        "samplers":   comfy.samplers.KSampler.SAMPLERS,
        "schedulers": comfy.samplers.KSampler.SCHEDULERS,
    })


@PromptServer.instance.routes.get("/ta_sampler_presets/list")
async def ta_presets_list(request):
    """
    Returns the full presets dictionary as JSON.

    Route: GET /ta_sampler_presets/list

    Returns:
        web.Response: JSON response containing all presets as a dict.
    """
    return web.json_response(_load_presets())


@PromptServer.instance.routes.post("/ta_sampler_presets/get")
async def ta_presets_get(request):
    """
    Returns the parameter dict for a single named preset.

    Route: POST /ta_sampler_presets/get
    Body:  {'preset': '<name>'}

    Returns:
        web.Response: JSON response with the preset's parameter dict,
                      or a 404 error if the preset name is not found.
    """
    try:
        body    = await request.json()
        name    = body.get("preset", "")
        presets = _load_presets()
        if name not in presets:
            return web.json_response({"error": f"Preset '{name}' not found."}, status=404)
        return web.json_response(presets[name])
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


@PromptServer.instance.routes.post("/ta_sampler_presets/save")
async def ta_presets_save(request):
    """
    Creates or updates a named preset and persists it to ta_sampler_presets.json.
    All parameter values are type-cast to their expected types before saving.

    Route: POST /ta_sampler_presets/save
    Body:  {'name': '<name>', 'data': {steps, cfg, start_at_step, end_at_step,
            sampler_name, scheduler}}

    Returns:
        web.Response: JSON response with {'ok': True} on success, or
                      {'ok': False, 'error': str} on validation failure or exception.
    """
    try:
        body  = await request.json()
        name  = body.get("name", "").strip()
        data  = body.get("data", {})
        if not name:
            return web.json_response({"ok": False, "error": "No preset name provided."})
        presets       = _load_presets()
        presets[name] = {
            "steps":         int(data.get("steps", 20)),
            "cfg":           float(data.get("cfg", 7.0)),
            "start_at_step": int(data.get("start_at_step", 0)),
            "end_at_step":   int(data.get("end_at_step", 9999)),
            "sampler_name":  str(data.get("sampler_name", "euler")),
            "scheduler":     str(data.get("scheduler", "normal")),
        }
        _save_presets(presets)
        print(f"[TASamplerPreset] Preset '{name}' saved.")
        return web.json_response({"ok": True})
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)})


@PromptServer.instance.routes.post("/ta_sampler_presets/delete")
async def ta_presets_delete(request):
    """
    Deletes a named preset from ta_sampler_presets.json.

    Route: POST /ta_sampler_presets/delete
    Body:  {'name': '<name>'}

    Returns:
        web.Response: JSON response with {'ok': True} on success, or
                      {'ok': False, 'error': str} if the preset is not found
                      or an exception occurs.
    """
    try:
        body    = await request.json()
        name    = body.get("name", "").strip()
        presets = _load_presets()
        if name not in presets:
            return web.json_response({"ok": False, "error": f"Preset '{name}' not found."})
        del presets[name]
        _save_presets(presets)
        print(f"[TASamplerPreset] Preset '{name}' deleted.")
        return web.json_response({"ok": True})
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)})


# ---------------------------------------------------------------------------
# Node: TASamplerPreset
# ---------------------------------------------------------------------------

class TASamplerPreset:
    """
    Loads sampler presets from ta_sampler_presets.json on every execution.

    All seven outputs (steps, cfg, sampler_name, scheduler, start_at_step,
    end_at_step, info) are directly connectable to TA KSampler inputs.
    The 'info' output provides a formatted summary string that can also be
    used by TAFluxGuidanceGate to detect FLUX presets.

    Browser-based preset editor: http://localhost:8188/ta_sampler_presets/ui
    """

    CATEGORY     = "TA Nodes/Sampling"
    FUNCTION     = "get_preset"
    RETURN_TYPES = ("INT",   "FLOAT", "STRING",       "STRING",    "INT",           "INT",         "STRING",)
    RETURN_NAMES = ("steps", "cfg",   "sampler_name", "scheduler", "start_at_step", "end_at_step", "info",)

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Reads the current preset names from ta_sampler_presets.json at node
        load time to populate the preset dropdown.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with the required preset input.
        """
        return {
            "required": {
                "preset": (_preset_names(), {
                    "default": _preset_names()[0],
                    "tooltip": "Select preset. Editor: http://localhost:8188/ta_sampler_presets/ui",
                }),
            },
        }

    def get_preset(self, preset: str):
        """
        Loads the selected preset from ta_sampler_presets.json and returns all
        its parameters as individual typed outputs.

        If the requested preset name is not found in the file (e.g. after a
        rename), the first available preset is used as a fallback and a warning
        is printed to the console.

        The 'info' output is a formatted multi-line string summarising all
        preset parameters. It is also used by TAFluxGuidanceGate — if the
        preset name contains 'FLUX', guidance is applied automatically.

        Args:
            preset (str): Name of the preset to load, as shown in the dropdown.

        Returns:
            tuple: (steps, cfg, sampler_name, scheduler, start_at_step,
                    end_at_step, info) with types (int, float, str, str, int,
                    int, str).
        """
        presets = _load_presets()

        if preset not in presets:
            print(f"[TASamplerPreset] Preset '{preset}' not found, using first available.")
            preset = list(presets.keys())[0]

        p    = presets[preset]
        info = (f"[{preset}]\n"
                f"steps        : {p['steps']}\n"
                f"cfg          : {p['cfg']}\n"
                f"sampler      : {p['sampler_name']}\n"
                f"scheduler    : {p['scheduler']}\n"
                f"start_at_step: {p['start_at_step']}\n"
                f"end_at_step  : {p['end_at_step']}")

        print(f"[TASamplerPreset] preset='{preset}' "
              f"steps={p['steps']} cfg={p['cfg']} "
              f"sampler={p['sampler_name']} scheduler={p['scheduler']} "
              f"start={p['start_at_step']} end={p['end_at_step']}")

        return (
            int(p["steps"]),
            float(p["cfg"]),
            str(p["sampler_name"]),
            str(p["scheduler"]),
            int(p["start_at_step"]),
            int(p["end_at_step"]),
            info,
        )


# ---------------------------------------------------------------------------
# Node Registration
# ---------------------------------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "ta_sampler_preset": TASamplerPreset,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ta_sampler_preset": "🎛️ TA Sampler Preset",
}

"""
================================================================================
Node Name   : TA Discord Link
Created     : 2026-03-13
Modified    : 2026-03-13
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    A purely informational node that displays a clickable Discord invite link
    directly inside the ComfyUI graph. No inputs, no outputs.

    The invite URL is stored in ta_discord_link.json and can be edited via
    the browser-based editor at:
    http://localhost:8188/ta_discord_link/ui

    The matching JS widget extension reads the URL from
    GET /ta_discord_link/config and renders a styled Discord button.
================================================================================
"""

import os
import json
from aiohttp import web
from server import PromptServer

# ──────────────────────────────────────────────
#  Paths
# ──────────────────────────────────────────────
_THIS_DIR   = os.path.dirname(os.path.abspath(__file__))
_CFG_FILE   = os.path.join(_THIS_DIR, "ta_discord_link.json")
_HTML_PATH  = os.path.join(_THIS_DIR, "web", "js", "ta_discord_link_ui.html")

_DEFAULT_CFG = {
    "discord_url": "https://discord.gg/YOUR_INVITE_CODE",
    "label":       "Join us on Discord",
}


# ──────────────────────────────────────────────
#  Config helpers
# ──────────────────────────────────────────────
def _load_cfg() -> dict:
    """
    Loads ta_discord_link.json and returns its contents.

    Creates the file with defaults if it does not exist. Returns _DEFAULT_CFG
    on any read or parse error without modifying the file.

    Returns:
        dict: Config dict with 'discord_url' and 'label' keys.
    """
    if not os.path.exists(_CFG_FILE):
        try:
            with open(_CFG_FILE, "w", encoding="utf-8") as f:
                json.dump(_DEFAULT_CFG, f, indent=2, ensure_ascii=False)
            print("[TADiscordLink] ta_discord_link.json created with defaults.")
        except Exception as e:
            print(f"[TADiscordLink] Could not create config file: {e}")
            return dict(_DEFAULT_CFG)

    try:
        with open(_CFG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {**_DEFAULT_CFG, **data}   # fill missing keys with defaults
        return dict(_DEFAULT_CFG)
    except Exception as e:
        print(f"[TADiscordLink] Error reading config: {e}")
        return dict(_DEFAULT_CFG)


def _save_cfg(cfg: dict) -> None:
    """
    Persists the given config dict to ta_discord_link.json.

    Args:
        cfg (dict): Config dict to write.
    """
    with open(_CFG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


# ──────────────────────────────────────────────
#  Web Endpoints
# ──────────────────────────────────────────────
@PromptServer.instance.routes.get("/ta_discord_link/ui")
async def ta_discord_link_ui(request):
    """
    Serves the browser-based Discord link editor HTML page.

    Route: GET /ta_discord_link/ui

    Returns:
        web.Response: HTML page, or 404 if the HTML file is missing.
    """
    if not os.path.exists(_HTML_PATH):
        return web.Response(text="HTML editor file not found.", status=404)
    with open(_HTML_PATH, "r", encoding="utf-8") as f:
        return web.Response(text=f.read(), content_type="text/html")


@PromptServer.instance.routes.get("/ta_discord_link/config")
async def ta_discord_link_config(request):
    """
    Returns the current Discord link config as JSON.

    Route: GET /ta_discord_link/config

    Returns:
        web.Response: JSON response with 'discord_url' and 'label'.
    """
    return web.json_response(_load_cfg())


@PromptServer.instance.routes.post("/ta_discord_link/save")
async def ta_discord_link_save(request):
    """
    Accepts a JSON body with 'discord_url' (required) and 'label' (optional)
    and persists them to ta_discord_link.json.

    Route: POST /ta_discord_link/save
    Body:  {'discord_url': str, 'label': str}

    Returns:
        web.Response: JSON {'ok': True} on success or {'ok': False, 'error': str}.
    """
    try:
        body = await request.json()
        url  = body.get("discord_url", "").strip()
        if not url:
            return web.json_response({"ok": False, "error": "discord_url must not be empty."})
        cfg = {
            "discord_url": url,
            "label":       body.get("label", _DEFAULT_CFG["label"]).strip() or _DEFAULT_CFG["label"],
        }
        _save_cfg(cfg)
        print(f"[TADiscordLink] Config saved: {url}")
        return web.json_response({"ok": True})
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)})


# ──────────────────────────────────────────────
#  Node
# ──────────────────────────────────────────────
class TADiscordLink:
    """
    Renders a clickable Discord invite link inside the ComfyUI node graph.

    This node has no functional inputs or outputs. The invite URL and button
    label are stored in ta_discord_link.json and can be changed via the
    browser editor at http://localhost:8188/ta_discord_link/ui.
    The JS widget fetches the current config via GET /ta_discord_link/config
    and renders a styled Discord button directly in the graph.
    """

    CATEGORY = "thomo.ART/utils"
    FUNCTION = "run"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ()

    def run(self):
        """No-op execution — all rendering is handled on the JS side."""
        return {}


# ──────────────────────────────────────────────
#  Registration
# ──────────────────────────────────────────────
NODE_CLASS_MAPPINGS = {
    "TADiscordLink": TADiscordLink,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TADiscordLink": "TA Discord Link",
}

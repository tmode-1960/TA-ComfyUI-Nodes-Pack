"""
================================================================================
Node Name   : TA Help Link
Created     : 2026-03-12
Modified    : 2026-03-12
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 1.2
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0
Description:
    Decorative utility node that displays a clickable button inside the
    ComfyUI workflow canvas. Label and page are configurable via the
    Properties panel (right-click → Properties). Clicking the button
    opens a local wiki page served via a registered ComfyUI route.

    Route  : GET /ta-nodes/wiki/{filename}
    Wiki   : wiki/index.html  (Markdown viewer)
    Pages  : wiki/*.md

    No inputs or outputs - purely decorative/informational.
================================================================================
"""

import os
from aiohttp import web
from server import PromptServer

# ---------------------------------------------------------------------------
# Static file route: /ta-nodes/wiki/<filename>
# Serves any file from the wiki/ subdirectory next to this module.
# ---------------------------------------------------------------------------

WIKI_DIR = os.path.join(os.path.dirname(__file__), "web", "wiki")


@PromptServer.instance.routes.get("/ta-nodes/wiki/{filename}")
async def serve_wiki_file(request):
    filename = request.match_info["filename"]

    # Basic path traversal guard
    if ".." in filename or "/" in filename or "\\" in filename:
        raise web.HTTPForbidden()

    filepath = os.path.join(WIKI_DIR, filename)
    if not os.path.isfile(filepath):
        raise web.HTTPNotFound()

    return web.FileResponse(filepath)


# ---------------------------------------------------------------------------
# Node definition
# ---------------------------------------------------------------------------

class TAHelpLink:

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ()
    FUNCTION = "noop"
    OUTPUT_NODE = True
    CATEGORY = "thomo.ART/utils"

    def noop(self):
        return {}


NODE_CLASS_MAPPINGS = {
    "TAHelpLink": TAHelpLink,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TAHelpLink": "TA Help Link",
}

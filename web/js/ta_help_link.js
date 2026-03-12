/**
 * TAHelpLink - Frontend Extension
 * Renders a clickable button inside the node that opens a local wiki page.
 * Label and page are configured via the Properties panel (right-click → Properties).
 *
 * Wiki viewer : wiki/index.html  → served at /ta-nodes/wiki/index.html
 * Markdown    : wiki/<page>.md   → served at /ta-nodes/wiki/<page>.md
 * Renderer    : web/js/marked.min.js
 *               → manuell herunterladen von https://github.com/markedjs/marked/releases
 *
 * Part of the TA Nodes Pack by thomo.ART
 */

import { app } from "../../scripts/app.js";

const BUTTON_HEIGHT  = 30;
const BUTTON_PADDING = 10;
const NODE_WIDTH     = 180;
const NODE_HEIGHT    = 58;

const WIKI_BASE = `${location.origin}/ta-nodes/wiki`;
// Note: marked.min.js served via /extensions/TA-ComfyUI-Nodes-Pack/marked.min.js

/**
 * Resolve the final URL.
 * - Full http(s):// URL → used as-is
 * - Filename (e.g. "help.md") → routed through /ta-nodes/wiki/index.html?page=...
 */
function resolveUrl(page) {
    if (!page) return null;
    if (/^https?:\/\//i.test(page)) return page;
    return `${WIKI_BASE}/index.html?page=${encodeURIComponent(page)}`;
}

app.registerExtension({
    name: "thomo.TAHelpLink",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "TAHelpLink") return;

        // Initialise properties with defaults on node creation
        const origOnNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            if (origOnNodeCreated) origOnNodeCreated.apply(this, arguments);

            if (!this.properties) this.properties = {};
            if (this.properties.label === undefined) this.properties.label = "📖 Help";
            if (this.properties.page  === undefined) this.properties.page  = "help.md";

            this.size      = [NODE_WIDTH, NODE_HEIGHT];
            this.resizable = false;
        };

        // Draw the button
        nodeType.prototype.onDrawForeground = function (ctx) {
            if (this.flags?.collapsed) return;

            const x     = BUTTON_PADDING;
            const w     = this.size[0] - BUTTON_PADDING * 2;
            const y     = (this.size[1] - BUTTON_HEIGHT) / 2;
            const label = this.properties?.label || "📖 Help";
            const hov   = this._helpLinkHovered;

            // Background
            ctx.fillStyle = hov ? "#3a7bd5" : "#2a5db0";
            ctx.beginPath();
            ctx.roundRect(x, y, w, BUTTON_HEIGHT, 6);
            ctx.fill();

            // Border
            ctx.strokeStyle = hov ? "#5a9bf5" : "#4a7dd0";
            ctx.lineWidth   = 1;
            ctx.stroke();

            // Label
            ctx.fillStyle    = "#ffffff";
            ctx.font         = "bold 13px Arial";
            ctx.textAlign    = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(label, x + w / 2, y + BUTTON_HEIGHT / 2);

            this._btnBounds = { x, y, w, h: BUTTON_HEIGHT };
        };

        // Fixed size
        nodeType.prototype.computeSize = function () {
            return [NODE_WIDTH, NODE_HEIGHT];
        };

        // Hover
        nodeType.prototype.onMouseMove = function (e, pos) {
            const b = this._btnBounds;
            if (!b) return;
            const hov = pos[0] >= b.x && pos[0] <= b.x + b.w &&
                        pos[1] >= b.y && pos[1] <= b.y + b.h;
            if (hov !== this._helpLinkHovered) {
                this._helpLinkHovered = hov;
                app.canvas.setDirty(true);
            }
            app.canvas.canvas.style.cursor = hov ? "pointer" : "";
        };

        nodeType.prototype.onMouseLeave = function () {
            if (this._helpLinkHovered) {
                this._helpLinkHovered = false;
                app.canvas.canvas.style.cursor = "";
                app.canvas.setDirty(true);
            }
        };

        // Click → open wiki
        nodeType.prototype.onMouseDown = function (e, pos) {
            const b = this._btnBounds;
            if (!b) return;
            const clicked = pos[0] >= b.x && pos[0] <= b.x + b.w &&
                            pos[1] >= b.y && pos[1] <= b.y + b.h;
            if (clicked) {
                const url = resolveUrl(this.properties?.page);
                if (url) window.open(url, "_blank", "noopener,noreferrer");
                return true;
            }
        };
    },
});

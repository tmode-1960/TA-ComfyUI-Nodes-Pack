/**
 * TADiscordLink — ComfyUI JS Widget Extension
 * © 2026, Thomas Möhrling (thomo.ART)
 * Version: 2.0
 *
 * Fetches the Discord invite URL from GET /ta_discord_link/config and renders
 * a styled Discord button inside the TADiscordLink node. Opens the server in
 * a new browser tab on click.
 *
 * The URL and label can be edited at http://localhost:8188/ta_discord_link/ui
 */

import { app } from "../../scripts/app.js";

const DISCORD_PURPLE       = "#5865F2";
const DISCORD_PURPLE_HOVER = "#4752C4";

const DISCORD_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
  width="18" height="18" fill="white"
  style="margin-right:6px;flex-shrink:0;">
  <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037
    c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0
    12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037
    A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027
    C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057
    19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028
    14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106
    13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128
    10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01
    c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01
    c.12.098.246.198.373.292a.077.077 0 0 1-.006.127
    12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107
    c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028
    19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054
    c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03z
    M8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419
    0-1.333.956-2.419 2.157-2.419
    1.21 0 2.176 1.096 2.157 2.42
    0 1.333-.956 2.418-2.157 2.418z
    m7.975 0c-1.183 0-2.157-1.085-2.157-2.419
    0-1.333.955-2.419 2.157-2.419
    1.21 0 2.176 1.096 2.157 2.42
    0 1.333-.946 2.418-2.157 2.418z"/>
</svg>`;

/** Fetch config once per page load and cache it. */
let _configCache = null;
async function _getConfig() {
    if (_configCache) return _configCache;
    try {
        const res = await fetch("/ta_discord_link/config");
        if (res.ok) _configCache = await res.json();
    } catch (e) {
        console.warn("[TADiscordLink] Could not fetch config:", e);
    }
    return _configCache ?? { discord_url: "#", label: "Join us on Discord" };
}

app.registerExtension({
    name: "thomo.ART.TADiscordLink",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "TADiscordLink") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;

        nodeType.prototype.onNodeCreated = function () {
            onNodeCreated?.apply(this, arguments);

            this.size     = [280, 90];
            this.resizable = false;

            // ── Wrapper div (needed for DOM widget sizing) ────────────────
            const wrapper = document.createElement("div");
            Object.assign(wrapper.style, {
                display:        "flex",
                flexDirection:  "column",
                gap:            "6px",
                width:          "100%",
                boxSizing:      "border-box",
            });

            // ── Discord button ────────────────────────────────────────────
            const btn = document.createElement("a");
            btn.target = "_blank";
            btn.rel    = "noopener noreferrer";
            btn.href   = "#";   // replaced after config loads

            Object.assign(btn.style, {
                display:        "inline-flex",
                alignItems:     "center",
                justifyContent: "center",
                width:          "100%",
                padding:        "8px 14px",
                background:     DISCORD_PURPLE,
                color:          "white",
                fontFamily:     "'gg sans', 'Noto Sans', sans-serif",
                fontSize:       "14px",
                fontWeight:     "600",
                borderRadius:   "6px",
                textDecoration: "none",
                cursor:         "pointer",
                boxSizing:      "border-box",
                transition:     "background 0.15s ease",
                userSelect:     "none",
            });

            btn.innerHTML = DISCORD_SVG + "Join us on Discord";

            btn.addEventListener("mouseenter", () => { btn.style.background = DISCORD_PURPLE_HOVER; });
            btn.addEventListener("mouseleave", () => { btn.style.background = DISCORD_PURPLE; });
            // Prevent LiteGraph from swallowing the click
            btn.addEventListener("pointerdown", (e) => e.stopPropagation());

            // ── Edit-link ─────────────────────────────────────────────────
            const editLink = document.createElement("a");
            editLink.href   = "/ta_discord_link/ui";
            editLink.target = "_blank";
            editLink.rel    = "noopener noreferrer";
            editLink.textContent = "⚙ Edit link…";
            Object.assign(editLink.style, {
                fontSize:       "11px",
                color:          "#aaa",
                textDecoration: "none",
                textAlign:      "center",
                display:        "block",
            });
            editLink.addEventListener("mouseenter", () => { editLink.style.color = "#fff"; });
            editLink.addEventListener("mouseleave", () => { editLink.style.color = "#aaa"; });
            editLink.addEventListener("pointerdown", (e) => e.stopPropagation());

            wrapper.appendChild(btn);
            wrapper.appendChild(editLink);

            this.addDOMWidget("discord_widget", "div", wrapper, {
                getValue: () => "",
                setValue: () => {},
            });

            // ── Load config and update button ─────────────────────────────
            _getConfig().then(cfg => {
                btn.href      = cfg.discord_url ?? "#";
                btn.innerHTML = DISCORD_SVG + (cfg.label ?? "Join us on Discord");
            });
        };
    },
});

/**
 * TA Sampler Preset - Editor Button
 * ===================================
 * Fügt dem TA Sampler Preset Node einen Button hinzu
 * der den Browser-Editor öffnet.
 *
 * Author: TA Nodes Pack
 */

import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "TA.SamplerPresetEditorButton",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "TASamplerPreset") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;

        nodeType.prototype.onNodeCreated = function () {
            if (onNodeCreated) onNodeCreated.apply(this, arguments);

            this.addWidget("button", "✏️ Preset Editor öffnen", null, () => {
                window.open(window.location.origin + "/ta_sampler_presets/ui", "_blank");
            });
        };
    },
});

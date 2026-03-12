/**
 * TA Model Preset - Editor Button
 * ================================
 * Fügt dem TA Model Preset Node einen Button hinzu
 * der den Browser-Editor öffnet.
 *
 * Author: TA Nodes Pack
 */

import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "TA.ModelPresetEditorButton",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "TAModelPreset") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;

        nodeType.prototype.onNodeCreated = function () {
            if (onNodeCreated) onNodeCreated.apply(this, arguments);

            this.addWidget("button", "✏️ Model Preset Editor öffnen", null, () => {
                window.open("http://localhost:8188/ta_model_presets/ui", "_blank");
            });
        };
    },
});

/**
 * TA Mini Model Switcher - Editor Button
 * =======================================
 * Fügt dem TA Mini Model Switcher Node einen Button hinzu
 * der den Browser-Editor öffnet.
 *
 * Author: TA Nodes Pack
 */

import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "TA.ModelChoicesEditorButton",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "TAUnifiedModelSwitcher") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;

        nodeType.prototype.onNodeCreated = function () {
            if (onNodeCreated) onNodeCreated.apply(this, arguments);

            this.addWidget("button", "✏️ Model Choices Editor öffnen", null, () => {
                window.open("http://localhost:8188/ta_model_choices/ui", "_blank");
            });
        };
    },
});

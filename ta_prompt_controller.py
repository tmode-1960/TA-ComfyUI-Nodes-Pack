class TAPromptController:
    """
    Manages the flow between a generated prompt (e.g. from VLM/LLM) and manual input.
    Allows switching between sources or combining them.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "manual_prompt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "dynamicPrompts": True,
                    "placeholder": "Type here or convert to input..."
                }),
                "mode": ([
                    "Manual Only",
                    "Generated Only",
                    "Combine: Manual + Generated",
                    "Combine: Generated + Manual",
                    "Clear / Empty"
                ], {
                    "default": "Manual Only"
                }),
                "delimiter": ("STRING", {
                    "default": ", ",
                    "multiline": False
                }),
            },
            "optional": {
                "generated_prompt": ("STRING", {
                    "forceInput": True,
                    "default": ""
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "process_prompt"
    CATEGORY = "TA Nodes/text"

    def process_prompt(self, manual_prompt, mode, delimiter, generated_prompt=""):
        if manual_prompt is None: manual_prompt = ""
        if generated_prompt is None: generated_prompt = ""

        result = ""

        if mode == "Manual Only":
            result = manual_prompt

        elif mode == "Generated Only":
            result = generated_prompt

        elif mode == "Combine: Manual + Generated":
            if manual_prompt and generated_prompt:
                result = f"{manual_prompt}{delimiter}{generated_prompt}"
            else:
                result = manual_prompt or generated_prompt

        elif mode == "Combine: Generated + Manual":
            if manual_prompt and generated_prompt:
                result = f"{generated_prompt}{delimiter}{manual_prompt}"
            else:
                result = generated_prompt or manual_prompt

        elif mode == "Clear / Empty":
            result = ""

        return (result,)

# Node Registration
NODE_CLASS_MAPPINGS = {
    "TAPromptController": TAPromptController
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TAPromptController": "TA Prompt Controller (Switch)"
}

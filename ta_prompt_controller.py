"""
================================================================================
Node Name   : TA Prompt Controller (Switch)
Created     : 2025
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Controls the flow between a manually typed prompt and a generated prompt
    (e.g. from a VLM or LLM node). Supports five modes: pass-through of either
    source, two combine orders, or an empty output. Intended as a central
    prompt routing node in TA workflows.
================================================================================
"""


class TAPromptController:
    """
    Manages the flow between a generated prompt (e.g. from VLM/LLM) and manual
    input. Allows switching between sources or combining them in either order.

    Five modes are available:
      - Manual Only:               Returns manual_prompt unchanged.
      - Generated Only:            Returns generated_prompt unchanged.
      - Combine: Manual + Generated: Joins manual then generated with delimiter.
      - Combine: Generated + Manual: Joins generated then manual with delimiter.
      - Clear / Empty:             Returns an empty string regardless of inputs.

    In Combine modes, if only one input is non-empty that value is returned
    without the delimiter.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Inputs:
            manual_prompt:    Free-text prompt typed directly in the node widget.
                              Supports dynamic prompts syntax.
            mode:             Selects the output routing / combination strategy.
            delimiter:        Separator string inserted between prompts in Combine
                              modes. Defaults to ', '.
            generated_prompt: Optional STRING input from an upstream LLM/VLM node.
                              Defaults to an empty string if not connected.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with required and optional inputs.
        """
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
        """
        Routes or combines the input prompts according to the selected mode.

        None values for either prompt input are treated as empty strings.
        In Combine modes the delimiter is only inserted when both inputs are
        non-empty; a single non-empty input is returned as-is.

        Args:
            manual_prompt (str):    Manually typed prompt string.
            mode (str):             One of the five routing mode strings.
            delimiter (str):        Separator inserted between prompts in Combine modes.
            generated_prompt (str): Prompt string from an upstream LLM/VLM node.
                                    Defaults to '' if not connected.

        Returns:
            tuple[str]: Single-element tuple containing the final prompt string.
        """
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

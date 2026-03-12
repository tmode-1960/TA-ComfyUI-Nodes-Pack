"""
================================================================================
Node Name   : TA Prompt Hub
Created     : 2025
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Central prompt collector node that gathers all prompt inputs in one place.
    Pure pass-through with no routing logic — use TAPromptController for mode
    switching. Also provides a combined_prompt output that joins positive_prompt,
    additional_prompt, and lora_trigger_words with ', ' (empty parts omitted).
================================================================================
"""


class TAPromptHub:
    """
    Central prompt collector — gathers all prompt inputs in one node.
    No logic, pure pass-through. Use TAPromptController for mode switching.

    Outputs:
      positive_prompt     – pass-through
      additional_prompt   – pass-through
      negative_prompt     – pass-through
      lora_trigger_words  – optional input, pass-through
      combined_prompt     – positive_prompt + additional_prompt + lora_trigger_words
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Inputs:
            positive_prompt:   Main positive prompt text. Supports dynamic prompts.
            additional_prompt: Secondary positive prompt, intended for style or
                               scene additions without LoRA trigger words.
            negative_prompt:   Negative prompt text. Supports dynamic prompts.
            lora_trigger_words: Optional STRING input from an upstream LoRA node.
                                Defaults to '' if not connected.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with required and optional inputs.
        """
        return {
            "required": {
                "positive_prompt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "dynamicPrompts": True,
                    "placeholder": "Positive prompt..."
                }),
                "additional_prompt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "dynamicPrompts": True,
                    "placeholder": "Additional positive prompt (no LoRA trigger words)..."
                }),
                "negative_prompt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "dynamicPrompts": True,
                    "placeholder": "Negative prompt..."
                }),
            },
            "optional": {
                "lora_trigger_words": ("STRING", {
                    "forceInput": True,
                    "default": ""
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "additional_prompt", "negative_prompt", "lora_trigger_words", "combined_prompt")
    FUNCTION = "collect_prompts"
    CATEGORY = "TA Nodes/text"

    def collect_prompts(self, positive_prompt, additional_prompt, negative_prompt, lora_trigger_words=""):
        """
        Passes all prompt inputs through unchanged and builds a combined prompt.

        None values for any input are normalized to empty strings. The
        combined_prompt output joins positive_prompt, additional_prompt, and
        lora_trigger_words with ', ', skipping any parts that are empty or
        whitespace-only.

        Args:
            positive_prompt (str):    Main positive prompt string.
            additional_prompt (str):  Secondary positive prompt string.
            negative_prompt (str):    Negative prompt string.
            lora_trigger_words (str): LoRA trigger word string from an upstream
                                      node. Defaults to '' if not connected.

        Returns:
            tuple[str, str, str, str, str]:
                (positive_prompt, additional_prompt, negative_prompt,
                 lora_trigger_words, combined_prompt)
        """
        if positive_prompt is None: positive_prompt = ""
        if additional_prompt is None: additional_prompt = ""
        if negative_prompt is None: negative_prompt = ""
        if lora_trigger_words is None: lora_trigger_words = ""

        # combined_prompt: join positive + additional + lora_trigger_words (non-empty parts only)
        parts = [p for p in [positive_prompt, additional_prompt, lora_trigger_words] if p.strip()]
        combined_prompt = ", ".join(parts)

        return (positive_prompt, additional_prompt, negative_prompt, lora_trigger_words, combined_prompt)


# Node Registration
NODE_CLASS_MAPPINGS = {
    "TAPromptHub": TAPromptHub
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TAPromptHub": "🔀 TA Prompt Hub"
}

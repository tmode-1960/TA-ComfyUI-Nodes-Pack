"""
================================================================================
Node Name   : TA Flux Guidance Gate
Created     : 2026-03-10
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Conditionally applies Flux Guidance to a conditioning tensor based on the
    active sampler preset. Guidance is only applied when the preset name
    contains 'FLUX'; otherwise the conditioning is passed through unchanged.
================================================================================
"""

import node_helpers


class TAFluxGuidanceGate:
    """
    Gates Flux Guidance based on the active sampler preset name.

    Passes the conditioning through node_helpers.conditioning_set_values with
    the specified guidance value only when the connected preset_info string
    contains 'FLUX' (case-insensitive). For all other presets the conditioning
    tensor is returned unmodified, avoiding unintended guidance injection into
    non-Flux samplers.
    """

    CATEGORY     = "TA Nodes/Sampling"
    FUNCTION     = "apply"
    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("conditioning",)

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Inputs:
            conditioning: The conditioning tensor to be passed through or modified.
            guidance:     The Flux guidance scale value applied when a FLUX preset
                          is active. Has no effect for non-Flux presets.
            preset_info:  The 'info' string output from a TA Sampler Preset node.
                          Used to detect whether the active preset is FLUX-based.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with all required inputs.
        """
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
                "guidance":     ("FLOAT", {
                    "default": 3.5, "min": 0.0, "max": 100.0, "step": 0.1,
                    "tooltip": "Flux Guidance scale – only applied when a FLUX preset is active.",
                }),
                "preset_info":  ("STRING", {
                    "default": "",
                    "tooltip": "Connect the 'info' output of a TA Sampler Preset node.",
                    "forceInput": True,
                }),
            },
        }

    def apply(self, conditioning, guidance, preset_info):
        """
        Applies or bypasses Flux Guidance depending on the active sampler preset.

        Checks whether the preset_info string contains 'FLUX' (case-insensitive).
        If a FLUX preset is detected, the guidance value is injected into the
        conditioning tensor via node_helpers.conditioning_set_values. Otherwise
        the conditioning is returned unmodified.

        Args:
            conditioning: The input conditioning tensor.
            guidance (float): Flux guidance scale to apply for FLUX presets.
            preset_info (str): Info string from a TA Sampler Preset node; used
                               to determine whether the active preset is FLUX-based.

        Returns:
            tuple: Single-element tuple containing the (modified or unmodified)
                   conditioning tensor.
        """
        is_flux = "FLUX" in preset_info.upper()

        if is_flux:
            print(f"[TAFluxGuidanceGate] FLUX preset detected – applying guidance={guidance}.")
            result = node_helpers.conditioning_set_values(
                conditioning, {"guidance": guidance}
            )
        else:
            print(f"[TAFluxGuidanceGate] No FLUX preset – passing conditioning through unchanged.")
            result = conditioning

        return (result,)


# ---------------------------------------------------------------------------
# Node Registration
# ---------------------------------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "TAFluxGuidanceGate": TAFluxGuidanceGate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TAFluxGuidanceGate": "🌊 TA Flux Guidance Gate",
}

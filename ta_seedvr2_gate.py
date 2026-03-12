"""
================================================================================
Node Name   : TA SeedVR2 Gate
Created     : 2025
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0


Description:
    Enable/disable gate for SeedVR2 upscaler pipeline.
    When disabled, all upstream nodes (SeedVR2LoadDiTModel, SeedVR2LoadVAEModel,
    image source) are skipped entirely due to lazy evaluation. When enabled,
    inputs pass through unchanged for normal workflow execution.
================================================================================
"""

from comfy_execution.graph import ExecutionBlocker


class TASeedVR2Gate:
    """
    Gate node for SeedVR2 upscaler pipeline using ComfyUI lazy evaluation.

    Controls execution of expensive upstream nodes like model loaders and image
    preparation. When enabled=False, optional inputs are never requested or
    executed, preventing unnecessary computation. When enabled=True, all inputs
    are passed through normally to downstream nodes.

    Uses check_lazy_status() to conditionally request lazy inputs and gate()
    to either return the real inputs or ExecutionBlocker placeholders.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Inputs:
        enabled: Master toggle. False = bypass upstream execution entirely.
        image: (optional/lazy) IMAGE tensor from upstream source.
        dit: (optional/lazy) SEEDVR2_DIT model tensor.
        vae: (optional/lazy) SEEDVR2_VAE model tensor.

        Returns:
        dict: ComfyUI INPUT_TYPES dictionary with required and optional inputs.
        """
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "image": ("IMAGE", {"lazy": True}),
                "dit": ("SEEDVR2_DIT", {"lazy": True}),
                "vae": ("SEEDVR2_VAE", {"lazy": True}),
            }
        }

    RETURN_TYPES = ("IMAGE", "SEEDVR2_DIT", "SEEDVR2_VAE")
    RETURN_NAMES = ("image", "dit", "vae")
    FUNCTION = "gate"
    CATEGORY = "TA Nodes"

    def check_lazy_status(self, enabled, image=None, dit=None, vae=None):
        """
        Determines which lazy inputs to request based on the enabled state.

        Called by ComfyUI during graph planning. Returns input names only when
        enabled=True, causing upstream nodes to execute. When enabled=False,
        returns empty list to skip all upstream execution entirely.

        Args:
        enabled (bool): Gate toggle state.
        image, dit, vae: Ignored; placeholders for lazy inputs.

        Returns:
        list: List of input names to request, or empty list to skip.
        """
        # Only request the inputs if the gate is enabled.
        # When enabled=False, ComfyUI skips all upstream nodes entirely.
        if enabled:
            return ["image", "dit", "vae"]
        return []

    def gate(self, enabled, image=None, dit=None, vae=None):
        """
        Passes inputs through when enabled, or returns blockers when disabled.

        Main execution method. Returns real inputs for normal workflow flow or
        ExecutionBlocker placeholders that prevent downstream execution.

        Args:
        enabled (bool): Gate toggle state.
        image: IMAGE tensor (lazy).
        dit: SEEDVR2_DIT model (lazy).
        vae: SEEDVR2_VAE model (lazy).

        Returns:
        tuple: (image, dit, vae) or (blocker, blocker, blocker).
        """
        if not enabled:
            blocker = ExecutionBlocker(None)
            return (blocker, blocker, blocker)
        return (image, dit, vae)


NODE_CLASS_MAPPINGS = {
    "TASeedVR2Gate": TASeedVR2Gate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TASeedVR2Gate": "TA SeedVR2 Gate v2.0"
}

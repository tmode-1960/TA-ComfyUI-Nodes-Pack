"""
================================================================================
Node Name   : TAFastLaplacianSharpen
Created     : 2026-10-01
Modified    : 2026-10-01
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 1.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0
Description:
    Fast Laplacian sharpen for IMAGE tensors (RGB or RGBA). CPU by default,
    optional GPU. Alpha channel is preserved and NOT sharpened — only the RGB
    components are processed with a 3x3 Laplacian kernel. Works with Qwen
    Image, FLUX, SDXL and other pipelines that emit RGBA.
Changelog:
    1.0   2026-10-01  Initial implementation
================================================================================
"""

from typing import Tuple

import numpy as np
import torch
import torch.nn.functional as F
import comfy.model_management


# 3x3 Laplacian kernel (second derivative, 4-cross, no diagonal weighting)
LAPLACIAN_KERNEL = np.array(
    [[0, -1, 0],
     [-1, 4, -1],
     [0, -1, 0]],
    dtype=np.float32,
)


class TAFastLaplacianSharpen:
    """
    Fast Laplacian sharpen node for ComfyUI IMAGE tensors.

    Applies a single-tap 3x3 Laplacian (cross) filter per color channel and
    adds a user-defined strength to the original. The result is clipped to
    [0..1]. The alpha channel (if present) is left untouched.

    Two processing paths:
    - CPU path  (default): numpy-based convolution, works on any hardware.
    - GPU path  (opt-in) : torch F.conv2d with groups=3 on RGB, then
                          re-attached alpha. Uses ComfyUI's torch device.

    The node is channel-count agnostic for 3 (RGB) and 4 (RGBA) inputs,
    which is required for pipelines like Qwen-Image that emit RGBA.
    """

    CATEGORY = "TA Nodes/Enhancement"
    FUNCTION = "apply_laplacian"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images":   ("IMAGE",),
                "strength": ("FLOAT",
                             {"default": 0.5, "min": 0.0, "max": 2.0, "step": 0.01}),
                "use_gpu":  ("BOOLEAN", {"default": False}),
            },
        }

    def apply_laplacian(
        self,
        images: torch.Tensor,
        strength: float,
        use_gpu: bool,
    ) -> Tuple[torch.Tensor]:
        """
        Apply Laplacian sharpen to a batch of IMAGE tensors.

        Args:
            images    : ComfyUI IMAGE tensor, shape (B, H, W, C) with C in {3, 4}.
            strength  : Sharpen strength added on top of the original.
                        0.0 returns the input unchanged (after clip).
            use_gpu   : If True, run on the ComfyUI torch device; otherwise CPU.

        Returns:
            Tuple[torch.Tensor]: (sharpened_IMAGE_tensor,).
        """
        channels = images.shape[-1]
        if channels not in (3, 4):
            raise ValueError(
                f"TAFastLaplacianSharpen erwartet RGB oder RGBA, "
                f"bekommen: {channels} Kanale"
            )

        if use_gpu:
            return self._apply_gpu(images, strength, channels)
        return self._apply_cpu(images, strength, channels)

    # ------------------------------------------------------------------
    # GPU path
    # ------------------------------------------------------------------
    def _apply_gpu(self, images: torch.Tensor, strength: float, channels: int):
        device = comfy.model_management.get_torch_device()

        # (B, H, W, C) -> (B, C, H, W)
        x = images.to(device=device, dtype=torch.float32).permute(0, 3, 1, 2)

        # Split alpha if present; only sharpen RGB (3 channels).
        if channels == 4:
            alpha = x[:, 3:4]
            rgb   = x[:, :3]
        else:
            alpha = None
            rgb   = x

        kernel = torch.tensor(LAPLACIAN_KERNEL,
                              dtype=rgb.dtype, device=device).expand(3, 1, 3, 3)

        edges = F.conv2d(rgb, kernel, padding=1, groups=3)
        out   = (rgb + strength * edges).clamp(0.0, 1.0)

        if alpha is not None:
            out = torch.cat((out, alpha), dim=1)

        # (B, C, H, W) -> (B, H, W, C) and move back to the intermediate device
        # ComfyUI uses to feed downstream nodes.
        out = out.permute(0, 2, 3, 1)
        return (out.to(comfy.model_management.intermediate_device()),)

    # ------------------------------------------------------------------
    # CPU path (default)
    # ------------------------------------------------------------------
    def _apply_cpu(self, images: torch.Tensor, strength: float, channels: int):
        if images.is_cuda:
            images = images.cpu()

        img = images.contiguous().numpy().astype(np.float32)  # (B, H, W, C)

        # Split alpha if present; only sharpen RGB.
        if channels == 4:
            alpha = img[..., 3:4]
            rgb   = img[..., :3]
        else:
            alpha = None
            rgb   = img

        # Edge padding keeps RGB at same HxW after the 3x3 convolution.
        p = np.pad(rgb,
                   pad_width=((0, 0), (1, 1), (1, 1), (0, 0)),
                   mode="edge")

        lap = (
            p[:, 1:-1, 0:-2] +
            p[:, 0:-2, 1:-1] +
            p[:, 2:  , 1:-1] +
            p[:, 1:-1, 2:  ] -
            4.0 * rgb
        )

        out = rgb + strength * lap
        np.clip(out, 0.0, 1.0, out=out)

        if alpha is not None:
            out = np.concatenate((out, alpha), axis=-1)

        return (torch.from_numpy(out),)


NODE_CLASS_MAPPINGS = {
    "TAFastLaplacianSharpen": TAFastLaplacianSharpen,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TAFastLaplacianSharpen": "🌀 TA Fast Laplacian Sharpen",
}

"""
================================================================================
Node Name   : TA Latent Preview
Created     : 2026-03-07
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Displays a LATENT tensor as a preview image directly inside the node using
    the latent2rgb projection. Requires no VAE and no TAESD — runs on any
    hardware. Output format is identical to ComfyUI's built-in PreviewImage node.
================================================================================
"""

import os
import uuid
import torch
import numpy as np
from PIL import Image
import folder_paths


# latent2rgb weights (ComfyUI LatentToRGB, supports 4- and 16-channel latents)
LATENT_RGB_FACTORS = [
    #   R        G        B
    [ 0.3512,  0.2946,  0.3430],
    [ 0.3037,  0.2151,  0.2835],
    [ 0.3172,  0.2827,  0.3164],
    [ 0.2775,  0.2775,  0.3310],
    [-0.0472,  0.0621,  0.0905],
    [-0.1543, -0.0937, -0.1290],
    [-0.0598, -0.0478, -0.0453],
    [ 0.0440,  0.0839,  0.0759],
    [-0.1225,  0.0110,  0.0543],
    [ 0.0507,  0.0873,  0.0775],
    [-0.0219,  0.0022,  0.0046],
    [-0.0275,  0.0270,  0.0206],
    [-0.0315, -0.0072, -0.0001],
    [ 0.0077,  0.0091,  0.0076],
    [-0.0218, -0.0125, -0.0162],
    [ 0.0124,  0.0052,  0.0074],
]

BIAS = [0.5006, 0.4229, 0.4572]


def latent_to_pil(latent_samples: torch.Tensor) -> list:
    """
    Converts a batch of latent tensors to a list of PIL RGB images using the
    latent2rgb projection matrix.

    Applies LATENT_RGB_FACTORS and BIAS to project each latent frame from
    latent space into approximate RGB colour space without requiring a VAE.
    Supports both 4-channel (standard SD/SDXL) and 16-channel (SD3 / Flux)
    latents by slicing the factor matrix to match the channel count.

    Args:
        latent_samples (torch.Tensor): Latent batch tensor with shape (B, C, H, W).

    Returns:
        list[Image.Image]: List of B PIL RGB images, one per batch entry.
    """
    s = latent_samples.cpu().float()
    b, c, h, w = s.shape

    factors = torch.tensor(LATENT_RGB_FACTORS[:c], dtype=torch.float32)  # (C, 3)
    bias    = torch.tensor(BIAS,                   dtype=torch.float32)   # (3,)

    s   = s.permute(0, 2, 3, 1)                        # (B, H, W, C)
    rgb = (s @ factors + bias).clamp(0.0, 1.0)         # (B, H, W, 3)

    images = []
    for i in range(b):
        arr = (rgb[i].numpy() * 255).astype(np.uint8)
        images.append(Image.fromarray(arr, "RGB"))
    return images


class TALatentPreview:
    """
    Displays a LATENT tensor as a preview image directly inside the ComfyUI node.

    Uses the latent2rgb projection matrix — no VAE decoder and no TAESD model
    are required, so the node runs on any hardware configuration. The UI output
    format (temp PNG files with filename/subfolder/type dict) is identical to
    ComfyUI's built-in PreviewImage node, ensuring full frontend compatibility.

    Also outputs the projected RGB data as a standard IMAGE tensor (B, H, W, 3)
    in float [0..1] range for optional use in downstream workflow nodes.
    """

    CATEGORY     = "TA Nodes/Sampling"
    FUNCTION     = "preview"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    OUTPUT_NODE  = True

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with the required LATENT input.
        """
        return {
            "required": {
                "latent": ("LATENT",),
            },
        }

    def preview(self, latent):
        """
        Projects the input latent tensor to RGB, saves preview PNGs to the
        ComfyUI temp directory, and returns both UI image references and an
        IMAGE tensor for downstream nodes.

        For each image in the batch a uniquely named PNG is written to the
        ComfyUI temp directory and registered in the 'ui' return dict so the
        frontend can display it inside the node. The same RGB projection is
        also returned as a float IMAGE tensor (B, H, W, 3) via 'result'.

        Args:
            latent (dict): ComfyUI LATENT dict containing a 'samples' key with
                           a tensor of shape (B, C, H, W).

        Returns:
            dict: ComfyUI combined UI + result dict:
                  - 'ui':     {'images': [{'filename', 'subfolder', 'type'}, ...]}
                  - 'result': tuple containing the IMAGE tensor (B, H, W, 3) float [0..1].
        """
        samples   = latent["samples"]          # (B, C, H, W)
        pil_imgs  = latent_to_pil(samples)

        temp_dir  = folder_paths.get_temp_directory()
        os.makedirs(temp_dir, exist_ok=True)

        ui_images = []
        for img in pil_imgs:
            filename = f"ta_latent_preview_{uuid.uuid4().hex[:12]}.png"
            filepath = os.path.join(temp_dir, filename)
            img.save(filepath, compress_level=1)
            ui_images.append({
                "filename":  filename,
                "subfolder": "",
                "type":      "temp",
            })

        # IMAGE tensor for downstream workflow nodes: (B, H, W, 3) float [0..1]
        s       = samples.cpu().float()
        b, c, h, w = s.shape
        factors = torch.tensor(LATENT_RGB_FACTORS[:c], dtype=torch.float32)
        bias    = torch.tensor(BIAS,                   dtype=torch.float32)
        rgb     = (s.permute(0, 2, 3, 1) @ factors + bias).clamp(0.0, 1.0)

        return {"ui": {"images": ui_images}, "result": (rgb,)}


# ---------------------------------------------------------------------------
# Node Registration
# ---------------------------------------------------------------------------


NODE_CLASS_MAPPINGS = {
    "TALatentPreview": TALatentPreview,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TALatentPreview": "🖼️ TA Latent Preview",
}
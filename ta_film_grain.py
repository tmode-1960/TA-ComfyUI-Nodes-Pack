"""
================================================================================
Node Name   : TAFilmGrain
Created     : 2026-11-13
Modified    : 2026-11-13
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 1.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0
Description:
    Self-contained Film Grain node for IMAGE tensors (RGB or RGBA).
    1:1 parameter-compatible with ProPostFilmGrain without external
    filmgrainer package imports (avoids namespace collisions). Alpha channel
    is preserved untouched.
Changelog:
    1.0   2026-11-13  Initial implementation
================================================================================
"""

from typing import Tuple

import numpy as np
import torch
from PIL import Image, ImageFilter


GRAIN_PROFILES = {
    "Fine":        (0.80, 0.25),
    "Fine Simple": (1.00, 0.18),
    "Coarse":      (1.60, 0.30),
    "Coarser":     (2.40, 0.36),
}


class TAFilmGrain:
    """
    Self-contained Film Grain node for ComfyUI IMAGE tensors.

    Applies organic luminance/chrominance film grain with shadow/highlight
    response, gamma shaping, optional grayscale conversion, and optional
    post-grain sharpening. Supports 3-channel (RGB) and 4-channel (RGBA)
    tensors; alpha is preserved unchanged.
    """

    CATEGORY = "TA Nodes/Enhancement"
    FUNCTION = "apply_filmgrain"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image":       ("IMAGE",),
                "gray_scale":  ("BOOLEAN", {"default": False}),
                "grain_type":  (["Fine", "Fine Simple", "Coarse", "Coarser"],),
                "grain_sat":   ("FLOAT", {"default": 0.15, "min": 0.0, "max": 1.0,  "step": 0.01}),
                "grain_power": ("FLOAT", {"default": 0.40, "min": 0.0, "max": 1.0,  "step": 0.01}),
                "shadows":     ("FLOAT", {"default": 0.20, "min": 0.0, "max": 1.0,  "step": 0.01}),
                "highs":       ("FLOAT", {"default": 0.20, "min": 0.0, "max": 1.0,  "step": 0.01}),
                "scale":       ("FLOAT", {"default": 0.65, "min": 0.0, "max": 10.0, "step": 0.01}),
                "sharpen":     ("INT",   {"default": 0,    "min": 0,   "max": 10}),
                "src_gamma":   ("FLOAT", {"default": 1.0,  "min": 0.0, "max": 10.0, "step": 0.01}),
                "seed":        ("INT",   {"default": 1,    "min": 1,   "max": 18446744073709551615}),
            },
        }

    def apply_filmgrain(
        self,
        image: torch.Tensor,
        gray_scale: bool,
        grain_type: str,
        grain_sat: float,
        grain_power: float,
        shadows: float,
        highs: float,
        scale: float,
        sharpen: int,
        src_gamma: float,
        seed: int,
    ) -> Tuple[torch.Tensor]:
        """
        Apply film grain to a batch of IMAGE tensors.

        Args:
            image       : ComfyUI IMAGE tensor, shape (B, H, W, C) with C in {3, 4}.
            gray_scale  : Convert RGB to grayscale before adding grain.
            grain_type  : Grain profile ("Fine", "Fine Simple", "Coarse", "Coarser").
            grain_sat   : Color saturation of the grain (0.0 = monochrome, 1.0 = full RGB).
            grain_power : Overall grain intensity [0..1].
            shadows     : Grain response in shadow areas [0..1].
            highs       : Grain response in highlight areas [0..1].
            scale       : Grain size scale factor.
            sharpen     : Optional post-grain sharpen passes [0..10].
            src_gamma   : Source gamma curve applied to luminance response.
            seed        : Base random seed (incremented per batch item).

        Returns:
            Tuple[torch.Tensor]: (grained_IMAGE_tensor,).
        """
        channels = image.shape[-1]
        if channels not in (3, 4):
            raise ValueError(
                f"TAFilmGrain erwartet RGB oder RGBA, bekommen: {channels} Kanale"
            )

        src = image.cpu() if image.is_cuda else image
        img_np = src.contiguous().numpy().astype(np.float32)
        batch_size, height, width, _ = img_np.shape
        out_np = np.empty_like(img_np)

        grain_size_mult, profile_amp = GRAIN_PROFILES.get(grain_type, (1.0, 0.25))
        eff_scale = max(0.25, float(scale) * grain_size_mult)
        gamma_val = max(0.05, float(src_gamma))

        for b in range(batch_size):
            frame = np.clip(img_np[b], 0.0, 1.0)
            if channels == 4:
                rgb = frame[..., :3]
                alpha = frame[..., 3:4]
            else:
                rgb = frame
                alpha = None

            if gray_scale:
                luma = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2])[..., None]
                rgb = np.repeat(luma, 3, axis=-1)

            if grain_power > 0.0:
                rng = np.random.default_rng((int(seed) + b) & 0xFFFFFFFFFFFFFFFF)
                noise_w = max(1, int(round(width / eff_scale)))
                noise_h = max(1, int(round(height / eff_scale)))

                mono_noise = rng.normal(0.0, 1.0, (noise_h, noise_w, 1)).astype(np.float32)
                color_noise = rng.normal(0.0, 1.0, (noise_h, noise_w, 3)).astype(np.float32)
                sat = float(np.clip(grain_sat, 0.0, 1.0))
                raw_noise = (1.0 - sat) * mono_noise + sat * color_noise

                if noise_w != width or noise_h != height:
                    resized_ch = []
                    for c in range(3):
                        ch_img = Image.fromarray(raw_noise[..., c], mode="F")
                        ch_res = ch_img.resize((width, height), resample=Image.BILINEAR)
                        resized_ch.append(np.asarray(ch_res, dtype=np.float32))
                    noise = np.stack(resized_ch, axis=-1)
                else:
                    noise = raw_noise

                lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
                if abs(gamma_val - 1.0) > 1e-4:
                    lum_g = np.power(np.clip(lum, 0.0, 1.0), 1.0 / gamma_val)
                else:
                    lum_g = lum

                mid_weight = 4.0 * lum_g * (1.0 - lum_g)
                shadow_weight = (1.0 - lum_g) ** 2 * float(shadows) * 2.0
                high_weight = (lum_g ** 2) * float(highs) * 2.0
                mask = np.clip(mid_weight + shadow_weight + high_weight, 0.0, 1.5)[..., None]

                amp = float(grain_power) * profile_amp
                rgb = np.clip(rgb + noise * amp * mask, 0.0, 1.0)

            if sharpen > 0:
                pil_rgb = Image.fromarray((rgb * 255.0).astype(np.uint8), mode="RGB")
                for _ in range(int(sharpen)):
                    pil_rgb = pil_rgb.filter(ImageFilter.SHARPEN)
                rgb = np.asarray(pil_rgb, dtype=np.float32) / 255.0

            if alpha is not None:
                out_np[b] = np.concatenate((rgb, alpha), axis=-1)
            else:
                out_np[b] = rgb

        return (torch.from_numpy(out_np),)


NODE_CLASS_MAPPINGS = {
    "TAFilmGrain": TAFilmGrain,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TAFilmGrain": "🎞️ TA Film Grain",
}

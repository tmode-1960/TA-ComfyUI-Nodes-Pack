"""
================================================================================
Node Name   : TA KSampler
Created     : 2026-03-07
Modified    : 2026-03-14
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.1
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Advanced KSampler node that accepts sampler_name and scheduler as plain
    STRING inputs, making it directly connectable to the TA Sampler Preset node.
    Provides per-step live latent2rgb preview via pbar.update_absolute(),
    identical in behaviour to ComfyUI's built-in KSampler preview.
================================================================================
"""

import struct
import torch
import numpy as np
from PIL import Image

import comfy.sample
import comfy.samplers
import comfy.utils
import latent_preview


# ── latent2rgb conversion factors (ComfyUI Latent2RGBPreviewer, 4+16 channel) ─
_FACTORS_RAW = [
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
_BIAS = [0.5006, 0.4229, 0.4572]


def _latent_to_pil(latent_tensor: torch.Tensor) -> Image.Image:
    """
    Converts a single latent frame tensor to a PIL RGB image.

    Applies the ComfyUI latent2rgb matrix (_FACTORS_RAW) and bias (_BIAS) to
    project the latent channels into RGB colour space. The result is upscaled
    to at least 512 px on the longest side using Lanczos resampling if the
    raw decoded image is smaller.

    Handles both standard (C, H, W) latents and FLUX.2 Klein packed 2D latents
    delivered as (H*W, C) by reshaping them to (C, H, W) before conversion.

    Args:
        latent_tensor (torch.Tensor): Single latent frame, either (C, H, W)
                                      or packed (H*W, C) as from FLUX.2 Klein.

    Returns:
        Image.Image: RGB PIL image, upscaled to at least 512 px on the longest side.
    """
    s = latent_tensor.cpu().float()

    # Guard: must be (C, H, W) at this point
    if s.dim() != 3:
        raise ValueError(f"_latent_to_pil expects 3D tensor (C, H, W), got shape {tuple(s.shape)}")

    c = s.shape[0]

    factors = torch.tensor(_FACTORS_RAW[:c], dtype=torch.float32)   # (C, 3)
    bias    = torch.tensor(_BIAS,            dtype=torch.float32)    # (3,)

    # (C, H, W) → (H, W, C) → (H, W, 3)
    rgb = (s.permute(1, 2, 0) @ factors + bias).clamp(0.0, 1.0)
    arr = (rgb.numpy() * 255).astype(np.uint8)
    img = Image.fromarray(arr, "RGB")

    # Upscale to at least 512 px on the longest side (Lanczos)
    w, h   = img.size
    target = 512
    if max(w, h) < target:
        scale = target / max(w, h)
        img   = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    return img


def _make_step_callback(model, steps: int):
    """
    Builds a sampling callback that sends a latent2rgb preview to the ComfyUI
    frontend after every denoising step via pbar.update_absolute().

    Behaviour is identical to latent_preview.prepare_callback(). Supports both
    standard 4D latents (B, C, H, W) and 5D video/Qwen latents (B, C, F, H, W)
    by normalising the tensor to (C, H, W) before conversion.

    Preview errors are caught silently so they never interrupt the sampling
    process; the progress bar still advances even if the preview fails.

    Args:
        model:      The ComfyUI model object (used for ProgressBar context).
        steps (int): Total number of sampling steps; used to initialise the
                     progress bar.

    Returns:
        callable: A callback function with the signature
                  callback(step, x0, x, total_steps).
    """
    pbar = comfy.utils.ProgressBar(steps)

    # Read the preview format from ComfyUI CLI settings (JPEG / PNG).
    preview_format = "JPEG"
    try:
        from comfy.cli_args import args as _cli_args
        fmt = getattr(_cli_args, "preview_format", "JPEG")
        if fmt in ("JPEG", "PNG"):
            preview_format = fmt
    except Exception:
        pass

    preview_failed = [False]  # mutable flag accessible inside closure

    def callback(step, x0, x, total_steps):
        # x0: denoised latent after this step, shape (B, C, H, W)
        if preview_failed[0]:
            pbar.update_absolute(step + 1, total_steps, None)
            return
        try:
            # Normalise shape to (C, H, W):
            # Standard 4D:        (B, C, H, W)       → x0[0]           e.g. FLUX Dev
            # Video / Qwen 5D:    (B, C, F, H, W)    → x0[0, :, 0, :, :]
            # FLUX.2 Klein 3D:    (B, tokens, C)      → depatchify to (C, H, W)
            if x0.dim() == 5:
                frame = x0[0, :, 0, :, :]           # (C, H, W)
            elif x0.dim() == 4:
                frame = x0[0]                        # (C, H, W)
            elif x0.dim() == 3:
                seq = x0[0]                          # (tokens, C)
                tokens, c = seq.shape
                found = False
                for h in range(int(tokens ** 0.5) + 1, 0, -1):
                    if tokens % h == 0:
                        w = tokens // h
                        if 0.25 <= h / w <= 4.0:
                            frame = seq.reshape(h, w, c).permute(2, 0, 1)  # (C, H, W)
                            found = True
                            break
                if not found:
                    pbar.update_absolute(step + 1, total_steps, None)
                    return
            else:
                frame = x0                           # fallback
            preview_img = _latent_to_pil(frame)
            pbar.update_absolute(step + 1, total_steps, ("JPEG", preview_img, None))
        except Exception as e:
            # On first failure: log once and disable preview for remaining steps.
            print(f"[TAKSampler] Preview not supported for this model "
                  f"(step {step+1}: {type(e).__name__}: {e}) — disabling preview.")
            preview_failed[0] = True
            pbar.update_absolute(step + 1, total_steps, None)

    return callback


class TAKSampler:
    """
    Advanced KSampler that accepts sampler_name and scheduler as plain STRING
    inputs instead of COMBO dropdowns, making it directly connectable to the
    TA Sampler Preset node.

    Provides per-step live latent2rgb preview via pbar.update_absolute(),
    identical in behaviour to ComfyUI's built-in KSampler preview. Preview can
    be toggled on/off via the 'preview' boolean input.
    """

    CATEGORY     = "TA Nodes/Sampling"
    FUNCTION     = "sample"
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with all required inputs.
        """
        return {
            "required": {
                "model":          ("MODEL",),
                "add_noise":      (["enable", "disable"], {"default": "enable"}),
                "noise_seed":     ("INT", {
                    "default": 0, "min": 0, "max": 0xffffffffffffffff,
                    "control_after_generate": True,
                }),
                "steps":          ("INT",   {"default": 20,  "min": 1,   "max": 200}),
                "cfg":            ("FLOAT", {"default": 7.0, "min": 0.0, "max": 30.0, "step": 0.1}),
                "sampler_name":   ("STRING", {
                    "default": "euler",
                    "tooltip": "e.g. euler, euler_ancestral, dpmpp_2m, dpmpp_sde …",
                }),
                "scheduler":      ("STRING", {
                    "default": "normal",
                    "tooltip": "e.g. normal, karras, exponential, simple, beta …",
                }),
                "positive":       ("CONDITIONING",),
                "negative":       ("CONDITIONING",),
                "latent_image":   ("LATENT",),
                "start_at_step":  ("INT", {"default": 0,    "min": 0, "max": 10000}),
                "end_at_step":    ("INT", {"default": 9999, "min": 0, "max": 99999}),
                "return_with_leftover_noise": (["disable", "enable"], {"default": "disable"}),
                "preview": ("BOOLEAN", {"default": True, "label_on": "true", "label_off": "false"}),
            },
        }

    def sample(
        self,
        model,
        add_noise,
        noise_seed,
        steps,
        cfg,
        sampler_name,
        scheduler,
        positive,
        negative,
        latent_image,
        start_at_step,
        end_at_step,
        return_with_leftover_noise,
        preview,
    ):
        """
        Executes the sampling process and returns the resulting latent tensor.

        Validates the sampler_name and scheduler strings against ComfyUI's
        registered values, falling back to safe defaults ('euler' / 'normal')
        if an unknown value is provided. Builds the noise tensor, optional noise
        mask, and step callback, then delegates to comfy.sample.sample().

        Args:
            model:                      ComfyUI MODEL object.
            add_noise (str):            'enable' to add noise; 'disable' for a
                                        zero noise tensor (useful for img2img).
            noise_seed (int):           RNG seed for reproducible noise generation.
            steps (int):                Total number of denoising steps.
            cfg (float):                Classifier-free guidance scale.
            sampler_name (str):         Name of the sampler algorithm, e.g. 'euler'.
                                        Falls back to 'euler' if not recognised.
            scheduler (str):            Name of the noise scheduler, e.g. 'karras'.
                                        Falls back to 'normal' if not recognised.
            positive:                   Positive CONDITIONING tensor.
            negative:                   Negative CONDITIONING tensor.
            latent_image (dict):        Input LATENT dict containing 'samples' and
                                        optionally 'batch_index' and 'noise_mask'.
            start_at_step (int):        Step index at which to begin sampling
                                        (0 = from the start).
            end_at_step (int):          Step index at which to stop sampling
                                        (9999 = run to completion).
            return_with_leftover_noise (str):
                                        'enable' to keep residual noise in the
                                        output; 'disable' for a fully denoised result.
            preview (bool):             If True, sends latent2rgb previews to the
                                        ComfyUI frontend after each step. If False,
                                        falls back to the standard ComfyUI callback.

        Returns:
            tuple: Single-element tuple containing the output LATENT dict with
                   the sampled 'samples' tensor.
        """
        # ── Validation ─────────────────────────────────────────────────────
        available_samplers   = comfy.samplers.KSampler.SAMPLERS
        available_schedulers = comfy.samplers.KSampler.SCHEDULERS

        if sampler_name not in available_samplers:
            print(f"[TAKSampler] ⚠️ Unknown sampler_name '{sampler_name}', "
                  f"using 'euler'. Available: {available_samplers}")
            sampler_name = "euler"

        if scheduler not in available_schedulers:
            print(f"[TAKSampler] ⚠️ Unknown scheduler '{scheduler}', "
                  f"using 'normal'. Available: {available_schedulers}")
            scheduler = "normal"

        # ── Flags ──────────────────────────────────────────────────────────
        disable_noise      = (add_noise == "disable")
        force_full_denoise = (return_with_leftover_noise == "disable")
        start_step         = start_at_step if start_at_step > 0   else None
        last_step          = end_at_step   if end_at_step  < 9999 else None

        # ── Prepare latent ─────────────────────────────────────────────────
        latent      = latent_image.copy()
        latent_data = latent["samples"]
        latent_data = comfy.sample.fix_empty_latent_channels(model, latent_data)

        # ── Noise ──────────────────────────────────────────────────────────
        if disable_noise:
            noise = torch.zeros(
                latent_data.size(),
                dtype=latent_data.dtype,
                layout=latent_data.layout,
                device="cpu",
            )
        else:
            batch_inds = latent.get("batch_index", None)
            noise      = comfy.sample.prepare_noise(latent_data, noise_seed, batch_inds)

        noise_mask   = latent.get("noise_mask", None)

        # ── Callback with live preview ──────────────────────────────────────
        callback     = _make_step_callback(model, steps) if preview else latent_preview.prepare_callback(model, steps)
        disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED

        # ── Sampling ───────────────────────────────────────────────────────
        samples = comfy.sample.sample(
            model,
            noise,
            steps,
            cfg,
            sampler_name,
            scheduler,
            positive,
            negative,
            latent_data,
            denoise            = 1.0,
            disable_noise      = disable_noise,
            start_step         = start_step,
            last_step          = last_step,
            force_full_denoise = force_full_denoise,
            noise_mask         = noise_mask,
            callback           = callback,
            disable_pbar       = disable_pbar,
            seed               = noise_seed,
        )

        latent["samples"] = samples
        return (latent,)


# ---------------------------------------------------------------------------
# Node Registration
# ---------------------------------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "TAKSampler": TAKSampler,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TAKSampler": "⚡ TA KSampler",
}

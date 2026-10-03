"""
================================================================================
Node Name   : TA SageAttention Toggler
Created     : 2025
Modified    : 2026-10-02
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.2
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0
Description:
    Patches a ComfyUI MODEL with an attention kernel and/or PyTorch FP16
    matmul acceleration. The attention engine is selected via mutually
    exclusive (XOR) toggles: SageAttention (all five ComfyUI-KJNodes modes:
    auto, qk_int8_pv_fp16_cuda, qk_int8_pv_fp16_triton, qk_int8_pv_fp8_cuda,
    qk_fp8_pv_fp8_cuda) or comfy-kitchen int8_attention. torch_enable is
    independent of the attention engine choice.
Changelog:
    2.2  2026-10-02  kitchen_enable Toggle (comfy-kitchen int8_attention)
================================================================================
"""

import torch
import logging
from comfy.model_management import soft_empty_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TA_SageAttentionToggler")

# Node mappings correctly reference the class
NODE_CLASS_MAPPINGS = {"TASageAttentionToggler": "TASageAttentionToggler"}
NODE_DISPLAY_NAME_MAPPINGS = {"TASageAttentionToggler": "🔧 TA SageAttention Toggler"}


class TASageAttentionToggler:
    """
    Applies an attention kernel and/or a PyTorch FP16 matmul patch to a MODEL.

    SageAttention and comfy-kitchen int8_attention are mutually exclusive:
    enabling both simultaneously raises a ValueError at sampling time. Exactly
    one (or neither) may be active. The FP16 matmul patch (torch_enable) is
    independent and can be combined with either engine.

    SageAttention replaces the standard attention function with a quantised
    CUDA/Triton kernel. comfy-kitchen provides an INT8 attention kernel
    (ck.int8_attention) backed by the comfy_kitchen dispatch system
    (hip/cuda/triton/eager backends).

    Both attention engines are optional; torch_enable is optional too.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Inputs:
            model:          The ComfyUI MODEL to patch.
            sage_enable:    Toggle to apply the SageAttention patch.
                            Mutually exclusive with kitchen_enable.
            torch_enable:   Toggle to apply the FP16 matmul patch.
                            Independent of the attention engine choice.
            sage_mode:      Selects the SageAttention kernel variant.
                            'auto' uses the default sageattn() entry point;
                            the other options select specific quantisation
                            configurations (CUDA or Triton backends).
            kitchen_enable: Toggle to apply the comfy-kitchen int8_attention
                            patch. Mutually exclusive with sage_enable.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with all required inputs.
        """
        return {
            "required": {
                "model": ("MODEL",),
                "sage_enable": ("BOOLEAN", {"default": True, "label_on": "✅ Sage ON", "label_off": "❌ OFF"}),
                "torch_enable": ("BOOLEAN", {"default": True, "label_on": "✅ Torch ON", "label_off": "❌ OFF"}),
                "sage_mode": ([
                    "auto",
                    "sageattn_qk_int8_pv_fp16_cuda",
                    "sageattn_qk_int8_pv_fp16_triton",
                    "sageattn_qk_int8_pv_fp8_cuda",
                    "sageattn_qk_fp8_pv_fp8_cuda"
                ], {"default": "auto"}),
                "kitchen_enable": ("BOOLEAN", {"default": False, "label_on": "✅ Kitchen ON", "label_off": "❌ OFF"}),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_patches"
    CATEGORY = "TA Smart LLM"

    def apply_patches(self, model, sage_enable, torch_enable, sage_mode, kitchen_enable):
        """
        Applies the selected patches to the model and returns the patched result.

        The attention engine (SageAttention or comfy-kitchen) is mutually
        exclusive: setting both sage_enable and kitchen_enable to True raises
        a ValueError. torch_enable is independent of the engine choice.

        If sage_enable is True, _apply_sage_patch() is called.
        If kitchen_enable is True, _apply_kitchen_patch() is called.
        If torch_enable is True, _apply_torch_patch() is called.
        All patches modify the model in-place and return it for chaining.

        Args:
            model:           ComfyUI MODEL object to patch.
            sage_enable (bool):   Whether to apply the SageAttention patch.
            torch_enable (bool):  Whether to apply the FP16 matmul patch.
            sage_mode (str):      SageAttention kernel variant to use.
            kitchen_enable (bool): Whether to apply the comfy-kitchen patch.

        Returns:
            tuple: Single-element tuple containing the patched MODEL object.

        Raises:
            ValueError: If both sage_enable and kitchen_enable are True.
        """
        logger.info(f"🚀 [TA] SageToggler START | Sage:{sage_enable} | Torch:{torch_enable} | Mode:{sage_mode} | Kitchen:{kitchen_enable}")

        if sage_enable and kitchen_enable:
            raise ValueError(
                "SageAttention und Comfort Kitchen sind exklusiv. "
                "Bitte nur eins aktivieren (sage_enable ODER kitchen_enable)."
            )

        patched_model = model

        applied = []

        if sage_enable:
            patched_model = self._apply_sage_patch(patched_model, sage_mode)
            applied.append(f"Sage({sage_mode})")

        if kitchen_enable:
            patched_model = self._apply_kitchen_patch(patched_model)
            applied.append("Kitchen(int8_attention)")

        if torch_enable:
            patched_model = self._apply_torch_patch(patched_model)
            applied.append("Torch FP16")

        if applied:
            logger.info(f"✅ [TA] Patches applied: {', '.join(applied)}")
        else:
            logger.info("⏭️ [TA] No patches applied – all toggles disabled, model passed through.")

        return (patched_model, )

    def _apply_sage_patch(self, model, sage_mode):
        """
        Patches the model with the specified SageAttention kernel.

        Imports the requested sageattention function and wraps it in a lambda
        that matches ComfyUI's attention call signature (q, k, v, is_causal,
        attn_mask, tensor_layout). The wrapped function is stored as
        model.sage_func and model.sage_active is set to True on success.

        If the sageattention package is not installed, model.sage_active is set
        to False and an installation hint is logged; the model is returned
        unmodified.

        Args:
            model:          ComfyUI MODEL object to patch.
            sage_mode (str): One of the five supported sage_mode strings.

        Returns:
            MODEL: The model with sage_func and sage_active attributes set.

        Raises:
            ValueError: If sage_mode is not one of the recognised mode strings.
        """
        logger.info(f"🔥 SageAttention PATCH: {sage_mode}")

        try:
            from sageattention import sageattn

            if sage_mode == "auto":
                sage_func = lambda q, k, v, is_causal=False, attn_mask=None, tensor_layout="NHD": \
                    sageattn(q, k, v, is_causal=is_causal, attn_mask=attn_mask, tensor_layout=tensor_layout)

            elif sage_mode == "sageattn_qk_int8_pv_fp16_cuda":
                from sageattention import sageattn_qk_int8_pv_fp16_cuda
                sage_func = lambda q, k, v, is_causal=False, attn_mask=None, tensor_layout="NHD": \
                    sageattn_qk_int8_pv_fp16_cuda(q, k, v, is_causal=is_causal, attn_mask=attn_mask,
                                                  pv_accum_dtype="fp32", tensor_layout=tensor_layout)

            elif sage_mode == "sageattn_qk_int8_pv_fp16_triton":
                from sageattention import sageattn_qk_int8_pv_fp16_triton
                sage_func = lambda q, k, v, is_causal=False, attn_mask=None, tensor_layout="NHD": \
                    sageattn_qk_int8_pv_fp16_triton(q, k, v, is_causal=is_causal, attn_mask=attn_mask,
                                                    tensor_layout=tensor_layout)

            elif sage_mode == "sageattn_qk_int8_pv_fp8_cuda":
                from sageattention import sageattn_qk_int8_pv_fp8_cuda
                sage_func = lambda q, k, v, is_causal=False, attn_mask=None, tensor_layout="NHD": \
                    sageattn_qk_int8_pv_fp8_cuda(q, k, v, is_causal=is_causal, attn_mask=attn_mask,
                                                 pv_accum_dtype="fp32+fp32", tensor_layout=tensor_layout)

            elif sage_mode == "sageattn_qk_fp8_pv_fp8_cuda":
                from sageattention import sageattn_qk_fp8_pv_fp8_cuda
                sage_func = lambda q, k, v, is_causal=False, attn_mask=None, tensor_layout="NHD": \
                    sageattn_qk_fp8_pv_fp8_cuda(q, k, v, is_causal=is_causal, attn_mask=attn_mask,
                                                tensor_layout=tensor_layout)

            else:
                raise ValueError(f"Unknown sage_mode: {sage_mode}")

            logger.info(f"✅ {sage_mode} loaded successfully!")
            model.sage_func = sage_func
            model.sage_active = True

        except ImportError as e:
            logger.error(f"❌ SageAttention import error: {e}")
            logger.info("💡 Install with: pip install sageattention-nightly")
            model.sage_active = False

        return model

    def _apply_kitchen_patch(self, model):
        """
        Patches the model with comfy-kitchen int8_attention.

        Imports comfy_kitchen.int8_attention and wraps it in a lambda that
        matches ComfyUI's attention call signature (q, k, v, is_causal,
        attn_mask, tensor_layout). The wrapped function is stored as
        model.kitchen_func and model.kitchen_active is set to True on success.

        If the comfy_kitchen package is not installed, model.kitchen_active
        is set to False and an installation hint is logged.

        Args:
            model: ComfyUI MODEL object to patch.

        Returns:
            MODEL: The model with kitchen_func and kitchen_active set.
        """
        logger.info(f"🔥 comfy-kitchen PATCH")

        try:
            from comfy_kitchen import int8_attention as ck_int8_attn

            kitchen_func = lambda q, k, v, is_causal=False, attn_mask=None, tensor_layout="NHD": \
                ck_int8_attn(q, k, v, is_causal=is_causal, attn_mask=attn_mask, tensor_layout=tensor_layout)

            logger.info(f"✅ comfy_kitchen int8_attention loaded successfully!")
            model.kitchen_func = kitchen_func
            model.kitchen_active = True

        except ImportError as e:
            logger.error(f"❌ comfy_kitchen import error: {e}")
            logger.info("💡 Install with: pip install comfy-kitchen")
            model.kitchen_active = False

        return model

    def _apply_torch_patch(self, model):
        """
        Enables PyTorch FP16 matmul accumulation on the CUDA backend.

        Sets torch.backends.cuda.matmul.allow_fp16_accumulation to True if the
        attribute is available (requires PyTorch Nightly 2.7+). The previous
        value is logged for reference. Registers _restore_torch as a callback
        on model._torch_callbacks if that attribute exists, and sets
        model.torch_patched = True.

        Args:
            model: ComfyUI MODEL object to patch.

        Returns:
            MODEL: The model with torch_patched set to True.
        """
        logger.info("🔥 Torch Backend PATCH")

        original_fp16 = None
        if hasattr(torch.backends.cuda.matmul, 'allow_fp16_accumulation'):
            original_fp16 = torch.backends.cuda.matmul.allow_fp16_accumulation
            torch.backends.cuda.matmul.allow_fp16_accumulation = True
            logger.info(f"✅ FP16 Matmul enabled (previously: {original_fp16})")
        else:
            logger.warning("⚠️ PyTorch Nightly 2.7+ required for FP16 Matmul")

        if hasattr(model, '_torch_callbacks'):
            model._torch_callbacks.append(self._restore_torch)

        model.torch_patched = True
        return model

    def _restore_torch(self):
        """
        Restores the PyTorch FP16 matmul accumulation setting to False and
        flushes the VRAM cache via soft_empty_cache().

        Intended to be registered as a teardown callback on the model so that
        the global torch backend setting is not left enabled after sampling.
        """
        if hasattr(torch.backends.cuda.matmul, 'allow_fp16_accumulation'):
            torch.backends.cuda.matmul.allow_fp16_accumulation = False
        logger.info("🔄 Torch Backend restored")
        soft_empty_cache()

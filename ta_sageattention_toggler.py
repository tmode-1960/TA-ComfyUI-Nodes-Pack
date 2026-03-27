"""
================================================================================
Node Name   : TA SageAttention Toggler
Created     : 2025
Modified    : 2026-03-27
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.1
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Patches a ComfyUI MODEL with SageAttention and/or PyTorch FP16 matmul
    acceleration. Exposes all five SageAttention modes available in
    ComfyUI-KJNodes: auto, qk_int8_pv_fp16_cuda, qk_int8_pv_fp16_triton,
    qk_int8_pv_fp8_cuda, and qk_fp8_pv_fp8_cuda.
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
    Applies SageAttention and/or PyTorch FP16 matmul patches to a MODEL.

    SageAttention replaces the standard attention function with a quantised
    CUDA/Triton kernel for faster inference. The FP16 matmul patch enables
    torch.backends.cuda.matmul.allow_fp16_accumulation for additional
    throughput on supported hardware (requires PyTorch Nightly 2.7+).

    Both patches are independent and can be enabled or disabled individually.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Inputs:
            model:        The ComfyUI MODEL to patch.
            sage_enable:  Toggle to apply the SageAttention patch.
            torch_enable: Toggle to apply the FP16 matmul patch.
            sage_mode:    Selects the SageAttention kernel variant.
                          'auto' uses the default sageattn() entry point;
                          the other options select specific quantisation
                          configurations (CUDA or Triton backends).

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
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_patches"
    CATEGORY = "TA Smart LLM"

    def apply_patches(self, model, sage_enable, torch_enable, sage_mode):
        """
        Applies the selected patches to the model and returns the patched result.

        Each patch is applied independently based on its toggle. If sage_enable
        is True, _apply_sage_patch() is called first; if torch_enable is True,
        _apply_torch_patch() is called afterwards. Both patches modify the model
        object in-place and also return it for chaining.

        Args:
            model:          ComfyUI MODEL object to patch.
            sage_enable (bool):  Whether to apply the SageAttention patch.
            torch_enable (bool): Whether to apply the FP16 matmul patch.
            sage_mode (str):     SageAttention kernel variant to use.

        Returns:
            tuple: Single-element tuple containing the patched MODEL object.
        """
        logger.info(f"🚀 [TA] SageToggler START | Sage:{sage_enable} | Torch:{torch_enable} | Mode:{sage_mode}")
        patched_model = model

        applied = []

        if sage_enable:
            patched_model = self._apply_sage_patch(patched_model, sage_mode)
            applied.append(f"Sage({sage_mode})")

        if torch_enable:
            patched_model = self._apply_torch_patch(patched_model)
            applied.append("Torch FP16")

        if applied:
            logger.info(f"✅ [TA] Patches applied: {', '.join(applied)}")
        else:
            logger.info("⏭️ [TA] No patches applied – both toggles disabled, model passed through.")

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

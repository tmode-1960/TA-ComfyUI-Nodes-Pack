"""
================================================================================
Node Name   : TA Load Model (with Name)
Created     : 2025
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Combined model loader for Diffusion Models, GGUF UNet models, and
    Checkpoints. Automatically detects the model type from the [D] / [G] / [C]
    prefix in the filename and routes to the appropriate loader. Returns the
    model, optional CLIP and VAE (checkpoints only), and the bare model name
    string as a TA_MODEL_NAME output.
================================================================================
"""

import folder_paths
import comfy.sd
import os
import sys
import io
import torch
from contextlib import redirect_stderr, redirect_stdout


def _scan_models() -> list:
    """
    Scans diffusion_models, unet/unet_gguf, and checkpoints directories and
    returns a sorted list of all discovered model filenames with type prefixes:

      [D]  diffusion_models  (non-GGUF)
      [G]  GGUF              (unet_gguf / unet folder, .gguf extension)
      [C]  checkpoints

    The prefixes are used by TALoadModelWithName.load_model() to select the
    correct loading strategy without requiring separate node inputs.

    Returns:
        list[str]: Sorted list of prefixed model name strings, e.g.
                   ['[C] v1-5-pruned.safetensors', '[D] flux1-dev.safetensors',
                    '[G] flux1-Q4_K_S.gguf']. Returns ['No models found'] if
                   no models are detected in any of the scanned directories.
    """
    entries = []

    # Diffusion models (non-GGUF)
    try:
        for name in folder_paths.get_filename_list("diffusion_models"):
            if not name.lower().endswith(".gguf"):
                entries.append(f"[D] {name}")
    except Exception:
        pass

    # GGUF: scan models/unet directly (folder_paths filters out .gguf files)
    try:
        unet_dirs = folder_paths.get_folder_paths("unet")
        for unet_dir in unet_dirs:
            if not os.path.isdir(unet_dir):
                continue
            for root, _, files in os.walk(unet_dir):
                for fname in files:
                    if fname.lower().endswith(".gguf"):
                        # Store path relative to the unet_dir as the model name
                        rel = os.path.relpath(os.path.join(root, fname), unet_dir)
                        entries.append(f"[G] {rel}")
    except Exception:
        pass

    # Checkpoints
    try:
        for name in folder_paths.get_filename_list("checkpoints"):
            entries.append(f"[C] {name}")
    except Exception:
        pass

    return sorted(entries) if entries else ["No models found"]


def _load_gguf(unet_name: str):
    """
    Loads a GGUF UNet model via the ComfyUI-GGUF custom node package.

    Attempts three loading strategies in order, falling back to the next if
    the previous raises an exception:

      1. Import UnetLoaderGGUF directly from the ComfyUI-GGUF nodes module.
      2. Look up 'UnetLoaderGGUF' in ComfyUI's global NODE_CLASS_MAPPINGS.
      3. Load the GGUF state dict manually via GGMLOps and gguf_sd_loader,
         then pass it to comfy.sd.load_diffusion_model_state_dict().

    All stdout/stderr output from the GGUF loaders is suppressed to keep the
    ComfyUI console clean.

    Args:
        unet_name (str): Relative path to the GGUF file within the unet folder,
                         e.g. 'flux1-Q4_K_S.gguf'.

    Returns:
        MODEL: Loaded ComfyUI model object.

    Raises:
        FileNotFoundError: If the GGUF file cannot be located in any unet directory.
        RuntimeError:      If all three loading strategies fail.
    """
    gguf_node_path = os.path.join(
        folder_paths.base_path, "custom_nodes", "ComfyUI-GGUF"
    )
    model = None

    # Resolve the absolute path to the GGUF file
    unet_path = None
    try:
        unet_dirs = folder_paths.get_folder_paths("unet")
        for unet_dir in unet_dirs:
            candidate = os.path.join(unet_dir, unet_name)
            if os.path.exists(candidate):
                unet_path = candidate
                break
    except Exception:
        pass

    if unet_path is None:
        raise FileNotFoundError(f"GGUF file not found: {unet_name}")

    # Strategy 1: UnetLoaderGGUF from the ComfyUI-GGUF nodes module
    try:
        if gguf_node_path not in sys.path:
            sys.path.insert(0, gguf_node_path)
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            try:
                from nodes import UnetLoaderGGUF
                model = UnetLoaderGGUF().load_unet(unet_name)[0]
            except ImportError:
                import importlib.util
                nodes_path = os.path.join(gguf_node_path, "nodes.py")
                if os.path.exists(nodes_path):
                    spec = importlib.util.spec_from_file_location("gguf_nodes", nodes_path)
                    gguf_nodes = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(gguf_nodes)
                    if hasattr(gguf_nodes, "UnetLoaderGGUF"):
                        model = gguf_nodes.UnetLoaderGGUF().load_unet(unet_name)[0]
    except Exception:
        pass

    # Strategy 2: NODE_CLASS_MAPPINGS lookup
    if model is None:
        try:
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                from nodes import NODE_CLASS_MAPPINGS
                if "UnetLoaderGGUF" in NODE_CLASS_MAPPINGS:
                    model = NODE_CLASS_MAPPINGS["UnetLoaderGGUF"]().load_unet(unet_name)[0]
        except Exception:
            pass

    # Strategy 3: Direct GGUF module loading via absolute path
    if model is None:
        try:
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                from ops import GGMLOps
                from loader import gguf_sd_loader
                sd = gguf_sd_loader(unet_path)
                model = comfy.sd.load_diffusion_model_state_dict(
                    sd, model_options={"custom_operations": GGMLOps()}
                )
        except Exception:
            pass

    if model is None:
        raise RuntimeError(
            f"Could not load GGUF model: {unet_name}\n"
            "Check that ComfyUI-GGUF is installed and the gguf package is available."
        )
    return model


class TALoadModelWithName:
    """
    Combined model loader for Diffusion Models, GGUF UNet models, and Checkpoints.

    Automatically detects the model type from the [D] / [G] / [C] prefix in the
    selected model_file string and routes to the appropriate loading strategy:

      [D]  comfy.sd.load_diffusion_model()               – standard diffusion model
      [G]  _load_gguf()                                   – GGUF quantised UNet
      [C]  comfy.sd.load_checkpoint_guess_config()        – full checkpoint

    Outputs:
      model       – always present for all model types
      clip        – populated for checkpoints only, None otherwise
      vae         – populated for checkpoints only, None otherwise
      model_name  – bare filename without path or extension (TA_MODEL_NAME type)
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with all required inputs.
        """
        return {
            "required": {
                "model_file": (_scan_models(),),
                "weight_dtype": (
                    ["auto", "fp8_e4m3fn", "fp8_e5m2"],
                    {"default": "auto",
                     "tooltip": "Relevant for Diffusion Models only. "
                                "Auto = ComfyUI decides based on the model."},
                ),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "TA_MODEL_NAME")
    RETURN_NAMES = ("model", "clip", "vae", "model_name")
    FUNCTION = "load_model"
    CATEGORY = "TA Nodes/loaders"

    def load_model(self, model_file: str, weight_dtype: str):
        """
        Loads the selected model file and returns its components.

        Parses the [D] / [G] / [C] prefix to determine the model type, then
        delegates to the appropriate ComfyUI loader. For diffusion models the
        weight_dtype option is applied when set to fp8_e4m3fn or fp8_e5m2.
        CLIP and VAE outputs are only populated for checkpoint models.

        Args:
            model_file (str):   Prefixed model name string as produced by
                                _scan_models(), e.g. '[D] flux1-dev.safetensors'.
            weight_dtype (str): Weight precision override for diffusion models.
                                One of 'auto', 'fp8_e4m3fn', or 'fp8_e5m2'.

        Returns:
            tuple: (model, clip, vae, model_name_only) where:
                   - model           : loaded ComfyUI MODEL object
                   - clip            : CLIP object (checkpoints) or None
                   - vae             : VAE object (checkpoints) or None
                   - model_name_only : bare filename string without path/extension

        Raises:
            ValueError: If model_file does not start with a recognised prefix.
        """
        # Separate prefix from actual filename
        if model_file.startswith("[D] "):
            kind = "diffusion"
            name = model_file[4:]
        elif model_file.startswith("[G] "):
            kind = "gguf"
            name = model_file[4:]
        elif model_file.startswith("[C] "):
            kind = "checkpoint"
            name = model_file[4:]
        else:
            raise ValueError(f"[TALoadModelWithName] Unknown format: '{model_file}'")

        model = clip = vae = None

        # --- Diffusion Model ---
        if kind == "diffusion":
            unet_path = folder_paths.get_full_path("diffusion_models", name)
            model_options = {}
            if weight_dtype == "fp8_e4m3fn":
                model_options["weight_dtype"] = torch.float8_e4m3fn
            elif weight_dtype == "fp8_e5m2":
                model_options["weight_dtype"] = torch.float8_e5m2

            with torch.inference_mode():
                if model_options:
                    model = comfy.sd.load_diffusion_model(unet_path, model_options=model_options)
                else:
                    model = comfy.sd.load_diffusion_model(unet_path)

        # --- GGUF ---
        elif kind == "gguf":
            model = _load_gguf(name)

        # --- Checkpoint ---
        elif kind == "checkpoint":
            ckpt_path = folder_paths.get_full_path("checkpoints", name)
            with torch.inference_mode():
                out = comfy.sd.load_checkpoint_guess_config(
                    ckpt_path,
                    output_vae=True,
                    output_clip=True,
                    embedding_directory=folder_paths.get_folder_paths("embeddings"),
                )
            model = out[0]
            clip  = out[1]
            vae   = out[2]

        model_name_only = os.path.splitext(os.path.basename(name))[0]
        print(f"[TALoadModelWithName] Loaded: [{kind.upper()}] '{model_name_only}'")
        return (model, clip, vae, model_name_only)


NODE_CLASS_MAPPINGS = {
    "TALoadModelWithName": TALoadModelWithName
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TALoadModelWithName": "TA Load Model (with Name)"
}

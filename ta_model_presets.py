"""
================================================================================
Node Name   : TA Model Presets
Created     : 2025
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Preset-based model loader. Loads Model, CLIP (single or dual for FLUX/SDXL)
    and VAE from a named preset defined in ta_model_presets.json. Supports
    Diffusion Models [D], GGUF UNet models [G], and full Checkpoints [C].
    Includes a browser-based preset editor at:
    http://localhost:8188/ta_model_presets/ui
================================================================================
"""

import folder_paths
import comfy.sd
import comfy.utils
import os
import sys
import io
import json
import torch
from contextlib import redirect_stderr, redirect_stdout
from aiohttp import web
from server import PromptServer

# ──────────────────────────────────────────────
#  Paths
# ──────────────────────────────────────────────
_THIS_DIR     = os.path.dirname(os.path.abspath(__file__))
_PRESETS_FILE = os.path.join(_THIS_DIR, "ta_model_presets.json")
_HTML_PATH    = os.path.join(_THIS_DIR, "web", "js", "ta_model_presets_ui.html")

_DEFAULT_PRESETS = [
    {
        "name": "ZImage (BF16)",
        "model_file":   "[D] ZIMAGE/z_image_turbo_bf16.safetensors",
        "clip_name_1":  "ZIMAGE/qwen_3_4b_bf16.safetensors",
        "clip_name_2":  "",
        "clip_type":    "lumina2",
        "clip_device":  "default",
        "vae_name":     "ZIMAGE/zImage_vae.safetensors",
        "shift":        3.0,
        "weight_dtype": "auto"
    },
    {
        "name": "FLUX Dev (FP8)",
        "model_file":   "[D] FLUX/flux1-dev-fp8.safetensors",
        "clip_name_1":  "FLUX/t5xxl_fp8_e4m3fn.safetensors",
        "clip_name_2":  "FLUX/clip_l.safetensors",
        "clip_type":    "flux",
        "clip_device":  "default",
        "vae_name":     "FLUX/FLUX_VAE.safetensors",
        "shift":        "",
        "weight_dtype": "fp8_e4m3fn"
    },
    {
        "name": "SDXL Checkpoint",
        "model_file":   "[C] SDXL/sdxl_base.safetensors",
        "clip_name_1":  "",
        "clip_name_2":  "",
        "clip_type":    "auto",
        "clip_device":  "default",
        "vae_name":     "",
        "shift":        "",
        "weight_dtype": "auto"
    }
]

# Map clip_type string → ComfyUI internal CLIPType enum constant.
# Built dynamically from the CLIPType enum so it stays current across ComfyUI versions.
def _build_clip_type_map() -> dict:
    """
    Builds a mapping from lowercase clip_type name strings to ComfyUI CLIPType
    enum members. 'auto' is mapped to None (caller decides the default).
    Common aliases (sdxl, sd1) are added for the stable_diffusion enum member
    if present, so preset files can use short names without breaking.

    Returns:
        dict: Mapping of {str: CLIPType | None}.
    """
    mapping = {"auto": None}
    try:
        for member in comfy.sd.CLIPType:
            key = member.name.lower()
            mapping[key] = member
    except Exception:
        pass
    # Aliases for common short names
    if "stable_diffusion" in mapping:
        mapping.setdefault("sdxl", mapping["stable_diffusion"])
        mapping.setdefault("sd1",  mapping["stable_diffusion"])
    return mapping

_CLIP_TYPE_MAP = _build_clip_type_map()


def _get_clip_type_names() -> list:
    """
    Returns all available CLIPType names as lowercase strings, prefixed with
    'auto'. Used to populate the clip_type dropdown in the browser editor.

    Returns:
        list[str]: List of clip type name strings, e.g. ['auto', 'flux', 'stable_diffusion', ...].
    """
    names = ["auto"]
    try:
        for member in comfy.sd.CLIPType:
            names.append(member.name.lower())
    except Exception:
        pass
    return names


def _normalize(path: str) -> str:
    """
    Normalizes path separators to forward slashes for cross-platform consistency.

    Args:
        path (str): File path string, potentially containing backslashes (Windows).

    Returns:
        str: Path string with all backslashes replaced by forward slashes.
    """
    return path.replace("\\", "/")


# ──────────────────────────────────────────────
#  JSON helpers
# ──────────────────────────────────────────────
def _ensure_presets_file() -> list:
    """
    Ensures ta_model_presets.json exists and returns its contents as a list.

    If the file does not exist it is created with _DEFAULT_PRESETS. If the file
    exists but is empty, invalid JSON, or not a list, _DEFAULT_PRESETS is
    returned as a safe fallback without modifying the file.

    Returns:
        list[dict]: List of preset dictionaries loaded from file, or
                    _DEFAULT_PRESETS on any error.
    """
    if not os.path.exists(_PRESETS_FILE):
        try:
            with open(_PRESETS_FILE, "w", encoding="utf-8") as f:
                json.dump(_DEFAULT_PRESETS, f, indent=2, ensure_ascii=False)
            print(f"[TAModelPreset] ta_model_presets.json created with {len(_DEFAULT_PRESETS)} example presets.")
        except Exception as e:
            print(f"[TAModelPreset] Could not create ta_model_presets.json: {e}")
            return _DEFAULT_PRESETS

    try:
        with open(_PRESETS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list) and data:
            return data
        return _DEFAULT_PRESETS
    except Exception as e:
        print(f"[TAModelPreset] Error reading ta_model_presets.json: {e}")
        return _DEFAULT_PRESETS


def _save_presets(presets: list) -> None:
    """
    Serializes the given list of preset dicts to ta_model_presets.json.

    Args:
        presets (list[dict]): List of preset dictionaries to persist.
    """
    with open(_PRESETS_FILE, "w", encoding="utf-8") as f:
        json.dump(presets, f, indent=2, ensure_ascii=False)


def _preset_names() -> list:
    """
    Returns the 'name' field of every preset in the presets file as a list.
    Falls back to 'Preset N' for entries without a name field.

    Returns:
        list[str]: Ordered list of preset name strings.
    """
    return [p.get("name", f"Preset {i}") for i, p in enumerate(_ensure_presets_file())]


def _get_preset_by_name(name: str) -> dict | None:
    """
    Looks up a preset dict by its 'name' field.

    Args:
        name (str): Preset name to search for.

    Returns:
        dict | None: Matching preset dict, or None if not found.
    """
    for p in _ensure_presets_file():
        if p.get("name") == name:
            return p
    return None


# ──────────────────────────────────────────────
#  Scan helpers – always forward slashes
# ──────────────────────────────────────────────
def _scan_model_files() -> list:
    """
    Scans diffusion_models, unet (GGUF), and checkpoints directories and
    returns a sorted list of all discovered model filenames with type prefixes:

      [D]  diffusion_models  (non-GGUF)
      [G]  GGUF              (.gguf files in the unet folder)
      [C]  checkpoints

    All paths use forward slashes for cross-platform consistency.

    Returns:
        list[str]: Sorted list of prefixed model name strings.
    """
    entries = []
    try:
        for name in folder_paths.get_filename_list("diffusion_models"):
            if not name.lower().endswith(".gguf"):
                entries.append(f"[D] {_normalize(name)}")
    except Exception:
        pass
    try:
        unet_dirs = folder_paths.get_folder_paths("unet")
        for unet_dir in unet_dirs:
            if not os.path.isdir(unet_dir):
                continue
            for root, _, files in os.walk(unet_dir):
                for fname in files:
                    if fname.lower().endswith(".gguf"):
                        rel = os.path.relpath(os.path.join(root, fname), unet_dir)
                        entries.append(f"[G] {_normalize(rel)}")
    except Exception:
        pass
    try:
        for name in folder_paths.get_filename_list("checkpoints"):
            entries.append(f"[C] {_normalize(name)}")
    except Exception:
        pass
    return sorted(entries)


def _scan_clip_files() -> list:
    """
    Scans the 'clip' and 'text_encoders' model directories and returns a
    sorted, deduplicated list of all found CLIP/text encoder filenames.
    All paths use forward slashes.

    Returns:
        list[str]: Sorted list of CLIP model filename strings.
    """
    entries = []
    for folder in ["clip", "text_encoders"]:
        try:
            entries += [_normalize(n) for n in folder_paths.get_filename_list(folder)]
        except Exception:
            pass
    return sorted(set(entries))


def _scan_vae_files() -> list:
    """
    Scans the 'vae' model directory and returns a sorted list of all found
    VAE filenames. All paths use forward slashes.

    Returns:
        list[str]: Sorted list of VAE filename strings, or [] on error.
    """
    try:
        return sorted(_normalize(n) for n in folder_paths.get_filename_list("vae"))
    except Exception:
        return []


# ──────────────────────────────────────────────
#  Web Endpoints
# ──────────────────────────────────────────────
@PromptServer.instance.routes.get("/ta_model_presets/ui")
async def ta_presets_ui(request):
    """
    Serves the browser-based preset editor HTML page.

    Route: GET /ta_model_presets/ui

    Returns:
        web.Response: HTML page content, or a 404 response if the HTML file
                      is not found at the expected path.
    """
    if not os.path.exists(_HTML_PATH):
        return web.Response(text="HTML file not found.", status=404)
    with open(_HTML_PATH, "r", encoding="utf-8") as f:
        return web.Response(text=f.read(), content_type="text/html")


@PromptServer.instance.routes.get("/ta_model_presets/list")
async def ta_presets_list(request):
    """
    Returns the full list of currently saved presets as JSON.

    Route: GET /ta_model_presets/list

    Returns:
        web.Response: JSON response with {'presets': [...]}.
    """
    return web.json_response({"presets": _ensure_presets_file()})


@PromptServer.instance.routes.get("/ta_model_presets/options")
async def ta_presets_options(request):
    """
    Returns all available model, CLIP, VAE, and clip_type options as JSON.
    Used by the browser editor to populate its dropdown menus.

    Route: GET /ta_model_presets/options

    Returns:
        web.Response: JSON response with {'models': [...], 'clips': [...],
                      'vaes': [...], 'clip_types': [...]}.
    """
    return web.json_response({
        "models":      _scan_model_files(),
        "clips":       _scan_clip_files(),
        "vaes":        _scan_vae_files(),
        "clip_types":  _get_clip_type_names(),
    })


@PromptServer.instance.routes.post("/ta_model_presets/save")
async def ta_presets_save(request):
    """
    Accepts a JSON body with a 'presets' list and persists it to
    ta_model_presets.json. Entries without a non-empty 'name' field are
    filtered out before saving.

    Route: POST /ta_model_presets/save
    Body:  {'presets': [{...}, ...]}

    Returns:
        web.Response: JSON response with {'ok': True} on success, or
                      {'ok': False, 'error': str} on validation failure or exception.
    """
    try:
        body    = await request.json()
        presets = body.get("presets", [])
        presets = [p for p in presets if isinstance(p, dict) and p.get("name", "").strip()]
        if not presets:
            return web.json_response({"ok": False, "error": "No valid presets provided."})
        _save_presets(presets)
        print(f"[TAModelPreset] {len(presets)} preset(s) saved.")
        return web.json_response({"ok": True})
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)})


# ──────────────────────────────────────────────
#  ModelSamplingAuraFlow Patch
# ──────────────────────────────────────────────
def _apply_auraflow_patch(model, shift: float):
    """
    Applies the ModelSamplingAuraFlow patch to a model, equivalent to using
    the ComfyUI node of the same name. Used to set the sigma shift value for
    AuraFlow-based architectures (e.g. Z-Image-Turbo).

    Looks up 'ModelSamplingAuraFlow' in NODE_CLASS_MAPPINGS and calls its
    patch_aura() method. If the node is not registered or the call fails,
    the original model is returned unmodified.

    Args:
        model:        ComfyUI MODEL object to patch.
        shift (float): Sigma shift value to apply.

    Returns:
        MODEL: Patched model, or the original model if the patch could not
               be applied.
    """
    try:
        from nodes import NODE_CLASS_MAPPINGS
        if "ModelSamplingAuraFlow" in NODE_CLASS_MAPPINGS:
            result = NODE_CLASS_MAPPINGS["ModelSamplingAuraFlow"]().patch_aura(model, shift)
            print(f"[TAModelPreset] ModelSamplingAuraFlow applied (shift={shift})")
            return result[0]
        else:
            print("[TAModelPreset] ModelSamplingAuraFlow not in NODE_CLASS_MAPPINGS – model unchanged")
            return model
    except Exception as e:
        print(f"[TAModelPreset] ModelSamplingAuraFlow error: {e} – model unchanged")
        return model


# ──────────────────────────────────────────────
#  GGUF Loader
# ──────────────────────────────────────────────
def _load_gguf(unet_name: str):
    """
    Loads a GGUF UNet model via the ComfyUI-GGUF custom node package.

    Attempts three loading strategies in order, falling back to the next if
    the previous raises an exception:

      1. Import UnetLoaderGGUF directly from the ComfyUI-GGUF nodes module.
      2. Look up 'UnetLoaderGGUF' in ComfyUI's global NODE_CLASS_MAPPINGS.
      3. Load the GGUF state dict manually via GGMLOps and gguf_sd_loader,
         then pass it to comfy.sd.load_diffusion_model_state_dict().

    All stdout/stderr output from the GGUF loaders is suppressed.

    Args:
        unet_name (str): Relative path to the GGUF file within the unet folder.

    Returns:
        MODEL: Loaded ComfyUI model object.

    Raises:
        FileNotFoundError: If the GGUF file cannot be located in any unet directory.
        RuntimeError:      If all three loading strategies fail.
    """
    gguf_node_path = os.path.join(
        folder_paths.base_path, "custom_nodes", "ComfyUI-GGUF"
    )
    model     = None
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


# ──────────────────────────────────────────────
#  CLIP Loader helper – uses ComfyUI's native CLIPLoader
# ──────────────────────────────────────────────
def _load_clip(clip_name_1: str, clip_name_2: str, clip_type: str):
    """
    Loads a CLIP model using ComfyUI's native CLIPLoader or DualCLIPLoader node.

    Selects the loader based on whether clip_name_2 is provided:
      - Single CLIP: CLIPLoader with clip_type (defaults to 'stable_diffusion'
        when 'auto' is specified).
      - Dual CLIP:   DualCLIPLoader with clip_type (defaults to 'flux' when
        'auto' is specified).

    Args:
        clip_name_1 (str): Primary CLIP / text encoder filename.
        clip_name_2 (str): Secondary CLIP filename for dual-CLIP setups (e.g. FLUX).
                           Pass an empty string for single-CLIP models.
        clip_type (str):   CLIP type string, e.g. 'flux', 'stable_diffusion', 'auto'.

    Returns:
        CLIP | None: Loaded ComfyUI CLIP object, or None if the loader node is
                     not available or an exception occurs.
    """
    try:
        from nodes import NODE_CLASS_MAPPINGS as _NCM

        ct = _CLIP_TYPE_MAP.get(clip_type.lower())

        if clip_name_2:
            # Dual CLIP → DualCLIPLoader
            if "DualCLIPLoader" in _NCM:
                clip_type_name = clip_type.lower() if clip_type.lower() != "auto" else "flux"
                return _NCM["DualCLIPLoader"]().load_clip(clip_name_1, clip_name_2, clip_type_name)[0]
            else:
                print("[TAModelPreset] DualCLIPLoader not found")
                return None
        else:
            # Single CLIP → CLIPLoader
            if "CLIPLoader" in _NCM:
                clip_type_name = clip_type.lower() if clip_type.lower() != "auto" else "stable_diffusion"
                return _NCM["CLIPLoader"]().load_clip(clip_name_1, clip_type_name)[0]
            else:
                print("[TAModelPreset] CLIPLoader not found")
                return None
    except Exception as e:
        print(f"[TAModelPreset] CLIP load error: {e}")
        return None


# ──────────────────────────────────────────────
#  Node
# ──────────────────────────────────────────────
class TAModelPreset:
    """
    Preset-based model loader node for ComfyUI.

    Loads Model, CLIP (single or dual for FLUX/SDXL), and VAE from a named
    preset defined in ta_model_presets.json. Supports Diffusion Models [D],
    GGUF UNet models [G], and full Checkpoints [C]. Optionally applies the
    ModelSamplingAuraFlow shift patch when a 'shift' value is set in the preset.

    Browser-based preset editor: http://localhost:8188/ta_model_presets/ui
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Reads the current preset names from ta_model_presets.json at node load
        time to populate the preset dropdown.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with the required preset input.
        """
        names = _preset_names()
        return {
            "required": {
                "preset": (names, {
                    "tooltip": "Editor: http://localhost:8188/ta_model_presets/ui"
                }),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "TA_MODEL_NAME")
    RETURN_NAMES = ("model", "clip", "vae", "model_name")
    FUNCTION = "load_preset"
    CATEGORY = "TA Nodes/loaders"

    def load_preset(self, preset: str):
        """
        Loads all model components defined by the selected preset.

        Reads the preset from ta_model_presets.json, parses the [D]/[G]/[C]
        model_file prefix to select the loading strategy, then loads the model,
        CLIP (if not provided by a checkpoint), and VAE (if not provided by a
        checkpoint). Optionally applies the ModelSamplingAuraFlow shift patch
        if the preset includes a non-empty 'shift' value.

        Args:
            preset (str): Name of the preset to load, as listed in the dropdown.

        Returns:
            tuple: (model, clip, vae, model_name_only) where:
                   - model           : loaded ComfyUI MODEL object
                   - clip            : CLIP object or None
                   - vae             : VAE object or None
                   - model_name_only : bare filename string without path/extension

        Raises:
            ValueError: If the preset name is not found or model_file has an
                        unrecognised prefix format.
        """
        p = _get_preset_by_name(preset)
        if p is None:
            raise ValueError(f"[TAModelPreset] Preset '{preset}' not found.")

        model_file   = _normalize(p.get("model_file", ""))
        clip_name_1  = _normalize(p.get("clip_name_1", p.get("clip_name", "")))
        clip_name_2  = _normalize(p.get("clip_name_2", ""))
        vae_name     = _normalize(p.get("vae_name", ""))
        clip_type    = p.get("clip_type", "auto")
        clip_device  = p.get("clip_device", "default")
        weight_dtype = p.get("weight_dtype", "auto")

        if model_file.startswith("[D] "):
            kind  = "diffusion"
            mname = model_file[4:]
        elif model_file.startswith("[G] "):
            kind  = "gguf"
            mname = model_file[4:]
        elif model_file.startswith("[C] "):
            kind  = "checkpoint"
            mname = model_file[4:]
        else:
            raise ValueError(f"[TAModelPreset] Unknown model_file format: '{model_file}'")

        model = clip = vae = None

        # ── Load model ──
        if kind == "diffusion":
            unet_path = folder_paths.get_full_path("diffusion_models", mname)
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

        elif kind == "gguf":
            model = _load_gguf(mname)

        elif kind == "checkpoint":
            # CLIP and VAE are bundled inside the checkpoint
            ckpt_path = folder_paths.get_full_path("checkpoints", mname)
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

        # ── Load CLIP (only if not already provided by a checkpoint) ──
        if clip is None and clip_name_1:
            clip = _load_clip(clip_name_1, clip_name_2, clip_type)

        # ── Load VAE (only if not already provided by a checkpoint) ──
        if vae is None and vae_name:
            try:
                from nodes import NODE_CLASS_MAPPINGS as _NCM
                if "VAELoader" in _NCM:
                    vae = _NCM["VAELoader"]().load_vae(vae_name)[0]
                else:
                    print(f"[TAModelPreset] VAELoader not found")
            except Exception as e:
                print(f"[TAModelPreset] VAE load error: {e}")

        model_name_only = os.path.splitext(os.path.basename(mname))[0]
        dual = " (Dual CLIP)" if clip_name_2 else ""

        # ── ModelSamplingAuraFlow patch (optional) ──
        shift_raw = p.get("shift", "")
        if shift_raw != "" and shift_raw is not None:
            try:
                shift = float(shift_raw)
                model = _apply_auraflow_patch(model, shift)
            except (ValueError, TypeError):
                pass

        print(f"[TAModelPreset] Loaded: Preset='{preset}' [{kind.upper()}]{dual} '{model_name_only}'")
        return (model, clip, vae, model_name_only)


NODE_CLASS_MAPPINGS = {
    "TAModelPreset": TAModelPreset,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TAModelPreset": "TA Model Presets",
}

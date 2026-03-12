"""
================================================================================
Node Name   : TA Save Image Optional
Created     : 2025
Modified    : 2026-03-12
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.1
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Optional image saver that extends ComfyUI's built-in SaveImage node.
    Supports JPEG and WebP output formats with configurable quality, an
    enable/disable toggle, and optional companion .txt files containing the
    positive and negative prompts alongside a timestamp and filename reference.
================================================================================
"""

import os
import datetime
import torch
import numpy as np
from PIL import Image
from nodes import SaveImage
import folder_paths


class TASaveImageOptional(SaveImage):
    """
    Extended image saver node with optional saving, format selection, and
    prompt logging.

    Inherits from ComfyUI's SaveImage to reuse its output directory and path
    resolution logic. Adds a boolean enable toggle so the node can be disabled
    without disconnecting it from the workflow. When enabled, images are saved
    as JPEG or WebP with the specified quality. Optionally writes a companion
    .txt file per image containing the positive/negative prompts, timestamp,
    and filename for documentation and dataset purposes.
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Inputs:
            images:           IMAGE tensor batch to save.
            filename_prefix:  Base filename string. Any image extension suffix
                              (.jpg, .jpeg, .webp, .png) is stripped automatically
                              before path construction.
            enabled:          Master toggle. When False the node is bypassed and
                              the input images are passed through unchanged.
            save_txt:         When 'enabled', writes a .txt companion file per
                              image with prompts, timestamp, and filename.
            positive_prompt:  Positive prompt string to include in the .txt file.
            negative_prompt:  Negative prompt string to include in the .txt file.
            save_format:      Output image format: 'jpg' or 'webp'.
            jpeg_quality:     Compression quality level (applies to both JPEG
                              and WebP). Selectable from 70–100.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with required and optional inputs.
        """
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "enabled": ("BOOLEAN", {"default": True, "label_on": "✅ Save ON", "label_off": "❌ OFF"}),
                "save_txt": (["enabled", "disabled"], {"default": "enabled"}),
                "positive_prompt": ("STRING", {"forceInput": True}),
                "negative_prompt": ("STRING", {"forceInput": True}),
            },
            "optional": {
                "save_format": (["jpg", "webp"], {"default": "jpg"}),
                "jpeg_quality": (["70", "80", "90", "95", "100"], {"default": "95"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "ta_save_images"
    OUTPUT_NODE = True
    CATEGORY = "TA Nodes/utils"

    def ta_save_images(self, images, filename_prefix, enabled, save_txt, positive_prompt, negative_prompt,
                       save_format="jpg", jpeg_quality="95", **kwargs):
        """
        Saves images to disk in the selected format and optionally writes
        companion .txt prompt files.

        When enabled is False the method returns immediately, passing the input
        images through without writing any files.

        For each image in the batch:
          1. Converts the float IMAGE tensor to a uint8 numpy array.
          2. Saves the image as JPEG or WebP using the specified quality.
          3. Optionally writes a .txt file with timestamp, filename, and prompts.

        File naming follows ComfyUI's standard counter convention:
        <filename_prefix>_<counter:05>_.<ext>

        Any image extension suffix in filename_prefix is stripped before path
        construction to prevent double extensions.

        Args:
            images:               Batch IMAGE tensor (B, H, W, 3) float [0..1].
            filename_prefix (str): Base filename; extension suffixes are stripped.
            enabled (bool):        Master toggle. False = pass-through, no I/O.
            save_txt (str):        'enabled' to write .txt companion files.
            positive_prompt (str): Positive prompt string for .txt output.
            negative_prompt (str): Negative prompt string for .txt output.
            save_format (str):     'jpg' or 'webp'. Defaults to 'jpg'.
            jpeg_quality (str):    Quality level string '70'–'100'. Defaults to '95'.
            **kwargs:              Absorbs any additional ComfyUI-injected inputs.

        Returns:
            dict: ComfyUI result dict {'result': (images,)} containing the
                  original input IMAGE tensor for downstream nodes.
        """
        if not enabled:
            return {"result": (images,)}

        quality = int(jpeg_quality)
        if save_format == "webp":
            ext = ".webp"
        else:
            ext = ".jpg"

        # Strip any image extension suffix from filename_prefix if present
        for suffix in [".jpg", ".jpeg", ".webp", ".png"]:
            if filename_prefix.lower().endswith(suffix):
                filename_prefix = filename_prefix[:-len(suffix)]
                break

        full_output_folder, filename, counter, subfolder, filename_prefix = \
            folder_paths.get_save_image_path(
                filename_prefix,
                self.output_dir,
                images[0].shape[1],
                images[0].shape[0]
            )

        current_counter = counter - len(images)

        for i, img in enumerate(images):
            img = ((img.cpu() * 255).clip(0, 255).cpu().numpy()).astype(np.uint8)
            pil_img = Image.fromarray(img)
            file_base = f"{filename}_{current_counter:05}_"
            save_path = os.path.join(full_output_folder, f"{file_base}{ext}")

            if save_format == "webp":
                pil_img.save(save_path, format="WEBP", quality=quality)
            else:
                pil_img.save(save_path, format="JPEG", quality=quality)
            current_counter += 1

        if save_txt == "enabled":
            now = datetime.datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            current_counter = counter - len(images)
            for i in range(len(images)):
                file_base = f"{filename}_{current_counter:05}_"
                txt_file = f"{file_base}.txt"
                output_text = (
                    f"DATE / TIME: {date_time_str}\n"
                    f"FILE: {file_base}{ext}\n"
                    f"{'='*30}\n"
                    f"POSITIVE PROMPT:\n{positive_prompt}\n\n"
                    f"NEGATIVE PROMPT:\n{negative_prompt}\n"
                    f"{'='*30}\n"
                )
                try:
                    file_path = os.path.join(full_output_folder, txt_file)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(output_text)
                except Exception as e:
                    print(f"[TA-Nodes] Error writing TXT file: {e}")
                current_counter += 1

        return {"result": (images,)}


NODE_CLASS_MAPPINGS = {
    "TASaveImageOptional": TASaveImageOptional
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "TASaveImageOptional": "TA Save Image Optional v2.1"
}

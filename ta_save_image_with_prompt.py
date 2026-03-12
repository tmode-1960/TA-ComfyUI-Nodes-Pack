"""
================================================================================
Node Name   : TA Save Image With Prompt
Created     : 2025
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0


Description:
    Image saver that extends ComfyUI's built-in SaveImage node.
    Reuses the original saving logic and adds optional companion .txt files
    containing the positive and negative prompts alongside a timestamp and
    filename reference. The images are passed through for further workflow use.
================================================================================
"""

import os
import datetime
import json
from PIL import Image
import numpy as np

# Import of the original SaveImage class
from nodes import SaveImage
import folder_paths


class TASaveImageWithPrompt(SaveImage):
    """
    Extended image saver node that reuses ComfyUI's SaveImage saving logic.

    Inherits from ComfyUI's SaveImage class to leverage its output directory
    resolution, filename counter logic, and UI preview generation. After
    calling the original save_images() method, optionally writes a companion
    .txt file per image containing the positive/negative prompts, timestamp,
    and filename for documentation and dataset preparation purposes.

    The input images are always returned unchanged for downstream workflow nodes.
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Inputs:
        images: IMAGE tensor batch from upstream nodes.
        filename_prefix: Base filename string passed to the original SaveImage.
        positive_prompt: Positive prompt string to include in the .txt file.
        negative_prompt: Negative prompt string to include in the .txt file.
        save_txt: When 'enabled', writes a .txt companion file per image with
                  prompts, timestamp, and filename reference.

        Returns:
        dict: ComfyUI INPUT_TYPES dictionary with required inputs.
        """
        # Get the original input definitions
        types = SaveImage.INPUT_TYPES()
        # Add our prompt-related inputs
        types["required"].update({
            "positive_prompt": ("STRING", {"forceInput": True}),
            "negative_prompt": ("STRING", {"forceInput": True}),
            "save_txt": (["enabled", "disabled"], {"default": "enabled"}),
        })
        return types

    # --- CHANGE: define return type ---
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    # -----------------------------------

    FUNCTION = "ta_save_images"
    OUTPUT_NODE = True
    CATEGORY = "TA Nodes/utils"

    def ta_save_images(self, images, filename_prefix, positive_prompt, negative_prompt, save_txt, **kwargs):
        """
        Saves images using the original SaveImage logic and optionally writes
        companion .txt prompt files.

        Workflow:
        1. Calls self.save_images() from the base SaveImage class to perform
           the actual PNG saving and generate UI preview information.
        2. If save_txt is 'enabled', reconstructs the exact filenames using
           folder_paths.get_save_image_path() and writes a .txt file for each
           image containing timestamp, filename, and prompts.

        File naming follows ComfyUI's standard counter convention:
        <filename_prefix>_<00001>_.png + <filename>_<00001>_.txt

        Args:
        images: Batch IMAGE tensor (B, H, W, 3) float [0..1].
        filename_prefix (str): Base filename passed to SaveImage.
        positive_prompt (str): Positive prompt string for .txt output.
        negative_prompt (str): Negative prompt string for .txt output.
        save_txt (str): 'enabled' to write .txt companion files.
        **kwargs: Absorbs any additional ComfyUI-injected inputs.

        Returns:
        dict: ComfyUI result dict with 'ui' (from SaveImage) and 'result'
              tuple containing the original input IMAGE tensor.
        """
        # 1. Call the original method (saves images and generates metadata)
        snap_res = self.save_images(images=images, filename_prefix=filename_prefix, **kwargs)

        # 2. TXT logic
        if save_txt == "enabled":
            full_output_folder, filename, counter, subfolder, filename_prefix = \
                folder_paths.get_save_image_path(
                    filename_prefix,
                    self.output_dir,
                    images[0].shape[1],
                    images[0].shape[0]
                )

            now = datetime.datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

            # Recalculate counter to the state BEFORE saving
            current_counter = counter - len(images)

            for i in range(len(images)):
                file_base = f"{filename}_{current_counter:05}_"
                txt_file = f"{file_base}.txt"

                output_text = (
                    f"DATE / TIME: {date_time_str}\n"
                    f"FILE: {file_base}.png\n"
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
                    print(f"[TA-Nodes] Error while writing TXT: {e}")

                current_counter += 1

        # --- CHANGE: return images together with original UI results ---
        # snap_res contains UI preview info; we pass 'images' as workflow output.
        return {"ui": snap_res["ui"], "result": (images,)}


NODE_CLASS_MAPPINGS = {
    "TASaveImageWithPrompt": TASaveImageWithPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TASaveImageWithPrompt": "TA Save Image With Prompt v2.0"
}

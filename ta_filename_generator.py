"""
================================================================================
Node Name   : TA Filename Generator
Created     : 2025
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Generates structured output file paths by combining an optional folder,
    an optional subfolder (which supports strftime date-format codes),
    a name prefix, workflow version, model name, and a formatted date string.
    Returns both a base filename and an upscaled variant.
================================================================================
"""

import datetime
import os

# List of date format options for the 'date_format' combo widget.
date_format_options = [
    "%Y%m%d%H%M",
    "%Y%m%d%H%M%S",
    "%Y%m%d",
    "%Y-%m-%d-%H_%M_%S",
    "%Y-%m-%d-%H_%M",
    "%Y-%m-%d",
    "%Y-%m-%d %H_%M_%S",
    "%Y-%m-%d %H_%M",
    "%H%M",
    "%H%M%S",
    "%H_%M",
    "%H_%M_%S"
]


class TAFilenameGenerator:
    """
    Custom ComfyUI node that replicates the filename-generation subgraph logic
    from thomo.ART workflows.

    Combines an optional output folder, an optional subfolder (which can contain
    strftime date-format codes such as %Y-%m-%d), a name prefix, workflow version,
    model name, and a formatted date string into a full file path.
    Returns both a base filename path and an upscaled variant path.
    """

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        All inputs are optional. The 'subfolder' field accepts plain text as well
        as strftime date-format codes (e.g. %Y-%m-%d), which are resolved at
        execution time. The 'date_format' combo controls the timestamp appended
        to the filename itself.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with all optional inputs.
        """
        return {
            "required": {},
            "optional": {
                "model_name": ("TA_MODEL_NAME",),
                "output_folder": ("STRING", {"default": "TA-Outputs"}),
                # The 'subfolder' field accepts plain strings as well as
                # strftime date-format codes, which are resolved internally.
                "subfolder": ("STRING", {"default": ""}),
                "name_prefix": ("STRING", {"default": "TA"}),
                "wf_version": ("STRING", {"default": "v2.50"}),
                "upscaled_suffix": ("STRING", {"default": "UPSCALED"}),
                "delimiter": ("STRING", {"default": "-"}),
                "date_format": (date_format_options, ),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("filename", "filename_up")

    FUNCTION = "generate_filenames"
    CATEGORY = "TA Nodes/utils"

    def generate_filenames(self, output_folder="TA-Outputs", subfolder="", name_prefix="TA", wf_version="v2.50", upscaled_suffix="UPSCALED", delimiter="-", date_format="%Y%m%d%H%M", model_name=None):
        """
        Builds and returns two OS-normalized file path strings: a base filename
        and an upscaled variant.

        Processing steps:
          1. Capture the current datetime.
          2. Format the date string for the filename using the selected date_format.
          3. Process the subfolder string through strftime to resolve any embedded
             date-format codes (e.g. '%Y-%m-%d' → '2026-03-11'). Plain text is
             passed through unchanged. Invalid codes fall back to the literal string.
          4. Assemble the base filename from [prefix, wf_version, model_name, date].
          5. Assemble the upscaled filename by appending the upscaled_suffix.
          6. Strip and clean the folder path components.
          7. Join all parts with os.path.join (empty subfolder is ignored).
          8. Normalize the final paths for the current OS (forward/back slashes).

        Args:
            output_folder (str):    Root output folder name. Default: 'TA-Outputs'.
            subfolder (str):        Optional subfolder name; supports strftime codes.
            name_prefix (str):      Short prefix string prepended to the filename.
            wf_version (str):       Workflow version tag, e.g. 'v2.50'.
            upscaled_suffix (str):  Suffix appended to the upscaled filename variant.
            delimiter (str):        Character used to join filename parts. Default: '-'.
            date_format (str):      strftime format string for the timestamp component.
            model_name (str|None):  Model name string from a TA_MODEL_NAME input.
                                    Falls back to 'model' if None.

        Returns:
            tuple[str, str]: (base_filepath, upscaled_filepath), both OS-normalized.
        """
        if model_name is None:
            model_name = "model"

        # 1. Get the current time.
        now = datetime.datetime.now()

        # 2. Format the date string for the filename (from the combo widget).
        try:
            date_string = now.strftime(date_format)
        except Exception as e:
            print(f"[TA-Nodes] Error formatting filename date: {e}")
            date_string = "DATE_ERROR"

        # 3. Process the 'subfolder' string.
        #    strftime resolves %-codes and leaves plain characters unchanged.
        try:
            processed_subfolder = now.strftime(subfolder)
        except ValueError as e:
            # If an invalid code (e.g. %q) is entered, use the literal string.
            print(f"[TA-Nodes] Warning: Invalid date format in subfolder '{subfolder}'. Using literal name.")
            processed_subfolder = subfolder

        # 4. Build the base filename WITHOUT folder path.
        parts_base = [
            name_prefix,
            wf_version,
            model_name,
            date_string
        ]
        base_filename_only = delimiter.join(filter(None, parts_base))

        # 5. Build the upscaled filename WITHOUT folder path.
        parts_upscaled_only = [
            base_filename_only,
            upscaled_suffix
        ]
        upscaled_filename_only = delimiter.join(filter(None, parts_upscaled_only))

        # 6. Strip and clean the folder path components.
        clean_output_folder = output_folder.strip().strip('/\\')
        # Use the processed (date-resolved) subfolder name.
        clean_subfolder = processed_subfolder.strip().strip('/\\')

        # 7. Build the final path using os.path.join.
        #    Empty strings (e.g. when subfolder is blank) are handled correctly.
        final_filename = os.path.join(clean_output_folder, clean_subfolder, base_filename_only)
        final_upscaled_filename = os.path.join(clean_output_folder, clean_subfolder, upscaled_filename_only)

        # 8. Normalize the path for the current operating system.
        final_filename = os.path.normpath(final_filename)
        final_upscaled_filename = os.path.normpath(final_upscaled_filename)

        # 9. Return both results.
        return (final_filename, final_upscaled_filename)


# ---------------------------------------------------------------------------------
#  NODE MAPPINGS
# ---------------------------------------------------------------------------------
NODE_CLASS_MAPPINGS = {
    "TAFilenameGenerator": TAFilenameGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TAFilenameGenerator": "TA Filename Generator"
}

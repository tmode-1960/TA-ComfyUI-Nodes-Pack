"""
================================================================================
Node Name   : TA Directory Captioning
Created     : 2025
Modified    : 2026-03-11
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 2.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0

Description:
    Iterates through a directory, sends images to LM Studio or Ollama Vision
    Models and saves the generated captions as .txt files alongside each image.
    Uses TASmartLLM model detection logic (LMStudio + Ollama, Vision tagging).
================================================================================
"""

import os
import base64
import requests
import time
from PIL import Image, ImageOps
from io import BytesIO

# Import TASmartLLM for model list, vision detection and tag logic.
# Falls back to a minimal inline implementation if ta_smart_llm is not available.
try:
    from .ta_smart_llm import TASmartLLM, is_vision_model, tag_model, strip_vision_tag
    _SMART_LLM_AVAILABLE = True
except ImportError:
    print("[TA-Captioning] WARN: ta_smart_llm not found. Using fallback model list.")
    _SMART_LLM_AVAILABLE = False

    VISION_KEYWORDS = ["llava", "vision", "-vl-", "_vl_", "vl-", "vl_",
                       "moondream", "minicpm-v", "internvl", "qwen-vl"]
    VISION_MANUAL = set()

    def is_vision_model(model_id: str) -> bool:
        lower = model_id.lower()
        return any(kw in lower for kw in VISION_KEYWORDS) or lower in VISION_MANUAL

    def tag_model(full_name: str) -> str:
        model_id = '/'.join(full_name.split('/')[1:])
        if is_vision_model(model_id):
            return f"{full_name} [Vision]"
        return full_name

    def strip_vision_tag(model: str) -> str:
        return model.replace(" [Vision]", "")

    class TASmartLLM:
        @classmethod
        def get_models(cls):
            models = []
            try:
                r = requests.get("http://127.0.0.1:1234/v1/models", timeout=2)
                if r.status_code == 200:
                    for m in r.json()['data']:
                        models.append(tag_model(f"LMStudio/{m['id']}"))
            except:
                pass
            try:
                r = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
                if r.status_code == 200:
                    for m in r.json()['models']:
                        models.append(tag_model(f"Ollama/{m['name']}"))
            except:
                pass
            return models if models else ["No Backend"]


# --- Helper function: normalize image and encode to Base64 ---

def encode_image_from_path(image_path: str, max_size: int = 1024) -> str:
    """
    Converts an image file to a Base64-encoded PNG string suitable for API submission.

    Normalization steps applied:
      - EXIF rotation correction (prevents incorrectly oriented images)
      - Color space conversion to RGB (removes RGBA channels and palette modes)
      - Resolution scaling to max_size px on the longest side (prevents HTTP 400 on large images)
      - Metadata stripping (clean PNG without embedded ComfyUI workflow chunks)

    Args:
        image_path (str): Absolute path to the source image file.
        max_size (int):   Maximum pixel size for the longest side. Defaults to 1024.

    Returns:
        str: Base64-encoded PNG string, or None if encoding failed.
    """
    try:
        with open(image_path, "rb") as f:
            img_bytes = f.read()

        pil_image = Image.open(BytesIO(img_bytes))
        pil_image = ImageOps.exif_transpose(pil_image)
        pil_image = pil_image.convert("RGB")
        pil_image.thumbnail((max_size, max_size), Image.LANCZOS)

        buffer = BytesIO()
        pil_image.save(buffer, format="PNG", optimize=False)

        return base64.b64encode(buffer.getvalue()).decode('utf-8')

    except Exception as e:
        print(f"[TA-Captioning] Error encoding {image_path}: {e}")
        return None


# --- Custom Node Class ---

class TACaptioning:
    """
    ComfyUI node that batch-captions all images in a given directory using a
    vision-capable LLM served by LM Studio or Ollama.

    For each image file (.png / .jpg / .jpeg / .webp) found in the target
    directory, the node:
      1. Encodes the image as a Base64 PNG (with normalization).
      2. Sends it together with the user-defined prompt to the selected model.
      3. Writes the generated caption text to a .txt file with the same base name.

    Existing caption files are skipped unless overwrite_existing is enabled.
    A summary status string is returned and printed to the console after the run.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Fetches the current model list from TASmartLLM (queries LM Studio and
        Ollama at node load time) and pre-selects the first vision-tagged model
        as the default.

        Returns:
            dict: ComfyUI INPUT_TYPES dictionary with all required inputs.
        """
        models = TASmartLLM.get_models()

        vision_models = [m for m in models if "[Vision]" in m]
        default_model = vision_models[0] if vision_models else (models[0] if models else "No Backend")

        return {
            "required": {
                "directory_path": ("STRING", {
                    "default": "C:/Images/to_caption",
                    "multiline": False
                }),
                "model": (models, {
                    "default": default_model
                }),
                "server_url": ("STRING", {
                    "default": "http://127.0.0.1:1234",
                    "multiline": False,
                    "tooltip": "LMStudio: http://127.0.0.1:1234 | Ollama: http://127.0.0.1:11434"
                }),
                "prompt": ("STRING", {
                    "default": (
                        "Describe this image in one continuous sentence or short paragraph. "
                        "No labels, no bullet points, no line breaks. "
                        "Focus on: subject, style, colors, lighting, composition, background. "
                        "No filler phrases, no interpretation. Respond in English."
                    ),
                    "multiline": True
                }),
                "system_prompt": ("STRING", {
                    "default": "You are a precise image captioning assistant for AI training datasets. Describe only what is visible. Be factual, concise, and always respond in English.",
                    "multiline": True
                }),
                "temperature": ("FLOAT", {
                    "default": 0.2, "min": 0.0, "max": 2.0, "step": 0.1
                }),
                "max_tokens": ("INT", {
                    "default": 150, "min": 1, "max": 131072
                }),
                "max_image_size": ("INT", {
                    "default": 1024, "min": 256, "max": 4096, "step": 128,
                    "tooltip": "Longest side in pixels. Larger images are downscaled (prevents HTTP 400)."
                }),
                "overwrite_existing": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Overwrite",
                    "label_off": "Skip existing"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "caption_directory"
    CATEGORY = "TA-Nodes/LMStudio"

    @classmethod
    def IS_CHANGED(cls, *args, **kwargs):
        """Forces re-execution on every queue run by returning the current timestamp."""
        return time.time()

    # ------------------------------------------------------------------ #
    #  Backend request dispatch                                            #
    # ------------------------------------------------------------------ #

    def _send_request(self, server_url, backend, model_name, prompt, system_prompt,
                      image_base64, temperature, max_tokens) -> str:
        """
        Dispatches the captioning request to the appropriate backend handler.

        Detects the backend from the model prefix ('LMStudio' or 'Ollama') and
        routes to the matching private method.

        Args:
            server_url (str):    Base URL of the inference server.
            backend (str):       Backend identifier, e.g. 'LMStudio' or 'Ollama'.
            model_name (str):    Model identifier without the backend prefix.
            prompt (str):        User prompt sent with the image.
            system_prompt (str): System-level instruction for the model.
            image_base64 (str):  Base64-encoded PNG image string.
            temperature (float): Sampling temperature for generation.
            max_tokens (int):    Maximum number of tokens to generate.

        Returns:
            str: Generated caption text from the model.
        """
        if "LMStudio" in backend:
            return self._send_lmstudio_request(
                server_url, model_name, prompt, system_prompt,
                image_base64, temperature, max_tokens
            )
        else:
            return self._send_ollama_request(
                server_url, model_name, prompt, system_prompt, image_base64
            )

    def _send_lmstudio_request(self, server_url, model_name, prompt, system_prompt,
                               image_base64, temperature, max_tokens) -> str:
        """
        Sends a vision chat completion request to an LM Studio server.

        Uses the OpenAI-compatible /v1/chat/completions endpoint. The image is
        passed as a base64 data URI inside the user message content array.

        Args:
            server_url (str):    Base URL of the LM Studio server.
            model_name (str):    Model identifier as returned by the LM Studio API.
            prompt (str):        User prompt text.
            system_prompt (str): System message for the chat.
            image_base64 (str):  Base64-encoded PNG image string.
            temperature (float): Sampling temperature.
            max_tokens (int):    Maximum tokens to generate.

        Returns:
            str: Stripped caption text from the model response.

        Raises:
            Exception: On connection errors or non-2xx HTTP responses.
        """
        url = f"{server_url}/v1/chat/completions"
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                ]}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        try:
            r = requests.post(url, json=payload, timeout=1200)
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content'].strip()
        except requests.exceptions.ConnectionError:
            raise Exception("Connection Error: LM Studio server not reachable.")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"LMStudio API HTTP Error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise Exception(f"LMStudio request failed: {str(e)}")

    def _send_ollama_request(self, server_url, model_name, prompt, system_prompt,
                             image_base64) -> str:
        """
        Sends a vision generation request to an Ollama server.

        Uses the Ollama /api/generate endpoint. System prompt and user prompt are
        concatenated as a single prompt string; the image is passed in the
        'images' field as a Base64 string.

        Args:
            server_url (str):    Base URL of the Ollama server.
            model_name (str):    Model name as listed by Ollama.
            prompt (str):        User prompt text.
            system_prompt (str): Prepended to the prompt as instructions.
            image_base64 (str):  Base64-encoded PNG image string.

        Returns:
            str: Stripped caption text from the model response.

        Raises:
            Exception: On connection errors or non-2xx HTTP responses.
        """
        url = f"{server_url}/api/generate"
        payload = {
            "model": model_name,
            "prompt": f"{system_prompt}\n\n{prompt}".strip(),
            "images": [image_base64],
            "stream": False
        }
        try:
            r = requests.post(url, json=payload, timeout=1200)
            r.raise_for_status()
            return r.json()['response'].strip()
        except requests.exceptions.ConnectionError:
            raise Exception("Connection Error: Ollama server not reachable.")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Ollama API HTTP Error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise Exception(f"Ollama request failed: {str(e)}")

    # ------------------------------------------------------------------ #
    #  Main execution function                                             #
    # ------------------------------------------------------------------ #

    def caption_directory(self, directory_path, model, server_url, prompt, system_prompt,
                          temperature, max_tokens, max_image_size, overwrite_existing):
        """
        Main node execution function. Iterates all images in the target directory
        and generates a caption .txt file for each one.

        Workflow per image:
          1. Check if a caption file already exists (skip if overwrite_existing is False).
          2. Encode the image to a normalized Base64 PNG via encode_image_from_path().
          3. Send the encoded image and prompts to the selected backend.
          4. Write the returned caption to a .txt file with the same base name.

        The model string is parsed to extract the backend prefix ('LMStudio' or
        'Ollama') and the actual model name. If Ollama is detected but the provided
        server_url does not contain port 11434, the URL is automatically corrected.

        Args:
            directory_path (str):    Absolute path to the directory containing images.
            model (str):             Selected model string including backend prefix and
                                     optional [Vision] tag, e.g. 'LMStudio/model-id [Vision]'.
            server_url (str):        Base URL of the inference server.
            prompt (str):            User prompt for the vision model.
            system_prompt (str):     System-level instruction for the model.
            temperature (float):     Sampling temperature for generation.
            max_tokens (int):        Maximum number of tokens to generate per caption.
            max_image_size (int):    Maximum pixel size for the longest image dimension.
            overwrite_existing (bool): If False, skips images that already have a .txt file.

        Returns:
            tuple[str]: Single-element tuple with a summary status string, e.g.:
                        "Done. 12 captions created, 3 skipped, 0 errors. (Total images: 15)"
        """
        clean_model = strip_vision_tag(model)
        parts       = clean_model.split('/', 1)
        backend     = parts[0]
        model_name  = parts[1] if len(parts) > 1 else clean_model

        if "Ollama" in backend and "11434" not in server_url:
            effective_url = "http://127.0.0.1:11434"
            print(f"[TA-Captioning] Ollama detected – using {effective_url} instead of {server_url}")
        else:
            effective_url = server_url.rstrip("/")

        if not os.path.isdir(directory_path):
            return (f"ERROR: Directory not found: {directory_path}",)

        image_files = [
            f for f in os.listdir(directory_path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
        ]

        if not image_files:
            return (f"NO IMAGES found in: {directory_path}",)

        print(f"\n{'='*60}")
        print(f"[TA-Captioning] Starting captioning for {len(image_files)} images...")
        print(f"[TA-Captioning] Backend      : {backend}")
        print(f"[TA-Captioning] Model        : {model_name}")
        print(f"[TA-Captioning] Server       : {effective_url}")
        print(f"[TA-Captioning] Max img size : {max_image_size}px")
        print(f"[TA-Captioning] Temperature  : {temperature}")
        print(f"[TA-Captioning] Max tokens   : {max_tokens}")
        print(f"[TA-Captioning] Overwrite    : {overwrite_existing}")
        print(f"{'='*60}\n")

        captioned_count = 0
        skipped_count   = 0
        error_count     = 0

        for filename in image_files:
            image_path   = os.path.join(directory_path, filename)
            base_name    = os.path.splitext(filename)[0]
            caption_path = os.path.join(directory_path, base_name + ".txt")

            if not overwrite_existing and os.path.exists(caption_path):
                print(f"ℹ️  '{filename}' already captioned – skipping.")
                skipped_count += 1
                continue

            print(f"⏳ Processing: {filename}...")

            image_base64 = encode_image_from_path(image_path, max_size=max_image_size)
            if not image_base64:
                print(f"❌ Could not encode '{filename}' – skipping.")
                error_count += 1
                continue

            try:
                caption = self._send_request(
                    effective_url, backend, model_name,
                    prompt, system_prompt,
                    image_base64, temperature, max_tokens
                )

                with open(caption_path, "w", encoding="utf-8") as f:
                    f.write(caption)

                print(f"✅ Saved caption for '{filename}'.")
                captioned_count += 1

            except Exception as e:
                print(f"❌ Error processing '{filename}': {e}")
                error_count += 1

        status_msg = (
            f"Done. {captioned_count} captions created, "
            f"{skipped_count} skipped, {error_count} errors. "
            f"(Total images: {len(image_files)})"
        )
        print(f"\n[TA-Captioning] {status_msg}\n")
        return (status_msg,)


# ------------------------------------------------------------------ #
#  ComfyUI node registration                                           #
# ------------------------------------------------------------------ #

NODE_CLASS_MAPPINGS         = {"TACaptioning": TACaptioning}
NODE_DISPLAY_NAME_MAPPINGS  = {"TACaptioning": "TA Directory Captioning"}

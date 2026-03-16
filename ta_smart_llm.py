"""
================================================================================
Node Name   : TA Smart LLM
Created     : 2025
Modified    : 2026-03-16
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 3.0
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0


Description:
    Smart LLM integration for LM Studio and Ollama backends with VRAM management.
    Auto-detects vision models (tags with [Vision]), supports image input for
    multimodal prompts, optional pre/post model unloading, and model caching.
    Returns generated prompt text and execution status.
================================================================================
"""

import requests
import torch
import base64
import json
import os
import subprocess
from io import BytesIO
from PIL import Image
import time

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ta_smart_llm_models.json")

# Keywords for automatic vision model detection (lowercase)
VISION_KEYWORDS = ["llava", "vision", "-vl-", "_vl_", "vl-", "vl_", "moondream", "minicpm-v", "internvl", "qwen-vl"]

# Manual additions (exact model names without backend prefix, lowercase)
# Example: VISION_MANUAL = {"my-vision-model-7b", "another-model-13b"}
VISION_MANUAL = set()


def is_vision_model(model_id: str) -> bool:
    lower = model_id.lower()
    if any(kw in lower for kw in VISION_KEYWORDS):
        return True
    if lower in VISION_MANUAL:
        return True
    return False


def tag_model(full_name: str) -> str:
    """
    Adds [Vision] suffix if the model supports image input.
    """
    model_id = '/'.join(full_name.split('/')[1:])
    if is_vision_model(model_id):
        return f"{full_name} [Vision]"
    return full_name


def strip_vision_tag(model: str) -> str:
    """
    Removes [Vision] tag for the API request.
    """
    return model.replace(" [Vision]", "")


class TASmartLLM:
    """
    ComfyUI node for LLM prompt generation via LM Studio or Ollama.
    
    Features:
    - Auto-discovery and caching of available models from both backends
    - Automatic vision model detection and image support
    - Optional VRAM cleanup before LLM inference (unloads ComfyUI image models)
    - Optional LLM unloading after generation to free GPU memory
    - Retry logic for transient API errors
    - Status feedback for workflow debugging
    """

    @classmethod
    def _load_cached_models(cls):
        try:
            with open(CACHE_FILE, "r") as f:
                return set(json.load(f))
        except:
            return set()

    @classmethod
    def _save_cached_models(cls, models):
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(sorted(models), f)
        except:
            pass

    @classmethod
    def get_models(cls):
        """
        Discovers and caches available models from LM Studio (port 1234) and
        Ollama (port 11434). Tags vision-capable models with [Vision] suffix.

        Display logic:
        - All known models are always shown (prevents validation errors).
        - Active models appear at the top of the list, offline models below.
        - No prefix is added to model names so stored values remain stable
          across restarts regardless of which backend is active.
        - Per-backend cache is updated on each call if the backend responds,
          so added/removed models are reflected immediately.
        """
        known = cls._load_cached_models()

        known_lmstudio = {m for m in known if m.startswith("LMStudio/")}
        known_ollama   = {m for m in known if m.startswith("Ollama/")}

        active_lmstudio = set()
        active_ollama   = set()

        # Query LM Studio — replace cache if reachable
        try:
            r = requests.get("http://127.0.0.1:1234/v1/models", timeout=0.5)
            if r.status_code == 200:
                known_lmstudio = {f"LMStudio/{m['id']}" for m in r.json()['data']}
                active_lmstudio = known_lmstudio
        except:
            pass

        # Query Ollama — replace cache if reachable
        try:
            r = requests.get("http://127.0.0.1:11434/api/tags", timeout=0.5)
            if r.status_code == 200:
                known_ollama = {f"Ollama/{m['name']}" for m in r.json()['models']}
                active_ollama = known_ollama
        except:
            pass

        cls._save_cached_models(known_lmstudio | known_ollama)

        active  = sorted(active_lmstudio | active_ollama)
        offline = sorted((known_lmstudio | known_ollama) - (active_lmstudio | active_ollama))

        # Active models first, offline models after — no prefix in stored value
        result = [tag_model(m) for m in active] + [tag_model(m) for m in offline]
        return result if result else ["No Backend"]

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines all input widgets shown in the ComfyUI node UI.

        Required Inputs:
        llm_enable: Master toggle to enable/disable the entire node.
        model: Dropdown of discovered models (LMStudio/Ollama, vision-tagged).
        user_prompt: Main user input prompt (multiline).
        system_prompt: System instruction for the LLM.
        unload_image_models_first: Unload ComfyUI image models before inference.
        unload_llm_after: Unload LLM model from backend after generation.

        Optional Inputs:
        image: IMAGE tensor for vision models (auto-detected).

        Returns:
        dict: ComfyUI INPUT_TYPES dictionary.
        """
        models = cls.get_models()
        return {
            "required": {
                "llm_enable": ("BOOLEAN", {"default": True, "label_on": "✅ LLM ON", "label_off": "❌ OFF"}),
                "model": (models, {"default": models[0] if models else "No Backend"}),
                "user_prompt": ("STRING", {"multiline": True, "default": ""}),
                "system_prompt": ("STRING", {"multiline": True, "default": "You are an expert SD prompt generator."}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.05}),
                "max_tokens": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 64}),
                "unload_image_models_first": ("BOOLEAN", {"default": False}),
                "unload_llm_after": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "image": ("IMAGE",)
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("prompt", "status")
    FUNCTION = "generate"
    CATEGORY = "TA Tools"

    @classmethod
    def IS_CHANGED(cls, llm_enable, model, user_prompt, system_prompt,
                   temperature=0.7, max_tokens=1024,
                   unload_image_models_first=False, unload_llm_after=False,
                   image=None):
        # Wenn deaktiviert: fixer Wert → Node wird von ComfyUI gecacht, kein erneuter Aufruf
        if not llm_enable:
            return "disabled"
        return time.time()

    def _backend_reachable(self, backend, port):
        """
        Checks if LM Studio or Ollama backend is responding.
        """
        try:
            url = f"http://127.0.0.1:{port}/v1/models" if "LMStudio" in backend else f"http://127.0.0.1:{port}/api/tags"
            return requests.get(url, timeout=0.5).status_code == 200
        except:
            return False

    def _unload_comfyui_models(self):
        """
        Unloads all ComfyUI image models from VRAM to free GPU memory.
        """
        try:
            import comfy.model_management as mm
            mm.unload_all_models()
            mm.soft_empty_cache()
        except Exception as e:
            print(f"[TA Smart LLM] Warning: Could not unload image models: {e}")

    def _unload_lmstudio_llm(self):
        """
        Unloads the active LM Studio model via lms CLI tool.
        """
        try:
            subprocess.run(["lms", "unload", "--all"], timeout=15, capture_output=True)
            print(f"[TA Smart LLM] LM Studio model unloaded successfully.")
        except Exception as e:
            print(f"[TA Smart LLM] Warning: Could not unload LM Studio model: {e}")

    def _unload_ollama_llm(self, model_name):
        """
        Unloads an Ollama model by calling it with keep_alive=0.
        """
        try:
            requests.post("http://127.0.0.1:11434/api/generate", json={
                "model": model_name,
                "keep_alive": 0
            }, timeout=10)
            print(f"[TA Smart LLM] Ollama model unloaded successfully: {model_name}")
        except Exception as e:
            print(f"[TA Smart LLM] Warning: Could not unload Ollama model: {e}")

    def _build_image_b64(self, image):
        """
        Converts IMAGE tensor to base64 PNG for vision model input.
        """
        img_array = (255 * image[0].cpu().numpy()).astype('uint8')
        img = Image.fromarray(img_array)
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

    def _post_with_retry(self, url, payload, is_lmstudio, max_retries=3, retry_delay=1.5):
        """
        Posts to LLM API with retry logic for transient errors.
        """
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                r = requests.post(url, json=payload, timeout=120)
                r.raise_for_status()
                return r.json()['choices'][0]['message']['content'] if is_lmstudio else r.json()['response']
            except requests.exceptions.HTTPError as e:
                last_error = e
                if e.response is not None and e.response.status_code in (400, 500, 502, 503) and attempt < max_retries:
                    time.sleep(retry_delay)
                    continue
                raise
            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < max_retries:
                    time.sleep(retry_delay)
                    continue
                raise
        raise last_error

    def generate(self, llm_enable, model, user_prompt, system_prompt,
                 temperature=0.7, max_tokens=1024,
                 unload_image_models_first=False, unload_llm_after=False,
                 image=None):
        """
        Main generation method. Queries the selected LLM and returns prompt + status.

        Workflow:
        1. Skip if disabled or backend unreachable.
        2. Optionally unload ComfyUI models for VRAM.
        3. Build payload (text + optional image b64).
        4. Send request to LM Studio/Ollama with retries.
        5. Optionally unload LLM model after.
        
        Args:
        llm_enable (bool): Master enable toggle.
        model (str): Selected model (tagged).
        user_prompt (str): User input.
        system_prompt (str): System instruction.
        unload_image_models_first (bool): Free VRAM before.
        unload_llm_after (bool): Free VRAM after.
        image: Optional IMAGE for vision models.

        Returns:
        tuple: (generated_prompt: str, status: str)
        """
        if not llm_enable:
            return ("", "DISABLED")

        clean_model = strip_vision_tag(model)
        backend = clean_model.split('/')[0]
        model_name = '/'.join(clean_model.split('/')[1:])
        port = 1234 if "LMStudio" in backend else 11434

        if not self._backend_reachable(backend, port):
            return ("", f"SKIPPED - {backend} not reachable")

        print(f"[TA Smart LLM] Loading model: {clean_model}")

        # Unload ComfyUI image models before LLM request
        if unload_image_models_first:
            self._unload_comfyui_models()

        full_prompt = user_prompt.strip()

        img_b64 = self._build_image_b64(image) if image is not None else None

        try:
            if "LMStudio" in backend:
                url = f"http://127.0.0.1:{port}/v1/chat/completions"
                if img_b64:
                    user_content = [
                        {"type": "text", "text": full_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                    ]
                else:
                    user_content = full_prompt
                payload = {
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }

                result = self._post_with_retry(url, payload, is_lmstudio=True)

                # Unload LM Studio model after request
                if unload_llm_after:
                    self._unload_lmstudio_llm()

            else:  # Ollama
                url = f"http://127.0.0.1:{port}/api/generate"
                payload = {
                    "model": model_name,
                    "prompt": f"{system_prompt}\n\n{full_prompt}".strip(),
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                }

                if img_b64:
                    payload["images"] = [img_b64]
                result = self._post_with_retry(url, payload, is_lmstudio=False)

                # Unload Ollama model after request
                if unload_llm_after:
                    self._unload_ollama_llm(model_name)

            return (result.strip(), f"{clean_model} ✅")

        except Exception as e:
            return (f"ERROR: {str(e)}", clean_model)


NODE_CLASS_MAPPINGS = {"TASmartLLM": TASmartLLM}
NODE_DISPLAY_NAME_MAPPINGS = {"TASmartLLM": "TA Smart LLM v3.0"}

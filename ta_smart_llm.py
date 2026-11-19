"""
================================================================================
Node Name   : TA Smart LLM
Created     : 2025
Modified    : 2026-11-17
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 3.9
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0


Description:
    Smart LLM integration for LM Studio, Ollama, and optional external
    OpenAI-compatible cloud providers (via environment variables) with VRAM
    management. Auto-detects vision models (tags with [Vision]), supports
    image input for multimodal prompts, optional pre/post model unloading,
    and model caching. Returns generated prompt text and execution status.

Changelog:
    3.9  2026-11-17  Add optional cloud LLM providers (Gemini, OpenAI, OpenRouter, Groq) via env vars
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
# VISION_MANUAL = set()
VISION_MANUAL = {"qwen3.5-9b-uncensored-hauhaucs-aggressive"}

# Cloud model prefixes that support multimodal image input
CLOUD_VISION_PREFIXES = ("gemini-", "gpt-4o", "gpt-4.1", "gpt-5", "claude-3", "claude-4", "pixtral")

# Non-chat model substrings to skip when listing cloud provider models
CLOUD_SKIP_MODEL_SUBSTRINGS = ("embedding", "imagen", "veo", "tts", "aqa")

# Optional OpenAI-compatible cloud providers (activated only when env var is set)
CLOUD_PROVIDERS = {
    "Gemini": {
        "env_var": "GEMINI_API_KEY",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "fallback_models": ["gemini-3.8-flash", "gemini-3-flash-preview", "gemini-3.5-flash-lite"],
        "supports_reasoning_effort": True,
    },
    "OpenAI": {
        "env_var": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "fallback_models": ["gpt-4o", "gpt-4o-mini"],
        "supports_reasoning_effort": False,
    },
    "OpenRouter": {
        "env_var": "OPENROUTER_API_KEY",
        "base_url": "https://openrouter.ai/api/v1",
        "fallback_models": ["openrouter/free"],
        "supports_reasoning_effort": False,
    },
    "Groq": {
        "env_var": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "fallback_models": ["llama-3.3-70b-versatile"],
        "supports_reasoning_effort": False,
    },
}


def _get_cloud_api_key(provider: str) -> str:
    """Returns the trimmed API key for a cloud provider from environment variables."""
    cfg = CLOUD_PROVIDERS.get(provider)
    if not cfg:
        return ""
    return os.environ.get(cfg["env_var"], "").strip()


def _sanitize_error(message: str, secret: str = "") -> str:
    """Ensures an API key is never leaked in logs or status outputs."""
    if secret and secret in message:
        return message.replace(secret, "***")
    return message


def is_vision_model(model_id: str) -> bool:
    lower = model_id.lower()
    if any(kw in lower for kw in VISION_KEYWORDS):
        return True
    if any(lower.startswith(prefix) for prefix in CLOUD_VISION_PREFIXES) and not any(
        skip in lower for skip in CLOUD_SKIP_MODEL_SUBSTRINGS
    ):
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
    def _discover_cloud_models(cls, provider, known_provider_models):
        """
        Discovers available models for a configured cloud provider.
        Returns (known_set, active_set) for that provider.
        """
        api_key = _get_cloud_api_key(provider)
        if not api_key:
            return known_provider_models, set()

        cfg = CLOUD_PROVIDERS[provider]
        url = f"{cfg['base_url']}/models"
        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            r = requests.get(url, headers=headers, timeout=2.0)
            if r.status_code == 200:
                discovered = set()
                for m in r.json().get("data", []):
                    m_id = (m.get("id") or "").strip()
                    if not m_id:
                        continue
                    if m_id.startswith("models/"):
                        m_id = m_id[len("models/"):]
                    if any(skip in m_id.lower() for skip in CLOUD_SKIP_MODEL_SUBSTRINGS):
                        continue
                    discovered.add(f"{provider}/{m_id}")
                if discovered:
                    return discovered, discovered
        except Exception:
            pass

        if known_provider_models:
            return known_provider_models, set()

        fallback = {f"{provider}/{m_id}" for m_id in cfg.get("fallback_models", [])}
        return fallback, set()

    @classmethod
    def get_models(cls):
        """
        Discovers and caches available models from LM Studio (port 1234),
        Ollama (port 11434), and configured cloud providers (when API key env
        vars are set). Tags vision-capable models with [Vision] suffix.
        """
        known = cls._load_cached_models()

        known_lmstudio = {m for m in known if m.startswith("LMStudio/")}
        known_ollama   = {m for m in known if m.startswith("Ollama/")}
        known_cloud    = {
            p: {m for m in known if m.startswith(f"{p}/")}
            for p in CLOUD_PROVIDERS
        }

        active_lmstudio = set()
        active_ollama   = set()
        active_cloud    = set()

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

        # Query configured cloud providers (only when env var is set)
        visible_cloud_known = set()
        all_cloud_known = set()
        for provider in CLOUD_PROVIDERS:
            p_known, p_active = cls._discover_cloud_models(provider, known_cloud[provider])
            all_cloud_known |= p_known
            if _get_cloud_api_key(provider):
                visible_cloud_known |= p_known
                active_cloud |= p_active

        cls._save_cached_models(known_lmstudio | known_ollama | all_cloud_known)

        active_all  = active_lmstudio | active_ollama | active_cloud
        visible_all = known_lmstudio | known_ollama | visible_cloud_known

        active  = sorted(active_all)
        offline = sorted(visible_all - active_all)

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
                "request_timeout": ("INT", {"default": 120, "min": 30, "max": 600, "step": 30}),
                "thinking_mode": ("BOOLEAN", {"default": True, "label_on": "✅ Thinking ON", "label_off": "❌ Thinking OFF"}),
                "unload_image_models_first": ("BOOLEAN", {"default": True}),
                "unload_llm_after": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "image": ("IMAGE",)
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt", "status", "reasoning")
    FUNCTION = "generate"
    CATEGORY = "TA Tools"

    @classmethod
    def IS_CHANGED(cls, llm_enable, model, user_prompt, system_prompt,
                   temperature=0.7, max_tokens=1024, request_timeout=120,
                   thinking_mode=False,
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

    def _post_with_retry(self, url, payload, is_openai, headers=None, max_retries=3, retry_delay=1.5, timeout=120):
        """
        Posts to LLM API with retry logic for transient errors (including 429 rate limits).
        For OpenAI-compatible APIs returns the full message dict; for Ollama returns the response string.
        """
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=timeout)
                r.raise_for_status()
                if is_openai:
                    return r.json()['choices'][0]['message']  # Return full message dict
                else:
                    return r.json()['response']
            except requests.exceptions.HTTPError as e:
                last_error = e
                status_code = e.response.status_code if e.response is not None else None
                if status_code in (400, 429, 500, 502, 503) and attempt < max_retries:
                    delay = retry_delay * attempt if status_code == 429 else retry_delay
                    time.sleep(delay)
                    continue
                raise
            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < max_retries:
                    time.sleep(retry_delay)
                    continue
                raise
        raise last_error

    def _build_openai_payload(self, model_name, system_prompt, full_prompt, img_b64,
                              temperature, max_tokens, extra_params=None):
        """Builds a standard OpenAI-compatible /chat/completions payload."""
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
        if extra_params:
            payload.update(extra_params)
        return payload

    def _extract_openai_response(self, message, thinking_mode):
        """Extracts (result, reasoning) from an OpenAI-compatible message dict."""
        content   = (message.get('content') or '').strip()
        reasoning = (message.get('reasoning_content') or '').strip()

        if thinking_mode:
            # Thinking ON -> return full content including thinking
            result = content if content else reasoning
        else:
            # Thinking OFF -> return only the final answer, strip thinking
            if content:
                result = content.split("</think>", 1)[-1].strip() if "</think>" in content else content
            else:
                result = reasoning.split("</think>", 1)[-1].strip() if "</think>" in reasoning else ""

        return result, reasoning

    def generate(self, llm_enable, model, user_prompt, system_prompt,
                 temperature=0.7, max_tokens=1024, request_timeout=120,
                 thinking_mode=False,
                 unload_image_models_first=False, unload_llm_after=False,
                 image=None):
        """
        Main generation method. Queries the selected LLM and returns prompt + status.

        Workflow:
        1. Skip if disabled or backend unreachable / API key missing.
        2. Optionally unload ComfyUI models for VRAM.
        3. Build payload (text + optional image b64).
        4. Send request to LM Studio, Ollama, or configured cloud provider with retries.
        5. Optionally unload local LLM model after.

        Args:
        llm_enable (bool): Master enable toggle.
        model (str): Selected model (tagged).
        user_prompt (str): User input.
        system_prompt (str): System instruction.
        unload_image_models_first (bool): Free VRAM before.
        unload_llm_after (bool): Free VRAM after (local backends only).
        image: Optional IMAGE for vision models.

        Returns:
        tuple: (generated_prompt: str, status: str, reasoning: str)
        """
        if not llm_enable:
            return ("", "DISABLED", "")

        clean_model = strip_vision_tag(model)
        backend = clean_model.split('/')[0]
        model_name = '/'.join(clean_model.split('/')[1:])
        is_cloud = backend in CLOUD_PROVIDERS
        api_key = ""

        if is_cloud:
            api_key = _get_cloud_api_key(backend)
            if not api_key:
                env_var = CLOUD_PROVIDERS[backend]["env_var"]
                return ("", f"SKIPPED - {backend} API key ({env_var}) not set", "")
        else:
            port = 1234 if "LMStudio" in backend else 11434
            if not self._backend_reachable(backend, port):
                return ("", f"SKIPPED - {backend} not reachable", "")

        print(f"[TA Smart LLM] Loading model: {clean_model}")

        # Unload ComfyUI image models before LLM request
        if unload_image_models_first:
            self._unload_comfyui_models()

        full_prompt = user_prompt.strip()
        img_b64 = self._build_image_b64(image) if image is not None else None

        try:
            if is_cloud:
                cfg = CLOUD_PROVIDERS[backend]
                url = f"{cfg['base_url']}/chat/completions"
                headers = {"Authorization": f"Bearer {api_key}"}
                extra_params = None
                if cfg.get("supports_reasoning_effort") and not thinking_mode:
                    extra_params = {"reasoning_effort": "none"}

                payload = self._build_openai_payload(
                    model_name, system_prompt, full_prompt, img_b64,
                    temperature, max_tokens, extra_params=extra_params
                )
                message = self._post_with_retry(
                    url, payload, is_openai=True, headers=headers, timeout=request_timeout
                )
                result, reasoning = self._extract_openai_response(message, thinking_mode)

            elif "LMStudio" in backend:
                url = f"http://127.0.0.1:{port}/v1/chat/completions"
                payload = self._build_openai_payload(
                    model_name, system_prompt, full_prompt, img_b64,
                    temperature, max_tokens
                )
                message = self._post_with_retry(
                    url, payload, is_openai=True, timeout=request_timeout
                )
                result, reasoning = self._extract_openai_response(message, thinking_mode)

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
                result = self._post_with_retry(url, payload, is_openai=False, timeout=request_timeout)
                reasoning = ""

                # Ollama: strip <think> tags if thinking is OFF
                if not thinking_mode and "</think>" in result:
                    reasoning = result.split("</think>", 1)[0].replace("<think>", "").strip()
                    result = result.split("</think>", 1)[-1].strip()

                # Unload Ollama model after request
                if unload_llm_after:
                    self._unload_ollama_llm(model_name)

            if result.strip():
                return (result.strip(), f"{clean_model} ✅", reasoning)
            else:
                return ("", f"WARNING: {clean_model} returned empty response", reasoning)

        except Exception as e:
            return (f"ERROR: {_sanitize_error(str(e), api_key)}", clean_model, "")


NODE_CLASS_MAPPINGS = {"TASmartLLM": TASmartLLM}
NODE_DISPLAY_NAME_MAPPINGS = {"TASmartLLM": "TA Smart LLM v3.9"}

"""
TA LMStudio Smart Loader - Simple & Reliable
Lets LM Studio handle the loading automatically via API
No CLI commands - just waits for model to be ready
"""

import time
import requests
import subprocess


class TALMStudioSmartLoader:
    """
    Simple loader that relies on LM Studio's automatic model loading
    When you send a request to a model, LM Studio loads it automatically
    This node just ensures the model is ready before continuing
    """
    
    _model_paths = {}
    
    # Vision model keywords - 'magistral' HINZUGEFÜGT
    _vision_keywords = [
        'vision', 'llava', 'pixtral', 'minicpm-v', 'cogvlm', 'internvl',
        'molmo', 'aria', 'phi-3-vision', 'phi-3.5-vision',
        'qwen-vl', 'qwen2-vl', 'qwen2.5-vl', 'qwen3-vl', 'qwq-vl',
        'llama-3.1', 'llama-3.2', 'llama3.1', 'llama3.2',
        'gemma-3', 'paligemma',
        'fuyu', 'kosmos', 'idefics', 'otter', 'flamingo', 'blip',
        'deepseek-vl', 'yi-vl', 'mplug', 'sphinx', 'video-llama',
        'ocr', 'gliese',
        'magistral', # Hinzugefügt, um mistralai/magistral-small-2509 als Vision Model zu kennzeichnen
    ]
    
    @classmethod
    def INPUT_TYPES(cls):
        models = cls.get_available_models()
        
        return {
            "required": {
                "model": (models, {
                    "default": models[0] if models else "qwen2-vl-7b-instruct"
                }),
                "server_url": ("STRING", {
                    "default": "http://localhost:1234",
                    "multiline": False
                }),
                "wait_for_ready": ("BOOLEAN", {
                    "default": True,
                    "label_on": "Wait for model",
                    "label_off": "Skip wait"
                }),
                "max_wait": ("INT", {
                    "default": 30,
                    "min": 5,
                    "max": 120,
                    "step": 5,
                    "tooltip": "Maximum seconds to wait for model to be ready"
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("model_name", "status")
    FUNCTION = "prepare_model"
    CATEGORY = "TA-Nodes/LMStudio"

    @classmethod
    def is_vision_model(cls, model_name):
        """Check if model is a vision model"""
        model_lower = model_name.lower()
        
        # Prüft, ob ein positives Vision-Keyword im Modellnamen enthalten ist
        return any(keyword in model_lower for keyword in cls._vision_keywords)

    @classmethod
    def is_valid_model(cls, model_name):
        """Filter out meta entries"""
        if not model_name or len(model_name) < 3:
            return False
        
        blocked = ['embedding', 'llm', 'you', 'default', 'none', 
                   'text-embedding', 'all-minilm', 'bge-', 'e5-']
        
        model_lower = model_name.lower()
        for blocked_term in blocked:
            if model_lower == blocked_term or model_lower.startswith(blocked_term):
                return False
        
        if model_name.isupper() and len(model_name) < 15:
            return False
        
        return True

    @classmethod
    def get_available_models(cls):
        """Get all available models from LM Studio"""
        cls._model_paths = {}
        
        try:
            result = subprocess.run(
                ['lms', 'ls', '--detailed'],
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                models = []
                
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if not line or 'Downloaded models' in line or line.startswith('-'):
                        continue
                    
                    parts = line.split()
                    if not parts:
                        continue
                    
                    full_path = parts[0].lstrip('/')
                    
                    # Create display name
                    if '/' in full_path:
                        path_parts = full_path.split('/')
                        display_name = '/'.join(path_parts[-2:]) if len(path_parts) >= 2 else path_parts[-1]
                    else:
                        display_name = full_path
                    
                    if not cls.is_valid_model(display_name):
                        continue
                    
                    # Mark vision models
                    if cls.is_vision_model(display_name):
                        display_name_marked = f"{display_name} (V)"
                    else:
                        display_name_marked = display_name
                    
                    cls._model_paths[display_name_marked] = full_path
                    models.append(display_name_marked)
                
                if models:
                    # Sort: Vision first
                    vision_models = sorted([m for m in models if '(V)' in m])
                    text_models = sorted([m for m in models if '(V)' not in m])
                    return vision_models + text_models
                else:
                    return cls.get_default_models()
            else:
                return cls.get_default_models()
                
        except Exception as e:
            print(f"[TA-SmartLoader] Error listing models: {e}")
            return cls.get_default_models()
    
    @classmethod
    def get_default_models(cls):
        """Fallback default models"""
        defaults = [
            "qwen2-vl-7b-instruct (V)",
            "llava-v1.5-7b (V)",
            "pixtral-12b (V)",
            "mistral-7b-instruct",
            "llama-3.1-8b-instruct",
        ]
        for model in defaults:
            if model not in cls._model_paths:
                cls._model_paths[model] = model.replace(" (V)", "")
        return defaults

    def check_server_ready(self, server_url):
        """Check if LM Studio server is running"""
        try:
            response = requests.get(f"{server_url}/v1/models", timeout=5)
            return response.status_code == 200
        except:
            return False

    def prepare_model(self, model, server_url, wait_for_ready, max_wait):
        """
        Simply returns the model name and waits if requested
        LM Studio will auto-load the model when it receives a request
        """
        clean_model = model.replace(" (V)", "")
        
        # Extract simple model name for API
        if '/' in clean_model:
            api_name = clean_model.split('/')[-1]
        else:
            api_name = clean_model
        
        print(f"\n{'='*60}")
        print(f"[TA-SmartLoader] Preparing: {model}")
        print(f"[TA-SmartLoader] API Name: {api_name}")
        print(f"[TA-SmartLoader] Server: {server_url}")
        print(f"{'='*60}\n")
        
        # Check if server is running
        if not self.check_server_ready(server_url):
            print(f"[TA-SmartLoader] ⚠ LM Studio server not reachable!")
            print(f"[TA-SmartLoader] Please ensure:")
            print(f"[TA-SmartLoader] 1. LM Studio is running")
            print(f"[TA-SmartLoader] 2. Server is started (→ button in LM Studio)")
            print(f"[TA-SmartLoader] 3. Server URL is correct: {server_url}")
            return (api_name, "Server not ready")
        
        print(f"[TA-SmartLoader] ✓ Server is running")
        
        # Optional: Wait a bit for stability
        if wait_for_ready:
            print(f"[TA-SmartLoader] Waiting 2s for model to be available...")
            time.sleep(2)
            print(f"[TA-SmartLoader] ✓ Ready")
        
        print(f"\n[TA-SmartLoader] ✓✓✓ MODEL READY ✓✓✓")
        print(f"[TA-SmartLoader] LM Studio will auto-load on first request\n")
        
        return (api_name, "Ready - Auto-load enabled")


# Node Registration
NODE_CLASS_MAPPINGS = {
    "TALMStudioSmartLoader": TALMStudioSmartLoader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TALMStudioSmartLoader": "TA LMStudio Smart Loader (Recommended)",
}
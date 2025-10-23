"""
TA LMStudio Model Selector Node
Shows available LM Studio models in a dropdown for selection
"""

import subprocess


class TALMStudioModelSelector:
    """
    Node for selecting LM Studio models from a dropdown
    Lists all installed models
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        models = cls.get_available_models()
        
        return {
            "required": {
                "model": (models, {
                    "default": models[0] if models else "llava-v1.5"
                }),
            },
            "optional": {
                "refresh": ("BOOLEAN", {
                    "default": False,
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_name",)
    FUNCTION = "select_model"
    CATEGORY = "TA-Nodes/LMStudio"

    @classmethod
    def get_available_models(cls):
        """
        Retrieves list of all available LM Studio models
        """
        try:
            result = subprocess.run(
                ['lms', 'ls', '--detailed'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                models = []
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if line.startswith('/'):
                        model_path = line.split()[0].lstrip('/')
                        model_name = model_path.split('/')[-1] if '/' in model_path else model_path
                        models.append(model_name)
                
                if models:
                    models.sort(key=str.lower)  # Case-insensitive alphabetisch sortieren
                    print(f"[TA-ModelSelector] Found {len(models)} models")
                    return models
                else:
                    print("[TA-ModelSelector] No models found, using defaults")
                    return cls.get_default_models()
            else:
                print("[TA-ModelSelector] lms command failed, using defaults")
                return cls.get_default_models()
                
        except FileNotFoundError:
            print("[TA-ModelSelector] lms CLI not found, using defaults")
            return cls.get_default_models()
        except Exception as e:
            print(f"[TA-ModelSelector] Error: {e}, using defaults")
            return cls.get_default_models()
    
    @classmethod
    def get_default_models(cls):
        """
        Fallback: Standard vision models
        """
        models = [
            "llava-v1.5",
            "qwen2-vl-7b-instruct",
            "pixtral-12b",
            "minicpm-v-2.6",
            "gemma-3-27b-it",
        ]
        models.sort(key=str.lower)  # Case-insensitive alphabetisch sortieren
        return models

    @classmethod
    def IS_CHANGED(cls, model, refresh=False):
        if refresh:
            return float("nan")
        return model

    def select_model(self, model, refresh=False):
        print(f"[TA-ModelSelector] Selected model: {model}")
        return (model,)


class TALMStudioLoadedModels:
    """
    Node that displays CURRENTLY LOADED models in LM Studio
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        loaded = cls.get_loaded_models()
        
        return {
            "required": {
                "model": (loaded, {
                    "default": loaded[0] if loaded else "no-model-loaded"
                }),
            },
            "optional": {
                "refresh": ("BOOLEAN", {
                    "default": False
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_name",)
    FUNCTION = "select_model"
    CATEGORY = "TA-Nodes/LMStudio"

    @classmethod
    def get_loaded_models(cls):
        """
        Retrieves list of CURRENTLY LOADED models
        """
        try:
            result = subprocess.run(
                ['lms', 'ps'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                models = []
                lines = result.stdout.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line or 'Currently loaded' in line or line.startswith('-'):
                        continue
                    
                    parts = line.split()
                    if parts:
                        model_name = parts[0]
                        models.append(model_name)
                
                if models:
                    models.sort(key=str.lower)  # Case-insensitive alphabetisch sortieren
                    print(f"[TA-LoadedModels] Currently loaded: {', '.join(models)}")
                    return models
                else:
                    return ["no-model-loaded"]
            else:
                return ["lms-error"]
                
        except Exception as e:
            print(f"[TA-LoadedModels] Error: {e}")
            return ["error-checking-models"]

    @classmethod
    def IS_CHANGED(cls, model, refresh=False):
        if refresh:
            return float("nan")
        return model

    def select_model(self, model, refresh=False):
        if model == "no-model-loaded":
            print("[TA-LoadedModels] WARNING: No model is currently loaded in LM Studio!")
        else:
            print(f"[TA-LoadedModels] Using loaded model: {model}")
        return (model,)


NODE_CLASS_MAPPINGS = {
    "TALMStudioModelSelector": TALMStudioModelSelector,
    "TALMStudioLoadedModels": TALMStudioLoadedModels,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TALMStudioModelSelector": "TA LMStudio Model Selector (All Models)",
    "TALMStudioLoadedModels": "TA LMStudio Model Selector (Loaded Only)",
}

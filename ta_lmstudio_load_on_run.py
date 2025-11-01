"""
TA LMStudio Load On Run Node - With Vision Model Marking
Marks vision models with (V) in the dropdown
"""

import subprocess
import time
import re


class TALMStudioLoadOnRun:
    """
    Node with vision model marking
    """
    
    _model_paths = {}
    _vision_keywords = [
        # Explicit vision keywords
        'vision', 'llava', 'pixtral', 'minicpm-v', 'cogvlm', 'internvl',
        'molmo', 'aria', 'phi-3-vision', 'phi-3.5-vision',
        # Qwen: ONLY VL variants are vision
        'qwen-vl', 'qwen2-vl', 'qwen2.5-vl', 'qwen3-vl', 'qwq-vl',
        # Llama: ONLY 3.1 and 3.2 have vision
        'llama-3.1', 'llama-3.2', 'llama3.1', 'llama3.2',
        # Gemma: ONLY Gemma 3 (Gemini-based) has vision
        'gemma-3', 'paligemma',
        # Other known vision models
        'fuyu', 'kosmos', 'idefics', 'otter', 'flamingo', 'blip',
        'deepseek-vl', 'yi-vl', 'mplug', 'sphinx', 'video-llama',
        # OCR models
        'ocr', 'gliese',
    ]
    
    @classmethod
    def INPUT_TYPES(cls):
        models = cls.get_available_models()
        
        return {
            "required": {
                "model": (models, {
                    "default": models[0] if models else "llava-v1.5"
                }),
                "context_length": ("INT", {
                    "default": 4096,
                    "min": 512,
                    "max": 131072,
                    "step": 512
                }),
                "gpu_mode": (["auto", "gpu_only", "hybrid", "cpu_only"], {
                    "default": "auto",
                    "tooltip": "auto=let LMStudio decide, gpu_only=all on GPU, hybrid=GPU+CPU (for 27B), cpu_only=CPU only"
                }),
                "wait_time": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 30,
                    "step": 1,
                    "display": "number",
                    "tooltip": "Seconds to wait after loading (10-15s for large models)"
                }),
                "unload_wait": ("INT", {
                    "default": 5,
                    "min": 0,
                    "max": 20,
                    "step": 1,
                    "display": "number",
                    "tooltip": "Extra seconds after unload for VRAM cleanup"
                }),
                "skip_unload": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Skip unload",
                    "label_off": "Try unload",
                    "tooltip": "Skip unload if it keeps failing"
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("model_name", "status")
    FUNCTION = "load_and_return"
    CATEGORY = "TA-Nodes/LMStudio"

    @classmethod
    def is_valid_model(cls, model_name):
        """
        Checks if an entry is a real model
        Filters meta entries like EMBEDDING, LLM, You, etc.
        """
        if not model_name or len(model_name) < 3:
            return False
        
        # Filter: Known meta entries (case-insensitive)
        blocked_entries = [
            'embedding', 'llm', 'you', 'default', 'none', 
            'text-embedding', 'all-minilm', 'bge-', 'e5-'
        ]
        
        model_lower = model_name.lower()
        for blocked in blocked_entries:
            if model_lower == blocked or model_lower.startswith(blocked):
                return False
        
        # Filter: Only uppercase letters (probably a category)
        if model_name.isupper() and len(model_name) < 15:
            return False
        
        return True
    
    @classmethod
    def is_vision_model(cls, model_name):
        """
        Checks if a model is a vision model
        Based on known vision model keywords
        """
        model_lower = model_name.lower()
        
        for keyword in cls._vision_keywords:
            if keyword in model_lower:
                return True
        
        return False

    @classmethod
    def get_available_models(cls):
        """Gets ALL available models and marks vision models"""
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
                lines = result.stdout.split('\n')
                
                for line in lines:
                    line = line.strip()
                    
                    if not line or 'Downloaded models' in line or line.startswith('-'):
                        continue
                    
                    parts = line.split()
                    if not parts:
                        continue
                    
                    full_path = parts[0]
                    if full_path.startswith('/'):
                        full_path = full_path.lstrip('/')
                    
                    # Create display name
                    if '/' in full_path:
                        path_parts = full_path.split('/')
                        if len(path_parts) >= 2:
                            display_name = '/'.join(path_parts[-2:])
                        else:
                            display_name = path_parts[-1]
                    else:
                        display_name = full_path
                    
                    # FILTER: Skip meta entries
                    if not cls.is_valid_model(display_name):
                        continue
                    
                    # CHECK IF VISION MODEL
                    if cls.is_vision_model(display_name):
                        # Add (V) for vision models
                        display_name_marked = f"{display_name} (V)"
                    else:
                        display_name_marked = display_name
                    
                    # Store both: marked name → full path
                    cls._model_paths[display_name_marked] = full_path
                    models.append(display_name_marked)
                
                if models:
                    # Sort: Vision models first, then alphabetically
                    vision_models = [m for m in models if '(V)' in m]
                    text_models = [m for m in models if '(V)' not in m]
                    
                    vision_models.sort()
                    text_models.sort()
                    
                    # Vision models first
                    sorted_models = vision_models + text_models
                    
                    return sorted_models
                else:
                    return cls.get_default_models()
            else:
                return cls.get_default_models()
                
        except Exception as e:
            print(f"[TA-LoadOnRun] Error listing models: {e}")
            return cls.get_default_models()
    
    @classmethod
    def get_default_models(cls):
        defaults = [
            "llava-v1.5-7b (V)",
            "qwen2-vl-7b-instruct (V)",
            "pixtral-12b (V)",
            "google/gemma-3-27b (V)",
            "llama-3.1-unhinged-vision-8b (V)",
        ]
        for model in defaults:
            if model not in cls._model_paths:
                # Remove (V) for the path
                model_path = model.replace(" (V)", "")
                cls._model_paths[model] = model_path
        return defaults

    def try_unload(self, unload_wait=5):
        """Attempts to unload with extended cleanup time"""
        print("[TA-LoadOnRun] Attempting to unload models...")
        
        try:
            result = subprocess.run(
                ['lms', 'unload', '--all', '-y'],
                capture_output=True,
                text=True,
                timeout=15,
                encoding='utf-8',
                errors='replace'
            )
            
            output = (result.stdout + result.stderr).lower()
            
            if 'no models to unload' in output or 'no models loaded' in output:
                print(f"[TA-LoadOnRun] ✓ No models loaded")
                return True
            elif result.returncode == 0 or 'unloaded' in output:
                print(f"[TA-LoadOnRun] ✓ Models unloaded")
                if unload_wait > 0:
                    print(f"[TA-LoadOnRun] Waiting {unload_wait}s for VRAM cleanup...")
                    time.sleep(unload_wait)
                return True
            else:
                print(f"[TA-LoadOnRun] ⚠ Unload code {result.returncode}, continuing...")
                time.sleep(min(unload_wait, 3))
                return False
                
        except subprocess.TimeoutExpired:
            print(f"[TA-LoadOnRun] ⚠ Unload timeout")
            time.sleep(min(unload_wait, 3))
            return False
        except Exception as e:
            print(f"[TA-LoadOnRun] ⚠ Unload error: {e}")
            return False

    def is_model_loaded(self, model_name):
        """Checks if model is loaded"""
        try:
            result = subprocess.run(
                ['lms', 'ps'],
                capture_output=True,
                text=True,
                timeout=5,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                output = result.stdout
                # Remove (V) from name for comparison
                clean_name = model_name.replace(" (V)", "")
                full_path = self._model_paths.get(model_name, clean_name)
                
                if clean_name in output or full_path in output:
                    return True
                
                name_parts = clean_name.replace('/', ' ').split()
                for part in name_parts:
                    if len(part) > 4 and part in output:
                        return True
                
                return False
            return False
        except:
            return False

    def wait_for_model_ready(self, model_name, max_wait=20):
        """Waits until model is ready"""
        print(f"[TA-LoadOnRun] Verifying model is ready...")
        
        for i in range(max_wait):
            if self.is_model_loaded(model_name):
                print(f"[TA-LoadOnRun] ✓ Model verified after {i+1}s")
                return True
            
            if i == 0 or (i+1) % 5 == 0:
                print(f"[TA-LoadOnRun]   Checking... ({i+1}/{max_wait}s)")
            
            time.sleep(1)
        
        print(f"[TA-LoadOnRun] ⚠ Could not verify model after {max_wait}s")
        return False

    def load_model(self, display_name, context_length, gpu_mode, wait_time, unload_wait, skip_unload):
        """Loads model with flexible GPU mode"""
        clean_name = display_name.replace(" (V)", "")
        full_path = self._model_paths.get(display_name, clean_name)
        
        print(f"[TA-LoadOnRun] === LOADING MODEL ===")
        print(f"[TA-LoadOnRun] Model: {display_name}")
        print(f"[TA-LoadOnRun] Path: {full_path}")
        print(f"[TA-LoadOnRun] Context: {context_length}")
        print(f"[TA-LoadOnRun] GPU Mode: {gpu_mode}")
        print(f"[TA-LoadOnRun] Wait: {wait_time}s / Unload wait: {unload_wait}s")
        
        # Check if model is too large
        is_large_model = any(x in display_name.lower() for x in ['27b', '30b', '34b', '70b'])
        if is_large_model and gpu_mode == "gpu_only":
            print(f"\n{'!'*60}")
            print(f"[TA-LoadOnRun] ⚠⚠⚠ WARNING ⚠⚠⚠")
            print(f"[TA-LoadOnRun] Large model ({display_name}) with gpu_only!")
            print(f"[TA-LoadOnRun] This will likely fail on 24GB VRAM")
            print(f"[TA-LoadOnRun] Recommended: Use 'hybrid' or 'auto' mode")
            print(f"{'!'*60}\n")
        
        try:
            # Unload if needed
            if not skip_unload:
                self.try_unload(unload_wait)
            else:
                print(f"[TA-LoadOnRun] Skipping unload")
            
            # Build load command
            load_cmd = ['lms', 'load', full_path, '-y', f'--context-length={context_length}']
            
            # Set GPU mode
            if gpu_mode == "gpu_only":
                load_cmd.append('--gpu=max')
            elif gpu_mode == "hybrid":
                load_cmd.append('--gpu=1')  # Standard GPU with automatic offload
            elif gpu_mode == "cpu_only":
                load_cmd.append('--gpu=0')
            else:  # auto
                # Let LM Studio decide based on model size
                if is_large_model:
                    load_cmd.append('--gpu=1')  # Use hybrid for large models
                    print(f"[TA-LoadOnRun] Auto mode: Using hybrid (GPU+CPU) for large model")
                else:
                    load_cmd.append('--gpu=max')
                    print(f"[TA-LoadOnRun] Auto mode: Using gpu_only for standard model")
            
            print(f"[TA-LoadOnRun] Command: {' '.join(load_cmd)}")
            
            result = subprocess.run(
                load_cmd,
                capture_output=True,
                text=True,
                timeout=180,
                encoding='utf-8',
                errors='replace'
            )
            
            # Check for VRAM errors
            error_text = (result.stdout + result.stderr).lower()
            has_vram_error = any(x in error_text for x in [
                'unable to allocate', 'cuda', 'out of memory', 'vram'
            ])
            
            if has_vram_error:
                print(f"\n{'='*60}")
                print(f"[TA-LoadOnRun] ⚠⚠⚠ VRAM ALLOCATION ERROR ⚠⚠⚠")
                print(f"[TA-LoadOnRun]")
                print(f"[TA-LoadOnRun] Model: {display_name}")
                print(f"[TA-LoadOnRun] This model is TOO LARGE for your 24GB VRAM!")
                print(f"[TA-LoadOnRun]")
                print(f"[TA-LoadOnRun] 💡 QUICK FIXES (in order of effectiveness):")
                print(f"[TA-LoadOnRun]")
                print(f"[TA-LoadOnRun] 1. Use HYBRID mode instead of gpu_only")
                print(f"[TA-LoadOnRun]    → Change gpu_mode to 'hybrid'")
                print(f"[TA-LoadOnRun]")
                print(f"[TA-LoadOnRun] 2. Use a SMALLER model (Recommended!)")
                print(f"[TA-LoadOnRun]    → llava-v1.5-13b (V)")
                print(f"[TA-LoadOnRun]    → qwen2-vl-7b-instruct (V)")
                print(f"[TA-LoadOnRun]    → pixtral-12b (V)")
                print(f"[TA-LoadOnRun]")
                print(f"[TA-LoadOnRun] 3. Reduce context to 512-1024")
                print(f"[TA-LoadOnRun]")
                print(f"[TA-LoadOnRun] 4. Use smaller quantization")
                print(f"[TA-LoadOnRun]    → Q3_K_M or Q2_K instead of Q4_0")
                print(f"{'='*60}\n")
            
            if result.returncode == 0:
                print(f"[TA-LoadOnRun] ✓ Load completed")
                print(f"[TA-LoadOnRun] Waiting {wait_time}s for initialization...")
                time.sleep(wait_time)
                
                if self.wait_for_model_ready(display_name, max_wait=20):
                    print(f"[TA-LoadOnRun] ✓✓✓ MODEL READY ✓✓✓")
                    return True, "Loaded and ready"
                else:
                    print(f"[TA-LoadOnRun] ⚠ Verification failed, might still work")
                    return True, "Loaded (not verified)"
            else:
                print(f"[TA-LoadOnRun] ✗ Load failed (code {result.returncode})")
                if result.stderr:
                    print(f"[TA-LoadOnRun] Error: {result.stderr[:400]}")
                return False, f"Load failed"
                
        except subprocess.TimeoutExpired:
            print("[TA-LoadOnRun] ✗ Timeout (>180s)")
            return False, "Timeout"
        except Exception as e:
            print(f"[TA-LoadOnRun] ✗ Error: {e}")
            return False, f"Error: {str(e)}"

    def load_and_return(self, model, context_length, gpu_mode, wait_time, unload_wait, skip_unload):
        """Executed on RUN"""
        
        clean_model = model.replace(" (V)", "")
        if '/' in clean_model:
            api_name = clean_model.split('/')[-1]
        else:
            api_name = clean_model
        
        print(f"\n{'='*60}")
        print(f"[TA-LoadOnRun] ===== WORKFLOW START =====")
        print(f"[TA-LoadOnRun] Model: {model}")
        print(f"[TA-LoadOnRun] Context: {context_length}")
        print(f"[TA-LoadOnRun] GPU Mode: {gpu_mode}")
        print(f"[TA-LoadOnRun] Wait: {wait_time}s | Unload: {unload_wait}s")
        print(f"{'='*60}\n")
        
        success, status = self.load_model(model, context_length, gpu_mode, wait_time, unload_wait, skip_unload)
        
        if success:
            print(f"\n[TA-LoadOnRun] ✓ READY FOR VISION NODE\n")
        else:
            print(f"\n[TA-LoadOnRun] ✗ LOAD FAILED - See tips above\n")
        
        return (api_name, status)


# Node Registration
NODE_CLASS_MAPPINGS = {
    "TALMStudioLoadOnRun": TALMStudioLoadOnRun,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TALMStudioLoadOnRun": "TA LMStudio Load (On Run)",
}

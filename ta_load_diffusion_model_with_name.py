import folder_paths
import comfy.sd
import os
import torch

class TALoadDiffusionModelWithName:
    """
    Lädt ein Diffusion-Modell (UNet) und gibt zusätzlich den Modellnamen aus
    Kompatibel mit PyTorch 2.8+
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "unet_name": (folder_paths.get_filename_list("diffusion_models"),),
                "weight_dtype": (["default", "fp8_e4m3fn", "fp8_e5m2"], {"default": "default"}),
            }
        }
    
    RETURN_TYPES = ("MODEL", "STRING")
    RETURN_NAMES = ("model", "model_name")
    FUNCTION = "load_unet"
    CATEGORY = "TA Nodes/loaders"
    
    def load_unet(self, unet_name, weight_dtype):
        # Lade das Diffusion Model (UNet)
        unet_path = folder_paths.get_full_path("diffusion_models", unet_name)
        
        # Bestimme die model_options basierend auf weight_dtype
        model_options = {}
        if weight_dtype == "fp8_e4m3fn":
            model_options["weight_dtype"] = torch.float8_e4m3fn
        elif weight_dtype == "fp8_e5m2":
            model_options["weight_dtype"] = torch.float8_e5m2
        # "default" bedeutet keine speziellen Optionen
        
        # PyTorch 2.8+ kompatibles Laden mit Kontext-Manager
        with torch.inference_mode():
            if model_options:
                model = comfy.sd.load_diffusion_model(unet_path, model_options=model_options)
            else:
                model = comfy.sd.load_diffusion_model(unet_path)
        
        # Extrahiere nur den Dateinamen ohne Pfad und Erweiterung
        model_name_only = os.path.splitext(os.path.basename(unet_name))[0]
        
        # Gebe Model und bereinigten Namen zurück
        return (model, model_name_only)


NODE_CLASS_MAPPINGS = {
    "TALoadDiffusionModelWithName": TALoadDiffusionModelWithName
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TALoadDiffusionModelWithName": "TA Load Diffusion Model (with Name)"
}
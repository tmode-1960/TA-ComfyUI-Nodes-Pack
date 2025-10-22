import folder_paths
import comfy.sd
import os
import logging
import sys
import traceback
import io
from contextlib import redirect_stderr, redirect_stdout

class TALoadGGUFModelWithName:
    """
    Lädt ein GGUF-Modell und gibt zusätzlich den Modellnamen aus
    Stille Version ohne Debug-Ausgaben
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        # Suche GGUF-Dateien in verschiedenen Verzeichnissen
        unet_names = []
        
        # Primär: unet_gguf Verzeichnis
        try:
            unet_names = folder_paths.get_filename_list("unet_gguf")
        except:
            pass
        
        # Fallback: unet Verzeichnis mit .gguf Filter
        if not unet_names:
            try:
                all_files = folder_paths.get_filename_list("unet")
                unet_names = [x for x in all_files if x.endswith(".gguf")]
            except:
                pass
        
        # Zweiter Fallback: diffusion_models mit .gguf Filter  
        if not unet_names:
            try:
                all_files = folder_paths.get_filename_list("diffusion_models")
                unet_names = [x for x in all_files if x.endswith(".gguf")]
            except:
                pass
        
        return {
            "required": {
                "unet_name": (unet_names if unet_names else ["No GGUF files found"],),
            }
        }
    
    RETURN_TYPES = ("MODEL", "STRING")
    RETURN_NAMES = ("model", "model_name")
    FUNCTION = "load_unet"
    CATEGORY = "TA Nodes/loaders"
    TITLE = "TA Load GGUF Model (with Name)"
    
    def load_unet(self, unet_name):
        # Versuche die Datei in verschiedenen Verzeichnissen zu finden
        unet_path = None
        for folder_type in ["unet_gguf", "unet", "diffusion_models"]:
            try:
                potential_path = folder_paths.get_full_path(folder_type, unet_name)
                if potential_path and os.path.exists(potential_path):
                    unet_path = potential_path
                    break
            except:
                continue
        
        if unet_path is None:
            raise FileNotFoundError(f"Could not find {unet_name} in any model directory")
        
        gguf_node_path = os.path.join(folder_paths.base_path, "custom_nodes", "ComfyUI-GGUF")
        model = None
        
        # Methode 1: Direkt die GGUF nodes.py importieren (ohne Ausgaben)
        try:
            if gguf_node_path not in sys.path:
                sys.path.insert(0, gguf_node_path)
            
            # Unterdrücke alle Ausgaben während des Imports
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                try:
                    from nodes import UnetLoaderGGUF
                    loader = UnetLoaderGGUF()
                    result = loader.load_unet(unet_name)
                    model = result[0]
                except ImportError:
                    # Alternative Import-Methode
                    import importlib.util
                    nodes_path = os.path.join(gguf_node_path, "nodes.py")
                    if os.path.exists(nodes_path):
                        spec = importlib.util.spec_from_file_location("gguf_nodes", nodes_path)
                        gguf_nodes = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(gguf_nodes)
                        
                        if hasattr(gguf_nodes, 'UnetLoaderGGUF'):
                            loader = gguf_nodes.UnetLoaderGGUF()
                            result = loader.load_unet(unet_name)
                            model = result[0]
        except:
            pass
        
        # Methode 2: Verwende die registrierte Node (ohne Ausgaben)
        if model is None:
            try:
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    from nodes import NODE_CLASS_MAPPINGS
                    
                    if "UnetLoaderGGUF" in NODE_CLASS_MAPPINGS:
                        loader_class = NODE_CLASS_MAPPINGS["UnetLoaderGGUF"]
                        loader = loader_class()
                        result = loader.load_unet(unet_name)
                        model = result[0]
            except:
                pass
        
        # Methode 3: Versuche die GGUF-spezifischen Module zu importieren (ohne Ausgaben)
        if model is None:
            try:
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    sys.path.insert(0, gguf_node_path)
                    
                    from gguf import GGUFReader
                    from ops import GGMLOps, GGMLLayer, GGMLTensor
                    from loader import gguf_sd_loader
                    
                    ops = GGMLOps()
                    sd = gguf_sd_loader(unet_path)
                    
                    model = comfy.sd.load_diffusion_model_state_dict(
                        sd, model_options={"custom_operations": ops}
                    )
            except:
                pass
        
        # Wenn alles fehlschlägt
        if model is None:
            error_msg = (
                f"Could not load GGUF model: {unet_name}\n\n"
                f"Please check:\n"
                f"1. ComfyUI-GGUF is properly installed\n"
                f"2. All dependencies are installed (gguf package)\n"
                f"3. The GGUF file is not corrupted"
            )
            raise RuntimeError(error_msg)
        
        # Extrahiere nur den Dateinamen ohne Pfad und Erweiterung
        model_name_only = os.path.splitext(os.path.basename(unet_name))[0]
        
        return (model, model_name_only)


NODE_CLASS_MAPPINGS = {
    "TALoadGGUFModelWithName": TALoadGGUFModelWithName
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TALoadGGUFModelWithName": "TA Load GGUF Model (with Name)"
}
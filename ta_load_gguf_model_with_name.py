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
    Loads a GGUF model and additionally outputs the model name
    Silent version without debug output
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        # Search for GGUF files in various directories
        unet_names = []
        
        # Primary: unet_gguf directory
        try:
            unet_names = folder_paths.get_filename_list("unet_gguf")
        except:
            pass
        
        # Fallback: unet directory with .gguf filter
        if not unet_names:
            try:
                all_files = folder_paths.get_filename_list("unet")
                unet_names = [x for x in all_files if x.endswith(".gguf")]
            except:
                pass
        
        # Second fallback: diffusion_models with .gguf filter
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
        # Try to find the file in various directories
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
        
        # Method 1: Directly import the GGUF nodes.py (without output)
        try:
            if gguf_node_path not in sys.path:
                sys.path.insert(0, gguf_node_path)
            
            # Suppress all output during import
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                try:
                    from nodes import UnetLoaderGGUF
                    loader = UnetLoaderGGUF()
                    result = loader.load_unet(unet_name)
                    model = result[0]
                except ImportError:
                    # Alternative import method
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
        
        # Method 2: Use the registered node (without output)
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
        
        # Method 3: Try to import GGUF-specific modules (without output)
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
        
        # If everything fails
        if model is None:
            error_msg = (
                f"Could not load GGUF model: {unet_name}\n\n"
                f"Please check:\n"
                f"1. ComfyUI-GGUF is properly installed\n"
                f"2. All dependencies are installed (gguf package)\n"
                f"3. The GGUF file is not corrupted"
            )
            raise RuntimeError(error_msg)
        
        # Extract only the filename without path and extension
        model_name_only = os.path.splitext(os.path.basename(unet_name))[0]
        
        return (model, model_name_only)


NODE_CLASS_MAPPINGS = {
    "TALoadGGUFModelWithName": TALoadGGUFModelWithName
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TALoadGGUFModelWithName": "TA Load GGUF Model (with Name)"
}

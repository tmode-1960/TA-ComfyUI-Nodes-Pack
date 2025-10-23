import folder_paths
import comfy.sd
import os
import torch

class TALoadCheckpointModelWithName:
    """
    Loads a checkpoint model and additionally outputs the model name
    Compatible with PyTorch 2.8+
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ckpt_name": (folder_paths.get_filename_list("checkpoints"),),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING")
    RETURN_NAMES = ("model", "clip", "vae", "model_name")
    FUNCTION = "load_checkpoint"
    CATEGORY = "TA Nodes/loaders"
    
    def load_checkpoint(self, ckpt_name):
        # Load the checkpoint
        ckpt_path = folder_paths.get_full_path("checkpoints", ckpt_name)
        
        # PyTorch 2.8+ compatible loading with context manager
        with torch.inference_mode():
            out = comfy.sd.load_checkpoint_guess_config(
                ckpt_path,
                output_vae=True,
                output_clip=True,
                embedding_directory=folder_paths.get_folder_paths("embeddings")
            )
        
        # Extract Model, CLIP and VAE
        model = out[0]
        clip = out[1]
        vae = out[2]
        
        # Extract only the filename without path and extension
        model_name_only = os.path.splitext(os.path.basename(ckpt_name))[0]
        
        # Return the cleaned model name as well
        return (model, clip, vae, model_name_only)


NODE_CLASS_MAPPINGS = {
    "TALoadCheckpointModelWithName": TALoadCheckpointModelWithName
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TALoadCheckpointModelWithName": "TA Load Checkpoint Model (with Name)"
}

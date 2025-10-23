"""
TA Nodes Pack - Custom Nodes for ComfyUI
Contains nodes for loading various model types with names and text processing
Plus LM Studio Vision Integration for Image-to-Prompt
Plus LM Studio Load On Run for controlled model loading
"""

# Import base loader nodes
from .ta_load_checkpoint_model_with_name import TALoadCheckpointModelWithName
from .ta_load_diffusion_model_with_name import TALoadDiffusionModelWithName
from .ta_load_gguf_model_with_name import TALoadGGUFModelWithName

# Import LM Studio Vision Nodes
from .ta_ebu_lmstudio_vision_node import (
    NODE_CLASS_MAPPINGS as LMSTUDIO_VISION_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS as LMSTUDIO_VISION_DISPLAY
)

# Import LM Studio Load On Run Node
from .ta_lmstudio_load_on_run import (
    NODE_CLASS_MAPPINGS as LOAD_ON_RUN_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS as LOAD_ON_RUN_DISPLAY
)

# Import LM Studio Model Selector Nodes
from .ta_lmstudio_model_selector import (
    NODE_CLASS_MAPPINGS as MODEL_SELECTOR_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS as MODEL_SELECTOR_DISPLAY
)

# Node class mappings - Base loaders
NODE_CLASS_MAPPINGS = {
    "TALoadCheckpointModelWithName": TALoadCheckpointModelWithName,
    "TALoadDiffusionModelWithName": TALoadDiffusionModelWithName,
    "TALoadGGUFModelWithName": TALoadGGUFModelWithName,
}

# Add LM Studio Vision Nodes
NODE_CLASS_MAPPINGS.update(LMSTUDIO_VISION_MAPPINGS)

# Add LM Studio Load On Run Node
NODE_CLASS_MAPPINGS.update(LOAD_ON_RUN_MAPPINGS)

# Add LM Studio Model Selector Nodes
NODE_CLASS_MAPPINGS.update(MODEL_SELECTOR_MAPPINGS)

# Display names for the UI - Base loaders
NODE_DISPLAY_NAME_MAPPINGS = {
    "TALoadCheckpointModelWithName": "TA Load Checkpoint Model (with Name)",
    "TALoadDiffusionModelWithName": "TA Load Diffusion Model (with Name)",
    "TALoadGGUFModelWithName": "TA Load GGUF Model (with Name)",
}

# Add LM Studio Vision display names
NODE_DISPLAY_NAME_MAPPINGS.update(LMSTUDIO_VISION_DISPLAY)

# Add LM Studio Load On Run display names
NODE_DISPLAY_NAME_MAPPINGS.update(LOAD_ON_RUN_DISPLAY)

# Add LM Studio Model Selector display names
NODE_DISPLAY_NAME_MAPPINGS.update(MODEL_SELECTOR_DISPLAY)

# Export for ComfyUI
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

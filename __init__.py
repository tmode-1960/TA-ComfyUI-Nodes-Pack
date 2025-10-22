"""
TA Nodes Pack - Custom Nodes für ComfyUI
Enthält Nodes zum Laden verschiedener Modelltypen mit Namen und Text-Processing
Plus LM Studio Vision Integration für Image-to-Prompt
Plus LM Studio Load On Run für kontrolliertes Laden von Modellen
"""

from .ta_load_checkpoint_model_with_name import TALoadCheckpointModelWithName
from .ta_load_diffusion_model_with_name import TALoadDiffusionModelWithName
from .ta_load_gguf_model_with_name import TALoadGGUFModelWithName

# Importiere LM Studio Vision Nodes
from .ta_ebu_lmstudio_vision_node import (
    NODE_CLASS_MAPPINGS as LMSTUDIO_VISION_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS as LMSTUDIO_VISION_DISPLAY
)

# Importiere LM Studio Load On Run Node
from .ta_lmstudio_load_on_run import (
    NODE_CLASS_MAPPINGS as LOAD_ON_RUN_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS as LOAD_ON_RUN_DISPLAY
)

# Node-Klassen-Mappings
NODE_CLASS_MAPPINGS = {
    "TALoadCheckpointModelWithName": TALoadCheckpointModelWithName,
    "TALoadDiffusionModelWithName": TALoadDiffusionModelWithName,
    "TALoadGGUFModelWithName": TALoadGGUFModelWithName,
}

# Füge LM Studio Vision Nodes hinzu
NODE_CLASS_MAPPINGS.update(LMSTUDIO_VISION_MAPPINGS)

# Füge LM Studio Load On Run Node hinzu
NODE_CLASS_MAPPINGS.update(LOAD_ON_RUN_MAPPINGS)

# Display-Namen für die UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "TALoadCheckpointModelWithName": "TA Load Checkpoint Model (with Name)",
    "TALoadDiffusionModelWithName": "TA Load Diffusion Model (with Name)",
    "TALoadGGUFModelWithName": "TA Load GGUF Model (with Name)",
}

# Füge LM Studio Vision Display Names hinzu
NODE_DISPLAY_NAME_MAPPINGS.update(LMSTUDIO_VISION_DISPLAY)

# Füge LM Studio Load On Run Display Names hinzu
NODE_DISPLAY_NAME_MAPPINGS.update(LOAD_ON_RUN_DISPLAY)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

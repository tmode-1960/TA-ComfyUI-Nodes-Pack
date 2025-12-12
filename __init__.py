"""
TA Nodes Pack - Custom Nodes for ComfyUI
Version: 1.0.9 (Updated for ta_captioning)
"""

# 1. Base Loader Nodes
from .ta_load_checkpoint_model_with_name import TALoadCheckpointModelWithName
from .ta_load_diffusion_model_with_name import TALoadDiffusionModelWithName
from .ta_load_gguf_model_with_name import TALoadGGUFModelWithName

# 2. LM Studio Vision Nodes (Image2Prompt & Tools)
from .ta_ebu_lmstudio_vision_node import (
    NODE_CLASS_MAPPINGS as LMSTUDIO_VISION_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS as LMSTUDIO_VISION_DISPLAY
)

# 3. LM Studio Load On Run Node
from .ta_lmstudio_load_on_run import (
    NODE_CLASS_MAPPINGS as LOAD_ON_RUN_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS as LOAD_ON_RUN_DISPLAY
)

# 4. LM Studio Smart Loader
try:
    from .ta_lmstudio_smart_loader import (
        NODE_CLASS_MAPPINGS as SMART_LOADER_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS as SMART_LOADER_DISPLAY
    )
    HAS_SMART_LOADER = True
except ImportError:
    print("[TA-Nodes] Smart Loader not found - install ta_lmstudio_smart_loader.py")
    HAS_SMART_LOADER = False

# 5. LM Studio Model Selector Nodes
from .ta_lmstudio_model_selector import (
    NODE_CLASS_MAPPINGS as MODEL_SELECTOR_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS as MODEL_SELECTOR_DISPLAY
)

# 6. TA Filename Generator
try:
    from .ta_filename_generator import TAFilenameGenerator
    HAS_FILENAME_GENERATOR = True
except ImportError:
    print("[TA-Nodes] TA Filename Generator not found - install ta_filename_generator.py")
    HAS_FILENAME_GENERATOR = False

# 7. TA Prompt Controller (NEU)
try:
    from .ta_prompt_controller import TAPromptController
    HAS_PROMPT_CONTROLLER = True
except ImportError:
    print("[TA-Nodes] TA Prompt Controller not found - install ta_prompt_controller.py")
    HAS_PROMPT_CONTROLLER = False

# 8. TA Directory Captioning Node (NEU)
try:
    from .ta_directory_captioning_node import ta_captioning
    HAS_CAPTIONING_NODE = True
except ImportError:
    print("[TA-Nodes] TA Directory Captioning Node not found - install ta_directory_captioning_node.py")
    HAS_CAPTIONING_NODE = False

# --------------------------------------------------------------------------------
# NODE REGISTRATION
# --------------------------------------------------------------------------------

# Initialize Mappings with Base Loaders
NODE_CLASS_MAPPINGS = {
    "TALoadCheckpointModelWithName": TALoadCheckpointModelWithName,
    "TALoadDiffusionModelWithName": TALoadDiffusionModelWithName,
    "TALoadGGUFModelWithName": TALoadGGUFModelWithName,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TALoadCheckpointModelWithName": "TA Load Checkpoint Model (with Name)",
    "TALoadDiffusionModelWithName": "TA Load Diffusion Model (with Name)",
    "TALoadGGUFModelWithName": "TA Load GGUF Model (with Name)",
}

# Add LM Studio Vision Nodes
NODE_CLASS_MAPPINGS.update(LMSTUDIO_VISION_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(LMSTUDIO_VISION_DISPLAY)

# Add LM Studio Load On Run Node
NODE_CLASS_MAPPINGS.update(LOAD_ON_RUN_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(LOAD_ON_RUN_DISPLAY)

# Add LM Studio Smart Loader (if available)
if HAS_SMART_LOADER:
    NODE_CLASS_MAPPINGS.update(SMART_LOADER_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(SMART_LOADER_DISPLAY)
    print("[TA-Nodes] ✓ Smart Loader enabled")

# Add LM Studio Model Selector Nodes
NODE_CLASS_MAPPINGS.update(MODEL_SELECTOR_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(MODEL_SELECTOR_DISPLAY)

# Add TA Filename Generator (if available)
if HAS_FILENAME_GENERATOR:
    NODE_CLASS_MAPPINGS["TAFilenameGenerator"] = TAFilenameGenerator
    NODE_DISPLAY_NAME_MAPPINGS["TAFilenameGenerator"] = "TA Filename Generator"
    print("[TA-Nodes] ✓ TA Filename Generator enabled")

# Add TA Prompt Controller (if available)
if HAS_PROMPT_CONTROLLER:
    NODE_CLASS_MAPPINGS["TAPromptController"] = TAPromptController
    NODE_DISPLAY_NAME_MAPPINGS["TAPromptController"] = "TA Prompt Controller (Switch)"
    print("[TA-Nodes] ✓ TA Prompt Controller enabled")

# Add TA Directory Captioning Node (NEU)
if HAS_CAPTIONING_NODE:
    NODE_CLASS_MAPPINGS["ta_captioning"] = ta_captioning
    NODE_DISPLAY_NAME_MAPPINGS["ta_captioning"] = "TA Directory Captioning (LM Studio)"
    print("[TA-Nodes] ✓ TA Directory Captioning Node enabled")

# Export for ComfyUI
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

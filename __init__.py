"""
TA Nodes Pack - Custom Nodes for ComfyUI
Version: 1.1.2 (Full Workflow Metadata Support)
"""

import os
import sys

# Pfad zum aktuellen Verzeichnis hinzufügen, um lokale Importe zu unterstützen
sys.path.insert(0, os.path.dirname(__file__))

# 1. Base Loader Nodes
try:
    from .ta_load_checkpoint_model_with_name import TALoadCheckpointModelWithName
    from .ta_load_diffusion_model_with_name import TALoadDiffusionModelWithName
    from .ta_load_gguf_model_with_name import TALoadGGUFModelWithName
    HAS_CORE_LOADERS = True
except ImportError:
    HAS_CORE_LOADERS = False

# 2. LM Studio Vision Nodes (Image2Prompt & Tools)
try:
    from .ta_ebu_lmstudio_vision_node import (
        NODE_CLASS_MAPPINGS as LMSTUDIO_VISION_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS as LMSTUDIO_VISION_DISPLAY
    )
    HAS_VISION_NODES = True
except ImportError:
    HAS_VISION_NODES = False

# 3. LM Studio Load On Run Node
try:
    from .ta_lmstudio_load_on_run import (
        NODE_CLASS_MAPPINGS as LOAD_ON_RUN_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS as LOAD_ON_RUN_DISPLAY
    )
    HAS_LOAD_ON_RUN = True
except ImportError:
    HAS_LOAD_ON_RUN = False

# 4. LM Studio Smart Loader
try:
    from .ta_lmstudio_smart_loader import (
        NODE_CLASS_MAPPINGS as SMART_LOADER_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS as SMART_LOADER_DISPLAY
    )
    HAS_SMART_LOADER = True
except ImportError:
    HAS_SMART_LOADER = False

# 5. LM Studio Model Selector Nodes
try:
    from .ta_lmstudio_model_selector import (
        NODE_CLASS_MAPPINGS as MODEL_SELECTOR_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS as MODEL_SELECTOR_DISPLAY
    )
    HAS_MODEL_SELECTOR = True
except ImportError:
    HAS_MODEL_SELECTOR = False

# 6. TA Filename Generator
try:
    from .ta_filename_generator import TAFilenameGenerator
    HAS_FILENAME_GENERATOR = True
except ImportError:
    HAS_FILENAME_GENERATOR = False

# 7. TA Prompt Controller
try:
    from .ta_prompt_controller import TAPromptController
    HAS_PROMPT_CONTROLLER = True
except ImportError:
    HAS_PROMPT_CONTROLLER = False

# 8. TA Directory Captioning Node
try:
    from .ta_directory_captioning_node import ta_captioning
    HAS_CAPTIONING_NODE = True
except ImportError:
    HAS_CAPTIONING_NODE = False

# 9. TA Save Image With Prompt (Mit Workflow-Metadata Fix)
try:
    from .ta_save_image_with_prompt import TASaveImageWithPrompt
    HAS_SAVE_IMAGE_PROMPT = True
except ImportError:
    HAS_SAVE_IMAGE_PROMPT = False


# --------------------------------------------------------------------------------
# NODE REGISTRATION
# --------------------------------------------------------------------------------

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Registrierung der Core-Loader
if HAS_CORE_LOADERS:
    NODE_CLASS_MAPPINGS["TALoadCheckpointModelWithName"] = TALoadCheckpointModelWithName
    NODE_CLASS_MAPPINGS["TALoadDiffusionModelWithName"] = TALoadDiffusionModelWithName
    NODE_CLASS_MAPPINGS["TALoadGGUFModelWithName"] = TALoadGGUFModelWithName
    
    NODE_DISPLAY_NAME_MAPPINGS["TALoadCheckpointModelWithName"] = "TA Load Checkpoint Model (with Name)"
    NODE_DISPLAY_NAME_MAPPINGS["TALoadDiffusionModelWithName"] = "TA Load Diffusion Model (with Name)"
    NODE_DISPLAY_NAME_MAPPINGS["TALoadGGUFModelWithName"] = "TA Load GGUF Model (with Name)"

# Registrierung LM Studio Vision
if HAS_VISION_NODES:
    NODE_CLASS_MAPPINGS.update(LMSTUDIO_VISION_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(LMSTUDIO_VISION_DISPLAY)

# Registrierung Load On Run
if HAS_LOAD_ON_RUN:
    NODE_CLASS_MAPPINGS.update(LOAD_ON_RUN_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(LOAD_ON_RUN_DISPLAY)

# Registrierung Smart Loader
if HAS_SMART_LOADER:
    NODE_CLASS_MAPPINGS.update(SMART_LOADER_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(SMART_LOADER_DISPLAY)

# Registrierung Model Selector
if HAS_MODEL_SELECTOR:
    NODE_CLASS_MAPPINGS.update(MODEL_SELECTOR_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(MODEL_SELECTOR_DISPLAY)

# Registrierung Filename Generator
if HAS_FILENAME_GENERATOR:
    NODE_CLASS_MAPPINGS["TAFilenameGenerator"] = TAFilenameGenerator
    NODE_DISPLAY_NAME_MAPPINGS["TAFilenameGenerator"] = "TA Filename Generator"

# Registrierung Prompt Controller
if HAS_PROMPT_CONTROLLER:
    NODE_CLASS_MAPPINGS["TAPromptController"] = TAPromptController
    NODE_DISPLAY_NAME_MAPPINGS["TAPromptController"] = "TA Prompt Controller (Switch)"

# Registrierung Captioning Node
if HAS_CAPTIONING_NODE:
    NODE_CLASS_MAPPINGS["ta_captioning"] = ta_captioning
    NODE_DISPLAY_NAME_MAPPINGS["ta_captioning"] = "TA Directory Captioning (LM Studio)"

# Registrierung der neuen Save-Node (Die Lösung für dein Workflow-Problem)
if HAS_SAVE_IMAGE_PROMPT:
    NODE_CLASS_MAPPINGS["TASaveImageWithPrompt"] = TASaveImageWithPrompt
    NODE_DISPLAY_NAME_MAPPINGS["TASaveImageWithPrompt"] = "TA Save Image & Prompt TXT"
    print("[TA-Nodes] ✓ TA Save Image & Prompt TXT (Metadata Support) enabled")


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
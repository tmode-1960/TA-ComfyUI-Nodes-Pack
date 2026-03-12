"""
TA Nodes v3.6 🔥
© Thomas Möhring (thomo.ART)
Erstelldatum: 2026-03-02
Änderungsdatum: 2026-03-12
Version: v3.9 - TAHelpLink hinzugefügt
"""
# Bestehende Nodes (bleiben unverändert)
from .ta_smart_llm import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
# Bestehende NEU Nodes
from .ta_llm_prompt_selector import TA_LLM_PromptSelector
from .ta_unified_model_switcher import TAUnifiedModelSwitcher
from .ta_save_image_optional import TASaveImageOptional
from .ta_save_image_with_prompt import TASaveImageWithPrompt
from .ta_sageattention_toggler import TASageAttentionToggler
from .ta_filename_generator import TAFilenameGenerator
from .ta_prompt_controller import TAPromptController
from .ta_prompt_hub import TAPromptHub
from .ta_load_model_with_name import TALoadModelWithName
from .ta_sampler_preset import TASamplerPreset
from .ta_ksampler import TAKSampler
from .ta_latent_preview import TALatentPreview
from .ta_seedvr2_gate import TASeedVR2Gate
from .ta_flux_guidance_gate import TAFluxGuidanceGate
from .ta_model_presets import TAModelPreset
from .ta_directory_captioning import TACaptioning
from .ta_cleanup_switch import TACleanupSwitch
from .ta_help_link import TAHelpLink

# Erweiterte Mappings (alt + neu)
NODE_CLASS_MAPPINGS.update({
    "TA_LLM_PromptSelector":  TA_LLM_PromptSelector,
    "TAUnifiedModelSwitcher": TAUnifiedModelSwitcher,
    "TASaveImageOptional":    TASaveImageOptional,
    "TASaveImageWithPrompt":  TASaveImageWithPrompt,
    "TASageAttentionToggler": TASageAttentionToggler,
    "TAFilenameGenerator":    TAFilenameGenerator,
    "TAPromptController":     TAPromptController,
    "TAPromptHub":            TAPromptHub,
    "TALoadModelWithName":    TALoadModelWithName,
    "ta_sampler_preset":      TASamplerPreset,
    "ta_ksampler":            TAKSampler,
    "ta_latent_preview":      TALatentPreview,
    "TASeedVR2Gate":          TASeedVR2Gate,
    "ta_flux_guidance_gate":  TAFluxGuidanceGate,
    "TAModelPreset":          TAModelPreset,
    "TACaptioning":           TACaptioning,
    "TACleanupSwitch":        TACleanupSwitch,
    "TAHelpLink":             TAHelpLink,
})

NODE_DISPLAY_NAME_MAPPINGS.update({
    "TA_LLM_PromptSelector":  "🎯 TA LLM Prompt Selector",
    "TAUnifiedModelSwitcher": "🧠 TA Unified Model Switcher",
    "TASaveImageOptional":    "💾 TA Save Image Optional",
    "TASaveImageWithPrompt":  "📝 TA Save Image With Prompt",
    "TASageAttentionToggler": "🔧 TA SageAttention Toggler",
    "TAFilenameGenerator":    "📁 TA Filename Generator",
    "TAPromptController":     "🗂️ TA Prompt Controller",
    "TAPromptHub":            "🔀 TA Prompt Hub",
    "TALoadModelWithName":    "📦 TA Load Model (with Name)",
    "ta_sampler_preset":      "🎛️ TA Sampler Preset",
    "ta_ksampler":            "⚡ TA KSampler",
    "ta_latent_preview":      "🖼️ TA Latent Preview",
    "TASeedVR2Gate":          "🚦 TA SeedVR2 Gate",
    "ta_flux_guidance_gate":  "🌊 TA Flux Guidance Gate",
    "TAModelPreset":          "🗂️ TA Model Presets",
    "TACaptioning":           "📷 TA Directory Captioning",
    "TACleanupSwitch":        "🧹 TA Cleanup Switch",
    "TAHelpLink":             "🔗 TA Help Link",
})

WEB_DIRECTORY = "./web/js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

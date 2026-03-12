"""
================================================================================
Node Name   : TACleanupSwitch
Created     : 2026-03-12
Modified    : 2026-03-12
Copyright   : © 2026, Thomas Möhrling (thomo.ART)
Version     : 1.2
--------------------------------------------------------------------------------
Part of ComfyUI-TA-Nodes-Pack
License     : Apache 2.0
Description:
    Combined VRAM/RAM cleanup node with an enable toggle.
    Replaces the three-node chain (Clear Cache All → VRAM-Cleanup → RAM-Cleanup)
    with a single switchable node. When enabled=False, all cleanup operations
    are skipped entirely. Passes through any input signal unchanged.

    VRAM cleanup  : unload_all_models() + soft_empty_cache() +
                    PromptServer free_memory flag + gc.collect()
    RAM cleanup   : SetSystemFileCacheSize + EmptyWorkingSet (all processes) +
                    SetProcessWorkingSetSize + retry loop with sleep
================================================================================
"""

import gc
import time
import platform
import ctypes
from ctypes import wintypes
import psutil
from server import PromptServer
import comfy.model_management


class AnyType(str):
    def __eq__(self, _) -> bool:
        return True
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")


class TACleanupSwitch:
    """
    Switchable combined VRAM/RAM cleanup node.
    When enabled=True, runs full VRAM + RAM cleanup identical to LAOGOU nodes.
    When enabled=False, does nothing at all (no overhead).
    """

    CATEGORY = "TA-Nodes"
    FUNCTION = "execute"
    OUTPUT_NODE = True
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("signal",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "enabled":       ("BOOLEAN", {"default": True, "label_on": "✅ ON", "label_off": "❌ OFF"}),
                "offload_model": ("BOOLEAN", {"default": True}),
                "offload_cache": ("BOOLEAN", {"default": True}),
                "retry_times":   ("INT", {"default": 3, "min": 1, "max": 10, "step": 1}),
            },
            "optional": {
                "signal": (any_type, {}),
            },
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float(time.time())

    def execute(self, enabled, offload_model, offload_cache, retry_times, signal=None):

        if not enabled:
            return (signal,)

        system = platform.system()

        # ── VRAM Cleanup ──────────────────────────────────────────────────────
        try:
            if offload_model:
                comfy.model_management.unload_all_models()

            if offload_cache:
                gc.collect()
                comfy.model_management.soft_empty_cache()
                PromptServer.instance.prompt_queue.set_flag("free_memory", True)

            print(f"🧹 VRAM cleanup done [offload_model: {offload_model}, offload_cache: {offload_cache}]")

        except Exception as e:
            print(f"❌ VRAM cleanup failed: {str(e)}")

        # ── RAM Cleanup ───────────────────────────────────────────────────────
        try:
            mem_before = psutil.virtual_memory()
            before_pct = mem_before.percent
            before_avail_mb = mem_before.available / (1024 * 1024)

            for _ in range(retry_times):

                # 1) File cache
                try:
                    if system == "Windows":
                        ctypes.windll.kernel32.SetSystemFileCacheSize(-1, -1, 0)
                    elif system == "Linux":
                        libc = ctypes.CDLL("libc.so.6")
                        libc.malloc_trim(0)
                except Exception:
                    pass

                # 2) EmptyWorkingSet on all processes
                if system == "Windows":
                    for proc in psutil.process_iter(['pid']):
                        try:
                            handle = ctypes.windll.kernel32.OpenProcess(
                                wintypes.DWORD(0x001F0FFF),
                                wintypes.BOOL(False),
                                wintypes.DWORD(proc.info['pid'])
                            )
                            ctypes.windll.psapi.EmptyWorkingSet(handle)
                            ctypes.windll.kernel32.CloseHandle(handle)
                        except Exception:
                            continue

                # 3) Working set trim
                try:
                    if system == "Windows":
                        ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
                except Exception:
                    pass

                time.sleep(1)

            mem_after = psutil.virtual_memory()
            after_pct = mem_after.percent
            after_avail_mb = mem_after.available / (1024 * 1024)
            freed_mb = after_avail_mb - before_avail_mb
            print(f"🧹 RAM cleanup done [{before_pct:.1f}% → {after_pct:.1f}%, freed: {freed_mb:.0f} MB]")

        except Exception as e:
            print(f"❌ RAM cleanup failed: {str(e)}")

        return (signal,)


# ---------------------------------------------------------------------------
# Node registration
# ---------------------------------------------------------------------------
NODE_CLASS_MAPPINGS = {
    "TACleanupSwitch": TACleanupSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TACleanupSwitch": "🧹 TA Cleanup Switch",
}

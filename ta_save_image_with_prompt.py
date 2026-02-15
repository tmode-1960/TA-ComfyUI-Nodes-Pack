import os
import datetime
import json
from PIL import Image
import numpy as np

# Import der originalen SaveImage Klasse
from nodes import SaveImage
import folder_paths

class TASaveImageWithPrompt(SaveImage):
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(s):
        # Wir holen die originalen Definitionen
        types = SaveImage.INPUT_TYPES()
        # Wir fügen unsere Prompts hinzu
        types["required"].update({
            "positive_prompt": ("STRING", {"forceInput": True}),
            "negative_prompt": ("STRING", {"forceInput": True}),
            "save_txt": (["enabled", "disabled"], {"default": "enabled"}),
        })
        return types

    # --- ÄNDERUNG: Wir definieren den Rückgabetyp ---
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    # -----------------------------------------------
    
    FUNCTION = "ta_save_images"
    OUTPUT_NODE = True
    CATEGORY = "TA Nodes/utils"

    def ta_save_images(self, images, filename_prefix, positive_prompt, negative_prompt, save_txt, **kwargs):
        
        # 1. Aufruf der originalen Methode (speichert das Bild und generiert Metadaten)
        snap_res = self.save_images(images=images, filename_prefix=filename_prefix, **kwargs)
        
        # 2. TXT-Logik
        if save_txt == "enabled":
            full_output_folder, filename, counter, subfolder, filename_prefix = \
                folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
            
            now = datetime.datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

            # Counter zurückrechnen auf den Stand VOR dem Speichern
            current_counter = counter - len(images)

            for i in range(len(images)):
                file_base = f"{filename}_{current_counter:05}_"
                txt_file = f"{file_base}.txt"
                
                output_text = (
                    f"DATE / TIME: {date_time_str}\n"
                    f"FILE: {file_base}.png\n"
                    f"{'='*30}\n"
                    f"POSITIVE PROMPT:\n{positive_prompt}\n\n"
                    f"NEGATIVE PROMPT:\n{negative_prompt}\n"
                    f"{'='*30}\n"
                )
                
                try:
                    file_path = os.path.join(full_output_folder, txt_file)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(output_text)
                except Exception as e:
                    print(f"[TA-Nodes] Fehler beim Schreiben der TXT: {e}")
                
                current_counter += 1

        # --- ÄNDERUNG: Wir geben die Bilder und die ursprünglichen UI-Ergebnisse zurück ---
        # snap_res enthält die UI-Vorschau-Infos, wir hängen die 'images' für den Workflow-Output an.
        return { "ui": snap_res["ui"], "result": (images,) }
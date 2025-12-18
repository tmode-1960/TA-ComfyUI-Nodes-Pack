import os
import datetime
from PIL import Image
import numpy as np
import folder_paths

class TASaveImageWithPrompt:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "positive_prompt": ("STRING", {"forceInput": True}),
                "negative_prompt": ("STRING", {"forceInput": True}),
                "save_txt": (["enabled", "disabled"], {"default": "enabled"}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "TA Nodes/utils"

    def save_images(self, images, filename_prefix, positive_prompt, negative_prompt, save_txt):
        # Ermittelt den Pfad und den Counter (für identische Namen)
        full_output_folder, filename, counter, subfolder, filename_prefix = \
            folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])

        results = list()
        now = datetime.datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        for image in images:
            # Bild-Konvertierung
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            # Basis-Dateiname (identisch für PNG und TXT)
            file_name = f"{filename}_{counter:05}_"
            file = f"{file_name}.png"
            
            # 1. Bild speichern
            img.save(os.path.join(full_output_folder, file), compress_level=4)
            
            # 2. Textdatei speichern (falls aktiviert)
            if save_txt == "enabled":
                txt_file = f"{file_name}.txt"
                
                # Formatierung mit Datum und Prompts
                output_text = (
                    f"DATE / TIME: {date_time_str}\n"
                    f"FILE: {file}\n"
                    f"{'='*30}\n"
                    f"POSITIVE PROMPT:\n{positive_prompt}\n\n"
                    f"NEGATIVE PROMPT:\n{negative_prompt}\n"
                    f"{'='*30}\n"
                )
                
                try:
                    with open(os.path.join(full_output_folder, txt_file), "w", encoding="utf-8") as f:
                        f.write(output_text)
                except Exception as e:
                    print(f"[TA-Nodes] Fehler beim Speichern der TXT: {e}")
            
            # Vorschau-Daten für ComfyUI UI
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            
            counter += 1
            
        return {"ui": {"images": results}}

NODE_CLASS_MAPPINGS = {"TASaveImageWithPrompt": TASaveImageWithPrompt}
NODE_DISPLAY_NAME_MAPPINGS = {"TASaveImageWithPrompt": "TA Save Image & Prompt TXT"}
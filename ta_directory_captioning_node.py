"""
TA Directory Captioning Node for ComfyUI
Part of ComfyUI-TA-Nodes-Pack
Iterates through a directory, sends images to LM Studio Vision Models
and saves the generated captions as .txt files.
"""

import os
import base64
import requests
import time
import sys
from PIL import Image
from io import BytesIO

# Importiere den Smart Loader, um die Liste der verfügbaren Modelle zu erhalten
# Dies setzt voraus, dass ta_lmstudio_smart_loader.py im selben Verzeichnis liegt.
try:
    from .ta_lmstudio_smart_loader import TALMStudioSmartLoader
except ImportError:
    print("[TA-Captioning] WARN: TALMStudioSmartLoader not found. Using default model list.")
    # Fallback-Klasse, falls der Smart Loader nicht gefunden wird
    class TALMStudioSmartLoader:
        @classmethod
        def get_available_models(cls):
            return ["llava-v1.5-7b (V)", "mistral-7b-instruct"]


# --- Hilfsfunktion: Bild in Base64 kodieren (von Dateipfad) ---

def encode_image_from_path(image_path: str) -> str:
    """Konvertiert eine Bilddatei von einem lokalen Pfad in einen Base64-String."""
    try:
        # 1. Bildbytes einlesen
        with open(image_path, "rb") as image_file:
            img_bytes = image_file.read()

        # 2. PIL Image erstellen und in PNG (generisches Format) konvertieren
        pil_image = Image.open(BytesIO(img_bytes))

        buffer = BytesIO()
        pil_image.save(buffer, format="PNG")

        # 3. Base64-Kodierung
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_base64

    except Exception as e:
        # DEUTSCH -> ENGLISCH
        print(f"[TA-Captioning] Error encoding {image_path}: {e}")
        return None


# --- Die Custom Node Klasse ---

class ta_captioning:

    @classmethod
    def INPUT_TYPES(cls):

        models = TALMStudioSmartLoader.get_available_models()

        vision_models = [m for m in models if '(V)' in m]
        default_model = vision_models[0] if vision_models else models[0] if models else "llava-v1.5-7b (V)"

        return {
            "required": {
                "directory_path": ("STRING", {"default": "C:/Bilder/zu_captionen", "multiline": False}),

                "model_selection": (models, {
                    "default": default_model
                }),

                "server_url": ("STRING", {"default": "http://localhost:1234", "multiline": False}),

                # Prompt für englische Ausgabe
                "prompt": ("STRING", {
                    "default": "Describe this image in detail in a single paragraph, ideal for Stable Diffusion. Avoid proper names and create a coherent, short text. Respond in English.",
                    "multiline": True
                }),

                "temperature": ("FLOAT", {
                    "default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1
                }),
                "max_tokens": ("INT", {
                    "default": 500, "min": 1, "max": 131072
                }),
                "overwrite_existing": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Overwrite",
                    "label_off": "Skip existing"
                }),
            },
            "optional": {
                # System Prompt für englische Ausgabe
                "system_prompt": ("STRING", {
                    "default": "You are a helpful AI assistant that describes images accurately and always responds in English.",
                    "multiline": True
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Captioning_Status",)
    FUNCTION = "caption_directory"
    CATEGORY = "TA-Nodes/LMStudio"


    def _send_lmstudio_request(self, server_url, model_name, prompt, system_prompt,
                              image_base64, temperature, max_tokens) -> str:
        """
        Sendet die Anfrage an LM Studio (OpenAI-kompatible API).
        """
        url = f"{server_url}/v1/chat/completions"
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # User message mit Bild und Text
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
                    }
                }
            ]
        })

        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            # Timeout von 1200 Sekunden (20 Minuten) für große Modelle
            response = requests.post(url, json=payload, timeout=1200)
            response.raise_for_status() # Löst Ausnahme für schlechte Statuscodes aus (4xx, 5xx)

            result = response.json()
            return result['choices'][0]['message']['content'].strip()

        except requests.exceptions.ConnectionError:
            raise Exception("Connection Error: LM Studio Server not reachable. Is LM Studio running and the server active?")
        except requests.exceptions.HTTPError as e:
            error_msg = f"LM Studio API HTTP Error {e.response.status_code}: {e.response.text}"
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")


    def caption_directory(self, directory_path, model_selection, server_url, prompt, temperature,
                          max_tokens, overwrite_existing, system_prompt=None):

        # Extrahieren des API-Modellnamens (entfernt die Markierung "(V)")
        api_model_name = model_selection.split(" (")[0]

        # 1. Validierung (DEUTSCH -> ENGLISCH)
        if not os.path.isdir(directory_path):
            return (f"ERROR: Directory not found: {directory_path}",)

        image_files = [f for f in os.listdir(directory_path)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

        # DEUTSCH -> ENGLISCH
        if not image_files:
            return (f"NO IMAGES found in: {directory_path}",)

        print(f"\n{'='*60}")
        # DEUTSCH -> ENGLISCH
        print(f"[TA-Captioning] Starting captioning for {len(image_files)} images...")
        print(f"[TA-Captioning] Model: {api_model_name} | Server: {server_url}")
        print(f"[TA-Captioning] Overwrite: {overwrite_existing}")
        print(f"{'='*60}\n")

        captioned_count = 0
        skipped_count = 0

        # 2. Iteration und Captioning
        for filename in image_files:
            image_path = os.path.join(directory_path, filename)
            base_filename = os.path.splitext(filename)[0]
            caption_path = os.path.join(directory_path, base_filename + ".txt")

            # Überspringen, falls Caption bereits existiert (DEUTSCH -> ENGLISCH)
            if not overwrite_existing and os.path.exists(caption_path):
                print(f"ℹ️ Caption for '{filename}' already exists. Skipping.")
                skipped_count += 1
                continue

            # DEUTSCH -> ENGLISCH
            print(f"⏳ Processing: {filename}...")

            # Kodierung des Bildes
            image_base64 = encode_image_from_path(image_path)
            if not image_base64:
                # DEUTSCH -> ENGLISCH
                print(f"❌ Error encoding '{filename}'. Skipping.")
                continue

            # API-Anfrage
            try:
                caption = self._send_lmstudio_request(
                    server_url, api_model_name, prompt, system_prompt,
                    image_base64, temperature, max_tokens
                )

                # Speichern der Caption
                with open(caption_path, "w", encoding="utf-8") as f:
                    f.write(caption)

                # DEUTSCH -> ENGLISCH
                print(f"✅ Caption for '{filename}' saved.")
                captioned_count += 1

            except Exception as e:
                # DEUTSCH -> ENGLISCH
                print(f"❌ Error processing '{filename}': {e}")

        # 3. Statusmeldung (DEUTSCH -> ENGLISCH)
        status_msg = (f"Captioning finished. {captioned_count} new captions created. "
                      f"{skipped_count} files skipped. (Total images: {len(image_files)})")
        return (status_msg,)

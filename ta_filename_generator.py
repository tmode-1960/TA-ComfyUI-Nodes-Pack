import datetime
import os

# Script-Version 1.3
# - Verarbeitet jetzt Datumsformat-Strings (z.B. %Y-%m-%d) im 'subfolder'-Feld.

# Die Liste der Datumsformate für das 'date_format' Combo-Feld
date_format_options = [
    "%Y%m%d%H%M",
    "%Y%m%d%H%M%S",
    "%Y%m%d",
    "%Y-%m-%d-%H_%M_%S",
    "%Y-%m-%d-%H_%M",
    "%Y-%m-%d",
    "%Y-%m-%d %H_%M_%S",
    "%Y-%m-%d %H_%M",
    "%H%M",
    "%H%M%S",
    "%H_%M",
    "%H_%M_%S"
]


class TAFilenameGenerator:
    """
    Eine Custom Node, die die Logik des Subgraphs zur Dateinamenerstellung
    von thomo.ART nachbildet.
    Sie kombiniert einen optionalen Ordner, einen optionalen Unterordner 
    (der Datums-Codes verarbeiten kann), Präfix, WF-Version, 
    Modellnamen und ein Datum zu einem Dateinamen.
    """

    @classmethod
    def INPUT_TYPES(s):
        """
        Definiert die Eingabe-Widgets für den Node.
        """
        return {
            "required": {
                "model_name": ("STRING", {"default": "Modelname"})
            },
            "optional": {
                "output_folder": ("STRING", {"default": "TA-Outputs"}),
                # Das 'subfolder'-Feld ist ein normaler STRING,
                # wird aber jetzt intern verarbeitet.
                "subfolder": ("STRING", {"default": ""}), 
                "name_prefix": ("STRING", {"default": "TA"}),
                "wf_version": ("STRING", {"default": "v2.50"}),    
                "upscaled_suffix": ("STRING", {"default": "UPSCALED"}),
                "delimiter": ("STRING", {"default": "-"}),
                "date_format": (date_format_options, ),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("filename", "filename_up")

    FUNCTION = "generate_filenames"
    CATEGORY = "TA Nodes/utils"

    def generate_filenames(self, model_name, output_folder, subfolder, name_prefix, wf_version, upscaled_suffix, delimiter, date_format):
        
        # 1. Aktuelle Zeit holen
        now = datetime.datetime.now()

        # 2. Datum-String für den DATEINAMEN holen (aus der Combo-Box)
        try:
            date_string = now.strftime(date_format) 
        except Exception as e:
            print(f"[TA-Nodes] Error formatting filename date: {e}")
            date_string = "DATE_ERROR"

        # --- NEU: Schritt 3 ---
        # 3. Den 'subfolder'-String verarbeiten.
        # strftime wandelt %-Codes um und lässt normale Zeichen unberührt.
        try:
            processed_subfolder = now.strftime(subfolder)
        except ValueError as e:
            # Falls ein ungültiger Code (z.B. %q) eingegeben wird,
            # verwende einfach den String so, wie er eingegeben wurde.
            print(f"[TA-Nodes] Warning: Invalid date format in subfolder '{subfolder}'. Using literal name.")
            processed_subfolder = subfolder
        # ---------------------

        # 4. Basis-Dateinamen OHNE Ordner erstellen
        parts_base = [
            name_prefix,
            wf_version,
            model_name,
            date_string
        ]
        base_filename_only = delimiter.join(filter(None, parts_base))

        # 5. Upscaled-Dateinamen OHNE Ordner erstellen
        parts_upscaled_only = [
            base_filename_only,
            upscaled_suffix
        ]
        upscaled_filename_only = delimiter.join(filter(None, parts_upscaled_only))

        # 6. Ordnerpfad-Komponenten bereinigen
        clean_output_folder = output_folder.strip().strip('/\\')
        # Verwende den verarbeiteten Unterordner-Namen
        clean_subfolder = processed_subfolder.strip().strip('/\\') 

        # 7. Finalen Pfad mit os.path.join erstellen
        # os.path.join fügt die Teile intelligent zusammen.
        # Leere Strings (z.B. wenn subfolder leer ist) werden ignoriert.
        final_filename = os.path.join(clean_output_folder, clean_subfolder, base_filename_only)
        final_upscaled_filename = os.path.join(clean_output_folder, clean_subfolder, upscaled_filename_only)
        
        # 8. Pfad für das Betriebssystem normalisieren
        final_filename = os.path.normpath(final_filename)
        final_upscaled_filename = os.path.normpath(final_upscaled_filename)
            
        # 9. Ergebnisse zurückgeben
        return (final_filename, final_upscaled_filename)

# ---------------------------------------------------------------------------------
#  NODE MAPPINGS
# ---------------------------------------------------------------------------------
NODE_CLASS_MAPPINGS = {
    "TAFilenameGenerator": TAFilenameGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TAFilenameGenerator": "TA Filename Generator"
}
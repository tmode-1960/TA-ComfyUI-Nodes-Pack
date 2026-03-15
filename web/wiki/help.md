# 📖 TA-ComfyUI-Nodes-Pack – Dokumentation

---

## Inhalt / Table of Contents

- **Deutsch**
  - [🧠 TA Unified Model Switcher](#de-ums)
    - [Beschreibung](#de-ums-beschreibung)
    - [Inputs & Outputs](#de-ums-io)
    - [Browser-Editor](#de-ums-editor)
    - [JSON-Datei Aufbau](#de-ums-json)
    - [Tipps & Besonderheiten](#de-ums-tipps)
  - [🗂️ TA Model Preset](#de-mp)
    - [Beschreibung](#de-mp-beschreibung)
    - [Inputs & Outputs](#de-mp-io)
    - [Browser-Editor](#de-mp-editor)
    - [JSON-Datei Aufbau](#de-mp-json)
    - [Tipps & Besonderheiten](#de-mp-tipps)
  - [📦 TA Load Model (with Name)](#de-lmn)
    - [Beschreibung](#de-lmn-beschreibung)
    - [Inputs & Outputs](#de-lmn-io)
    - [Tipps & Besonderheiten](#de-lmn-tipps)
  - [🤖 TA Smart LLM](#de-llm)
    - [Beschreibung](#de-llm-beschreibung)
    - [Inputs & Outputs](#de-llm-io)
    - [Vision-Modell-Erkennung](#de-llm-vision)
    - [Model-Caching](#de-llm-cache)
    - [Tipps & Besonderheiten](#de-llm-tipps)
  - [🔀 TA Prompt Hub](#de-ph)
    - [Beschreibung](#de-ph-beschreibung)
    - [Inputs & Outputs](#de-ph-io)
    - [Tipps & Besonderheiten](#de-ph-tipps)
  - [🗂️ TA Prompt Controller](#de-pc)
    - [Beschreibung](#de-pc-beschreibung)
    - [Inputs & Outputs](#de-pc-io)
    - [Tipps & Besonderheiten](#de-pc-tipps)
  - [🎛️ TA Sampler Preset & ⚡ TA KSampler](#de-sampler)
    - [Beschreibung](#de-sampler-beschreibung)
    - [Inputs & Outputs](#de-sampler-io)
    - [Browser-Editor](#de-sampler-editor)
    - [JSON-Datei Aufbau](#de-sampler-json)
    - [Tipps & Besonderheiten](#de-sampler-tipps)
  - [🧹 TA Cleanup Switch](#de-cs)
    - [Beschreibung](#de-cs-beschreibung)
    - [Inputs & Outputs](#de-cs-io)
    - [Tipps & Besonderheiten](#de-cs-tipps)
  - [🌊 TA Flux Guidance Gate](#de-fgg)
    - [Beschreibung](#de-fgg-beschreibung)
    - [Inputs & Outputs](#de-fgg-io)
    - [Tipps & Besonderheiten](#de-fgg-tipps)
  - [🔧 TA SageAttention Toggler](#de-sat)
    - [Beschreibung](#de-sat-beschreibung)
    - [Inputs & Outputs](#de-sat-io)
    - [SageAttention-Modi](#de-sat-modi)
    - [Tipps & Besonderheiten](#de-sat-tipps)
  - [📁 TA Filename Generator](#de-fg)
    - [Beschreibung](#de-fg-beschreibung)
    - [Inputs & Outputs](#de-fg-io)
    - [Tipps & Besonderheiten](#de-fg-tipps)
  - [💾 TA Save Image Optional & TA Save Image With Prompt](#de-save)
    - [Beschreibung](#de-save-beschreibung)
    - [Inputs & Outputs](#de-save-io)
    - [TXT-Begleitdatei](#de-save-txt)
    - [Tipps & Besonderheiten](#de-save-tipps)
  - [🎬 TA SeedVR2 Gate](#de-svr2)
    - [Beschreibung](#de-svr2-beschreibung)
    - [Inputs & Outputs](#de-svr2-io)
    - [Tipps & Besonderheiten](#de-svr2-tipps)
  - [💬 TA Discord Link](#de-dl)
    - [Beschreibung](#de-dl-beschreibung)
    - [Tipps & Besonderheiten](#de-dl-tipps)
- **English**
  - [🧠 TA Unified Model Switcher](#en-ums)
    - [Description](#en-ums-description)
    - [Inputs & Outputs](#en-ums-io)
    - [Browser Editor](#en-ums-editor)
    - [JSON File Structure](#en-ums-json)
    - [Tips & Notes](#en-ums-tips)
  - [🗂️ TA Model Preset](#en-mp)
    - [Description](#en-mp-description)
    - [Inputs & Outputs](#en-mp-io)
    - [Browser Editor](#en-mp-editor)
    - [JSON File Structure](#en-mp-json)
    - [Tips & Notes](#en-mp-tips)
  - [📦 TA Load Model (with Name)](#en-lmn)
    - [Description](#en-lmn-description)
    - [Inputs & Outputs](#en-lmn-io)
    - [Tips & Notes](#en-lmn-tips)
  - [🤖 TA Smart LLM](#en-llm)
    - [Description](#en-llm-description)
    - [Inputs & Outputs](#en-llm-io)
    - [Vision Model Detection](#en-llm-vision)
    - [Model Caching](#en-llm-cache)
    - [Tips & Notes](#en-llm-tips)
  - [🔀 TA Prompt Hub](#en-ph)
    - [Description](#en-ph-description)
    - [Inputs & Outputs](#en-ph-io)
    - [Tips & Notes](#en-ph-tips)
  - [🗂️ TA Prompt Controller](#en-pc)
    - [Description](#en-pc-description)
    - [Inputs & Outputs](#en-pc-io)
    - [Tips & Notes](#en-pc-tips)
  - [🎛️ TA Sampler Preset & ⚡ TA KSampler](#en-sampler)
    - [Description](#en-sampler-description)
    - [Inputs & Outputs](#en-sampler-io)
    - [Browser Editor](#en-sampler-editor)
    - [JSON File Structure](#en-sampler-json)
    - [Tips & Notes](#en-sampler-tips)
  - [🧹 TA Cleanup Switch](#en-cs)
    - [Description](#en-cs-description)
    - [Inputs & Outputs](#en-cs-io)
    - [Tips & Notes](#en-cs-tips)
  - [🌊 TA Flux Guidance Gate](#en-fgg)
    - [Description](#en-fgg-description)
    - [Inputs & Outputs](#en-fgg-io)
    - [Tips & Notes](#en-fgg-tips)
  - [🔧 TA SageAttention Toggler](#en-sat)
    - [Description](#en-sat-description)
    - [Inputs & Outputs](#en-sat-io)
    - [SageAttention Modes](#en-sat-modes)
    - [Tips & Notes](#en-sat-tips)
  - [📁 TA Filename Generator](#en-fg)
    - [Description](#en-fg-description)
    - [Inputs & Outputs](#en-fg-io)
    - [Tips & Notes](#en-fg-tips)
  - [💾 TA Save Image Optional & TA Save Image With Prompt](#en-save)
    - [Description](#en-save-description)
    - [Inputs & Outputs](#en-save-io)
    - [TXT Companion File](#en-save-txt)
    - [Tips & Notes](#en-save-tips)
  - [🎬 TA SeedVR2 Gate](#en-svr2)
    - [Description](#en-svr2-description)
    - [Inputs & Outputs](#en-svr2-io)
    - [Tips & Notes](#en-svr2-tips)
  - [💬 TA Discord Link](#en-dl)
    - [Description](#en-dl-description)
    - [Tips & Notes](#en-dl-tips)

---
---

# Deutsch

## <a id="de-ums"></a>🧠 TA Unified Model Switcher

### <a id="de-ums-beschreibung"></a>Beschreibung

Der **TA Unified Model Switcher** ermöglicht es, zwischen verschiedenen Modellen umzuschalten, ohne den Workflow zu verändern. Über ein Dropdown wählt man das gewünschte Modell aus – alle anderen Modell-Loader bleiben inaktiv und werden nicht geladen (Lazy Evaluation).

Der Node gibt `MODEL`, `CLIP`, `VAE` und den Modellnamen (`TA_MODEL_NAME`) aus und ist damit direkt mit dem restlichen Workflow verbindbar.

Die verfügbaren Auswahloptionen im Dropdown werden aus der Datei `ta_model_choices.json` gelesen und können über den integrierten Browser-Editor bearbeitet werden.

---

### <a id="de-ums-io"></a>Inputs & Outputs

#### Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `model_choice` | Dropdown | Auswahl des aktiven Modell-Slots. Optionen aus `ta_model_choices.json`. |
| `model_1` | MODEL *(lazy)* | Modell-Eingang für Slot 1 |
| `clip_1` | CLIP *(lazy)* | CLIP-Eingang für Slot 1 |
| `vae_1` | VAE *(lazy)* | VAE-Eingang für Slot 1 |
| `model_name_1` | TA_MODEL_NAME *(lazy)* | Modellname für Slot 1 |
| `model_2` | MODEL *(lazy)* | Modell-Eingang für Slot 2 |
| `clip_2` | CLIP *(lazy)* | CLIP-Eingang für Slot 2 |
| `vae_2` | VAE *(lazy)* | VAE-Eingang für Slot 2 |
| `model_name_2` | TA_MODEL_NAME *(lazy)* | Modellname für Slot 2 |
| `model_3` | MODEL *(lazy)* | Modell-Eingang für Slot 3 |
| `clip_3` | CLIP *(lazy)* | CLIP-Eingang für Slot 3 |
| `vae_3` | VAE *(lazy)* | VAE-Eingang für Slot 3 |
| `model_name_3` | TA_MODEL_NAME *(lazy)* | Modellname für Slot 3 |

> **Lazy:** Nicht ausgewählte Slots werden vom ComfyUI-Executor übersprungen – die zugehörigen Modell-Loader werden nicht ausgeführt und verbrauchen keinen VRAM.

#### Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `model` | MODEL | Das Modell des aktiven Slots |
| `clip` | CLIP | Der CLIP des aktiven Slots |
| `vae` | VAE | Die VAE des aktiven Slots |
| `active_model` | TA_MODEL_NAME | Name des aktiven Modells |

---

### <a id="de-ums-editor"></a>Browser-Editor

Die Auswahloptionen des Dropdowns können bequem über den integrierten Browser-Editor bearbeitet werden – ohne Änderungen an Dateien oder Code.

**Aufruf:**
```
http://localhost:8188/ta_model_choices/ui
```

Im Editor können Einträge hinzugefügt, umbenannt, gelöscht und in der Reihenfolge verschoben werden. Nach dem Speichern wird `ta_model_choices.json` aktualisiert.

> ⚠️ **ComfyUI muss nach Änderungen neu gestartet werden**, damit das Dropdown im Node die neuen Optionen anzeigt.

---

### <a id="de-ums-json"></a>JSON-Datei Aufbau

Die Datei `ta_model_choices.json` liegt im Stammverzeichnis des Node-Packs und hat folgenden Aufbau:

```json
{
    "choices": [
        "Z-Image Diffusion",
        "Z-Image GGUF",
        "Qwen Diffusion",
        "FLUX Diffusion",
        "Checkpoint"
    ]
}
```

- Die **Reihenfolge der Einträge** bestimmt die Slot-Zuordnung: Eintrag 1 → Slot 1, Eintrag 2 → Slot 2 usw.
- Die Datei wird beim ersten Start automatisch mit Standardwerten angelegt, falls sie nicht vorhanden ist.
- Änderungen an der Datei werden erst nach einem Neustart von ComfyUI wirksam.

---

### <a id="de-ums-tipps"></a>Tipps & Besonderheiten

**Slot nicht verbunden**
Wenn der ausgewählte Slot keine verbundenen Inputs (`model`, `clip`, `vae`) hat, bricht die Ausführung mit einer Fehlermeldung ab. Alle drei Eingänge des aktiven Slots müssen verdrahtet sein.

**Modellname-Fallback**
Ist kein `model_name`-Eingang verbunden, wird automatisch der Name der `model_choice`-Auswahl als Modellname weitergegeben.

**Lazy Evaluation**
Nur der aktive Slot wird ausgeführt. Modell-Loader für inaktive Slots werden übersprungen und laden kein Modell in den VRAM.

**Maximale Slot-Anzahl**
Der Node unterstützt aktuell bis zu **3 Slots**.

---
---

## <a id="de-mp"></a>🗂️ TA Model Preset

### <a id="de-mp-beschreibung"></a>Beschreibung

Der **TA Model Preset** lädt `MODEL`, `CLIP` und `VAE` anhand eines benannten Presets aus der Datei `ta_model_presets.json`. Ein Preset enthält alle nötigen Informationen für ein Modell – Dateipfade, CLIP-Typ, VAE und optionale Parameter wie den AuraFlow Shift.

Der Node unterstützt drei Modelltypen:

- **`[D]`** – Diffusion Models (`.safetensors`)
- **`[G]`** – GGUF UNet Models (`.gguf`, erfordert ComfyUI-GGUF)
- **`[C]`** – Checkpoints (CLIP und VAE werden aus dem Checkpoint geladen)

Presets werden über den integrierten Browser-Editor verwaltet und können ohne Änderungen am Workflow gewechselt werden.

---

### <a id="de-mp-io"></a>Inputs & Outputs

#### Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `preset` | Dropdown | Name des zu ladenden Presets. Optionen aus `ta_model_presets.json`. |

#### Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `model` | MODEL | Das geladene Modell |
| `clip` | CLIP | Der geladene CLIP (bei `[C]` aus dem Checkpoint) |
| `vae` | VAE | Die geladene VAE (bei `[C]` aus dem Checkpoint) |
| `model_name` | TA_MODEL_NAME | Dateiname des Modells ohne Pfad und Erweiterung |

---

### <a id="de-mp-editor"></a>Browser-Editor

Presets können bequem über den integrierten Browser-Editor erstellt und bearbeitet werden.

**Aufruf:**
```
http://localhost:8188/ta_model_presets/ui
```

Im Editor werden alle verfügbaren Modell-, CLIP- und VAE-Dateien aus den ComfyUI-Modellverzeichnissen automatisch als Dropdown-Optionen angeboten. Nach dem Speichern wird `ta_model_presets.json` aktualisiert.

> ⚠️ **ComfyUI muss nach Änderungen neu gestartet werden**, damit das Dropdown im Node die neuen Presets anzeigt.

---

### <a id="de-mp-json"></a>JSON-Datei Aufbau

Die Datei `ta_model_presets.json` liegt im Stammverzeichnis des Node-Packs. Jedes Preset ist ein Objekt in der Liste:

```json
[
  {
    "name": "ZImage (BF16)",
    "model_file":   "[D] ZIMAGE/z_image_turbo_bf16.safetensors",
    "clip_name_1":  "ZIMAGE/qwen_3_4b_bf16.safetensors",
    "clip_name_2":  "",
    "clip_type":    "lumina2",
    "clip_device":  "default",
    "vae_name":     "ZIMAGE/zImage_vae.safetensors",
    "shift":        3.0,
    "weight_dtype": "auto"
  }
]
```

| Feld | Beschreibung |
|------|--------------|
| `name` | Anzeigename im Dropdown |
| `model_file` | Pfad zur Modelldatei mit Präfix `[D]`, `[G]` oder `[C]` |
| `clip_name_1` | Primärer CLIP / Text Encoder |
| `clip_name_2` | Zweiter CLIP für Dual-CLIP-Modelle (z.B. FLUX), sonst leer lassen |
| `clip_type` | CLIP-Typ, z.B. `flux`, `lumina2`, `stable_diffusion`, `auto` |
| `clip_device` | Gerät für den CLIP-Loader, normalerweise `default` |
| `vae_name` | Pfad zur VAE-Datei |
| `shift` | AuraFlow Shift-Wert (z.B. `3.0` für Z-Image-Turbo), leer lassen wenn nicht benötigt |
| `weight_dtype` | Gewichts-Datentyp: `auto`, `fp8_e4m3fn` oder `fp8_e5m2` |

Die Datei wird beim ersten Start automatisch mit Beispiel-Presets angelegt, falls sie nicht vorhanden ist.

---

### <a id="de-mp-tipps"></a>Tipps & Besonderheiten

**ComfyUI-Neustart nach Änderungen**
Neue oder umbenannte Presets erscheinen erst nach einem Neustart von ComfyUI im Dropdown des Nodes. Der Browser-Editor speichert die JSON-Datei sofort, aber das Dropdown wird nur beim Start befüllt.

**Falscher oder fehlender Präfix**
Der Wert in `model_file` muss zwingend mit `[D] `, `[G] ` oder `[C] ` beginnen (inklusive Leerzeichen). Fehlt der Präfix oder ist er falsch, bricht die Ausführung mit einer Fehlermeldung ab. Der Browser-Editor setzt den Präfix automatisch korrekt.

**Dual-CLIP (z.B. FLUX)**
Für Modelle mit zwei Text Encodern (FLUX) `clip_name_1` und `clip_name_2` beide befüllen und `clip_type` auf `flux` setzen. Bei Single-CLIP-Modellen `clip_name_2` leer lassen.

**AuraFlow Shift**
Für AuraFlow-basierte Modelle wie Z-Image-Turbo kann ein `shift`-Wert gesetzt werden. Der Node wendet den Patch automatisch an. Für alle anderen Modelle das Feld leer lassen.

**Checkpoint-Modelle**
Bei `[C]`-Presets werden `clip_name_1`, `clip_name_2` und `vae_name` ignoriert – CLIP und VAE werden direkt aus dem Checkpoint geladen.
---
---

## <a id="de-lmn"></a>📦 TA Load Model (with Name)

### <a id="de-lmn-beschreibung"></a>Beschreibung

Der **TA Load Model (with Name)** ist ein kombinierter Modell-Loader für alle drei in TA-Workflows verwendeten Modelltypen: Diffusion Models, GGUF UNet-Modelle und Checkpoints. Er erkennt den Typ automatisch anhand eines Präfixes im Dateinamen und leitet an den passenden ComfyUI-Loader weiter.

Zusätzlich gibt er den bereinigten Modellnamen als `TA_MODEL_NAME`-Output aus – dieser kann direkt vom **TA Filename Generator** verwendet werden.

| Präfix | Typ | Loader |
|--------|-----|--------|
| `[D]` | Diffusion Model | `comfy.sd.load_diffusion_model()` |
| `[G]` | GGUF UNet | ComfyUI-GGUF (`UnetLoaderGGUF`) |
| `[C]` | Checkpoint | `comfy.sd.load_checkpoint_guess_config()` |

---

### <a id="de-lmn-io"></a>Inputs & Outputs

#### Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `model_file` | Dropdown | Modell-Dateiname mit Typ-Präfix, z.B. `[D] flux1-dev.safetensors`. Wird automatisch aus den ComfyUI-Modellverzeichnissen gescannt. |
| `weight_dtype` | auto / fp8_e4m3fn / fp8_e5m2 | Gewichtspräzision – nur relevant für Diffusion Models (`[D]`). Bei `auto` entscheidet ComfyUI. |

#### Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `model` | MODEL | Das geladene Modell – immer vorhanden. |
| `clip` | CLIP | CLIP-Objekt – nur bei Checkpoints (`[C]`), sonst `None`. |
| `vae` | VAE | VAE-Objekt – nur bei Checkpoints (`[C]`), sonst `None`. |
| `model_name` | TA_MODEL_NAME | Bereinigter Dateiname ohne Pfad und Endung, z.B. `flux1-dev`. |

---

### <a id="de-lmn-tipps"></a>Tipps & Besonderheiten

**Automatische Typ-Erkennung**
Das Dropdown zeigt alle gefundenen Modelle mit Präfix – kein separater Typ-Schalter nötig. Der Loader liest das Präfix beim Ausführen aus und wählt automatisch die richtige Ladestrategie.

**GGUF-Fallback**
Für GGUF-Modelle werden drei Ladestrategien nacheinander versucht (direkter Import, NODE_CLASS_MAPPINGS, manueller State-Dict-Load). Ist ComfyUI-GGUF nicht installiert, schlägt das Laden fehl und eine Fehlermeldung erscheint in der Konsole.

**CLIP und VAE nur bei Checkpoints**
Bei `[D]`- und `[G]`-Modellen sind `clip` und `vae` immer `None`. Diese Ausgänge nur bei `[C]`-Modellen verbinden.

**model_name für Dateinamen**
Der `model_name`-Ausgang gibt den bereinigten Dateinamen ohne Pfad und Endung zurück (z.B. `flux1-dev`) und ist direkt mit dem `model_name`-Eingang des **TA Filename Generator** verbindbar.

**weight_dtype**
`fp8_e4m3fn` und `fp8_e5m2` reduzieren den VRAM-Verbrauch bei Diffusion Models auf Kosten minimaler Qualitätsunterschiede. Hat keinen Effekt bei GGUF oder Checkpoint-Modellen.


---
---


---

## <a id="de-llm"></a>🤖 TA Smart LLM

### <a id="de-llm-beschreibung"></a>Beschreibung

Der **TA Smart LLM** verbindet ComfyUI mit lokalen LLM-Backends (**LM Studio** und **Ollama**) zur automatischen Prompt-Generierung. Er unterstützt zwei Anwendungsfälle:

- **Text2Prompt** – Aus einer kurzen Beschreibung oder Anweisung wird ein detaillierter Bildprompt generiert.
- **Image2Prompt** – Ein bestehendes Bild wird zusammen mit einem Text-Prompt an ein Vision-Modell geschickt, das daraus einen neuen oder beschreibenden Prompt erzeugt.

Der Node erkennt automatisch welche Modelle Vision-fähig sind und kennzeichnet sie im Dropdown mit dem Suffix `[Vision]`. Gibt er `MODEL`, `CLIP`, `VAE` zurück? Nein – er gibt den generierten Prompt als `STRING` sowie einen Status-Text zurück, der direkt zur Workflow-Diagnose genutzt werden kann.

---

### <a id="de-llm-io"></a>Inputs & Outputs

#### Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `llm_enable` | BOOLEAN | Master-Schalter. Bei `OFF` wird der Node übersprungen und gibt leeren String zurück. |
| `model` | Dropdown | Auswahl des LLM-Modells. Automatisch befüllt aus LM Studio und Ollama. Vision-Modelle sind mit `[Vision]` gekennzeichnet. |
| `user_prompt` | STRING | Haupteingabe für den LLM (Text2Prompt oder Bildbeschreibungsanweisung). |
| `system_prompt` | STRING | Systemanweisung für das Modell, z.B. Rolle oder Ausgabeformat. |
| `unload_image_models_first` | BOOLEAN | Entlädt ComfyUI-Bildmodelle vor der LLM-Anfrage, um VRAM freizugeben. |
| `unload_llm_after` | BOOLEAN | Entlädt das LLM-Modell nach der Generierung aus dem Backend. |
| `image` | IMAGE *(optional)* | Bild-Input für Vision-Modelle (Image2Prompt). Wird ignoriert wenn kein Vision-Modell ausgewählt ist. |

#### Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `prompt` | STRING | Der generierte Prompt-Text. |
| `status` | STRING | Status der Ausführung, z.B. `LMStudio/model ✅`, `DISABLED`, `SKIPPED - Ollama not reachable`. |

---

### <a id="de-llm-vision"></a>Vision-Modell-Erkennung

Der Node erkennt Vision-Modelle automatisch anhand des Modellnamens. Modelle deren Name Begriffe wie `vision`, `llava`, `vl`, `moondream` oder `qwen-vl` enthält, werden im Dropdown automatisch mit `[Vision]` gekennzeichnet.

Ist ein `[Vision]`-Modell ausgewählt **und** ein Bild am `image`-Eingang verbunden, wird das Bild als Base64 kodiert und zusammen mit dem Text-Prompt an das Modell geschickt (Image2Prompt).

Modelle die nicht automatisch erkannt werden, können manuell in `VISION_MANUAL` in der Datei `ta_smart_llm.py` eingetragen werden.

---

### <a id="de-llm-cache"></a>Model-Caching

Beim Start fragt der Node LM Studio (Port `1234`) und Ollama (Port `11434`) nach verfügbaren Modellen. Die Ergebnisse werden in der Datei `ta_smart_llm_models.json` im Node-Pack-Verzeichnis gespeichert.

Ist ein Backend beim nächsten Start nicht erreichbar, werden die zuletzt bekannten Modelle aus dem Cache geladen und im Dropdown angezeigt – so bleibt das Dropdown auch bei gestopptem Backend befüllt.

> ⚠️ **ComfyUI muss neu gestartet werden**, damit neu installierte Modelle im Dropdown erscheinen.

---

### <a id="de-llm-tipps"></a>Tipps & Besonderheiten

**Kein Backend erreichbar**
Ist weder LM Studio noch Ollama beim Start von ComfyUI erreichbar und kein Cache vorhanden, zeigt das Dropdown `No Backend`. Der Node gibt dann beim Ausführen `SKIPPED` als Status zurück und erzeugt keinen Fehler im Workflow.

**ComfyUI-Neustart nach Modellinstallation**
Neu installierte Modelle in LM Studio oder Ollama erscheinen erst nach einem Neustart von ComfyUI im Dropdown, da die Modellliste nur beim Start befüllt wird.

**VRAM-Management**
`unload_image_models_first` ist nützlich bei knappem VRAM – es entlädt alle ComfyUI-Bildmodelle bevor das LLM lädt. `unload_llm_after` gibt den VRAM nach der Generierung wieder frei, bevor der restliche Workflow die Bildmodelle lädt.

**Image2Prompt**
Für Image2Prompt ein `[Vision]`-Modell auswählen und ein Bild am `image`-Eingang verbinden. Im `user_prompt` die gewünschte Anweisung eingeben, z.B. `Describe this image as a detailed Stable Diffusion prompt.`

---
---

## <a id="de-ph"></a>🔀 TA Prompt Hub

### <a id="de-ph-beschreibung"></a>Beschreibung

Der **TA Prompt Hub** ist ein zentraler Sammelpunkt für alle Prompt-Eingaben in einem Workflow. Er bündelt positiven Prompt, zusätzlichen Prompt, negativen Prompt und optionale LoRA-Trigger-Wörter an einem einzigen Node – ohne eigene Logik, rein als Pass-Through.

Zusätzlich erzeugt er einen `combined_prompt`-Ausgang, der `positive_prompt`, `additional_prompt` und `lora_trigger_words` automatisch mit `, ` zusammenfügt (leere Teile werden dabei übersprungen).

Für Modusumschaltung (z.B. zwischen verschiedenen Prompt-Quellen) ist der **TAPromptController** zuständig – der TA Prompt Hub übernimmt keine Routing-Logik.

---

### <a id="de-ph-io"></a>Inputs & Outputs

#### Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `positive_prompt` | STRING | Haupt-Positivprompt. Unterstützt Dynamic Prompts. |
| `additional_prompt` | STRING | Zusätzlicher Positivprompt, z.B. für Stil oder Szene – ohne LoRA-Trigger-Wörter. |
| `negative_prompt` | STRING | Negativprompt. Unterstützt Dynamic Prompts. |
| `lora_trigger_words` | STRING *(optional)* | LoRA-Trigger-Wörter von einem vorgelagerten LoRA-Node. Leer wenn nicht verbunden. |

#### Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `positive_prompt` | STRING | Pass-through des Haupt-Positivprompts |
| `additional_prompt` | STRING | Pass-through des zusätzlichen Prompts |
| `negative_prompt` | STRING | Pass-through des Negativprompts |
| `lora_trigger_words` | STRING | Pass-through der LoRA-Trigger-Wörter |
| `combined_prompt` | STRING | Automatisch zusammengefügter Prompt aus `positive_prompt`, `additional_prompt` und `lora_trigger_words` (nicht-leere Teile, getrennt durch `, `) |

---

### <a id="de-ph-tipps"></a>Tipps & Besonderheiten

**combined_prompt**
Leere Felder werden beim Zusammenfügen automatisch übersprungen. Ist z.B. `additional_prompt` leer, enthält `combined_prompt` nur `positive_prompt` und `lora_trigger_words`.

**Keine Routing-Logik**
Der TA Prompt Hub schaltet nicht zwischen Prompt-Quellen um. Diese Aufgabe übernimmt der **TAPromptController**.

**LoRA-Trigger-Wörter**
`lora_trigger_words` ist ein optionaler Eingang – er muss nicht verbunden sein. Ist er nicht verbunden, wird er als leerer String behandelt.

---
---

## <a id="de-pc"></a>🗂️ TA Prompt Controller

### <a id="de-pc-beschreibung"></a>Beschreibung

Der **TA Prompt Controller** steuert den Prompt-Fluss zwischen einem manuell eingegebenen Prompt und einem generierten Prompt (z.B. vom TA Smart LLM oder einem VLM-Node). Über einen Modus-Schalter lässt sich auswählen, welche Quelle verwendet wird oder wie beide kombiniert werden.

Er ist als zentraler Routing-Node für Prompts in TA-Workflows gedacht und arbeitet eng mit dem **TA Prompt Hub** zusammen: Der TA Prompt Hub sammelt alle Prompt-Eingaben, der TA Prompt Controller entscheidet welche davon weitergeleitet wird.

**Verfügbare Modi:**

| Modus | Beschreibung |
|-------|--------------|
| `Manual Only` | Gibt `manual_prompt` unverändert weiter |
| `Generated Only` | Gibt `generated_prompt` unverändert weiter |
| `Combine: Manual + Generated` | Verbindet manuellen und generierten Prompt mit dem Trennzeichen |
| `Combine: Generated + Manual` | Verbindet generierten und manuellen Prompt in umgekehrter Reihenfolge |
| `Clear / Empty` | Gibt immer einen leeren String zurück |

---

### <a id="de-pc-io"></a>Inputs & Outputs

#### Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `manual_prompt` | STRING | Manuell eingegebener Prompt. Unterstützt Dynamic Prompts. |
| `mode` | Dropdown | Routing-Modus (siehe oben). |
| `delimiter` | STRING | Trennzeichen zwischen den Prompts in Combine-Modi. Standard: `, ` |
| `generated_prompt` | STRING *(optional)* | Generierter Prompt von einem vorgelagerten LLM/VLM-Node. Leer wenn nicht verbunden. |

#### Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `final_prompt` | STRING | Der resultierende Prompt gemäß gewähltem Modus |

---

### <a id="de-pc-tipps"></a>Tipps & Besonderheiten

**Combine-Modi mit nur einem Input**
Ist in einem Combine-Modus nur einer der beiden Prompts nicht leer, wird dieser direkt ohne Trennzeichen zurückgegeben – kein überflüssiges `, ` am Anfang oder Ende.

**Clear / Empty**
Der Modus `Clear / Empty` gibt unabhängig von den Eingaben immer einen leeren String zurück – nützlich um den Prompt-Fluss im Workflow gezielt zu unterbrechen.

**Zusammenspiel mit TA Prompt Hub**
Der TA Prompt Hub sammelt alle Prompt-Teile, der TA Prompt Controller entscheidet welche Quelle oder Kombination als `final_prompt` weitergegeben wird. Der `final_prompt` wird dann typischerweise an den `positive_prompt`-Eingang des TA Prompt Hub oder direkt ans Conditioning weitergeleitet.

---
---

## <a id="de-sampler"></a>🎛️ TA Sampler Preset & ⚡ TA KSampler

### <a id="de-sampler-beschreibung"></a>Beschreibung

**TA Sampler Preset** und **TA KSampler** sind als Paar konzipiert und ersetzen gemeinsam den eingebauten ComfyUI KSampler.

Der **TA Sampler Preset** lädt Sampler-Konfigurationen (Steps, CFG, Sampler, Scheduler, Start/End-Step) aus der Datei `ta_sampler_presets.json` und gibt alle Parameter als einzelne Ausgänge weiter. Diese sind direkt mit den Eingängen des TA KSampler verbindbar.

Der **TA KSampler** nimmt `sampler_name` und `scheduler` als einfache `STRING`-Eingänge statt als feste Dropdowns – das macht ihn direkt kompatibel mit dem TA Sampler Preset. Zusätzlich bietet er eine Live-Latent-Vorschau nach jedem Sampling-Schritt, identisch zum eingebauten ComfyUI KSampler.

Presets können über den integrierten Browser-Editor verwaltet werden.

---

### <a id="de-sampler-io"></a>Inputs & Outputs

#### TA Sampler Preset – Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `preset` | Dropdown | Name des zu ladenden Presets. Optionen aus `ta_sampler_presets.json`. |

#### TA Sampler Preset – Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `steps` | INT | Anzahl der Sampling-Schritte |
| `cfg` | FLOAT | CFG-Skalierungsfaktor |
| `sampler_name` | STRING | Name des Sampler-Algorithmus, z.B. `euler` |
| `scheduler` | STRING | Name des Noise-Schedulers, z.B. `karras` |
| `start_at_step` | INT | Erster aktiver Sampling-Schritt |
| `end_at_step` | INT | Letzter aktiver Sampling-Schritt |
| `info` | STRING | Formatierte Zusammenfassung aller Preset-Parameter |

#### TA KSampler – Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `model` | MODEL | Das zu verwendende Modell |
| `add_noise` | enable/disable | Rauschen zum Latent hinzufügen |
| `noise_seed` | INT | Seed für die Rauschgenerierung |
| `steps` | INT | Anzahl der Sampling-Schritte |
| `cfg` | FLOAT | CFG-Skalierungsfaktor |
| `sampler_name` | STRING | Sampler-Algorithmus, z.B. `euler`, `dpmpp_2m` |
| `scheduler` | STRING | Noise-Scheduler, z.B. `normal`, `karras`, `beta` |
| `positive` | CONDITIONING | Positives Conditioning |
| `negative` | CONDITIONING | Negatives Conditioning |
| `latent_image` | LATENT | Eingangs-Latent |
| `start_at_step` | INT | Erster aktiver Sampling-Schritt |
| `end_at_step` | INT | Letzter aktiver Sampling-Schritt |
| `return_with_leftover_noise` | enable/disable | Verbleibendes Rauschen im Output behalten |
| `preview` | BOOLEAN | Live-Latent-Vorschau nach jedem Schritt aktivieren |

#### TA KSampler – Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `latent` | LATENT | Das resultierende Latent nach dem Sampling |

---

### <a id="de-sampler-editor"></a>Browser-Editor

Presets können über den integrierten Browser-Editor erstellt, bearbeitet und gelöscht werden. Sampler- und Scheduler-Namen werden automatisch aus ComfyUI's eigenen Listen als Dropdowns angeboten.

**Aufruf:**
```
http://localhost:8188/ta_sampler_presets/ui
```

> ⚠️ **ComfyUI muss nach Änderungen neu gestartet werden**, damit das Dropdown im Node die neuen Presets anzeigt.

---

### <a id="de-sampler-json"></a>JSON-Datei Aufbau

Die Datei `ta_sampler_presets.json` liegt im Stammverzeichnis des Node-Packs:

```json
{
    "Z-Image Turbo": {
        "steps": 9,
        "cfg": 1.0,
        "start_at_step": 0,
        "end_at_step": 9999,
        "sampler_name": "euler",
        "scheduler": "beta"
    }
}
```

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `steps` | INT | Anzahl Sampling-Schritte |
| `cfg` | FLOAT | CFG-Skalierungsfaktor |
| `start_at_step` | INT | Erster aktiver Schritt (0 = Anfang) |
| `end_at_step` | INT | Letzter aktiver Schritt (9999 = bis zum Ende) |
| `sampler_name` | STRING | Sampler-Algorithmus |
| `scheduler` | STRING | Noise-Scheduler |

Die Datei wird beim ersten Start automatisch mit einem Beispiel-Preset angelegt.

---

### <a id="de-sampler-tipps"></a>Tipps & Besonderheiten

**Direkte Verbindung**
Alle Ausgänge des TA Sampler Preset können direkt mit den entsprechenden Eingängen des TA KSampler verbunden werden – kein manuelles Eintragen von Werten nötig.

**Unbekannter Sampler oder Scheduler**
Gibt der TA Sampler Preset einen `sampler_name` oder `scheduler` aus, der in ComfyUI nicht registriert ist, fällt der TA KSampler automatisch auf `euler` bzw. `normal` zurück und gibt eine Warnung in der Konsole aus.

**Live-Vorschau**
Der `preview`-Schalter am TA KSampler aktiviert eine Latent2RGB-Vorschau nach jedem Schritt. Das Verhalten ist identisch zum eingebauten ComfyUI KSampler. Bei Leistungsproblemen kann die Vorschau deaktiviert werden.

**info-Ausgang**
Der `info`-Ausgang des TA Sampler Preset enthält eine formatierte Zusammenfassung aller Parameter und wird auch vom **TAFluxGuidanceGate** verwendet – enthält der Preset-Name `FLUX`, wird die Flux Guidance automatisch aktiviert.

**ComfyUI-Neustart**
Neu angelegte Presets erscheinen erst nach einem Neustart von ComfyUI im Dropdown.

---
---

---
---

## <a id="de-cs"></a>🧹 TA Cleanup Switch

### <a id="de-cs-beschreibung"></a>Beschreibung

Der **TA Cleanup Switch** kombiniert VRAM- und RAM-Bereinigung in einem einzigen schaltbaren Node. Er ersetzt die bisherige Drei-Node-Kette (Clear Cache All → VRAM-Cleanup → RAM-Cleanup) und kann über einen Enable-Schalter vollständig deaktiviert werden – dann entstehen keinerlei Overhead.

Der Node leitet ein optionales Signal-Input unverändert durch, sodass er nahtlos in eine bestehende Node-Kette eingebaut werden kann.

---

### <a id="de-cs-io"></a>Inputs & Outputs

#### Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `enabled` | BOOLEAN | Master-Schalter. Bei `OFF` werden alle Cleanup-Operationen übersprungen. |
| `offload_model` | BOOLEAN | Entlädt alle ComfyUI-Bildmodelle aus dem VRAM (`unload_all_models()`). |
| `offload_cache` | BOOLEAN | Leert den GPU-Cache (`soft_empty_cache()`) und führt Python Garbage Collection durch. |
| `retry_times` | INT | Anzahl der Wiederholungen der RAM-Bereinigung (Standard: 3). |
| `signal` | * *(optional)* | Beliebiges Signal zum Durchleiten – z.B. ein Latent oder Image zur Steuerung der Ausführungsreihenfolge. |

#### Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `signal` | * | Das eingehende Signal unverändert weitergeleitet. |

---

### <a id="de-cs-tipps"></a>Tipps & Besonderheiten

**VRAM-Cleanup**
`offload_model` ruft `unload_all_models()` auf, `offload_cache` ruft zusätzlich `soft_empty_cache()` und `gc.collect()` auf. Beide können unabhängig voneinander aktiviert werden.

**RAM-Cleanup (Windows)**
Auf Windows wird `SetSystemFileCacheSize`, `EmptyWorkingSet` (auf allen laufenden Prozessen) und `SetProcessWorkingSetSize` aufgerufen. Auf Linux wird `malloc_trim()` verwendet. Die Anzahl der Durchläufe ist über `retry_times` konfigurierbar.

**Signal-Passthrough**
Der `signal`-Eingang akzeptiert jeden Typ (`*`). Damit lässt sich der Cleanup-Node an beliebiger Stelle in einen Workflow einbauen, ohne die Datenverbindungen zu unterbrechen.

**Deaktiviert = kein Overhead**
Bei `enabled=False` wird der gesamte Node übersprungen – es findet keinerlei Cleanup statt und das Signal wird sofort weitergeleitet.

---
---

## <a id="de-fgg"></a>🌊 TA Flux Guidance Gate

### <a id="de-fgg-beschreibung"></a>Beschreibung

Der **TA Flux Guidance Gate** wendet Flux Guidance auf ein Conditioning-Tensor an – aber nur dann, wenn das aktive Sampler-Preset ein FLUX-Preset ist. Für alle anderen Presets wird das Conditioning unverändert durchgeleitet.

Die Erkennung erfolgt automatisch anhand des `info`-Ausgangs des **TA Sampler Preset**: Enthält der Preset-Name `FLUX` (Groß-/Kleinschreibung egal), wird die Guidance injiziert. So ist keine manuelle Umschaltung nötig beim Wechsel zwischen FLUX- und Nicht-FLUX-Modellen.

---

### <a id="de-fgg-io"></a>Inputs & Outputs

#### Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `conditioning` | CONDITIONING | Das Conditioning das modifiziert oder durchgeleitet wird. |
| `guidance` | FLOAT | Flux Guidance Scale (Standard: 3.5). Wird nur bei FLUX-Presets angewendet. |
| `preset_info` | STRING | Der `info`-Ausgang des TA Sampler Preset Nodes. Wird zur FLUX-Erkennung verwendet. |

#### Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `conditioning` | CONDITIONING | Das modifizierte Conditioning (bei FLUX) oder unverändert (bei anderen Presets). |

---

### <a id="de-fgg-tipps"></a>Tipps & Besonderheiten

**Automatische FLUX-Erkennung**
Der Node prüft ob der Preset-Name im `info`-String das Wort `FLUX` enthält. Es reicht also, das Preset im TA Sampler Preset entsprechend zu benennen (z.B. `FLUX Dev` oder `My FLUX Preset`).

**Kein manuelles Umschalten**
Beim Wechsel von einem FLUX- zu einem Nicht-FLUX-Preset im TA Sampler Preset wird die Guidance automatisch deaktiviert – ohne den Workflow manuell anzupassen.

**preset_info verbinden**
Der `preset_info`-Eingang muss mit dem `info`-Ausgang eines TA Sampler Preset Nodes verbunden sein. Ist er nicht verbunden oder leer, wird das Conditioning immer unverändert durchgeleitet.

---
---

## <a id="de-sat"></a>🔧 TA SageAttention Toggler

### <a id="de-sat-beschreibung"></a>Beschreibung

Der **TA SageAttention Toggler** patcht ein ComfyUI MODEL mit SageAttention und/oder PyTorch FP16 Matmul-Beschleunigung. Beide Patches sind unabhängig voneinander aktivierbar.

**SageAttention** ersetzt die Standard-Attention-Funktion durch einen quantisierten CUDA/Triton-Kernel für schnellere Inferenz. Es stehen fünf Kernel-Varianten zur Auswahl.

**FP16 Matmul** aktiviert `torch.backends.cuda.matmul.allow_fp16_accumulation` für zusätzlichen Durchsatz auf unterstützter Hardware. Erfordert PyTorch Nightly 2.7+.

---

### <a id="de-sat-io"></a>Inputs & Outputs

#### Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `model` | MODEL | Das zu patchende ComfyUI-Modell. |
| `sage_enable` | BOOLEAN | SageAttention-Patch aktivieren/deaktivieren. |
| `torch_enable` | BOOLEAN | PyTorch FP16 Matmul-Patch aktivieren/deaktivieren. |
| `sage_mode` | Dropdown | SageAttention Kernel-Variante (siehe unten). |

#### Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `model` | MODEL | Das gepatchte Modell. |

---

### <a id="de-sat-modi"></a>SageAttention-Modi

| Modus | Beschreibung |
|-------|--------------|
| `auto` | Standard `sageattn()`-Einstiegspunkt, automatische Auswahl. |
| `sageattn_qk_int8_pv_fp16_cuda` | QK INT8 + PV FP16, CUDA-Kernel. Empfohlen für Ampere-GPUs (RTX 30xx). |
| `sageattn_qk_int8_pv_fp16_triton` | QK INT8 + PV FP16, Triton-Kernel. |
| `sageattn_qk_int8_pv_fp8_cuda` | QK INT8 + PV FP8, CUDA-Kernel. |
| `sageattn_qk_fp8_pv_fp8_cuda` | QK FP8 + PV FP8, CUDA-Kernel. Maximale Komprimierung. |

---

### <a id="de-sat-tipps"></a>Tipps & Besonderheiten

**Empfehlung für RTX 3090 (Ampere)**
Der Modus `sageattn_qk_int8_pv_fp16_cuda` ist auf Ampere-GPUs optimal und bietet das beste Verhältnis aus Geschwindigkeit und Qualität.

**SageAttention nicht installiert**
Ist das Paket `sageattention` nicht installiert, wird `sage_active = False` gesetzt und der Patch übersprungen. Installation: `pip install sageattention-nightly`

**FP16 Matmul**
Der Torch-Patch setzt `allow_fp16_accumulation = True` global für die CUDA-Backend-Session. Nach dem Sampling wird der Wert automatisch zurückgesetzt, sofern das Modell `_torch_callbacks` unterstützt. Erfordert PyTorch Nightly 2.7+.

**Beide Patches unabhängig**
`sage_enable` und `torch_enable` können beliebig kombiniert werden – auch einzeln oder beide deaktiviert.

---
---

## <a id="de-fg"></a>📁 TA Filename Generator

### <a id="de-fg-beschreibung"></a>Beschreibung

Der **TA Filename Generator** erstellt strukturierte Ausgabepfade für gespeicherte Bilder. Er kombiniert einen optionalen Ausgabeordner, einen optionalen Unterordner (der strftime-Datumscodes unterstützt), einen Namenspräfix, eine Workflow-Version, den Modellnamen und einen formatierten Zeitstempel.

Gibt zwei Pfade zurück: einen Basis-Pfad und einen Upscale-Pfad – beide direkt kompatibel mit den TA Save Image Nodes.

---

### <a id="de-fg-io"></a>Inputs & Outputs

#### Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `model_name` | TA_MODEL_NAME *(optional)* | Modellname-String vom TALoadModelWithName-Node. Fallback: `model`. |
| `output_folder` | STRING | Wurzelordner für die Ausgabe. Standard: `TA-Outputs`. |
| `subfolder` | STRING | Optionaler Unterordner. Unterstützt strftime-Codes wie `%Y-%m-%d`. |
| `name_prefix` | STRING | Kurzes Präfix am Anfang des Dateinamens. Standard: `TA`. |
| `wf_version` | STRING | Workflow-Versionstag, z.B. `v2.60`. |
| `upscaled_suffix` | STRING | Suffix für den Upscale-Pfad. Standard: `UPSCALED`. |
| `delimiter` | STRING | Trennzeichen zwischen den Dateinamen-Teilen. Standard: `-`. |
| `date_format` | Dropdown | strftime-Format für den Zeitstempel im Dateinamen. |

#### Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `filename` | STRING | Vollständiger Basis-Dateipfad, OS-normalisiert. |
| `filename_up` | STRING | Vollständiger Upscale-Dateipfad mit angehängtem Suffix. |

---

### <a id="de-fg-tipps"></a>Tipps & Besonderheiten

**Subfolder mit Datumscodes**
Der `subfolder`-Input verarbeitet strftime-Codes zum Ausführungszeitpunkt. `%Y-%m-%d` wird z.B. zu `2026-03-12`. Ungültige Codes werden als Literal-String verwendet.

**Dateinamenschema**
Der generierte Dateiname folgt dem Schema: `{prefix}{delim}{wf_version}{delim}{model_name}{delim}{date}`. Beispiel: `TA-v2.60-flux-dev-202603121430`

**Upscale-Pfad**
`filename_up` ist identisch mit `filename`, hat aber zusätzlich das `upscaled_suffix` angehängt – direkt verwendbar für den Upscale-Zweig im Workflow.

**Keine leeren Segmente**
Leere Teile (z.B. kein Subfolder) werden automatisch aus dem Pfad herausgefiltert – kein doppelter Separator.

---
---

## <a id="de-save"></a>💾 TA Save Image Optional & TA Save Image With Prompt

### <a id="de-save-beschreibung"></a>Beschreibung

Beide Nodes erweitern ComfyUI's eingebauten `SaveImage`-Node. Sie unterscheiden sich hauptsächlich im Ausgabeformat und im Enable-Schalter:

| Node | Format | Enable-Toggle |
|------|--------|---------------|
| **TA Save Image Optional** | JPEG oder WebP (konfigurierbare Qualität) | ✅ Ja – kann deaktiviert werden |
| **TA Save Image With Prompt** | PNG (Standard ComfyUI-Logik) | ❌ Nein – speichert immer |

Beide Nodes schreiben optional eine Begleit-`.txt`-Datei pro Bild mit positivem/negativem Prompt, Zeitstempel und Dateinamensreferenz.

---

### <a id="de-save-io"></a>Inputs & Outputs

#### TA Save Image Optional – Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `images` | IMAGE | Zu speichernder Bild-Tensor. |
| `filename_prefix` | STRING | Basis-Dateiname. Vorhandene Bild-Suffixe (`.jpg`, `.png` etc.) werden automatisch entfernt. |
| `enabled` | BOOLEAN | Master-Schalter. Bei `OFF` wird der Node übersprungen, das Bild weitergeleitet. |
| `save_txt` | enabled/disabled | Begleit-`.txt`-Datei pro Bild schreiben. |
| `positive_prompt` | STRING | Positiver Prompt für die `.txt`-Datei. |
| `negative_prompt` | STRING | Negativer Prompt für die `.txt`-Datei. |
| `save_format` | jpg / webp *(optional)* | Ausgabeformat. Standard: `jpg`. |
| `jpeg_quality` | 70–100 *(optional)* | Komprimierungsqualität für JPEG und WebP. Standard: `95`. |

#### TA Save Image With Prompt – Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `images` | IMAGE | Zu speichernder Bild-Tensor. |
| `filename_prefix` | STRING | Basis-Dateiname (Standard ComfyUI-Konvention). |
| `positive_prompt` | STRING | Positiver Prompt für die `.txt`-Datei. |
| `negative_prompt` | STRING | Negativer Prompt für die `.txt`-Datei. |
| `save_txt` | enabled/disabled | Begleit-`.txt`-Datei pro Bild schreiben. |

#### Outputs (beide Nodes)

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `IMAGE` | IMAGE | Das Eingangsbild unverändert weitergeleitet. |

---

### <a id="de-save-txt"></a>TXT-Begleitdatei

Wenn `save_txt` aktiviert ist, wird pro Bild eine `.txt`-Datei mit folgendem Inhalt erstellt:

```
DATE / TIME: 2026-03-12 14:30:00
FILE: TA-v2.60-flux-dev-202603121430_00001_.jpg
==============================
POSITIVE PROMPT:
<positiver Prompt>

NEGATIVE PROMPT:
<negativer Prompt>
==============================
```

---

### <a id="de-save-tipps"></a>Tipps & Besonderheiten

**Welchen Node verwenden?**
`TA Save Image Optional` bietet mehr Kontrolle (Format, Qualität, deaktivierbar) und eignet sich für den Hauptspeicher-Zweig. `TA Save Image With Prompt` ist einfacher und nutzt die volle ComfyUI PNG-Speicherlogik inklusive UI-Vorschau-Metadaten.

**Enable-Toggle (Optional)**
Bei `enabled=False` wird das Bild einfach weitergeleitet ohne dass etwas gespeichert wird – nützlich zum schnellen Deaktivieren ohne den Workflow umzubauen.

**Filename-Kompatibilität**
Der `filename`-Ausgang des **TA Filename Generator** kann direkt als `filename_prefix` für beide Save-Nodes verwendet werden. Vorhandene Bildendungen im Präfix werden automatisch entfernt.

---
---

## <a id="de-svr2"></a>🎬 TA SeedVR2 Gate

### <a id="de-svr2-beschreibung"></a>Beschreibung

Der **TA SeedVR2 Gate** steuert die Ausführung der SeedVR2-Upscaler-Pipeline über ComfyUI Lazy Evaluation. Ist der Gate deaktiviert, werden alle vorgelagerten Nodes (SeedVR2-Modell-Loader, Bildquelle) vollständig übersprungen – sie werden nicht einmal angefragt. Das verhindert das unnötige Laden der ca. 14 GB großen SeedVR2-Modelle wenn der Upscaler nicht benötigt wird.

---

### <a id="de-svr2-io"></a>Inputs & Outputs

#### Inputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `enabled` | BOOLEAN | Master-Schalter. `False` = alle vorgelagerten Nodes werden übersprungen. Standard: `False`. |
| `image` | IMAGE *(lazy, optional)* | Eingangs-Bild für den Upscaler. Wird nur angefragt wenn `enabled=True`. |
| `dit` | SEEDVR2_DIT *(lazy, optional)* | Geladenes SeedVR2 DiT-Modell. Wird nur angefragt wenn `enabled=True`. |
| `vae` | SEEDVR2_VAE *(lazy, optional)* | Geladenes SeedVR2 VAE-Modell. Wird nur angefragt wenn `enabled=True`. |

#### Outputs

| Name | Typ | Beschreibung |
|------|-----|--------------|
| `image` | IMAGE | Bild weitergeleitet (bei `enabled=True`) oder blockiert. |
| `dit` | SEEDVR2_DIT | DiT-Modell weitergeleitet oder blockiert. |
| `vae` | SEEDVR2_VAE | VAE-Modell weitergeleitet oder blockiert. |

---

### <a id="de-svr2-tipps"></a>Tipps & Besonderheiten

**Lazy Evaluation**
Der Node nutzt `check_lazy_status()` – ComfyUI fragt die optionalen Inputs (`image`, `dit`, `vae`) nur dann an, wenn `enabled=True`. Bei `enabled=False` laufen die SeedVR2-Loader-Nodes gar nicht erst, was VRAM und Ladezeit spart.

**Standard: deaktiviert**
Der Standard-Wert ist `False` – der Upscaler ist standardmäßig aus. Das ist bewusst so gewählt, um versehentliches Laden der großen Modelle zu vermeiden.

**ExecutionBlocker**
Bei `enabled=False` gibt der Node `ExecutionBlocker(None)`-Platzhalter zurück, die alle nachgelagerten Nodes in diesem Zweig blockieren.

---
---

## <a id="de-dl"></a>💬 TA Discord Link

### <a id="de-dl-beschreibung"></a>Beschreibung

Der **TA Discord Link** ist ein rein informativer Node, der einen klickbaren Discord-Einladungslink direkt im ComfyUI-Graph anzeigt. Er hat keine Inputs und keine Outputs.

Die Einladungs-URL und der Button-Text werden in `ta_discord_link.json` gespeichert und können über den integrierten Browser-Editor geändert werden.

**Browser-Editor:**
```
http://localhost:8188/ta_discord_link/ui
```

---

### <a id="de-dl-tipps"></a>Tipps & Besonderheiten

**URL ändern**
Die Standard-URL `https://discord.gg/YOUR_INVITE_CODE` muss nach der Installation einmalig über den Browser-Editor auf die eigene Discord-Einladung gesetzt werden.

**Kein Neustart nötig**
Änderungen über den Browser-Editor werden sofort in `ta_discord_link.json` gespeichert. Der Button im Graph zeigt die neue URL beim nächsten Laden des Workflows.


---
---

# English

## <a id="en-ums"></a>🧠 TA Unified Model Switcher

### <a id="en-ums-description"></a>Description

The **TA Unified Model Switcher** allows switching between different models without modifying the workflow. The desired model is selected via a dropdown – all other model loaders remain inactive and are not executed (lazy evaluation).

The node outputs `MODEL`, `CLIP`, `VAE`, and the model name (`TA_MODEL_NAME`), making it directly connectable to the rest of the workflow.

The available dropdown options are read from `ta_model_choices.json` and can be edited using the built-in browser editor.

---

### <a id="en-ums-io"></a>Inputs & Outputs

#### Inputs

| Name | Type | Description |
|------|------|-------------|
| `model_choice` | Dropdown | Selects the active model slot. Options from `ta_model_choices.json`. |
| `model_1` | MODEL *(lazy)* | Model input for slot 1 |
| `clip_1` | CLIP *(lazy)* | CLIP input for slot 1 |
| `vae_1` | VAE *(lazy)* | VAE input for slot 1 |
| `model_name_1` | TA_MODEL_NAME *(lazy)* | Model name for slot 1 |
| `model_2` | MODEL *(lazy)* | Model input for slot 2 |
| `clip_2` | CLIP *(lazy)* | CLIP input for slot 2 |
| `vae_2` | VAE *(lazy)* | VAE input for slot 2 |
| `model_name_2` | TA_MODEL_NAME *(lazy)* | Model name for slot 2 |
| `model_3` | MODEL *(lazy)* | Model input for slot 3 |
| `clip_3` | CLIP *(lazy)* | CLIP input for slot 3 |
| `vae_3` | VAE *(lazy)* | VAE input for slot 3 |
| `model_name_3` | TA_MODEL_NAME *(lazy)* | Model name for slot 3 |

> **Lazy:** Inactive slots are skipped by the ComfyUI executor – their model loaders are not executed and consume no VRAM.

#### Outputs

| Name | Type | Description |
|------|------|-------------|
| `model` | MODEL | The model from the active slot |
| `clip` | CLIP | The CLIP from the active slot |
| `vae` | VAE | The VAE from the active slot |
| `active_model` | TA_MODEL_NAME | Name of the active model |

---

### <a id="en-ums-editor"></a>Browser Editor

The dropdown options can be edited conveniently through the built-in browser editor – no file or code changes required.

**Open at:**
```
http://localhost:8188/ta_model_choices/ui
```

The editor allows adding, renaming, deleting, and reordering entries. After saving, `ta_model_choices.json` is updated.

> ⚠️ **ComfyUI must be restarted after changes** for the dropdown in the node to reflect the new options.

---

### <a id="en-ums-json"></a>JSON File Structure

The file `ta_model_choices.json` is located in the root directory of the node pack and has the following structure:

```json
{
    "choices": [
        "Z-Image Diffusion",
        "Z-Image GGUF",
        "Qwen Diffusion",
        "FLUX Diffusion",
        "Checkpoint"
    ]
}
```

- The **order of entries** determines the slot assignment: entry 1 → slot 1, entry 2 → slot 2, etc.
- The file is created automatically with default values on first launch if it does not exist.
- Changes to the file take effect only after restarting ComfyUI.

---

### <a id="en-ums-tips"></a>Tips & Notes

**Slot not connected**
If the selected slot has no connected inputs (`model`, `clip`, `vae`), execution will abort with an error message. All three inputs of the active slot must be wired.

**Model name fallback**
If no `model_name` input is connected, the name of the `model_choice` selection is automatically used as the model name.

**Lazy Evaluation**
Only the active slot is executed. Model loaders for inactive slots are skipped and do not load any model into VRAM.

**Maximum number of slots**
The node currently supports up to **3 slots**.

---
---

## <a id="en-mp"></a>🗂️ TA Model Preset

### <a id="en-mp-description"></a>Description

The **TA Model Preset** node loads `MODEL`, `CLIP`, and `VAE` based on a named preset from the file `ta_model_presets.json`. A preset contains all the information needed for a model – file paths, CLIP type, VAE, and optional parameters such as the AuraFlow shift.

The node supports three model types:

- **`[D]`** – Diffusion Models (`.safetensors`)
- **`[G]`** – GGUF UNet Models (`.gguf`, requires ComfyUI-GGUF)
- **`[C]`** – Checkpoints (CLIP and VAE are loaded from the checkpoint)

Presets are managed via the built-in browser editor and can be switched without any changes to the workflow.

---

### <a id="en-mp-io"></a>Inputs & Outputs

#### Inputs

| Name | Type | Description |
|------|------|-------------|
| `preset` | Dropdown | Name of the preset to load. Options from `ta_model_presets.json`. |

#### Outputs

| Name | Type | Description |
|------|------|-------------|
| `model` | MODEL | The loaded model |
| `clip` | CLIP | The loaded CLIP (from checkpoint for `[C]` presets) |
| `vae` | VAE | The loaded VAE (from checkpoint for `[C]` presets) |
| `model_name` | TA_MODEL_NAME | Model filename without path or extension |

---

### <a id="en-mp-editor"></a>Browser Editor

Presets can be created and edited conveniently through the built-in browser editor.

**Open at:**
```
http://localhost:8188/ta_model_presets/ui
```

The editor automatically lists all available model, CLIP, and VAE files from the ComfyUI model directories as dropdown options. After saving, `ta_model_presets.json` is updated immediately.

> ⚠️ **ComfyUI must be restarted after changes** for the dropdown in the node to reflect the new presets.

---

### <a id="en-mp-json"></a>JSON File Structure

The file `ta_model_presets.json` is located in the root directory of the node pack. Each preset is an object in the list:

```json
[
  {
    "name": "ZImage (BF16)",
    "model_file":   "[D] ZIMAGE/z_image_turbo_bf16.safetensors",
    "clip_name_1":  "ZIMAGE/qwen_3_4b_bf16.safetensors",
    "clip_name_2":  "",
    "clip_type":    "lumina2",
    "clip_device":  "default",
    "vae_name":     "ZIMAGE/zImage_vae.safetensors",
    "shift":        3.0,
    "weight_dtype": "auto"
  }
]
```

| Field | Description |
|-------|-------------|
| `name` | Display name in the dropdown |
| `model_file` | Path to the model file with prefix `[D]`, `[G]`, or `[C]` |
| `clip_name_1` | Primary CLIP / text encoder |
| `clip_name_2` | Second CLIP for dual-CLIP models (e.g. FLUX), leave empty otherwise |
| `clip_type` | CLIP type, e.g. `flux`, `lumina2`, `stable_diffusion`, `auto` |
| `clip_device` | Device for the CLIP loader, usually `default` |
| `vae_name` | Path to the VAE file |
| `shift` | AuraFlow shift value (e.g. `3.0` for Z-Image-Turbo), leave empty if not needed |
| `weight_dtype` | Weight data type: `auto`, `fp8_e4m3fn`, or `fp8_e5m2` |

The file is created automatically with example presets on first launch if it does not exist.

---

### <a id="en-mp-tips"></a>Tips & Notes

**ComfyUI restart after changes**
New or renamed presets will only appear in the node dropdown after restarting ComfyUI. The browser editor saves the JSON file immediately, but the dropdown is only populated at startup.

**Missing or incorrect prefix**
The value in `model_file` must start with `[D] `, `[G] `, or `[C] ` (including the space). If the prefix is missing or incorrect, execution will abort with an error message. The browser editor sets the correct prefix automatically.

**Dual-CLIP (e.g. FLUX)**
For models with two text encoders (FLUX), fill in both `clip_name_1` and `clip_name_2` and set `clip_type` to `flux`. For single-CLIP models, leave `clip_name_2` empty.

**AuraFlow Shift**
For AuraFlow-based models such as Z-Image-Turbo, a `shift` value can be set. The node applies the patch automatically. Leave the field empty for all other models.

**Checkpoint models**
For `[C]` presets, `clip_name_1`, `clip_name_2`, and `vae_name` are ignored – CLIP and VAE are loaded directly from the checkpoint.
---
---

## <a id="en-lmn"></a>📦 TA Load Model (with Name)

### <a id="en-lmn-description"></a>Description

The **TA Load Model (with Name)** is a combined model loader for all three model types used in TA workflows: Diffusion Models, GGUF UNet models, and Checkpoints. It automatically detects the type from a prefix in the filename and routes to the appropriate ComfyUI loader.

It also outputs the cleaned model name as a `TA_MODEL_NAME` output – directly usable by the **TA Filename Generator**.

| Prefix | Type | Loader |
|--------|------|--------|
| `[D]` | Diffusion Model | `comfy.sd.load_diffusion_model()` |
| `[G]` | GGUF UNet | ComfyUI-GGUF (`UnetLoaderGGUF`) |
| `[C]` | Checkpoint | `comfy.sd.load_checkpoint_guess_config()` |

---

### <a id="en-lmn-io"></a>Inputs & Outputs

#### Inputs

| Name | Type | Description |
|------|------|-------------|
| `model_file` | Dropdown | Model filename with type prefix, e.g. `[D] flux1-dev.safetensors`. Automatically scanned from ComfyUI model directories. |
| `weight_dtype` | auto / fp8_e4m3fn / fp8_e5m2 | Weight precision – only relevant for Diffusion Models (`[D]`). With `auto`, ComfyUI decides. |

#### Outputs

| Name | Type | Description |
|------|------|-------------|
| `model` | MODEL | The loaded model – always present. |
| `clip` | CLIP | CLIP object – only for Checkpoints (`[C]`), otherwise `None`. |
| `vae` | VAE | VAE object – only for Checkpoints (`[C]`), otherwise `None`. |
| `model_name` | TA_MODEL_NAME | Cleaned filename without path or extension, e.g. `flux1-dev`. |

---

### <a id="en-lmn-tips"></a>Tips & Notes

**Automatic type detection**
The dropdown shows all found models with their prefix – no separate type selector needed. The loader reads the prefix at execution time and automatically picks the right loading strategy.

**GGUF fallback**
For GGUF models, three loading strategies are attempted in order (direct import, NODE_CLASS_MAPPINGS lookup, manual state-dict load). If ComfyUI-GGUF is not installed, loading will fail and an error message will appear in the console.

**CLIP and VAE only for checkpoints**
For `[D]` and `[G]` models, `clip` and `vae` are always `None`. Only connect these outputs for `[C]` models.

**model_name for filenames**
The `model_name` output returns the cleaned filename without path or extension (e.g. `flux1-dev`) and is directly connectable to the `model_name` input of the **TA Filename Generator**.

**weight_dtype**
`fp8_e4m3fn` and `fp8_e5m2` reduce VRAM usage for Diffusion Models at the cost of minimal quality differences. Has no effect on GGUF or Checkpoint models.


---
---

## <a id="en-llm"></a>🤖 TA Smart LLM

### <a id="en-llm-description"></a>Description

The **TA Smart LLM** connects ComfyUI to local LLM backends (**LM Studio** and **Ollama**) for automatic prompt generation. It supports two use cases:

- **Text2Prompt** – Generates a detailed image prompt from a short description or instruction.
- **Image2Prompt** – Sends an existing image together with a text prompt to a vision model, which generates a new or descriptive prompt from it.

The node automatically detects which models are vision-capable and marks them in the dropdown with the suffix `[Vision]`. It returns the generated prompt as a `STRING` along with a status string that can be used directly for workflow diagnostics.

---

### <a id="en-llm-io"></a>Inputs & Outputs

#### Inputs

| Name | Type | Description |
|------|------|-------------|
| `llm_enable` | BOOLEAN | Master toggle. When `OFF`, the node is skipped and returns an empty string. |
| `model` | Dropdown | LLM model selection. Auto-populated from LM Studio and Ollama. Vision models are marked with `[Vision]`. |
| `user_prompt` | STRING | Main input for the LLM (Text2Prompt or image description instruction). |
| `system_prompt` | STRING | System instruction for the model, e.g. role or output format. |
| `unload_image_models_first` | BOOLEAN | Unloads ComfyUI image models before the LLM request to free VRAM. |
| `unload_llm_after` | BOOLEAN | Unloads the LLM model from the backend after generation. |
| `image` | IMAGE *(optional)* | Image input for vision models (Image2Prompt). Ignored if no vision model is selected. |

#### Outputs

| Name | Type | Description |
|------|------|-------------|
| `prompt` | STRING | The generated prompt text. |
| `status` | STRING | Execution status, e.g. `LMStudio/model ✅`, `DISABLED`, `SKIPPED - Ollama not reachable`. |

---

### <a id="en-llm-vision"></a>Vision Model Detection

The node automatically detects vision models based on the model name. Models whose names contain keywords such as `vision`, `llava`, `vl`, `moondream`, or `qwen-vl` are automatically marked with `[Vision]` in the dropdown.

If a `[Vision]` model is selected **and** an image is connected to the `image` input, the image is base64-encoded and sent together with the text prompt to the model (Image2Prompt).

Models that are not detected automatically can be added manually to `VISION_MANUAL` in `ta_smart_llm.py`.

---

### <a id="en-llm-cache"></a>Model Caching

On startup, the node queries LM Studio (port `1234`) and Ollama (port `11434`) for available models. The results are saved to `ta_smart_llm_models.json` in the node pack directory.

If a backend is unavailable on the next startup, the last known models are loaded from the cache and shown in the dropdown – keeping the dropdown populated even when a backend is stopped.

> ⚠️ **ComfyUI must be restarted** for newly installed models to appear in the dropdown.

---

### <a id="en-llm-tips"></a>Tips & Notes

**No backend reachable**
If neither LM Studio nor Ollama is reachable at ComfyUI startup and no cache exists, the dropdown shows `No Backend`. When executed, the node returns `SKIPPED` as status and does not cause a workflow error.

**ComfyUI restart after model installation**
Newly installed models in LM Studio or Ollama only appear in the dropdown after restarting ComfyUI, as the model list is only populated at startup.

**VRAM management**
`unload_image_models_first` is useful when VRAM is tight – it unloads all ComfyUI image models before the LLM loads. `unload_llm_after` frees VRAM after generation before the rest of the workflow loads image models.

**Image2Prompt**
For Image2Prompt, select a `[Vision]` model and connect an image to the `image` input. Enter the desired instruction in `user_prompt`, e.g. `Describe this image as a detailed Stable Diffusion prompt.`

---
---

## <a id="en-ph"></a>🔀 TA Prompt Hub

### <a id="en-ph-description"></a>Description

The **TA Prompt Hub** is a central collection point for all prompt inputs in a workflow. It bundles positive prompt, additional prompt, negative prompt, and optional LoRA trigger words into a single node – with no logic of its own, purely as a pass-through.

It also provides a `combined_prompt` output that automatically joins `positive_prompt`, `additional_prompt`, and `lora_trigger_words` with `, ` (empty parts are skipped).

For mode switching (e.g. between different prompt sources), the **TAPromptController** is responsible – the TA Prompt Hub contains no routing logic.

---

### <a id="en-ph-io"></a>Inputs & Outputs

#### Inputs

| Name | Type | Description |
|------|------|-------------|
| `positive_prompt` | STRING | Main positive prompt. Supports Dynamic Prompts. |
| `additional_prompt` | STRING | Secondary positive prompt, e.g. for style or scene – without LoRA trigger words. |
| `negative_prompt` | STRING | Negative prompt. Supports Dynamic Prompts. |
| `lora_trigger_words` | STRING *(optional)* | LoRA trigger words from an upstream LoRA node. Empty if not connected. |

#### Outputs

| Name | Type | Description |
|------|------|-------------|
| `positive_prompt` | STRING | Pass-through of the main positive prompt |
| `additional_prompt` | STRING | Pass-through of the additional prompt |
| `negative_prompt` | STRING | Pass-through of the negative prompt |
| `lora_trigger_words` | STRING | Pass-through of the LoRA trigger words |
| `combined_prompt` | STRING | Auto-joined prompt from `positive_prompt`, `additional_prompt`, and `lora_trigger_words` (non-empty parts, separated by `, `) |

---

### <a id="en-ph-tips"></a>Tips & Notes

**combined_prompt**
Empty fields are automatically skipped when joining. For example, if `additional_prompt` is empty, `combined_prompt` will only contain `positive_prompt` and `lora_trigger_words`.

**No routing logic**
The TA Prompt Hub does not switch between prompt sources. That responsibility belongs to the **TAPromptController**.

**LoRA trigger words**
`lora_trigger_words` is an optional input – it does not need to be connected. If not connected, it is treated as an empty string.

---
---

## <a id="en-pc"></a>🗂️ TA Prompt Controller

### <a id="en-pc-description"></a>Description

The **TA Prompt Controller** manages the prompt flow between a manually typed prompt and a generated prompt (e.g. from TA Smart LLM or a VLM node). A mode selector determines which source is used or how both are combined.

It is designed as the central prompt routing node in TA workflows and works closely with the **TA Prompt Hub**: the TA Prompt Hub collects all prompt inputs, while the TA Prompt Controller decides which one is forwarded.

**Available modes:**

| Mode | Description |
|------|-------------|
| `Manual Only` | Returns `manual_prompt` unchanged |
| `Generated Only` | Returns `generated_prompt` unchanged |
| `Combine: Manual + Generated` | Joins manual and generated prompt with the delimiter |
| `Combine: Generated + Manual` | Joins generated and manual prompt in reverse order |
| `Clear / Empty` | Always returns an empty string |

---

### <a id="en-pc-io"></a>Inputs & Outputs

#### Inputs

| Name | Type | Description |
|------|------|-------------|
| `manual_prompt` | STRING | Manually typed prompt. Supports Dynamic Prompts. |
| `mode` | Dropdown | Routing mode (see above). |
| `delimiter` | STRING | Separator between prompts in Combine modes. Default: `, ` |
| `generated_prompt` | STRING *(optional)* | Generated prompt from an upstream LLM/VLM node. Empty if not connected. |

#### Outputs

| Name | Type | Description |
|------|------|-------------|
| `final_prompt` | STRING | The resulting prompt according to the selected mode |

---

### <a id="en-pc-tips"></a>Tips & Notes

**Combine modes with only one input**
In a Combine mode, if only one of the two prompts is non-empty, it is returned directly without the delimiter – no stray `, ` at the start or end.

**Clear / Empty**
The `Clear / Empty` mode always returns an empty string regardless of the inputs – useful for deliberately interrupting the prompt flow in a workflow.

**Working with TA Prompt Hub**
The TA Prompt Hub collects all prompt parts; the TA Prompt Controller decides which source or combination is passed on as `final_prompt`. The `final_prompt` is then typically connected to the `positive_prompt` input of the TA Prompt Hub or directly to the conditioning.

---
---

## <a id="en-sampler"></a>🎛️ TA Sampler Preset & ⚡ TA KSampler

### <a id="en-sampler-description"></a>Description

**TA Sampler Preset** and **TA KSampler** are designed as a pair and together replace the built-in ComfyUI KSampler.

The **TA Sampler Preset** loads sampler configurations (steps, CFG, sampler, scheduler, start/end step) from `ta_sampler_presets.json` and exposes all parameters as individual outputs. These are directly connectable to the TA KSampler inputs.

The **TA KSampler** accepts `sampler_name` and `scheduler` as plain `STRING` inputs instead of fixed dropdowns – making it directly compatible with TA Sampler Preset. It also provides a live latent preview after every sampling step, identical in behaviour to the built-in ComfyUI KSampler.

Presets can be managed through the built-in browser editor.

---

### <a id="en-sampler-io"></a>Inputs & Outputs

#### TA Sampler Preset – Inputs

| Name | Type | Description |
|------|------|-------------|
| `preset` | Dropdown | Name of the preset to load. Options from `ta_sampler_presets.json`. |

#### TA Sampler Preset – Outputs

| Name | Type | Description |
|------|------|-------------|
| `steps` | INT | Number of sampling steps |
| `cfg` | FLOAT | CFG guidance scale |
| `sampler_name` | STRING | Sampler algorithm name, e.g. `euler` |
| `scheduler` | STRING | Noise scheduler name, e.g. `karras` |
| `start_at_step` | INT | First active sampling step |
| `end_at_step` | INT | Last active sampling step |
| `info` | STRING | Formatted summary of all preset parameters |

#### TA KSampler – Inputs

| Name | Type | Description |
|------|------|-------------|
| `model` | MODEL | The model to use |
| `add_noise` | enable/disable | Add noise to the latent |
| `noise_seed` | INT | Seed for noise generation |
| `steps` | INT | Number of sampling steps |
| `cfg` | FLOAT | CFG guidance scale |
| `sampler_name` | STRING | Sampler algorithm, e.g. `euler`, `dpmpp_2m` |
| `scheduler` | STRING | Noise scheduler, e.g. `normal`, `karras`, `beta` |
| `positive` | CONDITIONING | Positive conditioning |
| `negative` | CONDITIONING | Negative conditioning |
| `latent_image` | LATENT | Input latent |
| `start_at_step` | INT | First active sampling step |
| `end_at_step` | INT | Last active sampling step |
| `return_with_leftover_noise` | enable/disable | Keep residual noise in the output |
| `preview` | BOOLEAN | Enable live latent preview after each step |

#### TA KSampler – Outputs

| Name | Type | Description |
|------|------|-------------|
| `latent` | LATENT | The resulting latent after sampling |

---

### <a id="en-sampler-editor"></a>Browser Editor

Presets can be created, edited, and deleted through the built-in browser editor. Sampler and scheduler names are automatically offered as dropdowns populated from ComfyUI's own lists.

**Open at:**
```
http://localhost:8188/ta_sampler_presets/ui
```

> ⚠️ **ComfyUI must be restarted after changes** for the dropdown in the node to reflect the new presets.

---

### <a id="en-sampler-json"></a>JSON File Structure

The file `ta_sampler_presets.json` is located in the root directory of the node pack:

```json
{
    "Z-Image Turbo": {
        "steps": 9,
        "cfg": 1.0,
        "start_at_step": 0,
        "end_at_step": 9999,
        "sampler_name": "euler",
        "scheduler": "beta"
    }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `steps` | INT | Number of sampling steps |
| `cfg` | FLOAT | CFG guidance scale |
| `start_at_step` | INT | First active step (0 = from the beginning) |
| `end_at_step` | INT | Last active step (9999 = run to completion) |
| `sampler_name` | STRING | Sampler algorithm |
| `scheduler` | STRING | Noise scheduler |

The file is created automatically with an example preset on first launch.

---

### <a id="en-sampler-tips"></a>Tips & Notes

**Direct connection**
All outputs of TA Sampler Preset can be connected directly to the corresponding inputs of TA KSampler – no manual value entry needed.

**Unknown sampler or scheduler**
If TA Sampler Preset outputs a `sampler_name` or `scheduler` that is not registered in ComfyUI, TA KSampler automatically falls back to `euler` and `normal` respectively, and prints a warning to the console.

**Live preview**
The `preview` toggle on TA KSampler enables a Latent2RGB preview after every step. Behaviour is identical to the built-in ComfyUI KSampler. Preview can be disabled if performance is an issue.

**info output**
The `info` output of TA Sampler Preset contains a formatted summary of all parameters and is also used by **TAFluxGuidanceGate** – if the preset name contains `FLUX`, flux guidance is activated automatically.

**ComfyUI restart**
Newly created presets only appear in the dropdown after restarting ComfyUI.

---
---

## <a id="en-cs"></a>🧹 TA Cleanup Switch

### <a id="en-cs-description"></a>Description

The **TA Cleanup Switch** combines VRAM and RAM cleanup in a single switchable node. It replaces the previous three-node chain (Clear Cache All → VRAM-Cleanup → RAM-Cleanup) and can be fully disabled via an enable toggle – with zero overhead when off.

The node passes an optional signal input through unchanged, making it easy to insert into an existing node chain.

---

### <a id="en-cs-io"></a>Inputs & Outputs

#### Inputs

| Name | Type | Description |
|------|------|-------------|
| `enabled` | BOOLEAN | Master toggle. When `OFF`, all cleanup operations are skipped entirely. |
| `offload_model` | BOOLEAN | Unloads all ComfyUI image models from VRAM (`unload_all_models()`). |
| `offload_cache` | BOOLEAN | Clears the GPU cache (`soft_empty_cache()`) and runs Python garbage collection. |
| `retry_times` | INT | Number of RAM cleanup repetitions (default: 3). |
| `signal` | * *(optional)* | Any signal to pass through – e.g. a latent or image to control execution order. |

#### Outputs

| Name | Type | Description |
|------|------|-------------|
| `signal` | * | The incoming signal passed through unchanged. |

---

### <a id="en-cs-tips"></a>Tips & Notes

**VRAM cleanup**
`offload_model` calls `unload_all_models()`, `offload_cache` additionally calls `soft_empty_cache()` and `gc.collect()`. Both can be toggled independently.

**RAM cleanup (Windows)**
On Windows, `SetSystemFileCacheSize`, `EmptyWorkingSet` (on all running processes), and `SetProcessWorkingSetSize` are called. On Linux, `malloc_trim()` is used. The number of passes is configurable via `retry_times`.

**Signal passthrough**
The `signal` input accepts any type (`*`), allowing the cleanup node to be inserted anywhere in a workflow without interrupting data connections.

**Disabled = zero overhead**
When `enabled=False`, the entire node is skipped – no cleanup takes place and the signal is forwarded immediately.

---
---

## <a id="en-fgg"></a>🌊 TA Flux Guidance Gate

### <a id="en-fgg-description"></a>Description

The **TA Flux Guidance Gate** applies Flux Guidance to a conditioning tensor – but only when the active sampler preset is a FLUX preset. For all other presets the conditioning is passed through unchanged.

Detection is automatic based on the `info` output of the **TA Sampler Preset**: if the preset name contains `FLUX` (case-insensitive), the guidance is injected. No manual switching is needed when changing between FLUX and non-FLUX models.

---

### <a id="en-fgg-io"></a>Inputs & Outputs

#### Inputs

| Name | Type | Description |
|------|------|-------------|
| `conditioning` | CONDITIONING | The conditioning to be modified or passed through. |
| `guidance` | FLOAT | Flux Guidance scale (default: 3.5). Only applied for FLUX presets. |
| `preset_info` | STRING | The `info` output from a TA Sampler Preset node. Used for FLUX detection. |

#### Outputs

| Name | Type | Description |
|------|------|-------------|
| `conditioning` | CONDITIONING | The modified conditioning (for FLUX) or unchanged (for other presets). |

---

### <a id="en-fgg-tips"></a>Tips & Notes

**Automatic FLUX detection**
The node checks whether the preset name in the `info` string contains the word `FLUX`. It is sufficient to name the preset accordingly in TA Sampler Preset (e.g. `FLUX Dev` or `My FLUX Preset`).

**No manual switching**
When switching from a FLUX to a non-FLUX preset in TA Sampler Preset, guidance is automatically disabled – no manual workflow changes needed.

**Connect preset_info**
The `preset_info` input must be connected to the `info` output of a TA Sampler Preset node. If not connected or empty, the conditioning is always passed through unchanged.

---
---

## <a id="en-sat"></a>🔧 TA SageAttention Toggler

### <a id="en-sat-description"></a>Description

The **TA SageAttention Toggler** patches a ComfyUI MODEL with SageAttention and/or PyTorch FP16 matmul acceleration. Both patches are independent and can be toggled individually.

**SageAttention** replaces the standard attention function with a quantised CUDA/Triton kernel for faster inference. Five kernel variants are available.

**FP16 matmul** enables `torch.backends.cuda.matmul.allow_fp16_accumulation` for additional throughput on supported hardware. Requires PyTorch Nightly 2.7+.

---

### <a id="en-sat-io"></a>Inputs & Outputs

#### Inputs

| Name | Type | Description |
|------|------|-------------|
| `model` | MODEL | The ComfyUI model to patch. |
| `sage_enable` | BOOLEAN | Enable/disable the SageAttention patch. |
| `torch_enable` | BOOLEAN | Enable/disable the PyTorch FP16 matmul patch. |
| `sage_mode` | Dropdown | SageAttention kernel variant (see below). |

#### Outputs

| Name | Type | Description |
|------|------|-------------|
| `model` | MODEL | The patched model. |

---

### <a id="en-sat-modes"></a>SageAttention Modes

| Mode | Description |
|------|-------------|
| `auto` | Standard `sageattn()` entry point, automatic selection. |
| `sageattn_qk_int8_pv_fp16_cuda` | QK INT8 + PV FP16, CUDA kernel. Recommended for Ampere GPUs (RTX 30xx). |
| `sageattn_qk_int8_pv_fp16_triton` | QK INT8 + PV FP16, Triton kernel. |
| `sageattn_qk_int8_pv_fp8_cuda` | QK INT8 + PV FP8, CUDA kernel. |
| `sageattn_qk_fp8_pv_fp8_cuda` | QK FP8 + PV FP8, CUDA kernel. Maximum compression. |

---

### <a id="en-sat-tips"></a>Tips & Notes

**Recommendation for RTX 3090 (Ampere)**
The `sageattn_qk_int8_pv_fp16_cuda` mode is optimal on Ampere GPUs and offers the best balance of speed and quality.

**SageAttention not installed**
If the `sageattention` package is not installed, `sage_active` is set to `False` and the patch is skipped. Install with: `pip install sageattention-nightly`

**FP16 matmul**
The Torch patch sets `allow_fp16_accumulation = True` globally for the CUDA backend session. After sampling, the value is automatically restored if the model supports `_torch_callbacks`. Requires PyTorch Nightly 2.7+.

**Both patches are independent**
`sage_enable` and `torch_enable` can be combined freely – either individually or both disabled.

---
---

## <a id="en-fg"></a>📁 TA Filename Generator

### <a id="en-fg-description"></a>Description

The **TA Filename Generator** creates structured output paths for saved images. It combines an optional output folder, an optional subfolder (supporting strftime date codes), a name prefix, workflow version, model name, and a formatted timestamp.

Returns two paths: a base path and an upscaled path – both directly compatible with the TA Save Image nodes.

---

### <a id="en-fg-io"></a>Inputs & Outputs

#### Inputs

| Name | Type | Description |
|------|------|-------------|
| `model_name` | TA_MODEL_NAME *(optional)* | Model name string from a TALoadModelWithName node. Fallback: `model`. |
| `output_folder` | STRING | Root output folder. Default: `TA-Outputs`. |
| `subfolder` | STRING | Optional subfolder. Supports strftime codes like `%Y-%m-%d`. |
| `name_prefix` | STRING | Short prefix prepended to the filename. Default: `TA`. |
| `wf_version` | STRING | Workflow version tag, e.g. `v2.60`. |
| `upscaled_suffix` | STRING | Suffix appended to the upscaled path. Default: `UPSCALED`. |
| `delimiter` | STRING | Separator between filename parts. Default: `-`. |
| `date_format` | Dropdown | strftime format for the timestamp in the filename. |

#### Outputs

| Name | Type | Description |
|------|------|-------------|
| `filename` | STRING | Full base file path, OS-normalised. |
| `filename_up` | STRING | Full upscaled file path with the suffix appended. |

---

### <a id="en-fg-tips"></a>Tips & Notes

**Subfolder with date codes**
The `subfolder` input processes strftime codes at execution time. For example, `%Y-%m-%d` becomes `2026-03-12`. Invalid codes are used as literal strings.

**Filename scheme**
The generated filename follows the pattern: `{prefix}{delim}{wf_version}{delim}{model_name}{delim}{date}`. Example: `TA-v2.60-flux-dev-202603121430`

**Upscaled path**
`filename_up` is identical to `filename` but with the `upscaled_suffix` appended – ready to use for the upscale branch of your workflow.

**No empty segments**
Empty parts (e.g. no subfolder) are automatically filtered out of the path – no double separators.

---
---

## <a id="en-save"></a>💾 TA Save Image Optional & TA Save Image With Prompt

### <a id="en-save-description"></a>Description

Both nodes extend ComfyUI's built-in `SaveImage` node. The main differences are output format and the enable toggle:

| Node | Format | Enable Toggle |
|------|--------|---------------|
| **TA Save Image Optional** | JPEG or WebP (configurable quality) | ✅ Yes – can be disabled |
| **TA Save Image With Prompt** | PNG (standard ComfyUI logic) | ❌ No – always saves |

Both nodes optionally write a companion `.txt` file per image containing the positive/negative prompt, timestamp, and filename reference.

---

### <a id="en-save-io"></a>Inputs & Outputs

#### TA Save Image Optional – Inputs

| Name | Type | Description |
|------|------|-------------|
| `images` | IMAGE | Image tensor batch to save. |
| `filename_prefix` | STRING | Base filename. Existing image suffixes (`.jpg`, `.png` etc.) are stripped automatically. |
| `enabled` | BOOLEAN | Master toggle. When `OFF` the node is skipped and images are passed through. |
| `save_txt` | enabled/disabled | Write a companion `.txt` file per image. |
| `positive_prompt` | STRING | Positive prompt for the `.txt` file. |
| `negative_prompt` | STRING | Negative prompt for the `.txt` file. |
| `save_format` | jpg / webp *(optional)* | Output format. Default: `jpg`. |
| `jpeg_quality` | 70–100 *(optional)* | Compression quality for JPEG and WebP. Default: `95`. |

#### TA Save Image With Prompt – Inputs

| Name | Type | Description |
|------|------|-------------|
| `images` | IMAGE | Image tensor batch to save. |
| `filename_prefix` | STRING | Base filename (standard ComfyUI convention). |
| `positive_prompt` | STRING | Positive prompt for the `.txt` file. |
| `negative_prompt` | STRING | Negative prompt for the `.txt` file. |
| `save_txt` | enabled/disabled | Write a companion `.txt` file per image. |

#### Outputs (both nodes)

| Name | Type | Description |
|------|------|-------------|
| `IMAGE` | IMAGE | The input image passed through unchanged. |

---

### <a id="en-save-txt"></a>TXT Companion File

When `save_txt` is enabled, a `.txt` file is written per image with the following content:

```
DATE / TIME: 2026-03-12 14:30:00
FILE: TA-v2.60-flux-dev-202603121430_00001_.jpg
==============================
POSITIVE PROMPT:
<positive prompt>

NEGATIVE PROMPT:
<negative prompt>
==============================
```

---

### <a id="en-save-tips"></a>Tips & Notes

**Which node to use?**
`TA Save Image Optional` offers more control (format, quality, can be disabled) and is suited for the main save branch. `TA Save Image With Prompt` is simpler and uses the full ComfyUI PNG save logic including UI preview metadata.

**Enable toggle (Optional)**
When `enabled=False`, images are passed through without saving anything – useful for quickly disabling the save step without restructuring the workflow.

**Filename compatibility**
The `filename` output of **TA Filename Generator** can be used directly as `filename_prefix` for both save nodes. Any image extension in the prefix is stripped automatically.

---
---

## <a id="en-svr2"></a>🎬 TA SeedVR2 Gate

### <a id="en-svr2-description"></a>Description

The **TA SeedVR2 Gate** controls execution of the SeedVR2 upscaler pipeline using ComfyUI lazy evaluation. When disabled, all upstream nodes (SeedVR2 model loaders, image source) are skipped entirely – they are never even requested. This prevents the ~14 GB SeedVR2 models from loading when the upscaler is not needed.

---

### <a id="en-svr2-io"></a>Inputs & Outputs

#### Inputs

| Name | Type | Description |
|------|------|-------------|
| `enabled` | BOOLEAN | Master toggle. `False` = all upstream nodes are skipped entirely. Default: `False`. |
| `image` | IMAGE *(lazy, optional)* | Input image for the upscaler. Only requested when `enabled=True`. |
| `dit` | SEEDVR2_DIT *(lazy, optional)* | Loaded SeedVR2 DiT model. Only requested when `enabled=True`. |
| `vae` | SEEDVR2_VAE *(lazy, optional)* | Loaded SeedVR2 VAE model. Only requested when `enabled=True`. |

#### Outputs

| Name | Type | Description |
|------|------|-------------|
| `image` | IMAGE | Image passed through (when `enabled=True`) or blocked. |
| `dit` | SEEDVR2_DIT | DiT model passed through or blocked. |
| `vae` | SEEDVR2_VAE | VAE model passed through or blocked. |

---

### <a id="en-svr2-tips"></a>Tips & Notes

**Lazy evaluation**
The node uses `check_lazy_status()` – ComfyUI only requests the optional inputs (`image`, `dit`, `vae`) when `enabled=True`. When disabled, the SeedVR2 loader nodes never run, saving VRAM and load time.

**Default: disabled**
The default value is `False` – the upscaler is off by default. This is intentional to avoid accidentally loading the large models.

**ExecutionBlocker**
When `enabled=False`, the node returns `ExecutionBlocker(None)` placeholders that block all downstream nodes in this branch.

---
---

## <a id="en-dl"></a>💬 TA Discord Link

### <a id="en-dl-description"></a>Description

The **TA Discord Link** is a purely informational node that displays a clickable Discord invite link directly inside the ComfyUI graph. It has no inputs and no outputs.

The invite URL and button label are stored in `ta_discord_link.json` and can be changed via the built-in browser editor.

**Browser editor:**
```
http://localhost:8188/ta_discord_link/ui
```

---

### <a id="en-dl-tips"></a>Tips & Notes

**Changing the URL**
The default URL `https://discord.gg/YOUR_INVITE_CODE` must be updated once after installation via the browser editor to point to your own Discord invite.

**No restart needed**
Changes made via the browser editor are saved to `ta_discord_link.json` immediately. The button in the graph reflects the new URL on the next workflow load.


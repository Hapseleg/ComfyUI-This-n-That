#  Package Modules
import json
import os
import csv

# SimpleRatioSelector
def read_ratio_presets():
    p = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(p, "..\preset_ratios.csv")
    preset_ratios_dict = {}
    labels = []
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter="|", quotechar='"')
        for row in reader:
            preset_ratios_dict[row[0]] = [row[1], row[2]]
            labels.append(row[0])
    return preset_ratios_dict, labels

class SimpleRatioSelector:
    @classmethod
    def INPUT_TYPES(s):
        s.ratio_presets = read_ratio_presets()[1]
        s.preset_ratios_dict = read_ratio_presets()[0]
        return {
            "required": {
                "select_preset": (
                    s.ratio_presets,
                    {
                        "default": s.ratio_presets[0],
                        "tooltip": "Select a preset dimensions (Width x Height)",
                    },
                ),
                "portrait": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "This flips the orientation from landscape (Width x Height) to portrait (Height x Width)",
                    },
                ),
            },
            "hidden": {"unique_id": "UNIQUE_ID", "extra_pnginfo": "EXTRA_PNGINFO", "prompt": "PROMPT"},
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    CATEGORY = "utils"
    FUNCTION = "run"

    def run(self, select_preset, portrait, unique_id=None, extra_pnginfo=None, prompt=None):
        width, height = self.preset_ratios_dict[select_preset] # sample output: ['1920', '1080']
        
        #  If portrait is True, flip the width and height
        if portrait:
            width, height = height, width

        return (int(width), int(height))


# --------------------------------------------------
class ShowPrompt:
    def __init__(self):
        self.num = 0
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": ("BOOLEAN", {"default": True, "label_on": "prompt", "label_off": "workflow"}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID",}
        }

    CATEGORY = "utils/this_and_that"
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "run"
    OUTPUT_NODE = True

    def run(self, mode, unique_id, text="", prompt=None, **kwargs):
        # Force update
        def IS_CHANGED(self):
                self.num += 1 if self.num == 0 else -1
                return self.num
        setattr(self.__class__, 'IS_CHANGED', IS_CHANGED)
        
        clean_prompt = prompt
        for n in clean_prompt:
            if n == unique_id:
                clean_prompt[n]["inputs"]["display"] = ""
                # I assume theres max 1 of these nodes in the workflow... BREAK
                break
        text = json.dumps(clean_prompt)
        
        return {"ui": {"text": text}}


NODE_CLASS_MAPPINGS = {
    "Simple Ratio Selector (Hapse)": SimpleRatioSelector,
    "Show Prompt (Hapse)": ShowPrompt,
}
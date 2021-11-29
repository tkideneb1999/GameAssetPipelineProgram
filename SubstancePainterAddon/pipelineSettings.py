import os
from pathlib import Path
import json
import importlib

if __package__ == "":
    import PipelineConfigurator.pipelineSettingsCreator as pSC
else:
    from .GAPACore import pipelineSettingsCreator as pSC
    importlib.reload(pSC)


def get_pipeline_settings_location() -> str:
    return os.path.abspath(__file__)


def load_config(file_path) -> dict:
    """
    :param file_path: Path object to config file
    :return: data read from config file
    """
    data = {}
    with file_path.open("r", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


def create_pipeline_settings() -> pSC.PipelineSettingsCreator:
    pipeline_settings = pSC.PipelineSettingsCreator()
    pipeline_settings.has_set_outputs = True
    pipeline_settings.export_all = True
    # Add Configurations from json files in Config Directory
    configs_dir = Path(get_pipeline_settings_location()).parent / "Configs"
    print(f"[GAPA] searching for configs at: {str(configs_dir)}")
    config_paths = list(configs_dir.glob("*.json"))
    for config_path in config_paths:
        data = load_config(config_path)
        inputs = []
        for i in data["input"]["inputs"]:
            inputs.append((i["inputName"], i["type"]))
        outputs = []
        for o in data["output"]["outputs"]:
            outputs.append((o["outputName"], o["type"]))
        print(f"[GAPA] Inputs: {inputs}")
        print(f"[GAPA] Outputs: {outputs}")
        pipeline_settings.add_configuration(data["name"], inputs, outputs)

    # Add additional settings
    #   Normal Map type (OpenGL/DirectX)
    pipeline_settings.add_combobox_selection("Normal Map", ["Direct X", "OpenGL"])
    #   UDIM Workflow
    pipeline_settings.add_combobox_selection("UDIM Workflow", ["No UDIM", "Texture Set per UV Tile", "UV Tile"])
    #   Import Cameras
    pipeline_settings.add_checkbox("Import Cameras", False)
    #   Tangent per Fragment
    pipeline_settings.add_checkbox("Fragment Tangent", True)
    return pipeline_settings

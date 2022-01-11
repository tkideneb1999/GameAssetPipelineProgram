import os
from pathlib import Path

if __package__ == "":
    from MainApplication.PipelineConfigurator import pipelineSettingsCreator as pSC
else:
    from .Core import pipelineSettingsCreator as pSC


def get_pipeline_settings_location() -> str:
    return os.path.abspath(__file__)


def create_pipeline_settings() -> pSC.PipelineSettingsCreator:
    step_settings = pSC.PipelineSettingsCreator(configs_dir=Path(get_pipeline_settings_location()).parent / "Configs")
    step_settings.has_set_outputs = False
    step_settings.set_export_data_types(["fbx", "obj"])
    return step_settings

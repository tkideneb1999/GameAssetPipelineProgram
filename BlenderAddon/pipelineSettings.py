import os
from pathlib import Path

import pluginAPI


def get_pipeline_settings_location() -> str:
    return os.path.abspath(__file__)


def create_pipeline_settings() -> pluginAPI.PluginSettings:
    step_settings = pluginAPI.PluginSettings()
    step_settings.has_set_outputs = False
    step_settings.set_export_data_types(["fbx", "obj"])
    return step_settings

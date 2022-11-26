import os

import pluginAPI

WORKFILE_SUFFIX = "uproject"


def get_pipeline_settings() -> str:
    return os.path.abspath(__file__)


def create_pipeline_settings() ->pluginAPI.PluginSettings:
    step_settings = pluginAPI.PluginSettings()
    step_settings.has_set_outputs = False
    step_settings.export_all = False
    step_settings.set_export_data_types(["fbx", "obj"])
    step_settings.add_lineedit("Project File", pluginAPI.SettingsEnum.PROJECT)
    return step_settings

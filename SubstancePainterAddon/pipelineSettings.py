import os
from pathlib import Path
import importlib
import pluginAPI
importlib.reload(pluginAPI)


WORKFILE_SUFFIX = "spp"


def get_pipeline_settings_location() -> str:
    return os.path.abspath(__file__)


def create_pipeline_settings() -> pluginAPI.PluginSettings:
    settings_template = pluginAPI.PluginSettings(
        config_dir=Path(get_pipeline_settings_location()).parent / "Configs")

    # Set outputs (if outputs can be multiple sets, e.g. multiple texture sets)
    settings_template.has_set_outputs = True
    settings_template.set_export_data_types(["tga", "png", "tiff"])

    # Export all outputs at once
    settings_template.export_all = True

    # Add additional settings
    #   Normal Map type (OpenGL/DirectX)
    settings_template.add_combobox("Normal Map",
                                   pluginAPI.SettingsEnum.PIPELINE,
                                   ["Direct X", "OpenGL"])
    #   UDIM Workflow
    settings_template.add_combobox("UDIM Workflow",
                                   pluginAPI.SettingsEnum.PIPELINE,
                                   ["No UDIM", "Texture Set per UV Tile", "UV Tile"])
    #   Import Cameras
    settings_template.add_checkbox("Import Cameras",
                                   pluginAPI.SettingsEnum.PIPELINE,
                                   False)
    #   Tangent per Fragment
    settings_template.add_checkbox("Fragment Tangent",
                                   pluginAPI.SettingsEnum.PIPELINE,
                                   True)
    return settings_template

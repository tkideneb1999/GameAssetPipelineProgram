import os
from pathlib import Path
import json
import importlib

if __package__ == "":
    import MainApplication.PipelineConfigurator.pipelineSettingsCreator as pSC
else:
    from .Core import pipelineSettingsCreator as pSC
    importlib.reload(pSC)


def get_pipeline_settings_location() -> str:
    return os.path.abspath(__file__)


def create_pipeline_settings() -> pSC.PipelineSettingsCreator:
    pipeline_settings = pSC.PipelineSettingsCreator(
        configs_dir=Path(get_pipeline_settings_location()).parent / "Configs")

    # Set outputs (if outputs can be multiple sets, e.g. multiple texture sets)
    pipeline_settings.has_set_outputs = True

    # Export all outputs at once
    pipeline_settings.export_all = True

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

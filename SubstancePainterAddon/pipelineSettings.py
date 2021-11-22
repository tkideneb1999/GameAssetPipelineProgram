import os
import importlib

if __package__ == "":
    import PipelineConfigurator.pipelineSettingsCreator as pipelineSettingsCreator
else:
    from .GAPACore import pipelineSettingsCreator
    importlib.reload(pipelineSettingsCreator)


def get_pipeline_settings_location() -> str:
    return os.path.abspath(__file__)


def create_pipeline_settings() -> pipelineSettingsCreator.PipelineSettingsCreator:
    pipeline_settings = pipelineSettingsCreator.PipelineSettingsCreator()
    # Read Substance Painter Export Presets

    # Add Presets as Configuration
    pipeline_settings.add_configuration("UE4",
                                        [("lowpoly", "3D Asset"), ("highpoly", "3D Asset")],
                                        [("DA", "texture"), ("N", "texture"), ("ORM", "texture")])
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

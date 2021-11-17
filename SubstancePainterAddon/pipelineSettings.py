import os

if __package__ == "":
    from PipelineConfigurator.pipelineSettingsCreator import PipelineSettingsCreator
else:
    from .Core.pipelineSettingsCreator import PipelineSettingsCreator


def get_pipeline_settings_location() -> str:
    return os.path.abspath(__file__)


def create_pipeline_settings() -> PipelineSettingsCreator:
    # Read Substance Painter JSON Export Presets

    # Add Presets as Configuration

    # Add additional settings
    #   Normal Map type (OpenGL/DirectX)
    #   Import Cameras
    pass

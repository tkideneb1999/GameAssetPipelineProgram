import os

if __package__ == "":
    from PipelineConfigurator.pipelineSettingsCreator import PipelineSettingsCreator
else:
    from .Core.pipelineSettingsCreator import PipelineSettingsCreator


def get_pipeline_settings_location() -> str:
    return os.path.abspath(__file__)


def create_pipeline_settings() -> PipelineSettingsCreator:
    step_settings = PipelineSettingsCreator()
    step_settings.add_configuration("highpoly", [], [("highpoly", "3D Asset")])
    step_settings.add_configuration("lowpoly", [("highpoly", "3D Asset")], [("lowpoly", "3D Asset")])
    step_settings.add_configuration("highAndLow", [], [("highpoly", "3D Asset"), ("lowpoly", "3D Asset")])
    return step_settings

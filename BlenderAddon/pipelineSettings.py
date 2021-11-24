import os

if __package__ == "":
    from MainApplication.PipelineConfigurator import pipelineSettingsCreator as pSC
else:
    from .Core import pipelineSettingsCreator as pSC


def get_pipeline_settings_location() -> str:
    return os.path.abspath(__file__)


def create_pipeline_settings() -> pSC.PipelineSettingsCreator:
    step_settings = pSC.PipelineSettingsCreator()
    step_settings.has_multi_outputs = False
    step_settings.add_configuration("highpoly", [], [("highpoly", pSC.IOType.Mesh)])
    step_settings.add_configuration("lowpoly", [("highpoly", pSC.IOType.Mesh)], [("lowpoly", pSC.IOType.Mesh)])
    step_settings.add_configuration("highAndLow", [], [("highpoly", pSC.IOType.Mesh), ("lowpoly", pSC.IOType.Mesh)])
    return step_settings

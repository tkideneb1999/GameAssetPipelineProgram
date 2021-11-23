import os
import importlib

if __package__ == "":
    import PipelineConfigurator.pipelineSettingsCreator as pSC
else:
    from .GAPACore import pipelineSettingsCreator as pSC
    importlib.reload(pSC)


def get_pipeline_settings_location() -> str:
    return os.path.abspath(__file__)


def create_pipeline_settings() -> pSC.PipelineSettingsCreator:
    pipeline_settings = pSC.PipelineSettingsCreator()
    # Read Substance Painter Export Presets

    # Add Presets as Configuration
    pipeline_settings.add_configuration("UE4",
                                        [("lowpoly", pSC.IOType.Mesh),
                                         ("normal_base", pSC.IOType.Texture),
                                         ("ambient_occlusion", pSC.IOType.Texture),
                                         ("id", pSC.IOType.Texture),
                                         ("position", pSC.IOType.Texture),
                                         ("thickness", pSC.IOType.Texture),
                                         ("world_space_normals", pSC.IOType.Texture),
                                         ("curvature", pSC.IOType.Texture)],
                                        [("DA", pSC.IOType.Texture),
                                         ("N", pSC.IOType.Texture),
                                         ("ORM", pSC.IOType.Texture)])
    pipeline_settings.add_configuration("NoMaps",
                                        [("lowpoly", pSC.IOType.Mesh)],
                                        [("DA", pSC.IOType.Texture),
                                         ("N", pSC.IOType.Texture),
                                         ("ORM", pSC.IOType.Texture)])
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

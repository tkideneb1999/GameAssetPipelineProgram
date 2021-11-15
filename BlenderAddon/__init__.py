bl_info = {
    "name": " Game Asset Pipeline Automation",
    "blender": (2, 90, 3),
    "category": "Automation"
}


from pathlib import Path
import os

import bpy

from . import GAPA_Export
from . import GAPA_Import
from . import preferences
from .Core.settings import Settings
from .pipelineSettings import get_pipeline_settings_location


def menu_func(self, context):
    self.layout.operator(GAPA_Export.GAPAExport.bl_idname)
    self.layout.operator(GAPA_Import.GAPAImport.bl_idname)


classes = [GAPA_Export.GAPAExport, GAPA_Import.GAPAImport, preferences.GAPA_Preferences]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_file.append(menu_func)
    # TODO(Blender Addon): set addon enabled in settings
    settings = Settings()
    settings.load()
    blender_path = Path(bpy.app.binary_path)
    # Get Current File
    addon_location = Path(get_pipeline_settings_location())
    settings.enable_addon(blender_path.stem, addon_location)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    bpy.types.TOPBAR_MT_file.remove(menu_func)

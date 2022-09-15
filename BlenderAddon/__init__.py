bl_info = {
    "name": " Game Asset Pipeline Automation",
    "blender": (2, 90, 3),
    "category": "Automation"
}


from pathlib import Path

import bpy

from . import settingsLoader
settingsLoader.load_required_packages(use_main_app_pyside=True)

from Common.Core.settings import Settings
SETTINGS = Settings()
SETTINGS.load()

from . import GAPAExport
from . import GAPAImport

from .pipelineSettings import get_pipeline_settings_location


def menu_func(self, context):
    self.layout.operator(GAPAExport.GAPAExport.bl_idname)
    self.layout.operator(GAPAImport.GAPAImport.bl_idname)


classes = [GAPAExport.GAPAExport, GAPAImport.GAPAImport]


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

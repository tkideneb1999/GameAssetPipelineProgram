import importlib
import importlib.util
from pathlib import Path

import substance_painter.logging as spLog
import substance_painter.ui as spUI

from . import settingsLoader
settingsLoader.load_required_packages(use_main_app_pyside=False)

from Common.Core import settings as settingsModule

importlib.reload(settingsModule)
SETTINGS = settingsModule.Settings()
SETTINGS.load()


from . import GAPAImport
from . import GAPAExport
from . import pipelineSettings as pipelineSettingsModule

importlib.reload(GAPAImport)
importlib.reload(GAPAExport)
importlib.reload(pipelineSettingsModule)


IMPORT_PLUGIN = None
EXPORT_PLUGIN = None

PROJECT_PATH = None
PROGRAM_NAME = "Adobe Substance 3D Painter"


def start_plugin():
    # register Plugin
    spLog.info("[GAPA] registering Addon")
    settings = settingsModule.Settings()
    settings.load()
    settings.enable_addon(PROGRAM_NAME, Path(pipelineSettingsModule.get_pipeline_settings_location()))
    spLog.info("[GAPA] starting Addon")
    global IMPORT_PLUGIN
    IMPORT_PLUGIN = GAPAImport.GAPAImport(PROGRAM_NAME, spUI.get_main_window())
    spUI.add_action(
        spUI.ApplicationMenu.File,
        IMPORT_PLUGIN.import_dialog_action
    )

    global EXPORT_PLUGIN
    EXPORT_PLUGIN = GAPAExport.GAPAExport(PROGRAM_NAME, spUI.get_main_window())
    spUI.add_action(
        spUI.ApplicationMenu.File,
        EXPORT_PLUGIN.export_dialog_action
    )


def close_plugin():
    global IMPORT_PLUGIN
    spUI.delete_ui_element(IMPORT_PLUGIN.import_dialog_action)
    del IMPORT_PLUGIN

    global EXPORT_PLUGIN
    spUI.delete_ui_element(EXPORT_PLUGIN.export_dialog_action)
    del EXPORT_PLUGIN

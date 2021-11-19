import importlib
from pathlib import Path

import substance_painter.logging as spLog
import substance_painter.ui as spUI

from . import GAPAImport
from .GAPACore import settings as settingsModule
from . import pipelineSettings as pipelineSettingsModule

importlib.reload(GAPAImport)
importlib.reload(settingsModule)
importlib.reload(pipelineSettingsModule)


IMPORT_PLUGIN = None
EXPORT_PLUGIN = None

PROJECT_PATH = None


def start_plugin():
    # register Plugin
    spLog.info("[GAPA] registering Addon")
    settings = settingsModule.Settings()
    settings.load()
    settings.enable_addon("Substance Painter", Path(pipelineSettingsModule.get_pipeline_settings_location()))
    spLog.info("[GAPA] starting Addon")
    global IMPORT_PLUGIN
    IMPORT_PLUGIN = GAPAImport.GAPAImport(spUI.get_main_window())
    spUI.add_action(
        spUI.ApplicationMenu.File,
        IMPORT_PLUGIN.testDialogAction
    )
    # Export Plugin


def close_plugin():
    global IMPORT_PLUGIN
    del IMPORT_PLUGIN

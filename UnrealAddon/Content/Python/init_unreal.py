from pathlib import Path

import unreal

import settingsLoader

settingsLoader.load_required_packages(use_main_app_pyside=True)
from Common.Core.settings import Settings
SETTINGS = Settings()
SETTINGS.load()


from GAPAImport import GAPAImport
from pipelineSettings import get_pipeline_settings

def check_settings_validity():
    if not SETTINGS.has_settings:
        unreal.log_error("[GAPA] No Project Dir set in Settings")
    return SETTINGS.has_settings


PROGRAM_NAME = "Unreal Engine"
PROJECT_PATH = unreal.Paths().get_project_file_path()
if check_settings_validity():
    IMPORT_WINDOW = GAPAImport(PROGRAM_NAME, SETTINGS.current_project_info_path)
SETTINGS.enable_addon(PROGRAM_NAME, Path(get_pipeline_settings()))


def GAPA_start_import():
    if not check_settings_validity():
        return
    unreal.log("[GAPA] Starting Import Process")
    IMPORT_WINDOW.start_import_window()


def update_imports():
    if not check_settings_validity():
        return
    unreal.log_error("[GAPA] Updating Imports NOT IMPLEMENTED")


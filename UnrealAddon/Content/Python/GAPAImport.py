import unreal

import sys

from PySide6 import QtWidgets as qtw

from Common.Dialogs.importWizardView import ImportWizardView
from Common.Core.settings import Settings

from pipelineSettings import WORKFILE_SUFFIX


class GAPAImport:
    def __init__(self, program_name, project_path=None):
        self._qt_app = (qtw.QApplication.instance() or qtw.QApplication(sys.argv))
        self._project_path = project_path
        self._qt_window = None
        self._program_name = program_name
        self._tick_handle = None

    def start_import_window(self):
        if self._project_path is None:
            settings = Settings()
            settings.load()
            if not settings.has_settings:
                unreal.log_error("[GAPA] No Project Dir Set")
                return
            self._project_path = settings.current_project_info_path
        unreal.log("[GAPA] Starting Asset Importer")

        self._qt_window = ImportWizardView(self._project_path, self._program_name, WORKFILE_SUFFIX)
        self._tick_handle = unreal.register_slate_post_tick_callback(self.__register_tick)
        self._qt_app.aboutToQuit.connect(self.__unregister_tick)

        # register Functions
        self._qt_window.register_import_files_func(self.import_files)
        self._qt_window.register_save_workfile_func(self.save_workfile)
        self._qt_window.show()

    def __register_tick(self, delta_seconds):
        self._qt_app.processEvents()

    def __unregister_tick(self):
        unreal.unregister_slate_post_tick_callback(self._tick_handle)

    def import_files(self, filepaths_data, config, additional_settings) -> None:
        unreal.log_error("[GAPA] Importing not implemented")

    def save_workfile(self, filepath) -> None:
        unreal.log_error("[GAPA] Saving not implemented")

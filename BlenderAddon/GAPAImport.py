from pathlib import Path
import sys
import queue

import bpy

from qtpy import QtWidgets as qtw
from qtpy import QtCore as qtc

from Common.Dialogs.importWizardView import ImportWizardView
from Common.Core.settings import Settings
from .pipelineSettings import WORKFILE_SUFFIX


class GAPAImport(bpy.types.Operator):
    """Game Asset Pipeline Automation Import"""
    bl_idname = "wm.gapa_import"
    bl_label = "GAPA Import"
    bl_options = {'REGISTER'}

    qt_app = None
    qt_window = None
    bpy_timer = None
    qt_counter = 0
    bpy_queue = queue.Queue()
    qt_queue = queue.Queue()
    project_path = None

    def __init__(self):
        super().__init__()
        self.qt_app = (qtw.QApplication.instance() or qtw.QApplication(sys.argv))

    def _execute_queued(self):
        while not self.bpy_queue.empty():
            function = self.bpy_queue.get()
            function()

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.qt_window and not self.qt_window.isVisible():
                self.cancel(context)
                print("[GAPA] Qt Window not Visible")
                return {"FINISHED"}

            self.qt_app.processEvents()
            self._execute_queued()
            self.qt_counter += 1
        return {"PASS_THROUGH"}

    def execute(self, context):
        if self.project_path is None:
            settings = Settings()
            settings.load()
            if not settings.has_settings:
                print("[GAPA] No Project dir set in GAPA Settings")
                return {'FINISHED'}
            self.project_path = settings.current_project_info_path
        print("[GAPA] Starting Asset Importer")

        self.qt_window = ImportWizardView(self.project_path, "blender", WORKFILE_SUFFIX)
        self._add_qt_timer()
        self.qt_window.register_save_workfile_func(self.save_workfile)
        self.qt_window.register_import_files_func(self.import_files)

        self.qt_window.show()

        wm = context.window_manager
        print("[GAPA][Bpy] Adding Timer")
        self.bpy_timer = wm.event_timer_add(0.001, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        print("[GAPA] Cancelling")
        wm = context.window_manager
        wm.event_timer_remove(self.bpy_timer)

    def _process_qt_queue(self):
        while not self.qt_queue.empty():
            function = self.qt_queue.get()
            print(f"[GAPA] Running function {function.func.__name__} from Qt queue")
            function()

    def _add_qt_timer(self):
        self.qt_window.timer = qtc.QTimer()
        self.qt_window.timer.timeout.connect(self._process_qt_queue)
        self.qt_window.timer.start(1)

    def import_files(self, filepaths_data: list[tuple[str, Path]], config: str, additional_settings: dict) -> None:
        def import_func():
            for filepath in filepaths_data:
                file_suffix = filepath[1].suffix
                if file_suffix == ".fbx":
                    bpy.ops.import_scene.fbx(filepath=str(filepath))
                if file_suffix == ".obj":
                    bpy.ops.import_scene.obj(filepath=str(filepath))

        self.bpy_queue.put(import_func)

    def save_workfile(self, filepath: Path) -> None:
        def save_func():
            bpy.ops.wm.save_as_mainfile(filepath=str(filepath))

        self.bpy_queue.put(save_func)

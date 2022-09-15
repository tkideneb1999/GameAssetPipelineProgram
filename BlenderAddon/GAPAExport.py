from pathlib import Path
import sys
import queue

import bpy

from qtpy import QtWidgets as qtw
from qtpy import QtCore as qtc

from Common.Dialogs.exportWizardView import ExportWizardView
from Common.Core.settings import Settings
from .pipelineSettings import WORKFILE_SUFFIX


class GAPAExport(bpy.types.Operator):
    """Game Asset Pipeline Automation Export"""
    bl_idname = "wm.gapa_export"
    bl_label = "GAPA Export"
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
                if not self.bpy_queue.empty():
                    self._execute_queued()
                    return {"PASS_THROUGH"}
                self.cancel(context)
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
        print("[GAPA] Starting Asset Exporter")

        self.qt_window = ExportWizardView(self.project_path, "blender", WORKFILE_SUFFIX)
        # Register Functions
        self.qt_window.register_save_workfile_func(self.save_workfile)
        self.qt_window.register_export_func(self.export_file)

        self._add_qt_timer()
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

    def start_window(self) -> None:
        pass

    def _process_qt_queue(self):
        while not self.qt_queue.empty():
            function = self.qt_queue.get()
            print(f"[GAPA] Running function {function.func.__name__} from Qt queue")
            function()

    def _add_qt_timer(self):
        self.qt_window.timer = qtc.QTimer()
        self.qt_window.timer.timeout.connect(self._process_qt_queue)
        self.qt_window.timer.start(1)

    def export_file(self, file_paths: dict[str, dict[str, tuple[str, Path]]],
                    config_name: str,
                    export_settings: dict) -> None:
        def export_func():
            for output_set in file_paths:
                for o in file_paths[output_set]:
                    data = file_paths[output_set][o]
                    print(f"[GAPA] Exporting file type: {data[1].suffix}")
                    if data[1].suffix == ".fbx":
                        bpy.ops.export_scene.fbx(filepath=str(data[1]),
                                                 use_selection=export_settings["export_selected"])
                    if data[1].suffix == ".obj":
                        bpy.ops.export_scene.obj(filepath=str(data[1]),
                                                 use_selection=export_settings["export_selected"])

        self.bpy_queue.put(export_func)

    def save_workfile(self, filepath: list[Path]) -> None:
        def save_func():
            bpy.ops.wm.save_as_mainfile(filepath=str(filepath))

        self.bpy_queue.put(save_func)

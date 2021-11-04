from pathlib import Path
import sys
import queue

import bpy

# Append Path to PyQt5
pyQt_path = Path(r"F:\Studium\7 Semester\Bachelor Project\GameAssetPipelineProgram\venv\Lib\site-packages")
sys.path.append(str(pyQt_path))

from PyQt5 import QtWidgets as qtw

from .exportWizardView import ExportWizardView


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
        print("[GAPA] Starting Asset Exporter")
        project_info = context.preferences.addons[__package__].preferences.project_dir
        if project_info == "":
            print("[GAPA] No valid Project Dir set")
            return {'FINISHED'}

        self.qt_window = ExportWizardView(Path(project_info))
        ExportWizardView.qt_queue = self.qt_queue
        ExportWizardView.bpy_queue = self.bpy_queue
        self.qt_window.add_qt_timer()
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

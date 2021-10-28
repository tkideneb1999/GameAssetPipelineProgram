from pathlib import Path
import sys
import queue

import bpy

bl_info = {
    "name": " Game Asset Pipeline Automation",
    "blender": (2, 90, 3),
    "category": "Automation"
}

path = Path(r"F:\Studium\7 Semester\Bachelor Project\GameAssetPipelineProgram\venv\Lib\site-packages")
sys.path.append(str(path))

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class TestWindow(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = qtw.QVBoxLayout(self)
        self.button_layout = qtw.QHBoxLayout(self)
        self.ok_button = qtw.QPushButton("Much Test", self)
        self.ok_button.clicked.connect(self.close_dialog)
        self.button_layout.addWidget(self.ok_button)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)
        self.setWindowTitle("Much Wow")

        self.qt_queue = None

    def close_dialog(self):
        print("Closing Window")
        self.accept()

    def process_qt_queue(self):
        while not self.qt_queue.empty():
            function = self.qt_queue.get()
            print(f"Running function {function.func.__name__} from Qt queue")
            function()

    def add_qt_timer(self):
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.process_qt_queue)
        self.timer.start(1)


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
            print(f"Running Function {function.func.__name__} from Blender Queue")
            function()

    def modal(self, context, event):
        if event.type == "TIMER":
            if self.qt_window and not self.qt_window.isVisible():
                self.cancel(context)
                print("Qt Window not Visible")
                return {"FINISHED"}

            self.qt_app.processEvents()
            self._execute_queued()
            self.qt_counter += 1
        return {"PASS_THROUGH"}

    def execute(self, context):
        print("Starting Modal Operator")

        self.qt_window = TestWindow()
        self.qt_window.qt_queue = self.qt_queue
        self.qt_window.add_qt_timer()
        self.qt_window.show()

        wm = context.window_manager
        self.bpy_timer = wm.event_timer_add(0.001, window=context.window)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self.bpy_timer)


classes = [GAPAExport]


def menu_func(self, context):
    self.layout.operator(GAPAExport.bl_idname)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_file.append(menu_func)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    bpy.types.TOPBAR_MT_file.remove(menu_func)
    print("Goodbye World!")
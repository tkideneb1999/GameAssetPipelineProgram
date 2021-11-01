from pathlib import Path
import sys
import queue
import json

import bpy

# Append Path to PyQt5
pyQt_path = Path(r"F:\Studium\7 Semester\Bachelor Project\GameAssetPipelineProgram\venv\Lib\site-packages")
sys.path.append(str(pyQt_path))

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from .exportWizard_GUI import Ui_export_Wizard
from .Core.asset import Asset


class TestWindow(qtw.QDialog):
    def __init__(self, project_info: Path, parent=None):
        super().__init__(parent)
        self.ui = Ui_export_Wizard()
        self.ui.setupUi(self)

        # TODO(Blender Export): Load asset List
        # TODO(Blender Export): New Asset Wizard
        # TODO(Blender Export): Get Project Path

        self.qt_queue = None
        self.project_name = ""
        self.project_dir = project_info.parent
        self.levels = []
        self.pipelines = {}
        self.assets = []

        self.load_project_info(project_info)
        self.load_asset_list()

        self.ui.level_combobox.addItems(list(self.pipelines.keys()))  # TODO(Blender Addon): Actually filter asset list
        self.ui.asset_list.itemClicked.connect(self.asset_list_item_clicked)

    def close_dialog(self):
        print("Closing Window")
        self.accept()

    def asset_list_item_clicked(self, item: qtw.QListWidgetItem):
        selected_index = self.ui.asset_list.currentIndex().row()
        asset_data_light = self.assets[selected_index]
        asset = self.load_asset_details(asset_data_light[0], asset_data_light[1])
        self.display_asset_info(asset)

    def display_asset_info(self, asset: Asset):
        self.ui.asset_name_label.setText(asset.name)
        self.ui.asset_level_label.setText(asset.level)
        self.ui.asset_pipeline_label.setText("THIS IS A STAND IN")  # TODO(Blender Addon): Read Pipeline Name
        tags_string = ""
        for t in asset.tags:
            tags_string = tags_string + ", " + t
        self.ui.asset_tags_label.setText(tags_string)
        self.ui.asset_comment_label.setText(asset.comment)

    def process_qt_queue(self):
        while not self.qt_queue.empty():
            function = self.qt_queue.get()
            print(f"[GAPA] Running function {function.func.__name__} from Qt queue")
            function()

    def add_qt_timer(self):
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.process_qt_queue)
        self.timer.start(1)

    def load_asset_list(self):
        path = self.project_dir / "assets.meta"
        if not path.exists():
            if not path.is_file():
                raise Exception("Asset List does not exist.")
        with path.open("r", encoding="utf-8") as f:
            asset_list_info = f.readline()
            num_assets = int(asset_list_info.split()[1])
            for i in range(num_assets):
                asset_data_s = f.readline()
                asset_data = asset_data_s.split(',')
                asset_data[1] = asset_data[1].replace("\n", "")
                print(f"[GAPA] Loaded Asset: [0]{asset_data[0]}, [1]{asset_data[1]}")

                self.assets.append(asset_data)
                list_view_item = qtw.QListWidgetItem(asset_data[0])
                self.ui.asset_list.addItem(list_view_item)

    def load_project_info(self, path: Path):
        if not path.exists():
            if not path.is_file():
                if not path.suffix == "gapaproj":
                    raise Exception("Not a valid project info file")
        with path.open("r", encoding="utf-8") as f:
            project_data = json.loads(f.read())
            self.project_name = project_data["name"]

            self.levels.clear()
            for l in project_data["levels"]:
                l.replace("\n", "")
                self.levels.append(l)

            self.pipelines.clear()
            pipeline_data = project_data["pipelines"]
            for name in pipeline_data:
                self.pipelines[name] = Path(pipeline_data[name])

    def load_asset_details(self, name: str, level: str) -> Asset:
        asset = Asset(name, level=level)
        asset.load(self.project_dir)
        return asset

    def save_blend_file(self, asset: Asset):
        # bpy.ops.wm.save_as_mainfile(filepath=)
        # TODO(Blender Export): save blend file in correct folder
        pass


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
            print(f"[GAPA] Running Function {function.func.__name__} from Blender Queue")
            function()

    def modal(self, context, event):
        print("[GAPA] Running Modal")
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

        self.qt_window = TestWindow(Path(project_info))
        self.qt_window.qt_queue = self.qt_queue
        self.qt_window.add_qt_timer()
        self.qt_window.show()

        wm = context.window_manager
        self.bpy_timer = wm.event_timer_add(0.001, window=context.window)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        print("[GAPA] Cancelling")
        wm = context.window_manager
        wm.event_timer_remove(self.bpy_timer)

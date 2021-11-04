from pathlib import Path
import functools
import json
import sys

import bpy

# Append Path to PyQt5
pyQt_path = Path(r"F:\Studium\7 Semester\Bachelor Project\GameAssetPipelineProgram\venv\Lib\site-packages")
sys.path.append(str(pyQt_path))

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from .Core.asset import Asset
from .exportWizard_GUI import Ui_export_Wizard
from .PipelineStepViewer_GUI import Ui_pipeline_step_viewer
from .Core.pipeline import Pipeline


class ExportWizardView(qtw.QDialog):
    def __init__(self, project_info: Path, parent=None):
        super().__init__(parent)
        self.ui = Ui_export_Wizard()
        self.ui.setupUi(self)

        # TODO(Blender Export): New Asset Wizard

        self.project_name = ""
        self.project_dir = project_info.parent
        self.levels = []
        self.pipelines = {}
        self.assets = []
        self.loaded_asset = None

        self.load_project_info(project_info)
        self.load_asset_list()
        # TODO(Blender Addon): Check if work file is already saved for a specific asset

        self.ui.level_combobox.addItems(self.levels)
        # TODO(Blender Addon): Actually filter asset list -> traffic light, name system
        self.ui.asset_list.itemClicked.connect(self.asset_list_item_clicked)
        self.ui.publish_button.clicked.connect(self.publish_asset)

    def close_dialog(self):
        print("Closing Window")
        self.accept()

    def asset_list_item_clicked(self, item: qtw.QListWidgetItem):
        selected_index = self.ui.asset_list.currentIndex().row()
        asset_data_light = self.assets[selected_index]
        self.loaded_asset = self.load_asset_details(asset_data_light[0], asset_data_light[1])
        self.display_asset_info(self.loaded_asset)

    def publish_asset(self):
        if self.loaded_asset is None:
            print("[GAPA] No Asset selected")
            return
        # TODO(Blender Addon): Find correct step
        path = self.project_dir / self.loaded_asset.level / self.loaded_asset.name / f"{self.loaded_asset.name}.blend"
        self.save_blend_file(path)
        # TODO(Blender Addon): save in Blend file for what asset this is
        # TODO(Blender Addon): export selected assets
        # TODO(Blender Addon): Update asset meta file
        self.accept()

    def display_asset_info(self, asset: Asset):
        pipeline = Pipeline()
        pipeline.load(asset.pipeline_dir)
        self.ui.asset_name_label.setText(asset.name)
        self.ui.asset_level_label.setText(asset.level)
        self.ui.asset_pipeline_label.setText(pipeline.name)
        tags_string = ""
        for t in asset.tags:
            tags_string = tags_string + t + ", "
        self.ui.asset_tags_label.setText(tags_string)
        self.ui.asset_comment_label.setText(asset.comment)

        # Display pipeline steps
        for step in pipeline.pipeline_steps:
            step_widget = PipelineStepViewer(step.name, step.program, asset.pipeline_progress[step.uid]["state"])
            step_item = qtw.QListWidgetItem(parent=self.ui.pipeline_list)
            step_item.setSizeHint(step_widget.sizeHint())
            self.ui.pipeline_list.addItem(step_item)
            self.ui.pipeline_list.setItemWidget(step_item, step_widget)

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
            for level in project_data["levels"]:
                level.replace("\n", "")
                self.levels.append(level)

            self.pipelines.clear()
            pipeline_data = project_data["pipelines"]
            for name in pipeline_data:
                self.pipelines[name] = Path(pipeline_data[name])

    def load_asset_details(self, name: str, level: str) -> Asset:
        asset = Asset(name, level=level)
        asset.load(self.project_dir)
        return asset

    def save_blend_file(self, save_dir: Path):
        # bpy.ops.wm.save_as_mainfile(filepath=)
        # Determine Pipeline Step
        print("[GAPA][Qt] Issued Save Command")
        func = functools.partial(bpy.ops.wm.save_as_mainfile, filepath=str(save_dir))
        self.bpy_queue.put(func)

class PipelineStepViewer(qtw.QWidget):
    def __init__(self, step_name: str, step_program:str, step_state: str, parent=None):
        super(PipelineStepViewer, self).__init__(parent)
        self.ui = Ui_pipeline_step_viewer()
        self.ui.setupUi(self)
        self.ui.step_name_label.setText(step_name)
        self.ui.step_program_label.setText(step_program)
        self.ui.step_state.setText(step_state)
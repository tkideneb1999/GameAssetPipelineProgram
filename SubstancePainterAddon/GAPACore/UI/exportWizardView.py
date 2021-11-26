from pathlib import Path
import functools
import json
from collections.abc import Callable
import importlib

from PySide2 import QtWidgets as qtw
from PySide2 import QtCore as qtc

from .. import asset
from . import exportWizard_GUI

importlib.reload(asset)
importlib.reload(exportWizard_GUI)


class ExportWizardView(qtw.QDialog):
    def __init__(self, project_info, program, parent=None):
        # project_info: Path, program: str
        super().__init__(parent)
        self.ui = exportWizard_GUI.Ui_export_Wizard()
        self.ui.setupUi(self)
        self.ui.pipeline_viewer.set_current_program(program)

        # TODO(Blender Export): New Asset Wizard

        # Data
        self.project_name = ""
        self.project_dir = project_info.parent  # Path
        self.levels = []  # list[str]
        self.pipelines = {}  # dict[str, Path]
        self.assets = {}  # dict[str, list[str]]
        self.loaded_asset = None  # asset.Asset
        self.program = program  # str

        # Functions to register
        self.export_file_func = None  # Callable[Path, str, dict]
        self.save_workfile_func = None  # Callable[Path]
        self.get_output_sets_func = None  # Callable[]

        self.load_project_info(project_info)
        self.load_asset_list()
        # TODO(Blender Addon): Check if work file is already saved for a specific asset

        # TODO(Blender Addon): Actually filter asset list -> traffic light, name system
        self.ui.asset_list.s_asset_changed.connect(self.display_selected_asset)
        self.ui.publish_button.clicked.connect(self.publish_asset)

        self.ui.pipeline_viewer.s_step_selected.connect(self.display_step_outputs)

    def close_dialog(self):
        print("Closing Window")
        self.accept()

    def register_save_workfile_func(self, func) -> None:
        # func: Callable[Path]
        self.save_workfile_func = func

    def register_export_func(self, func) -> None:
        # func: Callable[Path, str, dict]
        self.export_file_func = func

    def publish_asset(self):
        if self.loaded_asset is None:
            print("[GAPA] No Asset selected")
            return
        selected_step_index = self.ui.pipeline_viewer.get_selected_index()
        if selected_step_index == -1:
            print("[GAPA] No step selected or nothing to export in this step")
            return
        export_all = self.loaded_asset.pipeline.pipeline_steps[selected_step_index].export_all
        if not export_all:
            if self.ui.outputs_list.currentRow() == -1:
                print("[GAPA] No output selected")
                return

        # Check if functions are registered
        if self.export_file_func is None:
            raise Exception("[GAPA] 'export' Function not registered")
        if self.save_workfile_func is None:
            raise Exception("[GAPA] 'save_workfile' function not registered")

        # Get selected step uid and output uid
        selected_step = self.loaded_asset.pipeline.pipeline_steps[selected_step_index]
        selected_step_uid = selected_step.uid
        print(f"[GAPA] selected index: {selected_step_index}; uid: {selected_step_uid}")

        multi_asset_workfile = False  # TODO(Blender Addon): Multi Asset Workfiles
        if multi_asset_workfile is False:
            path = self.project_dir / self.loaded_asset.level / self.loaded_asset.name / selected_step.get_folder_name() / f"{self.loaded_asset.name}.spp"
            self.save_workfile(path)
        if export_all:
            output_uids = []
            for o in selected_step.outputs:
                output_uids.append(o.uid)
        else:
            selected_output_index = self.ui.outputs_list.currentRow()
            output_uids = [selected_step.outputs[selected_output_index].uid]

        # TODO(Blender Addon):Select output format
        output_format = "tga"

        output_sets = None
        if self.loaded_asset.pipeline.pipeline_steps[selected_step_index].has_set_outputs:
            if self.get_output_sets_func is None:
                raise Exception("[GAPA] get_output_sets function not registered!")
            output_sets = self.get_output_sets_func()

        # Determine Absolute export path
        publish_data = self.loaded_asset.publish_step_file(selected_step_uid,
                                                           output_uids,
                                                           output_format,
                                                           output_sets=output_sets)
        rel_paths = publish_data[0]
        abs_paths = {}
        for output_set in rel_paths:
            for o in rel_paths[output_set]:
                abs_paths[output_set][o] = self.project_dir / rel_paths[output_set][o]

        # update asset pipeline progress data & save changes
        self.loaded_asset.save(self.project_dir)

        # get Config name
        config_name = self.loaded_asset.pipeline[selected_step_index].config
        export_settings = {"output_format": output_format}

        # send to blender Queue for export
        self.export_file(abs_paths, config_name, export_settings)

        self.accept()

    def display_selected_asset(self, level, index) -> None:
        # level: str, index: int
        asset_name = self.assets[level][index]
        self.loaded_asset = asset.Asset(asset_name, level, project_dir=self.project_dir)

        self.ui.asset_details.update_asset_details(self.loaded_asset.name,
                                                   self.loaded_asset.level,
                                                   self.loaded_asset.pipeline.name,
                                                   self.loaded_asset.tags,
                                                   self.loaded_asset.comment)
        self.ui.pipeline_viewer.update_view(self.loaded_asset)

    def display_step_outputs(self, index):
        # Show Outputs
        outputs = self.loaded_asset.pipeline.pipeline_steps[index].outputs
        outputs_names = []
        for o in outputs:
            outputs_names.append(o.name)
        self.ui.outputs_list.clear()
        self.ui.outputs_list.addItems(outputs_names)
        if self.loaded_asset.pipeline.pipeline_steps[index].export_all:
            self.ui.outputs_list.setSelectionMode(qtw.QAbstractItemView.NoSelection)
        else:
            self.ui.outputs_list.setSelectionMode(qtw.QAbstractItemView.SingleSelection)

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
                asset_data[1] = asset_data[1].replace('\n', '')
                if self.assets.get(asset_data[1]) is None:
                    self.assets[asset_data[1]] = [asset_data[0]]
                else:
                    self.assets[asset_data[1]].append(asset_data[0])
        self.ui.asset_list.update_asset_list(self.assets)

    def load_project_info(self, path):
        # path: Path
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

    def save_workfile(self, save_dir):
        # save_dir: Path
        func = functools.partial(self.save_workfile_func, filepath=str(save_dir))
        func()

    def export_file(self, paths, config_name, export_settings) -> None:
        # path: Path, file_format: str, use_selection: bool
        func = functools.partial(self.export_file_func,
                                 file_paths=paths,
                                 config_name=config_name,
                                 export_settings=export_settings)
        func()

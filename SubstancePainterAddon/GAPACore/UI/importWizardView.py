from pathlib import Path
import functools
import json
from collections.abc import Callable
import importlib

from PySide2 import QtWidgets as qtw
from PySide2 import QtCore as qtc

from .. import asset as assetModule
from . import importWizard_GUI

importlib.reload(assetModule)
importlib.reload(importWizard_GUI)


class ImportWizardView(qtw.QDialog):
    def __init__(self, project_info, program, parent=None):  # project_info: Path, program: str
        super().__init__(parent)
        self.ui = importWizard_GUI.Ui_import_Wizard()
        self.ui.setupUi(self)
        self.ui.pipeline_viewer.set_current_program(program)

        # TODO(Blender Export): New Asset Wizard

        # Data
        self.project_name = ""
        self.project_dir = project_info.parent
        self.levels = []  # list[str]
        self.pipelines = {}  # dict[str, Path]
        self.assets = {}  # dict[str, list[str]]
        self.loaded_asset = None  # assetModule.Asset
        self.program = program

        # Functions to register
        self.import_files_func = None  # Callable[list[tuple[str, Path]]]
        self.save_workfile_func = None  # Callable[Path]

        self.load_project_info(project_info)
        self.load_asset_list()
        # TODO(Blender Addon): Check if work file is already saved for a specific asset
        # TODO(Blender Addon): Actually filter asset list -> traffic light, name system

        self.ui.asset_list.s_asset_changed.connect(self.display_selected_asset)
        self.ui.pipeline_viewer.s_step_selected.connect(self.display_step_inputs)

        self.ui.import_button.clicked.connect(self.import_assets)

    def close_dialog(self):
        print("Closing Window")
        self.accept()

    def register_save_workfile_func(self, func) -> None:  # func: Callable[Path]
        """
        Registers the function that will save the workfile, to be executed when needed.
        :param func: Function object that has a path as an input that contains the path for the work file to be saved to
        """
        self.save_workfile_func = func

    def register_import_files_func(self, func) -> None:  # func: Callable[list[tuple[str, Path]]]
        """
        Registers the function that will import files from steps that have outputs connected to the inputs of the selected step.
        :param func: Function object that takes a list of paths. The paths contain the location of the exported files of the outputs
        """
        self.import_files_func = func

    def import_assets(self):
        # TODO(Blender Addon): Implement Button
        if self.loaded_asset is None:
            print("[GAPA] No Asset Selected")
            return
        if self.ui.pipeline_viewer.get_selected_index() == -1:
            print("[GAPA] No step to work on selected")
            return

        # Get selected step
        step_index = self.ui.pipeline_viewer.get_selected_index()
        import_data = self.loaded_asset.import_assets(step_index)  # TODO(Blender Addon): Handle different file types
        rel_filepaths = import_data[0]
        abs_filepaths = []
        for f in rel_filepaths:
            abs_filepaths.append((f[0], self.project_dir / f[1]))

        # TODO: Get Additional Pipeline Settings

        # import assets
        func = functools.partial(self.import_files_func,
                                 filepaths=abs_filepaths,
                                 config=import_data[1],
                                 additional_settings=import_data[2])
        func()

        # save workfile
        multi_asset_workfile = False  # TODO(Blender Addon): Multi Asset Workfiles
        if multi_asset_workfile is False:
            selected_step = self.loaded_asset.pipeline.pipeline_steps[step_index]
            rel_wf_path = Path() / self.loaded_asset.level / self.loaded_asset.name / selected_step.get_folder_name() / "workfiles" / f"{self.loaded_asset.name}.spp"  # TODO: Move file ending generation to program specific code
            abs_wf_path = self.project_dir / rel_wf_path
            self.loaded_asset.save_work_file(selected_step.uid, str(rel_wf_path))
            self.save_workfile(abs_wf_path)

        self.accept()

    def display_selected_asset(self, level, index) -> None:  # level: str, index: int
        asset_name = self.assets[level][index]
        self.loaded_asset = assetModule.Asset(asset_name, level, project_dir=self.project_dir)

        self.ui.asset_details.update_asset_details(self.loaded_asset.name,
                                                   self.loaded_asset.level,
                                                   self.loaded_asset.pipeline.name,
                                                   self.loaded_asset.tags,
                                                   self.loaded_asset.comment)
        self.ui.pipeline_viewer.update_view(self.loaded_asset)

    def display_step_inputs(self):
        # Show Inputs
        index = self.ui.pipeline_viewer.get_selected_index()
        inputs = self.loaded_asset.pipeline.pipeline_steps[index].inputs
        inputs_names = []
        for i in inputs:
            output_uid = self.loaded_asset.pipeline.io_connections[i.uid]
            output_name = self.loaded_asset.pipeline.get_output_name(output_uid)
            inputs_names.append(output_name)
        self.ui.inputs_list.clear()
        self.ui.inputs_list.addItems(inputs_names)

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

    def load_project_info(self, path):  # path: Path
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

    def load_asset_details(self, name, level) -> assetModule.Asset:  # name: str, level: str
        asset = assetModule.Asset(name, level, self.project_dir)
        return asset

    def save_workfile(self, save_dir):  # save_dir: Path
        # TODO(Blender Addon): Determine actual location (make dependent on user whether multi asset file or not)
        print("[GAPA][Qt] Issued Save Command")
        func = functools.partial(self.save_workfile_func, filepath=str(save_dir))
        func()

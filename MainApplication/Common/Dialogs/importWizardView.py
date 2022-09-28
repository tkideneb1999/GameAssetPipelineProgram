from pathlib import Path
import functools
import json
import sys
import os
import importlib

from qtpy import QtWidgets as qtw
from qtpy import QtCore as qtc

from ..Core import asset as assetModule
from . import importWizard_GUI
from .. import pluginHandler
from ..Core.assetDatabase import AssetDatabase
from ..Core.tagDatabase import TagDatabase

importlib.reload(assetModule)
importlib.reload(importWizard_GUI)
importlib.reload(pluginHandler)


class ImportWizardView(qtw.QDialog):
    def __init__(self, project_info, program, workfile_suffix, parent=None):  # project_info: Path, program: str
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

        self.asset_database = AssetDatabase()
        self.tag_database = TagDatabase()

        self.loaded_asset = None  # assetModule.Asset
        self.program = program
        self.workfile_suffix = workfile_suffix

        # Functions to register
        self.import_files_func = None  # Callable[list[tuple[str, Path]]]
        self.save_workfile_func = None  # Callable[Path]

        self.load_project_info(project_info)
        self.post_init(self.project_dir)
        self.load_asset_list()
        # TODO(Blender Addon): Check if work file is already saved for a specific asset
        # TODO(Blender Addon): Actually filter asset list -> traffic light, name system

        self.ui.asset_list.s_asset_changed.connect(self.display_selected_asset)
        self.ui.pipeline_viewer.s_step_selected.connect(self.display_step_inputs)
        self.ui.pipeline_viewer.s_open_file_explorer.connect(self.open_step_in_explorer)
        self.ui.pipeline_viewer.s_run_plugin.connect(self.run_plugin)
        self.ui.asset_list.s_open_file_explorer.connect(self.open_asset_in_explorer)
        self.ui.asset_list.s_tag_searchbar_selected.connect(self.tag_searchbar_selected)
        self.ui.asset_list.s_tag_selection_changed.connect(self.update_asset_list)

        self.ui.import_button.clicked.connect(self.import_assets)

        # Plugins
        self.plugin_handler = pluginHandler.PluginHandler(self.project_dir, self)

    def post_init(self, project_dir: Path):
        self.asset_database.set_project_dir(project_dir)
        if not self.tag_database.is_loaded():
            self.tag_database.load(project_dir)
        if self.tag_database.is_loaded():
            self.ui.asset_list.update_tags(self.tag_database.tag_names)

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
        import_data = self.loaded_asset.import_assets(step_index)
        rel_filepaths = import_data[0]
        abs_filepaths = []

        for output_set in rel_filepaths:
            if output_set == "workfiles":
                abs_filepaths.append(("workfiles", self.project_dir / rel_filepaths["workfiles"]))
                continue
            for output in rel_filepaths[output_set]:
                abs_filepaths.append((rel_filepaths[output_set][output][0],
                                      self.project_dir / rel_filepaths[output_set][output][1]))

        # import assets
        func = functools.partial(self.import_files_func,
                                 filepaths_data=abs_filepaths,
                                 config=import_data[1],
                                 additional_settings=import_data[2])
        func()

        # save workfile
        multi_asset_workfile = False  # TODO(Blender Addon): Multi Asset Workfiles
        if multi_asset_workfile is False:
            selected_step = self.loaded_asset.pipeline.pipeline_steps[step_index]
            rel_wf_path = Path() / self.loaded_asset.level / self.loaded_asset.name / selected_step.get_folder_name() / "workfiles" / f"{self.loaded_asset.name}.{self.workfile_suffix}"  # TODO: Move file ending generation to program specific code
            abs_wf_path = self.project_dir / rel_wf_path
            if abs_wf_path.exists():
                print("[GAPA] A Workfile already exists for this Asset at this step, saving as a new one")
                file_dir = abs_wf_path.parent
                version = 0
                while abs_wf_path.exists():
                    version += 1
                    abs_wf_path = file_dir / f"{self.loaded_asset.name}.{version}.spp"
                print(f"[GAPA] Saving workfile as: {abs_wf_path.name}")
            self.loaded_asset.save_work_file(selected_step.uid, str(rel_wf_path))
            self.save_workfile(abs_wf_path)

        self.accept()

    def display_selected_asset(self, asset_id: int) -> None:
        asset_info = self.asset_database.get_asset_by_id(asset_id)
        self.loaded_asset = assetModule.Asset(asset_info[0], asset_info[1], project_dir=self.project_dir)

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
            output_uid = self.loaded_asset.pipeline.io_connections.get(i.uid)
            if output_uid is None:
                continue
            inputs_names.append(i.name)
        self.ui.inputs_list.clear()
        self.ui.inputs_list.addItems(inputs_names)

    def load_asset_list(self):
        self.asset_database.load_asset_list()
        self.update_asset_list()

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

    def save_workfile(self, save_dir):  # save_dir: Path
        # TODO(Blender Addon): Determine actual location (make dependent on user whether multi asset file or not)
        print("[GAPA][Qt] Issued Save Command")
        func = functools.partial(self.save_workfile_func, filepath=str(save_dir))
        func()

    def open_asset_in_explorer(self, level: str, asset: str) -> None:
        if sys.platform == "win32":
            os.startfile(str(self.project_dir / level / asset))
        else:
            print("[GAPA] Opening file explorer only possible on Windows")

    def open_step_in_explorer(self, step_index: int) -> None:
        if sys.platform == "win32":
            step_folder_name = self.loaded_asset.pipeline.pipeline_steps[step_index].get_folder_name()
            os.startfile(str(self.project_dir / self.loaded_asset.level / self.loaded_asset.name / step_folder_name))
        else:
            print("[GAPA] Opening file explorer only possible on Windows")

    def run_plugin(self, step_index: int) -> None:
        self.plugin_handler.run_plugin(self.loaded_asset, step_index)
        self.loaded_asset.load(self.project_dir)
        self.ui.pipeline_viewer.update_view(self.loaded_asset)

    def tag_searchbar_selected(self):
        self.ui.asset_list.update_tags(self.tag_database.tag_names)

    def update_asset_list(self, tags=None):
        if tags is None or tags == []:
            self.ui.asset_list.update_asset_list(self.asset_database.get_all_assets())
        else:
            tag_IDs = self.tag_database.get_tag_IDs(tags)
            self.ui.asset_list.update_asset_list(self.asset_database.get_assets_by_tag(tag_IDs))

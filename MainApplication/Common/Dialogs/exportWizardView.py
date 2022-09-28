from pathlib import Path
import functools
import json
import sys
import os
import importlib

from qtpy import QtWidgets as qtw

from ..Core import asset as assetModule
from ..Core.assetDatabase import AssetDatabase
from ..Core.tagDatabase import TagDatabase
from . import exportWizard_GUI
from .. import pluginHandler


importlib.reload(assetModule)
importlib.reload(exportWizard_GUI)
importlib.reload(pluginHandler)


class ExportWizardView(qtw.QDialog):
    def __init__(self, project_info, program, workfile_suffix, parent=None):
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
        self.asset_database = AssetDatabase()
        self.tag_database = TagDatabase()
        self.loaded_asset = None  # asset.Asset
        self.program = program  # str
        self.workfile_suffix = workfile_suffix  # str

        # Functions to register
        self.export_file_func = None  # Callable[Path, str, dict]
        self.save_workfile_func = None  # Callable[Path]
        self.get_output_sets_func = None  # Callable[]

        self.load_project_info(project_info)
        self.post_init(self.project_dir)
        self.load_asset_list()
        # TODO(Blender Addon): Check if work file is already saved for a specific asset

        # TODO(Blender Addon): Actually filter asset list -> traffic light, name system
        self.ui.asset_list.s_asset_changed.connect(self.display_selected_asset)
        self.ui.publish_button.clicked.connect(self.publish_asset)

        self.ui.pipeline_viewer.s_step_selected.connect(self.display_step_outputs)
        self.ui.pipeline_viewer.s_run_plugin.connect(self.run_plugin)
        self.ui.pipeline_viewer.s_open_file_explorer.connect(self.open_step_in_explorer)
        self.ui.asset_list.s_open_file_explorer.connect(self.open_asset_in_explorer)
        self.ui.asset_list.s_tag_searchbar_selected.connect(self.tag_searchbar_selected)
        self.ui.asset_list.s_tag_selection_changed.connect(self.update_asset_list)

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

    def register_save_workfile_func(self, func) -> None:
        """
        Registers the function that will save the workfile, to be executed when needed.
        :param func: Function object that has a path as an input that contains the path for the work file to be saved to
        """
        # func: Callable[Path]
        self.save_workfile_func = func

    def register_export_func(self, func) -> None:
        """
        Registers the function that will import files from steps that have outputs connected to the inputs of the selected step.
        :param func: Function object that takes a list of paths. The paths contain the location of the exported files of the outputs
        """
        # func: Callable[Path, str, dict]
        self.export_file_func = func

    def register_get_output_sets_func(self, func) -> None:
        self.get_output_sets_func = func

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

        multi_asset_workfile = False  # TODO(Blender Addon): Multi Asset Workfiles
        if multi_asset_workfile is False:
            path = self.project_dir / self.loaded_asset.level / self.loaded_asset.name / selected_step.get_folder_name() / f"{self.loaded_asset.name}.{self.workfile_suffix}"
            self.save_workfile(path)  # TODO

        if not export_all:
            selected_output_index = self.ui.outputs_list.currentRow()
            output_uids = [selected_step.outputs[selected_output_index].uid]
            output_data_types = [selected_step.outputs[selected_output_index].data_type]
        else:
            output_uids = []
            output_data_types = []
            for output in selected_step.outputs:
                output_uids.append(output.uid)
                output_data_types.append(output.data_type)

        output_sets = None
        if self.loaded_asset.pipeline.pipeline_steps[selected_step_index].has_set_outputs:
            if self.get_output_sets_func is None:
                raise Exception("[GAPA] get_output_sets function not registered!")
            output_sets = self.get_output_sets_func()
        print(f"[GAPA] Output sets: {output_sets}")

        # Determine Absolute export path
        publish_data = self.loaded_asset.publish_step_file(selected_step_uid,
                                                           output_uids,
                                                           output_data_types,
                                                           output_sets=output_sets)
        abs_paths = publish_data
        for output_set in publish_data:
            for o in publish_data[output_set]:
                abs_paths[output_set][o] = (publish_data[output_set][o][0], self.project_dir / publish_data[output_set][o][1])

        # update asset pipeline progress data & save changes
        self.loaded_asset.save(self.project_dir)

        # TODO: Asset Level Settings
        export_settings = {"export_selected": self.ui.export_selected_checkbox.isChecked(),
                           "output_format": output_data_types}
        # get Config name
        config_name = self.loaded_asset.pipeline.pipeline_steps[selected_step_index].config

        # send to blender Queue for export
        self.export_file(abs_paths, config_name, export_settings)

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

    def load_asset_list(self):
        self.asset_database.load_asset_list()
        self.update_asset_list()

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

from pathlib import Path
import os
import sys
import re

from qtpy import QtWidgets as qtw
from qtpy import QtCore as qtc

from .assetManager_GUI import Ui_asset_manager
from .Common.Core.asset import Asset
from .newAssetWizard import NewAssetWizard
from .Common import pluginHandler
from .Common.Core.tagDatabase import TagDatabase
from .Common.Core.assetDatabase import AssetDatabase


class AssetManager(qtw.QWidget):
    s_level_added = qtc.Signal(str)  # Level Name
    s_level_removed = qtc.Signal(str)  # Level Name

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_asset_manager()
        self.ui.setupUi(self)
        self.ui.asset_list.mode = 1

        # Asset List
        self.ui.add_asset_button.clicked.connect(self.add_new_asset_with_button)
        self.ui.asset_list.s_asset_changed.connect(self.display_selected_asset)
        self.ui.asset_list.s_open_file_explorer.connect(self.open_asset_in_explorer)
        self.ui.asset_list.s_add_asset.connect(self.add_new_asset)
        self.ui.asset_list.s_remove_asset.connect(self.remove_asset)
        self.ui.asset_list.s_add_level.connect(self.add_new_level)
        self.ui.asset_list.s_remove_level.connect(self.remove_level)
        self.ui.asset_list.s_tag_searchbar_selected.connect(self.tag_searchbar_selected)
        self.ui.asset_list.s_tag_selection_changed.connect(self.update_asset_list)

        self.ui.pipeline_viewer.s_open_file_explorer.connect(self.open_step_in_explorer)
        self.ui.pipeline_viewer.s_run_plugin.connect(self.run_plugin)

        # Data
        self.asset_database = AssetDatabase()
        self.tag_database = TagDatabase()
        self.loaded_asset: Asset = None
        self.project_dir: Path = Path()
        self.pipelines: dict[str, Path] = {}
        self.special_characters = re.compile(r'[@!#$%^&*()<>?/\|}{~:]')

        # Plugins
        self.plugin_handler = pluginHandler.PluginHandler(parent=self)

    def add_new_asset(self, lvl_selected=False, lvl_name=""):
        print(f"Level Selected: {lvl_selected}, Level Name: {lvl_name}")

        pipeline_names = list(self.pipelines.keys())

        dialog = NewAssetWizard(self.asset_database.levels, pipeline_names, self.tag_database.tag_names)
        dialog.setWindowModality(qtc.Qt.ApplicationModal)
        if lvl_selected:
            dialog.set_starting_level(lvl_name)

        result = dialog.exec_()
        if result == 0:
            return

        # Get new asset data
        asset_name = dialog.get_name_data()
        asset_pipeline_name = dialog.get_pipeline_data()
        asset_level = dialog.get_level_data()
        asset_tags = dialog.get_tags_data()
        asset_comment = dialog.get_comment_data()

        if asset_name == "":
            print("[New Asset Wizard] Choose a name!")
            self.add_new_asset()
            return

        if asset_pipeline_name == "":
            print("[New Asset Wizard] Choose a pipeline or create a new one!")
            self.add_new_asset()
            return

        asset_pipeline_dir = self.project_dir / self.pipelines[asset_pipeline_name]

        # Check Data
        # Check if Asset Name already exists in Level
        tagIDs = []
        for tn in asset_tags:
            tagIDs.append(self.tag_database.get_tag_ID(tn))
        result = self.asset_database.add_new_asset(asset_name, asset_level, tagIDs)
        if result < 0:
            self.add_new_asset()
            return

        # Create Asset
        new_asset = Asset(
            asset_name,
            pipeline_dir=asset_pipeline_dir,
            project_dir=self.project_dir,
            level=asset_level,
            tags=asset_tags,
            asset_type="Model",
            comment=asset_comment)

        self.update_asset_list()

        # Serialize Asset
        new_asset.save(self.project_dir)
        self.save_asset_list()

    def add_new_asset_with_button(self) -> None:
        current_item = self.ui.asset_list.get_current_item()
        if current_item is not None:
            self.add_new_asset(True, current_item)
        else:
            self.add_new_asset()

    def remove_asset(self, asset_id: int) -> None:
        result = self.asset_database.remove_asset(asset_id)
        self.save_asset_list()
        path = self.project_dir / result[1] / result[0]
        path.rename(path.parent / f"deprecated_{result[0]}")
        self.update_asset_list()

    def add_new_level(self) -> None:
        text, ok = qtw.QInputDialog().getText(self, "Add Level", "Level Name:", qtw.QLineEdit.Normal, "")
        if not ok:
            return

        text_no_spaces = text.replace(' ', '')
        if self.special_characters.search(text_no_spaces):
            self.add_new_level()
        if not self.asset_database.add_level(text_no_spaces):
            self.add_new_level()

        self.s_level_added.emit(text_no_spaces)
        self.update_asset_list()

    def remove_level(self, level_name: str):
        self.asset_database.remove_level(level_name)
        self.s_level_removed.emit(level_name)
        self.save_asset_list()
        self.update_asset_list()

    def display_selected_asset(self, asset_id: int) -> None:
        asset_info = self.asset_database.get_asset_by_id(asset_id)
        self.loaded_asset = Asset(asset_info[0], asset_info[1], project_dir=self.project_dir)

        self.ui.asset_details.update_asset_details(self.loaded_asset.name,
                                                   self.loaded_asset.level,
                                                   self.loaded_asset.pipeline.name,
                                                   self.loaded_asset.tags,
                                                   self.loaded_asset.comment)
        self.ui.pipeline_viewer.update_view(self.loaded_asset)

    def tag_searchbar_selected(self):
        self.ui.asset_list.update_tags(self.tag_database.tag_names)

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
        self.loaded_asset.load(self.project_dir)
        self.plugin_handler.run_plugin(self.loaded_asset, step_index)
        self.loaded_asset.load(self.project_dir)
        self.ui.pipeline_viewer.update_view(self.loaded_asset)

    def add_levels(self, levels):
        for lvl in levels:
            self.asset_database.add_level(lvl)
        print("Viable Levels: ", self.asset_database.levels)
        self.update_asset_list()

    def update_pipelines(self, pipelines):
        self.pipelines = pipelines
        print(self.pipelines)

    def set_project_dir(self, project_dir):
        self.project_dir = project_dir
        self.plugin_handler.set_project_dir(project_dir)
        self.asset_database.set_project_dir(project_dir)
        if not self.tag_database.is_loaded():
            self.tag_database.load(project_dir)
        if self.tag_database.is_loaded():
            self.ui.asset_list.update_tags(self.tag_database.tag_names)

    def update_asset_list(self, tags=None):
        if tags is None or tags == []:
            self.ui.asset_list.update_asset_list(self.asset_database.get_all_assets())
        else:
            tag_IDs = self.tag_database.get_tag_IDs(tags)
            self.ui.asset_list.update_asset_list(self.asset_database.get_assets_by_tag(tag_IDs))

    # -------------
    # SERIALIZATION
    # -------------
    def save_asset_list(self) -> None:
        self.asset_database.save_asset_list()

    def load_asset_list(self) -> None:
        self.asset_database.load_asset_list()
        self.update_asset_list()


from pathlib import Path
import os
import sys
import re

from .Common.qtpy import QtWidgets as qtw
from .Common.qtpy import QtCore as qtc

from .assetManager_GUI import Ui_asset_manager
from .Common.Core.asset import Asset
from .newAssetWizard import NewAssetWizard
from . import pluginHandler


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

        self.ui.pipeline_viewer.s_open_file_explorer.connect(self.open_step_in_explorer)
        self.ui.pipeline_viewer.s_run_plugin.connect(self.run_plugin)

        # Data
        self.assets: dict[str, list[str]] = {}
        self.loaded_asset: Asset = None
        self.project_dir: Path = Path()
        self.pipelines: dict[str, Path] = {}
        self.special_characters = re.compile(r'[@!#$%^&*()<>?/\|}{~:]')

        # Plugins
        self.plugin_handler = pluginHandler.PluginHandler(parent=self)

    def add_new_asset(self, lvl_selected=False, lvl_name=""):
        print(f"Level Selected: {lvl_selected}, Level Name: {lvl_name}")

        pipeline_names = list(self.pipelines.keys())
        dialog = NewAssetWizard(list(self.assets.keys()), pipeline_names)
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
        for a in self.assets:
            if a[0] == asset_name and a[1] == asset_level:
                print(f"Asset{asset_name} already exists in Level {asset_level}.")
                # TODO: Assets: Optimize Asset search
                self.add_new_asset()
                return

        # Check if selected level is viable
        if asset_level not in list(self.assets.keys()):
            print(f"{asset_level} is not a valid Level.")
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

        self.assets[asset_level].append(asset_name)
        self.ui.asset_list.update_asset_list(self.assets)

        # Serialize Asset
        new_asset.save(self.project_dir)
        self.save_asset_list()

    def add_new_asset_with_button(self) -> None:
        current_item = self.ui.asset_list.get_current_item()
        if current_item is not None:
            self.add_new_asset(True, current_item)
        else:
            self.add_new_asset()

    def remove_asset(self, level: str, name: str) -> None:
        print(f"[GAPA] Removing Asset {name} from Level {level}")
        self.assets[level].remove(name)
        self.save_asset_list()
        path = self.project_dir / level / name
        path.rename(path.parent / f"deprecated_{name}")
        self.ui.asset_list.update_asset_list(self.assets)

    def add_new_level(self) -> None:
        print("[GAPA] Adding Levels not yet implemented")
        text, ok = qtw.QInputDialog().getText(self, "Add Level", "Level Name:", qtw.QLineEdit.Normal, "")
        if not ok:
            return
        text_no_spaces = text.replace(' ', '')
        if text_no_spaces in list(self.assets.keys()):
            print("[GAPA] Level name already exists")
            self.add_new_level()
        if self.special_characters.search(text_no_spaces):
            self.add_new_level()
        self.assets[text_no_spaces] = []
        self.s_level_added.emit(text_no_spaces)
        self.ui.asset_list.update_asset_list(self.assets)

    def remove_level(self, level_name: str):
        print(f"[GAPA] Removing Level: {level_name}")
        del self.assets[level_name]
        self.s_level_removed.emit(level_name)
        self.save_asset_list()
        self.ui.asset_list.update_asset_list(self.assets)

    def display_selected_asset(self, level_name: str, asset_name: str) -> None:
        self.loaded_asset = Asset(asset_name, level_name, project_dir=self.project_dir)

        self.ui.asset_details.update_asset_details(self.loaded_asset.name,
                                                   self.loaded_asset.level,
                                                   self.loaded_asset.pipeline.name,
                                                   self.loaded_asset.tags,
                                                   self.loaded_asset.comment)
        self.ui.pipeline_viewer.update_view(self.loaded_asset)

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
            self.assets[lvl] = []
        print("Viable Levels: ", list(self.assets.keys()))

    def update_pipelines(self, pipelines):
        self.pipelines = pipelines
        print(self.pipelines)

    def set_project_dir(self, project_dir):
        self.project_dir = project_dir
        self.plugin_handler.set_project_dir(project_dir)

    def update_asset_list(self):
        self.ui.asset_list.update_asset_list(self.assets)

    # -------------
    # SERIALIZATION
    # -------------
    def save_asset_list(self) -> None:
        path = self.project_dir / "assets.meta"
        if not path.exists():
            if not path.is_file():
                path.touch()
        with path.open("w", encoding="utf-8") as f:
            num_assets = 0
            for level in self.assets:
                num_assets += len(self.assets[level])
            f.write(f"assets {num_assets}\n")
            for level in self.assets:
                for asset in self.assets[level]:
                    data = f"{asset},{level}\n"
                    f.write(data)
            f.close()

    def load_asset_list(self) -> None:
        path = self.project_dir / "assets.meta"
        if not path.exists():
            raise Exception("Asset List does not exist.")
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


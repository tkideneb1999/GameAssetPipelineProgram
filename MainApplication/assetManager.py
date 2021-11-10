from pathlib import Path

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from assetManager_GUI import Ui_asset_manager
from asset import Asset
from newAssetWizard import NewAssetWizard


class AssetManager(qtw.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_asset_manager()
        self.ui.setupUi(self)

        # Asset List
        self.ui.add_asset_button.clicked.connect(self.add_new_asset)
        self.ui.remove_asset_button.clicked.connect(self.remove_asset)
        self.ui.asset_list.s_asset_changed.connect(self.display_selected_asset)

        # Data
        self.assets: dict[str, list[str]] = {}
        self.loaded_asset: Asset = None
        self.levels: list[str] = []
        self.project_dir: Path = Path()
        self.pipelines: dict[str, Path] = {}

    def add_new_asset(self) -> None:
        pipeline_names = list(self.pipelines.keys())
        dialog = NewAssetWizard(self.levels, pipeline_names)
        dialog.setWindowModality(qtc.Qt.ApplicationModal)
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
        if asset_level not in self.levels:
            print(f"{asset_level} is not a valid Level.")
            self.add_new_asset()
            return

        # Create Asset
        new_asset = Asset(
            asset_name,
            pipeline_dir=asset_pipeline_dir,
            level=asset_level,
            tags=asset_tags,
            asset_type="Model",
            comment=asset_comment)

        self.assets[asset_level] = asset_name
        self.ui.asset_list.update_asset_list(self.assets)

        # Serialize Asset
        new_asset.save(self.project_dir)
        self.save_asset_list()

    def remove_asset(self) -> None:
        selected_assets = self.ui.asset_list.selectedIndexes()
        if not selected_assets:
            return
        else:
            for i in selected_assets:
                print("[Asset Manager] Remove not yet implemented")
                # self.ui.asset_list.takeItem(i.row())
                # self.assets.remove(self.assets[i.row()])

        # TODO(Asset Manager): Remove Folder and files

    def display_selected_asset(self, level: str, index: int) -> None:
        asset_name = self.assets[level][index]
        self.loaded_asset = Asset(asset_name, level, project_dir=self.project_dir)

        self.ui.asset_details.update_asset_details(self.loaded_asset.name,
                                                   self.loaded_asset.level,
                                                   self.loaded_asset.pipeline.name,
                                                   self.loaded_asset.tags,
                                                   self.loaded_asset.comment)
        self.ui.pipeline_viewer.update_view(self.loaded_asset)

    def add_levels(self, levels):
        for lvl in levels:
            self.levels.append(lvl)
        print("Viable Levels: ", self.levels)

    def update_pipelines(self, pipelines):
        self.pipelines = pipelines
        print(self.pipelines)

    def set_project_dir(self, project_dir):
        self.project_dir = project_dir

    # -------------
    # SERIALIZATION
    # -------------
    def save_asset_list(self) -> None:
        path = self.project_dir / "assets.meta"
        if not path.exists():
            if not path.is_file():
                path.touch()
        with path.open("w", encoding="utf-8") as f:
            f.write(f"assets {len(self.assets)}\n")
            for level in self.assets:
                for asset in self.assets[level]:
                    data = f"{asset},{level}\n"
                    f.write(data)
            f.close()

    def load_asset_list(self) -> None:
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

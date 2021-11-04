from pathlib import Path

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from assetManager_GUI import Ui_asset_manager
from asset_GUI import Ui_asset
from asset import Asset
from newAssetWizard import NewAssetWizard


class AssetManager(qtw.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_asset_manager()
        self.ui.setupUi(self)

        self.ui.add_asset_button.clicked.connect(self.add_new_asset)
        self.ui.remove_asset_button.clicked.connect(self.remove_asset)

        # Data
        self.assets = []
        self.levels = []
        self.project_dir = Path()
        self.pipelines = {}
        self.registered_programs = []

    def add_new_asset(self):
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
            if a.asset.name == asset_name and a.asset.level == asset_level:
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

        asset_view = AssetView(new_asset, self.ui.asset_list)

        asset_item = qtw.QListWidgetItem()
        asset_item.setSizeHint(asset_view.sizeHint())
        self.ui.asset_list.addItem(asset_item)
        self.ui.asset_list.setItemWidget(asset_item, asset_view)

        self.assets.append(asset_view)

        # Serialize Asset
        self.save_asset(asset_view)
        self.save_asset_list()

    def remove_asset(self):
        selected_assets = self.ui.asset_list.selectedIndexes()
        if not selected_assets:
            return
        else:
            for i in selected_assets:
                print("[Asset Manager] Remove not yet implemented")
                # self.ui.asset_list.takeItem(i.row())
                # self.assets.remove(self.assets[i.row()])

        # TODO(Asset Manager): Remove Folder and files

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
    def save_asset_list(self):
        path = self.project_dir / "assets.meta"
        if not path.exists():
            if not path.is_file():
                path.touch()
        with path.open("w", encoding="utf-8") as f:
            f.write(f"assets {len(self.assets)}\n")
            for i in range(len(self.assets)):
                data = f"{self.assets[i].asset.name},{self.assets[i].asset.level}\n"
                f.write(data)
            f.close()

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

                asset = Asset(name=asset_data[0], level=asset_data[1].replace('\n', ''))
                self.load_asset(asset)

    def save_asset(self, asset_view):
        asset_view.asset.save(self.project_dir)

    def load_asset(self, asset):
        asset_view = AssetView(asset, self.ui.asset_list)
        asset_view.asset.load(self.project_dir)

        asset_item = qtw.QListWidgetItem()
        asset_item.setSizeHint(asset_view.sizeHint())
        self.ui.asset_list.addItem(asset_item)
        self.ui.asset_list.setItemWidget(asset_item, asset_view)

        self.assets.append(asset_view)
        asset_view.update_ui()


class AssetView(qtw.QWidget):
    def __init__(self, asset: Asset, parent=None):
        # GUI
        super().__init__(parent)
        self.ui = Ui_asset()
        self.ui.setupUi(self)

        # Data
        self.asset = asset

        self.update_ui()

    def update_ui(self):
        self.ui.name_label.setText(self.asset.name)
        self.ui.type_label.setText(self.asset.asset_type)

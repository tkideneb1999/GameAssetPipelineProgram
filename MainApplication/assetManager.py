from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from assetManager_GUI import Ui_asset_manager
from asset import Asset
from newAssetWizard import NewAssetWizard
from pathlib import Path


class AssetManager(qtw.QWidget):
    def __init__(self, parent):
        super().__init__(parent, )
        self.ui_asset_manager = Ui_asset_manager()
        self.ui_asset_manager.setupUi(self)

        self.ui_asset_manager.add_asset_button.clicked.connect(self.add_asset)
        self.ui_asset_manager.remove_asset_button.clicked.connect(self.remove_asset)
        self.assets = []
        self.levels = []
        self.project_dir = Path()

    def add_asset(self):
        dialog = NewAssetWizard(self.levels)
        dialog.setWindowModality(qtc.Qt.ApplicationModal)
        result = dialog.exec_()
        if result == 0:
            return

        # Get new asset data
        asset_name = dialog.get_name_data()
        asset_level = dialog.get_level_data()
        asset_tags = dialog.get_tags_data()
        asset_comment = dialog.get_comment_data()

        # Check Data
        # Check if Asset Name already exists in Level
        for a in self.assets:
            if a.name == asset_name and a.level == asset_level:
                print(f"Asset{asset_name} already exists in Level {asset_level}.")  # TODO: Optimize Asset search
                self.add_asset()
                return

        # Check if selected level is viable
        if asset_level not in self.levels:
            print(f"{asset_level} is not a valid Level.")
            self.add_asset()
            return

        # Create Asset
        new_asset = Asset(self.ui_asset_manager.asset_list, asset_name, asset_level, asset_tags, "Model", asset_comment)
        asset_item = qtw.QListWidgetItem()
        asset_item.setSizeHint(new_asset.sizeHint())
        self.ui_asset_manager.asset_list.addItem(asset_item)
        self.ui_asset_manager.asset_list.setItemWidget(asset_item, new_asset)

        self.assets.append(new_asset)

        # Create Files
        abs_asset_path = self.project_dir / new_asset.level / new_asset.name
        abs_asset_path.mkdir()
        # TODO: Create rest of asset files

    def remove_asset(self):
        selected_assets = self.ui_asset_manager.asset_list.selectedIndexes()
        if not selected_assets:
            return
        else:
            for i in selected_assets:
                self.ui_asset_manager.asset_list.takeItem(i.row())
                self.assets.remove(self.assets[i.row()])

        # TODO: Remove Folder

    def add_levels(self, levels):
        self.levels.append(levels)

    def set_project_dir(self, project_dir):
        self.project_dir = project_dir

from pathlib import Path
import json

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from assetManager_GUI import Ui_asset_manager
from asset import Asset
from newAssetWizard import NewAssetWizard
from pipeline import Pipeline


class AssetManager(qtw.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui_asset_manager = Ui_asset_manager()
        self.ui_asset_manager.setupUi(self)

        self.ui_asset_manager.add_asset_button.clicked.connect(self.add_new_asset)
        self.ui_asset_manager.remove_asset_button.clicked.connect(self.remove_asset)

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

        asset_pipeline_dir = self.project_dir / self.pipelines[asset_pipeline_name]

        # Check Data
        # Check if Asset Name already exists in Level
        for a in self.assets:
            if a.name == asset_name and a.level == asset_level:
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
            self.ui_asset_manager.asset_list,
            asset_name,
            pipeline_dir=asset_pipeline_dir,
            level=asset_level,
            tags=asset_tags,
            asset_type="Model",
            comment=asset_comment)
        asset_item = qtw.QListWidgetItem()
        asset_item.setSizeHint(new_asset.sizeHint())
        self.ui_asset_manager.asset_list.addItem(asset_item)
        self.ui_asset_manager.asset_list.setItemWidget(asset_item, new_asset)

        self.assets.append(new_asset)

        # Create Files
        abs_asset_path = self.project_dir / new_asset.level / new_asset.name
        abs_asset_path.mkdir()
        self.save_asset(new_asset)
        self.save_asset_list()

        # Create Pipeline Step Files
        pipeline = Pipeline()
        pipeline.load(asset_pipeline_dir)
        for s in range(len(pipeline.pipeline_steps)):
            path = abs_asset_path / pipeline.pipeline_steps[s].name / "export"
            path.mkdir(parents=True)

    def add_asset_data(self, name: str, level: str, tags: list, comment: str):
        # Check Data
        # Check if Asset Name already exists in Level
        for a in self.assets:
            if a.name == name and a.level == level:
                print(f"Asset{name} already exists in Level {level}.")
                # TODO: Assets: Optimize Asset search
                return False

        # Check if selected level is viable
        if level not in self.levels:
            print(f"{level} is not a valid Level.")
            return False

        # Create Asset
        new_asset = Asset(self.ui_asset_manager.asset_list, name, level, tags, "Model",
                          comment)
        asset_item = qtw.QListWidgetItem()
        asset_item.setSizeHint(new_asset.sizeHint())
        self.ui_asset_manager.asset_list.addItem(asset_item)
        self.ui_asset_manager.asset_list.setItemWidget(asset_item, new_asset)

        self.assets.append(new_asset)
        return True

    def remove_asset(self):
        selected_assets = self.ui_asset_manager.asset_list.selectedIndexes()
        if not selected_assets:
            return
        else:
            for i in selected_assets:
                self.ui_asset_manager.asset_list.takeItem(i.row())
                self.assets.remove(self.assets[i.row()])

        # TODO: Remove Folder and files

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
                data = f"{self.assets[i].name},{self.assets[i].level}\n"
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
                asset = Asset(self.ui_asset_manager.asset_list, name=asset_data[0], level=asset_data[1].replace('\n', ''))
                self.load_asset(asset)

    def save_asset(self, asset):
        asset_path = self.project_dir / asset.level / asset.name / f"{asset.name}.meta"
        if not asset_path.exists():
            if not asset_path.is_file():
                asset_path.touch()
        asset_data = {
            "name": asset.name,
            "level": asset.level,
            "type": asset.asset_type,
            "pipeline_dir": str(asset.pipeline_dir),
            "tags": asset.tags,
            "comment": asset.comment
        }

        with asset_path.open('w', encoding="utf-8") as f:
            f.write(json.dumps(asset_data, indent=4))
            f.close()

    def load_asset(self, asset):
        asset_path = self.project_dir / asset.level / asset.name / f"{asset.name}.meta"
        if not asset_path.exists():
            if not asset_path.is_file():
                raise Exception("File does not exist!")
        with asset_path.open('r', encoding='utf-8') as f:
            data = f.read()
            asset_data = json.loads(data)
            asset.name = asset_data["name"]
            asset.level = asset_data["level"]
            asset.type = asset_data["type"]
            asset.pipeline = asset_data["pipeline_dir"]
            asset.tags = json.loads(asset_data["tags"])
            asset.comment = asset_data["comment"]

        asset_item = qtw.QListWidgetItem()
        asset_item.setSizeHint(asset.sizeHint())
        self.ui_asset_manager.asset_list.addItem(asset_item)
        self.ui_asset_manager.asset_list.setItemWidget(asset_item, asset)

        self.assets.append(asset)

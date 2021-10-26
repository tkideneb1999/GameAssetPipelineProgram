from pathlib import Path

from PyQt5 import QtWidgets as qtw

from asset_GUI import Ui_asset
from pipeline import Pipeline


class Asset(qtw.QWidget):
    def __init__(self, parent, name: str, pipeline_dir=Path(), level="lvl01", tags=None, asset_type="Model", comment=""):
        super().__init__(parent)
        if tags is None:
            tags = []
        self.ui = Ui_asset()
        self.ui.setupUi(self)
        self.name = name
        self.level = level
        self.tags = tags
        self.asset_type = asset_type
        self.pipeline_dir = pipeline_dir
        self.comment = comment

        self.update_list_ui()

    def update_list_ui(self):
        self.ui.name_label.setText(self.name)
        self.ui.type_label.setText(self.asset_type)

from PyQt5 import QtWidgets as qtw
from asset_GUI import Ui_asset


class Asset(qtw.QWidget):
    def __init__(self, parent, name="test Asset", level="lvl01", tags=[], asset_type="Model", comment=""):
        super().__init__(parent)
        self.ui_asset = Ui_asset()
        self.ui_asset.setupUi(self)
        self.name = name
        self.level = level
        self.tags = tags
        self.asset_type = asset_type
        self.pipeline_step = "Modeling"  # TODO: Make dependent of first pipeline step
        self.comment = comment

        self.update_list_ui()

    def update_list_ui(self):
        self.ui_asset.name_label.setText(self.name)
        self.ui_asset.type_label.setText(self.asset_type)
        self.ui_asset.pipeline_step_label.setText(self.pipeline_step)

    def serialize_metadata(self):
        pass

from PyQt5 import QtWidgets as qtw

from asset_GUI import Ui_asset


class Asset(qtw.QWidget):
    def __init__(self, parent, name: str, pipeline: str, level="lvl01", tags=[], asset_type="Model", comment=""):
        super().__init__(parent)
        self.ui_asset = Ui_asset()
        self.ui_asset.setupUi(self)
        self.name = name
        self.level = level
        self.tags = tags
        self.asset_type = asset_type
        self.pipeline_step = "Modeling"  # TODO: Assets: Make dependent of first pipeline step
        self.pipeline = "Point to Pipeline"  # TODO: Assets: Make Pipeline Variable refer to pipeline as string
        self.comment = comment
        self.pipeline = pipeline

        self.update_list_ui()

    def update_list_ui(self):
        self.ui_asset.name_label.setText(self.name)
        self.ui_asset.type_label.setText(self.asset_type)
        self.ui_asset.pipeline_step_label.setText(self.pipeline_step)

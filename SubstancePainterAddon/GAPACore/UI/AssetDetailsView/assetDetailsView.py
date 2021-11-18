import importlib

from PySide2 import QtWidgets as qtw

from . import assetDetails_GUI

importlib.reload(assetDetails_GUI)


class AssetDetailsView(qtw.QWidget):
    def __init__(self, parent=None):
        super(AssetDetailsView, self).__init__(parent)
        self.ui = assetDetails_GUI.Ui_asset_details()
        self.ui.setupUi(self)

    def update_asset_details(self,
                             name, level, pipeline_name,
                             tags, comment) -> None:
        # name: str, level: str, pipeline_name: str, tags: list[str], comment: str
        self.ui.name_label.setText(name)
        self.ui.level_label.setText(level)
        self.ui.pipeline_label.setText(pipeline_name)
        tags_string = ""
        for t in range(10):
            tags_string = tags_string + tags[t]
            if t < len(tags) - 1:
                tags_string = tags_string + ", "
        self.ui.tags_label.setText(tags_string)
        self.ui.comment_label.setText(comment)

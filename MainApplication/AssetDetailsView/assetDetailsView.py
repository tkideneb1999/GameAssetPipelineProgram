from PyQt5 import QtWidgets as qtw

from MainApplication.AssetDetailsView.assetDetails_GUI import Ui_asset_details


class AssetDetailsView(qtw.QWidget):
    def __init__(self, parent=None):
        super(AssetDetailsView, self).__init__(parent)
        self.ui = Ui_asset_details()
        self.ui.setupUi(self)

    def update_asset_details(self,
                             name: str, level: str, pipeline_name: str,
                             tags: list[str], comment: str) -> None:
        self.ui.name_label.setText(name)
        self.ui.level_label.setText(level)
        self.ui.pipeline_label.setText(pipeline_name)
        tags_string = ""
        for t in range(len(tags)):
            tags_string += tags[t]
            if t < len(tags) - 1:
                tags_string += ", "
        self.ui.tags_label.setText(tags_string)
        self.ui.comment_label.setText(comment)

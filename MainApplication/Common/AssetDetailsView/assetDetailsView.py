from qtpy import QtWidgets as qtw

from .assetDetails_GUI import Ui_asset_details
from ..TagSearchbar import tagView

class AssetDetailsView(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_asset_details()
        self.ui.setupUi(self)
        self.tags: list[tagView.TagView] = []

    def update_asset_details(self,
                             name: str, level: str, pipeline_name: str,
                             tags: list[str], comment: str) -> None:
        self.ui.name_label.setText(name)
        self.ui.level_label.setText(level)
        self.ui.pipeline_label.setText(pipeline_name)
        for t in self.tags:
            self.ui.tags_layout.removeWidget(t)
            t.deleteLater()
        self.tags.clear()
        for nt in tags:
            tag = tagView.TagView(nt, removable=False, parent=self)
            self.ui.tags_layout.addWidget(tag)
            self.tags.append(tag)
        self.ui.comment_label.setText(comment)

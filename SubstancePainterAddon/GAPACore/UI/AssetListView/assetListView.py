import importlib

from PySide2 import QtWidgets as qtw
from PySide2 import QtCore as qtc

from . import assetList_GUI

importlib.reload(assetList_GUI)

class AssetListView(qtw.QWidget):
    s_level_changed = qtc.Signal(str)  # returns currently selected level
    s_asset_changed = qtc.Signal(str, int)  # Returns level and index of list of currently selected level

    def __init__(self, parent=None):
        super(AssetListView, self).__init__(parent)
        self.ui = assetList_GUI.Ui_asset_list_widget()
        self.ui.setupUi(self)

        # Data
        self.assets = {}  # dict[str, list[str]]
        self.levels = []  # list[str]

        # GUI
        self.ui.levels_combobox.clear()
        self.ui.levels_combobox.addItems(self.levels)
        self.current_level = self.ui.levels_combobox.currentText()
        self.ui.levels_combobox.currentTextChanged.connect(self.level_selection_changed)
        self.ui.asset_list.currentRowChanged.connect(self.asset_selection_changed)

    def update_asset_list(self, asset_data) -> None:
        # asset_data: dict[str, list[str]]
        self.assets = asset_data
        self.update_levels(list(asset_data.keys()))

    def update_levels(self, levels) -> None:
        # levels: list[str]
        self.levels = levels
        self.ui.levels_combobox.clear()
        self.ui.levels_combobox.addItems(levels)
        self.current_level = self.ui.levels_combobox.currentText()

    def level_selection_changed(self, level) -> None:
        # level: str
        if level == "":
            return
        self.current_level = level
        self.ui.asset_list.clear()
        self.ui.asset_list.addItems(self.assets[level])
        self.s_level_changed.emit(level)

    def asset_selection_changed(self, index) -> None:
        # index: int
        self.s_asset_changed.emit(self.current_level, index)

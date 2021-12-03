import functools

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from MainApplication.AssetListView.assetList_GUI import Ui_asset_list_widget


class AssetListView(qtw.QWidget):
    s_level_changed = qtc.pyqtSignal(str)  # returns currently selected level
    s_asset_changed = qtc.pyqtSignal(str, int)  # Returns level and index of list of currently selected level
    s_open_file_explorer = qtc.pyqtSignal(str, str)  # level name, asset name

    def __init__(self, parent=None):
        super(AssetListView, self).__init__(parent)
        self.ui = Ui_asset_list_widget()
        self.ui.setupUi(self)

        # Data
        self.assets: dict[str, list[str]] = {}
        self.levels: list[str] = []

        # GUI
        self.ui.levels_combobox.clear()
        self.ui.levels_combobox.addItems(self.levels)
        self.current_level = self.ui.levels_combobox.currentText()
        self.ui.levels_combobox.currentTextChanged.connect(self.level_selection_changed)
        self.ui.asset_list.currentRowChanged.connect(self.asset_selection_changed)
        self.ui.asset_list.installEventFilter(self)

    def update_asset_list(self, asset_data: dict[str, list[str]]) -> None:
        self.assets = asset_data
        self.update_levels(list(asset_data.keys()))

    def update_levels(self, levels: list[str]) -> None:
        self.levels = levels
        self.ui.levels_combobox.clear()
        self.ui.levels_combobox.addItems(levels)
        self.current_level = self.ui.levels_combobox.currentText()

    def eventFilter(self, source, event) -> bool:
        if event.type() == qtc.QEvent.ContextMenu and source is self.ui.asset_list:

            asset_name = source.itemAt(event.pos()).text()
            print(event.pos())
            func = functools.partial(self.s_open_file_explorer.emit, self.current_level, asset_name)

            menu = qtw.QMenu(self)
            open_action = menu.addAction("Open in Explorer")
            open_action.triggered.connect(func)
            menu.exec_(event.globalPos())
            return True
        return super().eventFilter(source, event)


    def level_selection_changed(self, level: str) -> None:
        if level == "":
            return
        self.current_level = level
        self.ui.asset_list.clear()
        self.ui.asset_list.addItems(self.assets[level])
        self.s_level_changed.emit(level)

    def open_asset_in_explorer(self, asset: str) -> None:
        pass

    def asset_selection_changed(self, index: int) -> None:
        self.s_asset_changed.emit(self.current_level, index)

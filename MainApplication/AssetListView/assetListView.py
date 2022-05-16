import functools

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from MainApplication.AssetListView.assetList_GUI import Ui_asset_list_widget


class AssetListView(qtw.QWidget):
    s_asset_changed = qtc.pyqtSignal(str, str)  # Returns level name and asset name
    s_open_file_explorer = qtc.pyqtSignal(str, str)  # level name, asset name

    def __init__(self, parent=None):
        super(AssetListView, self).__init__(parent)
        self.ui = Ui_asset_list_widget()
        self.ui.setupUi(self)
        self.ui.asset_tree.setColumnCount(1)

        # Data
        self.assets: dict[str, list[str]] = {}
        self.levels: list[str] = []

        # GUI
        self.ui.asset_tree.itemClicked.connect(self.selection_changed)
        self.ui.asset_tree.installEventFilter(self)

    def update_asset_list(self, asset_data: dict[str, list[str]]) -> None:
        self.ui.asset_tree.clear()
        for lvl in list(asset_data.keys()):
            tree_level = TreeLevel(lvl, self.ui.asset_tree)
            for ast in asset_data[lvl]:
                tree_asset = TreeAsset(ast, tree_level, [])

    def eventFilter(self, source, event) -> bool:
        if event.type() == qtc.QEvent.ContextMenu and source is self.ui.asset_tree:

            tree_object = source.itemAt(event.pos())
            if type(tree_object) is TreeLevel:
                print("[GAPA] Level selected")
            elif type(tree_object) is TreeAsset:
                func = functools.partial(self.s_open_file_explorer.emit, tree_object.parent().name, tree_object.name)

                menu = qtw.QMenu(self)
                open_action = menu.addAction("Open in Explorer")
                open_action.triggered.connect(func)
                menu.exec_(event.globalPos())
            return True
        return super().eventFilter(source, event)

    def selection_changed(self, item, column: int):
        if type(item) is TreeAsset:
            self.s_asset_changed.emit(item.parent().name, item.name)


class TreeLevel(qtw.QTreeWidgetItem):
    def __init__(self, name: str, root: qtw.QTreeWidget):
        super().__init__(root)
        self.name = name
        self.setText(0, name)


class TreeAsset(qtw.QTreeWidgetItem):
    def __init__(self, name: str, level: qtw.QTreeWidgetItem, tags: list[int]):
        super().__init__(level)
        self.tags = tags
        self.name = name
        self.setText(0, name)

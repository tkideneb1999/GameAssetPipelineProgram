import functools

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from .assetList_GUI import Ui_asset_list_widget
from ..warningPopUp import WarningPopUp


class AssetListView(qtw.QWidget):
    s_asset_changed = qtc.pyqtSignal(str, str)  # Returns level name and asset name
    s_open_file_explorer = qtc.pyqtSignal(str, str)  # level name, asset name
    s_add_asset = qtc.pyqtSignal(bool, str)  # level selected, level name
    s_remove_asset = qtc.pyqtSignal(str, str)  # level name, asset name
    s_add_level = qtc.pyqtSignal()
    s_remove_level = qtc.pyqtSignal(str)  # Level

    def __init__(self, parent=None, mode=0):
        super(AssetListView, self).__init__(parent)
        self.ui = Ui_asset_list_widget()
        self.ui.setupUi(self)
        self.ui.asset_tree.setColumnCount(1)

        # Data
        self.mode = mode

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
            is_asset = False
            is_tree_object = False
            lvl_name = ""
            asset_name = ""
            if type(tree_object) is TreeLevel:
                print("[GAPA] Level selected")
                is_tree_object = True
                lvl_name = tree_object.name
            elif type(tree_object) is TreeAsset:
                is_asset = True
                is_tree_object = True
                lvl_name = tree_object.parent().name
                asset_name = tree_object.name

            menu = qtw.QMenu(self)

            if self.mode == 1:
                if is_asset and is_tree_object:
                    open_func = functools.partial(self.s_open_file_explorer.emit, tree_object.parent().name,
                                                  tree_object.name)
                    open_action = menu.addAction("Open in Explorer")
                    open_action.triggered.connect(open_func)

                    rename_action = menu.addAction("Rename Asset...")
                    rename_action.setEnabled(False)

                    remove_action = menu.addAction("Remove from Project")
                    remove_func = functools.partial(self.remove_asset, lvl_name, asset_name)
                    remove_action.triggered.connect(remove_func)
                    menu.addSeparator()
                elif not is_asset and is_tree_object:
                    rename_action = menu.addAction("Rename Level...")
                    rename_action.setEnabled(False)
                    remove_action = menu.addAction("Remove from Project")
                    remove_func = functools.partial(self.remove_level, lvl_name)
                    remove_action.triggered.connect(remove_func)
                    menu.addSeparator()

                add_asset_func = functools.partial(self.s_add_asset.emit, is_tree_object, lvl_name)
                add_asset_action = menu.addAction("Add Asset...")
                add_asset_action.triggered.connect(add_asset_func)
                add_level_action = menu.addAction("Add Level...")
                add_level_action.triggered.connect(self.s_add_level.emit)

                menu.exec_(event.globalPos())
            return True
        return super().eventFilter(source, event)

    def remove_asset(self, lvl_name, asset_name):
        warning_dialog = WarningPopUp("This will remove the asset from the project!"
                                      "\nThe data will be marked deprecated and can still be accessed by navigating the folder structure.")
        if warning_dialog.exec_() == 1:
            self.s_remove_asset.emit(lvl_name, asset_name)

    def remove_level(self, lvl_name):
        warning_dialog = WarningPopUp("This will remove the level and the assets contained in it from the project!"
                                      "\nThe data will be marked deprecated and can still be accessed by navigating the folder structure.")
        if warning_dialog.exec_() == 1:
            self.s_remove_level.emit(lvl_name)

    def selection_changed(self, item, column: int):
        if type(item) is TreeAsset:
            self.s_asset_changed.emit(item.parent().name, item.name)

    def get_current_item(self):
        item_type = type(self.ui.asset_tree.currentItem())
        if item_type is TreeLevel:
            return self.ui.asset_tree.currentItem().text(0)
        elif item_type is TreeAsset:
            return self.ui.asset_tree.currentItem().parent().text(0)
        else:
            return None


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

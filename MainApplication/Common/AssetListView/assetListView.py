import functools

from qtpy import QtWidgets as qtw
from qtpy import QtCore as qtc

from .assetList_GUI import Ui_asset_list_widget
from ..warningPopUp import WarningPopUp


class AssetListView(qtw.QWidget):
    s_asset_changed = qtc.Signal(int)  # Returns asset ID
    s_open_file_explorer = qtc.Signal(int)  # Asset ID
    s_add_asset = qtc.Signal(bool, str)  # level selected, level name
    s_remove_asset = qtc.Signal(int)  # Asset ID
    s_add_level = qtc.Signal()
    s_remove_level = qtc.Signal(str)  # Level
    s_tag_selection_changed = qtc.Signal(list)  # List of Tags
    s_tag_searchbar_selected = qtc.Signal()

    def __init__(self, parent=None, mode=0):
        super().__init__(parent)
        self.ui = Ui_asset_list_widget()
        self.ui.setupUi(self)
        self.ui.asset_tree.setColumnCount(1)

        # Data
        self.mode = mode

        # GUI
        self.ui.asset_tree.itemClicked.connect(self.selection_changed)
        self.ui.asset_tree.installEventFilter(self)

        self.ui.tag_searchbar.s_added_tag.connect(self.tag_selection_changed)
        self.ui.tag_searchbar.s_removed_tag.connect(self.tag_selection_changed)
        self.ui.tag_searchbar.s_tag_edit_focused.connect(self.s_tag_searchbar_selected.emit)

    def update_asset_list(self, asset_data: dict) -> None:
        self.ui.asset_tree.clear()
        for lvl in list(asset_data.keys()):
            tree_level = TreeLevel(lvl, self.ui.asset_tree)
            for ast in asset_data[lvl]:
                tree_asset = TreeAsset(ast[0], ast[1], tree_level)
        self.ui.asset_tree.expandAll()

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
                asset_id = tree_object.asset_id

            menu = qtw.QMenu(self)

            if self.mode == 1:
                if is_asset and is_tree_object:
                    open_func = functools.partial(self.s_open_file_explorer.emit,
                                                  tree_object.asset_id)
                    open_action = menu.addAction("Open in Explorer")
                    open_action.triggered.connect(open_func)

                    # Not Implemented
                    rename_action = menu.addAction("Rename Asset...")
                    rename_action.setEnabled(False)

                    remove_action = menu.addAction("Remove from Project")
                    remove_func = functools.partial(self.remove_asset,
                                                    tree_object.asset_id)
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

    def remove_asset(self, asset_id):
        warning_dialog = WarningPopUp("This will remove the asset from the project!"
                                      "\nThe data will be marked deprecated and can still be accessed by navigating the folder structure.")
        if warning_dialog.exec_() == 1:
            self.s_remove_asset.emit(asset_id)

    def remove_level(self, lvl_name):
        warning_dialog = WarningPopUp("This will remove the level and the assets contained in it from the project!"
                                      "\nThe data will be marked deprecated and can still be accessed by navigating the folder structure.")
        if warning_dialog.exec_() == 1:
            self.s_remove_level.emit(lvl_name)

    def selection_changed(self, item, column: int):
        if type(item) is TreeAsset:
            self.s_asset_changed.emit(item.asset_id)

    def get_current_item(self):
        item_type = type(self.ui.asset_tree.currentItem())
        if item_type is TreeLevel:
            return self.ui.asset_tree.currentItem().text(0)
        elif item_type is TreeAsset:
            return self.ui.asset_tree.currentItem().parent().text(0)
        else:
            return None

    def tag_selection_changed(self, tag: str) ->None:
        self.s_tag_selection_changed.emit(self.ui.tag_searchbar.selected_tags)

    def update_tags(self, new_tag_list: list) -> None:
        self.ui.tag_searchbar.update_tags(new_tag_list)


class TreeLevel(qtw.QTreeWidgetItem):
    def __init__(self, name: str, root: qtw.QTreeWidget):
        super().__init__(root)
        self.name = name
        self.setText(0, name)


class TreeAsset(qtw.QTreeWidgetItem):
    def __init__(self, asset_id: int, name: str, level: qtw.QTreeWidgetItem):
        super().__init__(level)
        self.asset_id = asset_id
        self.name = name
        self.setText(0, name)

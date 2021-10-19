from PyQt5 import QtWidgets as qtw
from newAssetWizard_GUI import Ui_new_asset_wizard


class NewAssetWizard(qtw.QDialog):
    def __init__(self, levels):
        super().__init__()
        self.ui_new_asset_wizard = Ui_new_asset_wizard()
        self.ui_new_asset_wizard.setupUi(self)
        self.setWindowTitle("Create New Asset")
        self.ui_new_asset_wizard.levels_combo_box.addItems(levels)
        print("Test")

    def get_name_data(self):
        return self.ui_new_asset_wizard.name_line_edit.text()

    def get_level_data(self):
        return self.ui_new_asset_wizard.levels_combo_box.currentText()

    def get_tags_data(self):
        tags_string = self.ui_new_asset_wizard.tags_line_edit.text()
        tags_string.replace(' ', '')
        return tags_string.split(',')

    def get_comment_data(self):
        return self.ui_new_asset_wizard.comment_line_edit.text()

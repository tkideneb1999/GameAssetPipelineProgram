from PyQt5 import QtWidgets as qtw
from .newAssetWizard_GUI import Ui_new_asset_wizard


class NewAssetWizard(qtw.QDialog):
    def __init__(self, levels, pipelines):
        super().__init__()
        self.ui = Ui_new_asset_wizard()
        self.ui.setupUi(self)
        self.setWindowTitle("Create New Asset")
        self.ui.levels_combo_box.addItems(levels)
        self.ui.pipeline_combobox.addItems(pipelines)

    def set_starting_level(self, lvl_name: str):
        self.ui.levels_combo_box.setCurrentText(lvl_name)

    def get_name_data(self):
        return self.ui.name_line_edit.text()

    def get_pipeline_data(self):
        return self.ui.pipeline_combobox.currentText()

    def get_level_data(self):
        return self.ui.levels_combo_box.currentText()

    def get_tags_data(self):
        tags_string = self.ui.tags_line_edit.text()
        tags_string.replace(' ', '')
        return tags_string.split(',')

    def get_comment_data(self):
        return self.ui.comment_line_edit.text()

from PyQt5 import QtWidgets as qtw
from projectWizard_GUI import Ui_project_wizard


class ProjectWizard(qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.ui_project_wizard = Ui_project_wizard()
        self.ui_project_wizard.setupUi(self)

        self.ui_project_wizard.file_dialog_button.clicked.connect(self.launch_file_dialog)
        self.ui_project_wizard.open_project_button.clicked.connect(self.launch_open_project_dialog)

        self.existing_project_file = ""
        self.open_existing_project = False

    def launch_file_dialog(self):
        directory = qtw.QFileDialog.getExistingDirectory(self, 'Select Project Root')
        self.ui_project_wizard.project_dir_line_edit.setText(directory)

    def launch_open_project_dialog(self):
        dialog = qtw.QFileDialog(self)
        dialog.setFileMode(qtw.QFileDialog.ExistingFile)
        dialog.setNameFilter("Project File (*.gapaproj)")
        dialog.setViewMode(qtw.QFileDialog.Detail)
        result = dialog.exec_()
        if result == 0:
            return
        self.existing_project_file = dialog.selectedFiles()[0]
        self.open_existing_project = True
        self.accept()

    def get_project_name_data(self):
        return self.ui_project_wizard.project_name_line_edit.text()

    def get_project_dir_data(self):
        return self.ui_project_wizard.project_dir_line_edit.text()

    def get_levels_data(self):
        levels_string = self.ui_project_wizard.levels_line_edit.text()
        levels_string = levels_string.replace(" ", "")
        return levels_string.split(',')

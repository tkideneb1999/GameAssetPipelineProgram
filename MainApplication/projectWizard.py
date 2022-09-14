from .Common.qtpy import QtWidgets as qtw
from .Common.qtpy import QtCore as qtc
from .Common.qtpy import QtGui as qtg
from .projectWizard_GUI import Ui_project_wizard
import re
from pathlib import Path


class ProjectWizard(qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.ui_project_wizard = Ui_project_wizard()
        self.ui_project_wizard.setupUi(self)

        self.ui_project_wizard.file_dialog_button.clicked.connect(self.launch_file_dialog)
        self.ui_project_wizard.open_project_button.clicked.connect(self.launch_open_project_dialog)
        self.ui_project_wizard.level_list.installEventFilter(self)
        self.ui_project_wizard.project_dir_line_edit.editingFinished.connect(self.project_dir_editing_finished)
        self.ui_project_wizard.project_name_line_edit.editingFinished.connect(self.name_editing_finished)

        self.existing_project_file = ""
        self.open_existing_project = False
        self.checks = [False, False, False]  # Project Name, Project Dir, Levels
        self.special_characters = re.compile(r'[@!#$%^&*()<>?/\|}{~:]')

    def launch_file_dialog(self):
        directory = qtw.QFileDialog.getExistingDirectory(self, 'Select Project Root')
        if directory == "" or not Path(directory).exists():
            print("[GAPA] Not a valid Path")
            self.check_and_enable_creation(1, False)
            return
        self.ui_project_wizard.project_dir_line_edit.setText(directory)
        self.check_and_enable_creation(1, True)

    def project_dir_editing_finished(self):
        dir = self.ui_project_wizard.project_dir_line_edit.text()
        if dir == "" or not Path(dir).exists():
            print("[GAPA] Not a valid Path")
            self.check_and_enable_creation(1, False)
            return
        self.check_and_enable_creation(1, True)
        print("[GAPA] Valid Path Set")

    def name_editing_finished(self):
        name = self.ui_project_wizard.project_name_line_edit.text()
        if self.contains_special_characters(name) or name == "":
            self.ui_project_wizard.project_dir_line_edit.setText("")
            self.check_and_enable_creation(0, False)
            print("[GAPA] Not a valid Name")
        self.check_and_enable_creation(0, True)
        print("[GAPA] Valid Name Set")

    def eventFilter(self, source, event):
        if event.type() == qtc.QEvent.ContextMenu and source is self.ui_project_wizard.level_list:
            add_action = qtg.QAction("Add Level...")
            add_action.triggered.connect(self.add_level)
            rename_action = qtg.QAction("Rename Level")
            rename_action.triggered.connect(self.rename_level)
            remove_action = qtg.QAction("Remove Level")
            remove_action.triggered.connect(self.remove_level)

            context_menu = qtw.QMenu()
            context_menu.addAction(add_action)
            context_menu.addAction(rename_action)
            context_menu.addAction(remove_action)

            context_menu.exec_(event.globalPos())
            return True
        return super().eventFilter(source, event)

    def add_level(self):
        print("[GAPA] Test Adding Level")
        text, ok = qtw.QInputDialog().getText(self, "Rename", "Level Name:", qtw.QLineEdit.Normal, "")

        if (not text == "") and ok:
            if self.contains_special_characters(text):
                print("[GAPA] Level Name contains characters that are not allowed")
                return
            self.ui_project_wizard.level_list.addItem(text)
            self.check_and_enable_creation(2, True)

    def rename_level(self):
        if self.ui_project_wizard.level_list.currentItem() is None:
            print("[GAPA] No Level Selected")
            return
        print("[GAPA] Test Rename Level")
        cur_lvl_name = self.ui_project_wizard.level_list.currentItem().text()
        text, ok = qtw.QInputDialog().getText(self, "Rename", "Level Name:", qtw.QLineEdit.Normal, cur_lvl_name)

        if (not text == "") and ok:
            if self.contains_special_characters(text):
                print("[GAPA] Level Name contains characters that are not allowed")
                return
            self.ui_project_wizard.level_list.currentItem().setText(text)

    def remove_level(self):
        if self.ui_project_wizard.level_list.currentItem() is None:
            print("[GAPA] No Level Selected")
        print("[GAPA] Test Removing Level")
        self.ui_project_wizard.level_list.takeItem(self.ui_project_wizard.level_list.currentRow())
        if self.ui_project_wizard.level_list.count() <= 0:
            self.check_and_enable_creation(2, False)

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
        level_names = []
        for i in range(self.ui_project_wizard.level_list.count()):
            level_names.append(self.ui_project_wizard.level_list.item(i).text())
        print(f"[GAPA] Levels: {level_names}")
        return level_names

    def set_data(self, proj_data: dict) -> None:
        self.ui_project_wizard.project_name_line_edit.setText(proj_data["proj_name"])
        self.ui_project_wizard.project_dir_line_edit.setText(proj_data["proj_dir"])
        for lvl_name in proj_data["proj_lvls"]:
            self.ui_project_wizard.level_list.addItem(lvl_name)

    def contains_special_characters(self, string: str) -> bool:
        if self.special_characters.search(string) is None:
            return False
        return True

    def check_and_enable_creation(self, check_index: int, check_value: bool) -> None:
        self.checks[check_index] = check_value
        for check in self.checks:
            if not check:
                self.ui_project_wizard.okay_button.setEnabled(False)
                return
        self.ui_project_wizard.okay_button.setEnabled(True)

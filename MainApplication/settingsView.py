from pathlib import Path

from PyQt5 import QtWidgets as qtw

from settings_GUI import Ui_settings
from settings import Settings


class SettingsView(qtw.QWidget):
    def __init__(self, parent=None):
        super(SettingsView, self).__init__(parent)
        self.ui = Ui_settings()
        self.ui.setupUi(self)

        self.ui.register_program_button.clicked.connect(self.register_program)

        # Data
        self.settings = Settings()
        self.settings.load()
        self.update_programs_list()

    def register_program(self) -> None:
        file_dialog = qtw.QFileDialog(self)
        file_dialog.setFileMode(qtw.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Program (*.exe)")
        file_dialog.setViewMode(qtw.QFileDialog.Detail)
        result = file_dialog.exec_()
        if result == 0:
            return

        str_path = file_dialog.selectedFiles()[0]
        path = Path(str_path)
        name = path.stem

        # Update settings singleton
        self.settings.register_program(name, path)

        # Update UI
        self.update_programs_list()

    def update_programs_list(self) -> None:
        self.ui.programs_list.clear()
        for p in self.settings.program_registration.registered_programs:
            program_view = ProgramListViewItem(
                p,
                self.settings.program_registration.get_program_addon_enabled(p),
                str(self.settings.program_registration.get_program_path(p)))
            program_item = qtw.QListWidgetItem()
            program_item.setSizeHint(program_view.sizeHint())
            self.ui.programs_list.addItem(program_item)
            self.ui.programs_list.setItemWidget(program_item, program_view)


class ProgramListViewItem(qtw.QWidget):
    def __init__(self, name: str, addon_enabled: bool, path: str, parent=None):
        super(ProgramListViewItem, self).__init__(parent)

        self.name_label = qtw.QLabel(name)
        self.addon_enabled_label = qtw.QLabel(str(addon_enabled))
        self.addon_enabled_label.setMaximumWidth(100)
        self.path_label = qtw.QLabel(path)

        self.layout = qtw.QHBoxLayout()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.addon_enabled_label)
        self.layout.addWidget(self.path_label)
        self.setLayout(self.layout)


from PyQt5 import QtWidgets as qtw

from .localSettingsView import LocalSettingsView


class PluginAssetSettingsView(qtw.QDialog):
    def __init__(self, settings: dict, enable_execute=False, saved_settings=None, outputs=None, parent=None):
        super(PluginAssetSettingsView, self).__init__(parent)

        self.execute_clicked = False
        self.current_output = None
        self.dialog_layout = qtw.QVBoxLayout(self)
        self.dialog_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.dialog_layout)

        self.settings_widget = LocalSettingsView(settings, saved_settings, self)
        self.dialog_layout.addWidget(self.settings_widget)

        self.outputs = outputs
        if outputs is not None:
            self.output_list = qtw.QListWidget(self)
            output_strings = [f"{o[0]}, {o[1]}" for o in self.outputs]
            self.output_list.addItems(output_strings)
            self.output_list.currentRowChanged.connect(self.selected_output)

        self.button_layout = qtw.QHBoxLayout(self)

        self.save_button = qtw.QPushButton("Save", self)
        self.save_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.save_button)

        self.cancel_button = qtw.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

        if enable_execute:
            self.execute_button = qtw.QPushButton("Execute", self)
            self.execute_button.clicked.connect(self.click_execute)
            self.button_layout.addWidget(self.execute_button)

        self.dialog_layout.addLayout(self.button_layout)

    def get_settings(self) -> dict:
        return self.settings_widget.settings

    def click_execute(self):
        self.execute_clicked = True
        self.accept()

    def set_all_settings(self, settings: dict) -> None:
        self.settings_widget.set_all_settings(settings)

    def selected_output(self, index: int):
        self.current_output = self.outputs[index]

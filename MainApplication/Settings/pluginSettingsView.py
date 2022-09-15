from qtpy import QtWidgets as qtw
import MainApplication.Plugins.pluginAPI as pluginAPI


class PluginSettingsView(qtw.QDialog):
    def __init__(self, settings: pluginAPI.PluginSettings, parent=None):
        super(PluginSettingsView, self).__init__(parent)
        self.dialog_layout = qtw.QVBoxLayout(self)
        self.setLayout(self.dialog_layout)
        self.settings_GUI = {}
        self.init_settings(settings.global_settings)
        self.accept_button = qtw.QPushButton("Ok", self)
        self.accept_button.clicked.connect(self.accept)
        self.dialog_layout.addWidget(self.accept_button)

    def init_settings(self, settings: dict):
        for name in settings:
            if settings[name]["type"] == "lineedit":
                self.add_lineedit(name, settings[name]["data"])
            elif settings[name]["type"] == "combobox":
                self.add_combobox(name, settings[name]["data"])
            elif settings[name]["type"] == "checkbox":
                self.add_checkbox(name, settings[name]["data"])

    def set_settings(self, settings_data: dict) -> None:
        for param in settings_data:
            gui = self.settings_GUI.get(param)
            if gui is None:
                print(f"[GAPA] Settings Element under that name does not exist: {param}")
                continue
            gui_type = type(gui[0])
            if gui_type == qtw.QComboBox:
                self.settings_GUI[param][0].setCurrentText(settings_data[param])
            elif gui_type == qtw.QLineEdit:
                self.settings_GUI[param][0].setText(settings_data[param])
            elif gui_type == qtw.QCheckBox:
                self.settings_GUI[param][0].setChecked(settings_data[param])

    def get_settings(self) -> dict:
        settings_data = {}
        for gui_name in self.settings_GUI:
            gui_type = type(self.settings_GUI[gui_name][0])
            if gui_type == qtw.QComboBox:
                settings_data[gui_name] = self.settings_GUI[gui_name][0].currentText()
            elif gui_type == qtw.QLineEdit:
                settings_data[gui_name] = self.settings_GUI[gui_name][0].text()
            elif gui_type == qtw.QCheckBox:
                settings_data[gui_name] = self.settings_GUI[gui_name][0].isChecked()
        return settings_data

    def add_lineedit(self, name: str, default_value):
        lineedit = qtw.QLineEdit(self)
        lineedit.setObjectName(name)
        if default_value is not None:
            lineedit.setText(default_value)

        label = qtw.QLabel(self)
        label.setText(name)

        layout = qtw.QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(lineedit)

        self.settings_GUI[name] = [lineedit, label, layout]
        self.dialog_layout.addLayout(layout)

    def add_combobox(self, name: str, data: list):
        combobox = qtw.QComboBox(self)
        combobox.setObjectName(name)
        combobox.addItems(data)

        label = qtw.QLabel(self)
        label.setText(name)

        layout = qtw.QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(combobox)

        self.settings_GUI[name] = [combobox, label, layout]
        self.dialog_layout.addLayout(layout)

    def add_checkbox(self, name: str, default_value: bool):
        checkbox = qtw.QCheckBox(self)
        checkbox.setObjectName(name)
        checkbox.setText(name)
        checkbox.setChecked(default_value)
        self.settings_GUI[name] = [checkbox]
        self.dialog_layout.addWidget(checkbox)

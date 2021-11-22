import importlib.util

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from MainApplication.settings import Settings
from MainApplication.PipelineConfigurator.pipeline_step_settings_GUI import Ui_pipeline_step_settings_GUI
from MainApplication.PipelineConfigurator.pipelineSettingsCreator import PipelineSettingsCreator


class PipelineStepSettingsView(qtw.QWidget):

    s_selected_config = qtc.pyqtSignal(str)
    s_settings_added = qtc.pyqtSignal(dict)
    s_settings_changed = qtc.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(PipelineStepSettingsView, self).__init__(parent)
        self.ui = Ui_pipeline_step_settings_GUI()
        self.ui.setupUi(self)
        self.ui.configs_combobox.currentTextChanged.connect(self.config_changed)

        self.program = "None"
        self.settings: PipelineSettingsCreator = None
        self.settings_active = False
        self.additional_GUI: dict[str, list[qtw.QWidget]] = {}
        self.pipelineSettings: PipelineSettingsCreator = PipelineSettingsCreator()
        self.update_ui()

    def update_ui(self) -> bool:
        self.clear_additional_GUI()
        settings = Settings()
        self.ui.configs_combobox.clear()
        print("[GAPA] setting up UI for step program settings")
        if not settings.program_registration.get_program_addon_enabled(self.program):
            print(f"[GAPA] Addon not enabled for {self.program}")
            return False

        # Load Addon Module
        addon_path = settings.program_registration.get_program_addon_path(self.program)
        spec = importlib.util.spec_from_file_location(addon_path.stem, str(addon_path))
        step_settings_registration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(step_settings_registration)

        # Check if settings are defined
        try:
            step_settings_registration.create_pipeline_settings
        except NameError:
            print("[GAPA] create_pipeline_settings function not found, automatic pipeline export not possible")
            self.settings_active = False
            return False

        # Get settings and check if they are set
        self.settings = step_settings_registration.create_pipeline_settings()
        if self.settings is None or {}:
            print("[GAPA] No settings set")
            return False

        self.settings_active = True
        # Add configs to combobox
        self.ui.configs_combobox.addItems(self.settings.configs.keys())

        if self.settings.settings is None or {}:
            return True
        for name in self.settings.settings:
            if self.settings.settings[name]["type"] == "combobox":
                self.add_combobox(name, self.settings.settings[name]["data"])

            if self.settings.settings[name]["type"] == "checkbox":
                self.add_checkbox(name, self.settings.settings[name]["data"])
        return True

    def add_combobox(self, name: str, data: list[str]) -> None:
        combobox = qtw.QComboBox(self)
        combobox.setObjectName(name)
        combobox.addItems(data)
        c_label = qtw.QLabel(self)
        c_label.setText(name)
        c_layout = qtw.QHBoxLayout(self)
        c_layout.addWidget(c_label)
        c_layout.addWidget(combobox)
        self.additional_GUI[name] = [combobox, c_label, c_layout]
        self.ui.verticalLayout.addLayout(c_layout)

    def add_checkbox(self, name: str, data: bool) -> None:
        checkbox = qtw.QCheckBox(self)
        checkbox.setObjectName(name)
        checkbox.setText(name)
        checkbox.setChecked(data)
        self.additional_GUI[name] = [checkbox]
        self.ui.verticalLayout.addWidget(checkbox)

    def clear_additional_GUI(self) -> None:
        for name in self.additional_GUI:
            for widget in self.additional_GUI[name]:
                widget.deleteLater()
        self.additional_GUI.clear()

    def get_additional_settings(self) -> dict:
        data = {}
        for name in self.additional_GUI:
            if type(self.additional_GUI[name][0]) is qtw.QComboBox:
                data[name] = self.additional_GUI[name][0].currentText()
            if type(self.additional_GUI[name][0]) is qtw.QCheckBox:
                data[name] = self.additional_GUI[name][0].isChecked()
        return data

    def set_additional_settings(self, data: dict) -> None:
        for name in self.additional_GUI:
            if type(self.additional_GUI[name][0]) is qtw.QComboBox:
                data[name] = self.additional_GUI[name][0].setCurrentText(data[name])
            if type(self.additional_GUI[name][0]) is qtw.QCheckBox:
                data[name] = self.additional_GUI[name][0].setChecked(data[name])

    def program_changed(self, selected_program: str) -> bool:
        self.program = selected_program
        return self.update_ui()

    def config_changed(self, config: str) -> None:
        if self.settings_active and (not config == ""):
            self.s_selected_config.emit(config)

    def current_config(self) -> str:
        return self.ui.configs_combobox.currentText()

    def config_available(self) -> bool:
        return self.settings_active

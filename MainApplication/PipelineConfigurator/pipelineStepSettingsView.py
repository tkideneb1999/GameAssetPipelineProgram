import importlib.util

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from MainApplication.Core.settings import Settings
from MainApplication.PipelineConfigurator.pipeline_step_settings_GUI import Ui_pipeline_step_settings_GUI
from MainApplication.PipelineConfigurator.pipelineSettingsCreator import PipelineSettingsCreator
from MainApplication.Plugins.pluginAPI import PluginSettings


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
        self.is_plugin = False
        self.has_set_outputs = False
        self.export_all = False
        self.settings: PipelineSettingsCreator = None
        self.settings_active = False
        self.additional_GUI: dict[str, list[qtw.QWidget]] = {}
        self.update_ui()

    def update_ui(self) -> bool:
        settings = Settings()
        program_list = settings.program_registration.get_program_list()
        plugin_list = settings.plugin_registration.get_plugin_list()
        if self.program in program_list:
            self.is_plugin = False
            return self.update_ui_with_program()
        elif self.program in plugin_list:
            self.is_plugin = True
            return self.update_ui_with_plugin()

    def update_ui_with_program(self) -> bool:
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
        self.has_set_outputs = self.settings.has_set_outputs
        self.export_all = self.settings.export_all
        # Add configs to combobox
        configs_available = (not self.settings.configs == {})
        if configs_available:
            self.ui.configs_combobox.addItems(self.settings.configs.keys())

        if self.settings.settings is None or {}:
            return configs_available
        for name in self.settings.settings:
            if self.settings.settings[name]["type"] == "combobox":
                self.add_combobox(name, self.settings.settings[name]["data"])

            if self.settings.settings[name]["type"] == "checkbox":
                self.add_checkbox(name, self.settings.settings[name]["data"])
        return configs_available

    def update_ui_with_plugin(self) -> bool:
        self.clear_additional_GUI()
        self.ui.configs_combobox.clear()
        settings = Settings()

        # Get Plugin
        plugin = settings.plugin_registration.get_plugin(self.program)
        self.settings = plugin.register_settings()
        if self.settings is None:
            print("[GAPA] No settings set")
            self.settings_active = False
            return False

        self.settings_active = True
        self.has_set_outputs = self.settings.has_set_outputs
        self.export_all = self.settings.export_all

        configs_available = (not self.settings.configs == {})
        if configs_available:
            self.ui.configs_combobox.addItems(self.settings.configs.keys())

        if self.settings.pipeline_settings is None or {}:
            return configs_available
        for name in self.settings.pipeline_settings:
            if self.settings.pipeline_settings[name]["type"] == "combobox":
                self.add_combobox(name, self.settings.pipeline_settings[name]["data"])

            elif self.settings.pipeline_settings[name]["type"] == "checkbox":
                self.add_checkbox(name, self.settings.pipeline_settings[name]["data"])

            elif self.settings.pipeline_settings[name]["type"] == "lineedit":
                self.add_lineedit(name, self.settings.pipeline_settings[name]["data"])
        return configs_available

    # -------------
    # GUI Functions
    # -------------

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

    def add_lineedit(self, name: str, default_value: str):
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

    def clear_additional_GUI(self) -> None:
        for name in self.additional_GUI:
            for widget in self.additional_GUI[name]:
                widget.deleteLater()
        self.additional_GUI.clear()

    def get_additional_settings(self) -> dict:
        data = {}
        for name in self.additional_GUI:
            gui_type = type(self.additional_GUI[name][0])
            if gui_type is qtw.QComboBox:
                data[name] = self.additional_GUI[name][0].currentText()
            elif gui_type is qtw.QCheckBox:
                data[name] = self.additional_GUI[name][0].isChecked()
            elif gui_type is qtw.QLineEdit:
                data[name] = self.additional_GUI[name][0].text()

        return data

    def get_required_settings(self) -> dict:
        return {"has_set_outputs": self.has_set_outputs,
                "export_all": self.export_all,
                "is_plugin": self.is_plugin}

    def set_additional_settings(self, data: dict) -> None:
        for name in self.additional_GUI:
            gui_type = type(self.additional_GUI[name][0])
            if gui_type is qtw.QComboBox:
                data[name] = self.additional_GUI[name][0].setCurrentText(data[name])
            elif gui_type is qtw.QCheckBox:
                data[name] = self.additional_GUI[name][0].setChecked(data[name])
            elif gui_type is qtw.QLineEdit:
                data[name] = self.additional_GUI[name][0].setText(data[name])

    def program_changed(self, selected_program: str) -> bool:
        self.program = selected_program
        return self.update_ui()

    def config_changed(self, config: str) -> None:
        if self.settings_active and (not config == ""):
            if config is not self.ui.configs_combobox.currentText():
                self.ui.configs_combobox.setCurrentText(config)
            self.s_selected_config.emit(config)

    def current_config(self) -> str:
        return self.ui.configs_combobox.currentText()

    def config_available(self) -> bool:
        return self.settings_active

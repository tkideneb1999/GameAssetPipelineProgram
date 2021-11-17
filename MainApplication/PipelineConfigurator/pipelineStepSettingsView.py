import importlib.util

from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore as qtc

from MainApplication.settings import Settings
from MainApplication.PipelineConfigurator.pipelineSettingsCreator import PipelineSettingsCreator
from MainApplication.PipelineConfigurator.pipeline_step_settings_GUI import Ui_pipeline_step_settings_GUI


class PipelineStepSettingsView(QWidget):

    s_selected_config = qtc.pyqtSignal(str)

    def __init__(self, parent=None):
        super(PipelineStepSettingsView, self).__init__(parent)
        self.ui = Ui_pipeline_step_settings_GUI()
        self.ui.setupUi(self)
        self.ui.configs_combobox.currentTextChanged.connect(self.config_changed)

        self.program = "None"
        self.settings = {}
        self.settings_active = False
        self.pipelineSettings: PipelineSettingsCreator = PipelineSettingsCreator()
        self.update_ui()

    def update_ui(self) -> bool:
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
        self.ui.configs_combobox.addItems(self.settings.settings.keys())
        return True

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

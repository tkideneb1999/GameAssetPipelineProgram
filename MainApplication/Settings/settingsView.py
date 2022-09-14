from ..Common.qtpy import QtWidgets as qtw
from ..Common.qtpy import QtCore as qtc

from .settings_GUI import Ui_settings
from MainApplication.Common.Core.settings import Settings
from .plugin_item_GUI import Ui_plugin_item
from .pluginSettingsView import PluginSettingsView


class SettingsView(qtw.QWidget):
    s_program_registered = qtc.Signal()

    def __init__(self, parent=None):
        super(SettingsView, self).__init__(parent)
        self.ui = Ui_settings()
        self.ui.setupUi(self)

        # Plugin List GUI
        self.plugin_list_layout = qtw.QVBoxLayout(self)
        self.plugin_list_layout.addStretch()
        self.plugin_list = qtw.QWidget(self)
        self.plugin_list.setLayout(self.plugin_list_layout)
        self.ui.plugins_scrollbar.setWidget(self.plugin_list)

        # Data
        self.settings = Settings()
        self.settings.load()

        self.update_programs_list()
        self.update_plugin_list()

    def update_programs_list(self) -> None:
        self.ui.programs_list.clear()
        for p in self.settings.program_registration.registered_programs:
            program_view = ProgramListViewItem(
                p,
                self.settings.program_registration.get_program_addon_enabled(p))
            program_item = qtw.QListWidgetItem()
            program_item.setSizeHint(program_view.sizeHint())
            self.ui.programs_list.addItem(program_item)
            self.ui.programs_list.setItemWidget(program_item, program_view)

    def update_plugin_list(self) -> None:
        for p in self.settings.plugin_registration.registered_plugins:
            plugin_item = PluginListViewItem(p)
            plugin_item.setObjectName(p)
            self.plugin_list_layout.insertWidget(self.plugin_list_layout.count() - 1, plugin_item)
            plugin_item.s_launch_settings.connect(self.launch_plugin_settings)

    def launch_plugin_settings(self, name: str) -> None:
        print(f"[GAPA] Launching Plugin settings: {name}")
        module = self.settings.plugin_registration.registered_plugins[name]
        settings = module.register_settings()
        settings_data = self.settings.plugin_registration.global_settings[name]
        settings_dialog = PluginSettingsView(settings)
        settings_dialog.setWindowModality(qtc.Qt.ApplicationModal)
        settings_dialog.set_settings(settings_data)
        result = settings_dialog.exec_()
        if not result == 0:
            settings_data = settings_dialog.get_settings()
            self.settings.plugin_registration.global_settings[name] = settings_data
            self.settings.save()


class ProgramListViewItem(qtw.QWidget):
    def __init__(self, name: str, addon_enabled: bool, parent=None):
        super(ProgramListViewItem, self).__init__(parent)

        self.name_label = qtw.QLabel(name)
        self.addon_enabled_label = qtw.QLabel(str(addon_enabled))
        self.addon_enabled_label.setMaximumWidth(100)

        self.layout = qtw.QHBoxLayout()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.addon_enabled_label)
        self.setLayout(self.layout)


class PluginListViewItem(qtw.QWidget):
    s_launch_settings = qtc.Signal(str)

    def __init__(self, plugin_name, parent=None):
        super(PluginListViewItem, self).__init__(parent)
        self.ui = Ui_plugin_item()
        self.ui.setupUi(self)
        self.name = plugin_name
        self.ui.name_label.setText(plugin_name)
        self.ui.settings_button.clicked.connect(self.launch_settings)

    def launch_settings(self):
        self.s_launch_settings.emit(self.name)

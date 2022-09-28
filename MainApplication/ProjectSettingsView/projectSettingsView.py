from pathlib import Path
import json

from qtpy import QtWidgets as qtw
from qtpy import QtCore as qtc

from ..Common.Core.settings import Settings
from ..Common.localSettingsView import LocalSettingsView
from ..TagDatabaseView.tagDatabaseWidget import TagDatabaseWidget


class ProjectSettingsView(qtw.QWidget):
    def __init__(self, parent=None):
        super(ProjectSettingsView, self).__init__(parent)
        self.settings_layout = qtw.QVBoxLayout(self)
        self.settings_layout.setContentsMargins(0, 0, 0, 0)

        self.plugin_tab_widget = qtw.QTabWidget()
        self.plugin_tab_widget.setTabPosition(qtw.QTabWidget.West)
        self.settings_layout.addWidget(self.plugin_tab_widget)
        self.setLayout(self.settings_layout)
        self.tabs: dict[str, qtw.QWidget] = {}
        self.plugin_widgets: dict[str, LocalSettingsView] = {}

        self.project_dir: Path = None

        self.create_tab("Tag Database")
        self.tag_database = TagDatabaseWidget(self)
        self.tabs["Tag Database"].layout().addWidget(self.tag_database)

        settings = Settings()
        settings.load()
        for plugin_name in settings.plugin_registration.get_plugin_list():
            self.create_tab(plugin_name)
            plugin = settings.plugin_registration.get_plugin(plugin_name)
            plugin_gui_settings = plugin.register_settings()
            project_gui_settings = plugin_gui_settings.project_settings
            self.plugin_widgets[plugin_name] = LocalSettingsView(project_gui_settings)
            self.tabs[plugin_name].layout().addWidget(self.plugin_widgets[plugin_name])

        self.save_button = qtw.QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        self.button_layout = qtw.QHBoxLayout(self)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setAlignment(qtc.Qt.AlignLeft)
        self.button_layout.addWidget(self.save_button)
        self.settings_layout.addLayout(self.button_layout)

    def create_tab(self, name: str) -> None:
        self.tabs[name] = qtw.QWidget(self.plugin_tab_widget)
        layout = qtw.QVBoxLayout(self.tabs[name])
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(qtc.Qt.AlignTop)
        self.tabs[name].setLayout(layout)
        self.plugin_tab_widget.addTab(self.tabs[name], name)

    def set_project_dir(self, project_dir: Path) -> None:
        self.project_dir = project_dir
        self.tag_database.load_tags(self.project_dir)
        has_loaded = self.load()

    def save(self) -> None:
        if self.project_dir is None:
            print("[GAPA] No Project Dir set for Project Settings")
            return

        settings = {}
        for plugin_name in self.plugin_widgets:
            plugin_settings = self.plugin_widgets[plugin_name].get_settings()
            settings[plugin_name] = plugin_settings

        path = self.project_dir / "projectPluginSettings.json"
        if not path.exists():
            path.touch()
        with path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(settings, indent=4))

    def load(self) -> bool:
        if self.project_dir is None:
            print("[GAPA] No Project Dir set for Project Settings")
            return False

        path = self.project_dir / "projectPluginSettings.json"
        if not path.exists():
            print("[GAPA] projectPluginSettings.json does not exist using default")
            return False
        settings = {}
        with path.open("r", encoding="utf-8") as f:
            settings = json.loads(f.read())
        for plugin_name in settings:
            if plugin_name not in self.plugin_widgets:
                print(f"Plugin not registered but has saved settings: {plugin_name}")
                continue
            self.plugin_widgets[plugin_name].set_all_settings(settings[plugin_name])

import sys
from pathlib import Path
import json
import os

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from .MainApplication_GUI import Ui_MainWindow
from .PipelineConfigurator.pipelineConfigurator import PipelineConfigurator
from MainApplication.Settings.settingsView import SettingsView
from .assetManager import AssetManager
from .projectWizard import ProjectWizard
from .LoadCurrentProjectWizard.loadCurrentProjectWizard import LoadCurrentProjectWizard
from .ProjectSettingsView.projectSettingsView import ProjectSettingsView


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Game Asset Pipeline Automation")

        # set up tabs
        self.settingsWidget = SettingsView(self.ui.settings_tab)
        file_location = Path(os.path.abspath(__file__))
        print(file_location.parent)
        plugin_dir = file_location.parent / "Plugins"
        self.settingsWidget.settings.set_plugin_dir(plugin_dir)
        self.ui.settings_tab.layout().addWidget(self.settingsWidget)

        self.pipeline_configurator = PipelineConfigurator(self.ui.pipelines_tab)
        self.pipeline_configurator.s_pipeline_saved.connect(self.add_pipeline)

        self.ui.pipelines_tab.layout().addWidget(self.pipeline_configurator)

        self.assetManager = AssetManager(self.ui.assets_tab)
        self.assetManager.s_level_added.connect(self.add_level)
        self.assetManager.s_level_removed.connect(self.remove_level)
        self.ui.assets_tab.layout().addWidget(self.assetManager)

        self.project_settings_widget = ProjectSettingsView(self.ui.project_settings_tab)
        self.ui.project_settings_tab.layout().addWidget(self.project_settings_widget)

        self.ui.actionSet_as_current_project.triggered.connect(self.set_as_current_project)

        # Data
        self.project_name = ""
        self.project_dir = Path()
        self.levels = []
        self.pipelines = {}

    def launch_project_wizard(self, proj_data=None):
        project_wizard = ProjectWizard()
        if proj_data is not None:
            project_wizard.set_data(proj_data)
        project_wizard.setWindowModality(qtc.Qt.ApplicationModal)
        result = project_wizard.exec_()
        if result == 0:
            print("No Project dir set")
            self.launch_project_wizard()
            return

        # If Existing Project is opened
        if project_wizard.open_existing_project:
            self.project_dir = Path(project_wizard.existing_project_file).parent
            self.load_project_info()
            self.assetManager.add_levels(self.levels)
            self.assetManager.set_project_dir(self.project_dir)
            self.assetManager.update_pipelines(self.pipelines)
            self.assetManager.load_asset_list()
            self.pipeline_configurator.set_project_dir(self.project_dir)
            return

        # Check Data
        proj_name = project_wizard.get_project_name_data()
        proj_dir = project_wizard.get_project_dir_data()
        proj_lvls = project_wizard.get_levels_data()

        proj_name_ok = not (proj_name == "")
        proj_dir_ok = not (proj_dir == "") and Path(proj_dir).exists()
        proj_lvls_ok = not(len(proj_lvls) == 1 and proj_lvls[0] == "")

        if (not proj_name_ok) or (not proj_dir_ok) or (not proj_lvls_ok):
            proj_data = {}
            if not proj_name_ok:
                print("[GAPA] Not a valid Project Name")
                proj_data["proj_name"] = ""
            else:
                proj_data["proj_name"] = proj_name
            if not proj_dir_ok:
                print("[GAPA] Current Project Dir is not a valid path")
                proj_data["proj_dir"] = ""
            else:
                proj_data["proj_dir"] = Path(proj_dir)
            if not proj_lvls_ok:
                print("[GAPA] No Levels Supplied")
                proj_data["proj_lvls"] = []
            else:
                proj_data["proj_lvls"] = proj_lvls
            print("[GAPA] Restarting Project Wizard")
            self.launch_project_wizard(proj_data=proj_data)



        ## Check if Project Name is set
        #if proj_name == "":
        #    print("No Project Name set. Restarting Wizard")
        #    self.launch_project_wizard()
        #    return
#
        #if proj_dir is None:
        #    print("Current Project Dir is no a valid path. Restarting Wizard")
        #    self.launch_project_wizard()
        #    return
#
        #proj_dir = Path(proj_dir) / proj_name
#
        #if not proj_dir.parents[0].exists():
        #    print("Current Project Dir is no a valid path. Restarting Wizard")
        #    self.launch_project_wizard()
        #    return
#
        #if len(proj_lvls) == 0:
        #    print("No Levels Supplied. Restarting Project Wizard")
        #    self.launch_project_wizard()
        #    return

        # Set Project Data
        self.project_name = proj_name
        self.project_dir = Path(proj_dir) / self.project_name
        self.levels = proj_lvls

        # Set Asset Manager Data
        self.assetManager.add_levels(self.levels)
        self.assetManager.set_project_dir(self.project_dir)

        # Set Pipeline Data
        self.pipeline_configurator.set_project_dir(self.project_dir)

        # Set Project Settings Data
        self.project_settings_widget.set_project_dir(self.project_dir)

        # Create Level Folders
        for lvl in self.levels:
            path = self.project_dir / lvl
            path.mkdir(parents=True)
            print(path)

        self.save_project_info()
        self.assetManager.save_asset_list()

    def load_current_project(self) -> bool:
        current_project_wizard = LoadCurrentProjectWizard(self)
        current_project_wizard.setWindowModality(qtc.Qt.ApplicationModal)
        result = current_project_wizard.exec_()
        if result == 0:
            return False
        else:
            current_project = self.settingsWidget.settings.current_project_info_path
            self.project_dir = current_project.parent
            self.load_project_info()
            self.assetManager.add_levels(self.levels)
            self.assetManager.set_project_dir(self.project_dir)
            self.assetManager.update_pipelines(self.pipelines)
            self.assetManager.load_asset_list()
            self.pipeline_configurator.set_project_dir(self.project_dir)
            self.project_settings_widget.set_project_dir(self.project_dir)
            return True

    def add_pipeline(self, path: Path, name: str):
        r_path = path.relative_to(self.project_dir)
        self.pipelines[name] = r_path
        self.save_project_info()
        self.assetManager.update_pipelines(self.pipelines)

    def add_level(self, lvl_name: str):
        if lvl_name in self.levels:
            print("[GAPA] Level Name already exists")
        self.levels.append(lvl_name)
        self.save_project_info()
        path = self.project_dir / lvl_name
        path.mkdir(parents=True)

    def remove_level(self, lvl_name: str):
        self.levels.remove(lvl_name)
        self.save_project_info()
        path = self.project_dir / lvl_name
        path.rename(self.project_dir / f"deprecated_{lvl_name}")

    def set_as_current_project(self):
        self.settingsWidget.settings.set_current_project(self.project_dir / "projectInfo.gapaproj")

    # -------------
    # SERIALIZATION
    # -------------
    def save_project_info(self):
        path = self.project_dir / "projectInfo.gapaproj"
        if not path.exists():
            if not path.is_file():
                path.touch()
        with path.open("w", encoding="utf-8") as f:
            pipeline_data = {}
            for name in self.pipelines:
                pipeline_data[name] = str(self.pipelines[name])
            project_data = {"name": self.project_name, "levels": self.levels, "pipelines": pipeline_data}
            f.write(json.dumps(project_data, indent=4))
            f.close()

        self.project_settings_widget.save()

    def load_project_info(self):
        path = self.project_dir / "projectInfo.gapaproj"
        if not path.exists():
            if not path.is_file():
                if not path.suffix == "gapaproj":
                    raise Exception("Not a valid project info file")
        with path.open("r", encoding="utf-8") as f:
            project_data = json.loads(f.read())
            self.project_name = project_data["name"]

            self.levels.clear()
            self.levels = project_data["levels"]

            self.pipelines.clear()
            pipeline_data = project_data["pipelines"]
            for name in pipeline_data:
                self.pipelines[name] = Path(pipeline_data[name])


def start_GAPA():
    app = qtw.QApplication(sys.argv)
    print(sys.argv)

    window = MainWindow()
    window.show()
    if not window.load_current_project():
        window.launch_project_wizard()

    app.exec_()

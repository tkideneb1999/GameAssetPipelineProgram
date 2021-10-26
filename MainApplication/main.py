import sys
from pathlib import Path
import json
import os

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from MainApplication_GUI import Ui_MainWindow
from pipelineConfigurator import PipelineConfigurator
from assetManager import AssetManager
from projectWizard import ProjectWizard


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Game Asset Pipeline Automation")

        # set up tabs
        self.pipeline_configurator = PipelineConfigurator(self.ui.pipelines_tab)
        self.pipeline_configurator.pipeline_saved_signal.connect(self.add_pipeline)

        self.ui.pipelines_tab.layout().addWidget(self.pipeline_configurator)

        self.assetManager = AssetManager(self.ui.assets_tab)
        self.ui.assets_tab.layout().addWidget(self.assetManager)

        # Data
        self.project_name = ""
        self.project_dir = Path()
        self.levels = []
        self.pipelines = {}

    def launch_project_wizard(self):
        project_wizard = ProjectWizard()
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
            self.assetManager.load_asset_list()
            self.assetManager.update_pipelines(self.pipelines)
            self.pipeline_configurator.set_project_dir(self.project_dir)
            return

        # Check Data
        proj_name = project_wizard.get_project_name_data()
        proj_dir = project_wizard.get_project_dir_data()
        proj_lvls = project_wizard.get_levels_data()

        # Check if Project Name is set
        if proj_name == "":
            print("No Project Name set. Restarting Wizard")
            self.launch_project_wizard()
            return

        if proj_dir is None:
            print("Current Project Dir is no a valid path. Restarting Wizard")
            self.launch_project_wizard()
            return

        proj_dir = Path(proj_dir) / proj_name

        if not proj_dir.parents[0].exists():
            print("Current Project Dir is no a valid path. Restarting Wizard")
            self.launch_project_wizard()
            return

        if len(proj_lvls) == 0:
            print("No Levels Supplied. Restarting Project Wizard")
            self.launch_project_wizard()
            return

        # Set Project Data
        self.project_name = proj_name
        self.project_dir = proj_dir
        self.levels = proj_lvls

        # Set Asset Manager Data
        self.assetManager.add_levels(self.levels)
        self.assetManager.set_project_dir(self.project_dir)

        # Set Pipeline Data
        self.pipeline_configurator.set_project_dir(self.project_dir)

        # Create Level Folders
        for lvl in self.levels:
            path = self.project_dir / lvl
            path.mkdir(parents=True)
            print(path)

        self.save_project_info()
        self.assetManager.save_asset_list()

    def add_pipeline(self, path: Path, name: str):
        r_path = path.relative_to(self.project_dir)
        self.pipelines[name] = r_path
        self.save_project_info()
        self.assetManager.update_pipelines(self.pipelines)

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


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    print(sys.argv)

    window = MainWindow()
    window.show()
    window.launch_project_wizard()

    app.exec_()

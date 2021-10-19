import sys
from pathlib import Path
import json
import os

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from MainApplication_GUI import Ui_MainWindow
from Pipeline import Pipeline
from assetManager import AssetManager
from projectWizard import ProjectWizard


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_MainWindow = Ui_MainWindow()
        self.ui_MainWindow.setupUi(self)

        # set up tabs
        self.pipeline_GUI = Pipeline(self.ui_MainWindow.pipelines_tab)
        self.ui_MainWindow.pipelines_tab.layout().addWidget(self.pipeline_GUI)

        self.assetManager = AssetManager(self.ui_MainWindow.assets_tab)
        self.ui_MainWindow.assets_tab.layout().addWidget(self.assetManager)

        self.project_name = ""
        self.project_dir = Path()
        self.levels = []

    def launch_project_wizard(self):
        project_wizard = ProjectWizard()
        project_wizard.setWindowModality(qtc.Qt.ApplicationModal)
        result = project_wizard.exec_()
        if result == 0:
            print("No Project dir set")
            return

        # If Existing Project is opened
        if project_wizard.open_existing_project:
            self.project_dir = Path(project_wizard.existing_project_file).parent
            self.load_project_info()
            self.assetManager.add_levels(self.levels)
            self.assetManager.set_project_dir(self.project_dir)
            self.assetManager.load_asset_list()
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

        # Create Level Folders
        for lvl in self.levels:
            path = self.project_dir / lvl
            path.mkdir(parents=True)
            print(path)

        self.save_project_info()

    # -------------
    # SERIALIZATION
    # -------------
    def save_project_info(self):
        path = self.project_dir / "projectInfo.gapaproj"
        if not path.exists():
            if not path.is_file():
                path.touch()
        with path.open("w", encoding="utf-8") as f:
            project_data = {"name": self.project_name, "levels": json.dumps(self.levels)}
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
            self.levels = json.loads(project_data["levels"])



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    print(sys.argv)

    window = MainWindow()
    window.show()
    window.launch_project_wizard()

    app.exec_()

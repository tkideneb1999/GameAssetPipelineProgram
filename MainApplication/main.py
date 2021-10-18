import sys
from pathlib import Path

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from MainApplication_GUI import Ui_MainWindow
from Pipeline import Pipeline
from assetManager import AssetManager
from projectWizard import ProjectWizard
from pipelineServer import ServerListeningThread


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

        # Check Data
        proj_name = project_wizard.get_project_name_data()
        proj_dir = Path(project_wizard.get_project_dir_data()) / self.project_name
        proj_lvls = project_wizard.get_levels_data()

        if not proj_dir.parents[0].exists():
            print("Current Project Dir is no a valid path. Restarting Wizard")
            self.launch_project_wizard()
            return

        # Check if Project Name is set
        if proj_name == "":
            print("No Project Name set. Restarting Wizard")
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

        # TODO: Create metadata file to find Project

    def launch_server_thread(self):
        self.server = ServerListeningThread()
        self.server.new_connection_signal.connect(self.on_new_client_connected)
        self.server.start()

    @qtc.pyqtSlot()
    def on_new_client_connected(self):
        new_server_index = len(self.server.connectionThreads - 1)
        print("New Client Connected")
        self.server.connectionThreads[new_server_index].msg_received_signal.connect(self.print_client_message)

    def print_client_message(self, msg):
        print(msg)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.launch_project_wizard()
    window.launch_server_thread()

    app.exec_()

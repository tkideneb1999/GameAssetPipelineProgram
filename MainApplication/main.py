import socket
import threading
import transmission

'''
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"


def handle_client(conn, addr):
    print(f"{addr} connected.")

    connected = True
    while connected:
        msg = transmission.receiveMessage(conn)
        if msg is None:
            continue
        if msg == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] {msg}")
    print("[CLIENT] Client Closed Connection")
    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen()
print(f"started Listening on {SERVER}")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=[conn, addr])
    thread.start()
'''

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from MainApplication_GUI import Ui_MainWindow
from Pipeline import Pipeline
from assetManager import AssetManager
from projectWizard import ProjectWizard
import sys


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

        # launch project setup wizard
        self.project_name = ""
        self.project_dir = ""
        self.levels = []

    def launch_project_wizard(self):
        project_wizard = ProjectWizard()
        project_wizard.setWindowModality(qtc.Qt.ApplicationModal)
        result = project_wizard.exec_()
        if result == 0:
            print("No Project dir set")
            return

        # set project data
        self.project_name = project_wizard.get_project_name_data()
        self.project_dir = project_wizard.get_project_dir_data()
        self.levels = project_wizard.get_levels_data()
        self.assetManager.add_levels(self.levels)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.launch_project_wizard()

    app.exec_()

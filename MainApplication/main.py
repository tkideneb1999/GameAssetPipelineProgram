
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
from MainApplication_GUI import Ui_MainWindow
from PipelineConfig_GUI import PipelineConfigGUI
from PipelineConfig_GUI import PipelineStepGUI
import sys


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_MainWindow = Ui_MainWindow()
        self.ui_MainWindow.setupUi(self)
        self.pipeline_GUI = PipelineConfigGUI(self.ui_MainWindow.pipelines_tab)
        self.ui_MainWindow.pipelines_tab.layout().addWidget(self.pipeline_GUI)



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()


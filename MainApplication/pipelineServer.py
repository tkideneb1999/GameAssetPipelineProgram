from PyQt5 import QtCore as qtc
import os
import socket
import transmission

HEADER = 64

FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

'''
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


class ServerListeningThread(qtc.QThread):

    new_connection_signal = qtc.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.connectionThreads = []


    def run(self):
        PORT = 5050
        SERVER = socket.gethostbyname(socket.gethostname())
        ADDR = (SERVER, PORT)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)

        server.listen()
        print(f"started Listening on {SERVER}")

        while True:
            connection, address = server.accept()
            self.connectionThreads.append(ServerConnectionThread(connection, address))

            # Emit Signal on new Connection
            self.new_connection_signal.emit()

            self.connectionThreads[len(self.connectionThreads) - 1].start()


class ServerConnectionThread(qtc.QThread):
    def __init__(self, connection, address, parent=None):
        super().__init__(parent)
        self.connection = connection
        self.address = address
        self.msg_received_signal = qtc.pyqtSignal(str)

    def run(self):
        connected = True
        while connected:
            msg = transmission.receive_message(self.connection)
            if msg is None:
                continue
            if msg == DISCONNECT_MSG:
                connected = False

            # Emit Signal with message
            self.msg_received_signal.emit(msg)

            print(f"[{self.address}] {msg}")
        print("[CLIENT] Client Closed Connection")
        self.connection.close()

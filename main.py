
import socket
import threading
import transmission

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

import socket

HEADER = 64
FORMAT = 'utf-8'


def send_message(message, sock):
    e_msg = message.encode(FORMAT)
    l_msg = len(message)
    h_msg = str(l_msg).encode(FORMAT)
    h_msg += b' ' * (HEADER - len(h_msg))
    sock.send(h_msg)
    sock.send(e_msg)
    print(f"[SENT] {message}")


def receive_message(connection):
    msg_length = connection.recv(HEADER).decode(FORMAT)
    if not msg_length:
        return None
    msg_length = int(msg_length)
    msg = connection.recv(msg_length).decode(FORMAT)
    return msg
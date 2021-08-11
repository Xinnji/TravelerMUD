"""
file: server.py
author: Jason Scott-Hakanson

Start a game server.

Bind the server socket, open a world file, and generate 3 threads: accept
client connections, receive messages from clients, and send responses to
clients.
"""
import socket
import threading

import game
import events

IP = socket.gethostbyname(socket.gethostname())
PORT = 60420
HEADER_LENGTH = 10
FORMAT = 'utf-8'
DISCONNECT_MSG = 'qq'

worldfile = 'world.json'
world = game.loadworld(worldfile)
clients = {}


def receive_message(sock):
    """Receive a message from the socket."""
    msg_len = sock.recv(HEADER_LENGTH).decode(FORMAT)
    if not msg_len:
        return False
    msg_len = int(msg_len)
    return sock.recv(msg_len).decode(FORMAT)


def send_message(sock, msg):
    """Send a message through the socket."""
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER_LENGTH - len(send_len))
    sock.send(send_len)
    sock.send(message)


def input_handler(sock, username):
    """Handle receiving input: client -> server."""
    while sock:
        message = receive_message(sock)
        if message:
            events.parse(clients[username], message)
            if message == DISCONNECT_MSG:
                break
    # Delete the defunct sock from the dictionary.
    del clients[username]


def output_handler(sock, username):
    """Handle sending output: server -> client."""
    newest_msg = 0
    while sock:
        if clients[username]:
            for msg in clients[username].messages[newest_msg:len(clients[
                                                                  username].messages)]:
                send_message(sock, msg)
                newest_msg += 1
    sock.close()


# Instantiate server sock
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind server sock to ip:port
server.bind((IP, PORT))
# Server listens
server.listen()
# Server is now listening
print(f'Listening on {IP}:{PORT}')

# Start threads
while True:
    # Connections thread #######################################################
    conn, addr = server.accept()
    username = receive_message(conn)

    print(f'{username} connected on {addr}')

    # Add the player to the clients dict and introduce them to the world
    clients.append({
        "name": username,
        "conn": conn,
        ""
    })
    for player in STARTINGROOM.players:
        player.messages.append('A traveler appears.')
    STARTINGROOM.players.append(clients[username])
    clients[username].messages.append(f'Welcome, {username}. Try typing help '
                                     f'for a '
                               f'list of commands.')
    clients[username].look(None)

    # Server send thread
    server_output = threading.Thread(
        target=output_handler,
        args=(conn, username)
    )
    server_output.start()

    # Server receive thread
    server_input = threading.Thread(
        target=input_handler,
        args=(conn, username)
    )
    server_input.start()


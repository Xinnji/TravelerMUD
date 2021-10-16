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


# Constants
IP = socket.gethostbyname(socket.gethostname())
PORT = 60420
HEADER_LENGTH = 10
FORMAT = 'utf-8'
DISCONNECT_MSG = 'qq'


# Functions
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


def input_handler(sock, login):
    """Handle receiving input: client -> server."""
    while sock:
        message = receive_message(sock)
        if message:
            events.parse(clients[login], message)
            if message == DISCONNECT_MSG:
                break
    # Delete the defunct sock from the dictionary.
    del clients[login]


def output_handler(sock, login):
    """Handle sending output: server -> client."""
    newest_msg = 0
    while sock:
        if clients[login]:
            for msg in clients[login].messages[newest_msg:len(clients[
                                                                  login].messages)]:
                send_message(sock, msg)
                newest_msg += 1
    sock.close()


# Server
# Instantiate server sock
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind server sock to ip:port
server.bind((IP, PORT))
# Server listens
server.listen()
# Server is now listening
print(f'Listening on {IP}:{PORT}')

# Game world
# File containing the starting world state
worldfile = 'world.json'
# Load the world into memory
world = game.loadworld(worldfile)
# Room players start in
startroom = "Crossroads"

# Client threading
clients = set()
# Main thread: accept new clients
while True:
    # Accept the connection, get client socket and ip address
    conn, addr = server.accept()
    # First client input is login name (see client.py)
    login = receive_message(conn)
    # Print connection to server
    print(login + " connected on " + addr)
    # Store new player in clients
    clients.add((login, conn, addr))
    # Notify players in the start room that a player connected
    for p in filter(lambda p: p["loc"] == startroom, world["players"]):
        p["msgs"].append('A traveler appears.')
    world["rooms"][startroom]["inv"].append(clients[login])
    clients[login]["msgs"].append(f'Welcome, {login}. Try typing help for a '
                                  f'list of commands.')
    # clients[login].look(None)

    # Output thread: server sends output to clients
    server_output = threading.Thread(
        target=output_handler,
        args=(conn, login)
    )
    server_output.start()

    # Input thread: server receives input from clients
    server_input = threading.Thread(
        target=input_handler,
        args=(conn, login)
    )
    server_input.start()


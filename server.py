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
# IP = socket.gethostbyname(socket.gethostname())
IP = "localhost"
PORT = 60420
HEADER_LENGTH = 10
FORMAT = "utf-8"
DISCONNECT_MSG = "qq"


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
    send_len += b" " * (HEADER_LENGTH - len(send_len))
    sock.send(send_len)
    sock.send(message)


def input_handler(sock, login):
    """Handle receiving input: server <- client."""
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
            for msg in clients[login].messages[newest_msg:len(clients[login].messages)]:
                send_message(sock, msg)
                newest_msg += 1
    sock.close()


# Server setup
# Instantiate server sock
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind server sock to ip:port
server.bind((IP, PORT))
# Server listens
server.listen()
# Server is now listening
print(f"Listening on {IP}:{PORT}")


# Game world
# File containing the starting world state
worldfile = "world.json"
# Load the world into memory
world = game.loadworld(worldfile)
# Room players start in
startroom = "Crossroads"


# Accept new clients
clients = set()
while True:
    # Accept the connection, get client socket and ip address
    conn, addr = server.accept()

    # Client login
    while True:
        # Receive login from client
        login = receive_message(conn)
        if login:
            # Send response to client
            if filter(lambda p: p["login"] == login, world["players"]):
                # If the character already exists, send good
                send_message(conn, "good")
                new_char = False
            else:
                # Otherwise a new character is to be created
                send_message(conn, "bad")
                new_char = True
            # Receive password from client
            passwd = receive_message(conn)
            if passwd:
                # Create new character if necessary
                if new_char:
                    world["players"].append(
                        {
                            "login": login,
                            "passwd": passwd,
                            "aliases": [],
                            "inv": []
                        }
                    )
                # Log in the player and send a response to the client
                send_message(conn, "good")

    # Print connection to server
    print(login + " connected on " + addr)
    # Store new player in clients
    clients.add((login, conn, addr))
    # Notify players in the start room that a player connected
    for p in filter(lambda p: p["loc"] == startroom, world["players"]):
        p["msgs"].append("A traveler appears.")
    world["rooms"][startroom]["inv"].append(clients[login])

    # Server threading
    # Input: server <- client
    server_input = threading.Thread(target=input_handler,
                                    args=(conn, login))
    server_input.start()

    # Output: server -> client
    server_output = threading.Thread(target=output_handler,
                                     args=(conn, login))
    server_output.start()


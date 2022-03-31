"""
file: server.py
author: Jason Scott-Hakanson

Methods for the travelermud server.
"""
import socket
import threading
import game
import events


IP = "localhost"
PORT = 60420

ADDRESS = (IP, PORT)
HEADER_LENGTH = 10
FORMAT = "utf-8"

DISCONNECT_MSG = "qq"
DB = "world.db"


def recv_msg(con):
    """Receive a message from the socket."""
    msg_len = con.recv(HEADER_LENGTH).decode(FORMAT)
    if not msg_len:
        return False
    msg_len = int(msg_len)
    return con.recv(msg_len).decode(FORMAT)


def send_msg(con, _msg):
    """Send a message through the socket."""
    msg = _msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b" " * (HEADER_LENGTH - len(send_len))
    con.send(send_len)
    con.send(msg)


# def handle_in(con, username):
#     """Receive messages from clients."""
#     while con:
#         message = recv_msg(con)
#         if message:
#             events.parse(clients[login], message)
#             if message == DISCONNECT_MSG:
#                 break
#     con.close()


# def handle_out(con, username):
#     """Send messages to clients."""
#     newest_msg = 0
#     while con:
#         if clients[login]:
#             for msg in clients[login].messages[newest_msg:len(clients[login].messages)]:
#                 send_msg(con, msg)
#                 newest_msg += 1


def server_start():
    """Start a travelermud server."""
    # Create server socket and listen for connections
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen()
    print(f"Listening on {IP}:{PORT}")

    # Create game object
    game = Game(DB)

    # Create list of clients
    clients = {}

    # Accept new clients
    while True:
        # Accept the connection
        con, addr = server.accept()

        # Login the client
        try:
            username = recv_msg(con)
            if game.query(f"""select * from Player
                              where username={username};"""):
                send_msg("username good")
                password = recv_msg(con)
                if game.query(f"""select * from Player
                                  where username={username}
                                  and password={password};"""):
                    if username not in clients:
                        send_msg("password good")
                        game.login(username, password)
                    else:
                        send_msg("duplicate")
                        raise Exception("Username already logged in.")
                else:
                    send_msg("password bad")
                    raise Exception("Incorrect password for that username.")
            else:
                send_msg("username bad")

        print(username + " connected on " + addr) # Client connected to server

        # Store new player in clients
        clients[username] = (con, addr)

        # Notify players in the start room that a player connected
        for p in filter(lambda p: p["loc"] == startroom, world["players"]):
            p["msgs"].append("A traveler arrives.")
        world["rooms"][startroom]["inv"].append(clients[login])

        # Receive messages from clients
        server_in = threading.Thread(target=handle_in, args=(con, login))
        server_in.start()

        # Send messages to clients
        server_out = threading.Thread(target=handle_out, args=(con, login))
        server_out.start()

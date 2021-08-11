"""
file: events.py
author: Jason Scott-Hakanson
"""
import socket
import threading

IP = '128.193.251.127'
PORT = 60420
HEADER_LENGTH = 10
FORMAT = 'utf-8'


def send_message(sock, msg):
    """Send a message through the socket."""
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER_LENGTH - len(send_len))
    sock.send(send_len)
    sock.send(message)


def receive_message(sock):
    """Receive a message from the socket."""
    msg_len = sock.recv(HEADER_LENGTH).decode(FORMAT)
    if not msg_len:
        return False
    msg_len = int(msg_len)
    return sock.recv(msg_len).decode(FORMAT)


def input_handler(sock, username):
    """Handle receiving input: client -> server."""
    while sock:
        msg = input()
        if msg:
            send_message(sock, msg)
    print("The input stream ended.")


################################################################
# Run the application.
################################################################
# Setup client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

# Get a username
while True:
    username = input('Enter your username: ')
    if username:
        break

# Send username to server
send_message(client, username)

# Input thread: client -> server
input_thread = threading.Thread(target=input_handler,
                                args=(client, username))
input_thread.start()

# Output thread: server -> client
while client:
    message = receive_message(client)
    # Handle client output.
    if message:
        print(message)

# If the server closes the client will disconnect. Inform the user of this.
print("The output stream ended.")

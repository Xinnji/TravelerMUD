"""
file: events.py
author: Jason Scott-Hakanson
"""
import socket
import threading


# Constants
IP = "localhost"
PORT = 60420
HEADER_LENGTH = 10
FORMAT = "utf-8"


# Functions
def send_message(sock, msg):
    """Send a message through the socket."""
    enc_msg = msg.encode(FORMAT)
    msg_len = len(enc_msg)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b" " * (HEADER_LENGTH - len(send_len))
    sock.send(send_len)
    sock.send(enc_msg)


def receive_message(sock):
    """Receive a message from the socket."""
    msg_len = sock.recv(HEADER_LENGTH).decode(FORMAT)
    if not msg_len:
        return False
    msg_len = int(msg_len)
    return sock.recv(msg_len).decode(FORMAT)


def output_handler(sock):
    """Handle sending output: client -> server."""
    while sock:
        msg = input()
        if msg:
            send_message(sock, msg)
    print("The input stream ended.")


# Client setup
# Instantiate client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to a server
client.connect((IP, PORT))


# Client login
while True:
    # Get login from client
    login = input("Enter character login: ")
    # Send login to server
    send_message(client, login)
    # Get response back from server (see server.py)
    recv = receive_message(client)
    # Server checks whether the character exists
    if recv == "good":
        # If so
        passwd = input("Character found.\n"
                       "Enter character password: ")
    else:
        # If not
        passwd = input("Character not found."
                       "Create a password for your new character: ")
    # Send the password to the server
    send_message(client, passwd)
    # Get response back from server
    recv = receive_message(client)
    # Check if player was successfully logged in
    if recv == "good":
        # If so, welcome them and continue to threading
        print("Welcome, traveler. Try typing help for a list of commands.")
        break
    # If not, let them know and try to log in again.
    print("Something went wrong during login. Your login/password combination "
          "may not have been correct.")

# Client threading
# Output: client -> server
client_output = threading.Thread(target=output_handler,
                                 args=(client, login))
client_output.start()

# Input: client <- server
while client:
    message = receive_message(client)
    # Handle client output
    if message:
        print(message)

# If the server closes, inform the user
print("The output stream ended.")
# Stop the input thread
client_output.join()
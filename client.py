################################################################
# Constants & imports.
################################################################
import socket
import threading

IP = 'localhost'
PORT = 60420
HEADER_LENGTH = 10
FORMAT = 'utf-8'


################################################################
# Send a message.
################################################################
def send_message(socket, msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER_LENGTH - len(send_len))
    socket.send(send_len)
    socket.send(message)


################################################################
# Receive a message.
################################################################
def receive_message(socket):
    msg_len = socket.recv(HEADER_LENGTH).decode(FORMAT)
    if not msg_len:
        return False
    msg_len = int(msg_len)
    return socket.recv(msg_len).decode(FORMAT)


################################################################
# Handle client input.
################################################################
def input_handler(socket, username):
    while socket:
        msg = input()
        if msg:
            send_message(socket, msg)
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

# Threading
send_message(client, username)

# Client sending thread
input_thread = threading.Thread(
    target=input_handler,
    args=(client, username)
)
input_thread.start()

# Client receiving thread
while client:
    message = receive_message(client)
    # Handle client output.
    if message:
        print(message)

# If the server closes the client will disconnect. Inform the user of this.
print("The output stream ended.")

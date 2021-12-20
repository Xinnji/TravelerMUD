################################################################
# Constants, imports, and global variables.
################################################################
import socket
import threading
import travelermud

# IP = socket.gethostbyname(socket.gethostname())
IP = 'localhost'
PORT = 60420
HEADER_LENGTH = 10
FORMAT = 'utf-8'
DISCONNECT_MSG = 'qq'

clients = {}


################################################################
# Create some rooms for the world (temporary)
################################################################
hub = travelermud.Room("THE CROSSROADS", "Welcome to the crossroads, the place all travelers find themselves. Here, in the center of a clearing a camp fire crackles quietly. Next to the fire lies a fallen log. The dense, dark forest crowds in on all sides. Two foot paths intersect at the clearing, one leading through the forest north-south, the other east-west. The night sky is scattered with countles bright stars that twinkle, forming unknown constelations. The fire's warmth gives you comfort. Feel free to talk to the other travelers whom pass through while you are here.", {})
north = travelermud.Room("NORTH ROOM", "This is the room to the north of the crossroads. It is bitingly cold here. The wind howls unceasingly across the wasted plane, tearing at your clothes.", {'south': hub})
east = travelermud.Room("EAST ROOM", "This is the east room. A wide river can be seen here running north-south. Its waters are a deep blue.", {'west': hub})
south = travelermud.Room("SOUTH ROOM", "This is the room to the south of the crossroads. It is searing hot. Fires burn all around you. Sweat begins to bead on your forehead.", {'north': hub})
west = travelermud.Room("WEST ROOM", "This is the west room. Here, a rugged cliff rises suddenly from the ground to tower high above.", {'east': hub})
sky = travelermud.Room("THE SKY", "You weel freely through the air, high above the ground. Far below you see the smoke from the campfire in the crossroads.", {'down': hub})


################################################################
# Connect the rooms together (temporary)
################################################################
hub.exits['north'] = north
hub.exits['east'] = east
hub.exits['south'] = south
hub.exits['west'] = west
hub.exits['up'] = sky

# Starting room constant
STARTINGROOM = hub


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
# Handle server input.
################################################################
def input_handler(socket, username):
    while socket:
        message = receive_message(socket)
        if message:
            travelermud.parse(clients[username], message)
            if message == DISCONNECT_MSG:
                break

    # Delete the defunct socket from the dictionary.
    print(clients[username])
    del clients[username]
    # Push a disconnect message to all clients' inboxes.
    for client in clients:
        clients[client].messages.append(f'{username} has departed.')


################################################################
# Handle server output.
################################################################
def output_handler(socket, username):
    newest_msg = 0
    while socket:
        if clients[username]:
            for msg in clients[username].messages[newest_msg:len(clients[username].messages)]:
                send_message(socket, msg)
                newest_msg += 1
    socket.close()


################################################################
# Run the application.
################################################################
# Setup server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((IP, PORT))
server.listen()

print(f'Listening on {IP}:{PORT}')


################################################################
# Threading
################################################################
while True:
    # Connections thread
    conn, addr = server.accept()
    username = receive_message(conn)
    print(f'{username} connected on {addr}')

    # Add the player to the clients dict and introduce them to the world
    clients[username] = travelermud.Player(name=username, curr_room=STARTINGROOM)
    for player in STARTINGROOM.players:
        player.messages.append('A traveler appears.')
    STARTINGROOM.players.append(clients[username])
    clients[username].messages.append(f'Welcome, {username}. Try typing help for a list of commands.')
    clients[username].look(None)

    # Server sending thread
    server_output = threading.Thread(
        target=output_handler,
        args=(conn, username)
    )
    server_output.start()

    # Server receiving thread
    server_input = threading.Thread(
        target=input_handler,
        args=(conn, username)
    )
    server_input.start()

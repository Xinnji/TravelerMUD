"""
file: game.py
author: Jason Scott-Hakanson

Start the game world.

Load in the game world from a JSON "world file." Initialize a list for
saving clients' sockets and message history.
"""
from json import dumps, loads


def loadworld(file):
    """Load a static world file into a dict."""
    world = open(file, "r").read()
    return loads(world)


def saveworld(file, w_dict):
    """Save an active world dict into a JSON world file."""
    with open(file, 'w') as file:
        file.write(dumps(w_dict))


def handlemobs(mob):
    """Execute the events for each mob in the world in sequence."""



# Keep a dictionary of registered characters in the world file. This is the
# database for all player characters that have been created. When a player
# connects to the game, they are asked to log in. If the username they choose
# does not exist, it is added as a new character to the registry. Either way,
# they also enter a password for the character, and then are placed into the
# world as an online player. Their messages are stored in the online player
# area of the dict, and only their names are stored in their current rooms.
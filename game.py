"""
file: game.py
author: Jason Scott-Hakanson

Start the game world.

Load in the game world from a JSON "world file." Initialize a list for
saving clients' sockets and message history.
"""
from json import dumps, loads


def loadworld(self, file):
    """Load a static world file into a dict."""
    world = open(file, "r").read()
    return loads(world)


def saveworld(self, file, w_dict):
    """Save an active world dict into a JSON world file."""
    with open(file, 'w') as file:
        file.write(dumps(w_dict))

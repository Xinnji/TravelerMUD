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

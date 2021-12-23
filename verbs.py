"""
file: verbs.py
author: Jason Scott-Hakanson

In game commands.

Arguments:
playerid -- the unique identifier of the player
args -- argument string to be parsed by the verb

Commands that can be executed by the user as a player. Largely return
messages to be appended to the user's message box and sent to the client. Many
also change the player or world in some way before doing so.
"""


def go(playerid, args):
    """Change the player's location to a connected room."""


def look(playerid, args):
    """Print the description of the player's location, or an entity."""


def do(playerid, args):
    """Display an emoted message to all entities in the same room."""


def say(playerid, args):
    """Display a text message to all entities in the same room."""


def cast(playerid, args):
    """Allows a player of sufficient power to cast magical spells."""

"""
file: verbs.py
author: Jason Scott-Hakanson

In game commands.

Arguments:
id -- the unique identifier of the player
args -- argument string to be parsed by the verb

Commands that can be executed by the user as a player. Largely return
messages to be appended to the user's message box and sent to the client. Many
also edit the world file in some way before doing so.
"""


def go(id, args):
    """Move the player from a room to an adjacent one."""

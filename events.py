"""
file: events.py
author: Jason Scott-Hakanson

Function definitions for game events.

Events consist of all the methods that might occur in the game, whether
invoked by actors, objects, rooms, or anything else.
"""
import verbs


def parse(id, msg):
    """Player input event.

    Arguments:
    id -- the unique identifier of the player
    msg -- the input string to be parsed

    Split msg by whitespace. Call the corresponding verb from verbs.py,
    which will likely edit the world file in some way. Return a feedback
    message to the player.
    """
    verb, args = msg.split(maxsplit=1)

    try:
        return verbs.verb(id, args)
    except NameError:
        return f"That command could not be recognized."

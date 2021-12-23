"""
file: events.py
author: Jason Scott-Hakanson

Function definitions for game events.

Arguments:
entityid -- unique id of the entity being targeted by the event.

Events consist of all the methods that might occur in the game, whether
invoked by entities or rooms. Events are attached to entities in the database
by text and called in game in the same way verbs are called by parse.
"""
import verbs
import random


def parse(entityid, msg):
    """Player input event.

    Arguments:
    msg -- the input string to be parsed

    Split msg by whitespace. Call the corresponding verb from verbs.py,
    which will likely edit the worldfile in some way. Return a feedback
    message to the player.
    """
    verb, args = msg.split(" ", 1)

    try:
        return verbs.verb(entityid, args)
    except NameError:
        return random.choice(("What was that?",
                              "Excuse me?",
                              "I didn't catch that.",
                              "I don't understand."))


def burning(entityid):
    """You are on fire! Damage the entity by 1 stamina each second."""

"""
file: spells.py
author: Jason Scott-Hakanson

Magical spells used by the cast verb.

Arguments:
id -- the unique identifier of the player
args -- argument string to be parsed by the verb

A spell may only be used by an entity if their power level is equal or
greater than the power of the spell. Most spells tie an event to the targeted
entity, which then affects the entity until the event destroys itself.
"""


def unbeing(entityid, args):
    """Null an entity's location, effectively removing it from existence."""

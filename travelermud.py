###############################################################################
# Import statements
###############################################################################
from random import choice


###############################################################################
# Parse the message from the player to execute the command function.
###############################################################################
def parse(player, msg):
    global cmd_list
    cmd_list = {
        "help": (
            player.help,
            "Prints recognized verbs or help files for specified verbs. Uses: help | help <verb>"
        ),
        "name": (
            player.name,
            "Changes the player's name. Use: name <new name>"
        ),
        "describe": (
            player.describe,
            "Changes the player's description. Use: describe <new desc>"
        ),
        "look": (
            player.look,
            "Prints the description of the room and all players within, or of the specified player. Uses: look | look <name>"
        ),
        "say": (
            player.say,
            "Says something to all players in the room. Use: say <message>"
        ),
        "do": (
            player.do,
            "Emotes something to all players in the room. Use: do <action>"
        ),
        "go": (
            player.go,
            "Moves the player to the adjacent room in the specified direction, if it exists. Use: go <direction>"
        ),
        "alias": (
            player.alias,
            "Changes an alias. Aliases replace one string with another, allowing commands to be shortened. Uses: alias add <input> <replacement> | alias remove <input> | alias list"
        )
    }

    msg_split = msg.split(" ", 1)
    verb = msg_split[0].lower()
    args = msg_split[1] if len(msg_split) > 1 else None
    if verb in cmd_list:
        cmd_list[verb][0](args)
    else:
        player.messages.append(choice(("What was that?",
                                       "Excuse me?",
                                       "I didn't catch that.",
                                       "I don't understand.")))


###############################################################################
# Define the room class.
###############################################################################
class Room:
    def __init__(self, name="Unnamed Room", desc="This room has not been described.",exits={}):
        self.name = name
        self.desc = desc
        self.exits = exits
        self.players = []


###############################################################################
# Define the player class.
###############################################################################
class Player:
    def __init__(self, name="Stranger", desc="There is a nondescript stranger here.", room=None):
        self.name = name
        self.desc = desc
        self.room = room
        self.aliases = {}
        self.messages = []

###############################################################################
# Command function: Help the player by printing all the verbs.
###############################################################################
    def help(self, args):
        if args:
            # Print help doc of verb
            if args in cmd_list:
                self.messages.append(f"{args}: {cmd_list[args][1]}")
            else:
                self.messages.append(f"\"{args}\" is not a recognized verb.")
        else:
            # Print all possible verbs
            string = "Recognized verbs:\n"
            for verb in cmd_list:
                string = f"{string}    {verb}\n"
            self.messages.append(string)

###############################################################################
# Command function: Name the player.

# Hangs for some reason.
###############################################################################
    def name(self, args):
        if args:
            self.name = args
            self.messages.append(f"Your name is now \"{args}\".")
        else:
            self.messages.append("Verb name had no valid argument.")

###############################################################################
# Command function: Describe the player.
###############################################################################
    def describe(self, args):
        if args:
            self.desc = args
            self.messages.append(f"Your description is now \"{args}\".")
        else:
            self.messages.append("Verb describe had no valid argument.")

###############################################################################
# Command function: Look around the room.
###############################################################################
    def look(self, args):
        if args:
            # Look at player
            flag = False
            for player in self.room.players:
                if player.name.lower() == args.lower():
                    self.messages.append(player.desc)
                    flag = True
            if not flag:
                # No player found
                self.messages.append(f"There in nothing named \"{args}\" to look at.")
        else:
            # Look at room
            self.messages.append(f"\n{self.room.name}\n{self.room.desc}\n")
            for player in self.room.players:
                if player != self:
                    self.messages.append(player.desc)

###############################################################################
# Command function: Say something to the room.
###############################################################################
    def say(self, args):
        if args:
            for player in self.room.players:
                player.messages.append(f"{self.name} says \"{args}\"")
        else:
            self.messages.append("Verb say had no valid argument.")

###############################################################################
# Command function: Do something.
###############################################################################
    def do(self, args):
        if args:
            for player in self.room.players:
                player.messages.append(f"{self.name} {args}")
        else:
            self.messages.append("Verb do had no valid argument.")

###############################################################################
# Command function: Go to an adjacent room.
###############################################################################
    def go(self, args):
        if args:
            if args in self.room.exits:
                self.room.players.remove(self)
                for player in self.room.players:
                    player.messages.append(f"{self.name} travels {args}.")

                self.room = self.room.exits[args]

                for player in self.room.players:
                    player.messages.append(f"{self.name} walks in.")
                self.room.players.append(self)

                self.look(None)
            else:
                self.messages.append(f"You cannot go \"{args}\" from here.")
        else:
            self.messages.append("Verb go had no valid argument.")

###############################################################################
# Command function: Create or remove an alias.
###############################################################################
    def alias(self, args):
        if args:
            # add/edit or remove
            args = args.split(" ", 1)
            if args[0] == "list" and args[1] == "":
                string = "Aliases:\n"
                for arg in self.aliases:
                    string = f"{string}    {arg}: {arg[self.aliases]}\n"
                self.messages.append(string)
            elif args[0] == "remove":
                try:
                    del self.aliases[args[1]]
                    self.messages.append("Alias removed.")
                except KeyError:
                    self.messages.append("There was no alias by that name.")
            elif args[0] == "add" and args[1] != "":
                alias, text = args[1].split(" ", 1)
                if alias != "" and " " not in alias and text != "":
                    self.aliases[alias] = text
                    self.messages.append("Alias added.")
                else:
                    self.messages.append("Alias had an invalid name.")
            else:
                self.messages.append("Verb alias had invalid arguments (needs 1 to 3).")
        else:
            self.messages.append("Verb alias had no valid arguments.")

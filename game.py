"""
file: game.py
author: Jason Scott-Hakanson

Functions for starting, stopping and handling an instance of travelermud.
"""
import sqlite3


class Game:
    def __init__(self, db):
        """Load the SQLite database to be used for the game."""
        self.db = db
        with sqlite3.connect(self.db) as con:
            con.execute(
                """create table if not exists Room(
                id       integer not null unique primary key,
                name     text    not null,
                capacity integer not null default -1,
                event    text,
                desc     text    not null);""")
            con.execute(
                """create table if not exists Exit(
                exitid   integer not null,
                name     text    not null,
                enterid  integer not null,
                event    text,
                foreign key(enterid) references Room(id),
                foreign key(exitid)  references Room(id),
                unique(enterid, name));""")
            con.execute(
                """create table if not exists Entity(
                id       integer not null unique primary key,
                name     text    not null,
                stamina  integer,
                power    integer not null default 0,
                size     integer not null default 0,
                capacity integer not null default 0,
                location integer,
                event    text,
                intro    text    not null,
                desc     text    not null,
                foreign key(location) references Room(id));""")
            con.execute(
                """create table if not exists Player(
                id       integer not null unique primary key,
                username text    not null unique,
                password text    not null,
                name     text    not null,
                stamina  integer          default 20,
                power    integer not null default 0,
                size     integer not null default 20,
                capacity integer not null default 10,
                location integer,
                event    text             default "parse",
                intro    text    not null,
                desc     text    not null,
                foreign key(location) references Room(id));""")
        print(f"Loaded '{self.db}' successfully.")

    def query(self, body):
        """Execute a SQLite query on the loaded database."""
        with sqlite3.connect(self.db) as con:
            cur = con.execute(body)
        return cur

    def login(self, username, password):
        """Log clients into an existing character, or register a new one."""

    def logout(self, username, password):
        """Clean up a client that disconnects."""

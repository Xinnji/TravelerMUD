from game import *


# Instantiate a game object (sets up database if none found)
game = Game('world.db')

# Fill Room table with some example data
game.query('''insert into Room (name, desc) values ("Crossroads", "Welcome to the crossroads, the place all travelers find themselves. Here, in the center of a clearing a camp fire crackles quietly. Next to the fire lies a fallen log. The dense, dark forest crowds in on all sides. Two well-trod foot paths intersect at the clearing, one leading through the forest north-south, the other east-west. The night sky is scattered with countles bright stars that twinkle, forming unknown constelations. The fire's warmth gives you comfort. Feel free to talk to the other travelers whom pass through while you are here.");''')
game.query('''insert into Room (name, desc) values ("Wasteland", "This is the room to the north of the crossroads. It is bitingly cold here. The wind howls unceasingly across the wasted plane, tearing at your clothes.");''')
game.query('''insert into Room (name, desc) values ("River", "This is the east room. A wide river can be seen here running north-south. Its waters are a deep blue.");''')
game.query('''insert into Room (name, desc) values ("Burning Vale", "This is the room to the south of the crossroads. It is scorching hot. Fires burn all around you. Sweat begins to bead on your forehead.");''')
game.query('''insert into Room (name, desc) values ("Cliff Bottom", "This is the west room. Here, a rugged cliff rises suddenly from the ground to tower high above.");''')
game.query('''insert into Room (name, desc) values ("The Sky", "You weel freely through the air, high above the ground. Far below you see the smoke from the campfire in the crossroads.");''')
for row in game.query('''select * from Room;'''):
    print(row)

print()

# Fill Exit table with some example data
game.query('''insert into Exit (exitid, name, enterid) values (2, "north", 1);''')
game.query('''insert into Exit (exitid, name, enterid) values (3, "east", 1);''')
game.query('''insert into Exit (exitid, name, enterid) values (4, "south", 1);''')
game.query('''insert into Exit (exitid, name, enterid) values (5, "west", 1);''')
game.query('''insert into Exit (exitid, name, enterid) values (6, "up", 1);''')
game.query('''insert into Exit (exitid, name, enterid) values (1, "south", 2);''')
game.query('''insert into Exit (exitid, name, enterid) values (1, "west", 3);''')
game.query('''insert into Exit (exitid, name, enterid) values (1, "north", 4);''')
game.query('''insert into Exit (exitid, name, enterid) values (1, "east", 5);''')
game.query('''insert into Exit (exitid, name, enterid) values (1, "down", 6);''')
for row in game.query('''select
                            exitance.name,
                            Exit.name,
                            entrance.name
                         from Room as entrance
                         join Room as exitance on enterid = entrance.id
                         join Exit on exitid = exitance.id;'''):
    print(row[0], row[1], "from", row[2])

# Fill Entity table with some example data
game.query('''insert into Entity (name, desc) values ("Burning", "You are on Fire!", "burning 1");''')

# Infinitely take user input to interact with the database easily
while True:
    try:
        query = input(f"\nquery {game.worldfile}:  ")
        if query == "stop":
            break
        cur = list(game.query(query))
        print(len(cur), "rows found:")
        for row in cur:
            print("    ", row)
    except Exception as e:
        print(e)
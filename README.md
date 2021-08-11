# TravelerMUD
The skeleton for my very own Multi User Dimension.
## Files
- server.py - start a process that accepts client connections and opens a world json file.
- client.py - connect to a hosted server and take user input to direct player objects.
- game.py - stores game data. Function definitions for loading/saving the game, etc.
- verbs.py - function definitions for in-game player commands.
- events.py - function definitions for event functions (includes conditions, actor methods, etc.)
## Dev Tracker
### Out-of-game skeleton
- [ ] Static data for the world is stored in a database or JSON file format. This is just text 
  that needs to be 
  referenced for other things in the game so it doesn't need a class hierarchy.
- [ ] All methods for things in the world (conditions, entry effects, triggered events) are 
  coded as functions for an event class.
- [ ] Methods once coded are referenced from the JSON file/database for use in the game using 
  getattr, thus by text.
- [ ] A client connecting generates a new thread of the program, promps the user to log into a 
  character or create a new one with password, then logs them in with a player character.
### In-game features
#### Verbs
- [ ] go - move from one room to another connected one
- [ ] say - broadcast a message in your voice to everyone in the same room
- [ ] do - broadcast a message as an emote/action to everyone in the same room
- [ ] look - give the player the description of the thing they look at
- [ ] describe - change the long description of the player
- [ ] rename - change the short description of the player (from their own perspective).
- [ ] recognize - identify a player as the argument
- [ ] alias - add, remove, or give the player a list of their aliases. These are phrases that 
  are replaced in parsing
- [ ] god - create new game objects, including rooms, and edit their attributes. Essentially 
  edit the world file. Only available to ascendents.
- [ ] cast - invoke certain special events, like teleport, finger of death, fly, or invisibility.
  Only available to wizards.
#### Events
- [ ] parse - player input event
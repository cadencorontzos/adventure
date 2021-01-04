# File: AdvGame.py

"""
This module defines the AdvGame class, which records the information
necessary to play a game.
"""

###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# Unless you are implementing extensions, you won't need to add new       #
# public methods (i.e., methods called from other modules), but the       #
# amount of code you need to add is large enough that decomposing it      #
# into helper methods will be essential.                                  #
###########################################################################

from AdvRoom import AdvRoom
from tokenscanner import TokenScanner
from AdvObject import AdvObject

class AdvGame:

    def __init__(self,prefix,rooms):
        """Creates a new Adventure Game with the specified rooms"""
        self._rooms=rooms
        self._prefix = prefix
        self._playerInventory = set()
        self._objects= dict()
        self._synonyms = dict()
        try:
            with open(prefix+"Objects.txt") as f:
                while True:
                    obj = AdvObject.readObject(f)
                    if obj is None: break
                    name = obj.getName()
                    self._objects[name] = obj
        
        except IOError:
            pass
        try:
            with open(prefix+"Synonyms.txt") as f:
                while True:
                    
                    line=f.readline()
                    if line=="": break
                    line= line.split("=")
                    
                    self._synonyms[line[0]]= line[1][:-1]
                   
        
        except IOError:
            pass
        
        for key in self._objects:
            if self._objects[key].getInitialLocation() != "PLAYER":
                self._rooms[self._objects[key].getInitialLocation()].addObject(self._objects[key])
        
            else:
          
                self._playerInventory.add(self._objects[key])
    
    def getRoom(self, name):
        """Returns the room with the specified name."""
        return self._rooms[name]
    
    def isInInventory(self,name):
        if name==None: return None
        
        for obj in self._playerInventory:
            if obj.getName()== name:
                return True
            
        return False
    
    def getNextRoom(self, room,response):
        """Looks up the next room"""
        if response == "LOOK":
           return room.getName()
        for tup in room.getPassages():
            if tup[0] == response and self.isInInventory(tup[2]):
                return tup[1]
            elif tup[0] == response and tup[2] is None:
                return tup[1]
            

    def getInventory(self):
        if len(self._playerInventory) >= 1:
            print("You are carrying:")
            for obj in self._playerInventory:
                print("    "+ obj.getDescription())
        else:
            print("You are empty handed.")
          
    
    def Take(self,obj,room):
      
        if obj.getName() in room.getContents():
            room.removeObject(obj.getName())
            self._playerInventory.add(self._objects[obj.getName()])
            print("Taken.")
        else:
            print("I don't see that here.")
        
    def Drop(self,obj,room):
        if obj in self._playerInventory:
            
            self._playerInventory.remove(obj)
            room.addObject(obj)
            print("Dropped.")
        
    def run(self):
        """Steps through the rooms of the Adventure"""
        current = "START"
        revisiting= True
        loop=False
        while current != "EXIT":
            room = self.getRoom(current)
          
            newCurrent=None
   

            while room.getShortDescription()=="-":
           
                if room.getLongDescription() is not None:
                    for line in room.getLongDescription():
                        print(line)
                
                for passages in room.getPassages():
                    key= passages[2]
                    
                    nextRoom=passages[1]
                  
                    if key is None:
                        newCurrent=nextRoom
                        break
                    if self._objects[key] in self._playerInventory:
                        newCurrent=nextRoom
                        break
                if newCurrent=="EXIT":
                    current=newCurrent
                    break
                if newCurrent!=current:
                    current=newCurrent
                    room = self.getRoom(newCurrent)
            if newCurrent=="EXIT":
                continue

          
      
            if not room.hasBeenVisited() and room.getShortDescription()!="-":
                for line in room.getLongDescription():
                    print(line)
                for line in room.getObjectDescription():
                    print(line)
                room.setVisited()
            elif revisiting and not loop:
    
                print(room.getShortDescription())
                for line in room.getObjectDescription():
                    print(line)
            loop=False
            
            answer = input("> ").strip().upper()
      
            if self._synonyms.get(answer) is not None:
                answer= self._synonyms[answer]
           
            token = TokenScanner(answer)
            noneCalled=True
            while(token.hasMoreTokens()):
                
                command=token.nextToken()
                
                if command== "QUIT":
                    noneCalled=False
                    current = "EXIT"
                    
                if command== "LOOK":
                    for line in room.getLongDescription():
                        print(line)
                    for line in room.getObjectDescription():
                        print(line)
                    loop=True
                    noneCalled=False
                    break
                
                if command== "HELP":
                    for line in HELP_TEXT:
                        print(line)
                    noneCalled=False
                    
                if command == "DROP":
                    token.ignoreWhitespace()
                    s=token.nextToken()
                    if self._objects.get(s)!= None:
                        self.Drop(self._objects.get(s), room)
                    noneCalled=False
                        
                if command == "TAKE":
                    token.ignoreWhitespace()
                    s=token.nextToken()
                   
                    if self._objects.get(s) != None:
                        self.Take(self._objects.get(s), room)
                    else:
                        print("I don't see that here.")
                    noneCalled=False
                        
                if command == "INVENTORY":
                    noneCalled=False
                    self.getInventory()
                    
                

            
            next = self.getNextRoom(room, answer)
            if next is None:
                revisiting=False
                if noneCalled:
                    print("I don't understand that response.")
               
            else:
                
                revisiting=True
                current = next
# Constants
                
    @staticmethod
    def readAdventureGame(f,prefix):
        """Reads the entire game from the data file f."""
        rooms = { }
        while True:
            room = AdvRoom.readRoom(f)
            if room is None: break
            if len(rooms) == 0:
                rooms["START"] = room
            name = room.getName()
            rooms[name] = room
        return AdvGame(prefix,rooms)

HELP_TEXT = [
    "Welcome to Adventure!",
    "Somewhere nearby is Colossal Cave, where others have found fortunes in",
    "treasure and gold, though it is rumored that some who enter are never",
    "seen again.  Magic is said to work in the cave.  I will be your eyes",
    "and hands.  Direct me with natural English commands; I don't understand",
    "all of the English language, but I do a pretty good job.",
    "",
    "It's important to remember that cave passages turn a lot, and that",
    "leaving a room to the north does not guarantee entering the next from",
    "the south, although it often works out that way.  You'd best make",
    "yourself a map as you go along.",
    "",
    "Much of my vocabulary describes places and is used to move you there.",
    "To move, try words like IN, OUT, EAST, WEST, NORTH, SOUTH, UP, or DOWN.",
    "I also know about a number of objects hidden within the cave which you",
    "can TAKE or DROP.  To see what objects you're carrying, say INVENTORY.",
    "To reprint the detailed description of where you are, say LOOK.  If you",
    "want to end your adventure, say QUIT."
]

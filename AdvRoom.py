# File: AdvRoom.py

"""
This module is responsible for modeling a single room in Adventure.
"""

###########################################################################
# Your job in this milestone is to fill in the definitions of the         #
# methods listed in this file, along with any helper methods you need.    #
# The public methods shown in this file are the ones you need for         #
# Milestone #1.  You will need to add other public methods for later      #
# milestones, as described in the handout.  For Milestone #7, you will    #
# need to move the getNextRoom method into the AdvGame class and replace  #
# it with a getPassages method that returns the dictionary of passages.   #
###########################################################################

# Constants

MARKER = "-----"


class AdvRoom:

    def __init__(self, name, shortdesc, longdesc, passages):
        """Creates a new AdvRoom object with these attributes."""
        self._name = name
        self._shortdesc = shortdesc
        self._passages = passages
        self._longdesc= longdesc
        self._hasBeenVisited = False
        self._objects= set()

    def getName(self):
        """Returns the name of this room."""
        return self._name

    def getShortDescription(self):
        """Returns the list containing the Short Description of the room."""

        return self._shortdesc

    def setVisited(self):
        self._hasBeenVisited= not self._hasBeenVisited
        
        
    def hasBeenVisited(self):
        return self._hasBeenVisited
    
    def getObjectDescription(self):
        s=[]
     
        for obj in list(self._objects):
            s.append("There is a "+obj.getDescription()+ " here.")
        return s
    
    def getLongDescription(self):
        """Returns the list containing the long description of the room."""
    
            
        return self._longdesc
    
    def getPassages(self):
        return self._passages
                
        
    
    def addObject(self,obj):
        if obj.getInitialLocation() != "PLAYER":
            self._objects.add(obj)
        
    def removeObject(self, obj):
        for o in list(self._objects):
            if o.getName()==obj:
                old=o
        self._objects.remove(old)
       
        
        
    def containsObject(self,obj):
        check= set()
        check.add(obj)
        return check.issubset(self._objects)
    def getContents(self):
        names=set()
        for obj in self._objects:
            names.add(obj._name)
        return names
    @staticmethod
    def readRoom(f):
        """Reads one room from the data file f."""
        name = f.readline().rstrip()
        if name == "":
            return None
        shortDesc = f.readline().rstrip()
        text = [ ]
        
        while True:
            line = f.readline().rstrip()
            if line == MARKER: break
            text.append(line)
        passages = []
        while True:
            line = f.readline().rstrip()
            if line == "": break
            colon = line.find(":")
            if colon == -1:
                raise ValueError("Missing colon in " + line)
            response = line[:colon].strip().upper()
            next = line[colon + 1:].strip().split("/")
            if len(next) <2:
                next.append(None)
            passages.append((response,next[0],next[1]))

           
        return AdvRoom(name, shortDesc, text, passages)

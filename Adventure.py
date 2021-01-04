# File: Adventure.py
# ------------------
# This program plays the CSCI 121 Adventure game.

from AdvGame import AdvGame

# Constants

DATA_FILE_PREFIX = "Crowther"

# Main program

def Adventure():
    game= readAdventureFile()

    game.run()

def readAdventureFile():


    while True:
        try:
           
            with open(DATA_FILE_PREFIX + "Rooms.txt") as f:
                return AdvGame.readAdventureGame(f,DATA_FILE_PREFIX)
        except IOError:
            print("Please enter a valid prefix name.")


# Startup code

if __name__ == "__main__":
    Adventure()

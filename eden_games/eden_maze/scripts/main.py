# File name: main.py
# Developed by: Project Eden Development Team
# Date: 29/07/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2008 Funtrench PLC.            |
# |------------------------------------------------|
from EdenMaze import EdenMaze
# entry point for the Eden Maze
def main():
    """ main module for EdenMaze """
    # create the EdenMaze sample
    EdenEvolves = EdenMaze()
    # run the scene
    run()
if __name__ == "__main__":
    main()
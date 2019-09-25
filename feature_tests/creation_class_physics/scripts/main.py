# File name: main.py
# Developed by: Project Eden Development Team
# Date: 14/07/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from CreationTestPhysics import CreationTestPhysics
# entry point for the Creation client
def main():
    """ main module for any program """
    EdenEvolves = CreationTestPhysics()
    # run the scene
    base.run()
if __name__ == "__main__":
    main()
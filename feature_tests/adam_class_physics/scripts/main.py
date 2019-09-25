# File name: main.py
# Developed by: Project Eden Development Team
# Date: 29/07/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from AdamTestPhysics import AdamTestPhysics
# entry point for the Adam client
def main():
    """ main module for any program """
    # create the AdamTestPhysics sample
    EdenEvolves = AdamTestPhysics()
    # run the scene
    base.run()
if __name__ == "__main__":
    main()
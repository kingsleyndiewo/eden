# File name: main.py
# Developed by: Project Eden Development Team
# Date: 14/07/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from GenesisTest import GenesisTest
# entry point for the Genesis client
def main():
    """ main module for any program """
    # create the GenesisTest sample
    EdenEvolves = GenesisTest()
    # run the scene
    base.run()
if __name__ == "__main__":
    main()
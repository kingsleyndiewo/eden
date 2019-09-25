# File name: main.py
# Developed by: Project Eden Development Team
# Date: 28/05/2009
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from GenesisTestSpin import GenesisTestSpin
# entry point for the Genesis client
def main():
    """ main module for any program """
    # create the GenesisTest sample
    EdenEvolves = GenesisTestSpin()
    # run the scene
    base.run()
if __name__ == "__main__":
    main()
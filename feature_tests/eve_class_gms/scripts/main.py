# File name: main.py
# Developed by: Project Eden Development Team
# Date: 11/08/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from EveTestGMS import EveTestGMS
# entry point for the Eve client
def main():
    """ main module for any program """
    # create the EveTestGMS sample
    EdenEvolves = EveTestGMS()
    # run the scene
    base.run()
if __name__ == "__main__":
    main()
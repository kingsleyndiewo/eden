# File name: main.py
# Developed by: Project Eden Development Team
# Date: 01/06/2009
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from CheckerBoardTestAgent import CheckerBoardTestAgent
# entry point for the CheckerBoard client
def main():
    """ main module for any program """
    EdenEvolves = CheckerBoardTestAgent()
    # run the scene
    base.run()
if __name__ == "__main__":
    main()
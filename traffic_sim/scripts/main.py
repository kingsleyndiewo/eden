# File name: main.py
# Developed by: Nairobi Project Development Team
# Date: 10/11/2012
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2012 Intellect Alliance.            |
# |------------------------------------------------|
from TrafficSim import TrafficSim
# entry point for the Eve client
def main():
    """ main module for any program """
    # create the TrafficSim sample
    EdenEvolves = TrafficSim()
    # run the scene
    run()
if __name__ == "__main__":
    main()
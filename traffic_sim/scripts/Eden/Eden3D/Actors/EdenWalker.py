# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Actors]
# Desc: Actors Library - EdenWalker Class
# File name: EdenWalker.py
# Developed by: Project Eden Development Team
# Date: 04/07/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from Eden.Eden3D.Actors.EdenActor import EdenActor
# ---------------------------------------------
# A class to handle the walking action of an actor.
# Class definition for the EdenWalker class
# ---------------------------------------------
class EdenWalker(EdenActor):
    " The base class for all walking actors "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, actorDictionary, parentNode):
        # ancestral constructor
        EdenActor.__init__(self, actorDictionary, parentNode)
    # --------------------------MOTION-----------------------------
    def computeXY(self, frameInterval, modArgs = None):
        " computes steps in X and Y from heading "
        # utility function for moving actor
        # move 1 unit in a second; clockwise is positive heading
        if modArgs == None:
            # no modifier mode
            unitsForward = frameInterval * self.actorData['speed']
        else:
            # check the run variable
            if 'run_mode' in modArgs.keys():
                if modArgs['run'] == True:
                    t_s = self.actorData['speed'] + self.actorData['runSpeed']
                    unitsForward = frameInterval * t_s
                else:
                    unitsForward = frameInterval * self.actorData['speed']
            else:
                unitsForward = frameInterval * self.actorData['speed']
        steps2 = self.baseActor.getNetTransform().getMat().getRow3(1)
        steps2.setZ(0)
        steps2.normalize()
        unitsX = steps2.getX() * unitsForward
        unitsY = steps2.getY() * unitsForward
        return (unitsX, unitsY)
    def turnHeading(self, turnValue):
        " turns the actor either right or left "
        # left is positive
        self.baseActor.setH(self.baseActor.getH() + turnValue)


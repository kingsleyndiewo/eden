# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Actors]
# Desc: Actors Library - EdenAero Class
# File name: EdenAero.py
# Developed by: Project Eden Development Team
# Date: 04/07/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from Eden.Eden3D.Actors.EdenActor import EdenActor
# ---------------------------------------------
# A class to handle the flying action of an actor.
# Class definition for the EdenAero class
# ---------------------------------------------
class EdenAero(EdenActor):
    " The base class for all flying actors "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, actorDictionary, parentNode):
        # ancestral constructor
        EdenActor.__init__(self, actorDictionary, parentNode)
    # --------------------------MOTION-----------------------------
    def computeXY(self, frameInterval):
        " computes steps in X and Y from heading "
        # utility function for moving actor
        # move 1 unit in a second; clockwise is positive heading
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
    def turnPitch(self, turnValue):
        " turns the actor either up or down "
        # left is positive
        self.baseActor.setP(self.baseActor.getP() + turnValue)
    def turnRoll(self, turnValue):
        " turns the actor either clockwise or counterclockwise "
        # left is positive
        self.baseActor.setR(self.baseActor.getR() + turnValue)
    

# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.Pickers]
# Desc: Pickers Library - ActorPicker Class
# File name: ActorPicker.py
# Developed by: Project Eden Development Team
# Date: 29/07/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench Limited
# ---------------------------------------------
from Eden.EdenTools.Pickers.MousePicker import MousePicker
# ---------------------------------------------
# Class definition for the ActorPicker class
# ---------------------------------------------
class ActorPicker(MousePicker):
    " Extends MousePicker for 3D actor selection "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, worldClass, baseData): # constructor
        # get the bitmask
        t_bm = worldClass.geomBitMask
        MousePicker.__init__(self, t_bm, baseData['CNF']) # ancestral constructor
        # accept picking mouse event
        pickerButton = worldClass.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['pickerButton']
        worldClass.accept(pickerButton, self.actorSelector)
        # store these valuable pointers
        self.proxy = worldClass
        self.MWN = baseData['MWN']
        self.msgr = baseData['msgr']
        self.BCNF = baseData['BCNF']
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def actorSelector(self):
        " processes the mouse button avatar change event "
        # this gives up the screen coordinates of the mouse
        t_coord = self.MWN()
        # this makes the ray originate from the camera and its direction 
        # pointing to the screen coordinates of the mouse
        self.pickerRay.setFromLens(self.BCNF, t_coord.getX(), t_coord.getY())
        # run the traverser through the actors node to get collisions
        self.pickTrav.traverse(self.proxy.actorsNode)
        # the collision handler is a CollisionHandlerQueue; it lists all
        # the collisions that were detected during the most recent traversal
        if self.pickHandler.getNumEntries() > 0:
            # at least one collision occured; get the closest object
            self.pickHandler.sortEntries()
            pickedObject = self.pickHandler.getEntry(0).getIntoNodePath()
            # get the actor node containing the collided node
            pickedObject = pickedObject.findNetTag(self.proxy.pickerTag)
            if not pickedObject.isEmpty():
                # get the name of the selected actor
                t_s = pickedObject.getTag(self.proxy.pickerTag)
                # check whether the new actor is already our active avatar
                if  t_s != self.proxy.mainActor.baseActor.getTag(self.proxy.pickerTag):
                    # stop the actor animation for the current actor
                    self.proxy.idleSwitchedActor()
                    # change the actor
                    self.proxy.mainActor = self.proxy.actorStore[t_s]
                    # resolve animations again (just in case routine is different)
                    self.proxy.resolveAnimations()
                    # update actor camera position
                    self.proxy.updateActorCamera()
                    # send message
                    self.msgr('actor-switch')


        
        
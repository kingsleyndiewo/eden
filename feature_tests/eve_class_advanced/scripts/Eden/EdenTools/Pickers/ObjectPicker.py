# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.Pickers]
# Desc: Pickers Library - ObjectPicker Class
# File name: ObjectPicker.py
# Developed by: Project Eden Development Team
# Date: 29/05/2009
# Place: Nairobi, Kenya
# Copyright: (C)2009 Funtrench Limited
# ---------------------------------------------
from Eden.EdenTools.Pickers.MousePicker import MousePicker
# ---------------------------------------------
# Class definition for the ObjectPicker class
# ---------------------------------------------
class ObjectPicker(MousePicker):
    " Extends MousePicker for 3D object selection "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, worldClass, baseData): # constructor
        # get the bitmask
        t_bm = worldClass.geomBitMask
        MousePicker.__init__(self, t_bm, baseData['CNF']) # ancestral constructor
        # accept picking mouse event
        pickerButton = worldClass.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['pickerButton']
        worldClass.accept(pickerButton, self.objectSelector, [baseData['parentNode']])
        # store these valuable pointers
        self.proxy = worldClass
        self.triggerButton = pickerButton
        self.MWN = baseData['MWN']
        self.msgr = baseData['msgr']
        self.BCNF = baseData['BCNF']
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def objectSelector(self, parentNode):
        " processes the mouse button object select event "
        # this gives up the screen coordinates of the mouse
        t_coord = self.MWN()
        # this makes the ray originate from the camera and its direction 
        # pointing to the screen coordinates of the mouse
        self.pickerRay.setFromLens(self.BCNF, t_coord.getX(), t_coord.getY())
        # run the traverser through the parentNode to get collisions
        self.pickTrav.traverse(parentNode)
        # the collision handler is a CollisionHandlerQueue; it lists all
        # the collisions that were detected during the most recent traversal
        if self.pickHandler.getNumEntries() > 0:
            # at least one collision occured; get the closest object
            self.pickHandler.sortEntries()
            pickedObject = self.pickHandler.getEntry(0).getIntoNodePath()
            # get the object node containing the collided node
            pickedObject = pickedObject.findNetTag(self.proxy.pickerTag)
            if not pickedObject.isEmpty():
                # get the name of the selected object
                t_s = pickedObject.getTag(self.proxy.pickerTag)
                # check whether the new object is not our active object
                if  t_s != self.proxy.currentSelection:
                    # return the new selection
                    self.proxy.prevSelection = self.proxy.currentSelection
                    self.proxy.currentSelection = t_s
                    # send message
                    self.msgr('object-select')


        
        
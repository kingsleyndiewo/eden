# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.Pickers]
# Desc: Pickers Library - MousePicker Class
# File name: MousePicker.py
# Developed by: Project Eden Development Team
# Date: 29/07/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench PLC
# ---------------------------------------------
from pandac.PandaModules import *
# ---------------------------------------------
# Class definition for the MousePicker class
# ---------------------------------------------
class MousePicker:
    " Base class for all mouse pickers "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, geomBitMask, cameraPointer): # constructor
        # since we are using collision detection to do picking, we set
        # up the picker system conventionally with a traverser and a handler
        self.pickTrav = CollisionTraverser()
        self.pickHandler = CollisionHandlerQueue()
        # a collision node for our picker ray
        pickerNode = CollisionNode('pickerRay')
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        # attach that node to the camera since the ray will need to be positioned
        # relative to it
        self.pickerNode = cameraPointer(pickerNode)
        # set the FromCollideMask to match the actors' mask and zero the
        # IntoCollideMask because the ray can't be an into object
        self.pickerNode.node().setFromCollideMask(BitMask32.bit(geomBitMask))
        self.pickerNode.node().setIntoCollideMask(BitMask32.allOff())
        # add to traverser
        self.pickTrav.addCollider(self.pickerNode, self.pickHandler)
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    # Extended in child classes or manually

        
        
# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.Pickers]
# Desc: Pickers Library - ObjectMover Class
# File name: ObjectMover.py
# Developed by: Project Eden Development Team
# Date: 29/05/2009
# Place: Nairobi, Kenya
# Copyright: (C)2009 Funtrench Limited
# ---------------------------------------------
from Eden.EdenTools.Pickers.ObjectPicker import ObjectPicker
# ---------------------------------------------
# Class definition for the ObjectMover class
# ---------------------------------------------
class ObjectMover(ObjectPicker):
    " Extends ObjectPicker for 3D object moving "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, worldClass, baseData): # constructor
        ObjectPicker.__init__(self, worldClass, baseData) # ancestral constructor
        # accept stop moving mouse event
        t_mv = self.triggerButton + '-up'
        worldClass.accept(t_mv, self.objectStopper)
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def objectStopper(self):
        " stops the object from following mouse when the button is released "
        # send message
        self.msgr('object-released')

        
        
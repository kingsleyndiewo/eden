# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.SessionStudio]
# Desc: Session Studio Library - SessionBase Class 
# File name: SessionBase.py
# Developed by: Project Eden Development Team
# Date: 23/08/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench PLC
# ---------------------------------------------
from panda3d.core import *
# ---------------------------------------------
# Class definition for the SessionBase class
class SessionBase:
    " Base class for all session recorders/players "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, mouseWatcherNode): # constructor
        # make the session recorder
        self.sessionRecorder = RecorderController()
        # save the mouse watcher node
        self.MWN = mouseWatcherNode
        # save the mouse watcher node parent
        self.mwnParent = mouseWatcherNode.getParent()
        # add the default recorders
        self.addDefaultRecorders()
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    # -----------------------------------------------------------------------
    # ---------------------------RECORDER FUNCTIONS--------------------------
    def addDefaultRecorders(self):
        " adds recorders to sessionRecorder for capturing input "
        # we create a mouse recorder to capture inputs
        t_mr = MouseRecorder('edenMouse')
        # we add the mouse recorder to our session recorder
        self.sessionRecorder.addRecorder('edenMouse', t_mr.upcastToRecorderBase())
        # we attach the mouse recorder to the mouse watcher parent
        t_np = self.mwnParent.attachNewNode(t_mr)
        # we finally reparent the mouse watcher node to our mouse recorder
        self.MWN.reparentTo(t_np)
    # The rest is implemented in child classes
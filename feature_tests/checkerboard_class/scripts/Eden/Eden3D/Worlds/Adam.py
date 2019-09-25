# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Worlds]
# Desc: Worlds Library - Adam Class
# File name: Adam.py
# Developed by: Project Eden Development Team
# Date: 28/07/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench Limited
# ---------------------------------------------
from Eden.Eden3D.Worlds.Genesis import Genesis
# ---------------------------------------------
# A class that implements a basic world with one
# main actor in it. Entry point for a full 3D game.
# Startup options are loaded from config.xml
# Class definition for the Adam class
# ---------------------------------------------
class Adam(Genesis):
    " Extends Genesis class for actor-centred 3D worlds "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, remoteStarterTask = None, customPRC = None, edenClass = 'Adam'):
        Genesis.__init__(self, remoteStarterTask, customPRC, edenClass) # ancestral constructor
        # get actor details XML
        actorDetails = self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['mainActor']
        # load the main actor
        t_i = self.loadActor(actorDetails)
        self.mainActor = self.actorStore[t_i]
        self.mainActor.baseActor.setTag('Animated', 'False')
        # set up collision detection for mainActor
        self.setupActorCollision(t_i)
        self.camPos = self.mainActor.actorData['camPosition']
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    
    # ------------------SYSTEM SERVICES-------------------
    # ----------------------------------------------------
    
    # ------------------TASKS-----------------------------
    # ----------------------------------------------------
    
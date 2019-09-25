# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Worlds]
# Desc: Worlds Library - Eve Class
# File name: Eve.py
# Developed by: Project Eden Development Team
# Date: 29/07/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from Eden.Eden3D.Worlds.Genesis import Genesis
from Eden.EdenTools.Pickers.ActorPicker import ActorPicker
# ---------------------------------------------
# A class that implements a basic world with one
# variable main actor in it. Entry point for a full
# 3D game. Active avatar is selected via mouse click.
# Startup options are loaded from config.xml
# Class definition for the Eve class
# ---------------------------------------------
class Eve(Genesis):
    " Extends Genesis class for actor-centred 3D worlds "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, remoteStarterTask = None, ignorePicker = False, \
            customPRC = None, edenClass = 'Eve'):
        Genesis.__init__(self, remoteStarterTask, customPRC, edenClass) # ancestral constructor
        # get activatable actors list
        self.XPU.getSectionValues('subsection','Actors')
        actorList = self.XPU.Parser['XML_Values']['Actors_Values']
        # initialize picker tag
        self.pickerTag = 'Candidate'
        # get initial avatar
        initActor = self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['initialActor']
        for t_a in actorList.values():
            # load the actor
            t_i = self.loadActor(t_a)
            # set tag information
            self.actorStore[t_i].baseActor.setTag('Animated', 'False')
            self.actorStore[t_i].baseActor.setTag(self.pickerTag, t_i)
            # set up collision detection for the actor
            self.setupActorCollision(t_i)
            if t_i == initActor:
                # set the initial avatar
                self.mainActor = self.actorStore[t_i]
        self.updateActorCamera()
        if ignorePicker == False:
            # setup picker system
            # we have to give ActorPicker direct access to local data and methods
            # to avoid crowding Eve.
            # TODO: Find a more secure way to implement this
            t_d = {'CNF':base.camera.attachNewNode, \
                'MWN':base.mouseWatcherNode.getMouse, 'msgr':messenger.send, \
                'BCNF':base.camNode}
            self.avatarPicker = ActorPicker(self, t_d)
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    def idleSwitchedActor(self):
        " stops animation for the main actor before switching "
        self.mainActor.stopAnimation()
        self.mainActor.baseActor.pose(self.anime, self.mainActor.actorData['pose'])
        self.mainActor.baseActor.setTag('Animated', 'False')
    # ------------------SYSTEM SERVICES-----------------
    # ----------------------------------------------------
    def updateActorCamera(self):
        " updates camera position when avatar changes "
        self.camPos = self.mainActor.actorData['camPosition']
        # camera follows mainActor
        base.camera.setPos(self.mainActor.baseActor.getX() + self.camPos[0], \
            self.mainActor.baseActor.getY() + self.camPos[1], \
            self.mainActor.baseActor.getZ() + self.camPos[2])
        base.camera.lookAt(self.mainActor.baseActor)
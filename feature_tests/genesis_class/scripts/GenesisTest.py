# Package Description: Funtrench's Eden Software Development Kit
# Name: Eden Feature Tests SDK
# Desc: Test Project for the Genesis Class
# File name: GenesisTest.py
# Developed by: Project Eden Development Team
# Date: 14/07/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from Eden.Eden3D.Worlds.Genesis import Genesis
from Eden.Eden2D.Text2D import Text2D
from direct.task import Task
from panda3d.core import Point3
from direct.interval.IntervalGlobal import *
# --------------------------------------------------
# A class to demonstrate the features of the Genesis
# Class.
# Class definition for the GenesisTest class
# --------------------------------------------------
class GenesisTest(Genesis):
    " Extending the Genesis class for an actor in basic world "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        Genesis.__init__(self, self.starterTask) # ancestral constructor
        t_f = [('arial.egg', 'Arial')]
        self.textPlay = Text2D(self.edenVisuals.fpsValue, t_f)
        # load Eve, and loop her animation. We will demonstrate an
        # actor with lerp intervals. The camera will still be under
        # mouse control for this one.
        self.loadActor('Eve.xml')
        self.ladyEve = self.actorStore['Eve']
        # set up collision detection for Eve (Eve can collide with geometry)
        self.setupActorCollision(self.ladyEve.actorData['name'])
        self.ladyEve.loopAnimation('run')
        # load other objects (the ViS Cube)
        self.loadGeometry('cube', 'cube', (0.25,0.25,0.25), (0,0,5))
        # load the text resources
        self.textKeys = ['title', 'instruction1', 'instruction2', 'instruction3', \
          'instruction4', 'instruction5', 'instruction6', 'instruction7']
        # compute the text positions
        self.textPositions = []
        for t_p in range(8):
            t_j = ( -1.30, 0, 0.95 - (t_p * 0.05) )
            self.textPositions.append(t_j)
        # title
        self.textPlay.loadTextLine('Genesis Test. Powered by Funtrench', \
          self.textKeys[0])
        # instructions
        self.textPlay.loadTextLine('Press ESCAPE to quit', self.textKeys[1])
        t_i = 'LMB: Move camera X-Z, RMB: Move camera Y, MMB: Camera Orientation'
        self.textPlay.loadTextLine(t_i, self.textKeys[2])
        self.textPlay.loadTextLine('F/B: Increment/Decrement cube X', self.textKeys[3])
        self.textPlay.loadTextLine('G/H: Increment/Decrement cube Y', self.textKeys[4])
        self.textPlay.loadTextLine('A/J: Increment/Decrement cube Z', self.textKeys[5])
        self.textPlay.loadTextLine('I: Show game information', self.textKeys[6])
        self.textPlay.loadTextLine('D: Show documentation', self.textKeys[7])
        # game info
        self.textPlay.loadTextLine(self.gameID, 'Game')
        # manual text
        t_n =  self.gameMVC.mvcStructure['tier_resource']['text'] + '/GenesisTest.txt'
        self.textPlay.loadTextFile(t_n, 'Doc')
        # create the four lerp intervals needed to walk Eve back and forth
        self.ladyEvePosInterval1= self.ladyEve.baseActor.posInterval(7,Point3(0,-15,0), \
            startPos=Point3(0,10,0))
        self.ladyEvePosInterval2= self.ladyEve.baseActor.posInterval(7,Point3(0,10,0), \
            startPos=Point3(0,-15,0))
        self.ladyEveHprInterval1= self.ladyEve.baseActor.hprInterval(3,Point3(180,0,0), \
            startHpr=Point3(0,0,0))
        self.ladyEveHprInterval2= self.ladyEve.baseActor.hprInterval(3,Point3(0,0,0), \
            startHpr=Point3(180,0,0))
        # create and play the sequence that coordinates the intervals
        self.ladyEvePace = Sequence(self.ladyEvePosInterval1, self.ladyEveHprInterval1, \
        self.ladyEvePosInterval2, self.ladyEveHprInterval2, name = "ladyEvePace")
        self.ladyEvePace.loop()
        # setup key bindings
        self.accept("f", self.cubeAlter, [+1, "X"])
        self.accept("b", self.cubeAlter, [-1, "X"] )
        self.accept("g", self.cubeAlter, [+1, "Y"] )
        self.accept("h", self.cubeAlter, [-1, "Y"] )
        self.accept("a", self.cubeAlter, [+1, "Z"] )
        self.accept("j", self.cubeAlter, [-1, "Z"] )
        self.accept("s", self.screenCapture, ['../Genesis_'])
        self.accept("d", self.textPlay.displayText, ['Doc', 30, (-1.00,0,0.35), False])
        self.accept("i", self.textPlay.displayText, ['Game', 30, (0.20,0,0.95), False])
        self.accept("c", self.textPlay.clearScreen)
    # ------------------BEHAVIORS-------------------------
    # ----------------------------------------------------
    def cubeAlter(self, valueChange, valueType):
        " alters co-ordinate position of cube "
        if valueType == "X":
            self.objectStore['cube'][0].setX(self.objectStore['cube'][0].getX() + \
                valueChange)
        elif valueType == "Y":
            self.objectStore['cube'][0].setY(self.objectStore['cube'][0].getY() + \
                valueChange)
        elif valueType == "Z":
            self.objectStore['cube'][0].setZ(self.objectStore['cube'][0].getZ() + \
                valueChange)
    # ------------------TASKS-----------------------------
    # ----------------------------------------------------
    def starterTask(self, task):
        " task to handle the startup "
        if task.time == 0.0:
            if self.worldData['showMouse'] != 0:
                self.toggleMouseCursor()
            # if sound is at startup then play
            if self.mediaFlag[1] == True and self.worldData['playAfter'] == 0:
                self.gameMusic.setLoop(True)
                self.gameMusic.play()
            if self.mediaFlag[0] == True:
                # show the screens with the n-second delay
                self.edenVisuals.sequenceAllImages(self.visualDelay)
            return task.cont
        else:
            if self.edenVisuals.virginFlag == True:
                # show text
                self.textPlay.displayTextCluster(self.textKeys, self.textPositions)
                if self.worldData['showMouse'] != 0:
                    self.toggleMouseCursor()
                return task.done
            else:
                # all other frames
                return task.cont
    

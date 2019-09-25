# Package Description: Funtrench's Eden Software Development Kit
# Name: Eden Feature Tests SDK
# Desc: PandaAI Test Project for the Genesis Class
# File name: GenesisTestAI.py
# Developed by: Project Eden Development Team
# Date: 22/07/2008
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
# Class with unmoused camera.
# Class definition for the GenesisTestAdvanced class
# --------------------------------------------------
class GenesisTestAI(Genesis):
    " Extending the Genesis class for an actor in AI world "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        Genesis.__init__(self, self.starterTask, initAI = True) # ancestral constructor
        t_f = [('arial.egg', 'Arial')]
        self.textPlay = Text2D(self.edenVisuals.fpsValue, t_f)
        # load Eve, and loop her animation. The camera will follow the actor
        self.loadActor('Eve.xml')
        self.ladyEve = self.actorStore['Eve']
        # set up collision detection for Eve (Eve will collide with geometry)
        self.setupActorCollision(self.ladyEve.actorData['name'])
        # create AI actor
        self.smartEve = self.createAiCharacter('smartEve', self.ladyEve.baseActor, 200.0, 0.1, 30)
        self.ladyEve.loopAnimation('run')
        # add a camera task to the task manager
        self.camPos = self.ladyEve.actorData['camPosition']
        taskMgr.add(self.genesisCameraTask, 'cameraTask')
        # load other objects
        self.loadGeometry('cube', 'cube', (0.25,0.25,0.25), (0,0,0))
        self.loadGeometry('gazebo', 'gazebo', (0.75,0.75,0.75), (-8,28,0))
        # set obstacles
        self.smartEden.addObstacle(self.objectStore['cube'][0])
        self.smartEden.addObstacle(self.objectStore['gazebo'][0])
        # set obstacle avoidance
        self.smartEve[1].obstacleAvoidance(1.0)
        # load the text resources
        self.textKeys = ['title', 'instruction1', 'instruction2', 'instruction3', \
          'instruction4', 'instruction5', 'instruction6', 'instruction7', 'instruction8']
        # compute the text positions
        self.textPositions = []
        for t_p in range(9):
            t_j = ( -1.30, 0, 0.95 - (t_p * 0.05) )
            self.textPositions.append(t_j)
        # title
        self.textPlay.loadTextLine('Genesis Test Panda AI. Powered by Funtrench', \
            self.textKeys[0])
        # instructions
        self.textPlay.loadTextLine('Press ESCAPE to quit', self.textKeys[1])
        self.textPlay.loadTextLine('F/B: Increment/Decrement cube X', self.textKeys[2])
        self.textPlay.loadTextLine('G/H: Increment/Decrement cube Y', self.textKeys[3])
        self.textPlay.loadTextLine('A/J: Start/Stop wander mode', self.textKeys[4])
        self.textPlay.loadTextLine('K/P: Start/Stop cube pursuit', self.textKeys[5])
        self.textPlay.loadTextLine('M/V: Start/Stop cube evasion', self.textKeys[6])
        self.textPlay.loadTextLine('I: Show game information', self.textKeys[7])
        self.textPlay.loadTextLine('D: Show documentation', self.textKeys[8])
        # game info
        self.textPlay.loadTextLine(self.gameID, 'Game')
        # manual text
        t_n =  self.gameMVC.mvcStructure['tier_resource']['text'] + '/GenesisTest.txt'
        self.textPlay.loadTextFile(t_n, 'Doc')
        # setup key bindings
        self.accept("f", self.cubeAlter, [+1, "X"])
        self.accept("b", self.cubeAlter, [-1, "X"] )
        self.accept("g", self.cubeAlter, [+1, "Y"] )
        self.accept("h", self.cubeAlter, [-1, "Y"] )
        self.accept("a", self.wanderToggle, [1] )
        self.accept("j", self.wanderToggle, [0] )
        self.accept("k", self.pursueToggle, [1] )
        self.accept("p", self.pursueToggle, [0] )
        self.accept("m", self.evadeToggle, [1] )
        self.accept("v", self.evadeToggle, [0] )
        self.accept("s", self.screenCapture, ['../GenesisAI_'])
        self.accept("d", self.textPlay.displayText, ['Doc', 30, (-1.00,0,0.35), False])
        self.accept("i", self.textPlay.displayText, ['Game', 30, (0.05,0,0.95), False])
        self.accept("c", self.textPlay.clearScreen)
    # ------------------BEHAVIORS-------------------------
    # ----------------------------------------------------
    def wanderToggle(self, actionType):
        " start/stop Miranda's wander "
        if actionType == 0:
            # stop wander
            if self.smartEve[1].behaviorStatus('wander') == "active":
                self.smartEve[1].removeAi('wander')
        else:
            # start wander
            if self.smartEve[1].behaviorStatus('wander') == "disabled":
                self.smartEve[1].wander(5, 0, 25, 0.5)
    def pursueToggle(self, actionType):
        " start/stop Miranda's pursuit of cube "
        if actionType == 0:
            # stop pursuit
            if self.smartEve[1].behaviorStatus('pursue') == "active":
                self.smartEve[1].removeAi('pursue')
                self.smartEve[1].removeAi('arrival')
        else:
            # start pursuit
            if self.smartEve[1].behaviorStatus('pursue') == "disabled":
                self.smartEve[1].pursue(self.objectStore['cube'][0], 0.7)
                self.smartEve[1].arrival(4.0)
    def evadeToggle(self, actionType):
        " start/stop Miranda's evasion of cube "
        if actionType == 0:
            # stop evasion
            if self.smartEve[1].behaviorStatus('evade') == "active":
                self.smartEve[1].removeAi('evade')
        else:
            # start evasion
            if self.smartEve[1].behaviorStatus('evade') == "disabled":
                self.smartEve[1].evade(self.objectStore['cube'][0], 2.0, 5.0, 1.0)
    def cubeAlter(self, valueChange, valueType):
        " alters co-ordinate position of cube "
        if valueType == "X":
            self.objectStore['cube'][0].setX(self.objectStore['cube'][0].getX() + \
                valueChange)
        elif valueType == "Y":
            self.objectStore['cube'][0].setY(self.objectStore['cube'][0].getY() + \
                valueChange)
    # ------------------TASKS-----------------------------
    # ----------------------------------------------------
    def starterTask(self, task):
        " task to handle the startup "
        if task.time == 0.0:
            if self.worldData['showMouse'] != 0:
                # self.worldData['showMouse'] is 0 because for this sample
                # we don't need a cursor
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
                # we only include this as good practice in case config.xml is
                # edited to make the cursor visible.
                if self.worldData['showMouse'] != 0:
                    self.toggleMouseCursor()
                return task.done
            else:
                # all other frames
                return task.cont
    def genesisCameraTask(self, task):
        "updates camera position to follow Eve"
        # camera follows mainActor
        base.camera.setPos(self.ladyEve.baseActor.getX() + self.camPos[0], \
            self.ladyEve.baseActor.getY() + self.camPos[1], \
            self.ladyEve.baseActor.getZ() + self.camPos[2])
        base.camera.lookAt(self.ladyEve.baseActor)
        return task.cont

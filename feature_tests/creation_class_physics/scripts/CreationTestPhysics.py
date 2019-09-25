# Package Description: Funtrench's Eden Software Development Kit
# Name: Eden Feature Tests SDK
# Desc: Advanced Test Project for the Creation Class
# File name: CreationTestPhysics.py
# Developed by: Project Eden Development Team
# Date: 14/07/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from Eden.Eden3D.Worlds.Creation import Creation
from Eden.Eden2D.Text2D import Text2D
from direct.task import Task
from random import randint
# --------------------------------------------------
# A class to demonstrate the features of the Creation
# Class.
# Class definition for the CreationTestPhysics class
# --------------------------------------------------
class CreationTestPhysics(Creation):
    " Extending the Creation class for the advanced Eden world "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        # the startupTask can be a custom one as in this case or
        # you can argue 'Default' to use the default task provided
        # leaving it blank means you will handle startup tasks yourself
        Creation.__init__(self, self.starterTask) # ancestral constructor
        t_f = [('arial.egg', 'Arial')]
        self.textPlay = Text2D(self.edenVisuals.fpsValue, t_f)
        # load the text resources
        # -----------------------------------------------------------------
        self.textKeys = ['title', 'instruction1', 'instruction2', 'instruction3', \
          'instruction4']
        # compute the text positions
        self.textPositions = []
        for t_p in range(5):
            t_j = ( -1.30, 0, 0.95 - (t_p * 0.05) )
            self.textPositions.append(t_j)
        # title
        t_z = 'Creation Test Physics. Powered by Funtrench'
        self.textPlay.loadTextLine(t_z, self.textKeys[0])
        # instructions
        self.textPlay.loadTextLine('Press ESCAPE to quit', self.textKeys[1])
        self.textPlay.loadTextLine('F: Load cubes with physics', self.textKeys[2])
        self.textPlay.loadTextLine('I: Show game information', self.textKeys[3])
        self.textPlay.loadTextLine('D: Show documentation', self.textKeys[4])
        # game info - this variable contains all the game 'About' information
        # in a readily-presentable format.
        self.textPlay.loadTextLine(self.gameID, 'Game')
        # manual text
        t_n =  self.gameMVC.mvcStructure['tier_resource']['text'] + \
            '/CreationTest.txt'
        self.textPlay.loadTextFile(t_n, 'Doc')
        # -----------------------------------------------------------------
        # setup key bindings
        # load the cubes with physics
        self.accept("f", self.loadCubes, [])
        self.accept("s", self.screenCapture, ['../CreationPhysics_'])
        self.accept("d", self.textPlay.displayText, ['Doc', 30, (-1.00,0,0.35), False])
        self.accept("i", self.textPlay.displayText, ['Game', 30, (0.20,0,0.95), False])
        self.accept("c", self.textPlay.clearScreen)
    # ------------------BEHAVIORS-------------------------
    # ----------------------------------------------------
    def loadCubes(self):
        " loads a random number of cubes into the scene "
        t_c = randint(3, 7)
        # use the total mass instead of density in the setBox() ODE method
        # 'other' value is for storing additional masses for appending
        t_d = {'shape':2, 'density':0.0, 'other':None, 'X':1, 'Y':1, 'Z':1, \
            'collisionShape':0}
        # take advantage of new autofill feature in Creation for the extraData dictionary
        t_e = {'enablePhysics':True, 'objectMass':0.1, 'odeMass':t_d}
        for t_x in range(t_c):
            self.loadGeometry('cube', 'cube%d' % t_x, (0.15,0.15,0.15), \
                (-6 + (t_x * 3), 0, 10), t_e)
    # ------------------TASKS-----------------------------
    # ----------------------------------------------------
    def starterTask(self, task):
        " task to handle the startup "
        if task.time == 0.0:
            # hide the cursor for opening (only if it is visible). The setting
            # in config.xml will affect the cursor immediately from startup and
            # into the game. If you want to have it visible during the game but
            # not at startup, use the procedure demonstrated here.
            if self.worldData['showMouse'] != 0:
                # since the cursor is visible, this hides it
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
                # show the cursor again because now we are through with
                # opening screens
                if self.worldData['showMouse'] != 0:
                    self.toggleMouseCursor()
                return task.done
            else:
                # all other frames
                return task.cont
  

# Package Description: Funtrench's Eden Software Development Kit
# Name: Eden Feature Tests SDK
# Desc: Test Project for the Creation Class
# File name: CreationTest.py
# Developed by: Project Eden Development Team
# Date: 14/07/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from Eden.Eden3D.Worlds.Creation import Creation
from Eden.Eden2D.Text2D import Text2D
from direct.task import Task
# --------------------------------------------------
# A class to demonstrate the features of the Creation
# Class.
# Class definition for the CreationTest class
# --------------------------------------------------
class CreationTest(Creation):
    " Extending the Creation class for the basic Eden world "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        # the startupTask can be a custom one as in this case or
        # you can argue 'Default' to use the default task provided
        # leaving it blank means you will handle startup tasks yourself
        Creation.__init__(self, self.starterTask) # ancestral constructor
        t_f = [('arial.egg', 'Arial')]
        self.textPlay = Text2D(self.edenVisuals.fpsValue, t_f)
        # load geometry (the ViS Cube)
        self.loadGeometry('cube', 'cube', (0.25,0.25,0.25), (0,0,5))
        # load the text resources
        # -----------------------------------------------------------------
        self.textKeys = ['title', 'instruction1', 'instruction2', 'instruction3', \
          'instruction4', 'instruction5', 'instruction6', 'instruction7']
        # compute the text positions
        self.textPositions = []
        for t_p in range(8):
            t_j = ( -1.30, 0, 0.95 - (t_p * 0.05) )
            self.textPositions.append(t_j)
        # title
        self.textPlay.loadTextLine('Creation Test. Powered by Funtrench', \
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
        # game info - this variable contains all the game 'About' information
        # in a readily-presentable format.
        self.textPlay.loadTextLine(self.gameID, 'Game')
        # manual text
        t_n =  self.gameMVC.mvcStructure['tier_resource']['text'] + '/CreationTest.txt'
        self.textPlay.loadTextFile(t_n, 'Doc')
        # -----------------------------------------------------------------
        # setup key bindings
        self.accept("f", self.cubeAlter, [+1, "X"])
        self.accept("b", self.cubeAlter, [-1, "X"] )
        self.accept("g", self.cubeAlter, [+1, "Y"] )
        self.accept("h", self.cubeAlter, [-1, "Y"] )
        self.accept("a", self.cubeAlter, [+1, "Z"] )
        self.accept("j", self.cubeAlter, [-1, "Z"] )
        self.accept("s", self.screenCapture, ['../Creation_'])
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
  

# Package Description: Funtrench's Eden Software Development Kit
# Name: Eden Feature Tests SDK
# Desc: Test Project for the CheckerBoard Class
# File name: CheckerBoardTest.py
# Developed by: Project Eden Development Team
# Date: 19/08/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from Eden.Eden3D.Simulators.Board.CheckerBoard import CheckerBoard
from Eden.Eden2D.Text2D import Text2D
from direct.task import Task
from panda3d.core import Vec3
from direct.interval.IntervalGlobal import *
# --------------------------------------------------
# A class to demonstrate the features of the CheckerBoard
# Class.
# Class definition for the CheckerBoardTest class
# --------------------------------------------------
class CheckerBoardTest(CheckerBoard):
    " Extending the CheckerBoard class for the basic checkers replay game "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        CheckerBoard.__init__(self, ignorePicker = True) # ancestral constructor
        t_f = [('arial.egg', 'Arial')]
        self.textPlay = Text2D(self.edenVisuals.fpsValue, t_f)
        self.skinCode = 2
        # load the text resources
        # -----------------------------------------------------------------
        self.textKeys = ['title', 'instruction1', 'instruction2', 'instruction3', \
            'instruction4', 'instruction5', 'instruction6']
        # compute the text positions
        self.textPositions = []
        for t_p in range(7):
            t_j = Vec3( -1.30, 0, 0.95 - (t_p * 0.05) )
            self.textPositions.append(t_j)
        # title
        self.textPlay.loadTextLine('CheckerBoard Test. Powered by Funtrench', \
          self.textKeys[0])
        # instructions
        self.textPlay.loadTextLine('Press ESCAPE to quit', self.textKeys[1])
        self.textPlay.loadTextLine('Press B/W to turn board to your side', \
            self.textKeys[2])
        self.textPlay.loadTextLine('R: Run replay game', self.textKeys[3])
        self.textPlay.loadTextLine('H: Change board skin', self.textKeys[4])
        self.textPlay.loadTextLine('I: Show game information', self.textKeys[5])
        self.textPlay.loadTextLine('D: Show documentation', self.textKeys[6])
        # game info - this variable contains all the game 'About' information
        # in a readily-presentable format.
        self.textPlay.loadTextLine(self.gameID, 'Game')
        # manual text
        t_n =  self.gameMVC.mvcStructure['tier_resource']['text'] + \
            '/CheckerBoardTest.txt'
        self.textPlay.loadTextFile(t_n, 'Doc')
        # -----------------------------------------------------------------
        # load sound effects
        self.loadSoundEffect('piece.wav', 'pieceDown')
        self.loadSoundEffect('king.wav', 'kingCrown')
        self.loadSoundEffect('capture.wav', 'capturePiece')
        self.loadSoundEffect('victory.wav', 'winGame')
        self.loadSoundEffect('draw.wav', 'drawGame')
        # setup key bindings
        self.accept("s", self.screenCapture, ['../CheckerBoard_'])
        self.accept("d", self.textPlay.displayText, ['Doc', 30, Vec3(-1.00,0,0.35), False])
        self.accept("i", self.textPlay.displayText, ['Game', 30, Vec3(0.20,0,0.95), False])
        self.accept("c", self.textPlay.clearScreen)
        self.accept("h", self.changeSkin)
        self.accept("b", self.turnBoard, ['black'])
        self.accept("w", self.turnBoard, ['white'])
        self.accept("r", self.playReplay)
        # initialize message system
        t_d = {'pieceMove':(self.eventProcessor, ['M']), \
            'captureEvent':(self.eventProcessor, ['C']), \
            'kingEvent':(self.eventProcessor, ['K']), \
            'victoryEvent':(self.eventProcessor, ['V']), \
            'drawEvent':(self.eventProcessor, ['D'])}
        self.eventCodeLibrary['M'] = 'pieceDown'
        self.eventCodeLibrary['C'] = 'capturePiece'
        self.eventCodeLibrary['K'] = 'kingCrown'
        self.eventCodeLibrary['V'] = 'winGame'
        self.eventCodeLibrary['D'] = 'drawGame'
        self.initMessageSystem(t_d)
    # ------------------BEHAVIORS-------------------------
    # ----------------------------------------------------
    def playReplay(self):
        " playback a saved replay "
        # use the XML file moves
        self.readMovesFile('basic.xml')
    def changeSkin(self):
        " change the board texture "
        if self.skinCode < 20:
            pass
        else:
            self.skinCode = 1
        # set the new skin
        self.boardTexture = 'board_' + str(self.skinCode) + '.jpg'
        self.setBoardTexture()
        self.skinCode = self.skinCode + 1


    
  

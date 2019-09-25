# Package Description: Funtrench's Eden Software Development Kit
# Name: Eden Feature Tests SDK
# Desc: Test Project for the CheckerBoard Class
# File name: CheckersMarkIITest.py
# Developed by: Project Eden Development Team
# Date: 30/05/2009
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from Eden.Eden3D.Simulators.Board.CheckersMarkII import CheckersMarkII
from Eden.Eden2D.Text2D import Text2D
from Eden.Eden2D.Glass2D import Glass2D
from direct.task import Task
from panda3d.core import Vec3
from direct.interval.IntervalGlobal import *
# --------------------------------------------------
# A class to demonstrate the features of the CheckersMarkII
# Class.
# Class definition for the CheckersMarkIITest class
# --------------------------------------------------
class CheckersMarkIITest(CheckersMarkII):
    " Extending the CheckersMarkII class for an AI-versus-human game "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        CheckersMarkII.__init__(self, versusAI = True) # ancestral constructor
        t_f = [('arial.egg', 'Arial')]
        self.textPlay = Text2D(self.edenVisuals.fpsValue, t_f)
        self.hudBrush = Glass2D(self.gameMVC)
        self.skinCode = 2
        # load the text resources
        # -----------------------------------------------------------------
        self.textKeys = ['title', 'instruction1', 'instruction2', 'instruction3', \
            'instruction4']
        # compute the text positions
        self.textPositions = []
        for t_p in range(5):
            t_j = Vec3( -1.30, 0, 0.95 - (t_p * 0.05) )
            self.textPositions.append(t_j)
        # title
        self.textPlay.loadTextLine('CheckersMarkII Test. Powered by Funtrench', \
          self.textKeys[0])
        # instructions
        self.textPlay.loadTextLine('Press ESCAPE to quit', self.textKeys[1])
        self.textPlay.loadTextLine('H: Change board skin', self.textKeys[2])
        self.textPlay.loadTextLine('I: Show game information', self.textKeys[3])
        self.textPlay.loadTextLine('D: Show documentation', self.textKeys[4])
        # game info - this variable contains all the game 'About' information
        # in a readily-presentable format.
        self.textPlay.loadTextLine(self.gameID, 'Game')
        # manual text
        t_n =  self.gameMVC.mvcStructure['tier_resource']['text'] + \
            '/CheckersMarkIITest.txt'
        self.textPlay.loadTextFile(t_n, 'Doc')
        # -----------------------------------------------------------------
        # load sound effects
        self.loadSoundEffect('piece.wav', 'pieceDown')
        self.loadSoundEffect('king.wav', 'kingCrown')
        self.loadSoundEffect('capture.wav', 'capturePiece')
        self.loadSoundEffect('victory.wav', 'winGame')
        self.loadSoundEffect('draw.wav', 'drawGame')
        # setup key bindings
        self.accept("s", self.screenCapture, ['../CheckersMarkII_'])
        self.accept("d", self.textPlay.displayText, ['Doc', 30, Vec3(-1.00,0,0.35), False])
        self.accept("i", self.textPlay.displayText, ['Game', 30, Vec3(0.20,0,0.95), False])
        self.accept("c", self.textPlay.clearScreen)
        self.accept("h", self.changeSkin)
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
        # setup event bindings
        self.accept("startup-done", self.setupHUD)
    # ------------------BEHAVIORS-------------------------
    # ----------------------------------------------------
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
    def setupHUD(self):
        " setup the HUD for the game "
        # create the unit HUD
        self.hudBrush.loadHUD('gameHUD.xml', None)
        # activate message system to HUD communication
        self.hudPresent = True
        # initialize game
        self.setupMixedGame('smartRandom')

    
  
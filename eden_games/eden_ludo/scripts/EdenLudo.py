# Package Description: Funtrench Eden Games
# Name: Ludo 1.0
# Desc: Board Game powered by Eden
# File name: EdenLudo.py
# Developed by: Project Eden Development Team
# Date: 08/07/2009
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench PLC. www.funtrench.com       |
# |------------------------------------------------|
from Eden.Eden3D.Worlds.Creation import *
from Eden.Eden2D.Text2D import Text2D
from Eden.Eden2D.Menu2D import Menu2D
from Eden.Eden2D.Glass2D import Glass2D
from Eden.EdenTools.XMLParsers.ConfigParser import ConfigParser
from Eden.EdenTools.Pickers.ObjectPicker import ObjectPicker
from direct.task import Task
from random import randint
from ludo_globals import *
import sys
# --------------------------------------------------
# A class to implement the board game
# Class definition for the EdenLudo class
# --------------------------------------------------
class EdenLudo(Creation):
    " Class to implement the ludo board "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        Creation.__init__(self, self.starterTask) # ancestral constructor
        # 0 - green
        # 1 - yellow
        # 2 - red
        # 3 - blue
        # initialize variables
        self.boardPositions = boardPositions
        self.greenPath = greenPath
        self.yellowPath = yellowPath
        self.redPath = redPath
        self.bluePath = bluePath
        self.boardOccupants = boardOccupants
        t_f = [('arial.egg', 'Arial')]
        self.textPlay = Text2D(self.edenVisuals.fpsValue, t_f)
        self.mazeXPU = ConfigParser()
        self.menuBrush = Menu2D(self.gameMVC)
        self.hudBrush = Glass2D(self.gameMVC)
        # load start sound
        self.loadSoundEffect('start.wav', 'start')
        # load reset to start sound
        self.loadSoundEffect('reset1.wav', 'reset1')
        self.loadSoundEffect('reset2.wav', 'reset2')
        self.loadSoundEffect('reset3.wav', 'reset3')
        self.loadSoundEffect('reset4.wav', 'reset4')
        # load other sounds
        self.loadSoundEffect('pick.wav', 'pick')
        self.loadSoundEffect('move.wav', 'move')
        self.loadSoundEffect('warning.wav', 'warning')
        self.loadSoundEffect('six.wav', 'six')
        # load game music
        self.loadMusic('sound2.mp3', 'music2')
        # Flag which shows if dice is rolled or not
        self.rollFlag = False
        self.sixFlag = False
        # variable that indicates temporary position of a piece
        self.tempPosition = 0
        # dictionary of all players 
        # in self.teams each piece is recorded as [position in path,if the piece is at start, \
        #active player, if piece is at home]
        self.teams = {'Green':[[0,True,False,False],[0,True,False,False],[0,True,False,False], \
            [0,True,False,False]],'Red':[[0,True,False,False],[0,True,False,False], \
            [0,True,False,False],[0,True,False,False]],'Yellow':[[0,True,False,False], \
            [0,True,False,False],[0,True,False,False],[0,True,False,False]], \
            'Blue':[[0,True,False,False],[0,True,False,False],[0,True,False,False], \
            [0,True,False,False]]}
        self.player = ['Green','Yellow','Red','Blue']
        # variables that indicates team and player index
        self.teamIndex = 0
        self.playerIndex = 0
        # variable that indicates the active player
        self.activePlayer = ''
        # variable that indicates the previous player
        self.prevPlayer = ''
        # variable that indicates if a piece is raised / selected
        self.heightFlag = False
        # variable that indicates value of dice toss
        self.toss = 0
        # create callback function list
        self.callBackList = [(sys.exit, [0]), (self.beginNewGame, []), \
            (self.dummyCallBack, []), (self.dummyCallBack, []), (self.dummyCallBack, []), \
            (self.dummyCallBack, [])]
        # setup key mappings
        self.accept("r", self.rollDice, [])
        # we have to give ObjectPicker direct access to local data and methods
        t_d = {'CNF':base.camera.attachNewNode, \
            'MWN':base.mouseWatcherNode.getMouse, 'msgr':messenger.send, \
            'BCNF':base.camNode, 'parentNode':self.staticsNode}
        # set the bitMask for the geometry
        self.geomBitMask = self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['collisionBM']
        self.geometryNode.setCollideMask(BitMask32.bit(self.geomBitMask))
        # initialize picker tag
        self.pickerTag = 'Candidate'
        # must exist for object picker
        self.currentSelection = 'None'
        self.prevSelection = ''
        # if the picking system is set up, accept selection messages
        self.accept('object-select', self.processSelection)
        # instance the picker
        self.piecePicker = ObjectPicker(self, t_d)
    # ------------------BEHAVIORS-------------------------
    # ----------------------------------------------------
    def beginNewGame(self):
        " loads a new game "
        # show on HUD the turn of player 
        self.loadBoard()
        taskMgr.add(self.gameTask, 'gameTask')
        # stop startup (menu) music
        self.gameMusic.stop()
        self.jukeBox['music2'].play()
    def loadBoard(self):
        'function that loads the board and pieces'
        # build a pathname to the file
        t_g = self.gameMVC.mvcStructure['config'] + '/'
        t_g += 'fourHumans.xml'
        # parse board details XML (XPU = XML processing unit)
        self.mazeXPU.parseFile(t_g)
        # get maze information
        self.mazeXPU.getSectionValues('subsection','Players')
        self.mazeXPU.getSectionValues('subsection','Scale')
        # get the scale
        t_s = (self.mazeXPU.Parser['XML_Values']['Scale_Values'] \
            ['pScaleX'], self.mazeXPU.Parser['XML_Values']['Scale_Values'] \
            ['pScaleY'], self.mazeXPU.Parser['XML_Values']['Scale_Values'] \
            ['pScaleZ'])
        t_lp = ['Green','Yellow','Red','Blue']
        for t_x in range(4):
            for t_y in range(4):
                # get the positions
                t_p = (self.boardPositions['start'][t_x][t_y][0], self.boardPositions['start'][t_x][t_y][1], \
                    1.5)
                t_m = self.mazeXPU.Parser['XML_Values']['Players_Values']['model%d' % t_x]
                t_n = t_lp[t_x] + str(t_y)
                self.loadGeometry(t_m, t_n, t_s, t_p)
                # set the picker tag
                self.objectStore[t_n][0].setTag(self.pickerTag, t_n)
        # hide the menu
        self.menuBrush.hideMenu('Main')
    def rollDice(self):
        " function that indicates player's turn "
        if self.rollFlag == True:
            if self.sixFlag == True:
                self.printHud('Event','Please play first!')
                self.jukeBox['warning'].play()
                return False
            else:
                t_f = '%s player'  % self.activePlayer
                self.printHud('Turn',t_f)
                self.printHud('Event','Already rolled the dice!')
                self.printHud('Toss',self.toss)
                self.jukeBox['warning'].play()
                return False
        self.toss = randint(1,6)
        t_n = '%s rolled a %d' % (self.activePlayer, self.toss)
        self.printHud('Toss',t_n)
        self.rollFlag = True
        if self.toss == 6:
            self.sixFlag = True
            self.jukeBox['six'].play()
        if self.sixFlag == False:
            t_c = 0
            for t_d in range(len(self.teams[self.activePlayer])):
                if self.teams[self.activePlayer][t_d][1] == True:
                    t_c += 1
                else:
                    pass
            if t_c == len(self.teams[self.activePlayer]):
                self.prevPlayer = self.activePlayer
                self.teamIndex += 1
                if self.teamIndex == 4:
                    self.teamIndex = 0
                self.activePlayer = self.player[self.teamIndex]
                taskMgr.add(self.delayTask, 'delayTask')
                t_n= "%s player is unlucky %s's turn" % (self.prevPlayer, self.activePlayer)
                self.printHud('Turn',t_n)
                self.printHud('Event','Please roll dice')
                self.rollFlag = False
                return
            t_j = 0
            for t_k in range(4):
                if self.teams[self.activePlayer][t_k][1] == False and \
                self.teams[self.activePlayer][t_k][3] == False:
                    break
                else:
                    t_j += 1
            if t_j == 4:
                self.prevPlayer = self.activePlayer
                self.teamIndex += 1
                if self.teamIndex == 4:
                    self.teamIndex = 0
                self.activePlayer = self.player[self.teamIndex]
                taskMgr.add(self.delayTask, 'delayTask')
                t_n= "%s player is unlucky %s's turn" % (self.prevPlayer, self.activePlayer)
                self.printHud('Turn',t_n)
                self.printHud('Event','Please roll dice')
                self.rollFlag = False
    def printHud(self,path,message):
        " function that updates the HUD"
        self.hudBrush.menuList['Status']['labels'][path] \
                ['text'] = str(message)
    def processSelection(self):
        " function that processes when a piece is selected "
        if self.rollFlag == False:
            self.printHud('Toss','_ _ _')
            self.printHud('Event','Please roll dice first!')
            return False
        if self.currentSelection.find(self.activePlayer) == -1:
            #self.printHud('Toss','_ _ _')
            self.printHud('Event','Not your turn!')
            self.jukeBox['warning'].play()
            return False
        # At this point the selection is valid
        t_d = self.objectStore[self.currentSelection][0].getZ()
        if t_d != 2.0 and self.heightFlag == False:
            self.objectStore[self.currentSelection][0].setZ(2.0)
            self.heightFlag = True
            self.printHud('Event','Piece selected')
            self.findIndex()
            # set as selected piece
            self.teams[self.activePlayer][self.playerIndex][2] = True
            self.currentSelection = ''
        elif t_d != 2.0 and self.heightFlag == True:
            # set previous selection
            self.prevSelection = self.activePlayer + str(self.playerIndex)
            self.objectStore[self.prevSelection][0].setZ(1.5)
            self.objectStore[self.currentSelection][0].setZ(2.0)
            self.teams[self.activePlayer][self.playerIndex][2] = False
            self.printHud('Event','Selection changed')
            self.findIndex()
            self.teams[self.activePlayer][self.playerIndex][2] = True
            self.currentSelection = ''
            self.jukeBox['pick'].play()
        elif t_d == 2.0:
            if self.teams[self.activePlayer][self.playerIndex][3] == True:
                self.printHud('Event','Piece is already at home!')
                self.jukeBox['warning'].play()
                return False
            self.movePiece()
            self.jukeBox['move'].play()
            self.currentSelection = ''
    def findIndex(self):
        "returns index of current piece"
        for t_x in range(4):
            if self.currentSelection.find(str(t_x)) != -1:
                self.playerIndex = t_x
                break
    def movePiece(self):
        "moves the selected piece"
        if self.sixFlag == True and  self.teams[self.activePlayer][self.playerIndex][1] == True:
            t_l = [self.greenPath,self.yellowPath,self.redPath,self.bluePath]
            t_p = t_l[self.teamIndex][0][0]
            t_x = self.boardPositions['tiles'][t_p[0]][t_p[1]]
            self.objectStore[self.currentSelection][0].setX(t_x[0])
            self.objectStore[self.currentSelection][0].setY(t_x[1])
            self.objectStore[self.currentSelection][0].setZ(1.5)
            self.teams[self.activePlayer][self.playerIndex][2] = False
            self.resetPiece()
            self.rollFlag = False
            self.heightFlag = False
            self.printHud('Toss','_ _ _')
            self.printHud('Event','Extra turn')
            self.sixFlag = False
            self.teams[self.activePlayer][self.playerIndex][1] = False
            self.jukeBox['start'].play()
        elif self.sixFlag == False and  self.teams[self.activePlayer][self.playerIndex][1] == False:
            t_l = [self.greenPath,self.yellowPath,self.redPath,self.bluePath]
            self.teams[self.activePlayer][self.playerIndex][0] += self.toss
            t_r = self.teams[self.activePlayer][self.playerIndex][0]
            if t_r > 50:
                if t_r == 56:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][5]
                    self.teams[self.activePlayer][self.playerIndex][3] = True
                    self.jukeBox['six'].play()
                    t_j = 0
                    for t_k in range(4):
                        if self.teams[self.activePlayer][t_k][3] == True: 
                            t_j += 1
                        else:
                            pass
                    if t_j == 4:
                        t_n= "CONGRATULATIONS %s player all pieces are at \
                             home %s's turn" % (self.prevPlayer, self.activePlayer)
                        self.printHud('Turn',t_n)
                elif t_r == 57:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][4]
                    self.teams[self.activePlayer][self.playerIndex][0] = 55
                    t_r = self.teams[self.activePlayer][self.playerIndex][0]
                elif t_r == 58:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][3]
                    self.teams[self.activePlayer][self.playerIndex][0] = 54
                    t_r = self.teams[self.activePlayer][self.playerIndex][0]
                elif t_r == 59:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][2]
                    self.teams[self.activePlayer][self.playerIndex][0] = 53
                    t_r = self.teams[self.activePlayer][self.playerIndex][0]
                elif t_r == 60:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][1]
                    self.teams[self.activePlayer][self.playerIndex][0] = 52
                    t_r = self.teams[self.activePlayer][self.playerIndex][0]
                elif t_r == 61: 
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][0]
                    self.teams[self.activePlayer][self.playerIndex][0] = 51
                    t_r = self.teams[self.activePlayer][self.playerIndex][0]
                else:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][t_r - 51]
            else:
                t_s = 'tiles'
                t_p = t_l[self.teamIndex][0][t_r]
            t_x = self.boardPositions[t_s][t_p[0]][t_p[1]]
            self.objectStore[self.currentSelection][0].setX(t_x[0])
            self.objectStore[self.currentSelection][0].setY(t_x[1])
            self.objectStore[self.currentSelection][0].setZ(1.5)
            self.teams[self.activePlayer][self.playerIndex][2] = False
            self.resetPiece()
            self.rollFlag = False
            self.heightFlag = False
            self.prevPlayer = self.activePlayer
            self.teamIndex += 1
            if self.teamIndex == 4:
                self.teamIndex = 0
            self.activePlayer = self.player[self.teamIndex]
            self.printHud('Toss','_ _ _')
            t_f = "%s player" % self.activePlayer
            self.printHud('Event',"Please roll dice")
            self.printHud('Turn',t_f)
            self.checkHome()
        elif self.sixFlag == True and  self.teams[self.activePlayer][self.playerIndex][1] == False:
            t_l = [self.greenPath,self.yellowPath,self.redPath,self.bluePath]
            self.teams[self.activePlayer][self.playerIndex][0] += self.toss
            t_r = self.teams[self.activePlayer][self.playerIndex][0]
            if t_r > 50:
                if t_r == 56:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][5]
                    self.teams[self.activePlayer][self.playerIndex][3] = True
                    self.jukeBox['six'].play()
                    t_j = 0
                    for t_k in range(4):
                        if self.teams[self.activePlayer][t_k][3] == True: 
                            t_j += 1
                        else:
                            pass
                    if t_j == 4:
                        t_n= "CONGRATULATIONS %s player all pieces are at \
                             home %s's turn" % (self.prevPlayer, self.activePlayer)
                        self.printHud('Turn',t_n)
                elif t_r == 57:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][4]
                    self.teams[self.activePlayer][self.playerIndex][0] = 55
                    t_r = self.teams[self.activePlayer][self.playerIndex][0]
                elif t_r == 58:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][3]
                    self.teams[self.activePlayer][self.playerIndex][0] = 54
                    t_r = self.teams[self.activePlayer][self.playerIndex][0]
                elif t_r == 59:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][2]
                    self.teams[self.activePlayer][self.playerIndex][0] = 53
                    t_r = self.teams[self.activePlayer][self.playerIndex][0]
                elif t_r == 60:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][1]
                    self.teams[self.activePlayer][self.playerIndex][0] = 52
                    t_r = self.teams[self.activePlayer][self.playerIndex][0]
                elif t_r == 61: 
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][0]
                    self.teams[self.activePlayer][self.playerIndex][0] = 51
                    t_r = self.teams[self.activePlayer][self.playerIndex][0]
                else:
                    t_s = 'cTiles'
                    t_p = t_l[self.teamIndex][1][t_r - 51]
            else:
                t_s = 'tiles'
                t_p = t_l[self.teamIndex][0][t_r]
            t_x = self.boardPositions[t_s][t_p[0]][t_p[1]]
            self.objectStore[self.currentSelection][0].setX(t_x[0])
            self.objectStore[self.currentSelection][0].setY(t_x[1])
            self.objectStore[self.currentSelection][0].setZ(1.5)
            self.teams[self.activePlayer][self.playerIndex][2] = False
            self.resetPiece()
            self.rollFlag = False
            self.heightFlag = False
            self.printHud('Toss','_ _ _')
            self.printHud('Event',"Extra turn")
            self.sixFlag = False
            self.checkHome()
    def resetPiece(self):
        " function that resets a piece"
        for x in range(len(self.teams[self.activePlayer])):
            if self.teams['Green'][x][1] == False:
                t_w = 'Green%d' % x
                t_q = self.objectStore[t_w][0].getX()
                t_u = self.objectStore[t_w][0].getY()
                t_g = self.objectStore[self.currentSelection][0].getX()
                t_h = self.objectStore[self.currentSelection][0].getY()
                if t_q == t_g and t_u == t_h:
                    if self.currentSelection.find('Green') == -1:
                        t_z = self.boardPositions['start'][0][x]
                        self.objectStore[t_w][0].setX(t_z[0])
                        self.objectStore[t_w][0].setY(t_z[1])
                        self.teams['Green'][x][1] = True
                        self.teams['Green'][x][0] = 0
                        self.jukeBox['reset1'].play()
                    else:
                        pass            
        for x in range(len(self.teams[self.activePlayer])):
            if self.teams['Yellow'][x][1] == False:
                t_w = 'Yellow%d' % x
                t_q = self.objectStore[t_w][0].getX()
                t_u = self.objectStore[t_w][0].getY()
                t_g = self.objectStore[self.currentSelection][0].getX()
                t_h = self.objectStore[self.currentSelection][0].getY()
                if t_q == t_g and t_u == t_h:
                    if self.currentSelection.find('Yellow') == -1:
                        t_z = self.boardPositions['start'][1][x]
                        self.objectStore[t_w][0].setX(t_z[0])
                        self.objectStore[t_w][0].setY(t_z[1])
                        self.teams['Yellow'][x][1] = True
                        self.teams['Yellow'][x][0] = 0
                        self.jukeBox['reset2'].play()
                    else:
                        pass
        for x in range(len(self.teams[self.activePlayer])):
            if self.teams['Red'][x][1] == False:
                t_w = 'Red%d' % x
                t_q = self.objectStore[t_w][0].getX()
                t_u = self.objectStore[t_w][0].getY()
                t_g = self.objectStore[self.currentSelection][0].getX()
                t_h = self.objectStore[self.currentSelection][0].getY()
                if t_q == t_g and t_u == t_h:
                    if self.currentSelection.find('Red') == -1:
                        t_z = self.boardPositions['start'][2][x]
                        self.objectStore[t_w][0].setX(t_z[0])
                        self.objectStore[t_w][0].setY(t_z[1])
                        self.teams['Red'][x][1] = True
                        self.teams['Red'][x][0] = 0
                        self.jukeBox['reset3'].play()
                    else:
                        pass
        for x in range(len(self.teams[self.activePlayer])):
            if self.teams['Blue'][x][1] == False:
                t_w = 'Blue%d' % x
                t_q = self.objectStore[t_w][0].getX()
                t_u = self.objectStore[t_w][0].getY()
                t_g = self.objectStore[self.currentSelection][0].getX()
                t_h = self.objectStore[self.currentSelection][0].getY()
                if t_q == t_g and t_u == t_h:
                    if self.currentSelection.find('Blue') == -1:
                        t_z = self.boardPositions['start'][3][x]
                        self.objectStore[t_w][0].setX(t_z[0])
                        self.objectStore[t_w][0].setY(t_z[1])
                        self.teams['Blue'][x][1] = True
                        self.teams['Blue'][x][0] = 0
                        self.jukeBox['reset4'].play()
                    else:
                        pass 
    def checkHome(self):
        " function that checks if all the pieces are at home"
        t_z = 0
        for t_b in range(4):
                if self.teams[self.activePlayer][t_b][3] == True:
                    t_z += 1
                else:
                    pass
        if t_z == 4:
            self.prevPlayer = self.activePlayer
            self.teamIndex += 1
            self.activePlayer = self.player[self.teamIndex]
            t_u = "%s player" % self.activePlayer
            self.printHud('Event',"Please roll dice")
            self.printHud('Turn',t_u)
            self.checkHome()
    # ------------------TASKS-----------------------------
    # ----------------------------------------------------
    def starterTask(self, task):
        " task to handle the startup "
        if task.time == 0.0:
            # hide the cursor for startup if it is visible
            if self.worldData['showMouse'] != 0:
                self.toggleMouseCursor()
            # play menu music
            self.gameMusic.setLoop(True)
            self.gameMusic.play()
            # setup game music
            self.jukeBox['music2'].setLoop(True)
            # show the screens with an n-second delay
            self.edenVisuals.sequenceAllImages(self.visualDelay)
            return task.cont
        else:
            if self.edenVisuals.virginFlag == True:
                # load main menu after images are done
                self.menuBrush.loadMenu('main.xml', self.callBackList)
                # load about image
                # build a path for the image
                t_m = self.gameMVC.mvcStructure['tier_resource']['images'] + '/'
                t_m += 'about.png'
                self.edenVisuals.loadImage(t_m)
                # we need the mouse cursor
                self.toggleMouseCursor()
                return task.done
            else:
                # all other frames
                return task.cont
    def gameTask(self, task):
        " processes game events and validates score "
        if task.time == 0.0:
            # do all initialization for the game here
            # create the HUD
            self.hudBrush.loadHUD('status.xml', None)
            self.teamIndex = randint(1,4)
            self.teamIndex -= 1
            self.activePlayer = self.player[self.teamIndex]
            t_y = self.activePlayer + "'s turn"
            self.printHud('Turn',t_y)
            self.printHud('Event','Please to roll dice')
            # set the new title
            #self.hudBrush.menuList['Status']['labels'] \
            #    ['Dir']['text'] = self.defaultTitle
        return task.cont
    def delayTask(self, task):
        " task that delays the display of tossed"
        if (task.frame / 60) == 2:
            self.printHud('Toss','_ _ _')
            return task.done
        else:
            self.printHud('Toss',self.toss)
            return task.cont
        
    
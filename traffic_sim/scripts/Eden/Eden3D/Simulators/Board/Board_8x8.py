# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Simulators.Board]
# Desc: Board Game Simulators Library - Board_8x8 Class
# File name: Board_8x8.py
# Developed by: Project Eden Development Team
# Date: 22/05/2012
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from Eden.Eden3D.Worlds.Creation import *
from Eden.EdenTools.XMLParsers.ConfigParser import ConfigParser
from Eden.EdenTools.XMLGenerators.ConfigGenerator import ConfigGenerator
from Eden.EdenTools.Pickers.ObjectMover import ObjectMover
# ---------------------------------------------
# A class that implements a basic world with a 
# checkerboard in it. Entry point for a board game.
# Startup options are loaded from config.xml
# Class definition for the CheckerBoard class
# ---------------------------------------------
class Board_8x8(Creation):
    " Extends Creation for 8 x 8 game boards "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, remoteStarterTask = None, ignorePicker = False, \
            versusAI = False, customPRC = None, edenClass = '8x8_Board'):
        if remoteStarterTask == None:
            remoteStarterTask = self.starterTask
        Creation.__init__(self, remoteStarterTask, customPRC, edenClass) # ancestral constructor
        # set the bitMask for the geometry
        self.geomBitMask = self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['collisionBM']
        self.geometryNode.setCollideMask(BitMask32.bit(self.geomBitMask))
        # load board-specific settings
        self.defaultView = [self.worldData['cameraHpr'][0], \
            self.worldData['cameraHpr'][1], self.worldData['cameraHpr'][2]]
        # whether to flip the board automatically when the turn changes
        self.autoFlip = self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['autoFlip']
        self.boardTexture = self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['boardTexture']
        # apply the board texture
        if self.boardTexture == 'None':
            # the board model is textured (already loaded)
            pass
        else:
            self.setBoardTexture()
        # re-orient the board to default view
        self.resetView()
        # load board dimensions
        self.boardSpans = (self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['row1'], self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['column1'], self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['row8'], self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['column8'])
        # for messaging subsystem
        self.debugFlag = False
        self.customMessagesFlag = False
        self.eventCodeLibrary = {}
        # for recording sessions
        self.moveDelay = self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['moveInterval']
        self.moveDelay = self.moveDelay * self.edenVisuals.fpsValue
        self.movesList = None
        self.movesCount = 0
        self.recordGame = False
        self.delayReplayFlag = False
        self.logData = {'logFile':None, 'movesList':[]}
        # for AI games
        self.autoGameFlag = False
        self.gameType = self.XPU.Parser['XML_Values']['WorldDetails_Values']['gameType']
        # black always starts (checkers), white always starts (chess)
        self.sideTurn = 0
        self.activePiece = None
        self.legalMoves = []
        self.victoryFlag = False
        self.drawFlag = False
        # load the piece settings
        self.XPU.getSectionValues('subsection','Pieces')
        # initialize variables
        self.pieceScale = (self.XPU.Parser['XML_Values']['Pieces_Values']['scaleX'], \
            self.XPU.Parser['XML_Values']['Pieces_Values']['scaleY'], \
            self.XPU.Parser['XML_Values']['Pieces_Values']['scaleZ'])
        # piece side texturing
        self.pieceTextures = {}
        t_txb = self.XPU.Parser['XML_Values']['Pieces_Values']['texBlack']
        t_txw = self.XPU.Parser['XML_Values']['Pieces_Values']['texWhite']
        self.loadPieceTextures(t_txb, t_txw)
        self.pickingFlag = False
        self.hudPresent = False
        if ignorePicker == False:
            # setup picker system
            # we have to give ObjectPicker direct access to local data and methods
            # to avoid crowding Board_8x8.
            # TODO: Find a more secure way to implement this
            t_d = {'CNF':base.camera.attachNewNode, \
                'MWN':base.mouseWatcherNode.getMouse, 'msgr':messenger.send, \
                'BCNF':base.camNode, 'parentNode':self.world}
            # initialize picker tag
            self.pickerTag = 'Candidate'
            # must exist for object picker
            self.currentSelection = ''
            self.prevSelection = ''
            # instance the picker
            self.piecePicker = ObjectMover(self, t_d)
            # set the flag
            self.pickingFlag = True
            # the allowance on either side of a tile co-ordinate for a drop
            self.dropFactor = self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
                ['dropFactor']
            # if the picking system is set up, accept selection messages
            self.accept('object-select', self.processSelection)
            self.accept('object-released', self.processDrop)
            self.mouseDownFlag = False
            # add the followMouseTask to the task manager
            taskMgr.add(self.followMouseTask, 'followMouse')
            # initialize the versus-AI flag
            self.versusAIFlag = versusAI
            # check the game mode
            if self.versusAIFlag == True:
                # get the setting
                self.aiSide = self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
                    ['aiSide']
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    def resetView(self):
        " orients the board such that the top is clearly visible "
        base.camera.setHpr(self.defaultView[0], self.defaultView[1], self.defaultView[2])
    def setDefaultView(self, newView):
        " modifies the default view "
        for t_x in range(3):
            self.defaultView[t_x] = newView[t_x]
    def turnBoard(self, side = 'auto'):
        " flips board around to player's side "
        if side == "black":
            self.world.setH(0)
            self.world.setX(self.worldData['worldPosition'][0])
            self.world.setY(self.worldData['worldPosition'][1])
        elif side == "white":
            self.world.setH(180)
            t_x = self.worldData['worldPosition'][0] - (2 * \
                self.worldData['worldPosition'][0])
            t_t = 2.0 / math.tan((base.camera.getP() / 180.0) * math.pi)
            if t_t < 0:
                t_t = t_t * -1
            t_y = self.worldData['worldPosition'][1] * t_t
            self.world.setX(t_x)
            self.world.setY(t_y)
        else:
            # turn based on the side
            if self.sideTurn == 0 and self.gameType == 0:
                self.turnBoard('white')
            elif self.sideTurn == 1 and self.gameType == 0:
                self.turnBoard('black')
            elif self.sideTurn == 0 and self.gameType == 1:
                self.turnBoard('black')
            elif self.sideTurn == 1 and self.gameType == 1:
                self.turnBoard('white')
    # --------------------------RESOURCE LOADING-----------------------------
    def setBoardTexture(self):
        " updates board texture "
        # clear the board color to white (makes applied texture visible)
        self.world.clearColor()
        self.world.setColor(1,1,1,1)
        t_i = self.gameMVC.mvcStructure['tier_resource']['images'] + '/' + \
        self.boardTexture
        # load the texture and apply
        t_bt = loader.loadTexture(t_i)
        self.world.setTexture(t_bt, 1)
    def loadPieceTextures(self, blackPiece, whitePiece):
        " loads the textures designated for the pieces "
        t_i = self.gameMVC.mvcStructure['tier_resource']['images'] + '/'
        if blackPiece != 'None':
            t_b = t_i + blackPiece
            self.pieceTextures['black'] = loader.loadTexture(t_b)
        else:
            self.pieceTextures['black'] = None
        if whitePiece != 'None':
            t_w = t_i + whitePiece
            self.pieceTextures['white'] = loader.loadTexture(t_w)
        else:
            self.pieceTextures['white'] = None
    # ------------------SYSTEM SERVICES-----------------
    # ----------------------------------------------------
    def initMessageSystem(self, callBackBundle = None):
        " enables sending of custom messages for events "
        # get the messages settings (must exist)
        self.XPU.getSectionValues('subsection','Messages')
        # set the flag
        self.customMessagesFlag = True
        # message subsystem will be dealt with in daughter classes
        # just load settings and set up callbacks if any
        self.messageLibrary = {}
        for t_x in self.XPU.Parser['XML_Values']['Messages_Values'].keys():
            self.messageLibrary[t_x] = self.XPU.Parser['XML_Values'] \
                ['Messages_Values'][t_x]
            if callBackBundle != None:
                if callBackBundle.has_key(t_x):
                    self.accept(self.messageLibrary[t_x], callBackBundle[t_x][0], \
                        callBackBundle[t_x][1])
    def moveBoard(self, direction, magnitude):
        " displaces the board in X/Y/Z the given magnitude "
        if direction == "X":
            # move along the x-axis
            self.world.setX(self.world.getX() + magnitude)
        elif direction == "Y":
            # move along the y-axis
            self.world.setY(self.world.getY() + magnitude)
        elif direction == "Z":
            # move along the z-axis
            self.world.setZ(self.world.getZ() + magnitude)
        else:
            pass
    def computeTiles(self):
        " computes the co-ords of the valid tiles( row, column ) "
        # allows for making a convenience list of these
        # compute the span (space between pieces on a row)
        t_span = (self.boardSpans[2] - self.boardSpans[0]) / 7.0
        self.boardRows = []
        self.boardColumns = []
        for t_x in range(8):
            t_p = self.boardSpans[0] + (t_x * t_span)
            self.boardRows.append(t_p)
        # compute the span (space between pieces on a column)
        t_span = (self.boardSpans[3] - self.boardSpans[1]) / 7.0
        for t_y in range(8):
            t_p = self.boardSpans[1] + (t_y * t_span)
            self.boardColumns.append(t_p)
        # here we have all the rows and columns
        self.tileSize = t_span
        # each daughter class does its own magic from here
    # -----------AUTOMATED GAMES--------------------
    # Utilities for implementing AI, game recording and replays
    # -----------RECORDING GAMES----------------
    def setupLogging(self, logFile, level = '1', difficulty = 'medium'):
        " initiates logging of game moves for replay "
        self.recordGame = True
        # build to config directory
        t_s = self.gameMVC.mvcStructure['config'] + '/replays/' + logFile
        self.logData['logFile'] = t_s
        # clear anything in the list
        self.logData['movesList'] = []
        self.logData['level'] = level
        self.logData['difficulty'] = difficulty
    def generateLogFile(self):
        " generates and saves the XML moves file "
        # the XML Generating Unit
        movesXGU = ConfigGenerator()
        # create base
        t_hdr = "%s session saved replay file" % [self.worldData['edenClass']]
        movesXGU.createBase("moves", True, ["Copyright (C)2008 Funtrench Technologies PLC.",
        t_hdr])
        # create the About section
        movesXGU.createSection("section", "Name", "Description")
        movesXGU.createSectionComment("About this file", "Description")
        movesXGU.createValue("value", "valueName", "Title", "Moves List", "Description")
        movesXGU.createValue("value", "valueName", "Level", self.logData['level'], \
            "Description")
        movesXGU.createValue("value", "valueName", "Difficulty", \
            self.logData['difficulty'], "Description")
        # create the moves section
        t_list = []
        for t_v, t_x in enumerate(self.logData['movesList']):
            # create the value element
            t_s = str(t_x[0]) + ',' + str(t_x[1]) + ',' + str(t_x[2])
            # if we don't have leading zeros then the moves won't be sorted correctly
            if t_v > 8:
                t_movNo = str(t_v + 1)
            else:
                t_movNo = '0' + str(t_v + 1)
            t_list.append(("value", "valueName", t_movNo, t_s))
        movesXGU.createSectionWithValues("section", "Name", "Moves", t_list)
        # create the file
        movesXGU.generateXMLFile(self.logData['logFile'])
    # -----------REPLAYING GAMES----------------
    def readMovesFile(self, movesXML):
        " reads in moves from an XML file - automated (replay) games "
        if self.movesList != None:
            # a game is in progress
            return False
        # build to config directory
        t_s = self.gameMVC.mvcStructure['config'] + '/replays/' + movesXML
        # the XML Processing Unit
        movesXPU = ConfigParser()
        movesXPU.parseFile(t_s)
        movesXPU.getSectionValues('section','Moves')
        t_m = []
        t_k = movesXPU.Parser['XML_Values']['Moves_Values'].keys()
        t_k.sort()
        for t_x in t_k:
            # split into CSV list
            t_d = movesXPU.Parser['XML_Values']['Moves_Values'][t_x].split(',')
            t_d[0] = int(t_d[0])
            if t_d[0] == 0 and self.gameType == 0:
                t_d[1] = 'w' + t_d[1]
            elif t_d[0] == 1 and self.gameType == 0:
                t_d[1] = 'b' + t_d[1]
            elif t_d[0] == 0 and self.gameType == 1:
                t_d[1] = 'b' + t_d[1]
            elif t_d[0] == 1 and self.gameType == 1:
                t_d[1] = 'w' + t_d[1]
            t_d[2] = int(t_d[2])
            t_m.append(t_d)
        self.movesList = t_m
        # run the moves
        taskMgr.add(self.executeReplayTask, 'executeMoves')
        return True
    # ------------------AI PLAY----------------------
    def setupAutoGame(self, aiAgent = 'bruteRandom'):
        " plays an auto game using the argued AI module "
        if self.autoGameFlag != False:
            # game in progress
            return False
        else:
            self.activeAgent = aiAgent
            self.autoGameFlag = True
            taskMgr.add(self.executeAITask, 'executeAI')
            return True
    def setupMixedGame(self, aiAgent = 'safeRandom'):
        " starts a game between human and AI "
        if self.autoGameFlag != False:
            # game in progress
            return False
        if self.versusAIFlag == False:
            # invalid game mode for this function
            return False
        else:
            self.activeAgent = aiAgent
            self.autoGameFlag = True
            taskMgr.add(self.executeAISideTask, 'executeAIside')
            return True
    # ------------------MESSAGES---------------------
    def systemMessage(self, messageStr, extraData = None, eventName = ''):
        " handles system messages "
        # send the specified message
        if self.customMessagesFlag == True and eventName != '':
            messenger.send(self.messageLibrary[eventName])
        if self.debugFlag == True:
            print messageStr, extraData
        if self.hudPresent == True:
            # update the HUD
            self.hudBrush.menuList['Game']['labels']['Message']['text'] = messageStr
    # ------------------EVENTS-----------------------
    def eventProcessor(self, eventCode):
        " plays a sound effect associated with the event "
        # this is the default event processor (sound only)
        if self.eventCodeLibrary.has_key(eventCode):
            self.jukeBox[self.eventCodeLibrary[eventCode]].play()
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
                messenger.send('startup-done')
                return task.done
            else:
                # all other frames
                return task.cont
    def executeReplayTask(self, task):
        " plays an automated game (replay) "
        if task.time == 0.0:
            self.movesCount = 0
            if self.worldData['showMouse'] != 0:
                # hide the mouse during replay
                self.toggleMouseCursor()
        if self.delayReplayFlag == False:
            t_x = self.movesList[self.movesCount]
            self.processMoveEvent(t_x[0], t_x[1], t_x[2])
            # increment count
            self.movesCount = self.movesCount + 1
            self.delayReplayFlag = True
        else:
            if task.frame % self.moveDelay != 0:
                pass
            else:
                self.delayReplayFlag = False
        # quit on victory
        if self.victoryFlag == True or self.drawFlag == True:
            if self.worldData['showMouse'] != 0:
                # show the mouse after replay
                self.toggleMouseCursor()
            # empty moves list
            self.movesList = None
            return task.done
        else:
            return task.cont
    def executeAITask(self, task):
        " plays an automated game (AI) "
        if task.time == 0.0:
            if self.worldData['showMouse'] != 0:
                # hide the mouse during play
                self.toggleMouseCursor()
        if self.delayReplayFlag == False:
            # generate the AI move
            self.generateAIMove()
            self.delayReplayFlag = True
        else:
            if task.frame % self.moveDelay != 0:
                pass
            else:
                self.delayReplayFlag = False
        # quit on victory
        if self.victoryFlag == True or self.drawFlag == True:
            if self.worldData['showMouse'] != 0:
                # show the mouse after replay
                self.toggleMouseCursor()
            # reset flag
            self.autoGameFlag = False
            return task.done
        else:
            return task.cont
    def executeAISideTask(self, task):
        " plays a versus-AI game "
        if self.sideTurn == self.aiSide:
            # hide cursor for AI
            if self.winHandle[1] != True:
                self.toggleMouseCursor()
                # set the delay flag at the beginning of AI turn
                self.delayReplayFlag = True
            # delay to make sure the AI does not move instantly - it ain't pretty
            if self.delayReplayFlag == False:
                # generate the AI move
                self.generateAIMove()
            else:
                if task.frame % self.moveDelay != 0:
                    pass
                else:
                    self.delayReplayFlag = False
        else:
            # show cursor for human
            if self.winHandle[1] == True:
                self.toggleMouseCursor()
        # quit on victory
        if self.victoryFlag == True or self.drawFlag == True:
            if self.worldData['showMouse'] != 0:
                # show the mouse after replay
                if self.winHandle[1] == True:
                    self.toggleMouseCursor()
            # reset flag
            self.autoGameFlag = False
            return task.done
        else:
            return task.cont
    def followMouseTask(self, task):
        " task to allow moving pieces using the mouse "
        if self.mouseDownFlag == True:
            # this gives up the screen coordinates of the mouse
            if base.mouseWatcherNode.hasMouse():
                t_mp = base.mouseWatcherNode.getMouse()
                # set the position of the ray based on the mouse position
                self.piecePicker.pickerRay.setFromLens(base.camNode, t_mp.getX(), \
                    t_mp.getY())
                # compute the co-ordinates the mouse is hovering over
                # gets the point described by pickerRay.getOrigin(), which is
                # relative to the camera, relative instead to world
                t_np = self.world.getRelativePoint(camera, \
                    self.piecePicker.pickerRay.getOrigin())
                # same thing with the direction of the ray
                t_nv = self.world.getRelativeVector(camera, \
                    self.piecePicker.pickerRay.getDirection())
                t_pos = self.getPointBelowCursor(0.0, t_np, t_nv)
                self.objectStore[self.activePiece[0]][0].setX(t_pos[0])
                self.objectStore[self.activePiece[0]][0].setY(t_pos[1])
            else:
                # the focus is not on the 3D world; maybe minimized    
                pass
        else:
            pass
        return task.cont
# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Simulators.Board]
# Desc: Board Game Simulators Library - CheckerBoard Class
# File name: CheckerBoard.py
# Developed by: Project Eden Development Team
# Date: 21/08/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from Eden.Eden3D.Simulators.Board.Board_8x8 import Board_8x8
from Eden.Eden3D.Simulators.Board.checkers_globals import *
from random import randint
# ---------------------------------------------
# A class that implements a basic world with a 
# checkerboard in it. Entry point for a checkers game.
# Startup options are loaded from config.xml
# Class definition for the CheckerBoard class
# ---------------------------------------------
class CheckerBoard(Board_8x8):
    " Extends Board_8x8 for checkers game boards "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, remoteStarterTask = None, ignorePicker = False, \
            versusAI = False, customPRC = None, edenClass = 'CheckerBoard'):
        # ancestral constructor
        Board_8x8.__init__(self, remoteStarterTask, ignorePicker, versusAI, \
            customPRC, edenClass)
        # compute valid positions on board
        self.initTiles()
        # checkers
        self.checkersPieces = [self.XPU.Parser['XML_Values']['Pieces_Values'] \
            ['manBlack'], self.XPU.Parser['XML_Values']['Pieces_Values']['manWhite'], \
            self.XPU.Parser['XML_Values']['Pieces_Values']['kingBlack'], \
            self.XPU.Parser['XML_Values']['Pieces_Values']['kingWhite']]
        self.setupPieces()
        # initialize system
        # 1 - occupied
        # 0 - free
        self.board = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, \
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        # initialize player armies (tile, isKing)
        playerBlack = {'b1':[1, False], 'b2':[2, False], 'b3':[3, False], \
            'b4':[4, False], 'b5':[5, False], 'b6':[6, False], 'b7':[7, False], \
            'b8':[8, False], 'b9':[9, False], 'b10':[10, False], 'b11':[11, False], \
            'b12':[12, False]}
        playerWhite = {'w1':[32, False], 'w2':[31, False], 'w3':[30, False], \
            'w4':[29, False], 'w5':[28, False], 'w6':[27, False], 'w7':[26, False], \
            'w8':[25, False], 'w9':[24, False], 'w10':[23, False], 'w11':[22, False], \
            'w12':[21, False]}
        self.armies = [playerBlack, playerWhite]
        # for the move and capture computations
        self.hardCodes = {'whiteMoves':whiteMoves, 'blackMoves':blackMoves, \
            'kingMoves':kingMoves, 'whiteCaptures':whiteCaptures, \
            'blackCaptures':blackCaptures, 'kingCaptures':kingCaptures}
        self.hKeys = ['blackMoves', 'whiteMoves', 'blackCaptures', 'whiteCaptures']
        self.kingRows = [whiteKings, blackKings]
        self.capFlag = False
        # for AI agents
        self.agentList = {'bruteFirst':self.bruteFirstAgent, \
            'bruteRandom':self.bruteRandomAgent}
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    # ------------------MOVES------------------------
    def movePiece(self, dest):
        " moves the active piece from src to dest "
        # destination has already been checked by computeMoves
        if self.board[dest - 1] == 0:
            # save source tile
            t_src = self.activePiece[1][0]
            # move the piece
            self.armies[self.sideTurn][self.activePiece[0]][0] = dest
            self.objectStore[self.activePiece[0]] \
                [0].setPos(self.gamePositions[dest - 1][1], self.gamePositions[dest - 1] \
                [0], 0.0)
            # update tiles
            self.board[t_src - 1] = 0
            self.board[dest - 1] = 1
            # check for king
            if dest in self.kingRows[self.sideTurn]:
                if self.armies[self.sideTurn][self.activePiece[0]][1] == False:
                    self.armies[self.sideTurn][self.activePiece[0]][1] = True
                    # update to king model
                    self.crownKing(self.activePiece[0])
                    self.systemMessage("King!", [self.sideTurn, self.activePiece[0]], \
                        'kingEvent')
            self.systemMessage("Successful move", self.sideTurn, 'pieceMove')
            # change side
            if self.sideTurn == 1:
                self.sideTurn = 0
            else:
                self.sideTurn = 1
            if self.autoFlip == True:
                # turn the board
                self.turnBoard()
            self.activePiece = None
            return True
        else:
            self.activePiece = None
            self.systemMessage("Invalid move!")
            return False
    def computeMoves(self, piece, side):
        " computes all the possible moves a piece can make "
        # initialize
        capCheckFlag = False
        t_try = self.parseHardCodes(side, piece)
        t_ctry = self.parseHardCodes(side, piece, True)
        if len(t_ctry) != 0:
            capCheckFlag = True
        t_free = []
        # check for capture first
        if capCheckFlag == True:
            t_capt = self.computeCapture(side, t_ctry)
            if self.capFlag == True and t_capt != None:
                # capture is mandatory; reset flag after effecting capture
                return t_capt
            else:
                # no capture is possible
                pass
        for t_x in t_try:
            if self.board[t_x - 1] == 0:
                # add to the list of valid move destinations
                t_free.append(t_x)
        if len(t_free) == 0:
            # the piece/king can't move
            return None
        else:
            return t_free
    # ------------------CAPTURE----------------------
    def computeCapture(self, side, capList):
        " computes whether a piece has a valid capture "
        # check for capture
        t_clist = []
        for t_c in capList:
            # check if destination is free
            if self.board[t_c[0] - 1] == 0:
                # check if capture tile is not free
                if self.board[t_c[1] - 1] == 1:
                    # the tile must be occupied by the enemy
                    t_g = self.checkOccupant(t_c[1])
                    if t_g[0] != side:
                        # a capture is possible
                        self.capFlag = True
                        t_clist.append(t_c)
                    else:
                        # not a valid capture
                        pass
        else:
            # a capture is not possible
            self.capFlag = False
        if len(t_clist) == 0:
            # the piece can't capture
            # reset capFlag
            self.capFlag = False
            return None
        else:
            self.capFlag = True
            return t_clist
    # ------------------SELECT-----------------------
    def processSelection(self):
        " process a mouse piece selection event "
        if self.currentSelection in self.armies[0].keys():
            t_t = 0
        else:
            t_t = 1
        # reset capFlag; just in case
        self.capFlag = False
        t_r = self.selectPiece(t_t, self.currentSelection)
        if t_r == True:
            # activate piece
            self.mouseDownFlag = True
            if self.hudPresent == True:
                # update the HUD
                t_s = self.currentSelection + ' selected'
                self.hudBrush.menuList['Game']['labels']['Piece']['text'] = t_s
            self.currentSelection = ''
    def processDrop(self):
        " process a mouse piece drop event "
        # exit if mouse has been clicked someplace else
        if self.activePiece == None:
            return False
        # check if this is a valid position
        t_x = self.objectStore[self.activePiece[0]][0].getX()
        t_y = self.objectStore[self.activePiece[0]][0].getY()
        t_d = 0
        t_f = False
        # define bounds
        if t_x < self.boardColumns[0]:
            # left border
            t_x = self.boardColumns[0]
        elif t_x > self.boardColumns[7]:
            # right border
            t_x = self.boardColumns[7]
        if t_y > self.boardRows[7]:
            # top border
            t_y = self.boardRows[7]
        elif t_y < self.boardRows[0]:
            # bottom border
            t_y = self.boardRows[0]
        for t_v, t_g in enumerate(self.gamePositions):
            # check for columns
            if t_x == t_g[1]:
                # check for rows allowed
                t_f = True
            elif (t_g[1] - self.tileSize / self.dropFactor) <= t_x and (t_g[1] + \
                self.tileSize / self.dropFactor) >= t_x:
                # check for rows allowed
                t_f = True
            else:
                # check for rows not necessary, columns failed
                t_f = False
            if t_f == True:
                # check for rows
                if t_y == t_g[0]:
                    t_d = t_v + 1
                    break
                elif (t_g[0] - self.tileSize / self.dropFactor) <= t_y and (t_g[0] + \
                    self.tileSize / self.dropFactor) >= t_y:
                    t_d = t_v + 1
                    break
                else:
                    # rows check failed
                    t_f = False
        # if no valid position was encountered then t_d is still 0
        if t_d == 0:
            t_r = False
        else:
            # set position
            t_r = self.selectDestination(t_d)
        if t_r == False:
            # return to origin
            t_tp = self.gamePositions[self.activePiece[1][0] - 1]
            self.objectStore[self.activePiece[0]][0].setX(t_tp[1])
            self.objectStore[self.activePiece[0]][0].setY(t_tp[0])
        self.mouseDownFlag = False
        # update the HUD
        t_s = 'None Selected'
        self.hudBrush.menuList['Game']['labels']['Piece']['text'] = t_s
        self.currentSelection = ''
        return True
    def selectPiece(self, side, piece, serialSelect = False):
        " computes legal moves when a piece is selected "
        if self.sideTurn != side:
            self.systemMessage("Not your turn!")
            return False
        elif self.drawFlag == True or self.victoryFlag == True:
            # the game is over
            self.systemMessage("Game Over!")
            return False
        else:
            # compute the moves
            self.legalMoves = self.computeMoves(piece, side)
            if self.legalMoves == None:
                # check for a draw
                for t_dt in self.armies[side].keys():
                    if t_dt == piece:
                        # don't check for currently active piece
                            pass
                    else:
                        t_lm = self.computeMoves(t_dt, side)
                        if t_lm != None:
                            # there is a valid move in the game
                            break
                        else:
                            # reset capFlag and go to next piece    
                            self.capFlag = False
                else:
                    # we've not found a single piece that can move
                    self.drawFlag = True
                    self.systemMessage("Game is lost, no valid moves!", 0, 'drawEvent')
                    return False
                # reset capFlag
                self.capFlag = False
                self.systemMessage("No valid move!")
                return False
            else:
                if serialSelect == False and self.capFlag != True:
                    # we must check if any other piece can capture
                    t_legalPieces = []
                    for t_j in self.armies[side].keys():
                        if t_j == piece:
                            # don't check for currently active piece
                            pass
                        else:
                            # check if it is a capturable position
                            t_scl = self.parseHardCodes(side, t_j, True)
                            if len(t_scl) == 0:
                                # not a capturing position
                                pass
                            else:
                                self.computeCapture(side, t_scl)
                        # add to list of capturers and reset capFlag for next piece
                        if self.capFlag == True:
                            t_legalPieces.append(t_j)
                            self.capFlag = False
                    if len(t_legalPieces) == 0:
                        # it is valid to use current piece    
                        pass
                    else:
                        self.systemMessage("Capture is mandatory!")
                        return False
                # we must remember to reset capFlag if true at this point
                # but only after we move
                self.activePiece = [piece, self.armies[side][piece]]
                self.systemMessage("Valid moves computed!", self.legalMoves)
                return True
    def selectDestination(self, dest):
        " executes a move to a specified destination if valid "
        # can only be called if self.legalMoves has a valid list
        if self.legalMoves == None:
            self.systemMessage("No valid move to execute!")
            return False
        if self.capFlag != True:
            # normal move
            if dest in self.legalMoves:
                # execute the move
                t_b = self.movePiece(dest)
                if t_b == True:
                    self.legalMoves = None
                    self.systemMessage("Successful move to destination")
                    return True
                else:
                    # this should never happen; movePiece() will have a
                    # system message
                    return False
            else:
                self.systemMessage("Invalid destination")
                return False
        else:
            # capture move
            # variables for checking serial capture
            ts_side = 0
            ts_piece = self.activePiece[0]
            for t_x in self.legalMoves:
                if dest == t_x[0]:
                    # execute the move
                    t_b = self.movePiece(dest)
                    if t_b == True:
                        # remove the captured piece
                        self.board[t_x[1] - 1] = 0
                        # movePiece has already changed the sideTurn
                        t_y = self.checkOccupant(t_x[1])
                        # remove the captured piece
                        del self.armies[t_y[0]][t_y[1]]
                        self.objectStore[t_y[1]][0].removeNode()
                        del self.objectStore[t_y[1]]
                        self.systemMessage("Deleted", [t_y[0], t_y[1]])
                        # check for win
                        if len(self.armies[t_y[0]]) == 0:
                            self.victoryFlag = True
                        # store original side before move
                        if t_y[0] == 0:
                            ts_side = 1
                        else:
                            ts_side = 0
                        # halt if victory
                        if self.victoryFlag == True:
                            self.systemMessage("Victory", ts_side, 'victoryEvent')
                            return True
                        self.legalMoves = None
                        # reset capFlag
                        self.capFlag = False
                        self.systemMessage("Successful capture", ts_side, 'captureEvent')
                        # check for possibility of serial capture   
                        ts_cl = self.parseHardCodes(ts_side, ts_piece, True)
                        if len(ts_cl) != 0:
                            ts_check = True
                        else:
                            ts_check = False
                        if ts_check == True:
                            self.computeCapture(ts_side, ts_cl)
                        # the function only modifies self.capFlag
                        if self.capFlag == False:
                            # no new capture, just end
                            return True
                        else:
                            # serial capture is mandatory
                            # reset capFlag
                            self.capFlag = False
                            self.sideTurn = ts_side
                            if self.autoFlip == True:
                                # turn the board
                                self.turnBoard()
                            self.selectPiece(ts_side, ts_piece, True)
                            self.systemMessage("Serial capture set up", [ts_side, \
                                ts_piece])
                            return True
                    else:
                        # this should never happen; movePiece() will have a
                        # system message
                        return False
            else:
                self.systemMessage("Invalid destination")
                return False
    # ------------------AI / RULES / REPLAY SERVICES------------------
    def checkOccupant(self, tile):
        " checks the occupant of a tile and returns (side, piece) "
        for t_y in self.armies[0].keys():
            if self.armies[0][t_y][0] == tile:
                # return the piece
                return (0, t_y)
        for t_z in self.armies[1].keys():
            if self.armies[1][t_z][0] == tile:
                # return the piece
                return (1, t_z)
        # if the tile is free    
        return None
    def parseHardCodes(self, side, piece, capturer = False):
        " returns the moves available to a piece from hardcodes "
        if capturer == False:
            t_1 = 'kingMoves'
            t_2 = 4
            t_3 = 0
        else:
            t_1 = 'kingCaptures'
            t_2 = 0
            t_3 = 2
        if self.armies[side][piece][1] == False:
            # non-kings
            # check for trivial cases first to make quick exit
            if side == 0:
                if capturer == True:
                    # the piece must fall in the range
                    # black capture positions are 1 to 24
                    if self.armies[side][piece][0] not in range(1, 25):
                        return []
                # black positions are 1 to 28
                t_c = self.armies[side][piece][0] - 1
            else:
                if capturer == True:
                    # the piece must fall in the range
                    # white capture positions are 32 to 9
                    if self.armies[side][piece][0] not in whiteCapTiles:
                        return []
                # white positions are from 32 to 5
                t_c = self.armies[side][piece][0] - (9 - t_2)
                # 32 => 0 while 9 => 23 in the list
                t_c = (23 + t_2) - t_c
            return self.hardCodes[self.hKeys[side + t_3]][t_c]
        else:
            # kings
            t_c = self.armies[side][piece][0] - 1
            return self.hardCodes[t_1][t_c]
    def processMoveEvent(self, side, piece, dest):
        " attempts a move on the board "
        t_fback = self.effectMove(side, piece, dest)
        if t_fback == True:
            # successful move
            if self.recordGame == True:
                # record move
                self.logData['movesList'].append((side, piece, dest))
            # enter code for graphics and sound here
            return True
        else:
            # unsuccessful move
            # enter code for graphics and sound here
            return False
    def effectMove(self, side, piece, dest):
        " effect a move on the board "
        t_res = self.selectPiece(side, piece)
        if t_res == True:
            t_res = self.selectDestination(dest)
            return t_res
        else:
            self.systemMessage("Not allowed!")
            return False
    def generateAIMove(self):
        " generates an AI move on the board and calls processMoveEvent "
        # do a trial and error to get valid pieces
        t_val = []
        t_caps = []
        for t_x in self.armies[self.sideTurn].keys():
            # select the piece
            t_b = self.selectPiece(self.sideTurn, t_x)
            if t_b == True:
                t_val.append(t_x)
                if self.capFlag == True:
                    t_caps.append(t_x)
                    self.capFlag = False
        # at this point we have only valid moves; reset the vital vars
        self.activePiece = None
        self.capFlag = False
        self.legalMoves = None
        if len(t_caps) > 0:
            self.agentList[self.activeAgent](t_caps, True)
        else:
            self.agentList[self.activeAgent](t_val)
    # ------------------AGENTS------------------
    def bruteFirstAgent(self, validPieces, captureMoves = False):
        " effects the first valid move by brute force heuristics for the current side "
        # pick the first piece to move
        for t_a in validPieces:
            t_d = self.parseHardCodes(self.sideTurn, t_a, captureMoves)
            # the location to move the selected piece to
            # (we go with the first successful one)
            for t_e in t_d:
                if captureMoves == True:
                    t_f = self.effectMove(self.sideTurn, t_a, t_e[0])
                else:
                    t_f = self.effectMove(self.sideTurn, t_a, t_e)
                t_o = t_f
                if t_f == True:
                    break
            if t_o == True:
                # executed a move successfully
                break
    def bruteRandomAgent(self, validPieces, captureMoves = False):
        " effects a random valid move by brute force heuristics for the current side "
        t_lc = len(validPieces)
        # randomize the piece to move
        if t_lc == 1:
            t_a = validPieces[0]
        else:
            t_a = validPieces[randint(0, t_lc - 1)]
        t_d = self.parseHardCodes(self.sideTurn, t_a, captureMoves)
        self.randomAgentUtility(t_d, t_a, captureMoves)
    def randomAgentUtility(self, agentHardCodes, pieceChoice, captureMoves):
        " common code for the random agents "
        # the location to move the selected piece to
        # randomize the location to move to
        t_ld = len(agentHardCodes)
        t_f = False
        if t_ld == 1:
            t_e = agentHardCodes[0]
        else:
            t_e = agentHardCodes[randint(0, t_ld - 1)]
        while t_f == False:
            if captureMoves == True:
                t_f = self.effectMove(self.sideTurn, pieceChoice, t_e[0])
            else:
                t_f = self.effectMove(self.sideTurn, pieceChoice, t_e)
            # randomize again
            t_e = agentHardCodes[randint(0, t_ld - 1)]
    # ------------------BOARD SETUP------------------
    def setupPieces(self):
        " sets up pieces for a checkers game "
        # load pieces and arrange on board
        t_d = {'parentNode':self.world, 'bitMask':None, 'sphereFactor':1.0, \
               'enablePhysics':False, 'objectMass':0, 'terrainDetection':False}
        t_p = [0.0, 0.0, 0.0]
        for t_x in range(1, 13):
            # arrange the pieces
            t_z = 'b' + str(t_x)
            t_p[0] = self.gamePositions[t_x - 1][1]
            t_p[1] = self.gamePositions[t_x - 1][0]
            self.loadGeometry(self.checkersPieces[0], t_z, self.pieceScale, \
                t_p, extraData = t_d)
            # clear parent texture
            if self.pieceTextures['black'] != None:
                self.objectStore[t_z][0].clearTexture()
                self.objectStore[t_z][0].setTexture(self.pieceTextures['black'], 1)
            # set the picker tag
            if self.pickingFlag == True:
                self.objectStore[t_z][0].setTag(self.pickerTag, t_z)
        for t_y in range(1, 13):
            # arrange the pieces
            t_z = 'w' + str(t_y)
            t_p[0] = self.gamePositions[32 - t_y][1]
            t_p[1] = self.gamePositions[32 - t_y][0]
            self.loadGeometry(self.checkersPieces[1], t_z, self.pieceScale, \
                t_p, extraData = t_d)
            # clear parent texture
            if self.pieceTextures['white'] != None:
                self.objectStore[t_z][0].clearTexture()
                self.objectStore[t_z][0].setTexture(self.pieceTextures['white'], 1)
            # set the picker tag
            if self.pickingFlag == True:
                self.objectStore[t_z][0].setTag(self.pickerTag, t_z)
    def crownKing(self, piece):
        " updates a model to the king model "
        t_d = {'parentNode':self.world, 'bitMask':None, 'sphereFactor':1.0, \
               'enablePhysics':False, 'objectMass':0, 'terrainDetection':False}
        t_t = self.armies[self.sideTurn][self.activePiece[0]][0]
        t_y = self.gamePositions[t_t - 1]
        t_p = [t_y[1], t_y[0], 0.0]
        self.objectStore[piece][0].removeNode()
        del self.objectStore[piece]
        self.loadGeometry(self.checkersPieces[self.sideTurn + 2], piece, self.pieceScale, \
                t_p, extraData = t_d)
        t_j = ['black', 'white']
        t_v = t_j[self.sideTurn]
        # clear parent texture
        if self.pieceTextures[t_v] != None:
            self.objectStore[piece][0].clearTexture()
            self.objectStore[piece][0].setTexture(self.pieceTextures[t_v], 1)
        # set the picker tag
        if self.pickingFlag == True:
            self.objectStore[piece][0].setTag(self.pickerTag, piece)
    # ------------------SYSTEM SERVICES-----------------
    # ----------------------------------------------------
    def initTiles(self):
        " computes the co-ords of the valid tiles( row, column ) for checkers "
        # call ancestral function
        self.computeTiles()
        # checkers
        self.gamePositions = []
        for t_x in range(8):
            for t_y in range(4):
                if t_x % 2 == 0:
                    # for even rows - column 6, 4, 2, 0
                    self.gamePositions.append((self.boardRows[t_x], \
                        self.boardColumns[6 - (t_y * 2)]))
                else:
                    # for odd rows - column 7, 5, 3, 1
                    self.gamePositions.append((self.boardRows[t_x], \
                        self.boardColumns[7 - (t_y * 2)]))
# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Simulators.Board]
# Desc: Board Game Simulators Library - ChessBoard Class
# File name: ChessBoard.py
# Developed by: Project Eden Development Team
# Date: 21/08/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from Eden.Eden3D.Simulators.Board.Board_8x8 import Board_8x8
# ---------------------------------------------
# A class that implements a basic world with a 
# chessboard in it. Entry point for a chess game.
# Startup options are loaded from config.xml
# Class definition for the ChessBoard class
# ---------------------------------------------
class ChessBoard(Board_8x8):
    " Extends Board_8x8 for chess game boards "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, remoteStarterTask = None, ignorePicker = False, \
            versusAI = False, customPRC = None, edenClass = 'ChessBoard'):
        # ancestral constructor
        Board_8x8.__init__(self, remoteStarterTask, ignorePicker, edenClass)
        # compute valid positions on board
        self.initTiles()
        # chess
        self.chessPieces = [self.XPU.Parser['XML_Values']['Pieces_Values']['king'], \
        self.XPU.Parser['XML_Values']['Pieces_Values']['queen'], \
        self.XPU.Parser['XML_Values']['Pieces_Values']['rook'], \
        self.XPU.Parser['XML_Values']['Pieces_Values']['bishop'], \
        self.XPU.Parser['XML_Values']['Pieces_Values']['knight'], \
        self.XPU.Parser['XML_Values']['Pieces_Values']['pawn']]
        self.setupPieces()
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    def setupPieces(self):
        " sets up pieces for a chess game "
        # build the path to the static objects (non-animated)
        t_m = self.gameMVC.mvcStructure['tier_models']['geometry'] + '/'
        # initialize the pieces list
        t_l = ['king','queen','rook','bishop','knight','pawn']
        # load pieces and arrange on board
    # --------------------------RESOURCE LOADING-----------------------------
    # ------------------SYSTEM SERVICES-----------------
    # ----------------------------------------------------
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
    def initTiles(self):
        " computes the co-ords of the valid tiles( row, column ) for chess "
        # call ancestral function
        self.computeTiles()
        # chess
        pass
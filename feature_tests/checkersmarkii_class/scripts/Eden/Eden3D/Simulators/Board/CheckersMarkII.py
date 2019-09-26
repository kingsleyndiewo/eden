# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Simulators.Board]
# Desc: Board Game Simulators Library - CheckersMarkII Class
# File name: CheckersMarkII.py
# Developed by: Project Eden Development Team
# Date: 30/05/2009
# Place: Nairobi, Kenya
# Copyright: (C)2009 Funtrench Limited
# ---------------------------------------------
from Eden.Eden3D.Simulators.Board.CheckerBoard import CheckerBoard
from random import randint
# ---------------------------------------------
# A class that implements a basic world with a 
# checkerboard in it. Entry point for a board game.
# Startup options are loaded from config.xml
# Class definition for the CheckerBoard class
# ---------------------------------------------
class CheckersMarkII(CheckerBoard):
    " Extends CheckerBoard for advanced AI agents "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, remoteStarterTask = None, ignorePicker = False, \
            versusAI = False, customPRC = None, edenClass = 'CheckersMarkII'):
        # ancestral constructor
        CheckerBoard.__init__(self, remoteStarterTask, ignorePicker, versusAI, \
            customPRC, edenClass)
        # add AI agents
        self.agentList['safeRandom'] = self.safeRandomAgent
        self.agentList['smartRandom'] = self.smartRandomAgent
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    # ------------------AI / REPLAY SERVICES------------------
    def checkDanger(self, pieceTile):
        " checks if the piece argued is in jeopardy "
        if self.sideTurn == 0:
            t_st = 1
        else:
            t_st = 0
        for t_p in self.armies[t_st]:
            # check the capture hardcodes
            t_dl = self.parseHardCodes(t_st, t_p, True)
            if len(t_dl) != 0:
                # check if this piece's tile is the target of the capture
                for t_dx in t_dl:
                    if t_dx[1] == pieceTile:
                        # check if the destination is empty
                        if self.board[t_dx[0] - 1] == 0:
                            # danger on this tile
                            return True
                        else:
                            # right tile but capture not possible
                            pass
                    else:
                        # wrong tile
                        pass
            else:
                # not a capturing piece
                pass
        else:
            # we run out of enemies without a threat
            return False
                
    def checkTileHazard(self, piece):
        " checks if any of the valid moves of the piece argued lead to danger "
        t_hcd = self.parseHardCodes(self.sideTurn, piece)
        t_dt = []
        for t_y in t_hcd:
            t_b = self.checkDanger(t_y)
            if t_b == True:
                t_dt.append(t_y)
        # return a list of the danger tiles
        return t_dt
    # ------------------AGENTS------------------
    def safeRandomAgent(self, validPieces, captureMoves = False):
        " effects a random move but escapes danger "
        if captureMoves == False:
            # check if piece is in danger
            t_pm = []
            for t_x in validPieces:
                t_bl = self.checkDanger(self.armies[self.sideTurn][t_x][0])
                if t_bl == True:
                    # priority move
                    t_pm.append(t_x)
            if len(t_pm) > 0:
                # we must move a priority move
                validPieces = t_pm
        t_lc = len(validPieces)
        # randomize the piece to move
        if t_lc == 1:
            t_a = validPieces[0]
        else:
            t_a = validPieces[randint(0, t_lc - 1)] 
        t_d = self.parseHardCodes(self.sideTurn, t_a, captureMoves)
        self.randomAgentUtility(t_d, t_a, captureMoves)
    def smartRandomAgent(self, validPieces, captureMoves = False):
        " effects a random move but escapes danger "
        if captureMoves == False:
            # check if piece is in danger
            t_pm = []
            for t_x in validPieces:
                t_bl = self.checkDanger(self.armies[self.sideTurn][t_x][0])
                if t_bl == True:
                    # priority move
                    t_pm.append(t_x)
            if len(t_pm) > 0:
                # we must move a priority move
                validPieces = t_pm
            # check for hazardous tiles
            t_hz = []
            for t_x in validPieces:
                t_hz.append(self.checkTileHazard(t_x))
        t_lc = len(validPieces)
        # randomize the piece to move
        if t_lc == 1:
            t_a = validPieces[0]
            t_r = 0
        else:
            if captureMoves == True:
                t_a = validPieces[randint(0, t_lc - 1)]
            else:
                # check that we don't have danger tiles only
                t_f = False
                # store the list because we're deleting stuff
                t_bvp = validPieces
                while t_f == False:
                    t_r = randint(0, t_lc - 1)
                    t_a = validPieces[t_r]
                    t_dhc = self.parseHardCodes(self.sideTurn, t_a)
                    if len(t_dhc) > len(t_hz[t_r]):
                        # at least 1 safe move exists for this piece
                        t_f = True
                    elif len(validPieces) == 1:
                        # we have removed up to only one piece
                        # last man standing is what we use to
                        # avoid deleting everything
                        t_f = True
                    else:
                        # remove the piece
                        validPieces.remove(t_a)
        t_d = self.parseHardCodes(self.sideTurn, t_a, captureMoves)
        if captureMoves != True:
            # delete unwanted moves
            if len(t_hz[t_r]) != 0 and len(t_d) > len(t_hz[t_r]):
                for t_xv in t_hz[t_r]:
                    t_d.remove(t_xv)
        self.randomAgentUtility(t_d, t_a, captureMoves)
    
# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Simulators.Board]
# Desc: Board Game Simulators Library - Global defines for CheckerBoard Class
# AI knowledge-base file for CheckerBoard Class
# File name: CheckerBoard.py
# Developed by: Project Eden Development Team
# Date: 16/05/2012
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
# AI knowledge-base file
        #   +---+---+---+---+---+---+---+---+
        #   |   |[w]|   |[w]|   |[w]|   |[w]|
        #   +---+32-+---+31-+---+30-+---+29-+
        #   |[w]|   |[w]|   |[w]|   |[w]|   |
        #   +28-+---+27-+---+26-+---+25-+---+
        #   |   |[w]|   |[w]|   |[w]|   |[w]|
        #   +---+24-+---+23-+---+22-+---+21-+
        #   |[ ]|   |[ ]|   |[ ]|   |[ ]|   |
        #   +20-+---+19-+---+18-+---+17-+---+
        #   |   |[ ]|   |[ ]|   |[ ]|   |[ ]|
        #   +---+16-+---+15-+---+14-+---+13-+
        #   |[b]|   |[b]|   |[b]|   |[b]|   |
        #   +12-+---+11-+---+10-+---+9--+---+
        #   |   |[b]|   |[b]|   |[b]|   |[b]|
        #   +---+8--+---+7--+---+6--+---+5--+
        #   |[b]|   |[b]|   |[b]|   |[b]|   |
        #   +4--+---+3--+---+2--+---+1--+---+
# [b]  a black piece
# [B]  a black king
# [w]  a white piece
# [W]  a white king
# [ ]  an unoccupied dark square
# initialize player king rows
whiteKings = [29, 30, 31, 32]
blackKings = [1, 2, 3, 4]
# hardcode piece move possibilities for efficiency (dest1, dest2)
# white moves run from tile 28 to 1 - king row can't be moved to (28 possibilities)
whiteMoves = [(28, 27), (27, 26), (26, 25), (25,), (24,), (24, 23), \
    (23, 22), (22, 21), (20, 19), (19, 18), (18, 17), (17,), (16,), \
    (16, 15), (15, 14), (14, 13), (12, 11), (11, 10), (10, 9), (9,), (8,), \
    (8 ,7), (7, 6), (6, 5), (4, 3), (3, 2), (2, 1), (1,)]
# black moves run from tile 5 to 32 - king row can't be moved to (28 possibilities)
blackMoves = [(5, 6), (6, 7), (7, 8), (8,), (9,), (9, 10), (10, 11), \
    (11, 12), (13, 14), (14, 15), (15, 16), (16,), (17,), (17, 18), \
    (18, 19), (19, 20), (21, 22), (22, 23), (23, 24), (24,), (25,), \
    (25, 26), (26, 27), (27, 28), (29, 30), (30, 31), (31, 32), (32,)]
# hardcode king move possibilities for efficiency (dest1, dest2, dest3, dest4)
# kings can move onto all tiles (32 possibilities)
kingMoves = [(5, 6), (6, 7), (7, 8), (8, 8), (1, 9), (9, 10, 1, 2), (10, 11, 3, 2), \
    (11, 12, 4, 3), (13, 14, 6, 5), (14, 15, 7, 6), (15, 16, 7, 8), (16, 8), (17, 9), \
    (17, 18, 9, 10), (18, 19, 10, 11), (19, 20, 11, 12), (21, 22, 13, 14), \
    (22, 23, 14, 15), (23, 24, 15, 16), (24, 16), (25, 17), (25, 26, 17, 18), \
    (26, 27, 18, 19), (27, 28, 19, 20), (29, 30, 21, 22), (30, 31, 22, 23), \
    (31, 32, 23, 24), (32, 24), (25,), (25, 26), (26, 27), (27, 28)]
# hardcode capture possibilities for efficiency ((dest1, capt1), (dest2, capt2))
# white can capture only from tiles 32 to 9
whiteCapTiles = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, \
    26, 27, 28, 29, 30, 31, 32]
whiteCaptures = [((23, 27),), ((24, 27), (22, 26)), ((23, 26), (21, 25)), \
    ((22, 25),), ((19, 24),), ((20, 24), (18, 23)), ((19, 23), (17, 22)), \
    ((18, 22),), ((15, 19),), ((16, 19), (14, 18)), ((15, 18), (13, 17)), \
    ((14, 17),), ((11, 16),), ((12, 16), (10, 15)), ((11, 15), (9, 14)), \
    ((10, 14),), ((7, 11),), ((8, 11), (6, 10)), ((7, 10), (5, 9)), \
    ((6, 9),), ((3, 8),), ((4, 8), (2, 7)), ((3, 7), (1, 6)), ((2, 6),)]
# black can capture only from tiles 1 to 24
blackCaptures = [((10, 6),), ((9, 6), (11, 7)), ((10, 7), (12, 8)), ((11, 8),), \
    ((14, 9),), ((13, 9), (15, 10)), ((14, 10), (16, 11)), ((15, 11),), ((18, 14),), \
    ((17, 14), (19, 15)), ((18, 15), (20, 16)), ((19, 16),), ((22, 17),), \
    ((21, 17), (23, 18)), ((22, 18), (24, 19)), ((23, 19),), ((26, 22),), \
    ((25, 22), (27, 23)), ((26, 23), (28, 24)), ((27, 24),), ((30, 25),), \
    ((29, 25), (31, 26)), ((30, 26), (32, 27)), ((31, 27),)]
# kings can capture onto all tiles
# from 1 to 8 kings follow black
# from 9 to 24 kings are a union of white and black
# from 25 to 32 kings follow white
kingCaptures = [((10, 6),), ((9, 6), (11, 7)), ((10, 7), (12, 8)), ((11, 8),), \
    ((14, 9),), ((13, 9), (15, 10)), ((14, 10), (16, 11)), ((15, 11),), \
    ((18, 14), (2, 6)), ((17, 14), (19, 15), (3, 7), (1, 6)), \
    ((18, 15), (20, 16), (4, 8), (2, 7)), ((19, 16), (3, 8)), ((22, 17), (6, 9)), \
    ((21, 17), (23, 18), (7, 10), (5, 9)), ((22, 18), (24, 19), (8, 11), (6, 10)), \
    ((23, 19), (7, 11)), ((26, 22), (10, 14)), ((25, 22), (27, 23), (11, 15), (9, 14)), \
    ((26, 23), (28, 24), (12, 16), (10, 15)), ((27, 24), (11, 16)), ((30, 25), (14, 17)), \
    ((29, 25), (31, 26), (15, 18), (13, 17)), ((30, 26), (32, 27), (16, 19), (14, 18)), \
    ((31, 27), (15, 19)), ((18, 22),), ((19, 23), (17, 22)), ((20, 24), (18, 23)), \
    ((19, 24),), ((22, 25),), ((23, 26), (21, 25)), ((24, 27), (22, 26)), ((23, 27),)]
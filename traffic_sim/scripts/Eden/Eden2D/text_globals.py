# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden2D]
# Desc: Text Rendering Library - Global defines for Text2D Class
# File name: text_globals.py
# Developed by: Project Eden Development Team
# Date: 29/06/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from pandac.PandaModules import *
# ---------------------------------------------
# -----------------------NOTES------------------------------
# ----------------------------------------------------------
#   info on the property dictionary (class attribute)
#   a scale of 0.004 is about 1 pt
#   small caps allows capital letters of a smaller
#   scale instead of lowercase letters. The scale is
#   relative to the uppercase letters. 0.8 is default
#   slant of 1.0 is 45 degrees rightward, 0.0 is none
#   negative values for a leftward slant.
#   default color is white
#   default shadow offset is [0.05, 0.05]; the offset is
#   in screen units right and down
#   wordwrap is the line width in screen units
# ----------------------------------------------------------
# ----------------------Default Dictionary------------------
EdenDefaultProperties = {'Scale':0.004, 'FontSize':11.0, 'SmallCaps':False, \
    'SmallCapsScale':0.75, 'Slant':0.0, 'Color':Vec4(1,1,1,1), 'Shadow':[0.05, 0.05], \
    'ShadowColor':[0,0,0,1], 'WordWrap':15.0, 'Alignment':TextNode.ALeft, \
    'FrameColor':[0,0,0,1], 'FrameMargin':[0.2,0.2,0.2,0.2], 'CardColor':[1,1,1,1], \
    'CardMargin':[0.2,0.2,0.2,0.2], 'ShadowFlag':False, \
    'WrapFlag':False, 'FrameFlag':False, 'CardFlag':False, \
    'Position':(-1.30,0,0.97), 'Duplicates':True }
# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden  [Eden2D]
# Desc: Visuals Rendering Library - Glass2D Class
# File name: Glass2D.py
# Developed by: Project Eden Development Team
# Date: 15/08/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from Eden.Eden2D.Menu2D import Menu2D
# ---------------------------------------------
# A class to handle the drawing of 2D head-up displays.
# GIF images are not supported! Use PNG or TGA
# Class definition for the Glass2D class
# ---------------------------------------------
class Glass2D(Menu2D):
    " Extends Menu2D for 2D HUD systems; glass is from glass cockpits "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, proxyMVC):
        Menu2D.__init__(self, proxyMVC) # ancestral constructor
        # modify the path to point to the HUD folder
        self.menuPath = self.targetMVC.mvcStructure['config'] + '/huds/'
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    # ------------------HUD LOADING  & MANIPULATION------
    def loadHUD(self, glassXML, callBackList):
        " loads a HUD to the list; wrapper function "
        # for now this is just a proxy function but we might add HUD-specific
        # material later
        self.loadMenu(glassXML, callBackList)
    def showGlass(self, glassName):
        " makes a hidden HUD visible "
        self.showMenu(glassName)
    def hideGlass(self, glassName):
        " makes a visible HUD invisible "
        self.hideMenu(glassName)
    # -----------------------------------------------------------------------
    # --------------------------INTERNAL BEHAVIOURS--------------------------
    
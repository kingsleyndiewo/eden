# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden2D]
# Desc: Visuals Rendering Library - Menu2D Class
# File name: Menu2D.py
# Developed by: Project Eden Development Team
# Date: 08/08/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from direct.gui.DirectGui import *
from direct.gui import DirectGuiGlobals
from Eden.EdenTools.XMLParsers.ConfigParser import ConfigParser
from pandac.PandaModules import *
# ---------------------------------------------
# A class to handle the drawing of 2D menus.
# GIF images are not supported! Use PNG or TGA
# Class definition for the Menu2D class
# ---------------------------------------------
class Menu2D:
    " The base class for all 2D menu systems "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, proxyMVC):
        # save the reference to the gameMVC
        self.targetMVC = proxyMVC
        # build a path to the menus folder
        self.menuPath = self.targetMVC.mvcStructure['config'] + '/menus/'
        # create the menu configuration parser
        self.menuXPU = ConfigParser()
        # initialize the menu list
        self.menuList = {}
        # the string for any empty CSV list
        self.emptyList = 'NULL'
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    # ------------------MENU LOADING  & MANIPULATION------
    def loadMenu(self, menuXML, callBackList):
        " loads a menu to the list "
        # store the callback functions list
        self.callBacks = callBackList
        # parse menu details XML (XPU = XML processing unit)
        self.menuXPU.parseFile(self.menuPath + menuXML)
        # get menu information
        self.menuXPU.getSectionValues('section','Resources')
        self.menuXPU.getSectionValues('subsection','General')
        self.menuXPU.getSectionValues('subsection','Frame')
        self.menuXPU.getSectionValues('subsection','FrameImage')
        # get the menu name and make menu dictionary
        t_n = self.menuXPU.Parser['XML_Values']['General_Values']['name']
        self.menuList[t_n] = {'labels':{}, 'buttons':{}, 'optionMenus':{}, \
            'radioButtons':{}, 'sliders':{}}
        # fonts
        t_tf = self.menuXPU.Parser['XML_Values']['Resources_Values']['titleFont']
        t_bf = self.menuXPU.Parser['XML_Values']['Resources_Values']['bodyFont']
        t_p = self.targetMVC.mvcStructure['tier_text']['fonts'] + '/'
        t_tf = t_p + t_tf
        t_bf = t_p + t_bf
        self.menuList[t_n]['titleFont'] = loader.loadFont(t_tf)
        self.menuList[t_n]['bodyFont'] = loader.loadFont(t_bf)
        # background image
        t_bi = self.menuXPU.Parser['XML_Values']['Resources_Values']['backImage']
        if t_bi == 'None':
            # no image preferred
            self.menuList[t_n]['backImage'] = None
            self.menuList[t_n]['imagePosition'] = None
            self.menuList[t_n]['imageScale'] = None
        else:
            t_p = self.targetMVC.mvcStructure['tier_resource']['images'] + '/'
            t_bi = t_p + t_bi
            self.menuList[t_n]['backImage'] = loader.loadTexture(t_bi)
            self.menuList[t_n]['imagePosition'] = (self.menuXPU.Parser['XML_Values'] \
                ['FrameImage_Values']['posX'], self.menuXPU.Parser['XML_Values'] \
                ['FrameImage_Values']['posY'], self.menuXPU.Parser['XML_Values'] \
                ['FrameImage_Values']['posZ'])
            self.menuList[t_n]['imageScale'] = (self.menuXPU.Parser['XML_Values'] \
                ['FrameImage_Values']['scaleX'], self.menuXPU.Parser['XML_Values'] \
                ['FrameImage_Values']['scaleY'], self.menuXPU.Parser['XML_Values'] \
                ['FrameImage_Values']['scaleZ'])
        # the frame
        t_pos = (self.menuXPU.Parser['XML_Values']['Frame_Values']['posX'], \
            self.menuXPU.Parser['XML_Values']['Frame_Values']['posY'], \
            self.menuXPU.Parser['XML_Values']['Frame_Values']['posZ'])
        t_siz = (self.menuXPU.Parser['XML_Values']['Frame_Values']['sizeL'], \
            self.menuXPU.Parser['XML_Values']['Frame_Values']['sizeR'], \
            self.menuXPU.Parser['XML_Values']['Frame_Values']['sizeB'], \
            self.menuXPU.Parser['XML_Values']['Frame_Values']['sizeT'])
        t_col = (self.menuXPU.Parser['XML_Values']['Frame_Values']['colR'], \
            self.menuXPU.Parser['XML_Values']['Frame_Values']['colG'], \
            self.menuXPU.Parser['XML_Values']['Frame_Values']['colB'], \
            self.menuXPU.Parser['XML_Values']['Frame_Values']['colA'])
        t_bdm = (self.menuXPU.Parser['XML_Values']['Frame_Values']['borderW'], \
            self.menuXPU.Parser['XML_Values']['Frame_Values']['borderH'])
        self.menuList[t_n]['menuFrame'] = DirectFrame(frameSize = t_siz, \
            pos = t_pos, frameColor = t_col, image = self.menuList[t_n] \
            ['backImage'], image_pos = self.menuList[t_n]['imagePosition'],
            image_scale = self.menuList[t_n]['imageScale'], \
            relief = DirectGuiGlobals.RIDGE, borderWidth = t_bdm)
        # load labels (the setting is a CSV)
        t_ll = self.menuXPU.Parser['XML_Values']['General_Values']['labels']
        # check if there are none
        if t_ll != self.emptyList:
            t_l = t_ll.split(',')
            for t_x in t_l:
                self.loadLabel(t_x, t_n)
        # load buttons (the setting is a CSV)
        t_ll = self.menuXPU.Parser['XML_Values']['General_Values']['buttons']
        # check if there are none
        if t_ll != self.emptyList:
            t_l = t_ll.split(',')
            for t_x in t_l:
                self.loadButton(t_x, t_n)
        # load radio buttons (the setting is a CSV)
        t_ll = self.menuXPU.Parser['XML_Values']['General_Values']['radioButtons']
        # check if there are none
        if t_ll != self.emptyList:
            t_l = t_ll.split(',')
            for t_x in t_l:
                self.loadRadioButton(t_x, t_n)
        # load option menus (the setting is a CSV)
        t_ll = self.menuXPU.Parser['XML_Values']['General_Values']['optionMenus']
        # check if there are none
        if t_ll != self.emptyList:
            t_l = t_ll.split(',')
            for t_x in t_l:
                self.loadOptionMenu(t_x, t_n)
        # load sliders (the setting is a CSV)
        t_ll = self.menuXPU.Parser['XML_Values']['General_Values']['sliders']
        # check if there are none
        if t_ll != self.emptyList:
            t_l = t_ll.split(',')
            for t_x in t_l:
                self.loadSlider(t_x, t_n)
        # the menu is initially visible
        self.menuList[t_n]['visible'] = True
    def showMenu(self, menuName):
        " makes a hidden menu visible "
        if menuName not in self.menuList.keys():
            # not a loaded menu
            return False
        elif self.menuList[menuName]['visible'] == True:
            # already visible
            return False
        # show the menu
        self.menuList[menuName]['menuFrame'].show()
        self.menuList[menuName]['visible'] = True
    def hideMenu(self, menuName):
        " makes a visible menu invisible "
        if menuName not in self.menuList.keys():
            # not a loaded menu
            return False
        elif self.menuList[menuName]['visible'] == False:
            # already invisible
            return False
        # hide the menu
        self.menuList[menuName]['menuFrame'].hide()
        self.menuList[menuName]['visible'] = False
    def changeRadioValue(self, menuName, buttonName, newValue):
        " programmatically modifies the indicator value "
        # we need this function because the process is 2-calls
        if menuName not in self.menuList.keys():
            # not a loaded menu
            return False
        elif buttonName not in self.menuList[menuName]['radioButtons'].keys():
            # the radio button does not exist
            return False
        else:
            # change the value
            self.menuList[menuName]['radioButtons'][buttonName] \
                ['indicatorValue'] = newValue
            # update the value on element
            self.menuList[menuName]['radioButtons'][buttonName].setIndicatorValue()
    # -----------------------------------------------------------------------
    # --------------------------INTERNAL BEHAVIOURS--------------------------
    def loadLabel(self, labelName, menuName):
        " load settings for a label for the menu <menuName> "
        # parse settings
        self.menuXPU.getSectionValues('label', labelName)
        t_k = labelName + '_Values'
        # load label position
        t_pos = (self.menuXPU.Parser['XML_Values'][t_k]['posX'], \
            self.menuXPU.Parser['XML_Values'][t_k]['posY'], \
            self.menuXPU.Parser['XML_Values'][t_k]['posZ'])
        # load frame color for label
        t_cf = (self.menuXPU.Parser['XML_Values'][t_k]['fcolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolA'])
        # load text foreground color
        t_ct = (self.menuXPU.Parser['XML_Values'][t_k]['colR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colA'])
        # load text shadow color
        t_cs = (self.menuXPU.Parser['XML_Values'][t_k]['scolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolA'])
        # load text scaling
        t_sc = self.menuXPU.Parser['XML_Values'][t_k]['scale']
        # load text alignment
        if self.menuXPU.Parser['XML_Values'][t_k]['alignment'] == 0:
            # left justify
            t_alg = TextNode.ALeft
        elif self.menuXPU.Parser['XML_Values'][t_k]['alignment'] == 1:
            # center justify
            t_alg = TextNode.ACenter
        else:
            # right justify
            t_alg = TextNode.ARight
        # load text lock-state
        t_mc = self.menuXPU.Parser['XML_Values'][t_k]['mayChange']
        # load label text and font
        t_tx = self.menuXPU.Parser['XML_Values'][t_k]['text']
        t_fn = self.menuXPU.Parser['XML_Values'][t_k]['font']
        t_fn = self.menuList[menuName][t_fn]
        # create label
        self.menuList[menuName]['labels'][labelName] = DirectLabel(text = t_tx, \
            frameColor = t_cf, text_fg = t_ct, scale = t_sc, text_font = t_fn, \
            text_shadow = t_cs, textMayChange = t_mc, text_align = t_alg)
        # set on frame
        self.menuList[menuName]['labels'] \
            [labelName].reparentTo(self.menuList[menuName]['menuFrame'])
        self.menuList[menuName]['labels'][labelName].setPos(t_pos[0], t_pos[1], \
            t_pos[2])
    def loadButton(self, buttonName, menuName):
        " load settings for a button for the menu <menuName> "
        # parse settings
        self.menuXPU.getSectionValues('button', buttonName)
        t_k = buttonName + '_Values'
        # load button position
        t_pos = (self.menuXPU.Parser['XML_Values'][t_k]['posX'], \
            self.menuXPU.Parser['XML_Values'][t_k]['posY'], \
            self.menuXPU.Parser['XML_Values'][t_k]['posZ'])
        # load button text and font
        t_tx = self.menuXPU.Parser['XML_Values'][t_k]['text']
        t_fn = self.menuXPU.Parser['XML_Values'][t_k]['font']
        t_fn = self.menuList[menuName][t_fn]
        # load frame color for button
        t_cf = (self.menuXPU.Parser['XML_Values'][t_k]['fcolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolA'])
        # load text foreground color
        t_ct = (self.menuXPU.Parser['XML_Values'][t_k]['colR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colA'])
        # load text shadow color
        t_cs = (self.menuXPU.Parser['XML_Values'][t_k]['scolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolA'])
        # load text scaling
        t_sc = self.menuXPU.Parser['XML_Values'][t_k]['scale']
        # load text alignment
        if self.menuXPU.Parser['XML_Values'][t_k]['alignment'] == 0:
            # left justify
            t_alg = TextNode.ALeft
        elif self.menuXPU.Parser['XML_Values'][t_k]['alignment'] == 1:
            # center justify
            t_alg = TextNode.ACenter
        else:
            # right justify
            t_alg = TextNode.ARight
        # load callback function index
        t_cfi = self.menuXPU.Parser['XML_Values'][t_k]['callbackIndex']
        # create the button
        self.menuList[menuName]['buttons'][buttonName] = DirectButton( text = t_tx, \
            command = self.callBacks[t_cfi][0], extraArgs = self.callBacks[t_cfi] \
            [1], text_shadow = t_cs, scale = t_sc, frameColor = t_cf, text_fg = t_ct, \
            text_font = t_fn, text_align = t_alg)
        # set on the frame
        self.menuList[menuName]['buttons'] \
            [buttonName].reparentTo(self.menuList[menuName]['menuFrame'])
        self.menuList[menuName]['buttons'][buttonName].setPos(t_pos[0], t_pos[1], \
            t_pos[2])
    def loadRadioButton(self, buttonName, menuName):
        " load settings for a radio button for the menu <menuName> "
        # parse settings
        self.menuXPU.getSectionValues('radioButton', buttonName)
        t_k = buttonName + '_Values'
        # load button position
        t_pos = (self.menuXPU.Parser['XML_Values'][t_k]['posX'], \
            self.menuXPU.Parser['XML_Values'][t_k]['posY'], \
            self.menuXPU.Parser['XML_Values'][t_k]['posZ'])
        # load button text and font
        t_tx = self.menuXPU.Parser['XML_Values'][t_k]['text']
        t_fn = self.menuXPU.Parser['XML_Values'][t_k]['font']
        t_fn = self.menuList[menuName][t_fn]
        # load frame color for button
        t_cf = (self.menuXPU.Parser['XML_Values'][t_k]['fcolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolA'])
        # load text foreground color
        t_ct = (self.menuXPU.Parser['XML_Values'][t_k]['colR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colA'])
        # load text shadow color
        t_cs = (self.menuXPU.Parser['XML_Values'][t_k]['scolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolA'])
        # load text scaling
        t_sc = self.menuXPU.Parser['XML_Values'][t_k]['scale']
        # load text alignment
        if self.menuXPU.Parser['XML_Values'][t_k]['alignment'] == 0:
            # left justify
            t_alg = TextNode.ALeft
        elif self.menuXPU.Parser['XML_Values'][t_k]['alignment'] == 1:
            # center justify
            t_alg = TextNode.ACenter
        else:
            # right justify
            t_alg = TextNode.ARight
        # load callback function index
        t_cfi = self.menuXPU.Parser['XML_Values'][t_k]['callbackIndex']
        # load initial value
        t_iv = self.menuXPU.Parser['XML_Values'][t_k]['initialValue']
        # load the box placement relative to text ('left' or 'right')
        t_bxp = self.menuXPU.Parser['XML_Values'][t_k]['boxPlacement']
        # load the box border size
        t_bb = self.menuXPU.Parser['XML_Values'][t_k]['boxBorder']
        # load the box relief
        if self.menuXPU.Parser['XML_Values'][t_k]['boxRelief'] == 0:
            t_bxr = DirectGuiGlobals.SUNKEN
        else:
            t_bxr = DirectGuiGlobals.RAISED
        # load press effect
        t_pfx = self.menuXPU.Parser['XML_Values'][t_k]['pressEffect'] 
        # create the radio button
        self.menuList[menuName]['radioButtons'][buttonName] = DirectCheckButton( \
            text = t_tx, command = self.callBacks[t_cfi][0], \
            extraArgs = self.callBacks[t_cfi][1], text_shadow = t_cs, scale = t_sc, \
            frameColor = t_cf, text_fg = t_ct, text_font = t_fn, \
            indicatorValue = t_iv, boxPlacement = t_bxp, boxBorder = t_bb, \
            boxRelief = t_bxr, pressEffect = t_pfx, text_align = t_alg)
        # set on the frame
        self.menuList[menuName]['radioButtons'] \
            [buttonName].reparentTo(self.menuList[menuName]['menuFrame'])
        self.menuList[menuName]['radioButtons'][buttonName].setPos(t_pos[0], t_pos[1], \
            t_pos[2])
    def loadSlider(self, sliderName, menuName):
        " load settings for a slider for the menu <menuName> "
        # parse settings
        self.menuXPU.getSectionValues('slider', sliderName)
        t_k = sliderName + '_Values'
        # load slider position
        t_pos = (self.menuXPU.Parser['XML_Values'][t_k]['posX'], \
            self.menuXPU.Parser['XML_Values'][t_k]['posY'], \
            self.menuXPU.Parser['XML_Values'][t_k]['posZ'])
        # load slider text and font
        t_tx = self.menuXPU.Parser['XML_Values'][t_k]['text']
        t_fn = self.menuXPU.Parser['XML_Values'][t_k]['font']
        t_fn = self.menuList[menuName][t_fn]
        # load frame color for slider
        t_cf = (self.menuXPU.Parser['XML_Values'][t_k]['fcolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolA'])
        # load frame color for thumb
        t_cft = (self.menuXPU.Parser['XML_Values'][t_k]['tcolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['tcolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['tcolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['tcolA'])
        # load text foreground color
        t_ct = (self.menuXPU.Parser['XML_Values'][t_k]['colR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colA'])
        # load text shadow color
        t_cs = (self.menuXPU.Parser['XML_Values'][t_k]['scolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolA'])
        # load text scaling
        t_sc = self.menuXPU.Parser['XML_Values'][t_k]['scale']
        # load text alignment
        if self.menuXPU.Parser['XML_Values'][t_k]['alignment'] == 0:
            # left justify
            t_alg = TextNode.ALeft
        elif self.menuXPU.Parser['XML_Values'][t_k]['alignment'] == 1:
            # center justify
            t_alg = TextNode.ACenter
        else:
            # right justify
            t_alg = TextNode.ARight
        # load callback function index
        t_cfi = self.menuXPU.Parser['XML_Values'][t_k]['callbackIndex']
        # load initial value
        t_iv = self.menuXPU.Parser['XML_Values'][t_k]['initialValue']
        # load range
        t_rge = (self.menuXPU.Parser['XML_Values'][t_k]['rangeMinimum'], \
            self.menuXPU.Parser['XML_Values'][t_k]['rangeMaximum'])
        # load step value
        t_sv = self.menuXPU.Parser['XML_Values'][t_k]['stepValue']
        # load orientation
        if self.menuXPU.Parser['XML_Values'][t_k]['orientation'] == 0:
            # horizontal slider
            t_ox = DirectGuiGlobals.HORIZONTAL
        else:
            # vertical slider
            t_ox = DirectGuiGlobals.VERTICAL
        # load border width (a solution for the slider thumb's initially
        # massive border)
        t_bw = (self.menuXPU.Parser['XML_Values'][t_k]['borderWidth'], \
                self.menuXPU.Parser['XML_Values'][t_k]['borderHeight'])
        # create the radio button
        self.menuList[menuName]['sliders'][sliderName] = DirectSlider( \
            thumb_text = t_tx, command = self.callBacks[t_cfi][0], \
            extraArgs = self.callBacks[t_cfi][1], thumb_text_shadow = t_cs, \
            thumb_text_scale = t_sc, frameColor = t_cf, thumb_text_fg = t_ct, \
            thumb_text_font = t_fn, value = t_iv, range = t_rge, \
            pageSize = t_sv, orientation = t_ox, thumb_frameColor = t_cft, \
            thumb_borderWidth = t_bw, thumb_text_align = t_alg)
        # set on the frame
        self.menuList[menuName]['sliders'] \
            [sliderName].reparentTo(self.menuList[menuName]['menuFrame'])
        self.menuList[menuName]['sliders'][sliderName].setPos(t_pos[0], t_pos[1], \
            t_pos[2])
    def loadOptionMenu(self, optionName, menuName):
        " load settings for a optionMenu for the menu <menuName> "
        # parse settings
        self.menuXPU.getSectionValues('optionMenu', optionName)
        t_k = optionName + '_Values'
        # load optionMenu position
        t_pos = (self.menuXPU.Parser['XML_Values'][t_k]['posX'], \
            self.menuXPU.Parser['XML_Values'][t_k]['posY'], \
            self.menuXPU.Parser['XML_Values'][t_k]['posZ'])
        # load optionMenu text and font
        t_tx = self.menuXPU.Parser['XML_Values'][t_k]['text']
        t_fn = self.menuXPU.Parser['XML_Values'][t_k]['font']
        t_fn = self.menuList[menuName][t_fn]
        # load frame color for optionMenu
        t_cf = (self.menuXPU.Parser['XML_Values'][t_k]['fcolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['fcolA'])
        # load highlight color for optionMenu
        t_ch = (self.menuXPU.Parser['XML_Values'][t_k]['hcolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['hcolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['hcolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['hcolA'])
        # load text foreground color
        t_ct = (self.menuXPU.Parser['XML_Values'][t_k]['colR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['colA'])
        # load text shadow color
        t_cs = (self.menuXPU.Parser['XML_Values'][t_k]['scolR'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolG'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolB'], \
            self.menuXPU.Parser['XML_Values'][t_k]['scolA'])
        # load text scaling
        t_sc = self.menuXPU.Parser['XML_Values'][t_k]['scale']
        # load text alignment
        if self.menuXPU.Parser['XML_Values'][t_k]['alignment'] == 0:
            # left justify
            t_alg = TextNode.ALeft
        elif self.menuXPU.Parser['XML_Values'][t_k]['alignment'] == 1:
            # center justify
            t_alg = TextNode.ACenter
        else:
            # right justify
            t_alg = TextNode.ARight
        # load item list
        t_sp = self.menuXPU.Parser['XML_Values'][t_k]['itemList']
        t_sp = t_sp.split(',')
        t_il = []
        for t_x in t_sp:
            # add to item list
            t_il.append(self.menuXPU.Parser['XML_Values'][t_k][t_x])
        # load initial item
        t_ii = self.menuXPU.Parser['XML_Values'][t_k]['initialItem']
        # load callback function index
        t_cfi = self.menuXPU.Parser['XML_Values'][t_k]['callbackIndex']
        # create the option menu
        self.menuList[menuName]['optionMenus'][optionName] = DirectOptionMenu(text = \
            t_tx, scale = t_sc, items = t_il, initialitem = t_ii, highlightColor = t_ch, \
            command = self.callBacks[t_cfi][0], text_fg = t_ct, text_font = t_fn, \
            text_shadow = t_cs, frameColor = t_cf, text_align = t_alg)
        # parent to the frame
        self.menuList[menuName]['optionMenus'] \
            [optionName].reparentTo(self.menuList[menuName]['menuFrame'])
        self.menuList[menuName]['optionMenus'][optionName].setPos(t_pos[0], t_pos[1], \
            t_pos[2])

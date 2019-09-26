# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden2D]
# Desc: Text Rendering Library - Text2D Class
# File name: Text2D.py
# Developed by: Project Eden Development Team
# Date: 26/06/2008
# Place: Nairobi, Kenya
# ---------------------------------------------
from random import randint
from direct.task import Task
from .text_globals import *
import copy
# ---------------------------------------------
# A class to handle the drawing of 2D text on screen.
# TTF is directly supported; egg files are also cool
# EGG files are pre-generated fonts from TTF so they are
# a lot more portable. You can edit the texture in Photoshop
# and you can use the EGG even in a version of Panda that
# doesn't support FreeType.
# The delay in showText is dependent upon the fps value
# Class definition for the Text2D class
# ---------------------------------------------
class Text2D:
    " The base class for all static 2D text "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, fpsValue = 60.0, defaultFontList = None, defaultFont = 'Arial'):
        # load the defaults; we just use some equivalent of a header file
        self.loadedFonts = {}
        # load fonts from the MVC fonts directory
        if defaultFontList != None:
            for t_y in defaultFontList:
                try:
                    self.loadedFonts[t_y[1]] = loader.loadFont(t_y[0])
                except IOError:
                    print("Failed to load fonts")
        # the default dictionary can be edited in the globals file
        self.textConfig = EdenDefaultProperties
        self.textConfig['ActiveFont'] = defaultFont
        # --------------------------------------------------------------
        # if a delay of X seconds is requested, we compute the number
        # of frames this implies as (self.fpsValue * X). Then we can
        # use task.frame directly as our elapsed frame value.
        self.fpsValue = fpsValue
        self.virginFlag = True
        self.texts = {}
        # create a new node path just under aspect2d for text
        self.nodeEden = aspect2d.attachNewNode('EdenText')
        self.textNodeList = {}
        self.nodeCount = 0
        # task dictionary
        self.soloRegister = {}
    # ------------------DESTRUCTOR------------------------
    # ----------------------------------------------------
    def __del__(self):
        if self.virginFlag != True:
            # destroy the surface object
            self.nodeEden.removeNode()
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    def loadTextFile(self, fileName, textName, textProperties = None):
        " loads text to the dictionary from a file "
        if textProperties == None:
            # map to defaults dictionary
            # Python has very stupid pass-by-reference policies
            textProperties = copy.copy(self.textConfig)
        t_j = open(fileName, 'r')
        self.texts[textName] = [t_j.read(), textProperties]
    def loadTextLine(self, textString, textName, textProperties = None):
        " loads text to the dictionary from a string "
        if textProperties == None:
            # map to defaults dictionary
            # Python has very stupid pass-by-reference policies
            textProperties = copy.copy(self.textConfig)
        self.texts[textName] = [textString, textProperties]
    def loadFont(self, fontFileName, fontName):
        " loads a font to the loadedFonts dictionary "
        # load and store the font
        self.loadedFonts[fontName] = loader.loadFont(fontFileName)
    def displayText(self, textKey, intervalSec = 0, textPosition = None, \
        duplicates = True):
        " show some text for <interval> sec "
        # check for position
        if textPosition != None:
            # set the new position
            self.texts[textKey][1]['Position'] = textPosition
        self.texts[textKey][1]['Duplicates'] = duplicates
        # to make each task name unique we will mangle the name a bit
        t_g = randint(3, 300)
        t_k = randint(301, 500)
        # here we are assured of a truly unique value
        t_t = '%s%d%d' % (textKey, t_g, t_k)
        # add the solo task to the taskmanager
        taskMgr.add(self.soloTask, t_t)
        # if intervalSec is negative we assume user means 0
        if intervalSec < 0:
            intervalSec = 0
        t_ivl = intervalSec * self.fpsValue
        self.soloRegister[t_t] = [textKey, t_ivl, None]
    def displayTextCluster(self, textKeyList, textPositionList, intervalSec = 0 ):
        " show some group of text for <interval> sec "
        # position must be specified
        for t_a, t_b in enumerate(textKeyList):
            self.texts[ t_b ][1]['Position'] = textPositionList[t_a]
        # to make each task name unique we will mangle the name a bit
        t_g = randint(3, 300)
        t_k = randint(301, 500)
        # here we are assured of a truly unique value
        t_t = '%s%d%d' % (textKeyList[0], t_g, t_k)
        # add the solo cluster task to the taskmanager
        taskMgr.add(self.soloClusterTask, t_t)
        # if intervalSec is negative we assume user means 0
        if intervalSec < 0:
            intervalSec = 0
        t_ivl = intervalSec * self.fpsValue
        self.soloRegister[t_t] = [textKeyList, t_ivl, None]
    def blitText(self, textKey, delayValue = 0.0):
        " switch some text with other ( ideally of identical properties ) "
        # add the blit task to the taskmanager
        taskMgr.doMethodLater(delayValue, self.blitTask, "BlitText")
        self.textWanted = textKey
    def sequenceAllText(self, intervalSec, cleanUp = True):
        " show the sequence of texts, each for <interval> sec "
        # to make each task name unique we will mangle the name a bit
        t_g = randint(3, 300)
        t_k = randint(301, 500)
        t_t = '%d%d%d' % (t_g, intervalSec, t_k)
        # add the switcher task to the taskmanager
        taskMgr.add(self.switcherTask, t_t)
        # if intervalSec is negative or 0 we assume default
        if intervalSec <= 0:
            intervalSec = 3
        t_ivl = intervalSec * self.fpsValue
        # make a list of all the keys
        textKeyList = list(self.texts)
        self.soloRegister[t_t] = [textKeyList, t_ivl, cleanUp, 0]
    def clearScreen(self):
        " clears the surface( everything on aspect2d drawn from here ) "
        if self.virginFlag != True:
            # destroy the surface object
            self.nodeEden.removeNode()
            self.virginFlag = True
    # ------------------INTERNAL BEHAVIOURS---------------
    # ----------------------------------------------------
    def showText(self, textKey, cluster = False):
        " displays text from the dictionary "
        # create a new text node and set properties
        if self.texts[textKey][1]['Duplicates'] == True:
            # to make each node unique we will mangle the name a bit
            t_n = randint(3, 300)
            t_g = randint(301, 600)
            # here we are assured of a truly unique value
            t_s = '%s%d%d' % (textKey, self.nodeCount, t_n + t_g)
        else:
            # check if we have an existing node
            if textKey in self.textNodeList:
                return None
            else:
                # no mangling
                t_s = textKey
        self.nodeCount += 1
        self.newTextNode = TextNode(t_s)
        self.newTextNode.setText(self.texts[textKey][0])
        self.setProperties(self.texts[textKey][1])
        # attach to the main text node
        if self.virginFlag == True:
            # we create nodeEden again
            self.nodeEden = aspect2d.attachNewNode('Eden_Text')
        t_n = self.nodeEden.attachNewNode(self.newTextNode)
        t_n.setScale(self.texts[textKey][1]['Scale'] * self.texts[textKey][1] \
            ['FontSize'])
        # set the position
        t_pos = self.texts[textKey][1]['Position']
        t_n.setPos(t_pos[0], t_pos[1], t_pos[2])
        # now we store our new node path
        self.textNodeList[t_s] = t_n
        if self.virginFlag != False:
            self.virginFlag = False
        # return the node name
        return t_s
    def switchText(self, textKeySource, textKeyDest):
        " does a form of blitting "
        # use only for text that has same onscreen position
        if textKeyDest not in self.textNodeList:
            # the destination node does not exist
            return False
        else:
            # just switch text (position is ignored)
            self.textNodeList[textKeyDest].setText(self.texts[textKeySource][0])
            return True
    def setProperties(self, props2Set):
        " sets properties on the text node "
        self.newTextNode.setFont(self.loadedFonts[props2Set["ActiveFont"]])
        self.newTextNode.setSlant(props2Set["Slant"])
        self.newTextNode.setTextColor(props2Set["Color"])
        self.newTextNode.setAlign(props2Set["Alignment"])
        if props2Set["SmallCaps"] == True:
            self.newTextNode.setSmallCaps(props2Set["SmallCaps"])
            self.newTextNode.setSmallCapsScale(props2Set["SmallCapsScale"])
        if props2Set["ShadowFlag"] == True:
            self.newTextNode.setShadow(props2Set["Shadow"])
            self.newTextNode.setShadowColor(props2Set["ShadowColor"])
        if props2Set["WrapFlag"] == True:
            self.newTextNode.setWordwrap(props2Set["WordWrap"])
        if props2Set["FrameFlag"] == True:
            self.newTextNode.setFrameColor(props2Set["FrameColor"])
            self.newTextNode.setFrameAsMargin(props2Set["FrameMargin"])
        if props2Set["CardFlag"] == True:
            self.newTextNode.setCardColor(props2Set["CardColor"])
            self.newTextNode.setCardAsMargin(props2Set["CardMargin"])
    # -------------------------TASKS----------------------
    # ----------------------------------------------------
    def switcherTask(self, task):
        " switches texts from list "
        # remember that the 1st text is not shown yet
        if task.time == 0.0:
            # show the first text
            self.showText(self.soloRegister[task.name][0][0])
            self.soloRegister[task.name][3] = 1
            return task.cont
        elif (task.frame / self.soloRegister[task.name][3]) == \
            self.soloRegister[task.name][1]:
            # time for next text
            self.soloRegister[task.name][3] += 1
            if len(self.soloRegister[task.name][0]) >= \
                self.soloRegister[task.name][3]:
                # safe to show, text exists
                self.switchText(self.soloRegister[task.name][0] \
                    [self.soloRegister[task.name][3] - 1])
                return task.cont
            else:
                # out of text!
                if self.soloRegister[task.name][2] == True:
                    # clear the screen
                    self.clearScreen() 
                return task.done
        else:
            # all other frames
            return task.cont
    def soloTask(self, task):
        " delays for some text then clears "
        if task.time == 0.0:
            # show the text and get node name
            t_k = self.showText(self.soloRegister[task.name][0])
            if t_k == None:
                # we have tried to repeat a node that forbids duplicates
                return task.done
            else:
                # store
                self.soloRegister[task.name][2] = t_k
            if self.soloRegister[task.name][1] <= 0:
                # no delay; don't erase
                return task.done
            else:
                # we have a valid delay
                return task.cont
        elif task.frame == self.soloRegister[task.name][1]:
            # time for erasure
            self.textNodeList[self.soloRegister[task.name][2]].removeNode()
            del self.textNodeList[self.soloRegister[task.name][2]]
            return task.done
        else:
            # all other frames
            return task.cont
    def soloClusterTask(self, task):
        " delays for some text cluster then clears "
        if task.time == 0.0:
            # list to store the node names
            self.soloRegister[task.name][2] = []
            # show the text
            for t_r in self.soloRegister[task.name][0]:
                t_c = self.showText(t_r, True)
                if t_c != None:
                    # we are safe
                    self.soloRegister[task.name][2].append( t_c )
            if self.soloRegister[task.name][1] <= 0:
                # no delay; don't erase
                return task.done
            else:
                # we have a valid delay
                return task.cont
        elif task.frame == self.soloRegister[task.name][1]:
            # time for erasure
            for t_r in self.soloRegister[task.name][2]:
                self.textNodeList[t_r].removeNode()
                del self.textNodeList[t_r]
            return task.done
        else:
            # all other frames
            return task.cont
    def blitTask(self, task):
        " blits text, seriously "
        # we will not assume text is displayed
        if self.virginFlag == True:
            # no text on the screen
            return task.done
        else:
            self.switchText(self.textWanted)
            return task.done
                
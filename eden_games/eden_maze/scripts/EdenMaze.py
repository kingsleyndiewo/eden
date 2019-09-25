# Package Description: Funtrench's Eden Software Development Kit
# Name: Eden Maze 1.0 - There's always a way out
# Desc: Puzzle Game powered by Eden
# File name: EdenMaze.py
# Developed by: Project Eden Development Team
# Date: 06/08/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench PLC. www.funtrench.com       |
# |------------------------------------------------|
from Eden.Eden3D.Worlds.Adam import Adam
from Eden.Eden2D.Text2D import Text2D
from Eden.Eden2D.Menu2D import Menu2D
from Eden.Eden2D.Glass2D import Glass2D
from direct.task import Task
from random import randint
from pandac.PandaModules import Vec3, Point3, BitMask32
from Eden.EdenTools.XMLParsers.ConfigParser import ConfigParser
import sys
# --------------------------------------------------
# A class to implement the maze
# Class definition for the EdenMaze class
# --------------------------------------------------
class EdenMaze(Adam):
    " Extending the Adam class for the maze "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        Adam.__init__(self, self.starterTask) # ancestral constructor
        # create helper classes and initialize variables
        t_f = [('arial.egg', 'Arial')]
        self.textPlay = Text2D(self.edenVisuals.fpsValue, t_f)
        self.mazeXPU = ConfigParser()
        self.menuBrush = Menu2D(self.gameMVC)
        self.hudBrush = Glass2D(self.gameMVC)
        self.Credits = 10000
        self.delayCount = 0
        self.flagCount = 0
        self.aerialData = 0
        # variable that stores actor delay
        self.actorData = 0
        # variable that indicate which actor has been hit 
        self.actorLagIndex = 0
        # variable that holds the actors nodepath
        self.actorPath = ''
        # variables related to the dead ends
        self.Gcount = 0
        self.monsterPack = ['Gorilla', 'GWizard', 'BWizard']
        # for the camera shot
        self.camPosBackup = [0, 0, 0]
        self.blockPaint = None
        self.mazeChoice = 'easy.xml'
        self.defaultTitle = 'Level 1 - Easy: Get Miranda out of the maze!'
        # flags that reset to the main menu
        self.gameLost = False
        self.gameResigned = False
        # load bump sound
        self.loadSoundEffect('bump.wav', 'bump')
        # load dead end sound
        #self.loadSoundEffect('dead_end.wav', 'dead end')
        # load victory sound
        self.loadSoundEffect('victory.wav', 'victory')
        # load zoom sound
        self.loadSoundEffect('zoom.wav', 'zoom')
        # load gorilla sound
        self.loadSoundEffect('Gorilla.wav', 'growl')
        # load good wizard sound
        self.loadSoundEffect('GWizard.wav', 'add points')
        # load bad wizard sound
        self.loadSoundEffect('BWizard.wav', 'lose points')
        # load go back to start sound
        self.loadSoundEffect('Start.wav', 'start')
        # load loss of half points sound
        self.loadSoundEffect('halfpoints.wav', 'half points')
        # load game music
        self.loadMusic('sound2.mp3', 'music')
        # add the animation task to the task manager
        taskMgr.add(self.defaultAnimationTask, 'animationTask')
        # ------------------------------------------------------------------
        # Miranda is our maze avatar
        self.ladyMiranda = self.mainActor
        # ------------------------------------------------------------------
        # load the text resources
        self.textKeys = ['instruction1', 'instruction2', 'instruction3', \
          'instruction4','instruction5']
        # compute the text positions
        self.textPositions = []
        for t_p in range(5):
            t_j = Vec3( -1.30, 0, 0.90 - (t_p * 0.05) )
            self.textPositions.append(t_j)
        # instructions
        self.textPlay.loadTextLine('Arrow Keys: Control Miranda', self.textKeys[0])
        self.textPlay.loadTextLine('R/G/B: Place red/green/blue flag', self.textKeys[1])
        self.textPlay.loadTextLine('Q: Resign the game', self.textKeys[2])
        self.textPlay.loadTextLine('I: Show game information', self.textKeys[3])
        self.textPlay.loadTextLine('D: Show documentation', self.textKeys[4])
        # game info
        self.textPlay.loadTextLine(self.gameID, 'Game')
        # event notices
        self.eventsList = []
        self.eventsList.append("Don't bump into walls! 10 EdenPoints lost.")
        self.eventsList.append('Dead End! 500 EdenPoints lost.')
        self.eventsList.append('Victory! You found the exit.')
        self.eventsList.append('You were defeated! You lost all credits.')
        self.eventsList.append('You ran out of flags!')
        self.eventsList.append('Flag Count')
        self.eventsList.append('GORILLA!! 500 EdenPoints lost.')
        self.eventsList.append('GORILLA! 750 EdenPoints lost.')
        self.eventsList.append('GORILLA! 1000 EdenPoints lost.')
        self.eventsList.append('GOOD WIZARD! 250 EdenPoints gained.')
        self.eventsList.append('GOOD WIZARD! 300 EdenPoints gained.')
        self.eventsList.append('GOOD WIZARD! 500 EdenPoints gained.')
        self.eventsList.append('GOOD WIZARD! ZOOM!.')
        self.eventsList.append('BAD WIZARD! Half your points are gone!')
        self.eventsList.append('BAD WIZARD! Thrown back to START!')
        # manual text
        t_n =  self.gameMVC.mvcStructure['tier_resource']['text'] + '/EdenMaze.txt'
        self.textPlay.loadTextFile(t_n, 'Doc')
        # setup key mappings
        self.accept("r", self.setNewFlag, [0])
        self.accept("g", self.setNewFlag, [1])
        self.accept("b", self.setNewFlag, [2])
        self.accept("s", self.screenCapture, ['Maze_'])
        self.accept("d", self.textPlay.displayText, ['Doc', 30, Vec3(-0.70,0,0.50), False])
        self.accept("i", self.textPlay.displayText, ['Game', 30, Vec3(0.05,0,0.95), False])
        self.accept("c", self.textPlay.clearScreen)
        self.accept("a", self.aerialView, [])
        self.accept("q", self.gameResign, [])
        # setup notifications
        self.accept("image-done", self.reshowMenu, [])
        # create callback function list
        self.callBackList = [(sys.exit, [0]), (self.beginNewGame, []), \
            (self.showAbout, []), (self.loadPrefsMenu, []), (self.getNewLevel, []), \
            (self.dummyCallBack, [])]
    # ------------------BEHAVIORS-------------------------
    # ----------------------------------------------------
    def beginNewGame(self):
        " loads a new game "
        # stop menu music and play game music
        self.gameMusic.stop()
        self.jukeBox['music'].play()
        # re-initialize variables
        self.Credits = 10000
        self.delayCount = 0
        self.gameLost = False
        self.gameResigned = False
        # remove the cubes
        for t_x in self.objectStore.keys():
            if t_x.find(self.blockModel) != -1:
                # a valid block; remove it
                self.objectStore[t_x][0].removeNode()
                del self.objectStore[t_x]
        # remove the monsters
        for t_f in self.actorStore.keys():
            for t_y in self.monsterPack:
                if t_f.find(t_y) != -1:
                    self.actorStore[t_f].baseActor.removeNode()
                    del self.actorStore[t_f]
                    break
        # load the maze (from the menu we should get the level number)
        self.loadMaze(self.mazeChoice)
        # show text 
        self.textPlay.displayTextCluster(self.textKeys, self.textPositions)
        # hide the cursor again if necessary
        if self.worldData['showMouse'] == 0:
            self.toggleMouseCursor()
        # load monster pack
        self.loadModels()
        # hide the menu
        self.menuBrush.hideMenu('Main')
        # add the game task to the task manager
        taskMgr.add(self.gameTask, 'gameTask')
    def printEvent(self, eventNumber):
        " prints an event to the HUD "
        # display event notice with time
        t_l = self.worldData['localTime'] + ':-> ' + self.eventsList[eventNumber]
        self.hudBrush.menuList['Status']['labels']['Event'] \
            ['text'] = t_l
    def checkCredit(self):
        " checks whether we have sufficient credit to proceed "
        # if we go below zero the game is lost
        if self.Credits <= 0:
            self.printEvent(3)
            self.gameLost = True
        else:
            # update HUD and time
            t_y = '%d%s' % (self.Credits, ' EdenPoints remaining')
            self.hudBrush.menuList['Status']['labels'] \
                ['Credits']['text'] = t_y
            # show time every second
            t_g = 'TIME: ' + self.worldData['localTime']
            self.hudBrush.menuList['Status']['labels'] \
                ['Time']['text'] = t_g
    def setNewFlag(self, flagType):
        " marks a point with a flag of argued color "
        # first check if we are out of flags
        if self.flagCount == 0:
            # notify the player
            self.printEvent(4)
        else:
            # load the model with actor position
            t_pos = self.mainActor.baseActor.getPos()
            t_s = '%s%d' % ('flag', self.flagCount)
            # the flag should not be collision-enabled
            t_d = {'parentNode':None, 'bitMask':BitMask32.allOff(), \
            'sphereFactor':1.0, 'enablePhysics':False, 'terrainDetection':False}
            self.loadGeometry('flag', t_s, self.flagScale, t_pos, t_d)
            # drop a flag
            if flagType == 0:
                # a red flag
                self.objectStore[t_s][0].setColor(1.0,0.0,0.0,1.0)
                # show the new flag count
                self.eventsList[5] = '%s%d%s' % ('Red flag used. You have ', \
                    (self.flagCount - 1), ' flags left')
            elif flagType == 1:
                # a green flag
                self.objectStore[t_s][0].setColor(0.0,1.0,0.0,1.0)
                # show the new flag count
                self.eventsList[5] = '%s%d%s' % ('Green flag used. You have ', \
                    (self.flagCount - 1), ' flags left')
            else:
                # a blue flag
                self.objectStore[t_s][0].setColor(0.0,0.0,1.0,1.0)
                # show the new flag count
                self.eventsList[5] = '%s%d%s' % ('Blue flag used. You have ', \
                    (self.flagCount - 1), ' flags left')
            # notify player of flags remaining
            self.printEvent(5)
            # decrement the flag count
            self.flagCount -= 1
    def aerialView(self):
        " shows a brief aerial view of the maze "
        # add a value to self.camPos to raise the camera
        for t_x in range(3):
                # store the camera position
                self.camPosBackup[t_x] = self.camPos[t_x]
                self.camPos[t_x] = self.shotZoom[t_x]
        # create a task to delay restoring the camPos height
        taskMgr.add(self.aerialTask, 'aerialTask')
    # ------------------GAME INITIALIZATION SERVICES-----------
    # ---------------------------------------------------------
    def loadMaze(self, mazeXML):
        " loads the maze into the world "
        # build a pathname to the file
        t_g = self.gameMVC.mvcStructure['config'] + '/'
        t_g += mazeXML
        # parse maze details XML (XPU = XML processing unit)
        self.mazeXPU.parseFile(t_g)
        # get maze information
        self.mazeXPU.getSectionValues('subsection','Blocks')
        self.mazeXPU.getSectionValues('subsection','Scale')
        self.mazeXPU.getSectionValues('section','Setup')
        self.mazeXPU.getSectionValues('subsection','Positions')
        self.mazeXPU.getSectionValues('subsection','SpecialSpots')
        # get the maze block model
        self.blockModel = self.mazeXPU.Parser['XML_Values']['Blocks_Values']['model']
        # get the scale
        self.blockScale = (self.mazeXPU.Parser['XML_Values']['Scale_Values'] \
            ['scaleX'], self.mazeXPU.Parser['XML_Values']['Scale_Values'] \
            ['scaleY'], self.mazeXPU.Parser['XML_Values']['Scale_Values'] \
            ['scaleZ'])
        # get the flag scale
        self.flagScale = (self.mazeXPU.Parser['XML_Values']['Scale_Values'] \
            ['fScaleX'], self.mazeXPU.Parser['XML_Values']['Scale_Values'] \
            ['fScaleY'], self.mazeXPU.Parser['XML_Values']['Scale_Values'] \
            ['fScaleZ'])
        # get the extremes
        self.mazeExtremes = (self.mazeXPU.Parser['XML_Values']['Setup_Values'] \
            ['extremeX'], self.mazeXPU.Parser['XML_Values']['Setup_Values'] \
            ['extremeY'])
        # get dimensions
        self.mazeDimensions = (self.mazeXPU.Parser['XML_Values']['Setup_Values'] \
            ['length'], self.mazeXPU.Parser['XML_Values']['Setup_Values'] \
            ['width'])
        self.cubeSize = self.mazeXPU.Parser['XML_Values']['Setup_Values'] \
            ['cubeWidth']
        # get the flag count
        self.flagCount = self.mazeXPU.Parser['XML_Values']['Setup_Values'] \
            ['flagCount']
        # get the aerial view delay
        self.aerialData = self.mazeXPU.Parser['XML_Values']['Setup_Values'] \
            ['aerialDelay']
        # get the actor delay
        self.actorData = self.mazeXPU.Parser['XML_Values']['Setup_Values'] \
            ['actorDelay']
        # get special spots
        t_a = self.mazeXPU.Parser['XML_Values']['SpecialSpots_Values']['exits']
        self.exitList = t_a.split(':')
        t_b = self.mazeXPU.Parser['XML_Values']['SpecialSpots_Values']['deadEnds']
        self.deadEndList = t_b.split(':')
        t_t = self.mazeXPU.Parser['XML_Values']['SpecialSpots_Values']['deadEndFaces']
        self.deadEndFaces = t_t.split(':')
        self.exitKeys = []
        # we parse the maze level XML file
        t_m = self.mazeXPU.Parser['XML_Values']['Positions_Values'].keys()
        # select 2 random cube colors (R,G,B)
        t_col = self.randomColor()
        t_col2 = self.randomColor()
        self.blockPaint = (t_col, t_col2)
        t_k = 0
        for t_h in t_m:
            # calculate the color index
            if t_k % 2 == 0:
                t_f = 0
            else:
                t_f = 1
            t_k += 1
            if self.mazeXPU.Parser['XML_Values']['Positions_Values'][t_h] == 0:
                if t_h in self.exitList:
                    # make an exit detection solid
                    t_e = self.insertCube(t_h, colorIndex = t_f)
                    self.hideObject(t_e)
                    self.exitKeys.append(t_e)
                else:
                    # blank area
                    pass
            elif self.mazeXPU.Parser['XML_Values']['Positions_Values'][t_h] == 2:
                # get the position
                t_c = int(t_h)
                t_p = self.computePos(t_c)
                # move Miranda to her starting position
                # position her where a cube center would be to avoid collision
                self.ladyMiranda.baseActor.setPos(t_p[0] - int(self.cubeSize / 2), \
                    t_p[1] - int(self.cubeSize / 2), 0)
                self.startingPos = self.ladyMiranda.baseActor.getPos()
            else:
                # cube
                self.insertCube(t_h, colorIndex = t_f)
    def loadModels(self):
        t_r = len(self.monsterPack) - 1
        for t_x in self.deadEndList:
            t_c = randint(0, t_r)
            t_h = self.computePos(int(t_x))
            # load the monster
            t_g = '%s%d' % (self.monsterPack[t_c], self.Gcount)
            self.loadActor(self.monsterPack[t_c] + '.xml', t_g)
            self.actorStore[t_g].baseActor.setX(t_h[0] - int(self.cubeSize / 2))
            self.actorStore[t_g].baseActor.setY(t_h[1] - int(self.cubeSize / 2))
            # hide the actor
            self.actorStore[t_g].baseActor.hide()
            # set up collision detection for Gorilla
            self.setupActorCollision(t_g)
            # set name tag
            self.actorStore[t_g].baseActor.setTag('monsterName', t_g)
            # orient the monster
            t_v = self.deadEndFaces[self.deadEndList.index(t_x)]
            if t_v == 'E':
               self.actorStore[t_g].baseActor.setH(-90)
            elif t_v == 'W':
                self.actorStore[t_g].baseActor.setH(90)
            elif t_v == 'N':
                pass
            else:
                self.actorStore[t_g].baseActor.setH(180)
            # set up event handler
            self.accept('Miranda-into-%s' % t_g, self.actorsBumpHandler, [t_x, t_g])
            # increment count
            self.Gcount = self.Gcount + 1
    def insertCube(self, cubeIndex, deadEnd = False, colorIndex = 0):
        " inserts a cube into the maze "
        # get the position
        t_c = int(cubeIndex)
        t_p = self.computePos(t_c)
        # make sure the node name is unique
        t_s = cubeIndex + self.blockModel
        t_sf = 0.8
        # fill the extra arguments
        t_x = {'parentNode':None, 'bitMask':BitMask32.allOff(), \
            'sphereFactor':t_sf, 'enablePhysics':False, 'terrainDetection':False}
        # load the cube
        self.loadGeometry(self.blockModel, t_s, self.blockScale, \
            (t_p[0], t_p[1], 0.0), t_x)
        # setup collision
        self.setupObjectCollision(t_s)
        # set color
        #self.objectStore[t_s][0].setColor(self.blockPaint[colorIndex][0], \
            #self.blockPaint[colorIndex][1], self.blockPaint[colorIndex][2], 1.0)
        # accept events for collision
        # parameters in accept() are passed first, then those in send()
        self.accept('Miranda-into-%s' % t_s, self.actorsBumpHandler, [cubeIndex, None])
        return t_s
    def computePos(self, blockIndex):
        " computes the world position of a block "
        # the algorithm is (MaxX * X) + Y for block index
        t_m = blockIndex % self.mazeDimensions[1]
        # get row
        if t_m == 0:
            # end of row
            t_r = blockIndex / self.mazeDimensions[1]
            # get column
            t_c = self.mazeDimensions[1]
        else:
            # we have to truncate a decimal and add 1
            t_r = int(blockIndex / self.mazeDimensions[1]) + 1
            # get column
            t_c = t_m
        # compute position
        t_x = self.mazeExtremes[0] + ( (t_c - 1) * 6.2)
        t_y = self.mazeExtremes[1] + ( (t_r - 1) * 6.2)
        return (t_x, t_y)
    # ------------------SYSTEM SERVICES-------------------
    # ----------------------------------------------------
    def actorsBumpHandler(self, targetNode, extraData, entry):
        "handles when Miranda bumps into anything"
        if self.gameLost == True:
            return False
        if targetNode in self.exitList:
            # avoid winning when we have already lost
            if self.gameLost == True:
                pass
            else:
                # we found the exit!
                # lift the exits
                for t_w in self.exitKeys:
                    self.objectStore[t_w][0].setZ(5)
                self.jukeBox['victory'].play()
                self.printEvent(2)
                self.gameLost = True
        elif targetNode in self.deadEndList:
            # identify the monster
            t_n = entry.getIntoNodePath()
            t_j = t_n.getTag('monsterName')
            print t_j
            for t_d in self.monsterPack:
                if extraData.find(t_d) != -1:
                    break
            if t_d == 'Gorilla':
                # respond to gorilla collision
                t_l = randint(0,2)
                if t_l == 0:
                    self.Credits -= 500
                    self.printEvent(6)
                    self.jukeBox['growl'].play()  
                elif t_l == 1:
                    self.Credits -= 750
                    self.printEvent(7)
                    self.jukeBox['growl'].play()
                else:
                    self.Credits -= 1000
                    self.printEvent(8)
                    self.jukeBox['growl'].play()
                self.actorLagIndex = 1
                #self.actorPath = self.actorStore[extraData].baseActor
                taskMgr.add(self.actorLagTask, extraData)
            elif t_d == 'GWizard':
                # respond to GWizard collision
                t_l = randint(0,3)
                if t_l == 0:
                    self.Credits += 250
                    self.printEvent(9)
                    self.jukeBox['add points'].play()
                elif t_l == 1:
                    self.Credits += 300
                    self.printEvent(10)
                    self.jukeBox['add points'].play()
                elif t_l == 2:
                    self.Credits += 500
                    self.printEvent(11)
                    self.jukeBox['add points'].play()
                else:
                    self.aerialView()
                    self.printEvent(12)
                    self.jukeBox['zoom'].play()
                self.actorLagIndex = 2
                #self.actorPath = self.actorStore[extraData].baseActor
                taskMgr.add(self.actorLagTask, extraData)
            elif t_d == 'BWizard':
                # respond to BWizard collision
                t_l = randint(0,1)
                if t_l == 0:
                    self.ladyMiranda.baseActor.setPos(self.startingPos[0], self.startingPos[1], \
                        self.startingPos[2])
                    self.printEvent(14)
                    self.jukeBox['start'].play()
                elif t_l == 1:
                   self.Credits /= 2
                   self.printEvent(13)
                   self.jukeBox['half points'].play()
                self.actorLagIndex = 3
                #self.actorPath = self.actorStore[extraData].baseActor
                taskMgr.add(self.actorLagTask, extraData)
        else:
            # she bumped into a cube
            # play bump sound
            self.jukeBox['bump'].play()
            self.printEvent(0)
            # a credit is deducted
            self.Credits -= 1
            self.checkCredit()   
    def showAbout(self):
        " displays the about screen "
        # show the about screen
        self.edenVisuals.displayImage(3, 5)
        # hide the menu
        self.menuBrush.hideMenu('Main')
    def loadPrefsMenu(self):
        " loads the preferences menu "
        pass
    def getNewLevel(self, newLevel):
        " gets a new level selection from the menu "
        if newLevel == 'Level 1 - Easy':
            # set the easy maze
            self.mazeChoice = 'easy.xml'
        elif newLevel == 'Level 2 - Medium':
            # set the medium maze
            self.mazeChoice = 'medium.xml'
        elif newLevel == 'Level 3 - Hard':
            # set the medium maze
            self.mazeChoice = 'hard.xml'
        else:
            # set the default
            self.mazeChoice = 'easy.xml'
        # change the game title
        self.defaultTitle = newLevel + ': Get Miranda out of the maze!'
    def reshowMenu(self):
        " reshows the main menu after about screen exits "
        # a solo task only occurs during the about screen
        self.menuBrush.showMenu('Main')
    def randomColor(self):
        " generates a random 3-tuple of RGB color "
        t_col = []
        for t_x in range(3):
            t_g = randint(0, 75)
            # make a float between 0 and 0.75 (we avoid too much brightness)
            t_g /= 100.0
            t_col.append(t_g)
        return t_col
    def gameResign (self):
        " sets the gameResigned flag"
        self.gameResigned = True
        
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
            self.jukeBox['music'].setLoop(True)
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
            # set the new title
            self.hudBrush.menuList['Status']['labels'] \
                ['Dir']['text'] = self.defaultTitle
            return task.cont
        else:
            # check for game over
            if self.gameLost == True or self.gameResigned == True:
                # delay for 5 seconds (make sure victory sound is done)
                if self.delayCount == (self.edenVisuals.fpsValue * 2):
                    # return to main menu and end task
                    self.toggleMouseCursor()
                    # clear the screen
                    messenger.send("c")
                    # remove the HUD
                    self.hudBrush.hideGlass('Status')
                    del self.hudBrush.menuList['Status']
                    # stop game music and play menu music
                    self.jukeBox['music'].stop()
                    self.gameMusic.play()
                    self.menuBrush.showMenu('Main')
                    taskMgr.remove('gameTask')
                else:
                    # increment
                    self.delayCount += 1
                    return task.cont
            else:
                if (task.frame % self.edenVisuals.fpsValue) == 0:
                    # lose 40 credits every 1 second; you'll be dry in around
                    # 1.4 hours which is fair
                    self.Credits -= 40
                    self.checkCredit()
                elif task.frame == 8:
                    t_p = self.computePos(435)
                    t_p[0] - int(self.cubeSize / 2)
                    t_p[1] - int(self.cubeSize / 2)
                    t_s = [0, -7, 475]
                    for t_x in range(2):
                        t_s[t_x] += t_p[t_x]
                    self.shotZoom = (t_s[0], t_s[1], t_s[2])
                elif task.frame == 10:
                    # we show the snapshot on frame 10
                    # show the snapshot
                    self.aerialView()
                return task.cont
    def aerialTask(self, task):
        " delays the restoring of original camera height "
        if (task.frame / self.edenVisuals.fpsValue) == self.aerialData:
            # restore the camera distance value
            for t_x in range(3):
                self.camPos[t_x] = self.camPosBackup[t_x]
            return task.done
        else:
            return task.cont
    def actorLagTask(self, task):
        " delays the restoring of bumped actor in the scene "
        if task.frame == 0:
            self.actorStore[task.name].baseActor.show()
        if self.actorLagIndex == 1:   
            if (task.frame / self.edenVisuals.fpsValue) == self.actorData:
                self.actorStore[task.name].baseActor.hide()
                return task.done
            else:
                return task.cont
        elif self.actorLagIndex == 2:   
            if (task.frame / self.edenVisuals.fpsValue) == self.actorData:
                self.actorStore[task.name].baseActor.hide()
                return task.done
            else:
                return task.cont
        elif self.actorLagIndex == 3:   
            if (task.frame / self.edenVisuals.fpsValue) == self.actorData:
                self.actorStore[task.name].baseActor.hide()
                return task.done
            else:
                return task.cont   
            
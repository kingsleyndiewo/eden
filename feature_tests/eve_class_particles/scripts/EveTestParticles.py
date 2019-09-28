# Package Description: Funtrench's Eden Software Development Kit
# Name: Eden Feature Tests SDK
# Desc: Advanced III Test Project for the Eve Class
# File name: EveTestParticles.py
# Developed by: Project Eden Development Team
# Date: 11/08/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from Eden.Eden3D.Worlds.Eve import Eve
from Eden.Eden2D.Text2D import Text2D
from Eden.Eden2D.Glass2D import Glass2D
from direct.task import Task
# --------------------------------------------------
# A class to demonstrate the features of the Eve
# Class with unmoused camera and inventory management.
# Class definition for the EveTestParticles class
# --------------------------------------------------
class EveTestParticles(Eve):
    " Extending the Eve class for two selectable actors in a world "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        Eve.__init__(self, self.starterTask, customPRC={'fullscreen':False}) # ancestral constructor
        self.videoDone = False
        self.eventListPos = 0.40
        t_f = [('arial.egg', 'Arial')]
        self.textPlay = Text2D(self.edenVisuals.fpsValue, t_f)
        self.hudBrush = Glass2D(self.gameMVC)
        self.cycleCount = 1
        # load other objects (the ViS Cube)
        self.loadGeometry('cube', 'cube', (0.25,0.25,0.25), (0,0,5))
        # load sound effects
        self.loadSoundEffect('bump.snd', 'bump')
        self.loadSoundEffect('bump.wav', 'bump2')
        self.loadSoundEffect('switch.snd', 'switch')
        # add the animation task to the task manager
        taskMgr.add(self.defaultAnimationTask, 'animationTask')
        # ------------------------------------------------------------------
        # the Eve super-class has a variable main actor
        self.currentAvatar = self.mainActor
        # set the actor as the focal point
        self.GMMT.geoMipMap.setFocalPoint(self.currentAvatar.baseActor)
        # get a handle to Miranda's right hand
        self.actorStore['Miranda'].getJointNodePath('RightHand')
        self.rightHand = self.actorStore['Miranda'].jointsList['RightHand']
        # load the inventory that will be available to Miranda
        self.loadInventory('ToolBox.xml', 'Miranda')
        # inventory objects are different from ordinary geometry because
        # they will not exist in the objectStore. You cannot therefore use
        # the visibility methods of Creation on them. Use selectInventoryItem
        # which needs the inventoryName and the itemName as arguments
        # parent the objects to Miranda's hand
        for t_i in self.toolBoxLists['Miranda']:
            self.toolBox['Miranda'][t_i].reparentTo(self.rightHand)
        # accept events for collision
        # parameters in accept() are passed first, then those in send()
        self.accept('Miranda-into-Ralph', self.actorsBumpHandler, [0])
        self.accept('Ralph-into-Miranda', self.actorsBumpHandler, [1])
        # entry resolver flags for collisions; prevents us from processing
        # both Ralph bumping into Miranda and vice-versa at the same time
        self.bumpFlag = False
        self.isDelaying = False
        # ------------------------------------------------------------------
        # load the text resources
        self.textKeys = ['title', 'instruction1', 'instruction2', 'instruction3', \
          'instruction4', 'instruction5', 'instruction6', 'instruction7', \
          'instruction8', 'instruction9', 'events']
        # compute the text positions
        self.textPositions = []
        for t_p in range(10):
            t_j = ( -1.30, 0, 0.95 - (t_p * 0.05) )
            self.textPositions.append(t_j)
        # append the events label position
        self.textPositions.append(( -1.30, 0, 0.45))
        # title
        self.textPlay.loadTextLine('Eve Test Particles. Powered by Funtrench', self.textKeys[0])
        # instructions
        self.textPlay.loadTextLine('Press ESCAPE to quit', self.textKeys[1])
        self.textPlay.loadTextLine('Right-Click: Select(Activate) Actor', self.textKeys[2])
        self.textPlay.loadTextLine('Arrow Keys: Control Selected Actor', self.textKeys[3])
        self.textPlay.loadTextLine('F/B: Increment/Decrement cube X', self.textKeys[4])
        self.textPlay.loadTextLine('G/H: Increment/Decrement cube Y', self.textKeys[5])
        self.textPlay.loadTextLine('A/J: Increment/Decrement cube Z', self.textKeys[6])
        self.textPlay.loadTextLine('Y: Cycle through inventory', self.textKeys[7])
        self.textPlay.loadTextLine('I: Show game information', self.textKeys[8])
        self.textPlay.loadTextLine('D: Show documentation', self.textKeys[9])
        self.textPlay.loadTextLine('EVENTS:', self.textKeys[10])
        # game info
        self.textPlay.loadTextLine(self.gameID, 'Game')
        # manual text
        t_n =  self.gameMVC.mvcStructure['tier_resource']['text'] + '/EveTest.txt'
        self.textPlay.loadTextFile(t_n, 'Doc')
        # collision notice
        self.textPlay.loadTextLine('Miranda hit Ralph!', 'notice')
        self.textPlay.loadTextLine('Ralph hit Miranda!', 'notice2')
        # set up the particle system
        self.createParticleGenerator('eveGen')
        # setup key mappings
        self.accept("f", self.cubeAlter, [+1, "X"])
        self.accept("b", self.cubeAlter, [-1, "X"] )
        self.accept("g", self.cubeAlter, [+1, "Y"] )
        self.accept("h", self.cubeAlter, [-1, "Y"] )
        self.accept("a", self.cubeAlter, [+1, "Z"] )
        self.accept("j", self.cubeAlter, [-1, "Z"] )
        self.accept("y", self.pickTool, [])
        self.accept("s", self.screenCapture, ['../EveParticles_'])
        self.accept("d", self.textPlay.displayText, ['Doc', 30, (-0.70,0,0.45), False])
        self.accept("i", self.textPlay.displayText, ['Game', 30, (0.05,0,0.95), False])
        self.accept("c", self.textPlay.clearScreen)
        self.accept("v", self.edenVisuals.media['video'][0][1].stop, [])
        # accept switching message
        self.accept('actor-switch', self.switchHandler, [])
    # ------------------BEHAVIORS-------------------------
    # ----------------------------------------------------
    def cubeAlter(self, valueChange, valueType):
        " alters co-ordinate position of cube "
        if valueType == "X":
            self.objectStore['cube'][0].setX(self.objectStore['cube'][0].getX() + valueChange)
        elif valueType == "Y":
            self.objectStore['cube'][0].setY(self.objectStore['cube'][0].getY() + valueChange)
        elif valueType == "Z":
            self.objectStore['cube'][0].setZ(self.objectStore['cube'][0].getZ() + valueChange)
    def pickTool(self):
        " cycles through Miranda's inventory "
        self.selectInventoryItem('Miranda', self.toolBoxLists['Miranda'] \
            [self.cycleCount])
        self.cycleCount += 1
        if self.cycleCount == len(self.toolBoxLists['Miranda']):
            # reset
            self.cycleCount = 0
    def actorsBumpHandler(self, targetNode, entry):
        "handles when avatar bumps into anything"
        # if the flag is set, ignore collision
        if self.bumpFlag == True and self.isDelaying == False:
            # add delay task to the task manager
            taskMgr.add(self.bumpDelayTask, 'delayTask')
        elif self.bumpFlag == True and self.isDelaying == True:
            pass
        else:
            # we can process the collision
            if targetNode == 0:
                # Miranda bumped into Ralph
                # play bump sound
                self.jukeBox['bump'].play()
                self.printEvent('notice')
                # set the flag
                self.bumpFlag = True
            elif targetNode == 1:
                # Ralph bumped into Miranda
                # play bump sound
                self.jukeBox['bump2'].play()
                self.printEvent('notice2')
                # set the flag
                self.bumpFlag = True
    def printEvent(self, eventKey):
        " prints an event to the list on the screen "
        # display event notice for 15 seconds
        self.textPlay.displayText(eventKey, 15.0, (-1.30,0,self.eventListPos))
        # decrement for the next event
        self.eventListPos -= 0.05
        if self.eventListPos <= 0.00:
            # restore
            self.eventListPos = 0.40
    def updateHUD(self):
        " updates the info on the unit HUD "
        # get the actor name
        t_n = self.currentAvatar.actorData['name']
        # resolve the gender
        if t_n == 'Miranda':
            t_x = 'Female'
            # red
            t_c = (1.0, 0.0, 0.0, 1.0)
        else:
            t_x = 'Male'
            # blue
            t_c = (0.0, 0.0, 1.0, 1.0)
        self.hudBrush.menuList['Unit']['labels']['Name']['text'] = t_n
        self.hudBrush.menuList['Unit']['labels']['Sex']['text'] = t_x
        self.hudBrush.menuList['Unit']['labels']['Sex']['text_fg'] = t_c
    def switchHandler(self):
        " responds to an actor switch event "
        # update avatar variable
        self.currentAvatar = self.mainActor
        # schedule an update for the HUD
        self.updateHUD()
        # play the sound
        self.jukeBox['switch'].play()
    # ------------------TASKS-----------------------------
    # ----------------------------------------------------
    def starterTask(self, task):
        " task to handle the startup "
        if task.time == 0.0:
            # hide cursor
            if self.worldData['showMouse'] != 0:
                self.toggleMouseCursor()
            # show the screens with an n-second delay
            self.edenVisuals.sequenceAllImages(self.visualDelay)
            return task.cont
        else:
            if self.edenVisuals.virginFlag == True:
                if self.videoDone == False:
                    # display the video after images are done
                    self.edenVisuals.displayVideo(0)
                    self.videoDone = True
                    return task.cont
                else:
                    # play the music and show text after video is done
                    self.textPlay.displayTextCluster(self.textKeys, self.textPositions)
                    self.gameMusic.setLoop(True)
                    self.gameMusic.play()
                    # show cursor
                    if self.worldData['showMouse'] != 0:
                        self.toggleMouseCursor()
                    # create the unit HUD
                    self.hudBrush.loadHUD('unitHUD.xml', None)
                    # update the HUD info
                    self.updateHUD()
                    # add the altimeter to the task manager
                    taskMgr.add(self.altimeterTask, 'altimeterTask')
                    # particle generator.......activate!
                    self.loadParticlesFile('fire.xml', 'eveGen')
                    self.setGeneratorOrigin('eveGen', self.objectStore['cube'] \
                        [0], (0,2.5,0))
                    return task.done
            else:
                # all other frames
                return task.cont
    def bumpDelayTask(self, task):
        " task to delay actor bump processing for a default while "
        if task.frame == 1:
            # notify that we are delaying
            self.isDelaying = True
            return task.cont
        elif task.frame == 300:
            # 300 frames should be cool
            self.bumpFlag = False
            self.isDelaying = False
            return task.done
        else:
            return task.cont
    def altimeterTask(self, task):
        " task to update main actor's altitude "
        t_s = '%s%f%s' % ('Altitude: ', self.currentAvatar.baseActor.getZ(), \
            ' metres')
        if t_s != self.hudBrush.menuList['Unit']['labels']['Altitude']['text']:
            # show the altitude change
            self.hudBrush.menuList['Unit']['labels']['Altitude']['text'] = t_s
        return task.cont

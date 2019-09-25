# Package Description: The Nairobi Project
# Name: Eden Nairobi Project Simulation
# Desc: Simulator for Traffic Management Algorithms
# File name: TrafficSim.py
# Developed by: Nairobi Project Development Team
# Date: 10/11/2012
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2012 Intellect Alliance.            |
# |------------------------------------------------|
from Eden.Eden3D.Worlds.Eve import Eve
from Eden.Eden2D.Text2D import Text2D
from Eden.Eden2D.Glass2D import Glass2D
from direct.task import Task
# --------------------------------------------------
# A class to simulate various traffic algorithms
# Class with unmoused camera.
# Class definition for the TrafficSim class
# --------------------------------------------------
class TrafficSim(Eve):
    " Extending the Eve class for vehicular selectable actors in a world "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        Eve.__init__(self, self.starterTask) # ancestral constructor
        self.videoDone = False
        self.eventListPos = 0.40
        t_f = [('arial.egg', 'Arial')]
        self.textPlay = Text2D(self.edenVisuals.fpsValue, t_f)
        self.hudBrush = Glass2D(self.gameMVC)
        self.cycleCount = 1
        # load cars (geometry)
        for x in range(0, 12):
            self.loadGeometry('cartruck', 'cartruck%d' % x, (0.65,0.65,0.65), (8.5,0,x * 5))
            self.loadGeometry('yugo', 'yugo%d' % x, (0.35,0.35,0.35), (11.5,0,x * 5))
        # load sound effects
        self.loadSoundEffect('bump.snd', 'bump')
        self.loadSoundEffect('bump.wav', 'bump2')
        self.loadSoundEffect('switch.snd', 'switch')
        # add the animation task to the task manager
        taskMgr.add(self.defaultAnimationTask, 'animationTask')
        # ------------------------------------------------------------------
        # the Eve super-class has a variable main actor
        # we must do this assignment each time a change occurs
        self.currentAvatar = self.mainActor
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
          'instruction4', 'instruction5', 'instruction6', 'events']
        # compute the text positions
        self.textPositions = []
        for t_p in range(10):
            t_j = ( -1.30, 0, 0.95 - (t_p * 0.05) )
            self.textPositions.append(t_j)
        # append the events label position
        self.textPositions.append(( -1.30, 0, 0.45))
        # title
        self.textPlay.loadTextLine('Nairobi Project Traffic Sim. Powered by Eden3D', self.textKeys[0])
        # instructions
        self.textPlay.loadTextLine('Press ESCAPE to quit', self.textKeys[1])
        self.textPlay.loadTextLine('Right-Click: Select(Activate) Actor', self.textKeys[2])
        self.textPlay.loadTextLine('Arrow Keys: Control Selected Actor', self.textKeys[3])
        self.textPlay.loadTextLine('Y: Cycle through inventory', self.textKeys[4])
        self.textPlay.loadTextLine('I: Show game information', self.textKeys[5])
        self.textPlay.loadTextLine('D: Show documentation', self.textKeys[6])
        self.textPlay.loadTextLine('EVENTS:', self.textKeys[7])
        # game info
        self.textPlay.loadTextLine(self.gameID, 'Game')
        # manual text
        t_n =  self.gameMVC.mvcStructure['tier_resource']['text'] + '/TrafficSim.txt'
        self.textPlay.loadTextFile(t_n, 'Doc')
        # collision notice
        self.textPlay.loadTextLine('Miranda hit Ralph!', 'notice')
        self.textPlay.loadTextLine('Ralph hit Miranda!', 'notice2')
        # setup key mappings
        self.accept("y", self.pickTool, [])
        self.accept("s", self.screenCapture, ['../EveAdvanced_'])
        self.accept("d", self.textPlay.displayText, ['Doc', 30, (-0.70,0,0.45), False])
        self.accept("i", self.textPlay.displayText, ['Game', 30, (0.05,0,0.95), False])
        self.accept("c", self.textPlay.clearScreen)
        self.accept("v", self.edenVisuals.media['video'][0][1].stop, [])
        # accept switching message
        self.accept('actor-switch', self.switchHandler, [])
    # ------------------BEHAVIORS-------------------------
    # ----------------------------------------------------
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
        "prints an event to the list on the screen"
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
        # resolve health (for now we just set)
        t_h = 'Health - 100%'
        self.hudBrush.menuList['Unit']['labels']['Name']['text'] = t_n
        self.hudBrush.menuList['Unit']['labels']['Sex']['text'] = t_x
        self.hudBrush.menuList['Unit']['labels']['Sex']['text_fg'] = t_c
        self.hudBrush.menuList['Unit']['labels']['Health']['text'] = t_h
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
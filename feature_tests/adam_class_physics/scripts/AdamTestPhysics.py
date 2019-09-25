# Package Description: Funtrench's Eden Software Development Kit
# Name: Eden Feature Tests SDK
# Desc: Advanced Physics Test Project for the Adam Class
# File name: AdamTest.py
# Developed by: Project Eden Development Team
# Date: 12/08/2008
# Place: Nairobi, Kenya
# |------------------------------------------------|
# | (C)2009 Funtrench Limited.            |
# |------------------------------------------------|
from Eden.Eden3D.Worlds.Adam import Adam
from Eden.Eden2D.Text2D import Text2D
from direct.task import Task
from panda3d.core import Point3
from direct.interval.IntervalGlobal import *
# --------------------------------------------------
# A class to demonstrate the features of the Adam
# Class with unmoused camera. Physics demonstrated.
# Class definition for the AdamTestPhysics class
# --------------------------------------------------
class AdamTestPhysics(Adam):
    " Extending the Adam class for two actors in a physical world "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        Adam.__init__(self, self.starterTask) # ancestral constructor
        self.videoDone = False
        self.eventListPos = 0.40
        t_f = [('arial.egg', 'Arial')]
        self.textPlay = Text2D(self.edenVisuals.fpsValue, t_f)
        # load other objects (the ViS Cube)
        self.loadGeometry('cube', 'cube', (0.25,0.25,0.25), (0,0,5))
        # load bump sound
        self.loadSoundEffect('bump.snd', 'bump')
        # add the animation task to the task manager
        taskMgr.add(self.defaultAnimationTask, 'animationTask')
        # load Ralph, and loop his animation
        self.loadActor('Ralph.xml')
        self.sirRalph = self.actorStore['Ralph']
        # set up collision detection for Ralph
        self.setupActorCollision(self.sirRalph.actorData['name'])
        self.sirRalph.loopAnimation('run')
        # ------------------------------------------------------------------
        # Miranda is our main actor
        self.ladyMiranda = self.mainActor
        # accept events for collision
        # parameters in accept() are passed first, then those in send()
        self.accept('Miranda-into-Ralph', self.actorsBumpHandler, [0])
        # ------------------------------------------------------------------
        # load the text resources
        self.textKeys = ['title', 'instruction1', 'instruction2', 'instruction3', \
          'instruction4', 'instruction5', 'instruction6', 'instruction7', \
          'instruction8', 'events']
        # compute the text positions
        self.textPositions = []
        for t_p in range(9):
            t_j = ( -1.30, 0, 0.95 - (t_p * 0.05) )
            self.textPositions.append(t_j)
        # append the events label position
        self.textPositions.append(( -1.30, 0, 0.45))
        # title
        self.textPlay.loadTextLine('Adam Test Physics. Powered by Funtrench', self.textKeys[0])
        # instructions
        self.textPlay.loadTextLine('Press ESCAPE to quit', self.textKeys[1])
        self.textPlay.loadTextLine('Arrow Keys: Control Miranda', self.textKeys[2])
        self.textPlay.loadTextLine('F/B: Increment/Decrement cube X', self.textKeys[3])
        self.textPlay.loadTextLine('G/H: Increment/Decrement cube Y', self.textKeys[4])
        self.textPlay.loadTextLine('A/J: Increment/Decrement cube Z', self.textKeys[5])
        t_eb = "P/N: Activate/Disable Miranda's flying edenBoots!"
        self.textPlay.loadTextLine(t_eb, self.textKeys[6])
        self.textPlay.loadTextLine('I: Show game information', self.textKeys[7])
        self.textPlay.loadTextLine('D: Show documentation', self.textKeys[8])
        self.textPlay.loadTextLine('EVENTS:', self.textKeys[9])
        # game info
        self.textPlay.loadTextLine(self.gameID, 'Game')
        # manual text
        t_n =  self.gameMVC.mvcStructure['tier_resource']['text'] + '/AdamTest.txt'
        self.textPlay.loadTextFile(t_n, 'Doc')
        # collision notice
        self.textPlay.loadTextLine('Miranda hit Ralph!', 'notice')
        # create the four lerp intervals needed to walk Ralph back and forth
        self.sirRalphPosInterval1= self.sirRalph.baseActor.posInterval(10,Point3(0,-15,0), \
                startPos=Point3(0,35,0))
        self.sirRalphPosInterval2= self.sirRalph.baseActor.posInterval(10,Point3(0,35,0), \
                startPos=Point3(0,-10,0))
        self.sirRalphHprInterval1= self.sirRalph.baseActor.hprInterval(3,Point3(180,0,0), \
                startHpr=Point3(0,0,0))
        self.sirRalphHprInterval2= self.sirRalph.baseActor.hprInterval(3,Point3(0,0,0), \
                startHpr=Point3(180,0,0))
        # create and play the sequence that coordinates the intervals
        self.sirRalphPace = Sequence(self.sirRalphPosInterval1, self.sirRalphHprInterval1, \
        self.sirRalphPosInterval2, self.sirRalphHprInterval2, name = "sirRalphPace")
        self.sirRalphPace.loop()
        # setup key mappings
        self.accept("f", self.cubeAlter, [+1, "X"])
        self.accept("b", self.cubeAlter, [-1, "X"] )
        self.accept("g", self.cubeAlter, [+1, "Y"] )
        self.accept("h", self.cubeAlter, [-1, "Y"] )
        self.accept("a", self.cubeAlter, [+1, "Z"] )
        self.accept("j", self.cubeAlter, [-1, "Z"] )
        self.accept("s", self.screenCapture, ['../AdamPhysics_'])
        self.accept("d", self.textPlay.displayText, ['Doc', 30, (-0.70,0,0.50), False])
        self.accept("i", self.textPlay.displayText, ['Game', 30, (0.05,0,0.95), False])
        self.accept("c", self.textPlay.clearScreen)
        self.accept("v", self.edenVisuals.media['video'][0][1].stop, [])
        self.accept("k", self.printEveZ, [])
        # Physics info
        # ASS = 0.1
        # SFC = 0.9
        # DFC = 0.5
        # self.updatePCH()
        # load the forces (the wind is global)
        self.loadForcesfromXML('AdamForcePack.xml')
        # create a jetPack
        self.edenBoots = self.createJetPack('jet', 'edenBoots')
        # apply the jetpack to the actor
        self.accept("p", self.attachJetPackToActor, ['jet', self.edenBoots, 'Miranda'])
        # remove the jetpack from the actor
        self.accept("n", self.removeJetPackFromActor, ['jet', 'edenBoots', 'Miranda'])
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
    def actorsBumpHandler(self, targetNode, entry):
        "handles when Miranda bumps into anything"
        if targetNode == 0:
            # she bumped into Ralph
            # play bump sound
            self.jukeBox['bump'].play()
            self.printEvent('notice')
        else:
            # she bumped into something else (unimplemented)
            pass
    def printEvent(self, eventKey):
        "prints an event to the list on the screen"
        # display event notice for 15 seconds
        self.textPlay.displayText(eventKey, 15.0, (-1.30,0,self.eventListPos))
        # decrement for the next event
        self.eventListPos -= 0.05
        if self.eventListPos == 0.00:
            # restore
            self.eventListPos = 0.40
    def printEveZ(self):
        " prints the main actor's Z position to test terrain detection "
        # display event notice for 15 seconds
        t_s = '%s%f' % ('Z-position is: ', self.ladyMiranda.baseActor.getZ())
        self.textPlay.loadTextLine(t_s, t_s)
        self.textPlay.displayText(t_s, 15.0, (-1.30,0,self.eventListPos))
        # decrement for the next event
        self.eventListPos -= 0.05
        if self.eventListPos <= 0.00:
            # restore
            self.eventListPos = 0.40
    # ------------------TASKS-----------------------------
    # ----------------------------------------------------
    def starterTask(self, task):
        " task to handle the startup "
        if task.time == 0.0:
            # hide the cursor for startup if it is visible
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
                    # show the cursor again if necessary
                    if self.worldData['showMouse'] != 0:
                        self.toggleMouseCursor()
                    # add the camera update task
                    taskMgr.add(self.updateViewTask, 'viewUpdateTask')
                    return task.done
            else:
                # all other frames
                return task.cont
    # Though we have used the defaultAnimationTask of the Adam super-class - which
    # does exactly what the task below does, we could have used this one. The
    # advantage of using the default one in Adam is that it gets all settings from
    # the XML file of the main actor, making it a generic function that can be used
    # even where the main actor is variable - such as in the Eve super-class.
    # The task below is NOT used in this sample and CAN therefore be deleted.
    def animationTask(self, task):
        " task to move camera and active actor "
        # enable animation
        if True in self.controller.values():
            if self.ladyMiranda.baseActor.getTag('Animated') == 'False':
                if self.mods['run'] == True:
                    self.ladyMiranda.loopAnimation('run')
                else:
                    self.ladyMiranda.loopAnimation('walk')
                self.ladyMiranda.baseActor.setTag('Animated', 'True')
        else:
            if self.ladyMiranda.baseActor.getTag('Animated') == 'True':
                self.ladyMiranda.stopAnimation()
                self.ladyMiranda.baseActor.pose('walk', 2)
                self.ladyMiranda.baseActor.setTag('Animated', 'False')
        return task.cont
        

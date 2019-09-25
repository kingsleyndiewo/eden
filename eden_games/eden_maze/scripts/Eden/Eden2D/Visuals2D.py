# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden2D]
# Desc: Visuals Rendering Library - Visuals2D Class
# File name: Visuals2D.py
# Developed by: Project Eden Development Team
# Date: 26/06/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench PLC
# ---------------------------------------------
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from random import randint
from pandac.PandaModules import *
# ---------------------------------------------
# A class to handle the drawing of 2D images/video.
# GIF images are not supported! Use PNG or TGA
# AVI and MPG video only
# Class definition for the Visuals2D class
# ---------------------------------------------
class Visuals2D:
    " The base class for all 2D renderers "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, msgr, fpsValue = 60.0, screenRes = (800.0, 600.0) ):
        # initialize the media list
        self.media = { 'images':[], 'video':[] }
        # initialize variables
        self.virginFlag = True # the surface is empty
        self.waitVideo = False
        self.msgService = msgr
        # create the video display card
        self.videoCard = CardMaker('Eden Fullscreen')
        self.videoCard.setFrameFullscreenQuad()
        # based on the resolution we can scale the aspect2d
        # y ranges from (-1, 1) while x ranges from (-ratio, ratio)
        t_ratio = screenRes[0] / screenRes[1]
        self.aspectScale = (t_ratio, 1.0, 1.0)
        self.nodeScale = Vec3(t_ratio, 1.0, 1.0)
        # if a delay of X seconds is requested, we compute the number
        # of frames this implies as (self.fpsValue * X). Then we can
        # use task.frame directly as our elapsed frame value.
        self.fpsValue = fpsValue
        # task dictionary
        self.soloRegister = {}
    # ------------------DESTRUCTOR------------------------
    # ----------------------------------------------------
    def __del__(self):
        if self.virginFlag != True:
            # destroy the surface object
            self.Surface.destroy()    
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    # --------------------------RESOURCE LOADING-----------------------------
    def loadImage(self, fileName, xyzPos = (0, 0, 0) ):
        " loads an image to the list "
        # xyzPos is a tuple with y always 0 since x always represents east-west
        # and z always represents north-south. y is unused in aspect2d
        t_x = loader.loadTexture(fileName)
        self.media['images'].append([t_x, xyzPos])
    def loadVideo(self, fileName, xyzPos = (0, 0, 0), audioVolume = 0.5 ):
        " loads a video to the list "
        # xyzPos is a tuple with y always 0 since x always represents east-west
        # and z always represents north-south. y is unused in aspect2d
        # we convert it to a Vec3
        xyzPos = Vec3(xyzPos[0], xyzPos[1], xyzPos[2])
        # we use the new MovieTexture class (14/05/09)
        # -------------------------------------------
        t_x = MovieTexture('video')
        t_x.read(fileName)
        # instead of t_x = loader.loadTexture(fileName)
        # -------------------------------------------
        # we have to synchronize a video to its sound
        # we use OpenAL instead of FMOD in the Config.prc file
        # now (14/05/09): audio-library-name p3openal_audio
        t_y = loader.loadSfx(fileName)
        t_y.setVolume(audioVolume)
        # synchronize the video to the sound
        t_x.synchronizeTo(t_y)
        self.media['video'].append([t_x, t_y, xyzPos])
    # -----------------------------------------------------------------------
    # --------------------------MEDIA DISPLAY--------------------------------       
    def sequenceAllImages(self, intervalSec, cleanUp = True):
        " show the sequence of images, each for <interval> sec "
        # to make each task name unique we will mangle the name a bit
        t_g = randint(3, 300)
        t_k = randint(301, 500)
        t_t = '%d%d%d' % (t_g, intervalSec, t_k)
        # add the switcher task to the taskmanager
        taskMgr.add(self.switcherTask, t_t)
        # if intervalSec is negative or 0 we assume default
        if intervalSec <= 0:
            intervalSec = 3
        t_invl = intervalSec * self.fpsValue
        self.soloRegister[t_t] = [t_invl, cleanUp, 0]
    def displayImage(self, listIndex, intervalSec):
        " show an image for <interval> sec "
        # to make each task name unique we will mangle the name a bit
        t_g = randint(3, 300)
        t_k = randint(301, 500)
        # here we are assured of a truly unique value
        t_t = '%d%d%d' % (listIndex, t_g, t_k)
        # add the solo task to the taskmanager
        taskMgr.add(self.soloImageTask, t_t)
        # if intervalSec is negative we assume user means 0
        if intervalSec < 0:
            intervalSec = 0
        t_invl = intervalSec * self.fpsValue
        self.soloRegister[t_t] = [t_invl, listIndex]
    def displayVideo(self, listIndex, intervalSec = 0):
        " show a video for <interval> sec "
        # to make each task name unique we will mangle the name a bit
        t_g = randint(3, 300)
        t_k = randint(301, 500)
        # here we are assured of a truly unique value
        t_t = '%d%d%d' % (listIndex, t_g, t_k)
        # add the solo task to the taskmanager
        taskMgr.add(self.soloVideoTask, t_t)
        # if interval is 0 then we will play to the end (the default)
        # and if it is negative we assume user means 0
        if intervalSec < 0:
            intervalSec = 0
        t_invl = intervalSec * self.fpsValue
        self.soloRegister[t_t] = [t_invl, listIndex, False]
        # preprocess the card to avoid doing that during the task
        self.videoCard.setUvRange(self.media['video'][listIndex][0])
        self.Surface = NodePath(self.videoCard.generate())
        self.Surface.setScale(self.nodeScale)
        self.Surface.setPos(self.media['video'][listIndex][2])
    def blitImage(self, listIndex, delayValue = 0.0):
        " switch an image with another ( ideally of identical properties ) "
        # to make each task name unique we will mangle the name a bit
        t_g = randint(3, 300)
        t_k = randint(301, 500)
        # here we are assured of a truly unique value
        t_t = '%d%d%d' % (listIndex, t_g, t_k)
        # add the blit task to the taskmanager
        taskMgr.doMethodLater(delayValue, self.blitTask, t_t)
        self.soloRegister[t_t] = listIndex
    # -----------------------------------------------------------------------
    # ---------------------------SURFACE UTILITY FUNCTIONS-------------------
    def enableAlpha(self):
        " enables transparency on the screen "
        if self.virginFlag == False:
            self.Surface.setTransparency(TransparencyAttrib.MAlpha)
        else:
            # defer the enabling
            self.alphaWanted = True
    def clearScreen(self):
        " clears the surface( everything on aspect2d drawn from here ) "
        if self.virginFlag != True:
            # destroy the surface object
            self.Surface.destroy()
            self.virginFlag = True
    def saveScreenShot(self, fileName, screenShotFolder = None, imageComment = ''):
        " saves a screenshot of the scene to the filename "
        # the extension provided will determine the format
        if screenShotFolder == None:
            t_f = fileName
        else:
            t_f = screenShotFolder + fileName
        base.screenshot(t_f, 0, None, imageComment)
    def saveSequencedImages(self, filePrefix, length, fpsValue, movieFolder = None, \
        fileExtension = 'png', counterSize = 4):
        " save a movie of sequenced images "
        if movieFolder == None:
            t_f = filePrefix
        else:
            t_f = movieFolder + filePrefix
        # the extension provided will determine the format
        base.movie(t_f, length, fpsValue, fileExtension, counterSize)
    # -----------------------------------------------------------------------
    # --------------------------INTERNAL BEHAVIOURS--------------------------
    def showImage(self, listIndex):
        " displays an image in the list "
        self.Surface = OnscreenImage(image = self.media['images'][listIndex][0], \
            pos = self.media['images'][listIndex][1], scale = self.aspectScale)
        if self.virginFlag != False:
            self.virginFlag = False
        if self.alphaWanted == True:
            self.enableAlpha()
            self.alphaWanted = False
    def showVideo(self, listIndex):
        " displays a video in the list "
        self.Surface.setTexture(self.media['video'][listIndex][0])
        self.Surface.reparentTo(aspect2d)
        if self.virginFlag != False:
            self.virginFlag = False
        # synchronize to sound
        self.media['video'][listIndex][1].play()
    def switchImage(self, listIndex):
        " does a form of blitting "
        # use only for images that have same on-screen position!
        if self.virginFlag != False:
            # the surface is empty
            return False
        else:
            # just switch images (position is ignored)
            self.Surface.setImage(self.media['images'][listIndex][0])
            return True
    # --------------------------------TASKS----------------------------------
    # -----------------------------------------------------------------------
    def switcherTask(self, task):
        " switches images from list "
        # remember that the 1st image is not shown yet
        if task.time == 0.0:
            # show the first image
            self.showImage(0)
            self.soloRegister[task.name][2] = 1
            return task.cont
        elif (task.frame / self.soloRegister[task.name][2]) == \
            self.soloRegister[task.name][0]:
            # time for next image
            self.soloRegister[task.name][2] += 1
            if len(self.media['images']) >= self.soloRegister[task.name][2]:
                # safe to show, image exists
                self.switchImage(self.soloRegister[task.name][2] - 1)
                return task.cont
            else:
                # out of images!
                if self.soloRegister[task.name][1] == True:
                    # clear the screen
                    self.clearScreen()
                    # notify the system
                    self.msgService('sequence-done')
                return task.done
        else:
            # all other frames
            return task.cont
    def soloImageTask(self, task):
        " delays for a single image in list "
        # remember that the image is not shown
        if task.time == 0.0:
            # show the image
            self.showImage(self.soloRegister[task.name][1])
            if self.soloRegister[task.name][0] == 0:
                # no delay; don't erase
                return task.done
            else:
                # we have a valid delay
                return task.cont
        elif task.frame == self.soloRegister[task.name][0]:
            # time for erasure
            self.Surface.destroy()
            self.virginFlag = True
            # notify the system
            self.msgService('image-done')
            return task.done
        else:
            # all other frames
            return task.cont
    def soloVideoTask(self, task):
        " delays for a single video in list "
        # remember that the video is not shown
        if task.time == 0.0:
            # show the video
            self.showVideo(self.soloRegister[task.name][1])
            if self.soloRegister[task.name][0] == 0:
                # no delay; erase when done
                self.soloRegister[task.name][2] = True
            else:
                # we have a valid delay
                pass
            return task.cont
        elif (self.soloRegister[task.name][2] == False):
            if task.frame == self.soloRegister[task.name][0]:
                # time for erasure; no waiting for end
                self.Surface.destroy()
                self.virginFlag = True
                # notify the system
                self.msgService('video-done')
                return task.done
            else:
                # all other frames
                # just return
                return task.cont
        else:
            # check video status
            if self.media['video'][self.soloRegister[task.name][1]][1].status() == 1:
                # the video has stopped playing
                self.Surface.removeNode()
                self.virginFlag = True
                # notify the system
                self.msgService('video-done')
                return task.done
            else:
                # all other frames
                return task.cont
    def blitTask(self, task):
        " blits an image "
        # we will not assume an image is displayed
        if self.virginFlag == True:
            # no image on the screen
            return task.done
        else:
            self.switchImage(self.soloRegister[task.name])
            return task.done
                
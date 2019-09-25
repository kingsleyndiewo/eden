# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Worlds]
# Desc: Worlds Library - Creation Class
# File name: Creation.py
# Developed by: Project Eden Development Team
# Date: 30/06/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench Limited
# ---------------------------------------------
from direct.showbase.ShowBase import ShowBase
from Eden.Eden2D.Visuals2D import Visuals2D
from Eden.EdenTools.Systemic.MVC import *
from Eden.EdenTools.Systemic.SystemSensor import SystemSensor
from Eden.EdenTools.ParticleSystem.ParticleGenerator import ParticleGenerator
from Eden.EdenTools.XMLParsers.ConfigParser import ConfigParser
from Eden.Eden3D.Terrain.GeoMipMapper import GeoMipMapper
from panda3d.core import *
import sys
import math
from time import gmtime, localtime, strftime, time
# ---------------------------------------------
# A class that implements a basic world with nothing
# in it. Entry point for a 3D application.
# Startup options are loaded from config.xml
# Class definition for the Creation class
# ---------------------------------------------
class Creation(ShowBase):
    " The base class for all 3D worlds "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, remoteStarterTask = None, customPRC = None, edenClass = 'Creation'):
        # initialize the data dictionary
        # the edenClass variable is used to set the Eden super-class
        # used by the game. The descendant sets it when calling the
        # base class constructor
        self.worldData = {'edenClass':edenClass}
        self.mediaFlag = [0, 0]
        self.camfixFlag = False
        self.oobeFlag = False
        self.spinFlag = False
        self.spinFactor = 0
        self.lockMouse = False
        self.capCount = 0
        self.GFP = 'GFG-'
        self.clockInitTime = None
        self.physicsEngine = None
        self.enginesList = ['Panda', 'ODE']
        # the Z-value of the terrain detector collision ray
        self.detectorHeight = 2.0
        # get the system information
        self.systemInfo = SystemSensor(customData = customPRC)
        # import direct start here, after system sensor has run
        # -----------------------------------------------------
        ShowBase.__init__(self)
        # -----------------------------------------------------
        # check MVC structure (we must be in the scripts directory!)
        # self.worldData will contain the MVC data
        self.checkMVC('../')
        # at this point we have a valid MVC structure
        # create a new node path just under render for geometry
        self.geometryNode = render.attachNewNode('Geometry')
        # create another for actors
        self.actorsNode = render.attachNewNode('Actors')
        # create a node path to allow manipulation of loaded geometry without
        # affecting the pre-loaded stuff from config.xml
        self.staticsNode = self.geometryNode.attachNewNode('Statics')
        # create a special node just for the world
        self.worldNode = self.geometryNode.attachNewNode('worldRoot')
        # create a node for physics-enabled geometry
        self.geoPhysicsNode = self.staticsNode.attachNewNode('geoPhysics')
        # create a node for physics-enabled actors
        self.actorPhysicsNode = self.actorsNode.attachNewNode('actorPhysics')
        if self.worldData['isGenerated'] == False:
            # load the world model
            self.world = loader.loadModel(self.worldData['worldPath'])
            self.world.reparentTo(self.worldNode)
            # set the world scaling
            t_y = self.worldData['worldScale']
            self.world.setScale(t_y[0], t_y[1], t_y[2])
        else:
            # generate the terrain (it will be parented to self.worldNode)
            self.world = self.makeTerrain(self.worldData['worldPath'])
            # set the world scaling (only X and Y), Sz was set by the terrain
            # generator
            t_y = self.worldData['worldScale']
            self.world.setSx(t_y[0])
            self.world.setSy(t_y[1])
        # set the world position
        t_o = self.worldData['worldPosition']
        self.world.setPos(t_o[0], t_o[1], t_o[2])
        # create the window handle
        self.winHandle = [WindowProperties(), False]
        # check cursor status
        if self.worldData['showMouse'] == 0:
            # hide the cursor
            self.toggleMouseCursor()
        if self.camfixFlag == True:
            # disable the mouse in scene
            base.disableMouse()
            # set the camera position
            base.camera.setPos(self.worldData['cameraPos'][0], \
                self.worldData['cameraPos'][1], self.worldData['cameraPos'][2])
            base.camera.setHpr(self.worldData['cameraHpr'][0], \
                self.worldData['cameraHpr'][1], self.worldData['cameraHpr'][2])
        if self.lockMouse == True:
            # just disable the mouse; no positions
            base.disableMouse()
        # a dictionary for loaded geometry
        self.objectStore = {}
        # a dictionary for loaded sounds
        self.jukeBox = {}
        # a dictionary for the physics engine
        self.physicsStore = {'actors':{}, 'geometry':{}, 'forces':{}, \
            'globalForces':[]}
        # enable the particle system; we need it even if physics is
        # not used
        self.initParticleSystem()
        if self.worldData['enablePhysics'] == 1:
            # initialize the physics engine
            self.initPhysics()
        else:
            # set up non-physics terrain detection
            # create a terrain altitude detector
            self.terrainDetector = CollisionHandlerFloor()
        # set the key mappings
        self.accept("escape", sys.exit, [0])
        # add the starterTask
        if remoteStarterTask == 'Default':
            # add a default that depends on the visuals status
            if 1 in self.mediaFlag:
                # add the default startup task to the taskmanager
                # this task DOES NOT handle video yet!
                taskMgr.add(self.defStarterTask, 'Startup')
        elif remoteStarterTask == None:
            # do nothing
            pass
        else:
            # add the startup task to the taskmanager
            taskMgr.add(remoteStarterTask, 'Startup')
        # common components of the terrain detector (physics-independent)
        self.terraTrav = CollisionTraverser('terraDetector')
        # make the provision for fast-moving objects
        self.terraTrav.setRespectPrevTransform(True)
        # add the terrain detector task to the taskmanager
        taskMgr.add(self.terrainTask, 'terraDetector')
        # set the terrain detection flag to false initially
        self.terraDetection = False
        # for various useful operations, set a tag on the world
        self.world.setTag('EdenGeometry', 'Ground')
        # add the clock task to the task manager
        taskMgr.add(self.worldClockTask, 'edenTimeTask')
        # create an XPU for forces
        self.forceXPU = ConfigParser()
        # get a handle to the mouse watcher node (convenience)
        self.mouseWatch = base.buttonThrowers[0].getParent()
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    # --------------------------RESOURCE LOADING-----------------------------
    def loadGeometry(self, modelFile, modelName, scale = (1.0, 1.0, 1.0), \
        xyzPos = (0, 0, 0), extraData = {'parentNode':None, 'bitMask':None, \
            'sphereFactor':1.0, 'enablePhysics':False, 'objectMass':0, \
            'terrainDetection':False, 'odeMass':None}):
        " loads a model into the world "
        # to maintain compatibility with old code (08/07/09)
        t_ed = {'parentNode':None, 'bitMask':None, 'sphereFactor':1.0, \
            'enablePhysics':False, 'objectMass':0, 'terrainDetection':False, \
            'odeMass':None}
        for t_z in t_ed.keys():
            if t_z not in extraData.keys():
                extraData[t_z] = t_ed[t_z]
        if extraData['parentNode'] == None:
            extraData['parentNode'] = self.staticsNode
        if extraData['bitMask'] == None:
            # set default bitmask
            extraData['bitMask'] = self.geometryNode.getCollideMask()
        # build the path to the static objects (non-animated)
        t_m = self.gameMVC.mvcStructure['tier_models']['geometry'] + '/' + modelFile
        # the model is stored as [model, visibility]
        self.objectStore[modelName] = [loader.loadModel(t_m), True]
        self.objectStore[modelName][0].setScale(scale[0],scale[1],scale[2])
        self.objectStore[modelName][0].setPos(xyzPos[0],xyzPos[1],xyzPos[2])
        # we append useful collision information as 3rd element
        t_b = self.objectStore[modelName][0].getChild(0).getBounds()
        try:
            t_r = t_b.getRadius()
            t_c = t_b.getCenter()
        except:
            t_r = 1.0
            t_c = 1.0
        t_k = t_r * extraData['sphereFactor']
        t_d = {'center':t_c, 'weightedRadius':t_k}
        self.objectStore[modelName].append(t_d)
        # set its bitmask to match its parent
        self.objectStore[modelName][0].setCollideMask(extraData['bitMask'])
        self.objectStore[modelName][0].reparentTo(extraData['parentNode'])
        if extraData['enablePhysics'] == False:
            # we append physics status as the fourth element
            self.objectStore[modelName].append(False)
        else:
            # enable physics on the model
            self.enableObjectPhysics(modelName, extraData)
            if extraData['objectMass'] != 0:
                # set the mass of the object
                self.setObjectMass(modelName, extraData['objectMass'], extraData['odeMass'])
            # apply all global forces on the object
            for t_gf in self.physicsStore['globalForces']:
                self.attachForceToObject(modelName, self.GFP + t_gf)
            if extraData['terrainDetection'] == True and \
                self.physicsEngine == self.enginesList[0]:
                # setup common terrain detection components (physics-independent
                # but not available for ODE)
                # setup terrain detection on the object
                t_tcn = self.objectStore[modelName] \
                    [0].attachNewNode(CollisionNode(modelName + '_TCN'))
                # the ray points directly downward and begins at (0,0,self.detectorHeight)
                t_tcn.node().addSolid(CollisionRay(0, 0, self.detectorHeight, 0, 0, -1))
                # set the bitmasks
                t_tcn.node().setFromCollideMask(extraData['bitMask'])
                t_tcn.node().setIntoCollideMask(BitMask32.allOff())
                # add to the collision handler (physics-dependent)
                if extraData['enablePhysics'] == False:
                    # CollisionHandlerFloor
                    self.terrainDetector.addCollider(t_tcn, \
                        self.objectStore[modelName][0])
                else:
                    # CollisionHandlerGravity
                    self.terrainDetector.addCollider(t_tcn, \
                        self.physicsStore['geometry'][modelName][1])
                # add to the collision traverser
                self.terraTrav.addCollider(t_tcn, self.terrainDetector)
                # set the flag if not set
                if self.terraDetection != True:
                    self.terraDetection = True
    def loadSoundEffect(self, soundFile, soundName, fxVolume = 0.5):
        " loads a sound effect into the world jukebox "
        # build a path to the sound effect
        t_j = self.gameMVC.mvcStructure['tier_sound']['effects'] + '/' + soundFile
        # the effect is stored in the jukebox
        self.jukeBox[soundName] = loader.loadSfx(t_j)
        # set the volume
        self.jukeBox[soundName].setVolume(fxVolume)
    def loadMusic(self, soundFile, soundName, fxVolume = 0.5):
        " loads a music resource into the world jukebox "
        # build a path to the music
        t_j = self.gameMVC.mvcStructure['tier_sound']['music'] + '/' + soundFile
        # the music is stored in the jukebox
        self.jukeBox[soundName] = loader.loadSfx(t_j)
        # set the volume
        self.jukeBox[soundName].setVolume(fxVolume)
    def makeTerrain(self, terrainXML):
        " makes a new terrain based on the terrainXML details "
        # we will need a dictionary
        t_d = {}
        # parse the terrain configuration (XPU = XML processing unit)
        terraXPU = ConfigParser()
        terraXPU.parseFile(terrainXML)
        # get terrain information
        terraXPU.getSectionValues('section','terrainDetails')
        for t_x in terraXPU.Parser['XML_Values']['terrainDetails_Values'].keys():
            t_d[t_x] = terraXPU.Parser['XML_Values']['terrainDetails_Values'][t_x]
        # set the focal point node as required
        if terraXPU.Parser['XML_Values']['terrainDetails_Values'] \
            ['focalPointNode'] == 0:
            # camera is the focal point
            t_d['focalPointNode'] = base.camera
        else:
            # we have co-ordinates
            t_d['focalPointNode'] = Point3(t_d['focalX'], t_d['focalY'], t_d['focalZ'])
        # load the texture if provided
        if terraXPU.Parser['XML_Values']['terrainDetails_Values'] \
            ['textured'] == 1:
            # build a path to the filename
            t_j = self.gameMVC.mvcStructure['tier_resource']['images'] + '/' + \
                terraXPU.Parser['XML_Values']['terrainDetails_Values'] \
                ['baseTexture']
            # load the texture
            t_d['baseTexture'] = loader.loadTexture(t_j)
        # set the path for textures
        t_d['terrainPath'] = self.gameMVC.mvcStructure['tier_resource']['images'] \
            + '/terrain/'
        # make the terrain
        self.GMMT = GeoMipMapper(t_d, self.worldNode)
        return self.GMMT.baseTerrain
    # -----------------------------------------------------------------------
    # --------------------------UTILITY SERVICES-----------------------------
    def screenCapture(self, fileNamePrefix = 'edenShot_', fileExtension = '.jpg'):
        " captures the screen instantly to a file in current directory "
        t_r = '%s%d%s' % (fileNamePrefix, self.capCount, fileExtension)
        self.edenVisuals.saveScreenShot(t_r)
        self.capCount += 1
    def recordSIVideo(self, recordDuration, framesPerSecond, videoFolder, \
        imageFilePrefix = 'edenVideo_', fileExtension = 'png', digits = 4):
        " records a sequenced-image video to files in the folder specified "
        # warning! the game will slow down considerably during recording
        # try lower FPS values
        self.edenVisuals.saveSequencedImages(imageFilePrefix, recordDuration, \
            framesPerSecond, videoFolder, fileExtension, digits)
    # -----------------------------------------------------------------------
    # ----------------------------SOUND SERVICES-----------------------------
    def setSoundVolume(self, jukeKey, newVolume):
        " sets the volume of a loaded sound "
        if jukeKey not in self.jukeBox.keys():
            # the specified sound does not exist in the jukebox
            return False
        else:
            # check volume value
            if newVolume < 0.0:
                newVolume = 0.0
            elif newVolume > 1.0:
                newVolume = 1.0
            # apply the new volume
            self.jukeBox[jukeKey].setVolume(newVolume)
    def setJukeBoxVolume(self, newVolume):
        " sets the volume of the entire jukebox (effects & music) "
        # check volume value
        if newVolume < 0.0:
            newVolume = 0.0
        elif newVolume > 1.0:
            newVolume = 1.0
        # apply the new volume
        for t_x in self.jukeBox.values():
            t_x.setVolume(newVolume)
    def setSoundPan(self, newPan = 0.0):
        " pan a sound; hard left is -1.0 and hard right is 1.0 "
        # of course the center is 0.0, we default it to hint to everyone
        # that changing it from 0.0 isn't really such a good idea
        if jukeKey not in self.jukeBox.keys():
            # the specified sound does not exist in the jukebox
            return False
        else:
            # check pan value
            if newPan < -1.0:
                newPan = -1.0
            elif newPan > 1.0:
                newPan = 1.0
            # apply the new pan
            self.jukeBox[jukeKey].setBalance(newVolume)
    def getSoundLength(self, jukeKey):
        " returns the length of the sound in seconds "
        if jukeKey not in self.jukeBox.keys():
            # the specified sound does not exist in the jukebox
            return False
        else:
            # check length
            return self.jukeBox[jukeKey].length()
    # -----------------------------------------------------------------------
    # --------------------------OBJECT MANIPULATION--------------------------
    def hideObject(self, objectName):
        " conceals a visible object (does not destroy it) "
        if objectName not in self.objectStore.keys():
            # the specified object does not exist in the world
            return False
        elif self.objectStore[objectName][1] == False:
            # object is already hidden
            pass
        else:
            # hide the object
            self.objectStore[objectName][0].hide()
            self.objectStore[objectName][1] = False
    def showObject(self, objectName):
        " reveals a hidden object "
        if objectName not in self.objectStore.keys():
            # the specified object does not exist in the world
            return False
        elif self.objectStore[objectName][1] == True:
            # object is already visible
            pass
        else:
            # show the object
            self.objectStore[objectName][0].show()
            self.objectStore[objectName][1] = True
    def moveObject(self, objectName, newPos):
        " moves an object to a new position in the world "
        # just enriching the SDK, setPos() is adequate enough
        if objectName not in self.objectStore.keys():
            # the specified object does not exist in the world
            return False
        else:
            # move the object
            self.objectStore[objectName][0].setPos(newPos[0],newPos[1],newPos[2])
    def moveGroundObject(self, objectName, newPos):
        " moves an object to a new position in the world with Z constant "
        if objectName not in self.objectStore.keys():
            # the specified object does not exist in the world
            return False
        else:
            # we assume that X and Y are the first 2, so a 2-tuple can
            # be passed without issue
            self.objectStore[objectName][0].setX(newPos[0])
            self.objectStore[objectName][0].setY(newPos[1])
    def getModifierKeyState(self, modKey):
        " returns the state of CONTROL, ALT or SHIFT key "
        if modKey == 'ALT' or modKey == 0:
            return base.getAlt()
        elif modKey == 'SHIFT' or modKey == 1:
            return base.getShift()
        elif modKey == 'CONTROL' or modKey == 2:
            return base.getControl()
    # -----------------------------------------------------------------------
    # --------------------------PARTICLE SERVICES----------------------------
    def initParticleSystem(self):
        " initializes the particle system and any support processes "
        base.enableParticles()
        # create the dictionary to store the generators
        self.pGenStore = {}
    def createParticleGenerator(self, pGenName):
        " creates a particle generator and stores in the global pGen store "
        t_p = ParticleGenerator()
        self.pGenStore[pGenName] = t_p
    def loadParticlesFile(self, particleFile, pGenName, fileSource = 0, \
        fileType = 0):
        " loads a particle configuration/XML file to the named generator "
        if pGenName not in self.pGenStore.keys():
            # the specified generator does not exist in the world
            return False
        else:
            # load the given file
            if fileType == 0:
                # load XML
                # get the images path
                t_p = self.gameMVC.mvcStructure['tier_resource']['images'] + '/'
                t_p2 = self.gameMVC.mvcStructure['config'] + '/particles/'
                t_d = {'mvcImagePath':t_p, 'mvcConfigPath':t_p2}
                self.pGenStore[pGenName].loadXMLConfig(particleFile, t_d)
            else:
                if fileSource == 0:
                    # we build a path to config/particles
                    t_s = self.gameMVC.mvcStructure['config'] + '/particles/'
                    t_s += particleFile
                    self.pGenStore[pGenName].loadDriver(t_s)
                else:
                    # this is a full path
                    self.pGenStore[pGenName].loadDriver(particleFile)
    def setGeneratorOrigin(self, pGenName, nodePath, xyzPos):
        " sets the origin of a particle generator "
        if pGenName not in self.pGenStore.keys():
            # the specified generator does not exist in the world
            return False
        else:
            # set the origin (birth point for particles)
            self.pGenStore[pGenName].setOrigin(nodePath, xyzPos)
    # -----------------------------------------------------------------------
    # --------------------------PHYSICS SERVICES-----------------------------
    def initPhysics(self):
        " initializes the world for physics operations "
        # read physics settings
        self.XPU.getSectionValues('subsection','Physics')
        self.physicsEngine = self.XPU.Parser['XML_Values']['Physics_Values']['physicsEngine']
        if self.physicsEngine == self.enginesList[0]:
            # setup Panda Physics
            self.physicsManager = base.physicsMgr   
            # create the universal force node
            self.universalFN = ForceNode('universal')
            # create the node path for universal forces
            self.universalNode = render.attachNewNode(self.universalFN)
            # ensure the flag is set
            self.worldData['enablePhysics'] = 1
            # setup physics terrain detection
            # create a terrain altitude detector
            self.terrainDetector = CollisionHandlerGravity()
            if 'extraManager' in self.XPU.Parser['XML_Values']['Physics_Values']:
                # check whether it is needed
                if self.XPU.Parser['XML_Values']['Physics_Values'] \
                    ['extraManager'] == 1:
                    # create an extra physics manager for special operations
                    self.extraPhysicsManager = PhysicsManager()
                    # create and attach its integrators
                    t_lei = LinearEulerIntegrator()
                    t_aei = AngularEulerIntegrator()
                    self.extraPhysicsManager.attachLinearIntegrator(t_lei)
                    self.extraPhysicsManager.attachAngularIntegrator(t_aei)
                    # add a task to update the physics manager
                    taskMgr.add(self.updatePhysics, 'managerUpdate')
                else:
                    # no extra manager
                    pass
        elif self.physicsEngine == self.enginesList[1]:
            # setup ODE physics
            self.odeWorld = OdeWorld()
            self.loadODESettings()
            # ensure the flag is set
            self.worldData['enablePhysics'] = 1
            # initialize the simulation time
            self.odeStepSize = 1.0 / self.edenVisuals.fpsValue
            self.OdeDta = 0.0
            # add to task manager
            taskMgr.doMethodLater(1.0, self.odeSimulationTask, "ODE Simulation")
        else:
            # no valid engine
            # ensure the flag is reset
            self.worldData['enablePhysics'] = 0
            return False
        # check gravity
        if self.XPU.Parser['XML_Values']['Physics_Values']['globalGravity'] == 1:
            # enable standard global gravity
            self.setGlobalGravity()
        elif self.XPU.Parser['XML_Values']['Physics_Values'] \
            ['globalGravity'] == 2:
            # enable a custom global gravity
            t_h = self.XPU.Parser['XML_Values']['Physics_Values']['gravity']
            self.setGlobalGravity(t_h)
        else:
            # default is no gravity
            pass
    def enableObjectPhysics(self, objectName, odeData = None):
        " enables physics for an object "
        if objectName not in self.objectStore.keys():
            # the specified object does not exist in the world
            return False
        else:
            if self.physicsEngine == self.enginesList[0]:
                # Panda physics
                t_s = objectName + '-physics'
                # we store the ActorNode as (NodePath, Node)
                t_a = ActorNode(t_s)
                t_n = self.geoPhysicsNode.attachNewNode(t_a)
                self.physicsStore['geometry'][objectName] = [t_n, t_a]
                self.physicsManager.attachPhysicalNode(t_a)
                # reparent the object to the new physics node
                self.objectStore[objectName][0].reparentTo(t_n)
            elif self.physicsEngine == self.enginesList[1]:
                # ODE Physics
                t_b = OdeBody(self.odeWorld)
                t_b.setPosition(self.objectStore[objectName][0].getPos(render))
                t_b.setQuaternion(self.objectStore[objectName][0].getQuat(render))
                # we store the ODE body in the physicsStore
                self.physicsStore['geometry'][objectName] = [t_b]
                # setup collision geometry for ODE
                if odeData['odeMass']['collisionShape'] == 0:
                    t_cg = OdeBoxGeom(self.odeSpace, odeData['odeMass']['X'], \
                        odeData['odeMass']['Y'], odeData['odeMass']['Z'])
                elif odeData['odeMass']['collisionShape'] == 1:
                    t_cg = OdeCappedCylinderGeom(self.odeSpace, odeData['odeMass']['radius'], \
                        odeData['odeMass']['length'])
                elif odeData['odeMass']['collisionShape'] == 2:
                    t_cg = OdeCylinderGeom(self.odeSpace, odeData['odeMass']['radius'], \
                        odeData['odeMass']['length'])
                elif odeData['odeMass']['collisionShape'] == 3:
                    t_cg = OdePlaneGeom(self.odeSpace, Vec4(odeData['odeMass'] \
                        ['vector'][0], odeData['odeMass']['vector'][1], odeData['odeMass'] \
                        ['vector'][2], odeData['odeMass']['vector'][3]))
                elif odeData['odeMass']['collisionShape'] == 4:
                    t_cg = OdeRayGeom(self.odeSpace, odeData['odeMass']['rayLength'])
                elif odeData['odeMass']['collisionShape'] == 5:
                    t_cg = OdeSphereGeom(self.odeSpace, odeData['odeMass']['radius'])
                elif odeData['odeMass']['collisionShape'] == 6:
                    t_cg = OdeTriMeshGeom(self.odeSpace, odeData['odeMass']['triMeshData'])
                t_cg.setCollideBits(BitMask32(odeData['bitMask']))
                t_cg.setCategoryBits(odeData['bitMask'])
                t_cg.setBody(self.physicsStore['geometry'][objectName][0])
            # set the physics status - we append physics status as the fourth element
            self.objectStore[objectName].append(True)
    def setObjectMass(self, objectName, newMass, odeMassData = None):
        " sets the mass on a physics-enabled object (KG) "
        if objectName not in self.objectStore.keys():
            # the specified object does not exist in the world
            return False
        elif self.objectStore[objectName][3] == False:
            # physics is not enabled
            return False
        else:
            # we are sure of physics so just set the mass
            if self.physicsEngine == self.enginesList[0]:
                # Panda physics
                self.physicsStore['geometry'][objectName] \
                    [1].getPhysicsObject().setMass(newMass)
            elif self.physicsEngine == self.enginesList[1]:
                # ODE physics
                t_m = self.createODEMass(odeMassData['shape'], newMass, odeMassData)
                # check for attachments
                if odeMassData['other'] != None:
                    for t_x in odeMassData['other']:
                        t_m.add(self.createODEMass(t_x[0], t_x[1], t_x[2]))
                # attach the mass to the body and store the mass object
                self.physicsStore['geometry'][objectName][0].setMass(t_m)
                self.physicsStore['geometry'][objectName].append(t_m)
    def loadODESettings(self):
        " loads settingfs from the ODE XML file "
        # load the ODE settings
        t_m = self.gameMVC.mvcStructure['config'] + '/'
        t_m += self.XPU.Parser['XML_Values']['Physics_Values']['odeXML']
        self.odeXPU = ConfigParser()
        self.odeXPU.parseFile(t_m)
        self.odeXPU.getSectionValues('section','Settings')
        # create ODE space and setup collision detection
        if self.odeXPU.Parser['XML_Values']['Settings_Values']['odeSpace'] == 0:
            self.odeSpace = OdeSimpleSpace()
        # TODO: Set arguments for the other two ODE spaces
        elif self.odeXPU.Parser['XML_Values']['Settings_Values']['odeSpace'] == 1:
            self.odeSpace = OdeQuadTreeSpace()
        elif self.odeXPU.Parser['XML_Values']['Settings_Values']['odeSpace'] == 2:
            self.odeSpace = OdeHashSpace()
        else:
            # load the default
            self.odeSpace = OdeSimpleSpace()
        # setup ODE terrain detection
        if self.odeXPU.Parser['XML_Values']['Settings_Values'] \
            ['enableTerrainDetection'] == True:
            # we only need one of these
            t_v = self.odeXPU.Parser['XML_Values']['Settings_Values']['planeVec4']
            t_vl = t_v.split(':')
            # convert to floating point
            for t_c in range(len(t_vl)):
                t_vl[t_c] = float(t_vl[t_c])
            t_gg = OdePlaneGeom(self.odeSpace, Vec4(t_vl[0], t_vl[1], t_vl[2], t_vl[3]))
            t_gg.setCollideBits(self.geometryNode.getCollideMask())
            t_gg.setCategoryBits(self.geometryNode.getCollideMask())
        self.odeSpace.setAutoCollideWorld(self.odeWorld)
        self.defContactGroup = OdeJointGroup()
        self.odeSpace.setAutoCollideJointGroup(self.defContactGroup)
        # The surface table is needed for autoCollide
        self.odeWorld.initSurfaceTable(self.odeXPU.Parser['XML_Values'] \
            ['Settings_Values']['surfaceCount'])
        t_s = self.odeXPU.Parser['XML_Values']['Settings_Values']['surfaceList']
        t_sl = t_s.split(':')
        for t_x in t_sl:
            self.odeXPU.getSectionValues('surface', t_x)
            # check the Coulomb friction coefficient for infinity
            if self.odeXPU.Parser['XML_Values']['%s_Values' % t_x]['CSF'] < 0:
                t_mu = OdeUtils.getInfinity()
            else:
                t_mu = self.odeXPU.Parser['XML_Values']['%s_Values' % t_x]['CSF']
            self.odeWorld.setSurfaceEntry(self.odeXPU.Parser['XML_Values'] \
                ['%s_Values' % t_x]['surfaceID1'], self.odeXPU.Parser['XML_Values'] \
                ['%s_Values' % t_x]['surfaceID2'], t_mu , self.odeXPU.Parser['XML_Values'] \
                ['%s_Values' % t_x]['bounce'], self.odeXPU.Parser['XML_Values'] \
                ['%s_Values' % t_x]['bounceVelocity'], self.odeXPU.Parser['XML_Values'] \
                ['%s_Values' % t_x]['softERP'], self.odeXPU.Parser['XML_Values'] \
                ['%s_Values' % t_x]['softCFM'], self.odeXPU.Parser['XML_Values'] \
                ['%s_Values' % t_x]['CDF'], self.odeXPU.Parser['XML_Values'] \
                ['%s_Values' % t_x]['dampingFactor'])
    def createODEMass(self, massType, massValue, odeMassData):
        " creates and returns an OdeMass object "
        # create the object
        t_am = OdeMass()
        if massType == 0:
            # massless object
            t_am.setZero()
        elif massType == 1:
            # spherical object
            if odeMassData['density'] == 0.0:
                # we use the argued total mass
                t_am.setSphereTotal(massValue, odeMassData['radius'])
            else:
                # use the density
                t_am.setSphere(odeMassData['density'], odeMassData['radius'])
                t_am.setMass(massValue)
        elif massType == 2:
            # box object
            if odeMassData['density'] == 0.0:
                # we use the argued total mass
                t_am.setBoxTotal(massValue, odeMassData['X'], odeMassData['Y'], \
                    odeMassData['Z'])
            else:
                # use the density
                t_am.setBox(odeMassData['density'], odeMassData['X'], \
                    odeMassData['Y'], odeMassData['Z'])
                t_am.setMass(massValue)
        elif massType == 3:
            # cylinder object
            if odeMassData['density'] == 0.0:
                # we use the argued total mass
                t_am.setCylinderTotal(massValue, odeMassData['direction'], \
                    odeMassData['r'], odeMassData['l'])
            else:
                # use the density
                t_am.setCylinder(odeMassData['density'], odeMassData['direction'], \
                    odeMassData['r'], odeMassData['l'])
                t_am.setMass(massValue)
        elif massType == 4:
            # capsule object
            if odeMassData['density'] == 0.0:
                # we use the argued total mass
                t_am.setCapsuleTotal(massValue, odeMassData['direction'], \
                    odeMassData['r'], odeMassData['l'])
            else:
                # use the density
                t_am.setCapsule(odeMassData['density'], odeMassData['direction'], \
                    odeMassData['r'], odeMassData['l'])
                t_am.setMass(massValue)
        return t_am
    def adjustODEMass(self, objectName, newMass):
        " modifies the mass value of an object in the ODE world "
        self.physicsStore['geometry'][objectName][1].adjust(newMass)
    def setGlobalGravity(self, gravityPull = 9.81):
        " apply gravity globally to the world; default is 9.81 ms^2 downward "
        # this will affect all physics-enabled objects
        # gravity doesn't care how much the model weighs
        # for ODE, we negate the gravityPull value first
        if self.worldData['enablePhysics'] != 1:
            # we don't have a prepared physics engine!
            return False
        else:
            if self.physicsEngine == self.enginesList[0]:
                # create the force (it has to be positie for this method)
                self.terrainDetector.setGravity(gravityPull)
            elif self.physicsEngine == self.enginesList[1]:
                # enable gravity on ODE world
                self.odeWorld.setGravity(0, 0, -gravityPull)
    def loadForcesfromXML(self, forceXML, procList = [None]):
        " loads force(s) from an XML file "
        # build a path to the XML
        t_xf = self.gameMVC.mvcStructure['config'] + '/forces/'
        # parse menu details XML (XPU = XML processing unit)
        self.forceXPU.parseFile(t_xf + forceXML)
        # get the forces list (the setting is a CSV)
        self.forceXPU.getSectionValues('section','forceList')
        t_ll = self.forceXPU.Parser['XML_Values']['forceList_Values']['forces']
        t_l = t_ll.split(',')
        for t_x in t_l:
            # parse settings
            self.forceXPU.getSectionValues('force', t_x)
            t_k = t_x + '_Values'
            # get the force information
            t_n = self.forceXPU.Parser['XML_Values'][t_k]['name']
            if self.forceXPU.Parser['XML_Values'][t_k]['isGlobal'] == 0:
                t_g = False
            else:
                t_g = True
            t_t = self.forceXPU.Parser['XML_Values'][t_k]['forceType']
            t_xyz = (self.forceXPU.Parser['XML_Values'][t_k]['forceX'], \
                self.forceXPU.Parser['XML_Values'][t_k]['forceY'],
                self.forceXPU.Parser['XML_Values'][t_k]['forceZ'])
            if len(self.forceXPU.Parser['XML_Values'][t_k]) > 5:
                # copy the dictionary for the extra args
                t_ea = self.forceXPU.Parser['XML_Values'][t_k]
            else:
                t_ea = {}
            if t_t == 9:
                # set the function argument
                t_ea['UDFF'] = procList[self.forceXPU.Parser['XML_Values'] \
                    [t_k]['UDFF']]
            # create the force
            self.createForce(t_n, t_t, t_xyz, t_ea, t_g)
    def createForce(self, forceName, forceType, forceXYZ, uniqueArgs = {}, \
        setGlobal = False):
        " creates a new force and stores in the force store "
        # forceXYZ is in Newtons
        # TODO: Investigate makeCopy()
        # create the force
        if forceType == 1:
            # linear vector force - simple directed vector force
            t_f = LinearVectorForce(forceXYZ[0], forceXYZ[1], forceXYZ[2])
            # set mass dependence (only linear forces)
            t_f.setMassDependent(uniqueArgs['massDependence'])
        elif forceType == 2:
            # angular vector force - simple directed torque force
            t_f = AngularVectorForce(forceXYZ[0], forceXYZ[1], forceXYZ[2])
        elif forceType == 3:
            # linear jitter force - a descendant of linear random force
            t_f = LinearJitterForce(forceXYZ[0], forceXYZ[1], forceXYZ[2])
            # set mass dependence (only linear forces)
            t_f.setMassDependent(uniqueArgs['massDependence'])
        elif forceType == 4:
            # linear noise force - a descendant of linear random force
            # repeating noise force vector
            t_f = LinearNoiseForce(forceXYZ[0], forceXYZ[1], forceXYZ[2])
            # set mass dependence (only linear forces)
            t_f.setMassDependent(uniqueArgs['massDependence'])
        elif forceType == 5:
            # linear sink force - attractor force (black hole)
            t_f = LinearSinkForce(forceXYZ[0], forceXYZ[1], forceXYZ[2])
            # set mass dependence (only linear forces)
            t_f.setMassDependent(uniqueArgs['massDependence'])
            # set force center (only linear distance forces)
            t_fc = uniqueArgs['forceCenter']
            t_f.setForceCenter(t_fc[0], t_fc[1], t_fc[2])
            # set force radius (only linear distance forces)
            t_f.setRadius(uniqueArgs['forceRadius'])
            # set fall off type (only linear distance forces)
            if uniqueArgs['fallOffType'] == 0:
                t_ft = t_f.FTONEOVERR
            elif uniqueArgs['fallOffType'] == 1:
                t_ft = t_f.FTONEOVERRSQUARED
            else:
                t_ft = t_f.FTONEOVERRCUBED
            t_f.setFalloffType(t_ft)
        elif forceType == 6:
            # linear source force - repellant force
            t_f = LinearSourceForce(forceXYZ[0], forceXYZ[1], forceXYZ[2])
            # set mass dependence (only linear forces)
            t_f.setMassDependent(uniqueArgs['massDependence'])
            # set force center (only linear distance forces)
            t_fc = uniqueArgs['forceCenter']
            t_f.setForceCenter(t_fc[0], t_fc[1], t_fc[2])
            # set force radius (only linear distance forces)
            t_f.setRadius(uniqueArgs['forceRadius'])
            # set fall off type (only linear distance forces)
            if uniqueArgs['fallOffType'] == 0:
                t_ft = t_f.FTONEOVERR
            elif uniqueArgs['fallOffType'] == 1:
                t_ft = t_f.FTONEOVERRSQUARED
            else:
                t_ft = t_f.FTONEOVERRCUBED
            t_f.setFalloffType(t_ft)
        elif forceType == 7:
            # linear friction force - frictional drag force
            t_f = LinearFrictionForce(forceXYZ[0], forceXYZ[1], forceXYZ[2])
            # set mass dependence (only linear forces)
            t_f.setMassDependent(uniqueArgs['massDependence'])
            # set coefficient of friction (float value)
            t_f.setCoef(uniqueArgs['frictionCoefficient'])
        elif forceType == 8:
            # linear control force - can be global yet affect only one object
            # handy for games where the player applies a force on one object
            # has a setPhysicsObject method and a setVector method
            t_f = LinearControlForce(forceXYZ[0], forceXYZ[1], forceXYZ[2])
            # set mass dependence (only linear forces)
            t_f.setMassDependent(uniqueArgs['massDependence'])
        elif forceType == 9:
            # linear user defined force
            t_f = LinearUserDefinedForce(forceXYZ[0], forceXYZ[1], forceXYZ[2])
            # set mass dependence (only linear forces)
            t_f.setMassDependent(uniqueArgs['massDependence'])
            # set evaluator function (UDFF - User-Defined Force Function)
            t_f.setProc(uniqueArgs['UDFF'])
        elif forceType == 10:
            # linear cylinder vortex force - defines a cylinder inside of which
            # all forces are tangential to the theta of the particle wrt the z-axis
            # in local coordinate space
            # this will suck anything that it can reach directly into orbit and
            # will NOT let go
            t_f = LinearCylinderVortexForce(forceXYZ[0], forceXYZ[1], forceXYZ[2])
            # set mass dependence (only linear forces)
            t_f.setMassDependent(uniqueArgs['massDependence'])
            # set cylinder length
            t_f.setLength(uniqueArgs['cylinderLength'])
            # set cylinder radius
            t_f.setRadius(uniqueArgs['cylinderRadius'])
            # set coefficient (float value)
            t_f.setCoef(uniqueArgs['coefficient'])
        else:
            # default
            t_f = LinearVectorForce(forceXYZ[0], forceXYZ[1], forceXYZ[2])
            # set mass dependence (only linear forces)
            t_f.setMassDependent(uniqueArgs['massDependence'])
        # we store the force raw (force, forceType)
        if setGlobal == False:
            self.physicsStore['forces'][forceName] = (t_f, forceType)
        else:
            self.physicsStore['forces'][self.GFP + forceName] = (t_f, forceType)
            self.physicsStore['globalForces'].append(forceName)
            # attach it to all objects loaded for physics so far
            for t_x in self.physicsStore['geometry'].keys():
                self.attachForceToObject(t_x, self.GFP + forceName)
            # send a message that we added a new global force; we'll catch it
            # in Genesis to apply this to actors. accept parameters are passed
            # LAST!
            messenger.send('Eden: Global Force Created', [forceName])
    # -----------------CONVENIENCE FUNCTIONS FOR createForce----------------
    def createGlobalForce(self, forceName, forceType, forceXYZ, uniqueArgs = {}):
        " creates a new global force and stores in the global force store "
        # create the force
        self.createForce(forceName, forceType, forceXYZ, uniqueArgs, True)
    def createLinearVectorForce(self, forceName, forceXYZ, massDependence, \
        setGlobal):
        " creates a new LVF; developer convenience front for createForce "
        # create the force
        self.createForce(forceName, 1, forceXYZ, \
            {'massDependence':massDependence}, setGlobal)
    def createAngularVectorForce(self, forceName, forceXYZ, setGlobal):
        " creates a new AVF; developer convenience front for createForce "
        # create the force
        self.createForce(forceName, 2, forceXYZ, {}, setGlobal)
    def createUniversalForce(self, forceName):
        " applies an existing force universally; just under render "
        if self.worldData['enablePhysics'] != 1:
            # we don't have a prepared physics engine!
            return False
        elif forceName not in self.physicsStore['forces'].keys():
            # the specified force does not exist
            return False
        else:
            self.universalFN.addForce(self.physicsStore['forces'][forceName][0])
            if self.physicsStore['forces'][forceName][1] != 2:
                # a linear force
                self.physicsManager.addLinearForce(self.physicsStore['forces'] \
                    [forceName][0])
            else:
                # an angular force
                self.physicsManager.addAngularForce(self.physicsStore['forces'] \
                    [forceName][0])
    def attachForceToObject(self, objectName, forceName):
        " attaches an existing force to an object "
        if objectName not in self.objectStore.keys():
            # the specified object does not exist in the world
            return False
        elif forceName not in self.physicsStore['forces'].keys():
            # the specified force does not exist
            return False
        elif self.objectStore[objectName][3] == False:
            # physics is not enabled
            return False
        else:
            # create a force node
            t_fn = ForceNode(objectName + forceName)
            # attach the force node to the object
            self.objectStore[objectName].attachNewNode(t_fn)
            # add the force to the force node
            t_fn.addForce(self.physicsStore['forces'][forceName][0])
            # add the force (for now we only have one rotational force)
            if self.physicsStore['forces'][forceName][1] != 2:
                # a linear force
                self.physicsStore['geometry'][objectName] \
                    [1].getPhysical(0).addLinearForce(self.physicsStore['forces'] \
                    [forceName][0])
            else:
                # an angular force
                self.physicsStore['geometry'][objectName] \
                    [1].getPhysical(0).addAngularForce(self.physicsStore['forces'] \
                    [forceName][0])
    def removeForceFromObject(self, objectName, forceName):
        " removes an existing force from an object "
        if objectName not in self.objectStore.keys():
            # the specified object does not exist in the world
            return False
        elif forceName not in self.physicsStore['forces'].keys():
            # the specified force does not exist
            return False
        elif self.objectStore[objectName][3] == False:
            # physics is not enabled
            return False
        else:
            # remove the force (for now we only have one rotational force)
            if self.physicsStore['forces'][forceName][1] != 2:
                # a linear force
                self.physicsStore['geometry'][objectName] \
                    [1].getPhysical(0).removeLinearForce(self.physicsStore['forces'] \
                    [forceName][0])
            else:
                # an angular force
                self.physicsStore['geometry'][objectName] \
                    [1].getPhysical(0).removeAngularForce(self.physicsStore['forces'] \
                    [forceName][0])
    def createJetPack(self, forceName, jetPackName):
        " creates a node with a force attached to it "
        # this can be a jet engine, car engine or whatever. It is
        # not for jet packs only
        if forceName not in self.physicsStore['forces'].keys():
            # the specified force does not exist
            return False
        else:
            # create the node
            t_jp = NodePath(jetPackName)
            # create a force node
            t_fn = ForceNode(jetPackName + forceName)
            # get the force node path
            t_fnp = t_jp.attachNewNode(t_fn)
            # add the force
            t_fn.addForce(self.physicsStore['forces'][forceName][0])
            # return the jetPack node path
            # the client will just have to call:
            # actorNode.getPhysical(0).add<L/A>Force(self.physicsStore['forces']
            #   [forceName][0])
            # with the returned node path we can set the jetpack position once it
            # is parented, and set its HPR
            return t_jp
    def attachJetPackToObject(self, forceName, jetPack, objectName, \
        packPos = (0,0,0), packHpr = None):
        " convenience function for attaching jetpacks to objects "
        if objectName not in self.objectStore.keys():
            # the specified object does not exist in the world
            return False
        elif forceName not in self.physicsStore['forces'].keys():
            # the specified force does not exist
            return False
        elif self.objectStore[objectName][3] == False:
            # physics is not enabled
            return False
        else:
            # reparent the jetpack
            jetPack.reparentTo(self.objectStore[objectName][0])
            # set a tag to show it exists
            self.objectStore[objectName][0].setTag(jetPack.getName(), 'active')
            # set position and orientation on parent
            jetPack.setPos(packPos[0], packPos[1], packPos[2])
            if packHpr == None:
                # set the HPR to match the parent
                jetPack.setHpr(self.objectStore[objectName][0].getH(), \
                    self.objectStore[objectName][0].getP(), \
                    self.objectStore[objectName][0].getR())
            else:
                # set custom HPR
                jetPack.setHpr(packHpr[0], packHpr[1], packHpr[2])
            # add the force (for now we only have one rotational force)
            if self.physicsStore['forces'][forceName][1] != 2:
                # a linear force
                self.physicsStore['geometry'][objectName] \
                    [1].getPhysical(0).addLinearForce(self.physicsStore['forces'] \
                    [forceName][0])
            else:
                # an angular force
                self.physicsStore['geometry'][objectName] \
                    [1].getPhysical(0).addAngularForce(self.physicsStore['forces'] \
                    [forceName][0])
    def removeJetPackFromObject(self, forceName, jetPackName, objectName):
        " convenience function for removing jetpacks from objects "
        if objectName not in self.objectStore.keys():
            # the specified object does not exist in the world
            return False
        elif forceName not in self.physicsStore['forces'].keys():
            # the specified force does not exist
            return False
        elif self.objectStore[objectName][3] == False:
            # physics is not enabled
            return False
        else:
            # check if the jetPack is on the object
            t_f = self.objectStore[objectName][0].findNetTag(jetPackName)
            if not t_f.isEmpty():
                # check whether the pack is active
                t_av = self.objectStore[objectName][0].getTag(jetPackName)
                if t_av == 'active':
                    # find the jetpack node
                    t_jo = self.objectStore[objectName][0].find(jetPackName)
                    # remove the jetpack
                    t_jo.removeNode()
                    # remove the force
                    if self.physicsStore['forces'][forceName][1] != 2:
                        # a linear force
                        self.physicsStore['geometry'][objectName] \
                            [1].getPhysical(0).removeLinearForce(self.physicsStore['forces'] \
                            [forceName][0])
                    else:
                        # an angular force
                        self.physicsStore['geometry'][objectName] \
                            [1].getPhysical(0).removeAngularForce(self.physicsStore['forces'] \
                            [forceName][0])
                    # remove the tag
                    self.objectStore[objectName][0].setTag(jetPackName, 'removed')
                else:
                    # the pack does not exist (was removed)
                    return False
            else:
                # no jet pack
                return False
    # -----------------------------------------------------------------------
    # --------------------------CURSOR MANIPULATION--------------------------
    def toggleMouseCursor(self):
        " hides/shows the mouse cursor "
        if self.winHandle[1] == False:
            # hide the cursor
            self.winHandle[0].setCursorHidden(True) 
            base.win.requestProperties(self.winHandle[0])
            self.winHandle[1] = True
        else:
            # show the cursor
            self.winHandle[0].setCursorHidden(False) 
            base.win.requestProperties(self.winHandle[0])
            self.winHandle[1] = False
    # ------------------CAMERA SERVICES-----------------
    # ----------------------------------------------------
    def spinCamera(self, spinFactor):
        " sets the camera spin task "
        if self.spinFlag == False:
            # set the variables
            self.spinFlag = True
            self.spinFactor = spinFactor
            taskMgr.add(self.spinCameraTask, "SpinCameraTask")
    def stopCameraSpin(self):
        " convenience function "
        # set the variables
        self.spinFlag = False
    def toggleOOBE(self):
        " enables/disables out-of-body experience "
        if self.oobeFlag == False:
            self.oobeFlag = True
        else:
            self.oobeFlag = False
        base.oobe()
    def getPointBelowCursor(self, zValue, cursorPoint, cursorVec):
        " mathematical utility function for object moving "
        # zValue is the z co-ordinate of the plane below the cursor
        return cursorPoint + cursorVec * ((zValue - cursorPoint.getZ()) / cursorVec.getZ())
    # ------------------SYSTEM SERVICES-----------------
    # ----------------------------------------------------
    def checkMVC(self, mvcRootDir):
        " checks validity of the MVC root "
        # create the MVC instance for Creation
        self.gameMVC = MVC_System(mvcRootDir)
        # check validity of structure
        if self.gameMVC.fullMVC == False:
            print 'The game MVC structure is incomplete'
            if len(self.gameMVC.mvcStructure['Missing_Folders']) != 0:
                print 'The components missing are:\n', \
                self.gameMVC.mvcStructure['Missing_Folders']
            if len(self.gameMVC.mvcStructure['Missing_Files']) != 0:
                print 'The vital files missing are:\n', \
                self.gameMVC.mvcStructure['Missing_Files']
            print 'For more information read the Eden documentation\n'
            # quit
            sys.exit(1)
        else:
            # A valid game directory was found.
            # parse config.xml
            self.XPU = ConfigParser()
            # isolated the parsing of config.xml to allow setting of some
            # different file
            self.parseConfigXML(self.gameMVC.mvcStructure['config.xml'])
    def parseConfigXML(self, configXML):
        " parse the main configuration file "
        # parse the configuration (XPU = XML processing unit)
        self.XPU.parseFile(configXML)
        # get about information
        self.XPU.getSectionValues('section','About')
        # get world information for loading
        self.XPU.getSectionValues('subsection','WorldDetails')
        # -------------------------- ID DATA ACQUISITION-----------------------
        # store the game ID
        self.gameID = ''
        t_g = self.XPU.Parser['XML_Values']['About_Values']['displayOrder']
        t_g = t_g.split(',')
        for t_y in t_g:
            t_x = t_y + ' : ' + self.XPU.Parser['XML_Values']['About_Values'] \
            [t_y] + '\n'
            self.gameID += t_x
        # add the renderer
        t_x = 'Rendering Framework : ' + self.systemInfo.systemData['renderer'] \
            + '\n'
        self.gameID += t_x
        # ------------------------------------------------------------------
        # check whether the world model is an actual model or needs to be
        # generated
        if self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['worldType'] == 0:
            # save the world path
            t_m = self.gameMVC.mvcStructure['tier_models']['geometry'] + '/'
            t_m += self.XPU.Parser['XML_Values']['WorldDetails_Values']['world']
            self.worldData['worldPath'] = t_m
            self.worldData['isGenerated'] = False
        else:
            # get the data for the terrain
            t_m = self.gameMVC.mvcStructure['config'] + '/'
            t_m += self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
                ['terrainData']
            self.worldData['worldPath'] = t_m
            self.worldData['isGenerated'] = True
        # get the world scaling
        self.worldData['worldScale'] = (self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['scaleX'], self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['scaleY'], self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['scaleZ'])
        # get the world initial position
        self.worldData['worldPosition'] = (self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['posX'], self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['posY'], self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['posZ'])
        # save the default FPS
        self.worldData['defaultFPS'] = self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['defaultFPS']
        # saves the physics option
        self.worldData['enablePhysics'] = self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['enablePhysics']
        # save mouse cursor visibility
        self.worldData['showMouse'] = self.XPU.Parser['XML_Values'] \
            ['WorldDetails_Values']['showMouse']
        if self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['cameraDefaults'] != 1:
            # get camera initialization data
            self.XPU.getSectionValues('subsection','Camera')
            if self.XPU.Parser['XML_Values']['Camera_Values'] \
                ['cameraTrait'] == 'FIXED':
                # save the camera data
                self.worldData['cameraPos'] = (self.XPU.Parser['XML_Values'] \
                    ['Camera_Values']['cameraX'], self.XPU.Parser['XML_Values'] \
                    ['Camera_Values']['cameraY'], self.XPU.Parser['XML_Values'] \
                    ['Camera_Values']['cameraZ'])
                self.worldData['cameraHpr'] = (self.XPU.Parser['XML_Values'] \
                    ['Camera_Values']['cameraH'], self.XPU.Parser['XML_Values'] \
                    ['Camera_Values']['cameraP'], self.XPU.Parser['XML_Values'] \
                    ['Camera_Values']['cameraR'])
                self.camfixFlag = True
        else:
            # we use camera defaults but still fix the camera
            self.lockMouse = True
        # ---------------------VISUALS AND SOUND------------------
        # we need Visuals2D even where no visuals are present; for screenshots
        # and video. Visuals2D needs a handle to messenger.send() for alerts
        self.edenVisuals = Visuals2D(messenger.send, self.worldData['defaultFPS'], \
                self.systemInfo.systemData['screenResolution'])
        # check startup visuals status and load if necessary
        if self.XPU.Parser['XML_Values']['WorldDetails_Values']['visualsCount'] == 0:
            # no visuals to display on startup
            pass
        else:
            # get visuals data for loading (isolated visuals loading to allow
            # loading of visuals from some other section)
            self.loadStartupVisuals('subsection','Visuals')
        # check startup sound status and load if necessary
        if self.XPU.Parser['XML_Values']['WorldDetails_Values']['playSound'] == 0:
            # no sound to play
            pass
        else:
            # get sound data for loading (isolated sound loading to allow
            # loading of sound from some other section)
            self.loadStartupSound('subsection','Sound')
        # indicate that the MVC structure was valid
        self.validMVC = True
    def loadStartupVisuals(self, tagID, tagValue):
        " loads startup visuals from the specified section "
        self.XPU.getSectionValues(tagID, tagValue)
        t_p = tagValue + '_Values'
        # load the visuals
        t_u = self.XPU.Parser['XML_Values'][t_p].keys()[:]
        t_u.sort()
        for t_j in t_u:
            t_a = t_j.split('_')
            if t_a[0] == 'screen':
                # build a path for the image
                t_m = self.gameMVC.mvcStructure['tier_resource']['images'] + '/'
                t_r = self.XPU.Parser['XML_Values'][t_p] \
                    [t_j].split(':')
                t_m += t_r[0]
                # get the position
                t_pos = (float(t_r[1]),float(t_r[2]),float(t_r[3]))
                # load the image
                self.edenVisuals.loadImage(t_m, t_pos)
            elif t_a[0] == 'video':
                # build a path for the video
                t_m = self.gameMVC.mvcStructure['tier_resource']['video'] + '/'
                t_r = self.XPU.Parser['XML_Values'][t_p] \
                    [t_j].split(':')
                t_m += t_r[0]
                # get the position
                t_pos = (float(t_r[1]),float(t_r[2]),float(t_r[3]))
                # load the video
                self.edenVisuals.loadVideo(t_m, t_pos)
        # enable alpha
        self.edenVisuals.enableAlpha()
        # store the delay
        self.visualDelay = self.XPU.Parser['XML_Values'][t_p] \
        ['interval']
        self.mediaFlag[0] = 1
    def loadStartupSound(self, tagID, tagValue):
        " loads startup sound from the specified section "
        self.XPU.getSectionValues(tagID, tagValue)
        t_p = tagValue + '_Values'
        # build a path for the sound
        t_m = self.gameMVC.mvcStructure['tier_sound']['music'] + '/'
        t_r = self.XPU.Parser['XML_Values'][t_p]['music'].split(':')
        t_m += t_r[0]
        # get the volume
        t_vol = float(t_r[1])
        # load the sound
        self.gameMusic = loader.loadSfx(t_m)
        self.gameMusic.setVolume(t_vol)
        self.worldData['playAfter'] = self.XPU.Parser['XML_Values'] \
        [t_p]['follows']
        self.mediaFlag[1] = 1
    def dummyCallBack(self, dummyArg = 0):
        " a dummy callback function for debugging menus & HUDs "
        # this function does nothing!    
        pass
    # ------------------TASKS-----------------------------
    # ----------------------------------------------------
    def defStarterTask(self, task):
        " task to handle the startup "
        if task.time == 0.0:
            # if sound is at startup then play
            if self.mediaFlag[1] == True and self.worldData['playAfter'] == 0:
                self.gameMusic.setLoop(True)
                self.gameMusic.play()
            if self.mediaFlag[0] == True:
                # show the screens with the n-second delay
                self.edenVisuals.sequenceAllImages(self.visualDelay)
            return task.cont
        else:
            if self.edenVisuals.virginFlag == True:
                # visuals are done
                messenger.send('startup-done')
                return task.done
            else:
                # all other frames
                return task.cont
    def terrainTask(self, task):
        " task to run the terrain traverser "
        if self.terraDetection != True:
            # no terrain detections have been enabled
            return task.cont
        else:
            # some object is detecting terrain; traverse the world node only
            self.terraTrav.traverse(self.worldNode)
            return task.cont
    def updatePhysics(self, task):
        " updates the global Creation physics manager, not the base one "
        # run the physics manager
        t_tm = globalClock.getDt()
        self.extraPhysicsManager.doPhysics(t_tm)
    def worldClockTask(self, task):
        " task to update the global time values "
        # get the time both UTC and local, the returned tuple is of the form:
        # ----------------------------------------------
        #   Index   -   Value
        #   0       -   Year
        #   1       -   Month
        #   2       -   DayOfMonth
        #   3       -   Hour
        #   4       -   Minute
        #   5       -   Second
        #   6       -   DayOfWeek (Monday is 0)
        #   7       -   DayOfYear (upto 366)
        # ----------------------------------------------
        if task.time == 0.0:
            # we get the initial values of the time
            t_ist = long(time())
            t_utc = gmtime(t_ist)
            t_lcl = localtime(t_ist)
            self.clockInitTime = [t_lcl, t_utc]
        if (task.frame % self.edenVisuals.fpsValue) == 0:
            # run every second
            t_ist = long(time())
            t_utc = gmtime(t_ist)
            t_lcl = localtime(t_ist)
            self.worldData['systemTime'] = [t_lcl, t_utc]
            # compute the strings
            # local
            self.worldData['localTime'] = strftime("%H:%M:%S", \
                t_lcl)
            # UTC
            self.worldData['zuluTime'] = strftime("%H:%M:%S", \
                t_utc)
        return task.cont
    def spinCameraTask(self, task):
        " task to spin camera - rotate world "
        if self.spinFlag == True:
            angledegrees = task.time * self.spinFactor
            angleradians = angledegrees * (math.pi / 180.0)
            # do not disturb camera height
            base.camera.setX(base.camera.getX() * math.sin(angleradians))
            base.camera.setY(base.camera.getY() * math.cos(angleradians))
            base.camera.setH(angledegrees)
            return task.cont
        else:
            return task.done
    def odeSimulationTask(self, task):
        " task to simulate physics using ODE "
        # Add the deltaTime for the task to the accumulator
        self.OdeDta += globalClock.getDt()
        while self.OdeDta > self.odeStepSize:
          # Remove a stepSize from the accumulator until
          # the accumulated time is less than the stepsize
          self.OdeDta -= self.odeStepSize
          # call autocollide to setup contact joints
          self.odeSpace.autoCollide()
          # Step the simulation
          self.odeWorld.quickStep(self.odeStepSize)
        # set the new positions for all objects
        for t_x in self.physicsStore['geometry'].keys():
            self.objectStore[t_x][0].setPosQuat(render, self.physicsStore['geometry'] \
                [t_x][0].getPosition(), Quat(self.physicsStore['geometry'][t_x] \
                [0].getQuaternion()))
        # empty the contact joints
        self.defContactGroup.empty()
        return task.cont

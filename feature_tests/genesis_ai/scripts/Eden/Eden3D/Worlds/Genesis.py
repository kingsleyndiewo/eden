# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Worlds]
# Desc: Worlds Library - Genesis Class
# File name: Genesis.py
# Developed by: Project Eden Development Team
# Date: 04/07/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench PLC
# ---------------------------------------------
from Eden.Eden3D.Worlds.Creation import *
from Eden.Eden3D.Actors.EdenWalker import EdenWalker
from Eden.Eden3D.Actors.EdenAero import EdenAero
# ---------------------------------------------
# A class that implements a basic world with options
# for loading actors and collision detection. Entry
# point for a full 3D game.
# Startup options are loaded from config.xml
# Class definition for the Genesis class
# ---------------------------------------------
class Genesis(Creation):
    " Extends Creation class for practical 3D worlds "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, remoteStarterTask = None, customPRC = None, edenClass = 'Genesis', initAI = False):
        Creation.__init__(self, remoteStarterTask, customPRC, edenClass, initAI) # ancestral constructor
        # set the bitMask for the geometry
        self.geomBitMask = self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['collisionBM']
        self.geometryNode.setCollideMask(BitMask32.bit(self.geomBitMask))
        # save handler type
        self.handlerType = self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['collisionHandler']
        # create a collision handler based on the config setting
        if self.handlerType == 0:
            # default is a CollisionHandlerPusher
            self.edenColHandler = CollisionHandlerPusher()
        elif self.handlerType == 1:
            # the manual CollisionHandlerEvent
            self.edenColHandler = CollisionHandlerEvent()
        elif self.handlerType == 2:
            # the advanced PhysicsCollisionHandler
            # the actor must be a physics ActorNode!
            self.edenColHandler = PhysicsCollisionHandler()
            # store the parameters
            t_dfc = self.edenColHandler.getDynamicFrictionCoef()
            t_sfc = self.edenColHandler.getStaticFrictionCoef()
            t_ass = self.edenColHandler.getAlmostStationarySpeed()
            self.pchData = {'DFC':t_dfc, 'SFC':t_sfc, 'ASS':t_ass}
        else:
            # default
            self.edenColHandler = CollisionHandlerPusher()
        # add notifiers for the collision event
        # in is for initial collision
        # out is for end of collision
        # again is for sustained collision
        self.edenColHandler.addInPattern('%fn-into-%in')
        self.edenColHandler.addAgainPattern('%fn-again-%in')
        self.edenColHandler.addOutPattern('%fn-out-%in')
        # we create a single, global collision traverser for the world
        self.edenTraverser = CollisionTraverser('edenTraverser')
        base.cTrav = self.edenTraverser
        # enable fluid collision detection for fast-moving objects
        base.cTrav.setRespectPrevTransform(True)
        # a dictionary for loaded actors
        self.actorStore = {}
        # a dictionary for inventories
        self.toolBox = {}
        self.toolBoxLists = {}
        # for Adam and Eve
        if self.worldData['edenClass'] in ['Adam', 'Eve']:
            # initialize variables
            self.modifiers = {}
            self.walkerArgs = None
            self.prevTime = 0.0
            self.controller = {}
            # setup key mappings
            self.keyboardSetup()
            # add the mainActor movement task to the task manager
            taskMgr.add(self.MoverTask, 'MoveTask')
        # accept global force creation message
        self.accept('Eden: Global Force Created', self.updateActorsGFs, [])
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    # --------------------------COLLISION DETECTION-----------------------------
    def setupActorCollision(self, actorName):
        " sets up collision detection for an actor "
        if actorName not in self.actorStore.keys():
            # the specified actor does not exist in the world
            return False
        # setup sphere collision on the actorObject
        t_c = self.actorStore[actorName].actorData['collider']
        self.actorStore[actorName].setupCollider(self.geomBitMask, t_c)
        if self.handlerType == 0:
            # add to the collision handler if it is a CollisionHandlerPusher
            self.edenColHandler.addCollider(self.actorStore[actorName].actorCnode, \
                self.actorStore[actorName].baseActor)
        elif self.handlerType == 2:
            # add the actorNode to the collision handler if it is a
            # PhysicsCollisionHandler
            self.edenColHandler.addCollider(self.actorStore[actorName].actorCnode, \
                self.physicsStore['actors'][actorName][0])
        if t_c != 1:
            # we add our collider and handler to it
            self.edenTraverser.addCollider(self.actorStore[actorName].actorCnode, \
                self.edenColHandler)
    def setupObjectCollision(self, objectName):
        " sets up collision for a geometry object "
        # I had to make this just for EdenMaze
        # removes the shaking bug of the pusher from cube-like objects
        if objectName not in self.objectStore.keys():
            # the specified object does not exist in the world
            return False
        else:
            # setup sphere collision on the object
            # we create a new collision node
            t_Cnode = CollisionNode(objectName)
            # we create a new collision sphere to fit the object
            t_s = CollisionSphere(self.objectStore[objectName][2]['center'], \
                self.objectStore[objectName][2]['weightedRadius'])
            # then give the cnode something to hold - the sphere
            t_Cnode.addSolid(t_s)
            # we get the node path of the cnode, now parented to actorObject
            self.objectStore[objectName][2]['colNode'] = \
                self.objectStore[objectName][0].attachNewNode(t_Cnode)
            # all objects have collider type 1
            self.objectStore[objectName][2] \
                ['colNode'].node().setFromCollideMask(BitMask32.allOff())
            self.objectStore[objectName][2] \
                ['colNode'].setCollideMask(BitMask32.bit(self.geomBitMask))
    def updatePCH(self):
        " updates the physics collision handler with modified values "
        if self.handlerType != 2:
            # not a PCH
            return False
        else:
            # update values
            # dynamic friction coefficient
            self.edenColHandler.setDynamicFrictionCoef(self.pchData['DFC'])
            # static friction coefficient
            self.edenColHandler.setStaticFrictionCoef(self.pchData['SFC'])
            # almost-stationary speed
            self.edenColHandler.setAlmostStationarySpeed(self.pchData['ASS'])
    # --------------------------PANDA AI BEHAVIORS---------------------------
    def createAiCharacter(self, charName, charNP, charMass, moveForce, maxForce):
        " creates an AI character and attaches to AI node "
        if self.aiReady == False:
            return None
        else:
            # create character
            aiChar = AICharacter(charName, charNP, charMass, moveForce, maxForce)
            # add to AI node
            self.smartEden.addAiChar(aiChar)
            # get behaviors
            aiBehaviors = aiChar.getAiBehaviors()
            # return object
            return (aiChar, aiBehaviors)
    # --------------------------RESOURCE LOADING-----------------------------
    def loadInventory(self, invFile, inventoryName):
        " loads an object inventory to the main store "
        # inventory objects are different from ordinary geometry because
        # they will not exist in the objectStore. You cannot therefore use
        # the visibility methods of Creation on them.
        # create a dictionary
        self.toolBox[inventoryName] = {}
        # build a pathname to the file
        t_g = self.gameMVC.mvcStructure['config'] + '/'
        t_g += invFile
        # parse inventory details XML
        invXPU = ConfigParser()
        # parse the configuration (XPU = XML processing unit)
        invXPU.parseFile(t_g)
        # get inventory item names information
        invXPU.getSectionValues('subsection','Names')
        invXPU.getSectionValues('subsection','Initial')
        # get the list of items
        t_l = invXPU.Parser['XML_Values']['Names_Values'].values()
        for t_y in t_l:
            # get the item's section
            invXPU.getSectionValues('itemsection', t_y)
            # get model name and load
            t_q = '%s_Values' % t_y
            t_mo = invXPU.Parser['XML_Values'][t_q]['model']
            # build path
            t_mod = self.gameMVC.mvcStructure['tier_models']['geometry'] + '/' + t_mo
            t_model = loader.loadModel(t_mod)
            # get scale values and set
            t_scl = (invXPU.Parser['XML_Values'][t_q]['scaleX'], \
                invXPU.Parser['XML_Values'][t_q]['scaleY'], \
                invXPU.Parser['XML_Values'][t_q]['scaleZ'])
            t_model.setScale(t_scl[0], t_scl[1], t_scl[2])
            # get XYZ position values and set
            t_pos = (invXPU.Parser['XML_Values'][t_q]['posX'], \
                invXPU.Parser['XML_Values'][t_q]['posY'], \
                invXPU.Parser['XML_Values'][t_q]['posZ'])
            t_model.setPos(t_pos[0], t_pos[1], t_pos[2])
            # get HPR values and set
            t_hpr = (invXPU.Parser['XML_Values'][t_q]['itemH'], \
                invXPU.Parser['XML_Values'][t_q]['itemP'], \
                invXPU.Parser['XML_Values'][t_q]['itemR'])
            t_model.setHpr(t_hpr[0], t_hpr[1], t_hpr[2])
            # store the model
            self.toolBox[inventoryName][t_y] = t_model
        # we save the list as a convenience
        self.toolBoxLists[inventoryName] = t_l
        # the client will parent the item independently so no need for
        # any action on Eden's part
        # hide all except the item initially visible
        t_j = invXPU.Parser['XML_Values']['Initial_Values']['initVisible']
        if t_j != 'None':
            self.selectInventoryItem(inventoryName, t_j)
    def loadActor(self, actorDetailsFile, overrideName = None):
        " loads a new actor with details in <actorname>.xml "
        # build a pathname to the file
        t_j = self.gameMVC.mvcStructure['config'] + '/'
        t_j += actorDetailsFile
        # parse actor details XML
        actorXPU = ConfigParser()
        # parse the configuration (XPU = XML processing unit)
        actorXPU.parseFile(t_j)
        # get actor information
        actorXPU.getSectionValues('subsection','Main')
        actorXPU.getSectionValues('subsection','Animations')
        actorXPU.getSectionValues('section','Setup')
        # we will build a dictionary
        actorDetails = {}
        # prepare a list of not-so-common keys that might be needed
        t_ncl = ['runSpeed','swimSpeed','strollSpeed','flySpeed']
        # build the pathname to the model
        t_p = self.gameMVC.mvcStructure['tier_models']['actors'] + '/'
        t_p += actorXPU.Parser['XML_Values']['Main_Values']['model']
        actorDetails['actor'] = t_p
        # save the actor scale, sphereFactor, collider info and name
        actorDetails['scale'] = (actorXPU.Parser['XML_Values']['Main_Values'] \
            ['scaleX'], actorXPU.Parser['XML_Values']['Main_Values']['scaleY'], \
            actorXPU.Parser['XML_Values']['Main_Values']['scaleZ'])
        actorDetails['sphereFactor'] = actorXPU.Parser['XML_Values']['Main_Values'] \
            ['sphereFactor']
        actorDetails['collider'] = actorXPU.Parser['XML_Values']['Setup_Values'] \
            ['collider']
        if overrideName == None:
            actorDetails['name'] = actorXPU.Parser['XML_Values']['Main_Values']['name']
        else:
            actorDetails['name'] = overrideName
        # save the animations
        actorDetails['animations'] = {}
        for t_i in actorXPU.Parser['XML_Values']['Animations_Values'].keys():
            # build the pathname to the animation
            t_b = self.gameMVC.mvcStructure['tier_models']['actors'] + '/animations/'
            t_b += actorXPU.Parser['XML_Values']['Animations_Values'][t_i]
            actorDetails['animations'][t_i] = t_b
        # save the default animations
        actorDetails['routine'] = actorXPU.Parser['XML_Values']['Setup_Values'] \
            ['defaultAnimation']
        actorDetails['pose'] = actorXPU.Parser['XML_Values']['Setup_Values'] \
            ['defaultPose']
        # save position, heading and speed
        actorDetails['position'] = (actorXPU.Parser['XML_Values']['Setup_Values'] \
            ['positionX'], actorXPU.Parser['XML_Values']['Setup_Values']['positionY'], \
            actorXPU.Parser['XML_Values']['Setup_Values']['positionZ'])
        actorDetails['initialHeading'] = actorXPU.Parser['XML_Values']['Setup_Values'] \
            ['heading']
        actorDetails['speed'] = actorXPU.Parser['XML_Values']['Setup_Values']['speed']
        # check for not-so-commons and save
        for t_nv in t_ncl:
            if t_nv in actorXPU.Parser['XML_Values']['Setup_Values'].keys():
                # save the rare setting
                actorDetails[t_nv] = actorXPU.Parser['XML_Values']['Setup_Values'] \
                    [t_nv]
        # check whether this is a tracked actor
        if actorXPU.Parser['XML_Values']['Setup_Values']['isTracked'] == 1:
            actorDetails['camPosition'] = [actorXPU.Parser['XML_Values']['Setup_Values'] \
            ['cameraX'], actorXPU.Parser['XML_Values']['Setup_Values']['cameraY'], \
            actorXPU.Parser['XML_Values']['Setup_Values']['cameraZ']]
        # we store the new actor in our actor store
        # 0 - EdenWalker
        # 1 - EdenAero
        if actorXPU.Parser['XML_Values']['Setup_Values']['actorType'] == 0:
            self.actorStore[actorDetails['name']] = EdenWalker(actorDetails, \
                self.actorsNode)
        elif actorDetails['actorType'] == 1:
            self.actorStore[actorDetails['name']] = EdenAero(actorDetails, \
                self.actorsNode)
        else:
            # we will add other walkers here
            pass
        # check whether physics is wanted
        if actorXPU.Parser['XML_Values']['Setup_Values']['enablePhysics'] == 1:
            # check if the world has physics capability
            if self.worldData['enablePhysics'] != 1:
                # we don't have a prepared physics engine!
                pass
            else:
                # setup physics
                actorDetails['mass'] = actorXPU.Parser['XML_Values']['Setup_Values'] \
                ['mass']
                self.enableActorPhysics(actorDetails['name'])
                self.setActorMass(actorDetails['name'], actorDetails['mass'])
                # apply all global forces on the object
                for t_gf in self.physicsStore['globalForces']:
                    self.attachForceToActor(actorDetails['name'], self.GFP + t_gf)
        # check for terrain detection
        if actorXPU.Parser['XML_Values']['Setup_Values']['detectTerrain'] == 1:
            # setup terrain detection on the object
            t_tcn = self.actorStore[actorDetails \
                ['name']].baseActor.attachNewNode(CollisionNode(actorDetails['name'] \
                + '_TCN'))
            # the ray points directly downward
            t_tcn.node().addSolid(CollisionRay(0, 0, self.detectorHeight, 0, 0, -1))
            # set the bitmasks
            t_tcn.node().setFromCollideMask(BitMask32.bit(self.geomBitMask))
            t_tcn.node().setIntoCollideMask(BitMask32.allOff())
            # add to the collision handler (physics-dependent)
            if actorXPU.Parser['XML_Values']['Setup_Values']['enablePhysics'] == 0:
                # CollisionHandlerFloor
                self.terrainDetector.addCollider(t_tcn, \
                self.actorStore[actorDetails['name']].baseActor)
            else:
                # check if the world has physics capability
                if self.worldData['enablePhysics'] != 1:
                    # we don't have a prepared physics engine!
                    # CollisionHandlerFloor
                    self.terrainDetector.addCollider(t_tcn, \
                        self.actorStore[actorDetails['name']].baseActor)
                else:
                    # CollisionHandlerGravity
                    self.terrainDetector.addCollider(t_tcn, \
                        self.physicsStore['actors'][actorDetails['name']][0])
            # add to the collision traverser
            self.terraTrav.addCollider(t_tcn, self.terrainDetector)
            # set the flag if not set
            if self.terraDetection != True:
                self.terraDetection = True
        # return the name (used as key in actorStore)
        return actorDetails['name']
    # --------------------------INVENTORY MANIPULATION-----------------------
    def selectInventoryItem(self, inventoryName, itemName):
        " shows the inventory item selected and hides the rest "
        if itemName not in self.toolBox[inventoryName].keys():
            # item is not in inventory
            return False
        else:
            # hide all items first
            for t_x in self.toolBoxLists[inventoryName]:
                # hide item
                self.toolBox[inventoryName][t_x].hide()
            # show selected
            self.toolBox[inventoryName][itemName].show()
    # -----------------------------------------------------------------------
    # --------------------------UTILITY SERVICES-----------------------------
    # -----------------------------------------------------------------------
    # --------------------------PHYSICS SERVICES-----------------------------
    def enableActorPhysics(self, actorName):
        " enables physics for an actor "
        if actorName not in self.actorStore.keys():
            # the specified actor does not exist in the world
            return False
        else:
            t_s = actorName + '-physics'
            # we store the ActorNode as (NodePath, Node)
            t_a = ActorNode(t_s)
            t_n = self.actorPhysicsNode.attachNewNode(t_a)
            self.physicsStore['actors'][actorName] = [t_n, t_a]
            self.physicsManager.attachPhysicalNode(t_a)
            # reparent the object to the new physics node
            self.actorStore[actorName].baseActor.reparentTo(t_n)
            # set the physics status
            self.actorStore[actorName].physicsStatus = True
    def setActorMass(self, actorName, newMass):
        " sets the mass on a physics-enabled actor (KG) "
        if actorName not in self.actorStore.keys():
            # the specified actor does not exist in the world
            return False
        elif self.actorStore[actorName].physicsStatus == False:
            # physics is not enabled
            return False
        else:
            # we are sure of physics so just set the mass
            self.physicsStore['actors'][actorName] \
                [1].getPhysicsObject().setMass(newMass)
    def attachForceToActor(self, actorName, forceName):
        " attaches an existing force to an actor "
        if actorName not in self.actorStore.keys():
            # the specified actor does not exist in the world
            return False
        elif forceName not in self.physicsStore['forces'].keys():
            # the specified force does not exist
            return False
        elif self.actorStore[actorName].physicsStatus == False:
            # physics is not enabled
            return False
        else:
            # create a force node
            t_fn = ForceNode(actorName + forceName)
            # attach the force node to the object
            self.actorStore[actorName].baseActor.attachNewNode(t_fn)
            # add the force to the force node
            t_fn.addForce(self.physicsStore['forces'][forceName][0])
            # add the force (for now we only have one rotational force)
            if self.physicsStore['forces'][forceName][1] != 2:
                # a linear force
                self.physicsStore['actors'][actorName] \
                    [1].getPhysical(0).addLinearForce(self.physicsStore['forces'] \
                    [forceName][0])
            else:
                # an angular force
                self.physicsStore['actors'][actorName] \
                    [1].getPhysical(0).addAngularForce(self.physicsStore['forces'] \
                    [forceName][0])
    def removeForceFromActor(self, actorName, forceName):
        " removes an existing force from an actor "
        if actorName not in self.actorStore.keys():
            # the specified actor does not exist in the world
            return False
        elif forceName not in self.physicsStore['forces'].keys():
            # the specified force does not exist
            return False
        elif self.actorStore[actorName].physicsStatus == False:
            # physics is not enabled
            return False
        else:
            # remove the force (for now we only have one rotational force)
            if self.physicsStore['forces'][forceName][1] != 2:
                # a linear force
                self.physicsStore['actors'][actorName] \
                    [1].getPhysical(0).removeLinearForce(self.physicsStore['forces'] \
                    [forceName][0])
            else:
                # an angular force
                self.physicsStore['actors'][actorName] \
                    [1].getPhysical(0).removeAngularForce(self.physicsStore['forces'] \
                    [forceName][0])
    def attachJetPackToActor(self, forceName, jetPack, actorName, \
        packPos = (0,0,0), packHpr = None):
        " convenience function for attaching jetpacks to actors "
        if actorName not in self.actorStore.keys():
            # the specified actor does not exist in the world
            return False
        elif forceName not in self.physicsStore['forces'].keys():
            # the specified force does not exist
            return False
        elif self.actorStore[actorName].physicsStatus == False:
            # physics is not enabled
            return False
        else:
            # reparent the jetpack
            jetPack.reparentTo(self.actorStore[actorName].baseActor)
            # set a tag to show it exists
            self.actorStore[actorName].baseActor.setTag(jetPack.getName(), 'active')
            # set position and orientation on parent
            jetPack.setPos(packPos[0], packPos[1], packPos[2])
            if packHpr == None:
                # set the HPR to match the parent
                jetPack.setHpr(self.actorStore[actorName].baseActor.getH(), \
                    self.actorStore[actorName].baseActor.getP(), \
                    self.actorStore[actorName].baseActor.getR())
            else:
                # set custom HPR
                jetPack.setHpr(packHpr[0], packHpr[1], packHpr[2])
            # add the force (for now we only have one rotational force)
            if self.physicsStore['forces'][forceName][1] != 2:
                # a linear force
                self.physicsStore['actors'][actorName] \
                    [1].getPhysical(0).addLinearForce(self.physicsStore['forces'] \
                    [forceName][0])
            else:
                # an angular force
                self.physicsStore['actors'][actorName] \
                    [1].getPhysical(0).addAngularForce(self.physicsStore['forces'] \
                    [forceName][0])
    def removeJetPackFromActor(self, forceName, jetPackName, actorName):
        " convenience function for removing jetpacks from actors "
        if actorName not in self.actorStore.keys():
            # the specified actor does not exist in the world
            return False
        elif forceName not in self.physicsStore['forces'].keys():
            # the specified force does not exist
            return False
        elif self.actorStore[actorName].physicsStatus == False:
            # physics is not enabled
            return False
        else:
            # check if the jetPack is on the object
            t_f = self.actorStore[actorName].baseActor.findNetTag(jetPackName)
            if not t_f.isEmpty():
                # check whether the pack is active
                t_av = self.actorStore[actorName].baseActor.getTag(jetPackName)
                if t_av == 'active':
                    # find the jetpack node
                    t_jo = self.actorStore[actorName].baseActor.find(jetPackName)
                    # remove the jetpack
                    t_jo.removeNode()
                    # remove the force
                    if self.physicsStore['forces'][forceName][1] != 2:
                        # a linear force
                        self.physicsStore['actors'][actorName] \
                            [1].getPhysical(0).removeLinearForce(self.physicsStore['forces'] \
                            [forceName][0])
                    else:
                        # an angular force
                        self.physicsStore['actors'][actorName] \
                            [1].getPhysical(0).removeAngularForce(self.physicsStore['forces'] \
                            [forceName][0])
                    # remove the tag
                    self.actorStore[actorName].baseActor.setTag(jetPackName, 'removed')
                else:
                    # the pack does not exist (was removed)
                    return False
            else:
                # no jet pack
                return False
    # -----------------------------------------------------------------------
    # --------------------------SYSTEM SERVICES------------------------------
    def updateController(self, controlAction, keyValue):
        " updates the controller dictionary "
        # we capture the state of the controller keys
        self.controller[controlAction] = keyValue
        # we check the modifiers
        for t_x in self.modifiers.keys():
            self.modifiers[t_x][1] = self.getModifierKeyState(self.modifiers[t_x][0])
            self.walkerArgs[t_x] = self.modifiers[t_x][1]
    def updateActorsGFs(self, forceKey):
        " updates current actors when a new global force is created "
        # attach it to all actors loaded for physics so far
        for t_x in self.physicsStore['actors'].keys():
            self.attachForceToActor(t_x, self.GFP + forceKey)
    def keyboardSetup(self):
        " sets up key mappings from config.xml "
        # get key mappings information
        self.XPU.getSectionValues('section','Keys')
        for t_e in self.XPU.Parser['XML_Values']['Keys_Values'].keys():
            t_f = self.XPU.Parser['XML_Values']['Keys_Values'][t_e]
            # set key mappings for movement
            self.accept(t_f, self.updateController, [t_e, True] )
            self.accept('%s-up' % t_f, self.updateController, [t_e, False] )
            self.controller[t_e] = False
        if self.XPU.Parser['XML_Values']['WorldDetails_Values'] \
            ['enableModifiers'] == 1:
            self.XPU.getSectionValues('section','KeyModifiers')
            self.walkerArgs = {}
            # get key modifiers
            for t_e in self.XPU.Parser['XML_Values']['KeyModifiers_Values'].keys():
                t_f = self.XPU.Parser['XML_Values']['KeyModifiers_Values'][t_e]
                # set key modifiers
                self.modifiers[t_e] = [t_f, False]
                self.walkerArgs[t_e] = False
                self.walkerArgs[t_e + '_mode'] = True
    def resolveAnimations(self):
        " makes acceptable string values for animation keys "
        self.anime = str(self.mainActor.actorData['routine'])
    # -----------------------------------------------------------------------
    # --------------------------TASKS----------------------------------------
    def defaultAnimationTask(self, task):
        " task to handle the mainActor animations "
        # from Python 1.6.x loopAnimation() requires a non-Unicode string
        if task.frame == 0:
            self.resolveAnimations()
        # enable animation
        if True in self.controller.values():
          if self.mainActor.baseActor.getTag('Animated') == 'False':
            self.mainActor.loopAnimation(self.anime)
            self.mainActor.baseActor.setTag('Animated', 'True')
        else:
          if self.mainActor.baseActor.getTag('Animated') == 'True':
            self.mainActor.stopAnimation()
            self.mainActor.baseActor.pose(self.anime, \
                self.mainActor.actorData['pose'])
            self.mainActor.baseActor.setTag('Animated', 'False')
        return task.cont
    def updateViewTask(self, task):
        " task to update camera position when actor moves via forces "
        # check whether the actor isn't moving
        if True not in self.controller.values():
            # we ensure that the camera does not fall below the world
            t_az = self.mainActor.baseActor.getZ()
            t_wz = self.world.getZ()
            if t_az < t_wz:
                t_az = t_wz
            base.camera.setPos(self.mainActor.baseActor.getX() + self.camPos[0], \
                self.mainActor.baseActor.getY() + self.camPos[1], \
                t_az + self.camPos[2])
            base.camera.lookAt(self.mainActor.baseActor)
        return task.cont
    def MoverTask(self, task):
        " task to move camera and active actor "
        # calculate the frame interval
        elapsed = task.time - self.prevTime
        if self.controller['forward'] == True:
          newXY = self.mainActor.computeXY(elapsed, self.walkerArgs)
          self.mainActor.baseActor.setX(self.mainActor.baseActor.getX() - newXY[0])
          self.mainActor.baseActor.setY(self.mainActor.baseActor.getY() - newXY[1])
        if self.controller['backward'] == True:
          newXY = self.mainActor.computeXY(elapsed, self.walkerArgs)
          self.mainActor.baseActor.setX(self.mainActor.baseActor.getX() + newXY[0])
          self.mainActor.baseActor.setY(self.mainActor.baseActor.getY() + newXY[1])
        if self.controller['turnleft'] == True:
          # turn 90 degrees in a second
          self.mainActor.turnHeading(elapsed * 90)
        if self.controller['turnright'] == True:
          # turn 90 degrees in a second
          self.mainActor.turnHeading(-(elapsed * 90))
        # camera follows mainActor
        # we ensure that the camera does not fall below the world
        t_az = self.mainActor.baseActor.getZ()
        t_wz = self.world.getZ()
        if t_az < t_wz:
            t_az = t_wz
        base.camera.setPos(self.mainActor.baseActor.getX() + self.camPos[0], \
            self.mainActor.baseActor.getY() + self.camPos[1], \
            t_az + self.camPos[2])
        base.camera.lookAt(self.mainActor.baseActor)
        # update self.prevTime
        self.prevTime = task.time
        return task.cont
# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Actors]
# Desc: Actors Library - EdenActor Class
# File name: EdenActor.py
# Developed by: Project Eden Development Team
# Date: 04/07/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench PLC
# ---------------------------------------------
from direct.actor import Actor
from panda3d.core import *
from copy import copy
# ---------------------------------------------
# A base class to handle actor operations.
# Class definition for the EdenActor class
# ---------------------------------------------
class EdenActor:
    " The base class for all actors "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, actorDictionary, parentNode):
        # Load actor
        self.baseActor = Actor.Actor(actorDictionary['actor'], \
        actorDictionary['animations'])
        t_y = actorDictionary['scale']
        self.baseActor.setScale(t_y[0], t_y[1], t_y[2])
        self.baseActor.reparentTo(parentNode)
        # set the heading (where baseActor faces at opening)
        self.baseActor.setH(actorDictionary['initialHeading'])
        # set the actor position in world
        xyzPos = actorDictionary['position']
        self.baseActor.setPos(xyzPos[0],xyzPos[1],xyzPos[2])
        # store useful data
        self.actorData = copy(actorDictionary)
        # get bounds, center and radius
        t_b = self.baseActor.getChild(0).getBounds()
        t_r = t_b.getRadius()
        t_c = t_b.getCenter()
        self.actorData['bounds'] = t_b
        self.actorData['center'] = t_c
        self.actorData['radius'] = t_r
        # for collision detection
        self.actorCnode = None
        # for storing actual exposed nodes for joints
        self.jointsList = {}
        # for storing control dummy nodes for joints
        self.controllerList = {}
        # for physics status
        self.physicsStatus = False
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    # --------------------------ANIMATION--------------------------
    def playAnimation(self, animKey):
        " plays one iteration of an actor's animation "
        if animKey not in self.actorData['animations'].keys():
            # the specified animation does not exist
            return False
        else:
            # play the animation
            self.baseActor.play(animKey)
    def loopAnimation(self, animKey):
        " loops an actor's animation "
        if animKey not in self.actorData['animations'].keys():
            # the specified animation does not exist
            return False
        else:
            # loop the animation
            self.baseActor.loop(animKey)
    def stopAnimation(self):
        " stops an animation; just for completeness "
        self.baseActor.stop()
    def getAnimationControl(self, animKey):
        " returns a controller for a specific animation "
        return self.baseActor.getAnimControl(animKey)
    # --------------------------COLLISION--------------------------
    def computeSphere(self):
        " computes the dimensions of a collision sphere for the actor "
        # the sphere radius is actor radius * sphereFactor
        t_k = self.actorData['radius'] * self.actorData['sphereFactor']
        t_s = CollisionSphere(self.actorData['center'], t_k)
        return t_s
    def setupCollider(self, bitMask, collisionType = 0):
        " sets up sphere collision detection for the actor "
        # we create a new collision node
        t_Cnode = CollisionNode(self.actorData['name'])
        # we create a new collision sphere to fit actorObject
        # then give the cnode something to hold - the sphere
        t_Cnode.addSolid(self.computeSphere())
        # we get the node path of the cnode, now parented to actorObject
        self.actorCnode = self.baseActor.attachNewNode(t_Cnode)
        if collisionType == 0:
            # we set the FromCollisionMask of our actorObject to match the geometry
            # and the IntoCollisionMask to zero (actorObject only collides into things)
            self.actorCnode.node().setFromCollideMask(BitMask32.bit(bitMask))
            self.actorCnode.setCollideMask(BitMask32.allOff())
        elif collisionType == 1:
            # we set the FromCollisionMask of our actorObject to zero
            # and the IntoCollisionMask to match geometry (actorObject is only
            # collided into by things)
            self.actorCnode.node().setFromCollideMask(BitMask32.allOff())
            self.actorCnode.setCollideMask(BitMask32.bit(bitMask))
        else:
            # our actorObject is both a from and into object
            self.actorCnode.node().setFromCollideMask(BitMask32.bit(bitMask))
            self.actorCnode.setCollideMask(BitMask32.bit(bitMask))
    def showCnode(self):
        " shows the actor's collision node "
        self.actorCnode.show()
    def hideCnode(self):
        " hides the actor's collision node "
        self.actorCnode.hide()
    # --------------------------JOINTS------------------------------
    def getJointNodePath(self, jointName, modelRoot = 'modelRoot' ):
        " returns a node path for a joint; used in holding (attach) operations "
        # the node path obtained can act as a parent for any object.
        # the parented object becomes attached to the joint
        # useful for guns and inventory items. This node can NOT be used
        # to control an actor's joint!
        t_y = self.baseActor.exposeJoint(None, modelRoot, jointName)
        if t_y == None:
            # the joint does not exist
            return False
        else:
            # successful operation
            self.jointsList[jointName] = t_y
            return True
    def getJointControlPath(self, jointName, modelRoot = 'modelRoot' ):
        " returns a node path for a joint; used for control operations "
        # the node path obtained is a dummy node! It is transformed and
        # every frame this transform is applied to the joint in question.
        # It can NOT be used for holding operations!
        t_y = self.baseActor.controlJoint(None, modelRoot, jointName)
        if t_c == None:
            # the joint does not exist
            return False
        else:
            # successful operation
            self.controllerList[jointName] = t_c
            return True
    def releaseJointControlPath(self, jointName, modelRoot = 'modelRoot' ):
        " releases a joint from control operations "
        if jointName not in self.controllerList.keys():
            # invalid joint
            return False
        else:
            self.baseActor.releaseJoint(modelRoot, jointName)
            del self.controllerList[jointName]
            return True
    def listAllJoints(self):
        " lists all detected joints in the actor skeleton "
        self.baseActor.listJoints()
    # --------------------------VISIBILITY--------------------------
    def hideMe(self):
        " hides the actor "
        self.baseActor.hide()
    def showMe(self):
        " shows the actor "
        self.baseActor.show()
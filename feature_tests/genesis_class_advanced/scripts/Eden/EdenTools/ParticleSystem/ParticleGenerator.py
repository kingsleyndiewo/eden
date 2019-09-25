# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.ParticleSystem]
# Desc: ParticleSystem Library - ParticleGenerator Class 
# File name: ParticleGenerator.py
# Developed by: Project Eden Development Team
# Date: 13/09/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench Limited
# ---------------------------------------------
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from Eden.EdenTools.XMLParsers.ConfigParser import ConfigParser
from Eden.EdenTools.ParticleSystem.particle_globals import *
# ---------------------------------------------
# Class definition for the ParticleGenerator class
class ParticleGenerator:
    " Base class for all particle generators "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        # create the ParticleEffect object
        self.rootGenerator = ParticleEffect()
        self.particleXPU = ConfigParser()
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def loadDriver(self, fileName):
        " loads the executable code file of a specific effect "
        # open the file and read in text
        t_dv = open(fileName, 'r')
        t_data = t_dv.read()
        # delete all instances of '\r'
        t_data = t_data.replace('\r', '')
        try:
            exec t_data
        except:
            print 'Failed to load particle driver file: ', \
            repr(fileName)
            raise
    def setOrigin(self, parentNode, xyzPos = (0,0,0)):
        " sets the birth point of the generator "
        # set the parent
        self.rootGenerator.start(parentNode)
        # set the position relative to the parent
        self.rootGenerator.setPos(xyzPos[0], xyzPos[1], xyzPos[2])
    def loadXMLConfig(self, xmlParticle, extraData = None):
        " loads an XML config and feeds to the generic driver "
        # parse particles details XML (XPU = XML processing unit)
        self.particleXPU.parseFile(extraData['mvcConfigPath'] + xmlParticle)
        # get particles information
        self.particleXPU.getSectionValues('section','Generator')
        self.particleXPU.getSectionValues('subsection','General')
        self.particleXPU.getSectionValues('subsection','Factory')
        self.particleXPU.getSectionValues('subsection','Renderer')
        self.particleXPU.getSectionValues('subsection','Emitter')
        self.particleXPU.getSectionValues('subsection','forceGeneral')
        # get extra path data
        # store the needed paths
        t_m = extraData['mvcImagePath']
        # create the configuration dictionary
        t_xpd = {'f':{}, 'r':{}, 'e':{}, 'x':{}}
        # load the xml data into the dictionary
        # ---------------------------------------------------------------------
        # GENERAL GENERATOR PARAMETERS
        # ---------------------------------------------------------------------
        t_xpd['pos'] = (self.particleXPU.Parser['XML_Values'] \
            ['Generator_Values']['posX'], self.particleXPU.Parser['XML_Values'] \
            ['Generator_Values']['posY'], self.particleXPU.Parser['XML_Values'] \
            ['Generator_Values']['posZ'] )
        t_xpd['hpr'] = (self.particleXPU.Parser['XML_Values'] \
            ['Generator_Values']['genH'], self.particleXPU.Parser['XML_Values'] \
            ['Generator_Values']['genP'], self.particleXPU.Parser['XML_Values'] \
            ['Generator_Values']['genR'] )
        t_xpd['scale'] = (self.particleXPU.Parser['XML_Values'] \
            ['Generator_Values']['scaleX'], self.particleXPU.Parser['XML_Values'] \
            ['Generator_Values']['scaleY'], self.particleXPU.Parser['XML_Values'] \
            ['Generator_Values']['scaleZ'])
        # ---------------------------------------------------------------------
        # GENERAL PARTICLES PARAMETERS
        # ---------------------------------------------------------------------
        for t_x in self.particleXPU.Parser['XML_Values']['General_Values'].keys():
            t_xpd[t_x] = self.particleXPU.Parser['XML_Values']['General_Values'] \
            [t_x]
        # ---------------------------------------------------------------------
        # FACTORY PARAMETERS
        # ---------------------------------------------------------------------
        for t_x in self.particleXPU.Parser['XML_Values']['Factory_Values'].keys():
            t_xpd['f'][t_x] = self.particleXPU.Parser['XML_Values']['Factory_Values'] \
            [t_x]
        # ---------------------------------------------------------------------
        # RENDERER PARAMETERS
        # ---------------------------------------------------------------------
        for t_x in self.particleXPU.Parser['XML_Values']['Renderer_Values'].keys():
            t_xpd['r'][t_x] = self.particleXPU.Parser['XML_Values']['Renderer_Values'] \
            [t_x]
        if t_xpd['renderer'] == 'SpriteParticleRenderer':
            # get the texture for sprite particle renderers
            t_m += t_xpd['r']['texture']
            t_xpd['r']['texture'] = t_m
        elif t_xpd['renderer'] == 'GeomParticleRenderer':
            # get the node for geom particle renderers
            t_xpd['r']['geomNode'] = extraData['geomNode']
        # ---------------------------------------------------------------------
        # EMITTER PARAMETERS
        # ---------------------------------------------------------------------
        for t_x in self.particleXPU.Parser['XML_Values']['Emitter_Values'].keys():
            t_xpd['e'][t_x] = self.particleXPU.Parser['XML_Values']['Emitter_Values'] \
            [t_x]
        # ---------------------------------------------------------------------
        # FORCE GROUP PARAMETERS
        # ---------------------------------------------------------------------
        for t_x in self.particleXPU.Parser['XML_Values']['forceGeneral_Values'].keys():
            t_xpd['x'][t_x] = self.particleXPU.Parser['XML_Values'] \
            ['forceGeneral_Values'][t_x]
        # ---------------------------------------------------------------------
        # LOAD THE DRIVER
        # ---------------------------------------------------------------------
        self.genericDriver(t_xpd)
    # ------------------SERVICE METHODS-------------------
    # ----------------------------------------------------
    def genericDriver(self, effectData):
        " generic particle driver that allows XML definitions "
        self.rootGenerator.reset()
        self.rootGenerator.setPos(effectData['pos'][0], effectData['pos'][1], \
            effectData['pos'][2])
        self.rootGenerator.setHpr(effectData['hpr'][0], effectData['hpr'][1], \
            effectData['hpr'][2])
        self.rootGenerator.setScale(effectData['scale'][0], effectData['scale'][1], \
            effectData['scale'][2])
        # create the Particles object
        t_ps = Particles(effectData['name'])
        # Particles parameters
        # ---------------------------------------------------------------------
        # poolSize - maximum number of simultaneous particles (0 to infinity)
        # birthRate - seconds between particle births (0 to infinity)
        # litterSize - number of particles created at each birth (1 to infinity)
        # litterSpread - variation of litter size (0 to infinity)
        # localVelocityFlag - whether or not velocities are absolute (boolean)
        # systemGrowsOlder - whether or not the system has a lifespan (boolean)
        # systemLifespan - age of the system in seconds (0 to infinity)
        # Factory - PointParticleFactory or ZSpinParticleFactory
        # Renderer - PointParticleRenderer, LineParticleRenderer,
        #   SparkleParticleRenderer, SpriteParticleRenderer, GeomParticleRenderer
        # Emitter - BoxEmitter, DiscEmitter, PointEmitter, RectangleEmitter,
        #   RingEmitter, SphereSurfaceEmitter, SphereVolumeEmitter,
        #   TangentRingEmitter
        # ---------------------------------------------------------------------
        t_ps.setFactory(effectData['factory'])
        t_ps.setRenderer(effectData['renderer'])
        t_ps.setEmitter(effectData['emitter'])
        t_ps.setPoolSize(effectData['poolSize'])
        t_ps.setBirthRate(effectData['birthRate'])
        t_ps.setLitterSize(effectData['litterSize'])
        t_ps.setLitterSpread(effectData['litterSpread'])
        t_ps.setSystemLifespan(effectData['systemLifeSpan'])
        t_ps.setLocalVelocityFlag(effectData['LVF'])
        t_ps.setSystemGrowsOlderFlag(effectData['SGOF'])
        # ---------------------------------------------------------------------
        # Factory parameters
        # ---------------------------------------------------------------------
        # lifespanBase - average lifespan in seconds (0 to infinity)
        # lifespanSpread - variation in lifespan (0 to infinity)
        # massBase - average particle mass (0 to infinity)
        # massSpread - variation in particle mass (0 to infinity)
        # terminalVelocityBase - average particle terminal velocity (0 to infinity)
        # terminalVelocitySpread - variation in terminal velocity (0 to infinity)
        # ---------------------------------------------------------------------
        t_ps.factory.setLifespanBase(effectData['f']['lifeSpanBase'])
        t_ps.factory.setLifespanSpread(effectData['f']['lifeSpanSpread'])
        t_ps.factory.setMassBase(effectData['f']['massBase'])
        t_ps.factory.setMassSpread(effectData['f']['massSpread'])
        t_ps.factory.setTerminalVelocityBase(effectData['f']['TVB'])
        t_ps.factory.setTerminalVelocitySpread(effectData['f']['TVSpread'])
        # ---------------------------------------------------------------------
        # ZSpin factories have some additional parameters:
        # initialAngle - starting angle in degrees (0, 360) 
        # initialAngleSpread - spread of initial angle (0, 360) 
        # finalAngle - final angle in degrees (0, 360) 
        # finalAngleSpread - spread of final angle (0, 360)
        # ---------------------------------------------------------------------
        if effectData['factory'] == 'ZSpinParticleFactory':
            # we have to get the unique parameters
            t_ps.factory.setInitialAngle(effectData['f']['initialAngle'])
            t_ps.factory.setInitialAngleSpread(effectData['f']['initialAngleSpread'])
            t_ps.factory.setFinalAngle(effectData['f']['finalAngle'])
            t_ps.factory.setFinalAngleSpread(effectData['f']['finalAngleSpread'])
        # ---------------------------------------------------------------------
        # Renderer parameters
        # ---------------------------------------------------------------------
        # alphaMode - Alpha setting over particle lifetime (BaseParticleRenderer
        #               object: PR_ALPHA_NONE, PR_ALPHA_OUT, PR_ALPHA_IN or
        #               PR_ALPHA_USER)
        # userAlpha - Alpha value for ALPHA_USER alpha mode (Float)   
        # ---------------------------------------------------------------------
        t_ps.renderer.setAlphaMode(alphaModeList[effectData['r']['alphaMode']])
        t_ps.renderer.setUserAlpha(effectData['r']['userAlpha'])
        # ---------------------------------------------------------------------
        # PointParticle renderers have some additional parameters:
        # pointSize - width and height of points, in pixels (float) 
        # startColor - starting color (RGBA) 
        # endColor - ending color (RGBA) 
        # blendType - how the particles blend from the start color to the end
        #   color (ONE_COLOR, BLEND_LIFE, BLEND_VEL)
        # blendMethod - interpolation method between colors (LINEAR, CUBIC)
        # ---------------------------------------------------------------------
        if effectData['renderer'] == 'PointParticleRenderer':
            # we have to get the unique parameters
            t_ps.renderer.setPointSize(effectData['r']['pointSize'])
            t_ps.renderer.setStartColor(Vec4(effectData['r']['startColR'], \
                effectData['r']['startColG'], effectData['r']['startColB'], \
                effectData['r']['startColA']))
            t_ps.renderer.setEndColor(Vec4(effectData['r']['endColR'], \
                effectData['r']['endColG'], effectData['r']['endColB'], \
                effectData['r']['endColA']))
            t_ps.renderer.setBlendType(blendModeList[effectData['r']['blendType']])
            t_ps.renderer.setBlendMethod(interpolModeList[effectData['r']['blendMethod']])
        # ---------------------------------------------------------------------
        # LineParticle renderers have some additional parameters:
        # headColor - color of leading end (RGBA)
        # tailColor - color of trailing end (RGBA) 
        # ---------------------------------------------------------------------
        elif effectData['renderer'] == 'LineParticleRenderer':
            # we have to get the unique parameters
            t_ps.renderer.setHeadColor(Vec4(effectData['r']['headColR'][0], \
                effectData['r']['headColG'][1], effectData['r']['headColB'][2], \
                effectData['r']['headColA'][3]))
            t_ps.renderer.setTailColor(Vec4(effectData['r']['tailColR'], \
                effectData['r']['tailColG'], effectData['r']['tailColB'], \
                effectData['r']['tailColA']))
        # ---------------------------------------------------------------------
        # SparkleParticle renderers have some additional parameters:
        # centerColor - color of leading end (RGBA)
        # edgeColor - color of trailing end (RGBA)
        # birthRadius - initial sparkle radius (0 to infinity)
        # deathRadius - final sparkle radius (0 to infinity)
        # lifeScale - whether or not sparkle radius is fixed to birthRadius
        #               (NO_SCALE or SCALE)
        # ---------------------------------------------------------------------
        elif effectData['renderer'] == 'SparkleParticleRenderer':
            # we have to get the unique parameters
            t_ps.renderer.setCenterColor(Vec4(effectData['r']['centerColR'], \
                effectData['r']['centerColG'], effectData['r']['centerColB'], \
                effectData['r']['centerColA']))
            t_ps.renderer.setEdgeColor(Vec4(effectData['r']['edgeColR'], \
                effectData['r']['edgeColG'], effectData['r']['edgeColB'], \
                effectData['r']['edgeColA']))
            t_ps.renderer.setBirthRadius(effectData['r']['birthRadius'])
            t_ps.renderer.setDeathRadius(effectData['r']['deathRadius'])
            t_ps.renderer.setLifeScale(lifeScaleList[effectData['r']['lifeScale']])
        # ---------------------------------------------------------------------
        # SpriteParticle renderers have some additional parameters:
        # texture - Panda texture to use as sprite image (texture)
        # color - color (RGBA)
        # xScaleFlag - if true, x scale is interpolated over particle life (boolean)
        # yScaleFlag - if true, y scale is interpolated over particle life (boolean)
        # animAngleFlag - if true, particles are set to spin on the Z axis (boolean) 
        # initialXScale - initial x scaling factor (0, infinity) 
        # finalXScale - final x scaling factor (0, infinity) 
        # initialYScale - initial y scaling factor (0, infinity) 
        # finalYScale - final y scaling factor (0, infinity) 
        # nonAnimatedTheta - if false, sets the counterclockwise Z rotation of
        # all sprites, in degrees (boolean) 
        # alphaBlendMethod - sets the interpolation blend method (LINEAR, CUBIC) 
        # alphaDisable If true, alpha blending is disabled (boolean) 
        # ---------------------------------------------------------------------
        elif effectData['renderer'] == 'SpriteParticleRenderer':
            # we have to get the unique parameters
            t_ps.renderer.setTexture(loader.loadTexture(effectData['r']['texture']))
            t_ps.renderer.setColor(Vec4(effectData['r']['colR'], \
                effectData['r']['colG'], effectData['r']['colB'], \
                effectData['r']['colA']))
            t_ps.renderer.setXScaleFlag(effectData['r']['xScaleFlag'])
            t_ps.renderer.setYScaleFlag(effectData['r']['yScaleFlag'])
            t_ps.renderer.setAnimAngleFlag(effectData['r']['animAngleFlag'])
            t_ps.renderer.setInitialXScale(effectData['r']['initialXScale'])
            t_ps.renderer.setFinalXScale(effectData['r']['finalXScale'])
            t_ps.renderer.setInitialYScale(effectData['r']['initialYScale'])
            t_ps.renderer.setFinalYScale(effectData['r']['finalYScale'])
            t_ps.renderer.setNonanimatedTheta(effectData['r']['nonAnimatedTheta'])
            t_ps.renderer.setAlphaBlendMethod(interpolModeList[effectData['r'] \
                ['blendMethod']])
            t_ps.renderer.setAlphaDisable(effectData['r']['disableAlpha'])
        # ---------------------------------------------------------------------
        # GeomParticle renderers have some additional parameters:
        # geomNode - Panda geometry scene graph node (node)
        elif effectData['renderer'] == 'GeomParticleRenderer':
            # we have to get the unique parameters
            t_ps.renderer.setGeomNode(effectData['r']['geomNode'])
        # ---------------------------------------------------------------------
        # Emitter parameters
        # ---------------------------------------------------------------------
        # emissionType - emission mode (ET_EXPLICIT, ET_RADIATE, ET_CUSTOM)
        # explicitLaunchVector - initial velocity in explicit mode (x,y,z)
        # radiateOrigin - point particles launch away from in radiate mode (x,y,z)
        # amplitude - launch velocity multiplier (-infinity to infinity float)
        # amplitudeSpread - spread for launch velocity multiplier (0 to infinity)
        # offsetForce - user defined force (x,y,z)
        # ---------------------------------------------------------------------
        t_ps.emitter.setEmissionType(emissionList[effectData['e']['emissionType']])
        t_ps.emitter.setExplicitLaunchVector(Vec3(effectData['e']['elvX'], effectData['e'] \
            ['elvY'], effectData['e']['elvZ']))
        t_ps.emitter.setRadiateOrigin(Point3(effectData['e']['roX'], effectData['e'] \
            ['roY'], effectData['e']['roZ']))
        t_ps.emitter.setAmplitude(effectData['e']['amplitude'])
        t_ps.emitter.setAmplitudeSpread(effectData['e']['amplitudeSpread'])
        t_ps.emitter.setOffsetForce(Vec3(effectData['e']['offX'], effectData['e'] \
            ['offY'], effectData['e']['offZ']))
        # ---------------------------------------------------------------------
        # Box emitters have some additional parameters:
        # minBound - minimum point for box volume (x,y,z)
        # maxBound - maximum point for box volume (x,y,z) 
        # ---------------------------------------------------------------------
        if effectData['emitter'] == 'BoxEmitter':
            # we have to get the unique parameters
            t_ps.emitter.setMinBound(Vec3(effectData['e']['minBoundX'], \
                effectData['e']['minBoundY'], effectData['e']['minBoundZ']))
            t_ps.emitter.setMaxBound(Vec3(effectData['e']['maxBoundX'], \
                effectData['e']['maxBoundY'], effectData['e']['maxBoundZ']))
        # ---------------------------------------------------------------------
        # Disc emitters have some additional parameters:
        # radius - radius of disc (0, infinity)
        # outerAngle - particle launch angle at edge of disc (0, 360)
        # innerAngle - particle launch angle at center of disc (0, 360)
        # outerMagnitude - launch velocity multiplier at edge of disc (-infinity
        #   to infinity float)
        # innerMagnitude - launch velocity multiplier at center of disc (-infinity
        #   to infinity float)
        # cubicLerping - whether or not magnitude/angle interpolation is cubic
        #   (boolean)
        # ---------------------------------------------------------------------
        elif effectData['emitter'] == 'DiscEmitter':
            # we have to get the unique parameters
            t_ps.emitter.setRadius(effectData['e']['discRadius'])
            t_ps.emitter.setOuterAngle(effectData['e']['outerAngle'])
            t_ps.emitter.setInnerAngle(effectData['e']['innerAngle'])
            t_ps.emitter.setOuterMagnitude(effectData['e']['outerMagnitude'])
            t_ps.emitter.setInnerMagnitude(effectData['e']['innerMagnitude'])
            t_ps.emitter.setCubicLerping(effectData['e']['cubicLerping'])
        # ---------------------------------------------------------------------
        # Point emitters have some additional parameters:
        # location - location of outer point (x,y,z)
        # ---------------------------------------------------------------------
        elif effectData['emitter'] == 'PointEmitter':
            # we have to get the unique parameters
            t_ps.emitter.setLocation(Vec3(effectData['e']['locationX'], \
                effectData['e']['locationY'], effectData['e']['locationZ']))
        # ---------------------------------------------------------------------
        # Rectangle emitters have some additional parameters:
        # minBound - 2D point defining the rectangle (x,z)
        # maxBound - 2D point defining the rectangle (x,z)
        # ---------------------------------------------------------------------
        elif effectData['emitter'] == 'RectangleEmitter':
            # we have to get the unique parameters
            t_ps.emitter.setMinBound(effectData['e']['minBoundX'], \
                effectData['e']['minBoundZ'])
            t_ps.emitter.setMaxBound(effectData['e']['maxBoundX'], \
                effectData['e']['maxBoundZ'])
        # ---------------------------------------------------------------------
        # Ring emitters have some additional parameters:
        # radius - radius of ring (0 to infinity)
        # angle - particle launch angle (0,360)
        # ---------------------------------------------------------------------
        elif effectData['emitter'] == 'RingEmitter':
            # we have to get the unique parameters
            t_ps.emitter.setRadius(effectData['e']['ringRadius'])
            t_ps.emitter.setAngle(effectData['e']['launchAngle'])
        # ---------------------------------------------------------------------
        # SphereSurface emitters have some additional parameters:
        # radius - radius of sphere (0 to infinity)
        # ---------------------------------------------------------------------
        elif effectData['emitter'] == 'SphereSurfaceEmitter':
            # we have to get the unique parameters
            t_ps.emitter.setRadius(effectData['e']['sphereRadius'])
        # ---------------------------------------------------------------------
        # SphereVolume emitters have some additional parameters:
        # radius - radius of sphere (0 to infinity)
        # ---------------------------------------------------------------------
        elif effectData['emitter'] == 'SphereVolumeEmitter':
            # we have to get the unique parameters
            t_ps.emitter.setRadius(effectData['e']['sphereRadius'])
        # ---------------------------------------------------------------------
        # TangentRing emitters have some additional parameters:
        # radius - radius of ring (0 to infinity)
        # ---------------------------------------------------------------------
        elif effectData['emitter'] == 'TangentRingEmitter':
            # we have to get the unique parameters
            t_ps.emitter.setRadius(effectData['e']['ringRadius'])
        # ---------------------------------------------------------------------
        # add the particle object to the generator
        # ---------------------------------------------------------------------
        self.rootGenerator.addParticles(t_ps)
        # ---------------------------------------------------------------------
        # set the forces (if any)
        # ---------------------------------------------------------------------
        if effectData['x']['nullSection'] != True:
            # create the ForceGroup object
            t_fg = ForceGroup(effectData['x']['fgName'])
            # create the force(s)
            for t_h in range(effectData['x']['forceCount']):
                # get the force t_h
                t_s = '%s%d' % ('force', t_h)
                self.particleXPU.getSectionValues('force', t_s)
                t_a = t_s + '_Values'
                # create the force
                t_b = self.particleXPU.Parser['XML_Values'][t_a]['forceType']
                t_f1 = forceList[t_b](self.particleXPU.Parser['XML_Values'][t_a] \
                    ['forceX'], self.particleXPU.Parser['XML_Values'][t_a] \
                    ['forceY'], self.particleXPU.Parser['XML_Values'][t_a] \
                    ['forceZ'])
                # set the force parameters
                t_f1.setActive(self.particleXPU.Parser['XML_Values'][t_a] \
                    ['setForceActive'])
                # add the force to the force group
                t_fg.addForce(t_f1)
            # add the force group to the generator
            self.rootGenerator.addForceGroup(t_fg)
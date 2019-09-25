# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.ParticleSystem]
# Desc: ParticleSystem Library - Global defines for ParticleGenerator Class 
# File name: particle_globals.py
# Developed by: Project Eden Development Team
# Date: 16/09/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench Limited
# ---------------------------------------------
from panda3d.core import *
from panda3d.physics import *
# ---------------------------------------------
# utility lists
alphaModeList = (BaseParticleRenderer.PRALPHANONE, BaseParticleRenderer.PRALPHAOUT, \
        BaseParticleRenderer.PRALPHAIN, BaseParticleRenderer.PRALPHAUSER)
blendModeList = (PointParticleRenderer.PPONECOLOR, PointParticleRenderer.PPBLENDLIFE, \
        PointParticleRenderer.PPBLENDVEL)
interpolModeList = (BaseParticleRenderer.PPNOBLEND, BaseParticleRenderer.PPBLENDLINEAR, \
        BaseParticleRenderer.PPBLENDCUBIC)
lifeScaleList = (SparkleParticleRenderer.SPNOSCALE, SparkleParticleRenderer.SPSCALE)
emissionList = (BaseParticleEmitter.ETEXPLICIT, BaseParticleEmitter.ETRADIATE, \
                BaseParticleEmitter.ETCUSTOM)
forceList = (LinearVectorForce, AngularVectorForce, LinearJitterForce, \
             LinearNoiseForce )
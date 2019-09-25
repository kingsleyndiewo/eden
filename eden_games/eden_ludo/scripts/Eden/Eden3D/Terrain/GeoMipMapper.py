# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Terrain]
# Desc: Terrain Library - GeoMipMapper Class
# File name: GeoMipMapper.py
# Developed by: Project Eden Development Team
# Date: 10/08/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench PLC
# ---------------------------------------------
from direct.task import Task
from pandac.PandaModules import *
# ---------------------------------------------
# A base class to handle geometrical mipmapping.
# Intended as a helper class for the Worlds.
# Class definition for the GeoMipMapper class
# ---------------------------------------------
class GeoMipMapper:
    " The base class for all geometrical mipmappers "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, terraDictionary, parentNode):
        # Generate the terrain
        t_trn = GeoMipTerrain(terraDictionary['name'])
        # We either get a path to a heightfield or the name of
        # a heightfield in the terrainLib directory
        if terraDictionary['source'] == 0:
            # we get the heightfield from MVC terrain folder
            # We have to build a filename in this branch due to
            # new setHeightfield function (14/05/09)
            t_hf = terraDictionary['terrainPath'] + terraDictionary['heightField']
        else:
                # we have a fully formed file path
                t_hf = terraDictionary['heightField']
        # heightfields are now given simply as a file path (14/05/09)
        # -----------------------------------------------------
        t_trn.setHeightfield(t_hf)
        # -----------------------------------------------------
        # Set terrain properties
        t_trn.setBlockSize(terraDictionary['blockSize'])
        t_trn.setFactor(terraDictionary['chunkQuality'])
        # this is the node where quality has to be greatest
        # usually you want this to be base.camera
        # a Point2 or Point3 location can also be specified
        t_trn.setFocalPoint(terraDictionary['focalPointNode'])
        if terraDictionary['disableLOD'] == 0:
            # set the LOD option
            t_trn.setBruteforce(False)
            # set minimum LOD level (the higher the figure, the less
            # the quality at focal point)
            t_trn.setMinLevel(terraDictionary['minimumLOD'])
        else:
            # set the LOD option (you better have a super-computer)
            # or a really small heightfield
            t_trn.setBruteforce(True)
        # get the node path and parent it
        self.baseTerrain = t_trn.getRoot()
        self.baseTerrain.reparentTo(parentNode)
        # we scale the Z-axis to exaggerate the roughness of the
        # terrain - we might want mountains or hills
        self.baseTerrain.setSz(terraDictionary['heightScale'])
        # prepare the terrain base color
        t_c = (terraDictionary['baseR'], terraDictionary['baseG'], \
            terraDictionary['baseB'])
        # set the terrain base texture (if any)
        if terraDictionary['textured'] == 1:
            # set the wrap mode
            if terraDictionary['wrapMode'] == 0:
                # WMRepeat - tiles the texture to infinity
                terraDictionary['baseTexture'].setWrapU(Texture.WMRepeat)
                terraDictionary['baseTexture'].setWrapV(Texture.WMRepeat)
            elif terraDictionary['wrapMode'] == 1:
                # WMClamp - the edge pixels stretch out to infinity
                terraDictionary['baseTexture'].setWrapU(Texture.WMClamp)
                terraDictionary['baseTexture'].setWrapV(Texture.WMClamp)
            elif terraDictionary['wrapMode'] == 2:
                # WMBorderColor - the specified color is applied from end of
                # the texture to infinity
                terraDictionary['baseTexture'].setWrapU(Texture.WMBorderColor)
                terraDictionary['baseTexture'].setWrapV(Texture.WMBorderColor)
                terraDictionary['baseTexture'].setBorderColor(VBase4(t_c[0], \
                    t_c[1], t_c[2], 1.0))
            elif terraDictionary['wrapMode'] == 3:
                # WMMirror - the texture is tiled in flip-flops to infinity
                terraDictionary['baseTexture'].setWrapU(Texture.WMMirror)
                terraDictionary['baseTexture'].setWrapV(Texture.WMMirror)
            # apply the texture
            self.baseTerrain.setTexture(terraDictionary['baseTexture'])
            # if we set the base color it shows through the texture so we
            # leave it out unless someone wants WMBorderColor
        else:
            # no texture so we can just apply base color indiscriminately
            self.baseTerrain.setColor(t_c[0], t_c[1], t_c[2], 1.0)
        # generate the terrain
        t_trn.generate()
        if terraDictionary['autoUpdate'] == 1:
            # add a task to keep updating the terrain
            t_sr = str(terraDictionary['name'])
            taskMgr.add(t_trn.update, t_sr, extraArgs = [])
        else:
            # the client will deal with this manually (dimwit)
            pass
        # save a pointer to the GeoMipTerrain instance
        self.geoMipMap = t_trn
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    # the daughter classes will extend this
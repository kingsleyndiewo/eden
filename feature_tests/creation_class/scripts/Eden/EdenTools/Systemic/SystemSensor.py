# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.Systemic]
# Desc: System Library - SystemSensor Class 
# File name: SystemSensor.py
# Developed by: Project Eden Development Team
# Date: 30/07/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench Limited
# ---------------------------------------------
import sys
from platform import *
from panda3d.core import ConfigVariableString, ConfigVariableBool
from panda3d.core import getModelPath, Filename
# ---------------------------------------------
# Class definition for the SystemSensor class
class SystemSensor:
    " Base class for all system information parsers "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, skipPrc = False, customData = None): # constructor
        # get the Python executable path
        pyExec = sys.executable
        # get the Python root folder
        if pyExec.endswith('python.exe') == True:
            # we are on Windows so the executable is python.exe
            t_y = pyExec.partition('python.exe')
            # get the root folder
            t_y = t_y[0]
            pyRoot = t_y
            # get the Eden root (17/08/09) - Eden Inside
            edenRoot = 'Eden'
        else:
            # on Linux the Python root is usr/local/lib/python
            pyRoot = '/usr/local/lib/python'
            # get the Eden root (17/08/09) - Eden Inside
            edenRoot = 'Eden'
        # get the Python version
        pyVer = python_version()
        # get the operating system
        sysName = system()
        # save all to a dictionary
        self.systemData = {'interpreter':pyExec, 'pythonVersion':pyVer, \
            'OS':sysName, 'screenResolution':None, 'rootFolder':pyRoot, \
            'edenRoot':edenRoot}
        if skipPrc != True:
            # ---------------------------CONFIG.PRC---------------------
            # We will obtain various settings from the Config.prc
            # file. That should be a pretty solid location to get good
            # information pertaining to the graphics subsystem.
            # ---------------------------RESOLUTION---------------------
            # we force the default to 800 x 600 (Panda uses 640 x 480)
            # Don't mind the warning that will appear; we know what we
            # are doing.
            t_res = ConfigVariableString('win-size', '800 600')
            t_s = t_res.getValue()
            # the value at this point is '800 600'
            t_s = t_s.split(' ')
            # at this point it is [800, 600]
            self.updateResolution(int(t_s[0]), int(t_s[1]))
            # ---------------------------FUNTRENCH EDEN PRC DEFAULTS---
            # These were put here so that we don't have to set them in the
            # prc file
            if customData == None:
                # set default values
                customData = {'win-origin':'-2 -2', 'window-title':'Eden 3D System', \
                    'fullscreen':True, 'audio-library-name':'p3openal_audio', \
                    'extraPaths':[]}
                # extra paths
                customData['extraPaths'].append(edenRoot + "/Eden2D/fontLib")
            t_wo = ConfigVariableString('win-origin', customData['win-origin'])
            t_wt = ConfigVariableString('window-title', customData['window-title'])
            t_fs = ConfigVariableBool('fullscreen', customData['fullscreen'])
            t_al = ConfigVariableString('audio-library-name', customData['audio-library-name'])
            # set the values if different
            if t_wo.getValue() != '-2 -2':
                t_wo.setValue('-2 -2')
            if t_wt.getValue() != 'Eden 3D System':
                t_wt.setValue('Eden 3D System')
            if t_fs.getValue() != True:
                t_fs.setValue(True)
            if t_al.getValue() != 'p3openal_audio':
                t_al.setValue('p3openal_audio')
            # add extra paths to the model path
            t_fpt = getModelPath()
            for t_y in customData['extraPaths']:
                t_fpt.appendPath(t_y)
            # ---------------------------RENDERING---------------------
            t_ren = ConfigVariableString('load-display')
            t_ren = t_ren.getValue()
            t_valid = {'pandagl':'OpenGL', 'pandadx8':'DirectX 8.0', \
                'pandadx9':'DirectX 9.0'}
            if t_ren in t_valid.keys():
                # we parsed a correct engine
                self.systemData['renderer'] = t_valid[t_ren]
            else:
                # something must be very wrong!
                self.systemData['renderer'] = 'Unavailable'
            # ----------------------END--CONFIG.PRC---------------------
        else:
            # this class can be used outside a Panda-related system
            pass
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def updateResolution(self, scrX, scrY):
        " updates the resolution value to reflect changes "
        # NOTE: if these aren't a float, unpredictable results occur
        scrX *= 1.0 
        scrY *= 1.0
        # we won't update the prc object, just our local value.
        self.systemData['screenResolution'] = (scrX, scrY)
    def convertFilename(self, filePath):
        " converts a Windows filename to Panda(UNIX) format "
        # WRONG:
            # loader.loadModel("c:\\Program Files\\My Game\\Models\\Model1.egg")
        # RIGHT:
            # loader.loadModel("/c/Program Files/My Game/Models/Model1.egg")
        return Filename.fromOsSpecific(filePath)
    # ------------------SERVICE METHODS-------------------
    # ----------------------------------------------------
    
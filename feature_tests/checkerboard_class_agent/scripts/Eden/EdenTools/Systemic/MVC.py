# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.Systemic]
# Desc: System Library - MVC_System Class
# File name: MVC.py
# Developed by: Project Eden Development Team
# Date: 16/06/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench Limited
# ---------------------------------------------
import sys
from os.path import *
import os
from mvc_globals import *
from panda3d.core import getModelPath
# ---------------------------------------------
# Class definition for the MVC_System class
class MVC_System:
    " Base class for all MVC traversers "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, rootDir): # constructor
        # Figure out the Python root, since we have SystemSensor in creation
        # this is a duplicate but we are using sys anyway so let's just do
        # it independently. Also, this makes our MVC independent of SystemSensor
        t_p = sys.executable
        # Store the MVC root directory
        t_d = abspath(rootDir) # just to make sure we have a valid path
        # initialize structure dictionary
        self.mvcStructure = {'PythonPath':t_p, '/':t_d}
        self.mvcStructure['Missing_Folders'] = []
        self.mvcStructure['Missing_Files'] = []
        # list of MVC components under root
        self.mvcStructure['MVC_Components'] = mvc_dirs
        self.mvcStructure['MVC_Files'] = mvc_files
        # list of convenience components
        self.mvcStructure['MVC_ResourceTier'] = mvc_resourceTier
        self.mvcStructure['MVC_SoundTier'] = mvc_soundsTier
        self.mvcStructure['MVC_ModelsTier'] = mvc_modelsTier
        self.mvcStructure['MVC_TextTier'] = mvc_textTier
        # location of valid convenience paths
        self.mvcStructure['tier_resource'] = {}
        self.mvcStructure['tier_models'] = {}
        self.mvcStructure['tier_sound'] = {}
        self.mvcStructure['tier_text'] = {}
        # verify the MVC
        self.verifyMVC(t_d)
        # set the root directory on the path if valid MVC
        if self.fullMVC == True:
            sys.path.insert(0, t_d)
        # add extra paths to the model path if existent
        t_fpt = getModelPath()
        try:
            t_fpt.appendPath(self.mvcStructure['tier_text']['fonts'])
        except KeyError:
            print "Eden Warning: No fonts directory found"
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def printMVC(self):
        " prints the MVC tree "
        print self.mvcStructure['/']
        for t_y in self.mvcStructure['MVC_Components']:
            print '\t' + self.mvcStructure[t_y]
    # ------------------SERVICE METHODS-------------------
    # ----------------------------------------------------
    def verifyMVC(self, mvcRootDir):
        " verifies that all vital dirs and files are present "
        # ---------------------DIRECTORIES---------------------
        for t_x in self.mvcStructure['MVC_Components']:
            t_s = mvcRootDir + '/' + t_x
            if isdir(t_s) == True:
                # the t_x subdirectory exists
                # by using abspath() we let Python resolve for UNIX/Windows
                self.mvcStructure[t_x] = abspath(t_s)
                if t_x == 'resources':
                    # build paths for convenience
                    # we will save all paths relative to 'scripts'
                    for t_p in self.mvcStructure['MVC_ResourceTier']:
                        t_h = mvcRootDir + '/' + t_x + '/' + t_p
                        if isdir(t_h) == True:
                            # the t_p subdirectory exists
                            # we use relative paths which prevents path errors
                            # in loader.load<object>
                            t_h = '../' + t_x + '/' + t_p
                            self.mvcStructure['tier_resource'][t_p] = t_h
                            # just one more nest for tier-2
                            if t_p == 'sound':
                                # build paths for convenience
                                # we will save all paths relative to 'scripts'
                                for t_v in self.mvcStructure['MVC_SoundTier']:
                                    t_z = mvcRootDir + '/' + t_x + '/' + t_p + \
                                        '/' + t_v
                                    if isdir(t_z) == True:
                                        # the t_v subdirectory exists
                                        # we use relative paths .....
                                        t_z = '../' + t_x + '/' + t_p + '/' + t_v
                                        self.mvcStructure['tier_sound'] \
                                        [t_v] = t_z
                            elif t_p == 'models':
                                # build paths for convenience
                                # we will save all paths relative to 'scripts'
                                for t_v in self.mvcStructure['MVC_ModelsTier']:
                                    t_z = mvcRootDir + '/' + t_x + '/' + t_p + \
                                        '/' + t_v
                                    if isdir(t_z) == True:
                                        # the t_v subdirectory exists
                                        # we use relative paths .....
                                        t_z = '../' + t_x + '/' + t_p + '/' + t_v
                                        self.mvcStructure['tier_models'] \
                                        [t_v] = t_z
                            elif t_p == 'text':
                                # build paths for convenience
                                # we will save all paths relative to 'scripts'
                                for t_v in self.mvcStructure['MVC_TextTier']:
                                    t_z = mvcRootDir + '/' + t_x + '/' + t_p + \
                                        '/' + t_v
                                    if isdir(t_z) == True:
                                        # the t_v subdirectory exists
                                        # we use relative paths .....
                                        t_z = '../' + t_x + '/' + t_p + '/' + t_v
                                        self.mvcStructure['tier_text'] \
                                        [t_v] = t_z
            else:
                self.mvcStructure[t_x] = NO_EXIST
                # store the name of the missing component
                self.mvcStructure['Missing_Folders'].append(t_x)
        # ---------------------DIRECTORIES---------------------
        # -----------------------------------------------------
        # ---------------------FILES---------------------------
        for t_x in self.mvcStructure['MVC_Files']:
            t_s = mvcRootDir + '/' + t_x[0] + '/' + t_x[1]
            if isfile(t_s) == True:
                # the t_x[1] file exists
                # by using abspath() we let Python resolve for UNIX/Windows
                self.mvcStructure[t_x[1]] = abspath(t_s)
            else:
                self.mvcStructure[t_x[1]] = NO_EXIST
                # store the name of the missing component
                self.mvcStructure['Missing_Files'].append(t_x[1])
        # ---------------------FILES---------------------------
        # if NO_EXIST was stored then set the incomplete flag
        if NO_EXIST not in self.mvcStructure.values():
            self.fullMVC = True
        else:
            self.fullMVC = False
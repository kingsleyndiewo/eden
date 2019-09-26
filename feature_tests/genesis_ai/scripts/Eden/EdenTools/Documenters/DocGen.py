# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.Documenters]
# Desc: Documenters Library - DocGen Class 
# File name: DocGen.py
# Developed by: Project Eden Development Team
# Date: 04/08/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench Limited
# ---------------------------------------------
from Eden.EdenTools.Systemic.SystemSensor import SystemSensor
from os import execl, chdir
# ---------------------------------------------
# Class definition for the DocGen class
class DocGen:
    " Base class for all documentation generators "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        # get python path
        self.sysInfo = SystemSensor(True)
        self.sysExec = self.sysInfo.systemData['interpreter']
        self.pyPath = self.sysInfo.systemData['rootFolder']
        # generate the path to the python module pydoc
        if self.pyPath.find('\\') != -1:
            # Windows
            t_y = self.pyPath + 'Lib\\pydoc.py'
            self.edenDocs = self.sysInfo.systemData['edenRoot'] + '\\Docs'
        else:
            # Linux
            t_y = self.pyPath + 'Lib/pydoc.py'
            self.edenDocs = self.sysInfo.systemData['edenRoot'] + '/Docs'
        self.modulePath = t_y
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def generateDoc(self, packageName, docPath):
        " generates a documentation HTML for the package argued "
        # change the current directory to the documentation directory
        # otherwise we won't know where the HTML is
        chdir(docPath)
        # we run pydoc with pydoc -w <name> to generate a HTML file
        # <name>.html
        execl(self.sysExec, 'python', self.modulePath, \
            '-w', packageName)
    # ------------------SERVICE METHODS-------------------
    # ----------------------------------------------------
    
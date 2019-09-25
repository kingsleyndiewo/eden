# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.Documenters]
# Desc: Documenters Library - EdenHelper Class 
# File name: EdenHelper.py
# Developed by: Project Eden Development Team
# Date: 04/08/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from Eden.EdenTools.Documenters.DocGen import DocGen
# ---------------------------------------------
# Class definition for the EdenHelper class
class EdenHelper(DocGen):
    " Extends DocGen to document the Eden API "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, packageList = ['Eden']): # constructor
        DocGen.__init__(self) # ancestral constructor
        self.packageList = packageList
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def docEden(self):
        "generates full documentation for Eden"
        for t_x in self.packageList:
            # generate package documentation
            self.generateDoc(t_x, self.edenDocs)
    # ------------------SERVICE METHODS-------------------
    # ----------------------------------------------------
    
# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.XMLGenerators]
# Desc: XML Generating Library - ConfigGenerator Class
# File name: ConfigGenerator.py
# Developed by: Project Eden Development Team
# Date: 13/05/2009
# Place: Nairobi, Kenya
# Copyright: (C)2009 Funtrench Limited
# ---------------------------------------------
from XGenerator import XGenerator
# ---------------------------------------------
# Class definition for the XGenerator class
# ---------------------------------------------
class ConfigGenerator(XGenerator):
    " Extends XGenerator for configuration generators "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        XGenerator.__init__(self) # ancestral constructor
        # define list of value tagIDs
        self.valueTags = ['value', 'ivalue', 'fvalue', 'bvalue']
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def generateConfigXML(self, fileName, tabWidth = '    '):
        " saves the generated configuration XML to file "
        # use ordinary file I/O method
        t_f = open(fileName, 'w')
        # write the header and a newline
        t_f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        # write the child nodes
        for t_node in self.XMLDocument.childNodes:
            # TODO: check if it is a value element
            t_node.writexml(t_f, tabWidth, tabWidth, '\n')
        t_f.close()
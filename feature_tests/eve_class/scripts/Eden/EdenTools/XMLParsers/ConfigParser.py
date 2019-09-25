# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.XMLParsers]
# Desc: XML Parsing Library - ConfigParser Class
# File name: ConfigParser.py
# Developed by: Project Eden Development Team
# Date: 17/06/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench Limited
# ---------------------------------------------
from XParser import XParser
# ---------------------------------------------
# Class definition for the ConfigParser class
# ---------------------------------------------
class ConfigParser(XParser):
    " Extends XParser for configuration parsers "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        XParser.__init__(self) # ancestral constructor
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def getSectionValues(self, tagID, tagValue, tagName = 'Name'):
        " get list of values from a config.xml section via getSection "
        # get the section
        XParser.getSection(self, tagID, tagValue, tagName)
        # make values key from the section tagValue
        t_y = tagValue + '_Values'
        # generate the section key
        t_j = tagID + '_' + tagName + '_' + tagValue
        # get the section values
        self.getPrefixValues(self.Parser['XML_Sections'][t_j], t_y)
    def getPrefixValues(self, XMLsection, sectionName, baseTagID = 'value', \
        tagName = 'valueName'):
        " get list of type-ified values from a config.xml parsed section "
        # the section's values must all have the same baseTagID and tagName!
        # prefix b for boolean, f for float, i for integer, and no prefix for
        # normal string
        t_b = 'b' + baseTagID
        t_f = 'f' + baseTagID
        t_i = 'i' + baseTagID
        # get children
        sectionTree = XMLsection.getElementsByTagName(baseTagID)
        bSectionTree = XMLsection.getElementsByTagName(t_b)
        fSectionTree = XMLsection.getElementsByTagName(t_f)
        iSectionTree = XMLsection.getElementsByTagName(t_i)
        # fill each name:value pair into a dictionary
        self.Parser['XML_Values'][sectionName] = {}
        for t_t in sectionTree:
            self.Parser['XML_Values'][sectionName][t_t.attributes[tagName].value] \
                = t_t.firstChild.data
        if bSectionTree != None:
            for t_k in bSectionTree:
                # 0 is False and <non-zero> is True; 1 would be a strong
                # convention but we allow anything else
                if int(t_k.firstChild.data) == 0:
                    self.Parser['XML_Values'][sectionName][t_k.attributes[tagName].value] \
                    = False
                else:
                    self.Parser['XML_Values'][sectionName][t_k.attributes[tagName].value] \
                    = True
        if fSectionTree != None:
            for t_k in fSectionTree:
                self.Parser['XML_Values'][sectionName][t_k.attributes[tagName].value] \
                    = float(t_k.firstChild.data)
        if iSectionTree != None:
            for t_l in iSectionTree:
                self.Parser['XML_Values'][sectionName][t_l.attributes[tagName].value] \
                    = int(t_l.firstChild.data)
# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.XMLParsers]
# Desc: XML Parsing Library - XParser Class
# File name: XParser.py
# Developed by: Project Eden Development Team
# Date: 28/05/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench Limited
# ---------------------------------------------
from xml.dom import minidom
# ---------------------------------------------
# Class definition for the XParser class
# ---------------------------------------------
class XParser:
    " Base class for all XML parsers "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        # initialize parser dictionary
        # ------------------------NOTES-------------------------------
        # the dictionary has the structure below:
        # XML_Content holds the entire file
        # Section_Lists holds lists identified by tagID
        # XML_Sections holds unique sections by tagID_tagName_tagValue
        # XML_Values holds unique value lists by argued name
        # ------------------------NOTES-------------------------------
        self.Parser = {'Section_Lists':{}, 'XML_Sections':{}, 'XML_Values':{}}
        self.LoadedFlag = False
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def parseFile(self, fileName):
        " parses an XML file into a file-like object "
        # load the xml file and parse
        self.Parser['XML_Content'] = minidom.parse(fileName)
        self.LoadedFlag = True
    # ------------------------NOTES-------------------------------
    # using the example <section Name = "About"> we can define:
    #   tagID     ==>     section
    #   tagName   ==>     Name
    #   tagValue  ==>     About
    # ------------------------NOTES-------------------------------
    def getSectionList(self, tagID):
        " returns a list of all XML sections having the tagID given "
        if self.LoadedFlag == False:
            # the file must be loaded
            return False
        else:
            # the file is loaded
            # we store the result in a key tagID
            self.Parser['Section_Lists'][tagID] = \
            self.Parser["XML_Content"].getElementsByTagName(tagID)
    def getSection(self, tagID, tagValue, tagName = 'Name'):
        " returns a single XML section matching the 3 tag components "
        # the tagID-tagName-tagValue combination must be unique in the file!
        # since getSectionList checks for loading we can skip that
        t_b = self.getSectionList(tagID)
        if t_b == False:
            # the file was not loaded
            return False
        else:
            # the file is loaded
            t_p = self.Parser['Section_Lists'][tagID]
            # search for the tagValue requested
            for x in t_p:
                # the section must have the given tagName
                if tagName in x.attributes:
                    t_a = x.attributes[tagName]
                    if t_a.value == tagValue:
                        # the tagValue was found
                        # create a unique key
                        t_s = tagID + '_' + tagName + '_' + tagValue
                        self.Parser['XML_Sections'][t_s] = x
                        break
            else:
                # the tagValue does not exist
                return False
            return True
    def getValues(self, XMLsection, sectionName, tagID = 'value', \
        tagName = 'valueName'):
        " get list of values from a config.xml parsed section "
        # the section's values must all have the same tagID and tagName!
        # get children
        sectionTree = XMLsection.getElementsByTagName(tagID)
        # fill each name:value pair into a dictionary
        self.Parser['XML_Values'][sectionName] = {}
        for t_t in sectionTree:
            self.Parser['XML_Values'][sectionName][t_t.attributes[tagName].value] \
                = t_t.firstChild.data
    # beyond this, each parser does it's own magic
        
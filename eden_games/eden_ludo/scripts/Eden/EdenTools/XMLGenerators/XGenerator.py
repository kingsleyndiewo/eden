# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.XMLGenerators]
# Desc: XML Generating Library - XGenerator Class
# File name: XGenerator.py
# Developed by: Project Eden Development Team
# Date: 08/05/2009
# Place: Nairobi, Kenya
# Copyright: (C)2009 Funtrench PLC
# ---------------------------------------------
from xml.dom.minidom import Document, Node
# ---------------------------------------------
# Class definition for the XGenerator class
# ---------------------------------------------
class XGenerator:
    " Base class for all XML generators "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self): # constructor
        # initialize the minidom document and the elements dictionary
        self.XMLDocument = Document()
        self.elementStore = {'baseElement':None, 'sections':{}}
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def createBase(self, baseName, topLevelComments = False, commentList = None):
        " creates the outermost XML element "
        # append comments at the top if present
        if topLevelComments == True:
            self.createTopLevelComments(commentList)
        self.elementStore['baseElement'] = self.XMLDocument.createElement(baseName)
        self.XMLDocument.appendChild(self.elementStore['baseElement'])
    def createSection(self, tagID, tagName, tagValue, appendToBase = True, parent = None):
        " creates the section <tagID tagName = tagValue> "
        self.elementStore['sections'][tagValue] = self.XMLDocument.createElement(tagID)
        self.elementStore['sections'][tagValue].setAttribute(tagName, tagValue)
        if appendToBase == True:
            # the section belongs just one level below base
            self.elementStore['baseElement'].appendChild(self.elementStore \
                ['sections'][tagValue])
        else:
            # the section is nested in another section
            self.elementStore['sections'][parent].appendChild(self.elementStore \
                ['sections'][tagValue])
    def createValue(self, tagID, tagName, tagValue, data, parent):
        " creates a value <tagID tagName = tagValue>Data</tagID> under the given parent "
        t_Val = self.XMLDocument.createElement(tagID)
        t_Val.setAttribute(tagName, tagValue)
        # all values are in Unicode
        data = u"" + data
        t_Data = self.XMLDocument.createTextNode(data)
        t_Val.appendChild(t_Data)
        # add to required section
        self.elementStore['sections'][parent].appendChild(t_Val)
    def createSectionWithValues(self, tagID, tagName, tagValue, valueList, appendToBase = \
        True, parent = None):
        " creates a section and fills with the values "
        # create the section
        self.createSection(tagID, tagName, tagValue, appendToBase, parent)
        # add values
        for t_x in valueList:
            # add value t_x = [tagID, tagName, tagValue, data]
            self.createValue(t_x[0], t_x[1], t_x[2], t_x[3], tagValue)
    def createTopLevelComments(self, commentList):
        " creates top level comments in order of list "
        if commentList != None:
            for t_c in commentList:
                # add comment
                t_Cmt = self.XMLDocument.createComment(t_c)
                self.XMLDocument.appendChild(t_Cmt)
        else:
            pass
    def createSectionComment(self, commentString, section):
        " creates a comment and parents it to the named section "
        # create comment
        t_Cmt = self.XMLDocument.createComment(commentString)
        self.elementStore['sections'][section].appendChild(t_Cmt)
    def printFile(self, tabWidth = '\t'):
        " outputs the generated XML to screen with specified indent "
        print self.XMLDocument.toprettyxml(indent = tabWidth)
    def generateXMLFile(self, fileName, tabWidth = '    '):
        " saves the generated XML to file "
        # use ordinary file I/O method
        t_f = open(fileName, 'w')
        # write the header and a newline
        t_f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        # write the child nodes
        for t_node in self.XMLDocument.childNodes:
            t_node.writexml(t_f, tabWidth, tabWidth, '\n')
        t_f.close()
    # ------------------SERVICE METHODS-------------------
    # ----------------------------------------------------
    # The various Node Types are defined as:
        #   ELEMENT_NODE                = 1
        #   ATTRIBUTE_NODE              = 2
        #   TEXT_NODE                   = 3
        #   CDATA_SECTION_NODE          = 4
        #   ENTITY_REFERENCE_NODE       = 5
        #   ENTITY_NODE                 = 6
        #   PROCESSING_INSTRUCTION_NODE = 7
        #   COMMENT_NODE                = 8
        #   DOCUMENT_NODE               = 9
        #   DOCUMENT_TYPE_NODE          = 10
        #   DOCUMENT_FRAGMENT_NODE      = 11
        #   NOTATION_NODE               = 12
    def isCommentNode(self, testNode):
        " returns true if the node is a comment node "
        if testNode.nodeType == Node.COMMENT_NODE:
            return True
        else:
            return False
    def isTextNode(self, testNode):
        " returns true if the node is a text node "
        if testNode.nodeType == Node.TEXT_NODE:
            return True
        else:
            return False
    # from this point each generator does its own magic
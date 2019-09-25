# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.SessionStudio]
# Desc: Session Studio Library - SessionRecorder Class
# File name: ConfigParser.py
# Developed by: Project Eden Development Team
# Date: 23/08/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from SessionBase import SessionBase, Filename
# ---------------------------------------------
# Class definition for the SessionRecorder class
# ---------------------------------------------
class SessionRecorder(SessionBase):
    " Extends SessionBase for session recorders "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, mouseWatcherNode): # constructor
        SessionBase.__init__(self, mouseWatcherNode) # ancestral constructor
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def recordSession(self, sessionFile):
        " records the session to a file "
        self.sessionRecorder.beginRecord(Filename.fromOsSpecific(sessionFile))
    def stopRecording(self):
        if self.sessionRecorder.isRecording():
            # stop the recorder
            self.sessionRecorder.close()
    def getStatus(self):
        # return recording status
        return self.sessionRecorder.isRecording()
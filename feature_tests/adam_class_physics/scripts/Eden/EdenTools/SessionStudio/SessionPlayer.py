# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.SessionStudio]
# Desc: Session Studio Library - SessionPlayer Class
# File name: SessionPlayer.py
# Developed by: Project Eden Development Team
# Date: 23/08/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Funtrench Limited
# ---------------------------------------------
from SessionBase import SessionBase, Filename
# ---------------------------------------------
# Class definition for the SessionRecorder class
# ---------------------------------------------
class SessionPlayer(SessionBase):
    " Extends SessionBase for session players "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, mouseWatcherNode): # constructor
        SessionBase.__init__(self, mouseWatcherNode) # ancestral constructor
    # ------------------BEHAVIOURS------------------------
    # ----------------------------------------------------
    def playSession(self, sessionFile):
        " plays the session from a file "
        self.sessionRecorder.beginPlayback(Filename.fromOsSpecific(sessionFile))
    def getStatus(self):
        # return playing status
        return self.sessionRecorder.isPlaying()
    def getTimeStamp(self):
        " gets the date and time of original recording (seconds) "
        return self.sessionRecorder.getStartTime()
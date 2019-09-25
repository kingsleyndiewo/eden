# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [Eden3D.Simulators.Outdoor]
# Desc: Simulators Library - Motor Class
# File name: Motor.py
# Developed by: Project Eden Development Team
# Date: 30/07/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
from Eden.Eden3D.Worlds.Eve import Eve
# ---------------------------------------------
# A class that implements a basic race car
# simulator with capacity for loading cars.
# Entry point for a racing car game.
# Startup options are loaded from config.xml
# Class definition for the Motor class
# ---------------------------------------------
class Motor(Eve):
    " Extends Eve class for race car simulators "
    # ------------------CONSTRUCTOR------------------------
    # ----------------------------------------------------
    def __init__(self, remoteStarterTask = None, customPRC = None, edenClass = 'Motor'):
        # we want Eve's features without the picker system
        Eve.__init__(self, remoteStarterTask, True, customPRC, edenClass) # ancestral constructor
        
    # ------------------PUBLIC BEHAVIOURS-----------------
    # ----------------------------------------------------
    
    # ------------------SYSTEM SERVICES-----------------
    # ----------------------------------------------------
    
    # ------------------TASKS-----------------
    # ----------------------------------------------------
    
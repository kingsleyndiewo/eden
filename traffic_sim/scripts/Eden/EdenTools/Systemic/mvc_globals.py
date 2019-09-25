# Package Description: Funtrench's Eden 3D Development Framework
# Name: Funtrench Eden [EdenTools.Systemic]
# Desc: System Library - global defines for the MVC class 
# File name: mvc_globals.py
# Developed by: Project Eden Development Team
# Date: 16/06/2008
# Place: Nairobi, Kenya
# Copyright: (C)2008 Intellect Alliance
# ---------------------------------------------
# module defines
NO_EXIST = 'Not Found'
# ---------------------------------------------
# the top-level directories under root (must exist)
mvc_dirs = ['resources', 'scripts', 'config']
# the directories in the resources lower tiers (not vital)
# we build the paths for convenience
mvc_resourceTier = ['images', 'models', 'sound', 'text', 'video']
mvc_modelsTier = ['actors', 'geometry']
mvc_soundsTier = ['effects', 'music']
mvc_textTier = ['fonts']
# vital files (must exist)
# we store a tuple of (dir, file) for each
mvc_files = [('scripts', 'main.py'), ('config', 'config.xml')]
Place your Python souce tree here.

:prc(warning): changing default value for ConfigVariable win-origin from '' to '-1 -1'.
:prc(warning): changing default value for ConfigVariable window-title from 'Panda' to 'Eden 3D System'.
:prc(warning): changing default value for ConfigVariable fullscreen from '0' to '1'.
:prc(warning): changing default value for ConfigVariable audio-library-name from 'null' to 'p3openal_audio'.
:prc(warning): changing default value for ConfigVariable load-display from 'pandagl' to '*'.
Known pipe types:
  glxGraphicsPipe
(all display modules loaded.)
:pnmimage:png(warning): iCCP: known incorrect sRGB profile
:pnmimage:png(warning): iCCP: known incorrect sRGB profile
:pnmimage:png(warning): iCCP: known incorrect sRGB profile
:ffmpeg(warning): Estimating duration from bitrate, this may be inaccurate
Traceback (most recent call last):
  File "/windows/metro/Code Factory/Eden/feature_tests/creation_class/scripts/Eden/Eden3D/Worlds/Creation.py", line 1301, in worldClockTask
:task(
    t_ist = int(time())
NameError: name 'long' is not defined
Traceback (most recent call last):
  File "/windows/metro/Code Factory/Eden/feature_tests/creation_class/scripts/main.py", line 16, in <module>
    main()
  File "/windows/metro/Code Factory/Eden/feature_tests/creation_class/scripts/main.py", line 14, in main
    base.run()
  File "/usr/local/lib/python3.7/dist-packages/direct/showbase/ShowBase.py", line 3124, in run
    self.taskMgr.run()
  File "/usr/local/lib/python3.7/dist-packages/direct/task/Task.py", line 531, in run
error): Exception occurred in PythonTask edenTimeTask
    self.step()
  File "/usr/local/lib/python3.7/dist-packages/direct/task/Task.py", line 485, in step
    self.mgr.poll()
  File "/windows/metro/Code Factory/Eden/feature_tests/creation_class/scripts/Eden/Eden3D/Worlds/Creation.py", line 1301, in worldClockTask
    t_ist = int(time())
NameError: name 'long' is not defined

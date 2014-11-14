RealTimeSpringMaya
==================

Realtime Spring , a similar tool in 3ds max developed by Harrison Yu .

How to Use:
Drag the "scripts/RealTimeSpring.mel" into maya or make button of it.

UI is written in .net ( the installer will automatically copy "clr.pyd"
and "Python.Runtime.dll" into maya script folder)

this script require the mll plug in the MXSController folder ( the
folder also contains source code ). the plug in simulate the max script
controller does , which evaluate python code each system tick no matter
user or time changes any value .

Note . this script system not been massively test . may cause problem
during network render . please use your own risk .

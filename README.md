RealTimeSpringMaya
==================

Realtime Spring , a similar tool in 3ds max developed by Harrison Yu .

How to Use:
Drag the "RealTimeSpring/scripts/RealTimeSpring.mel" into maya or make button of it.

UI is written in .net
(
  the installer will automatically copy "clr.pyd"
  and "Python.Runtime.dll" into maya script folder 
  Fixed problem : forgot to upload Python.Runtime.dll

  if you want to compile your own python pyd corrisponding to older maya version ,
  please go to https://github.com/pythonnet/pythonnet.
  in project setting change the python version . i.e. PYTHON2_4
)

this script require the mll plug in the MXSController folder ( the
folder also contains source code ). the plug in simulate the max script
controller does , which evaluate python code each system tick no matter
user or time changes any value .

Note . this script system not been massively test . may cause problem
during network render . please use it at your own risk .

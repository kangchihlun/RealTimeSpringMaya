import maya.cmds as cmds
cmds.NewScene()

cmds.unloadPlugin("Kang_SimpExpNode")
cmds.loadPlugin("Kang_SimpExpNode")


def createRTTNode(sel,root): #root 應該為 rig root #root='sphere1' sel='locator1'
	ScriptNode = cmds.createNode('Kang_SimpExpNode')
	RttTractor_S = cmds.createNode('renderSphere')
	RttTractor = cmds.listRelatives(RttTractor_S,parent=True)[0]

	# 測試動態Attr連結
	# Input
	cmds.addAttr(ScriptNode,ln='TX',at="float")
	cmds.addAttr(ScriptNode,ln='TY',at="float")
	cmds.addAttr(ScriptNode,ln='TZ',at="float")

	cmds.addAttr(ScriptNode,ln='RX',at="float")
	cmds.addAttr(ScriptNode,ln='RY',at="float")
	cmds.addAttr(ScriptNode,ln='RZ',at="float")

	# Input Connection
	cmds.connectAttr((root+'.tx'),(ScriptNode+'.TX'))
	cmds.connectAttr((root+'.ty'),(ScriptNode+'.TY'))
	cmds.connectAttr((root+'.tz'),(ScriptNode+'.TZ'))

	cmds.connectAttr((root+'.rx'),(ScriptNode+'.RX'))
	cmds.connectAttr((root+'.ry'),(ScriptNode+'.RY'))
	cmds.connectAttr((root+'.rz'),(ScriptNode+'.RZ'))

	# OutPut
	cmds.addAttr(ScriptNode,ln='XOut',at="float")
	cmds.addAttr(ScriptNode,ln='YOut',at="float")
	cmds.addAttr(ScriptNode,ln='ZOut',at="float")

	# Output Connection
	cmds.connectAttr((ScriptNode+'.XOut'),(RttTractor+'.translateX'))
	cmds.connectAttr((ScriptNode+'.YOut'),(RttTractor+'.translateY'))
	cmds.connectAttr((ScriptNode+'.ZOut'),(RttTractor+'.translateZ'))

	#TargetLocator recognizing
	if(not cmds.objExists(sel+'.Rec')):
		cmds.addAttr(sel,ln='Rec',at="float")
	cmds.addAttr(ScriptNode,ln='Rec',at="float")
	cmds.connectAttr((sel+'.Rec'),(ScriptNode+'.Rec'))

	# In Out Pairing
	cmds.setAttr((ScriptNode+'.inAttrNameArr'),"TX;TY;TZ;RX;RY;RZ",type="string")
	cmds.setAttr((ScriptNode+'.outAttrNameArr'),"XOut;YOut;ZOut",type="string")

	# RealTime Spring Parameters
	cmds.addAttr(ScriptNode,ln='v',dt="double3")
	cmds.setAttr((ScriptNode+'.v'), 0,0,0,type="double3")
	cmds.addAttr(ScriptNode,ln='cValue',dt="double3")
	cmds.setAttr((ScriptNode+'.cValue'), 0,0,0,type="double3")
	cmds.addAttr(ScriptNode,ln='sf',at="float")
	cmds.setAttr((ScriptNode+'.sf'), 3.0)
	cmds.addAttr(ScriptNode,ln='df',at="float")
	cmds.setAttr((ScriptNode+'.df'), 0.3)
	cmds.addAttr(ScriptNode,ln='oldTime',at="float")
	cmds.setAttr((ScriptNode+'.oldTime'), 0.0)

	# set py import cmd
	pyth='D:/05Py/NMAAssetToolSet/RealTimeSpring/script/RTS_Cmd_Import.py'
	f=open(pyth,'r')
	pycmdstr=''
	line =f.readline()
	pycmdstr +=line
	while(line!=''):
		line=f.readline()
		pycmdstr += line
	f.close()
	cmds.setAttr((ScriptNode+'.pyImportCmd'),pycmdstr,type="string")

	# set py cmd
	pyth='D:/05Py/NMAAssetToolSet/RealTimeSpring/script/RTS_Cmd.py'
	f=open(pyth,'r')
	pycmdstr=''
	line =f.readline()
	pycmdstr +=line
	while(line!=''):
		line=f.readline()
		pycmdstr += line
	f.close()
	cmds.setAttr((ScriptNode+'.pyCmd'),pycmdstr,type="string")

sp = cmds.createNode('renderSphere')
cmds.createNode('locator')
cmds.parent('locator1','sphere1')
cmds.select('sphere1')
createRTTNode(cmds.ls(sl=True,type='transform')[0],'sphere1')
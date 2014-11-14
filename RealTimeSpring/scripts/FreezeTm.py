# -*- coding: utf-8 -*-

import maya.cmds as cmds
def setAttrToZero(_objS):
	_trAttr =('.tx', '.ty', '.tz', '.rx', '.ry', '.rz')
	_sAttr =('.sx', '.sy', '.sz')
	for j in range(6):
		cmds.setAttr(_objS+_trAttr[j], 0)
	for k in range(3):
		cmds.setAttr(_objS+_sAttr[k], 1)

def FreezeTm(_zeroObj):
	_grpName = cmds.group(em=True, name=_zeroObj+'_zeroGrp#')
	cmds.parent(_grpName, _zeroObj) 
	setAttrToZero(_grpName)
	_parentObj = cmds.listRelatives(_zeroObj, p=True)
	try:
		cmds.parent(_grpName, _parentObj)
		cmds.parent(_zeroObj, _grpName)
	except:    
		cmds.parent(_grpName, w=True)
		cmds.parent(_zeroObj, _grpName)
	return _parentObj

def FreezeJntRotation():
	sel=cmds.ls(sl=1)
	n=len(sel)
	for i in range(0,n):
		tm=cmds.xform(sel[i],q=1,ws=1,m=1)
		order=cmds.xform(sel[i],q=1,roo=1)
		cmds.xform(sel[i],ws=1,roo='xyz',m=tm)
		rot=cmds.xform(sel[i],q=1,ro=1)
		cmds.joint(sel[i],e=1,roo=order,o=rot)
		cmds.xform(sel[i],ro=[0,0,0])
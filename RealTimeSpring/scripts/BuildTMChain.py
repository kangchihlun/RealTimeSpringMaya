# -*- coding: utf-8 -*-
# Last Modified 2014/01/01
# Author Chih Lun Kang

import maya.cmds as cmds
import maya.mel as mm
import FreezeTm
import __builtin__
import maya.OpenMaya as om
reload(RealTimeSpring)
curSel = cmds.ls(sl=True,type='joint')
if(len(curSel)):
	curSel=curSel[0]

# 製作之前，檢查joint有否link
prevParent=None
prevParent = cmds.listRelatives(curSel,parent=True)
if(prevParent):
	prevParent=prevParent[0]
cmds.parent(curSel,w=True)

#產生主控制器
mainCtrl_sp = cmds.createNode('renderSphere')
mainCtrl_orig = cmds.listRelatives(mainCtrl_sp,parent=True)[0]
mainCtrl = (curSel+'_spCtrl')

cmds.rename(mainCtrl_orig,mainCtrl)
cmds.xform(mainCtrl,m=(cmds.xform( curSel,q=True, m=True ,ws=True)),ws=True)
FreezeTm.FreezeTm(mainCtrl)
cmds.pointConstraint(curSel,mainCtrl)
cmds.setAttr(mainCtrl+".tx",lock=True)
cmds.setAttr(mainCtrl+".ty",lock=True)
cmds.setAttr(mainCtrl+".tz",lock=True)
cmds.setAttr(mainCtrl+".sx",lock=True)
cmds.setAttr(mainCtrl+".sy",lock=True)
cmds.setAttr(mainCtrl+".sz",lock=True)

# 產生spring bone
curChain=[curSel]
allChild = cmds.listRelatives(curSel,ad=True)
spTmChain=[]
spTargChain=[]
springNdCol=[]
spFkTmChain=[]
orientConstNdCol=[]
curChain.extend(allChild)
for jnt in curChain:
	dupTM = cmds.createNode('transform',n=(jnt+'_sprb'))
	cmds.xform(dupTM,m=(cmds.xform(jnt,q=True,m=True,ws=True)),ws=True)
	cmds.setAttr(dupTM+".displayHandle",1)
	spTmChain.append(dupTM)
for k in range(0,len(spTmChain)):#k=0
	_p = cmds.listRelatives(curChain[k],parent=True)
	if(_p):
		_p = _p[0]
		sp = _p+'_sprb'
		if(cmds.objExists(sp)):
			cmds.parent(spTmChain[k],sp)
	else:
		cmds.parent(spTmChain[k],mainCtrl)


# 產生Tractor Set
for k in range(0,len(allChild)):#k=0
	tractTarg_shp = cmds.createNode('renderBox')
	tractTarg_orig = cmds.listRelatives(tractTarg_shp,parent=True)[0]
	tractTarg = (allChild[k]+'_sprt')
	cmds.rename(tractTarg_orig ,tractTarg)
	cmds.setAttr(tractTarg+'.size',0.1,0.1,0.1)
	cmds.xform(tractTarg,m=(cmds.xform(allChild[k],q=True,m=True,ws=True)),ws=True)
	rtsN = __builtin__.g_RTSROInstance.createRTTNode(tractTarg,chainIdx=k,chainRoot=mainCtrl,sf=3.0,df=0.3)
	springNdCol.append(rtsN)
	spTargChain.append(tractTarg)

for tar in spTargChain:#tar=spTargChain[0]
	targ=tar[:-1]+'b'
	springNd=tar+'_sprn'
	_p = cmds.listRelatives(targ,parent=True)
	if(_p):
		_p_p = cmds.listRelatives(_p,parent=True)
		if(_p_p):
			# AimConst
			cmds.aimConstraint(springNd,_p,wuo=_p_p[0],u=[-1,0,0])
			# Parent
			cmds.parent(tar,_p_p[0])

# group sorting
mot='MotionSystem'
if(not cmds.objExists('MotionSystem')):
	mot = cmds.group(em=True,n="MotionSystem")
	cmds.setAttr("MotionSystem.tx",lock=True)
	cmds.setAttr("MotionSystem.ty",lock=True)
	cmds.setAttr("MotionSystem.tz",lock=True)
	cmds.setAttr("MotionSystem.rx",lock=True)
	cmds.setAttr("MotionSystem.ry",lock=True)
	cmds.setAttr("MotionSystem.rz",lock=True)
	cmds.setAttr("MotionSystem.sx",lock=True)
	cmds.setAttr("MotionSystem.sy",lock=True)
	cmds.setAttr("MotionSystem.sz",lock=True)
for sp in springNdCol:
	cmds.parent(sp,mot)
	
# FK setting
for bo in curChain:
	boxShp=cmds.curve( degree = 1,\
	knot = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],\
	point = [(-0.5, 1, -0.5),\
			 (-0.5, 1, 0.5),\
			 (0.5, 1, 0.5),\
			 (0.5, 1, -0.5),\
			 (-0.5, 1, -0.5),\
			 (-0.5, 0, -0.5),\
			 (-0.5, 0, 0.5),\
			 (0.5,0, 0.5),\
			 (0.5, 1, 0.5),\
			 (-0.5, 1, 0.5),\
			 (-0.5, 0, 0.5),\
			 (-0.5, 0, -0.5),\
			 (0.5, 0, -0.5),\
			 (0.5, 1, -0.5),\
			 (0.5, 1, 0.5),\
			 (0.5, 0, 0.5),\
			 (0.5, 0, -0.5)]\
	,n=(bo+'_FK')
	)
	
	cmds.makeIdentity(boxShp,apply=True)
	xScale = cmds.getAttr(bo+".radius")
	yScale = xScale
	zScale = xScale
	_child = cmds.listRelatives(bo,c=True)
	if(_child):
		childPos= cmds.xform(_child[0],q=True,t=True,ws=True)
		thisPos = cmds.xform(bo,q=True,t=True,ws=True)
		childPos_om = om.MVector(childPos[0],childPos[1],childPos[2])
		thisPos_om = om.MVector(thisPos[0],thisPos[1],thisPos[2])
		dist=childPos_om-thisPos_om
		yScale = dist.length()
	cmds.setAttr(boxShp+'.sx',xScale)
	cmds.setAttr(boxShp+'.sy',yScale)
	cmds.setAttr(boxShp+'.sz',zScale)
	cmds.setAttr(boxShp+'.rz',-90)
	cmds.makeIdentity(boxShp,apply=True)
	# 設定matrix
	cmds.xform(boxShp,m=(cmds.xform(bo,q=True,m=True,ws=True)),ws=True)
	spFkTmChain.append(boxShp)

for k in range(0,len(curChain)):
	_p = cmds.listRelatives(curChain[k],p=True)
	if(_p):
		t_p = _p[0]+'_FK'
		if(cmds.objExists(t_p)):
			cmds.parent(spFkTmChain[k],t_p)

for fkb in spFkTmChain:
	if(not(cmds.listRelatives(fkb,p=True))):
		cmds.parent(fkb,mainCtrl)

for ch in spFkTmChain:
	FreezeTm.FreezeTm(ch)

# Orig Bone Orient Between FK&Spring
for i in range(0,len(spTmChain)):
	jnt = ((spTmChain[i]).split('_sprb'))[0]
	if(cmds.objExists(jnt)):
		ornd = cmds.orientConstraint(spTmChain[i],spFkTmChain[i],jnt)
		if(ornd):
			if(cmds.objExists(ornd[0])):
				orientConstNdCol.append(ornd[0])


# blendWeight
cmds.addAttr(mainCtrl,ln='FK_Spr',at="float",maxValue=1.0, minValue=0.0)
reversend = cmds.createNode('reverse',n=(curSel+'_revr'))
cmds.connectAttr(mainCtrl+".FK_Spr",reversend+'.inputX')


for oric in orientConstNdCol:
	allattr = cmds.listAttr(oric)
	aw0=allattr[-1]
	aw1=allattr[-2]
	cmds.connectAttr(mainCtrl+".FK_Spr",oric+'.'+aw0)
	cmds.connectAttr(reversend+".outputX",oric+'.'+aw1)

# Joint Link 回去，如果有parent
if(cmds.objExists(prevParent)):
	cmds.parent(curSel,prevParent)

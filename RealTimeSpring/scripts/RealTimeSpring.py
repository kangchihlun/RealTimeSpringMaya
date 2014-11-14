# -*- coding: utf-8 -*-
# Last Modified 2013/12/27
# Author Chih Lun Kang
'''
		RealTime Spring in Maya 
		概念完全繼承max版 RealTime Spring
	
'''
import sys,os
import __builtin__
import copy
import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as om
try:import clr 
except:pass

if(clr):
	clr.AddReference("System")
	clr.AddReference("System.Drawing")
	clr.AddReference("System.Windows.Forms")
	import System
	import System.Drawing
	import System.Windows.Forms
	from DotNet import WinForms
	reload(WinForms)
import FreezeTm

def enum(**enums):
	return type('Enum', (), enums)

class Container():
	def __init__(self,_node):
		self.node = _node

def getParentRecursive(_node_ , _type_ , rt):
	_parent = (cmds.listRelatives(_node_,p=True,type=_type_))
	if(not _parent):
		rt.node = _node_
	else:
		getParentRecursive(_parent[0] , _type_ , rt)



class RTSROWin():
	def __init__(self,ToolRoot):
		self.thisScrptRoot = ToolRoot
		self.onRefreshUI()
		__builtin__.g_RTSROInstance = self
		try:__builtin__.g_RTSROWin.TopMost=True
		except:pass
		self.curSelIdx=0 # 當前選中的
		self.AddSceneScriptJob()
	def createUI_MainFrame(self):
		#####################################################################################
		################################      Main UI      ##################################
		#####################################################################################
		_size=[352,352]#734/2
		__builtin__.g_RTSROWin = WinForms.GUI(cls='Form',size=_size,
				text="Realtime Spring Maya by Kang")#(http://kangchihlun.byethost18.com/)
		self.Form = __builtin__.g_RTSROWin
		self.Form.Show()

		# Skeletal Tool 分頁：設置骨架
		self.panel1 = WinForms.GUI(cls='Panel',size=_size,pos=[0,0] ,p=self.Form)
		# SpringList
		self.SpringList = WinForms.GUI(cls='ListView',size=[334,200],pos=[8,70],p=self.panel1)
		self.initListView(self.SpringList)
		
		self.btnAddPos = WinForms.GUI(cls='Button',size=[80,20],pos=[16,16],text="Build Single",p=self.panel1)
		#self.btnRescan = WinForms.GUI(cls='Button',size=[88,20],pos=[240,43],text="Rescan",p=self.panel1)
		self.btnMakeChain = WinForms.GUI(cls='Button',size=[80,20],pos=[16,40],text='Build Chain',p=self.panel1)
		#self.btnRmCur = WinForms.GUI(cls='Button',size=[90,20],pos=[240,40],text='Remove Chain',p=self.panel1)
		
		self.spnSprFac = WinForms.GUI(cls='Spinner',size=[56,2],range=[0,10,3.0],pos=[152,16],scale=2,p=self.panel1)
		self.spnDmpFac = WinForms.GUI(cls='Spinner',size=[56,2],range=[0,1.333,0.3],pos=[152,40],scale=2,p=self.panel1)
		self.spnWFac = WinForms.GUI(cls='Spinner',size=[56,2],range=[0,1.0,0.0],pos=[270,16],scale=2,p=self.panel1)
		
		lbl1 = WinForms.GUI(cls='Label',size=[40,16],pos=[220,16],text='Weight',p=self.panel1)
		lbl3 = WinForms.GUI(cls='Label',size=[40,16],pos=[104,16],text='Spring',p=self.panel1)
		lbl4 = WinForms.GUI(cls='Label',size=[48,16],pos=[104,40],text='Damping',p=self.panel1)
		grp1 = WinForms.GUI(cls='GroupBox',size=[334,70],pos=[8,0],text="Make Spring At First Selected Node Position",p=self.panel1)
		
		# 右鍵選單
		self.mnui = System.Windows.Forms.MenuItem("Delete Chain")
		self.fillInSpreadSheet(self.SpringList)
	def onRefreshUI(self):
		if(clr):
			try:
				__builtin__.g_RTSROWin.Close()
			except:
				pass
			self.createUI_MainFrame()
			self.ConnectEvents()
	def initListView(self,lv):#
		lv.BackColor = System.Drawing.Color.Green
		lv.ForeColor = System.Drawing.Color.White
		
		lv.GridLines = True  
		lv.View = System.Windows.Forms.View.Details 
		lv.MultiSelect =True
		lv.FullRowSelect = True
		
		lv.LabelEdit = True
		lv.AllowColumnReorder =False
		lv.Checkboxes = False
		lv.HideSelection = False
		
		lv.Columns.Add("-",28) 
		lv.Columns.Add("ChainRoot",120)
		lv.Columns.Add("Spring",50)
		lv.Columns.Add("Damp",50)
		lv.Columns.Add("Weight",54)
		lv.Columns.Add("-",32	)

	def fillInSpreadSheet(self,lv):
		lv.Items.Clear()
		# 找場景中的KangSimpNode
		kNdCol=cmds.ls(type='Kang_SimpExpNode')
		__builtin__.sprNdCol=[]
		for k in range(0,len(kNdCol)):
			if(
			    (cmds.objExists(kNdCol[k]+'.chainRoot')) and
			    (cmds.objExists(kNdCol[k]+'.sf')) and 
			    (cmds.objExists(kNdCol[k]+'.df'))
			  ):
				_chainRoot_  = cmds.listConnections(kNdCol[k]+'.chainRoot')[0]
				if((not _chainRoot_ in __builtin__.sprNdCol) and (cmds.objExists(_chainRoot_))):
					__builtin__.sprNdCol.append(_chainRoot_)
					
		for k in range(0,len(__builtin__.sprNdCol)):
			li= System.Windows.Forms.ListViewItem(str(k))
			li.SubItems.Add(__builtin__.sprNdCol[k])
			expNd  = cmds.listConnections( __builtin__.sprNdCol[k]+'.chainRoot',type='Kang_SimpExpNode')[0]
			if(cmds.objExists(expNd)):
				sprVal = round(cmds.getAttr(expNd+'.sf'),4)
				dfVal = round(cmds.getAttr(expNd+'.df'),4)
				wVal = round(cmds.getAttr(__builtin__.sprNdCol[k]+'.FK_Spr'),4)
				li.SubItems.Add(str(sprVal))
				li.SubItems.Add(str(dfVal))
				li.SubItems.Add(str(wVal))
				lv.Items.Add(li)
		
	# Connect Events
	def ConnectEvents(self):
		self.SpringList.MouseDown += self.OnSpringListMouseDown
		self.SpringList.MouseDoubleClick += self.OnSpringListDoubleClk
		self.btnAddPos.Click += self.OnbtnAddPosPressed
		self.btnMakeChain.Click += self.BuildSpChain
		#self.btnRescan.Click += self.onReScanPress
		self.mnui.Click += self.onDelChainPress
		self.spnSprFac.ValueChanged += self.onSprValChanged
		self.spnDmpFac.ValueChanged += self.onDmpValChanged
		self.spnWFac.ValueChanged += self.onWeiValChanged
		self.Form.Closing += self.OnFormClose
	def OnFormClose(self,s,e):
		try:
			cmds.scriptJob(k=self.sjName_Open,f=1)
			cmds.scriptJob(k=self.sjName_New,f=1)
			return
		except:pass

	def OnSpringListMouseDown(self,s,e):
		hit= self.SpringList.HitTest (System.Drawing.Point(e.X,e.Y))
		itm = hit.Item
		if(type(itm)==System.Windows.Forms.ListViewItem):
			self.curSelIdx= int(itm.SubItems[0].Text)
			self.spnSprFac.Value=WinForms.DotNetDecimalProc(float(itm.SubItems[2].Text))
			self.spnDmpFac.Value=WinForms.DotNetDecimalProc(float(itm.SubItems[3].Text))
			self.spnWFac.Value=WinForms.DotNetDecimalProc(float(itm.SubItems[4].Text))
			
		if(e.Button == System.Windows.Forms.MouseButtons.Right):
			mnu = System.Windows.Forms.ContextMenu()
			mnu.MenuItems.Add(self.mnui)
			mnu.Show(s,System.Drawing.Point(e.X, e.Y))

	def OnSpringListDoubleClk(self,s,e):
		info = self.SpringList.HitTest(e.X,e.Y)
		itm = info.Item
		if(type(itm)==System.Windows.Forms.ListViewItem):
			self.curSelIdx= int(itm.SubItems[0].Text)
			MainC = itm.SubItems[1].Text
			if(cmds.objExists(MainC)):
				cmds.select(MainC,r=True)

	def onDelChainPress(self,s,e):
		cMain = self.SpringList.Items[self.curSelIdx].SubItems[1].Text
		if(cmds.objExists(cMain)):
			expNdCol = cmds.listConnections( cMain+'.chainRoot',type='Kang_SimpExpNode')
			if expNdCol:
				for exN in expNdCol:
					sprNode=cmds.listConnections( exN+'.XOut',type='transform')
					if(sprNode):
						for spn in sprNode:
							cmds.delete(spn)
			_mainP = cmds.listRelatives(cMain,p=True)
			if(_mainP):
				cmds.delete(_mainP[0],hi="below")
		self.fillInSpreadSheet(self.SpringList)

	def onReScanPress(self,s,e):
		self.fillInSpreadSheet(self.SpringList)

	def onSprValChanged(self,s,e):
		sprnNdCol=__builtin__.sprNdCol
		if(sprnNdCol):
			if(len(sprnNdCol)):
				curMCt = sprnNdCol[self.curSelIdx]
				expNdCol = cmds.listConnections( curMCt+'.chainRoot',type='Kang_SimpExpNode')
				for ex in expNdCol:
					cmds.setAttr(ex+'.sf',System.Decimal.ToDouble(s.Value))
		# Change UI Text
		self.SpringList.Items[self.curSelIdx].SubItems[2].Text = System.Decimal.ToString(s.Value)

	def onDmpValChanged(self,s,e):
		sprnNdCol=__builtin__.sprNdCol
		if(sprnNdCol):
			if(len(sprnNdCol)):
				curMCt = sprnNdCol[self.curSelIdx]
				expNdCol = cmds.listConnections( curMCt+'.chainRoot',type='Kang_SimpExpNode')
				for ex in expNdCol:
					cmds.setAttr(ex+'.df',System.Decimal.ToDouble(s.Value))
		# Change UI Text
		self.SpringList.Items[self.curSelIdx].SubItems[3].Text = System.Decimal.ToString(s.Value)

	def onWeiValChanged(self,s,e):
		sprnNdCol=__builtin__.sprNdCol
		if(sprnNdCol):
			if(len(sprnNdCol)):
				curMCt = sprnNdCol[self.curSelIdx]
				cmds.setAttr(curMCt+'.FK_Spr',System.Decimal.ToDouble(s.Value))
		# Change UI Text
		self.SpringList.Items[self.curSelIdx].SubItems[4].Text = System.Decimal.ToString(s.Value)

	def findHierarchyRoot(self,obj): # obj='joint9'
		par = Container(obj)
		getParentRecursive(obj ,cmds.nodeType(obj),par)
		return par.node

	def OnbtnAddPosPressed(self,s,e):
		sel=cmds.ls(sl=True,type='transform')
		if(len(sel)):
			sfv=System.Decimal.ToDouble(self.spnSprFac.Value)
			dfv=System.Decimal.ToDouble(self.spnDmpFac.Value)
			self.createRTTNode(sel[0], sf=sfv, df=dfv)

	def AddSceneScriptJob(self):
		if not('sjName' in dir()):
			self.sjName_Open = cmds.scriptJob(e=['SceneOpened','import __builtin__\n__builtin__.g_RTSROInstance.fillInSpreadSheet(__builtin__.g_RTSROInstance.SpringList)'])
			self.sjName_New = cmds.scriptJob(e=['NewSceneOpened','import __builtin__\n__builtin__.g_RTSROInstance.fillInSpreadSheet(__builtin__.g_RTSROInstance.SpringList)'])


	def createRTTNode(self,sel,chainIdx=0,chainRoot=None,sf=3.0,df=0.3): #sel = 'joint4' # sel=None
		ScriptNode = cmds.createNode('Kang_SimpExpNode')
		#RttTractor_S = cmds.createNode('renderSphere')
		#RttTractor = cmds.listRelatives(RttTractor_S,parent=True)[0]
		RttTractor_orig = cmds.createNode('transform')
		RttTractor = (sel+'_sprn')
		cmds.rename(RttTractor_orig,RttTractor)
		#cmds.toggle(RttTractor ,rotatePivot=True)
		cmds.setAttr(RttTractor+".displayHandle",1)
		loc = cmds.xform(sel,q=True,t=True,ws=True)
		
		# 測試動態Attr連結
		# Input
		cmds.addAttr(ScriptNode,ln='TX',at="float")
		cmds.addAttr(ScriptNode,ln='TY',at="float")
		cmds.addAttr(ScriptNode,ln='TZ',at="float")

		cmds.addAttr(ScriptNode,ln='RX',at="float")
		cmds.addAttr(ScriptNode,ln='RY',at="float")
		cmds.addAttr(ScriptNode,ln='RZ',at="float")
		cmds.addAttr(ScriptNode,ln='T',at="float")
		
		# decompose obj'sworld matrix 
		decomp = cmds.createNode('decomposeMatrix')
		cmds.connectAttr( sel+'.worldMatrix',decomp+'.inputMatrix')

		# Input Connection
		cmds.connectAttr((decomp+'.outputTranslateX'),(ScriptNode+'.TX'))
		cmds.connectAttr((decomp+'.outputTranslateY'),(ScriptNode+'.TY'))
		cmds.connectAttr((decomp+'.outputTranslateZ'),(ScriptNode+'.TZ'))

		cmds.connectAttr((decomp+'.outputRotateX'),(ScriptNode+'.RX'))
		cmds.connectAttr((decomp+'.outputRotateY'),(ScriptNode+'.RY'))
		cmds.connectAttr((decomp+'.outputRotateZ'),(ScriptNode+'.RZ'))
		# 時間更新也要通知
		if(cmds.objExists('time1')):
			cmds.connectAttr(('time1.outTime'),(ScriptNode+'.T'))
		
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
			cmds.addAttr(sel,ln='Rec',at="short")
		cmds.addAttr(ScriptNode,ln='Rec',at="short")
		cmds.connectAttr((sel+'.Rec'),(ScriptNode+'.Rec'))
		
		if(chainRoot):
			if(not cmds.objExists(chainRoot+'.chainRoot')):
				cmds.addAttr(chainRoot,ln='chainRoot',at="short")
			cmds.addAttr(ScriptNode,ln='chainRoot',at="short")
			cmds.connectAttr((chainRoot+'.chainRoot'),(ScriptNode+'.chainRoot'))
			
		# 當前的骨節是第幾個
		cmds.setAttr((sel+'.Rec'),chainIdx)
		
		# In Out Pairing
		cmds.setAttr((ScriptNode+'.inAttrNameArr'),"TX;TY;TZ;RX;RY;RZ;T",type="string")
		cmds.setAttr((ScriptNode+'.outAttrNameArr'),"XOut;YOut;ZOut",type="string")

		# RealTime Spring Parameters
		cmds.addAttr(ScriptNode,ln='v',dt="double3")
		cmds.setAttr((ScriptNode+'.v'), 0,0,0,type="double3")
		cmds.addAttr(ScriptNode,ln='cValue',dt="double3")
		cmds.setAttr((ScriptNode+'.cValue'), loc[0],loc[1],loc[2],type="double3")
		cmds.addAttr(ScriptNode,ln='sf',at="float")
		cmds.setAttr((ScriptNode+'.sf'), sf)
		cmds.addAttr(ScriptNode,ln='df',at="float")
		cmds.setAttr((ScriptNode+'.df'), df)
		cmds.addAttr(ScriptNode,ln='oldTime',at="float")
		cmds.setAttr((ScriptNode+'.oldTime'), 0.0)

		# set py import cmd
		pyth=self.thisScrptRoot+'/RTS_Cmd_Import.py'
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
		pyth=self.thisScrptRoot+'/RTS_Cmd.py'
		f=open(pyth,'r')
		pycmdstr=''
		line =f.readline()
		pycmdstr +=line
		while(line!=''):
			line=f.readline()
			pycmdstr += line
		f.close()
		cmds.setAttr((ScriptNode+'.pyCmd'),pycmdstr,type="string")
		return RttTractor

	def BuildSpChain(self,s,e):
		curSel = cmds.ls(sl=True,type='joint')
		if(len(curSel)):
			curSel=curSel[0]
		else:
			return
		#檢查有否Child
		allChild = cmds.listRelatives(curSel,ad=True)
		if(not allChild):
			return
		# 製作之前，檢查joint有否link
		prevParent=None
		prevParent = cmds.listRelatives(curSel,parent=True)
		if(prevParent):
			prevParent=prevParent[0]
		try:cmds.parent(curSel,w=True)
		except:pass

		#產生主控制器
		mainCtrl_sp = cmds.createNode('renderSphere')
		cmds.setAttr(mainCtrl_sp+'.radius',(cmds.getAttr(curSel+'.radius'))*2.5)
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
			sfv=System.Decimal.ToDouble(self.spnSprFac.Value)
			dfv=System.Decimal.ToDouble(self.spnDmpFac.Value)
			rtsN = self.createRTTNode(tractTarg,chainIdx=k,chainRoot=mainCtrl,sf=sfv, df=dfv)
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
		cmds.addAttr(mainCtrl,ln='FK_Spr',at="float",maxValue=1.0, minValue=0.0,k=True)
		reversend = cmds.createNode('reverse',n=(curSel+'_revr'))
		cmds.connectAttr(mainCtrl+".FK_Spr",reversend+'.inputX')


		for oric in orientConstNdCol:
			allattr = cmds.listAttr(oric)
			aw0=allattr[-1]
			aw1=allattr[-2]
			cmds.connectAttr(mainCtrl+".FK_Spr",oric+'.'+aw0)
			cmds.connectAttr(reversend+".outputX",oric+'.'+aw1)

		#print prevParent
		# Joint Link 回去，如果有parent
		if(prevParent):
			if(cmds.objExists(prevParent)):
				try:cmds.parent(curSel,prevParent)
				except:pass
		# 更新 SpringList
		self.fillInSpreadSheet(self.SpringList)
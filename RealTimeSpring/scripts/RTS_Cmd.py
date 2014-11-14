if(True):#this='Kang_SimpExpNode1'
	thisv_at=cmds.getAttr(this+'.v')
	thisv = om.MVector(thisv_at[0][0],thisv_at[0][1],thisv_at[0][2])
	thisdf=cmds.getAttr(this+'.df')
	thiscValue_at=cmds.getAttr(this+'.cValue')
	thiscValue=om.MVector(thiscValue_at[0][0],thiscValue_at[0][1],thiscValue_at[0][2])
	
	targetNode = cmds.listConnections(this+'.Rec')[0]
	targetNodeWS_T = cmds.xform(targetNode,q=True,t=True,ws=True)
	DrvNodepos=om.MVector(targetNodeWS_T[0],targetNodeWS_T[1],targetNodeWS_T[2]) 
	thissf = cmds.getAttr(this+'.sf')
	thisoldTime=cmds.getAttr(this+'.oldTime')
	
	if(not(cmds.play (q=True,state=True))):
		thissf*=0.2
		thisdf*=0.2
	thisv = -thisv*thisdf+(DrvNodepos-thiscValue)*thissf
	cTime= time.time()
	diff = (cTime - thisoldTime)/320.0
	
	
	if(diff<0):
		diff=-diff
	if (diff>0.1):
		diff=0.1
	if math.fabs(thiscValue.x)>=10000:
		thisv.x=0.0
		thisv.y=0.0
		thisv.z=0.0
		thiscValue.x=0.0
		thiscValue.y=0.0
		thiscValue.z=0.0

	thiscValue += thisv*diff
	
	XOut = thiscValue.x
	YOut = thiscValue.y
	ZOut = thiscValue.z
	
	cmds.setAttr(this+'.oldTime',cTime)
	cmds.setAttr(this+'.v',thisv.x,thisv.y,thisv.z,type='double3')
	cmds.setAttr(this+'.cValue',thiscValue.x,thiscValue.y,thiscValue.z,type='double3' )
	_val = (cmds.getAttr(this+'.cValue'))[0][0]


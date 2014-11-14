//
// Copyright (C) Kang
// 
// File: Kang_SimpExpNodeNode.cpp
//
// Dependency Graph Node: Kang_SimpExpNode
//
// Author: Maya Plug-in Wizard 2.0
//

#include "Kang_SimpExpNodeNode.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MGlobal.h>

//using namespace std;
// You MUST change this to a unique value!!!  The id is a 32bit value used
// to identify this type of node in the binary file format.  
//
MTypeId     Kang_SimpExpNode::id( 0x810BC );

// Example attributes
// 
MObject     Kang_SimpExpNode::pyCmd;        
MObject     Kang_SimpExpNode::pyImportCmd;
MObject     Kang_SimpExpNode::inAttrNameArr;
MObject     Kang_SimpExpNode::outAttrNameArr;


Kang_SimpExpNode::Kang_SimpExpNode() 
{
	bPyImpExecuted=false;
}


Kang_SimpExpNode::~Kang_SimpExpNode() 
{
	
}

MStatus Kang_SimpExpNode::addNewInOutPair(MString inAttrName, MString outAttrName)
{
	//if(m_RefTargets.Num())
	//{
	//	int foundRefTargIndx=-1;
	//	 找 outAttrName 有沒有在 m_RefTargets 清單中
	//	for(int k = 0;k<m_RefTargets.Num();k++)
	//	{
	//		if(m_RefTargets[k]->chName == outAttrName)
	//		{
	//			m_RefTargets[k]->nodifiers.append(inAttrName);
	//			foundRefTargIndx = k;
	//		}
	//	}
	//	if(foundRefTargIndx==-1)
	//	{
	//		NotifiedInfo* refTarg = new NotifiedInfo();
	//		refTarg->chName = outAttrName;
	//		refTarg->nodifiers.append(inAttrName);
	//		m_RefTargets.AddItem(refTarg);
	//	}
	//}
	//else
	//{
	//	NotifiedInfo* refTarg = new NotifiedInfo();
	//	refTarg->chName = outAttrName;
	//	refTarg->nodifiers.append(inAttrName);
	//	m_RefTargets.AddItem(refTarg);
	//}


	//Add Out Attr
	int found=-1;
	for(int k = 0;k<m_OutputAttrNames.length();k++)
	{
		if( outAttrName == m_OutputAttrNames[k])
			found =k;
	}
	if(found==-1)
		m_OutputAttrNames.append(outAttrName);

	//Add In Attr
	found=-1;
	for(int k = 0;k<m_InputAttrNames.length();k++)
	{
		if( inAttrName == m_InputAttrNames[k])
			found =k;
	}
	if(found==-1)
		m_InputAttrNames.append(outAttrName);
	return MS::kSuccess;
}


MStatus Kang_SimpExpNode::removeInOutPair(MString inAttrName, MString outAttrName)
{
	//for(int k = 0;k<m_RefTargets.Num();k++)
	//{
	//	if(m_RefTargets[k]->chName == outAttrName)
	//	{
	//		int fndIdx=-1;
	//		for(int j = 0;j<m_RefTargets[k]->nodifiers.length();j++)
	//		{
	//			if(m_RefTargets[k]->nodifiers[j]==inAttrName)
	//				fndIdx=k;
	//		}
	//		if(fndIdx != -1)
	//		{
	//			m_RefTargets[k]->nodifiers.remove(fndIdx);
	//			return MS::kSuccess ;
	//		}
	//	}
	//}	
	int found=-1;
	for(int k = 0;k<m_OutputAttrNames.length();k++)
	{
		if( outAttrName == m_OutputAttrNames[k])
			found =k;
	}
	if(found!=-1)
		m_OutputAttrNames.remove(found);

	//Add In Attr
	found=-1;
	for(int k = 0;k<m_InputAttrNames.length();k++)
	{
		if( inAttrName == m_InputAttrNames[k])
			found =k;
	}
	if(found!=-1)
		m_InputAttrNames.remove(found);

	return MS::kFailure;
}


MStatus Kang_SimpExpNode::compute( const MPlug& plug, MDataBlock& data )
{
		MStatus status;
        MObject thisNode = thisMObject();
        MFnDependencyNode fnThisNode( thisNode );
		MString& pyRes=MString("");

#pragma region GetThis
		MString fnThisNodeStr = MString("this ='");
		fnThisNodeStr += fnThisNode.name();
		fnThisNodeStr += MString("'");
		if(fnThisNodeStr.length())
		{
			//const char* temppstr = fnThisNodeStr.asChar();
			MGlobal::executePythonCommand (	fnThisNodeStr,pyRes,false,false);
		}
		
#pragma endregion
#pragma region calc
		for(int j = 0;j<m_OutputAttrNames.length();j++)
		{
			if ( plug.partialName() == m_OutputAttrNames[j] )
			{
				MStringArray replacedPyCmdStrArr;
				
				//把python 代碼 提到 所有的 pa 的字部分都替換成 pa 的值(目前只支援 Numaric Type)
				for(int k = 0;k<m_InputAttrNames.length();k++)
				{
					MString paName = m_InputAttrNames[k];
					MPlug pA = fnThisNode.findPlug( paName, &status );
					if ( MStatus::kSuccess == status )
					{
						MDataHandle inputData = data.inputValue( pA, &status );
						CHECK_MSTATUS( status );
						const uint size = 65535;
						char st[size];
						float value;
						value = inputData.asFloat();
						sprintf(st,"%f",value);
						MString pyCmdStr = MString("");
						pyCmdStr += paName + MString(" = ");
						pyCmdStr += MString(st);
						MGlobal::executePythonCommand (	pyCmdStr,pyRes,false,false);
					}
				}

				/***
					執行 code 本體
				***/
				MString pycmd;
				MPlug pyCmdPlug = fnThisNode.findPlug( pyCmd, &status );
				if ( MStatus::kSuccess == status )
				{
					status = pyCmdPlug.getValue(pycmd);
					if(pycmd.length());
						MGlobal::executePythonCommand (	pycmd,pyRes,false,false);
				}

				// 執行最後python的結果，需自動產生
				float res=0.f;
				MGlobal::executePythonCommand (m_OutputAttrNames[j],pyRes,false,false);
				if(res=pyRes.asFloat())
				{
					// Python 最後的結果，目前不保證有值
					MDataHandle outputHandle = data.outputValue( plug );
					outputHandle.set( res );
				}
				data.setClean(plug);
			}
		}
#pragma endregion
        return( MS::kSuccess );
}

MStatus Kang_SimpExpNode::setDependentsDirty( const MPlug &plugBeingDirtied,
                MPlugArray &affectedPlugs )
{
		MStatus				stat;
		MObject thisNode = thisMObject();
		MFnDependencyNode fnThisNode( thisNode );

#pragma region FirstExecute_Py_Import
		// 第一次執行
		MString& pycmd=MString("");
		MString& pyRes=MString("");
		MPlug pyCmdImpPlug = fnThisNode.findPlug( pyImportCmd , &stat );
		if ( MStatus::kSuccess == stat )
		{
			stat = pyCmdImpPlug.getValue(pycmd);
			if(pycmd.length())
			{
				if(!bPyImpExecuted) 
				{
					MGlobal::executePythonCommand (pycmd,pyRes,false,false);
					bPyImpExecuted=true;
				}
			}
		}

#pragma endregion 


#pragma region GetPairArrFromString
		MString& inArrStr=MString("");
		MStringArray& ret=MStringArray();
		MPlug inArrPlug = fnThisNode.findPlug( inAttrNameArr , &stat );
		if ( MStatus::kSuccess == stat )
		{
			stat = inArrPlug.getValue(inArrStr);
			if(inArrStr.length())
			{
				char semicolumn = ';';
				inArrStr.split(semicolumn,ret);
				if(ret.length())
				{
					m_InputAttrNames=ret;
					for(int k=0;k<m_InputAttrNames.length();k++)
					{
						MString Str=m_InputAttrNames[k];
						const char* st = Str.asChar();
					}
				}
			}
		}

		MString& outArrStr=MString("");
		MStringArray& retout =MStringArray();
		MPlug outArrPlug = fnThisNode.findPlug( outAttrNameArr , &stat );
		if ( MStatus::kSuccess == stat )
		{
			stat = outArrPlug.getValue(outArrStr);
			if(outArrStr.length())
			{
				char semicolumn = ';';
				outArrStr.split(semicolumn,retout);
				if(ret.length())
				{
					m_OutputAttrNames=retout;
					for(int k=0;k<m_OutputAttrNames.length();k++)
					{
						MString Str=m_OutputAttrNames[k];
						const char* st = Str.asChar();
					}
				}
				
			}
		}

#pragma endregion
#pragma region markDirty
		for(int j = 0;j<m_InputAttrNames.length();j++)
		{
			if ( plugBeingDirtied.partialName() == m_InputAttrNames[j] )
			{
				for(int k = 0;k<m_OutputAttrNames.length();k++)
				{
					MPlug pB = fnThisNode.findPlug(  m_OutputAttrNames[k], &stat );
					if ( MStatus::kSuccess == stat ) 
					{
						CHECK_MSTATUS( affectedPlugs.append( pB ) );
					}
				}	
			}
		}
#pragma endregion

		return( MS::kSuccess );
}

void* Kang_SimpExpNode::creator()
{
	Kang_SimpExpNode* ret = new Kang_SimpExpNode();
	return ret;
}

MStatus Kang_SimpExpNode::initialize()
{
	MStatus				stat;
	MFnGenericAttribute genAttr;
	MFnTypedAttribute	typedAttr;

	
	pyImportCmd = typedAttr.create( "pyImportCmd", "pi",MFnStringData::kString);
	if (!stat) {
		stat.perror("can't create pyImportCmd Attr");
		return stat;
	}
	stat = addAttribute (pyImportCmd);
	if (!stat) { stat.perror("addAttribute"); return stat;}



	pyCmd = typedAttr.create( "pyCmd", "py",MFnStringData::kString);
	if (!stat) {
		stat.perror("can't create pyCmd Attr");
		return stat;
	}
	stat = addAttribute (pyCmd);
	if (!stat) { stat.perror("addAttribute"); return stat;}

	

	inAttrNameArr = typedAttr.create( "inAttrNameArr", "in",MFnStringData::kString);
	if (!stat) {
		stat.perror("can't create inAttrNameArr Attr");
		return stat;
	}
	stat = addAttribute (inAttrNameArr);
	if (!stat) { stat.perror("addAttribute"); return stat;}



	outAttrNameArr = typedAttr.create( "outAttrNameArr", "out",MFnStringData::kString);
	if (!stat) {
		stat.perror("can't create outAttrNameArr Attr");
		return stat;
	}
	stat = addAttribute (outAttrNameArr);
	if (!stat) { stat.perror("addAttribute"); return stat;}

	return MS::kSuccess;

}


#pragma region Cmd_setPyCommandStr

void* pyScriptNodeCmd_setPyCommandStr::creator()
{
	return new pyScriptNodeCmd_setPyCommandStr;
}
MStatus pyScriptNodeCmd_setPyCommandStr::doIt( const MArgList& args )
{
	MStatus stat = MS::kSuccess;
	// 找尋Node
	if( args.length() == 2 )
	{
		MString KangSimpNodeName = args.asString(0,&stat);
		MString pyCmdStr =  args.asString(1,&stat);

		MItDependencyNodes iter( MFn::kInvalid);
		int sceneNdCnt=0;
		for ( ; !iter.isDone(); iter.next() ) 
		{
			sceneNdCnt++;
			MObject object = iter.item();
			MFnDependencyNode node( object );
			if (node.name() == KangSimpNodeName)
			{
				Kang_SimpExpNode* kangNode = (Kang_SimpExpNode*)(node.userNode());
				if(kangNode)
				{
					//MStringArray splitedCmdStrArr; 
					//char enter = '\n';
					//pyCmdStr.split(enter, splitedCmdStrArr);
					//if(splitedCmdStrArr.length())
					//{
					//	kangNode->m_pyCommandStrArr = MStringArray( splitedCmdStrArr );
					//	for(int k=0;k<kangNode->m_pyCommandStrArr.length();k++)
					//	{
					//		MString st = kangNode->m_pyCommandStrArr[k];
					//		//fprintf(stderr,"__pycmd = %s\n",st.asChar());
					//	}
					//}
					kangNode->m_pyCommandStr = pyCmdStr;
				}
			}
		}
		return MS::kSuccess;
	}
	else
	{
		displayError("must specify a Kang_SimpExpNode name and python Command str"); return MS::kFailure;
	}
}
#pragma endregion

#pragma region Cmd_setPyImportCommandStr

void* pyScriptNodeCmd_setPyImportCommandStr::creator()
{
	return new pyScriptNodeCmd_setPyCommandStr;
}
MStatus pyScriptNodeCmd_setPyImportCommandStr::doIt( const MArgList& args )
{
	MStatus stat = MS::kSuccess;
	// 找尋Node
	if( args.length() == 2 )
	{
		MString KangSimpNodeName = args.asString(0,&stat);
		MString pyCmdStr =  args.asString(1,&stat);

		MItDependencyNodes iter( MFn::kInvalid);
		int sceneNdCnt=0;
		for ( ; !iter.isDone(); iter.next() ) 
		{
			sceneNdCnt++;
			MObject object = iter.item();
			MFnDependencyNode node( object );
			if (node.name() == KangSimpNodeName)
			{
				Kang_SimpExpNode* kangNode = (Kang_SimpExpNode*)(node.userNode());
				if(kangNode)
				{
					kangNode->m_py_ImportCmdStr = pyCmdStr;
				}
			}
		}
		return MS::kSuccess;
	}
	else
	{
		displayError("must specify a Kang_SimpExpNode name and python Command str "); return MS::kFailure;
	}
}
#pragma endregion

#pragma region Cmd_addNewInOutPair
void* pyScriptNodeCmd_addNewInOutPair::creator()
{
	return new pyScriptNodeCmd_addNewInOutPair;
}
MStatus pyScriptNodeCmd_addNewInOutPair::doIt( const MArgList& args )
{
	MStatus stat = MS::kSuccess;
	// 找尋Node
	if( args.length() == 3 )
	{
		MString KangSimpNodeName = args.asString(0,&stat);
		MString inAttrName =  args.asString(1,&stat);
		MString outAttrName =  args.asString(2,&stat);

		MItDependencyNodes iter( MFn::kInvalid);
		int sceneNdCnt=0;
		for ( ; !iter.isDone(); iter.next() ) 
		{
			sceneNdCnt++;
			MObject object = iter.item();
			MFnDependencyNode node( object );
			if (node.name() == KangSimpNodeName)
			{
				Kang_SimpExpNode* kangNode = (Kang_SimpExpNode*)(node.userNode());
				if(kangNode)
				{
					kangNode->addNewInOutPair(inAttrName, outAttrName);
				}
			}
		}
		return MS::kSuccess;
	}
	else
	{
		displayError("must specify a Kang_SimpExpNode name , In Attr Name , Out Attr Name."); return MS::kFailure;
	}
}
#pragma endregion

#pragma region Cmd_removeInOutPair
void* pyScriptNodeCmd_removeInOutPair::creator()
{
	return new pyScriptNodeCmd_removeInOutPair;
}
MStatus pyScriptNodeCmd_removeInOutPair::doIt( const MArgList& args )
{
	MStatus stat = MS::kSuccess;
	// 找尋Node
	if( args.length() == 3 )
	{
		MString KangSimpNodeName = args.asString(0,&stat);
		MString inAttrName =  args.asString(1,&stat);
		MString outAttrName =  args.asString(2,&stat);

		MItDependencyNodes iter( MFn::kInvalid);
		int sceneNdCnt=0;
		for ( ; !iter.isDone(); iter.next() ) 
		{
			sceneNdCnt++;
			MObject object = iter.item();
			MFnDependencyNode node( object );
			if (node.name() == KangSimpNodeName)
			{
				Kang_SimpExpNode* kangNode = (Kang_SimpExpNode*)(node.userNode());
				if(kangNode)
				{
					kangNode->removeInOutPair(inAttrName,outAttrName);
				}
			}
		}
		return MS::kSuccess;
	}
	else
	{
		displayError("must specify a Kang_SimpExpNode name , In Attr Name , Out Attr Name."); return MS::kFailure;
	}
}

#pragma endregion
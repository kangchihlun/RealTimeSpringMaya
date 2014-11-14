//
// Copyright (C) Kang
// 
// File: pluginMain.cpp
//
// Author: Maya Plug-in Wizard 2.0
//

#include "Kang_SimpExpNodeNode.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
//
//	Description:
//		this method is called when the plug-in is loaded into Maya.  It 
//		registers all of the services that this plug-in provides with 
//		Maya.
//
//	Arguments:
//		obj - a handle to the plug-in object (use MFnPlugin to access it)
//
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "Kang", "2013", "Any");

	status = plugin.registerNode( "Kang_SimpExpNode", Kang_SimpExpNode::id, Kang_SimpExpNode::creator,
								  Kang_SimpExpNode::initialize );
	plugin.registerCommand( "pyScriptNodeCmd_setPyCommandStr", pyScriptNodeCmd_setPyCommandStr::creator);
	plugin.registerCommand( "pyScriptNodeCmd_setPyImportCommandStr", pyScriptNodeCmd_setPyImportCommandStr::creator);
	plugin.registerCommand( "pyScriptNodeCmd_addNewInOutPair", pyScriptNodeCmd_addNewInOutPair::creator);
	plugin.registerCommand( "pyScriptNodeCmd_removeInOutPair", pyScriptNodeCmd_removeInOutPair::creator);

	if (!status) 
	{
		status.perror("registerNode");
		return status;
	}

	return status;
}

MStatus uninitializePlugin( MObject obj)
//
//	Description:
//		this method is called when the plug-in is unloaded from Maya. It 
//		deregisters all of the services that it was providing.
//
//	Arguments:
//		obj - a handle to the plug-in object (use MFnPlugin to access it)
//
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( Kang_SimpExpNode::id );
	plugin.deregisterCommand( "pyScriptNodeCmd_setPyCommandStr" );
	plugin.deregisterCommand( "pyScriptNodeCmd_addNewInOutPair" );
	plugin.deregisterCommand( "pyScriptNodeCmd_removeInOutPair" );
	if (!status) 
	{
		status.perror("deregisterNode");
		return status;
	}

	return status;
}

# -*- coding: utf-8 -*-
# Last Modified 2013/12/21
# Author Chih Lun Kang
#在執行之前，先 copy plugin Folder
import sys,os
import __builtin__
import shutil
import maya.mel
import maya.cmds as cmds

def listdir_joined(path):
	return [os.path.join(path, entry) for entry in os.listdir(path)]
	
def getfileRecursive(path,outArr):
	if(os.path.isfile(path)):
		_type_ = (path.split("."))[-1]
		#if(fileType == _type_):
		outArr.append(path)
	elif(os.path.isdir(path)):
		_folders_ = [x for x in listdir_joined(path)]
		for f in _folders_ :
			getfileRecursive(f,outArr)



class PluginCopier:
	# 建構子參數解說：
	# CurScrptPth : 當前script 執行路徑
	def __init__(self,CurScrptPth=''): 
		self.loadDecomposeMatDll()
		self.thisScrptPth = CurScrptPth
		self.copyReqFileToFolder()
	def loadDecomposeMatDll(self):
		mversion = (maya.mel.eval("float $mayaVersion = `getApplicationVersionAsFloat` ;"))
		if(mversion >2012):
			if not cmds.pluginInfo(("matrixNodes.mll"),q=True,loaded=True):
				cmds.loadPlugin("matrixNodes.mll")
				#set autoloaded
				cmds.pluginInfo("matrixNodes.mll",e=True,autoload=True)

	def copyReqFileToFolder(self):
		plugFileName='Kang_SimpExpNode' # 修改這個
		
		#判斷版本，一律假設64bit
		mversion = str(maya.mel.eval("float $mayaVersion = `getApplicationVersionAsFloat` ;"))
		strMversion= mversion.split('.')[0]
		#丟到有帶版本號的 script folder 
		usd = cmds.internalVar(usd=True)
		usrFold = usd[:-8]
		custPlugFold = usrFold + "plug-ins/"
		cpyDestFolder = custPlugFold
		plgFod = self.thisScrptPth + '/MXSController/mll/maya'+strMversion +'/'
		
		plgDllFile = plgFod+plugFileName+'.mll'
		cpyDestDllFile=cpyDestFolder+plugFileName+'.mll'
		
		# 有可能會有版本衝突，先刪除
		try:
			os.remove(cpyDestDllFile)
		except:
			pass
		opRes=None
		if(os.path.isfile(cpyDestDllFile)):
			try:opRes = open(cpyDestDllFile,'r')
			except:pass
		if(not opRes): #檔存在的話就不用co了
			try:res=os.makedirs(cpyDestFolder)#強制建Folder
			except:pass
			#Copy 所需的pyd files	
			#import shutil
			shutil.copy2(plgDllFile, cpyDestDllFile)
		else:
			opRes.close()
		
		#臨時加入當前 plugin Folder
		sysplugFldPth = maya.mel.eval("$sr = `getenv MAYA_PLUG_IN_PATH`;")
		if(not (cpyDestFolder in sysplugFldPth)):
			maya.mel.eval("$str = `putenv MAYA_PLUG_IN_PATH \""+cpyDestFolder+"\"`;")
		
		#load
		try:cmds.unloadPlugin(plugFileName)
		except:pass
		if not cmds.pluginInfo((plugFileName+".mll"),q=True,loaded=True):
			cmds.loadPlugin(plugFileName)
			#set autoloaded
			cmds.pluginInfo((plugFileName+".mll"),e=True,autoload=True)

		#找尋maya.env檔，寫入
		usd = cmds.internalVar(usd=True)
		usrFold = usd[:-8]
		mayaEnvFilePath = usrFold+"Maya.env"
		if os.path.isfile(mayaEnvFilePath):
			# read all
			f=open(mayaEnvFilePath,'r')
			allLines = []
			newAllLines = []
			line =f.readline()
			line = line.replace("\r", "")
			line = line.replace("\n", "")
			if(len(line)):
				allLines.append(line)
			while(line!=''):
				line=f.readline()
				if(len(line)):
					line = line.replace("\r", "")
					line = line.replace("\n", "")
					allLines.append(line)
			f.close()
			if(len(allLines)):
				for li in allLines: #li=allLines[0]
					if("MAYA_PLUG_IN_PATH" in li):
						lnChk = li.replace(" ", "")
						lnChk = li.replace("=", "")
						ssrt = lnChk.split('MAYA_PLUG_IN_PATH')[1]
						ssrt  = ssrt.replace(" ", "")
						if(not len(ssrt)):
							li += cpyDestFolder
						elif(not cpyDestFolder in li):
							li += ';'+cpyDestFolder
					li += "\r\n"
					newAllLines.append(li)
			else:
				newAllLines.append("MAYA_PLUG_IN_PATH = "+cpyDestFolder)
			#write all
			f = open (mayaEnvFilePath , 'w')
			f.writelines(newAllLines)
			f.close()
		else: #創一個新的
			f = open (mayaEnvFilePath, 'w+')
			f.write("MAYA_PLUG_IN_PATH="+cpyDestFolder)
			f.close()




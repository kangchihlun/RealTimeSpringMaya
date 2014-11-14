# -*- coding: utf-8 -*-
# Last Modified 2013/11/21
# Author Chih Lun Kang
#在執行之前，先 copy Python.Runtime.dll clr.pyd 這兩個檔案到 script Folder
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

class ClrDllCopier:
	# 建構子參數解說：
	# nextClass : copy 所需dll 之後接著要建立的class
	# CurScrptPth : 當前script 執行路徑
	def __init__(self,CurScrptPth=''):  #CurScrptPth='C:/PipeToolSet/VCAT/pyModule'
		self.thisScrptPth = CurScrptPth
		#self.__nextClassType__ = nextClass
		self.copyReqFileToFolder()
	def copyReqFileToFolder(self):
		#判斷版本，一律假設64bit
		mversion = str(maya.mel.eval("float $mayaVersion = `getApplicationVersionAsFloat` ;"))
		strMversion= mversion.split('.')[0]
		#script folder
		cpyDestFolder = str(maya.mel.eval("string $mayascrptfp = `internalVar -usd `"))
		plgFod = self.thisScrptPth + '/DotNet/clr/maya'+strMversion +'/'
		
		plgDllFile = plgFod+'Python.Runtime.dll'
		plgPydFile = plgFod+'clr.pyd'
		cpyDestDllFile=cpyDestFolder+'Python.Runtime.dll'
		cpyDestPydFile=cpyDestFolder+'clr.pyd'
		# 有可能會有版本衝突，先刪除
		
		try:
			os.remove(cpyDestDllFile)
			os.remove(cpyDestPydFile)
		except:
			pass
		
		
		opRes=None
		if(os.path.isfile(cpyDestDllFile)):
			try:opRes = open(cpyDestDllFile,'r')
			except:pass
		#print("###############  OpenRes = "+ type(opRes).__name__ + "###########")
		if(not opRes): #檔存在的話就不用co了
			try:res=os.makedirs(cpyDestFolder)#強制建Folder
			except:pass
			#Copy 所需的pyd files	
			#import shutil
			shutil.copy2(plgDllFile, cpyDestDllFile)
			shutil.copy2(plgPydFile, cpyDestPydFile)
		else:
			opRes.close()
		
		
		# 複製所需的額外擴充模組 dll：
		plgFodCustC = self.thisScrptPth + '/DotNet/clr/CustCtrls/'
		allDlls=[]
		getfileRecursive(plgFodCustC,allDlls)
		for d in allDlls:
			_file_ = d.split('/')[-1]
			_cpyDestFolder = cpyDestFolder+"CustCtrls/"
			_cpyDestDll = _cpyDestFolder + _file_
			# 嘗試開啟
			opRes=None
			if(os.path.isfile(_cpyDestDll)):
				try:opRes = open(_cpyDestDll,'r')
				except:pass
			if(not opRes): #檔存在的話就不用co了
				try:res=os.makedirs(_cpyDestFolder)#強制建Folder
				except:pass
				#Copy 所需的額外擴充模組 dll	
				shutil.copy2(d,_cpyDestDll)
			else:
				opRes.close()
			
		#加入 sys.path
		if(not cpyDestFolder in sys.path):
			sys.path.append(cpyDestFolder)
		# 加入 __builtin__ path
		__builtin__.DotNetDllPath = cpyDestFolder+"CustCtrls/"



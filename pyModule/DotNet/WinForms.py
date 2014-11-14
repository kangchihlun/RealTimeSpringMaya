# -*- coding: utf-8 -*-
# Last Modified 2013/12/30
# Author Chih Lun Kang
'''
	WinForm 簡單指令
	
'''
import sys,os
import __builtin__
import copy
import maya.mel as mel
import maya.cmds as cmds

try:import clr 
except:pass

if(clr):
	clr.AddReference("System")
	clr.AddReference("System.Drawing")
	clr.AddReference("System.Windows.Forms")
	import System
	import System.Drawing
	import System.Windows.Forms
	
# Dotnet 的Decimal 不知為何無法處理小數點
# 所以要特別處理，5位數應該夠用
def DotNetDecimalProc(floatNum = 5.3):
	rest_floatNum = round((floatNum - int(floatNum)),5)
	rest_floatNum_st = str(rest_floatNum)
	if(rest_floatNum_st.index('.')):
		num_s = (rest_floatNum_st.split('.'))[1]
		num_f = float(num_s)
		pwdAmt = len(num_s)
		d0 = System.Decimal(floatNum) # d4 = System.Decimal.ToDouble(d0)
		d1 = System.Decimal(num_f)
		d2 = System.Decimal(float(pow(10,pwdAmt)))
		d3 = System.Decimal.Divide(d1,d2)
		d4 = System.Decimal.Add(d0,d3)
		return d4
	return (System.Decimal.Zero)

def GUI(cls='',
          n='ctrl',
          pos=[0,0],
          p=None,
          size=[10,10],
          text="",
          img='',
          bc = System.Drawing.Color.DimGray,
          range = [0,10,1], # Only for NumericUpDown/TrackBar
          scale = 1, # Only for NumericUpDown/TrackBar
          checked=True, # Only for CheckBox
          enabled=True,
          tooltip=""
          ):
		
	_Ctrl = None
	if(cls == 'Form'):
		_Ctrl = System.Windows.Forms.Form()
		_Ctrl.MaximizeBox =False
		_Ctrl.MinimizeBox =False
		_Ctrl.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
	elif(cls == 'Panel'):
		_Ctrl = System.Windows.Forms.Panel()
	elif(cls == 'PictureBox'):
		_Ctrl = System.Windows.Forms.PictureBox()
	elif(cls == 'Button'):
		_Ctrl = System.Windows.Forms.Button()
		_Ctrl.FlatStyle = System.Windows.Forms.FlatStyle.Popup
	elif(cls == 'EditText'):
		_Ctrl = System.Windows.Forms.TextBox()
	elif(cls == 'CheckButton'):
		_Ctrl = System.Windows.Forms.CheckBox()
		_Ctrl.Checked=checked
		_Ctrl.Appearance = System.Windows.Forms.Appearance.Button
	elif(cls == 'CheckBox'):
		_Ctrl = System.Windows.Forms.CheckBox()
		_Ctrl.Checked=checked
		_Ctrl.Appearance = System.Windows.Forms.Appearance.Normal
	elif(cls == 'RadioButton'):
		_Ctrl = System.Windows.Forms.RadioButton()
	elif(cls == 'ListView'):
		_Ctrl = System.Windows.Forms.ListView()
	elif(cls == 'Label'):
		_Ctrl = System.Windows.Forms.Label()
	elif(cls == 'GroupBox'):
		_Ctrl = System.Windows.Forms.GroupBox()
	elif(cls == 'Spinner'):
		_Ctrl = System.Windows.Forms.NumericUpDown() #scale=1 range=[0,1.0,0.3]
		_Ctrl.DecimalPlaces=scale
		ff = ( float(1.0/pow(10,scale)))
		_Ctrl.Increment = DotNetDecimalProc(floatNum=ff)
		_Ctrl.Minimum = DotNetDecimalProc(floatNum=range[0])
		_Ctrl.Maximum = DotNetDecimalProc(floatNum=range[1])
		_Ctrl.Value = DotNetDecimalProc(floatNum=range[2])
	elif(cls == 'Slider'):
		_Ctrl = System.Windows.Forms.TrackBar()
		_Ctrl.LargeChange = scale
		_Ctrl.TickStyle = System.Windows.Forms.TickStyle.TopLeft
		_Ctrl.Minimum = range[0]
		_Ctrl.Maximum = range[1]
		_Ctrl.Value = range[2]
		_Ctrl.TickFrequency = range[1]/5
		_Ctrl.TabIndex = 0
		_Ctrl.TabStop = False
	elif(cls == 'Image'):
		_Ctrl = System.Windows.Forms.PictureBox()
	elif(cls == 'TabControl'):
		_Ctrl = System.Windows.Forms.TabControl()
	elif(cls == 'TabPage'):
		_Ctrl = System.Windows.Forms.TabPage()
	elif(cls == 'DropDownList'):
		_Ctrl = System.Windows.Forms.ComboBox()
	if(_Ctrl):
		# 處理 Img
		_Img = None
		if(len(img)):
			try:_Ctrl.Image = System.Drawing.Image.FromFile(img)
			except:pass
		# 通用屬性
		#try:
		_Ctrl.Size = System.Drawing.Size(size[0],size[1])
		_Ctrl.Width = size[0]
		_Ctrl.Height = size[1]
		_Ctrl.Location = System.Drawing.Point(pos[0],pos[1])
		_Ctrl.Name = n
		_Ctrl.BackColor = bc
		_Ctrl.Text = text
		_Ctrl.Enabled = enabled
		
		if(tooltip):
			toolTip1  = System.Windows.Forms.ToolTip()
			toolTip1.AutoPopDelay = 5000
			toolTip1.InitialDelay = 100
			toolTip1.ReshowDelay = 100
			
			toolTip1.ShowAlways = True
			toolTip1.SetToolTip(_Ctrl, tooltip);
		if(p):
			p.Controls.Add(_Ctrl)
		#except:pass
		return _Ctrl

def sldGrp(size=[120,60]):
	pass
def rdoBtnGrp(size=[10,10],Text="None"):
	pass
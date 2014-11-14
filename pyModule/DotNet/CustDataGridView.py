# -*- coding: utf-8 -*-
# Last Modified 2013/11/26
# Author Chih Lun Kang

try:import clr
except:pass
if(clr):
		clr.AddReference("System")
		clr.AddReference("System.Windows.Forms")
		clr.AddReference("System.Drawing")
		import System
		import System.Windows.Forms
		import System.Drawing
		from DotNet import ExtensionAssembly
		from DotNet import Copier
import math

def CreateCustGV(columnCount = 2 , rowCount = 10):
	if(clr):
		DataGridViewExtension=None
		compileRes=None
		try:import DataGridViewExtension
		except:pass
		
		if (not DataGridViewExtension):
			compileRes = ExtensionAssembly.CreateDataGridViewExtensionAssembly()
			if compileRes:
				import DataGridViewExtension
		if DataGridViewExtension:
			import DataGridViewExtension
			inGV = System.Windows.Forms.DataGridView()
			cc = DataGridViewExtension.Style()
			cc.SetDoubleBuffer(inGV)
			font = inGV.Font
			#inGV.Font = System.Drawing.Font(font.FontFamily,font.Size,System.Drawing.FontStyle.Bold )
			inGV.Font = System.Drawing.Font(font.FontFamily,font.Size, 24 )
			bc = DataGridViewExtension.ImageTextCellColumn()
			bc.LabelBackColor = System.Drawing.Color.FromArgb( 70 ,System.Drawing.Color.DarkRed )
			bc.LabelForeColor = System.Drawing.Color.FromArgb( 200,System.Drawing.Color.Black )
			bc.HighQuality = True
			bc.StringFormat.Alignment = System.Drawing.StringAlignment.Center
			bc.StringFormat.LineAlignment = System.Drawing.StringAlignment.Far
			bc.DefaultCellStyle.BackColor = System.Drawing.Color.Beige 


			p = System.Windows.Forms.Padding(2)
			p.Bottom = 16
			bc.DefaultCellStyle.Padding = p
			bc.ImageLayout = System.Windows.Forms.DataGridViewImageCellLayout.Normal
			
			inGV.ColumnHeadersDefaultCellStyle.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleCenter
			inGV.ReadOnly = True
			inGV.MultiSelect = True
			inGV.Dock = System.Windows.Forms.DockStyle.Fill
			inGV.RowTemplate.Height = 60
			inGV.AutoSize = True
			inGV.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill
			inGV.AutoSizeRowsMode = System.Windows.Forms.DataGridViewAutoSizeRowsMode.AllCells
			inGV.AutoSizeRowsMode = System.Windows.Forms.DataGridViewAutoSizeRowsMode.None
			inGV.RowHeadersWidthSizeMode = System.Windows.Forms.DataGridViewRowHeadersWidthSizeMode.EnableResizing
			for k in range(0,columnCount):
				inGV.Columns.Add (bc.Clone())
				
			inGV.RowCount = rowCount
			inGV.ColumnHeadersVisible = inGV.ShowEditingIcon = inGV.RowHeadersVisible = False
			inGV.AllowUserToaddRows = inGV.AllowUserToDeleteRows = inGV.AllowUserToResizeColumns = False
			inGV.AllowUserToResizeRows = False
			inGV.VerticalScrollBar.Visible = True
			return inGV

# 產生 image based DataGrid View ，只需傳入圖片路徑
def createImgBasedCustGV(imgPth,columnCnt = 5): #imgPth='D:/05Py/NMAAssetToolSet/Pipe12Tool_SkelTool/images'
	if(clr):
		gv = CreateCustGV(columnCount=columnCnt)
		# 收集UI圖片
		allimgs=[]
		imgCol=[] # bmp 收集
		Copier.getfileRecursive(imgPth,allimgs) 
		for p in allimgs:
			bmp = System.Drawing.Bitmap(p)
			bmp.tag = p
			imgCol.append(bmp)

		gv.SuspendLayout()
		if(len(imgCol)):
			gv.RowCount = int(math.ceil( float(len(imgCol))/columnCnt ))
		else:
			gv.RowCount = 0
		
		for i in range(0,gv.RowCount): #i=gv.RowCount-1
			for j in range(0,columnCnt): #j=columnCnt-1 gv.ColumnCount
				c = i * columnCnt + j
				idx = c % len(imgCol)
				bmp = imgCol[idx]
				cell = gv.Rows[i].Cells[j]
				#cell.ImageLayout = System.Windows.Forms.DataGridViewImageCellLayout.Zoom if( (cell.Size.Width < bmp.Width) or (cell.Size.Height < bmp.Height)) else System.Windows.Forms.DataGridViewImageCellLayout.Normal
				#cell.ImageLayout = System.Windows.Forms.DataGridViewImageCellLayout.Zoom
				cell.ImageLayout = System.Windows.Forms.DataGridViewImageCellLayout.Stretch
				cell.Height = bmp.Height
				cell.Width = bmp.Width
				if not cell.ImageTextCellColumn.ShowLabel:cell.ShowLabel = False
				cell.Value = bmp
				cell.Description = bmp.tag
				cell.ToolTipText = bmp.tag
		gv.ResumeLayout()
		return gv


#gv.Rows[26].Cells.Count
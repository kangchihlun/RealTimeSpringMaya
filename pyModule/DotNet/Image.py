# -*- coding: utf-8 -*-
# Last Modified 2013/12/4
# Author Chih Lun Kang
import os
try:import clr
except:pass
if(clr):
		clr.AddReference("System")
		clr.AddReference("System.Drawing")
		
		import System
		import System.Drawing
		import System.Drawing.Imaging
		import System.Drawing.Drawing2D
		
# 位圖轉灰階作法
# http://tech.pro/tutorial/660/csharp-tutorial-convert-a-color-image-to-grayscale

def MakeGrayscale3(original):
	newBitmap = System.Drawing.Bitmap(original.Width, original.Height);
	g = System.Drawing.Graphics.FromImage(newBitmap)
	#create the grayscale ColorMatrix	
	colorMatrix = System.Drawing.Imaging.ColorMatrix()
	colorMatrix.Matrix00=.3
	colorMatrix.Matrix01=.3
	colorMatrix.Matrix02=.3
	colorMatrix.Matrix10=.59
	colorMatrix.Matrix11=.59
	colorMatrix.Matrix12=.59
	colorMatrix.Matrix20=.11
	colorMatrix.Matrix21=.11
	colorMatrix.Matrix22=.11
	colorMatrix.Matrix33=1
	colorMatrix.Matrix44=1
	attributes = System.Drawing.Imaging.ImageAttributes()
	#set the color matrix attribute
	attributes.SetColorMatrix(colorMatrix);
	#draw the original image on the new image
	#using the grayscale color matrix
	g.DrawImage(original, System.Drawing.Rectangle(0, 0,  original.Width, original.Height), 
      0, 0, original.Width, original.Height, System.Drawing.GraphicsUnit.Pixel, attributes)

	#dispose the Graphics object
	g.Dispose()
	return newBitmap

# 轉換矩陣換成紫色
def MakePurple(original):
	newBitmap = System.Drawing.Bitmap(original.Width, original.Height);
	g = System.Drawing.Graphics.FromImage(newBitmap)
	#create the grayscale ColorMatrix	
	colorMatrix = System.Drawing.Imaging.ColorMatrix()
	colorMatrix.Matrix00=.3
	colorMatrix.Matrix01=.3
	colorMatrix.Matrix02=.3
	colorMatrix.Matrix10=.59
	colorMatrix.Matrix11=.59
	colorMatrix.Matrix12=.59

	colorMatrix.Matrix23=1
	colorMatrix.Matrix34=1
	attributes = System.Drawing.Imaging.ImageAttributes()
	#set the color matrix attribute
	attributes.SetColorMatrix(colorMatrix);
	#draw the original image on the new image
	#using the grayscale color matrix
	g.DrawImage(original, System.Drawing.Rectangle(0, 0,  original.Width, original.Height), 
      0, 0, original.Width, original.Height, System.Drawing.GraphicsUnit.Pixel, attributes)

	#dispose the Graphics object
	g.Dispose()
	return newBitmap

# -*- coding: utf-8 -*-
# Last Modified 2013/11/26
# Author Chih Lun Kang


try:import clr
except:pass
if(clr):
		clr.AddReference("System")
		#clr.AddReference("System.IO")
		clr.AddReference("System.Windows")
		import System
		import System.IO
		import System.Reflection
		asm = System.Reflection.Assembly
		asm = asm.LoadWithPartialName("PresentationFramework") # ���J�һݪ�dll
		import System.Windows
		import Microsoft
		
def compileCSharpAsm( sourceCode =""):
	csharpProvider = Microsoft.CSharp.CSharpCodeProvider()
	compilerParams = System.CodeDom.Compiler.CompilerParameters()

	compilerParams.ReferencedAssemblies.AddRange("System.dll","System.Windows.Forms.dll","System.Drawing.dll")

	compilerParams.GenerateInMemory = True
	compilerResults = csharpProvider.CompileAssemblyFromSource( compilerParams,[sourceCode])

	if( compilerResults.Errors.Count ):
		result = System.Windows.MessageBox.Show("Errors encountered while compiling C# code")
		'''
		errs = stringstream ""
		for i = 0 to (compilerResults.Errors.Count-1) do
		(
			err = compilerResults.Errors.Item[i]
			format "Error:% Line:% Column:% %\n" err.ErrorNumber err.Line err.Column err.ErrorText to:errs 
		)
		MessageBox (errs as string) title: "Errors encountered while compiling C# code"
		format "%\n" errs
		'''
	else:
		return compilerResults.CompiledAssembly

def CreateCSharpCustomStructAssembly(forceRecompile=True):
	if(forceRecompile and clr):
		source = ""
		source += "using System;\n"
		source += "using System.Reflection;\n"
		source += "namespace ClrPyExtensions\n"
		source += "{\n"
		source += "	public class MyData\n"
		source += "{\n"
		source += "	public string Image;\n"
		source += " public MyData()\n"
		source += "{\n"
		source += "	\n"
		source += "}\n"
		source += "}\n"
		source += "}\n"
		return compileCSharpAsm(source)



def CreateDataGridViewExtensionAssembly(forceRecompile=True):
	if(forceRecompile and clr):
		source = ""
		source += "using System;\n"
		source += "using System.Reflection;\n"
		source += "using System.Runtime.InteropServices;\n"
		source += "using System.Drawing;\n"
		source += "using System.Windows.Forms;\n"
		source += "namespace DataGridViewExtension\n"
		source += "{\n"
		source += "	public class Style\n"
		source += "	{\n"
		source += "	 public void SetStyle(Control control, ControlStyles styles, bool newValue)\n"
		source += "	 {\n"
		source += "	 object[] args = { styles, newValue };\n"
		source += "	 typeof(Control).InvokeMember(\"SetStyle\",\n"
		source += "	 BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.InvokeMethod,\n"
		source += "	 null, control, args);\n"
		source += "	 }\n"
		source += "	 public bool SetSelectable(Control control, bool newValue)\n"
		source += "	 {\n"
		source += "	 SetStyle(control, ControlStyles.Selectable, newValue);\n"
		source += "	 return newValue;\n"
		source += "	 }\n"
		source += "	 public void SetDoubleBuffer(Control control)\n"
		source += "	 {\n"
		source += "	 SetStyle(control, ControlStyles.DoubleBuffer | ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint | ControlStyles.Opaque, true);\n"
		source += "	 }\n"
		source += "	}\n"
		source += "	public class ImageTextCellColumn : DataGridViewImageColumn\n"
		source += "	{\n"
		source += "	 private Boolean showLabel;\n"
		source += "	 private Boolean highQuality;\n"
		source += "	 private String label;\n"
		source += "	 private StringFormat stringFormat;\n"
		source += "	 private Color labelBackColor;\n"
		source += "	 private Color labelForeColor;\n"
		source += "	 public ImageTextCellColumn()\n"
		source += "	 {\n"
		source += "	 this.ShowLabel = true;\n"
		source += "	 this.HighQuality = false;\n"
		source += "	 this.StringFormat = new StringFormat();\n"
		source += "	 this.LabelForeColor = Color.White;\n"
		source += "	 this.LabelBackColor = Color.FromArgb(100, Color.Black);\n"
		source += "	 this.CellTemplate = new ImageTextCell();\n"
		source += "	 }\n"
		source += "	 public override object Clone()\n"
		source += "	 {\n"
		source += "	 ImageTextCellColumn c = base.Clone() as ImageTextCellColumn;\n"
		source += "	 c.ShowLabel = this.showLabel;\n"
		source += "	 c.HighQuality = this.highQuality;\n"
		source += "	 c.Label = this.label;\n"
		source += "	 c.StringFormat = this.stringFormat;\n"
		source += "	 c.LabelForeColor = this.labelForeColor;\n"
		source += "	 c.LabelBackColor = this.labelBackColor;\n"
		source += "	 return c;\n"
		source += "	 }\n"
		source += "	 private ImageTextCell ImageTextCellTemplate\n"
		source += "	 {\n"
		source += "	 get { return this.CellTemplate as ImageTextCell; }\n"
		source += "	 }\n"
		source += "	 public Boolean ShowLabel\n"
		source += "	 {\n"
		source += "	 get { return this.showLabel; }\n"
		source += "	 set { this.showLabel = value; }\n"
		source += "	 }\n"
		source += "	 public Boolean HighQuality\n"
		source += "	 {\n"
		source += "	 get { return this.highQuality; }\n"
		source += "	 set { this.highQuality = value; }\n"
		source += "	 }\n"
		source += "	 public String Label\n"
		source += "	 {\n"
		source += "	 get { return this.label; }\n"
		source += "	 set { this.label = value; }\n"
		source += "	 }\n"
		source += "	 public StringFormat StringFormat\n"
		source += "	 {\n"
		source += "	 get { return this.stringFormat; }\n"
		source += "	 set { this.stringFormat = value; }\n"
		source += "	 }\n"
		source += "	 public Color LabelForeColor\n"
		source += "	 {\n"
		source += "	 get { return this.labelForeColor; }\n"
		source += "	 set { this.labelForeColor = value; }\n"
		source += "	 }\n"
		source += "	 public Color LabelBackColor\n"
		source += "	 {\n"
		source += "	 get { return this.labelBackColor; }\n"
		source += "	 set { this.labelBackColor = value; }\n"
		source += "	 }\n"
		source += "	}\n"
		source += "	public class ImageTextCell : DataGridViewImageCell\n"
		source += "	{\n"
		source += "	 private Boolean showLabel;\n"
		source += "	 private String label;\n"
		source += "	 private Color labelBackColor;\n"
		source += "	 private Color labelForeColor;\n"
		source += "	 public ImageTextCell()\n"
		source += "	 {\n"
		source += "	 this.ShowLabel = true;\n"
		source += "	 }\n"
		source += "	 public override object Clone()\n"
		source += "	 {\n"
		source += "	 ImageTextCell c = base.Clone() as ImageTextCell;\n"
		source += "	 c.ShowLabel = this.showLabel;\n"
		source += "	 c.Label = this.label;\n"
		source += "	 c.LabelForeColor = this.labelForeColor;\n"
		source += "	 c.LabelBackColor = this.labelBackColor;\n"
		source += "	 return c;\n"
		source += "	 }\n"
		source += "	 public Boolean ShowLabel\n"
		source += "	 {\n"
		source += "	 get\n"
		source += "	 {\n"
		source += "	 if (this.OwningColumn == null || this.ImageTextCellColumn == null) { return showLabel; }\n"
		source += "	 else return (this.showLabel & this.ImageTextCellColumn.ShowLabel);\n"
		source += "	 }\n"
		source += "	 set { if (this.showLabel != value) { this.showLabel = value; } }\n"
		source += "	 }\n"
		source += "	 public String Label\n"
		source += "	 {\n"
		source += "	 get\n"
		source += "	 {\n"
		source += "	 if (this.OwningColumn == null || this.ImageTextCellColumn == null) { return label; }\n"
		source += "	 else if (this.label != null)\n"
		source += "	 {\n"
		source += "	 return this.label;\n"
		source += "	 }\n"
		source += "	 else\n"
		source += "	 {\n"
		source += "	 return this.ImageTextCellColumn.Label;\n"
		source += "	 }\n"
		source += "	 }\n"
		source += "	 set { if (this.label != value) { this.label = value; } }\n"
		source += "	 }\n"
		source += "	 public Color LabelForeColor\n"
		source += "	 {\n"
		source += "	 get\n"
		source += "	 {\n"
		source += "	 if (this.OwningColumn == null || this.ImageTextCellColumn == null) { return labelForeColor; }\n"
		source += "	 else if (this.labelForeColor != Color.Empty)\n"
		source += "	 {\n"
		source += "	 return this.labelForeColor;\n"
		source += "	 }\n"
		source += "	 else\n"
		source += "	 {\n"
		source += "	 return this.ImageTextCellColumn.LabelForeColor;\n"
		source += "	 }\n"
		source += "	 }\n"
		source += "	 set { if (this.labelForeColor != value) { this.labelForeColor = value; } }\n"
		source += "	 }\n"
		source += "	 public Color LabelBackColor\n"
		source += "	 {\n"
		source += "	 get\n"
		source += "	 {\n"
		source += "	 if (this.OwningColumn == null || this.ImageTextCellColumn == null) { return labelBackColor; }\n"
		source += "	 else if (this.labelBackColor != Color.Empty)\n"
		source += "	 {\n"
		source += "	 return this.labelBackColor;\n"
		source += "	 }\n"
		source += "	 else\n"
		source += "	 {\n"
		source += "	 return this.ImageTextCellColumn.LabelBackColor;\n"
		source += "	 }\n"
		source += "	 }\n"
		source += "	 set { if (this.labelBackColor != value) { this.labelBackColor = value; } }\n"
		source += "	 }\n"
		source += "	 protected override void Paint(Graphics graphics, Rectangle clipBounds, Rectangle cellBounds, int rowIndex,\n"
		source += "	 DataGridViewElementStates cellState, object value, object formattedValue, string errorText,\n"
		source += "	 DataGridViewCellStyle cellStyle, DataGridViewAdvancedBorderStyle advancedBorderStyle, DataGridViewPaintParts paintParts)\n"
		source += "	 {\n"
		source += "	 // Paint the base content\n"
		source += "	 if (this.ImageTextCellColumn.HighQuality)\n"
		source += "	 {\n"
		source += "	 graphics.InterpolationMode = System.Drawing.Drawing2D.InterpolationMode.HighQualityBicubic;\n"
		source += "	 graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.HighQuality;\n"
		source += "	 }\n"
		source += "	 base.Paint(graphics, clipBounds, cellBounds, rowIndex,\n"
		source += "	 cellState, value, formattedValue, errorText,\n"
		source += "	 cellStyle, advancedBorderStyle, paintParts);\n"
		source += "	 if (this.ShowLabel && this.Label != null)\n"
		source += "	 {\n"
		source += "	 // Draw the image clipped to the cell.\n"
		source += "	 System.Drawing.Drawing2D.GraphicsContainer container = graphics.BeginContainer();\n"
		source += "	 SizeF ss = graphics.MeasureString(this.Label, cellStyle.Font,\n"
		source += "	 new SizeF(cellBounds.Width, cellBounds.Height), this.ImageTextCellColumn.StringFormat);\n"
		source += "	 ss = new SizeF((float)Math.Round(ss.Width), (float)Math.Round(ss.Height));\n"
		source += "	 ss = SizeF.Add(ss, new SizeF(0, 2));\n"
		source += "	 Single px = cellBounds.X;\n"
		source += "	 Single py = cellBounds.Y;\n"
		source += "	 switch (this.ImageTextCellColumn.StringFormat.LineAlignment)\n"
		source += "	 {\n"
		source += "	 case StringAlignment.Far:\n"
		source += "	 {\n"
		source += "	 py = (cellBounds.Height - ss.Height) + cellBounds.Y;\n"
		source += "	 break;\n"
		source += "	 }\n"
		source += "	 case StringAlignment.Center:\n"
		source += "	 {\n"
		source += "	 py = (cellBounds.Height - ss.Height) / 2 + cellBounds.Y;\n"
		source += "	 break;\n"
		source += "	 }\n"
		source += "	 }\n"
		source += "	 Rectangle rect = new Rectangle((int)px, (int)py, (int)cellBounds.Width, (int)ss.Height);\n"
		source += "	 graphics.SetClip(rect);\n"
		source += "	 graphics.FillRectangle(new SolidBrush(this.LabelBackColor), rect);\n"
		source += "	 graphics.DrawString(this.Label, cellStyle.Font, new SolidBrush(this.LabelForeColor), \n"
		source += "	 (RectangleF)cellBounds, this.ImageTextCellColumn.StringFormat);\n"
		source += "	 graphics.EndContainer(container);\n"
		source += "	 }\n"
		source += "	 }\n"
		source += "	 public ImageTextCellColumn ImageTextCellColumn\n"
		source += "	 {\n"
		source += "	 get { return this.OwningColumn as ImageTextCellColumn; }\n"
		source += "	 }\n"
		source += "	}\n"
		source += "}\n"
		return compileCSharpAsm( source )


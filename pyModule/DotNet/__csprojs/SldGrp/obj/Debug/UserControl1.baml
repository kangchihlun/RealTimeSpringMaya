   M S B A M L   `   `   `  ����A  =SldGrp, Version=1.0.0.0, Culture=neutral, PublicKeyToken=nullclr-namespace:SldGrpSldGrp  5          SldGrp.UserControl1   5      \ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5      R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5      Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5      @d2http://schemas.microsoft.com/expression/blend/2008     5      "cclr-namespace:SldGrp     5        � 	Resources  5
        SldGrp.RoundingConverter   RoundingConverter��%   &	          5   
   6   5      .��5      �  � ColumnDefinitions 5   
   �� 5      $
��119* �6   6.   �� 5      $	��59* �6   6-   .+�5   
   �� -   5        $��sldValue��5      $��0��6!    � Minimum$ 0Q�61    � Maximum$	 100Q�6=   $��Center=�6K   6g   �� 5   
   -   5         ��Name$ txtSliderValue��5      $��1��6+   {�.  $��19��6N    �� Left$ 0��6Z   
 �� Top$ 25��6j   $��5q�6z   ��5      ��  �� ElementName$ sldValue�� �� Path$ Value�	 �� 	Converter#	 [  .��6r   
 � ToolTip$
 
fishy fish��5      .��5      5      5      
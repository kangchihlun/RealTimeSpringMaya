/*
Copyright (c) 2010, Daniel De Sousa (daniel@dandesousa.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE
 */
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Controls.Primitives;

namespace PhoenixControlLib
{
   /// <summary>
   /// Follow steps 1a or 1b and then 2 to use this custom control in a XAML file.
   ///
   /// Step 1a) Using this custom control in a XAML file that exists in the current project.
   /// Add this XmlNamespace attribute to the root element of the markup file where it is 
   /// to be used:
   ///
   ///     xmlns:MyNamespace="clr-namespace:PhoenixControlLib"
   ///
   ///
   /// Step 1b) Using this custom control in a XAML file that exists in a different project.
   /// Add this XmlNamespace attribute to the root element of the markup file where it is 
   /// to be used:
   ///
   ///     xmlns:MyNamespace="clr-namespace:PhoenixControlLib;assembly=PhoenixControlLib"
   ///
   /// You will also need to add a project reference from the project where the XAML file lives
   /// to this project and Rebuild to avoid compilation errors:
   ///
   ///     Right click on the target project in the Solution Explorer and
   ///     "Add Reference"->"Projects"->[Select this project]
   ///
   ///
   /// Step 2)
   /// Go ahead and use your control in the XAML file.
   ///
   ///     <MyNamespace:CustomControl1/>
   ///
   /// </summary>
   [TemplatePart(Name = NumericSpinnerControl.ElementNumericTextBox, Type = typeof(TextBox))]
   [TemplatePart(Name = NumericSpinnerControl.ElementIncrementButton, Type = typeof(Button))]
   [TemplatePart(Name = NumericSpinnerControl.ElementDecrementButton, Type = typeof(Button))]
   public class NumericSpinnerControl : RangeBase
   {
      #region Constants / Part Definitions

      private const string ElementNumericTextBox = "PART_NumericTextBox";
      private const string ElementIncrementButton = "PART_IncrementButton";
      private const string ElementDecrementButton = "PART_DecrementButton";

      private static double MIN_INTERVAL = 0.01;
      private static double DEFAULT_INTERVAL = 1.0;

      #endregion

      #region Data / UI Controls

      private TextBox numericTextBox;
      private Button incrementButton, decrementButton;

      #endregion

      #region Dependency Properties



      public int Precision
      {
         get { return (int)GetValue(PrecisionProperty); }
         set { SetValue(PrecisionProperty, value); }
      }

      // Using a DependencyProperty as the backing store for Precision.  This enables animation, styling, binding, etc...
      public static readonly DependencyProperty PrecisionProperty =
          DependencyProperty.Register("Precision", typeof(int), typeof(NumericSpinnerControl), new PropertyMetadata(2));

      

      public double IncrementValue
      {
         get { return (double)GetValue(IncrementValueProperty); }
         set { SetValue(IncrementValueProperty, value); }
      }

      // Using a DependencyProperty as the backing store for IncrementValue.  This enables animation, styling, binding, etc...
      public static readonly DependencyProperty IncrementValueProperty =
          DependencyProperty.Register("IncrementValue", typeof(double),
          typeof(NumericSpinnerControl),
          new FrameworkPropertyMetadata(DEFAULT_INTERVAL,
             new PropertyChangedCallback(NumericSpinnerControl.OnIntervalTimeChanged),
             new CoerceValueCallback(NumericSpinnerControl.CoerceInterval)),
             new ValidateValueCallback(NumericSpinnerControl.isValidInterval));

      #endregion

      #region Dependency Property Callbacks

      private static bool isValidInterval(object value)
      {
         double val = (double)value;

         return val >= MIN_INTERVAL;
      }

      private static object CoerceInterval(DependencyObject d, object value)
      {
         double val = (double)value;

         if (val < MIN_INTERVAL)
            return MIN_INTERVAL;
         else
            return val;
      }

      protected static void OnIntervalTimeChanged(DependencyObject d, DependencyPropertyChangedEventArgs args)
      {
      }

      #endregion

      public NumericSpinnerControl()
      {
          this.Maximum = double.MaxValue;
          this.Minimum = 0.0;
      }

      static NumericSpinnerControl()
      {
         DefaultStyleKeyProperty.OverrideMetadata(typeof(NumericSpinnerControl), new FrameworkPropertyMetadata(typeof(NumericSpinnerControl)));
      }

      /// <summary>
      /// When applying the template, load the parts into the data fields 
      /// of this Custom Control
      /// </summary>
      public override void OnApplyTemplate()
      {
         base.OnApplyTemplate();

         numericTextBox = GetTemplateChild(ElementNumericTextBox) as TextBox;
         if (numericTextBox != null)
         {
            numericTextBox.IsReadOnly = true;
            Binding tbBinding = new Binding("Value");
            tbBinding.Source = this;
            tbBinding.Mode = BindingMode.TwoWay;
            tbBinding.StringFormat = "{0:F" + Precision + "}";
            numericTextBox.SetBinding(TextBox.TextProperty, tbBinding);
         }

         incrementButton = GetTemplateChild(ElementIncrementButton) as Button;
         if (incrementButton != null)
         {
            incrementButton.Click += new RoutedEventHandler(incrementButton_Click);
         }

         decrementButton = GetTemplateChild(ElementDecrementButton) as Button;
         if (decrementButton != null)
         {
            decrementButton.Click += new RoutedEventHandler(decrementButton_Click);
         }
      }

      void incrementButton_Click(object sender, RoutedEventArgs e)
      {
         this.Value += this.IncrementValue;
      }

      void decrementButton_Click(object sender, RoutedEventArgs e)
      {
         this.Value -= this.IncrementValue;
      }
   }
}

"""GUI calculator application using tkinter."""

import tkinter as tk
from tkinter import font, ttk
from typing import Optional
from .converter import UnitConverter


class CalculatorGUI:
    """GUI calculator with tkinter interface."""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.resizable(False, False)
        
        # Calculator state
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.conversion_mode = False
        
        # Create GUI components
        self._create_conversion_tab()
        self._create_buttons()
        
        # Bind keyboard events
        self._bind_keyboard()
    
    def _create_conversion_tab(self):
        """Create unit conversion interface."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        
        # Calculator tab
        calc_frame = tk.Frame(self.notebook)
        self.notebook.add(calc_frame, text="Calculator")
        
        # Move existing display and buttons to calc frame
        self.display_frame = tk.Frame(calc_frame, bg="black", padx=10, pady=10)
        self.display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        
        # Conversion tab
        conv_frame = tk.Frame(self.notebook)
        self.notebook.add(conv_frame, text="Convert")
        
        self._create_conversion_interface(conv_frame)
        
        # Update display creation
        self._update_display_for_tab()
    
    def _update_display_for_tab(self):
        """Update display to work with tab system."""
        # Result label
        result_font = font.Font(family="Arial", size=24, weight="bold")
        result_label = tk.Label(
            self.display_frame,
            textvariable=self.result_var,
            font=result_font,
            bg="black",
            fg="white",
            anchor="e"
        )
        result_label.pack(fill="both", expand=True)
    
    def _create_conversion_interface(self, parent):
        """Create unit conversion interface."""
        # Value input
        tk.Label(parent, text="Value:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.conv_value = tk.Entry(parent, font=("Arial", 12), width=15)
        self.conv_value.grid(row=0, column=1, padx=5, pady=5)
        
        # From unit
        tk.Label(parent, text="From:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.conv_from = ttk.Combobox(parent, font=("Arial", 12), width=13, state="readonly")
        self.conv_from.grid(row=1, column=1, padx=5, pady=5)
        
        # To unit
        tk.Label(parent, text="To:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
        self.conv_to = ttk.Combobox(parent, font=("Arial", 12), width=13, state="readonly")
        self.conv_to.grid(row=2, column=1, padx=5, pady=5)
        
        # Category selection
        tk.Label(parent, text="Category:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
        self.conv_category = ttk.Combobox(parent, font=("Arial", 12), width=13, state="readonly")
        self.conv_category['values'] = ['length', 'weight', 'temperature']
        self.conv_category.set('length')
        self.conv_category.grid(row=3, column=1, padx=5, pady=5)
        self.conv_category.bind('<<ComboboxSelected>>', self._update_unit_options)
        
        # Convert button
        convert_btn = tk.Button(parent, text="Convert", font=("Arial", 12), 
                               command=self._perform_conversion, bg="#ff9500", fg="white")
        convert_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        
        # Result display
        self.conv_result = tk.StringVar()
        self.conv_result.set("Result: ")
        result_label = tk.Label(parent, textvariable=self.conv_result, 
                               font=("Arial", 14, "bold"), bg="white")
        result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
        # Initialize unit options
        self._update_unit_options()
    
    def _update_unit_options(self, event=None):
        """Update unit options based on selected category."""
        category = self.conv_category.get()
        units = UnitConverter.get_supported_units()
        
        if category in units:
            unit_list = units[category]
            self.conv_from['values'] = unit_list
            self.conv_to['values'] = unit_list
            if unit_list:
                self.conv_from.set(unit_list[0])
                self.conv_to.set(unit_list[1] if len(unit_list) > 1 else unit_list[0])
    
    def _perform_conversion(self):
        """Perform unit conversion."""
        try:
            value = float(self.conv_value.get())
            from_unit = self.conv_from.get()
            to_unit = self.conv_to.get()
            
            result = UnitConverter.convert(value, from_unit, to_unit)
            
            # Format result
            if isinstance(result, float) and result.is_integer():
                self.conv_result.set(f"Result: {int(result)} {to_unit}")
            else:
                self.conv_result.set(f"Result: {result:.4f} {to_unit}")
                
        except ValueError as e:
            self.conv_result.set(f"Error: {e}")
        except Exception as e:
            self.conv_result.set(f"Error: {e}")
    
    def _create_display(self):
        """Create the display area."""
        # Display is now created in _create_conversion_tab
        pass
    
    def _create_buttons(self):
        """Create calculator buttons."""
        button_config = [
            ("C", 1, 0, "clear"), ("±", 1, 1, "negate"), ("%", 1, 2, "percent"), ("÷", 1, 3, "divide"),
            ("7", 2, 0, "7"), ("8", 2, 1, "8"), ("9", 2, 2, "9"), ("×", 2, 3, "multiply"),
            ("4", 3, 0, "4"), ("5", 3, 1, "5"), ("6", 3, 2, "6"), ("−", 3, 3, "subtract"),
            ("1", 4, 0, "1"), ("2", 4, 1, "2"), ("3", 4, 2, "3"), ("+", 4, 3, "add"),
            ("0", 5, 0, "0"), (".", 5, 1, "decimal"), ("⌫", 5, 2, "backspace"), ("=", 5, 3, "equals")
        ]
        
        button_font = font.Font(family="Arial", size=16)
        
        for text, row, col, action in button_config:
            # Determine button color
            if text in "C±%⌫":
                bg_color = "#e0e0e0"
                fg_color = "black"
            elif text in "÷×−+=":
                bg_color = "#ff9500"
                fg_color = "white"
            else:
                bg_color = "#f0f0f0"
                fg_color = "black"
            
            # Create button
            btn = tk.Button(
                self.window,
                text=text,
                font=button_font,
                bg=bg_color,
                fg=fg_color,
                relief="raised",
                bd=2,
                command=lambda a=action: self._button_click(a)
            )
            
            # Special width for 0 button
            if text == "0":
                btn.grid(row=row+1, column=col, columnspan=2, sticky="nsew", padx=2, pady=2)
            else:
                btn.grid(row=row+1, column=col, sticky="nsew", padx=2, pady=2)
            
            # Configure grid weights
            self.window.grid_rowconfigure(row+1, weight=1)
            self.window.grid_columnconfigure(col, weight=1)
    
    def _bind_keyboard(self):
        """Bind keyboard events to calculator functions."""
        self.window.bind('<Key>', self._keyboard_input)
        self.window.bind('<Return>', lambda e: self._button_click("equals"))
        self.window.bind('<Escape>', lambda e: self._button_click("clear"))
        self.window.bind('<BackSpace>', lambda e: self._button_click("backspace"))
    
    def _keyboard_input(self, event):
        """Handle keyboard input."""
        key = event.char
        
        if key.isdigit() or key == '.':
            self._button_click(key)
        elif key == '+':
            self._button_click("add")
        elif key == '-':
            self._button_click("subtract")
        elif key == '*':
            self._button_click("multiply")
        elif key == '/':
            self._button_click("divide")
    
    def _button_click(self, action: str):
        """Handle button clicks."""
        try:
            if action.isdigit():
                self._append_digit(action)
            elif action == "decimal":
                self._append_decimal()
            elif action == "clear":
                self._clear()
            elif action == "backspace":
                self._backspace()
            elif action == "negate":
                self._negate()
            elif action == "percent":
                self._percent()
            elif action in ["add", "subtract", "multiply", "divide"]:
                self._set_operator(action)
            elif action == "equals":
                self._calculate()
        except Exception:
            self.result_var.set("Error")
    
    def _append_digit(self, digit: str):
        """Append a digit to the current input."""
        if self.result_var.get() == "0":
            self.result_var.set(digit)
        else:
            current = self.result_var.get()
            self.result_var.set(current + digit)
    
    def _append_decimal(self):
        """Append decimal point."""
        current = self.result_var.get()
        if "." not in current:
            self.result_var.set(current + ".")
    
    def _clear(self):
        """Clear the display."""
        self.result_var.set("0")
    
    def _backspace(self):
        """Remove last character."""
        current = self.result_var.get()
        if len(current) > 1:
            self.result_var.set(current[:-1])
        else:
            self.result_var.set("0")
    
    def _negate(self):
        """Negate the current number."""
        current = self.result_var.get()
        if current != "0":
            if current.startswith("-"):
                self.result_var.set(current[1:])
            else:
                self.result_var.set("-" + current)
    
    def _percent(self):
        """Convert to percentage."""
        try:
            current = float(self.result_var.get())
            result = current / 100
            self.result_var.set(str(result))
        except ValueError:
            self.result_var.set("Error")
    
    def _set_operator(self, operator: str):
        """Set the operator for calculation."""
        current = self.result_var.get()
        if not current.endswith(" "):
            operator_symbols = {
                "add": "+",
                "subtract": "-",
                "multiply": "*",
                "divide": "/"
            }
            self.result_var.set(current + f" {operator_symbols[operator]} ")
    
    def _calculate(self):
        """Perform the calculation."""
        try:
            expression = self.result_var.get()
            # Replace display symbols with Python operators
            expression = expression.replace("×", "*").replace("÷", "/")
            
            result = eval(expression)
            
            # Format result
            if isinstance(result, float) and result.is_integer():
                self.result_var.set(str(int(result)))
            else:
                self.result_var.set(str(result))
        except Exception:
            self.result_var.set("Error")
    
    def run(self):
        """Start the GUI application."""
        self.window.mainloop()


def main():
    """Main function for GUI calculator."""
    app = CalculatorGUI()
    app.run()


if __name__ == "__main__":
    main()
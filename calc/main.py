"""Terminal-based calculator application."""

import re
import sys
from typing import Union
from .converter import UnitConverter


class Calculator:
    """Simple calculator supporting basic arithmetic operations."""
    
    def evaluate(self, expression: str) -> Union[float, int]:
        """
        Evaluate a mathematical expression.
        
        Args:
            expression: Mathematical expression to evaluate
            
        Returns:
            Result of the evaluation
            
        Raises:
            ValueError: If expression is invalid
        """
        # Remove whitespace and convert to lowercase
        expression = expression.replace(' ', '').lower()
        
        # Validate expression
        if not self._is_valid_expression(expression):
            raise ValueError("Invalid mathematical expression")
        
        try:
            # Use eval for simple arithmetic (safe in this controlled context)
            result = eval(expression)
            return result
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {e}")
    
    def _is_valid_expression(self, expression: str) -> bool:
        """Validate that expression contains only allowed characters."""
        # Allow numbers, operators, parentheses, and decimal points
        pattern = r'^[0-9+\-*/().]+$'
        return bool(re.match(pattern, expression))


def print_help():
    """Print help information."""
    help_text = """
Terminal Calculator - Help

Supported operations:
    + : Addition
    - : Subtraction
    * : Multiplication
    / : Division
    ( ) : Parentheses for grouping

Unit conversions:
    100 ft to m : Convert 100 feet to meters
    5 lb to kg : Convert 5 pounds to kilograms
    32 f to c : Convert 32 Fahrenheit to Celsius

Examples:
    2 + 3
    10 * 5
    (2 + 3) * 4
    10 / 2
    3.14 * 2
    100 ft to m

Commands:
    help : Show this help message
    units : Show supported units
    quit : Exit the calculator
    exit : Exit the calculator
"""
    print(help_text)


def print_units():
    """Print supported units."""
    units = UnitConverter.get_supported_units()
    
    print("\nSupported Units:")
    print("-" * 20)
    
    for category, unit_list in units.items():
        print(f"\n{category.title()}: {', '.join(unit_list)}")
    
    print("\nConversion format: value unit to unit")
    print("Example: 100 ft to m")


def main():
    """Main calculator application loop."""
    calculator = Calculator()
    
    print("Terminal Calculator")
    print("Type 'help' for commands or 'quit' to exit")
    print("-" * 40)
    
    while True:
        try:
            # Get user input
            user_input = input("calc> ").strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            elif user_input.lower() == 'help':
                print_help()
                continue
            elif user_input.lower() == 'units':
                print_units()
                continue
            
            # Check for unit conversion
            if ' to ' in user_input.lower():
                try:
                    value, from_unit, to_unit = UnitConverter.parse_conversion(user_input)
                    result = UnitConverter.convert(value, from_unit, to_unit)
                    
                    # Format output
                    if isinstance(result, float) and result.is_integer():
                        print(f"= {int(result)} {to_unit}")
                    else:
                        print(f"= {result} {to_unit}")
                    continue
                except ValueError as e:
                    print(f"Conversion error: {e}")
                    continue
            
            # Evaluate expression
            result = calculator.evaluate(user_input)
            
            # Format output (remove .0 for whole numbers)
            if isinstance(result, float) and result.is_integer():
                print(f"= {int(result)}")
            else:
                print(f"= {result}")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
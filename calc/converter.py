"""Unit conversion utilities for calculator."""

from typing import Dict, Tuple


class UnitConverter:
    """Handles unit conversions for various measurement types."""
    
    # Length conversions (to meters)
    LENGTH_UNITS: Dict[str, float] = {
        'mm': 0.001,
        'cm': 0.01,
        'm': 1.0,
        'km': 1000.0,
        'in': 0.0254,
        'ft': 0.3048,
        'yd': 0.9144,
        'mi': 1609.344
    }
    
    # Weight conversions (to kilograms)
    WEIGHT_UNITS: Dict[str, float] = {
        'mg': 0.000001,
        'g': 0.001,
        'kg': 1.0,
        'oz': 0.0283495,
        'lb': 0.453592,
        'ton': 907.185
    }
    
    # Temperature conversions (special handling)
    TEMP_UNITS = ['c', 'f', 'k']
    
    @classmethod
    def convert_length(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Convert length units."""
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        if from_unit not in cls.LENGTH_UNITS or to_unit not in cls.LENGTH_UNITS:
            raise ValueError(f"Unsupported length unit. Supported: {list(cls.LENGTH_UNITS.keys())}")
        
        # Convert to meters first, then to target unit
        meters = value * cls.LENGTH_UNITS[from_unit]
        result = meters / cls.LENGTH_UNITS[to_unit]
        return result
    
    @classmethod
    def convert_weight(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Convert weight units."""
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        if from_unit not in cls.WEIGHT_UNITS or to_unit not in cls.WEIGHT_UNITS:
            raise ValueError(f"Unsupported weight unit. Supported: {list(cls.WEIGHT_UNITS.keys())}")
        
        # Convert to kilograms first, then to target unit
        kg = value * cls.WEIGHT_UNITS[from_unit]
        result = kg / cls.WEIGHT_UNITS[to_unit]
        return result
    
    @classmethod
    def convert_temperature(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature units."""
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        if from_unit not in cls.TEMP_UNITS or to_unit not in cls.TEMP_UNITS:
            raise ValueError(f"Unsupported temperature unit. Supported: {cls.TEMP_UNITS}")
        
        # Convert to Celsius first
        celsius = 0.0
        if from_unit == 'c':
            celsius = value
        elif from_unit == 'f':
            celsius = (value - 32) * 5/9
        elif from_unit == 'k':
            celsius = value - 273.15
        
        # Convert from Celsius to target
        if to_unit == 'c':
            return celsius
        elif to_unit == 'f':
            return celsius * 9/5 + 32
        elif to_unit == 'k':
            return celsius + 273.15
        else:
            raise ValueError("Unsupported temperature unit")
    
    @classmethod
    def parse_conversion(cls, expression: str) -> Tuple[float, str, str]:
        """Parse conversion expression like '100 ft to m'."""
        parts = expression.lower().split()
        
        if len(parts) < 4 or parts[2] != 'to':
            raise ValueError("Invalid conversion format. Use: 'value unit to unit'")
        
        try:
            value = float(parts[0])
        except ValueError:
            raise ValueError("Invalid number in conversion")
        
        from_unit = parts[1]
        to_unit = parts[3]
        
        return value, from_unit, to_unit
    
    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Perform unit conversion."""
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        # Determine conversion type
        if from_unit in cls.LENGTH_UNITS and to_unit in cls.LENGTH_UNITS:
            return cls.convert_length(value, from_unit, to_unit)
        elif from_unit in cls.WEIGHT_UNITS and to_unit in cls.WEIGHT_UNITS:
            return cls.convert_weight(value, from_unit, to_unit)
        elif from_unit in cls.TEMP_UNITS and to_unit in cls.TEMP_UNITS:
            return cls.convert_temperature(value, from_unit, to_unit)
        else:
            raise ValueError("Cannot convert between different unit types")
    
    @classmethod
    def get_supported_units(cls) -> Dict[str, list]:
        """Get all supported units by category."""
        return {
            'length': list(cls.LENGTH_UNITS.keys()),
            'weight': list(cls.WEIGHT_UNITS.keys()),
            'temperature': cls.TEMP_UNITS
        }
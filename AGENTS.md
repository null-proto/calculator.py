# Calculator Project

Terminal and GUI calculator applications built with Python and Poetry.

## Project Structure

```
calc.py/
├── pyproject.toml          # Poetry configuration
├── calc/
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Terminal calculator application
│   ├── gui.py              # GUI calculator application
│   └── converter.py        # Unit conversion utilities
└── AGENTS.md               # This file
```

## Setup

1. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

## Usage

### Running the Calculator

#### Terminal Calculator

1. Using Poetry (recommended):
   ```bash
   poetry run calc
   ```

2. Using the script directly:
   ```bash
   python -m calc.main
   ```

#### GUI Calculator

1. Using Poetry (recommended):
   ```bash
   poetry run gui
   ```

2. Using the script directly:
   ```bash
   python -m calc.gui
   ```

### Calculator Features

#### Terminal Calculator
- **Basic Operations**: Addition (+), Subtraction (-), Multiplication (*), Division (/)
- **Parentheses**: Support for grouping expressions
- **Decimal Numbers**: Floating-point arithmetic
- **Unit Conversions**: Convert between units using "value unit to unit" format
- **Commands**: 
  - `help` - Show help information
  - `units` - Show supported units for conversion
  - `quit` or `exit` - Exit the calculator

#### GUI Calculator
- **Basic Operations**: Addition (+), Subtraction (-), Multiplication (×), Division (÷)
- **Decimal Numbers**: Floating-point arithmetic
- **Additional Functions**: 
  - Clear (C)
  - Backspace (⌫)
  - Negate (±)
  - Percent (%)
- **Unit Conversions**: Tabbed interface for converting length, weight, and temperature
- **Keyboard Support**: Use keyboard for numbers and operators
- **Visual Interface**: Button-based calculator with display

### Examples

```
calc> 2 + 3
= 5

calc> 10 * 5
= 50

calc> (2 + 3) * 4
= 20

calc> 10 / 2
= 5

calc> 3.14 * 2
= 6.28

calc> 100 ft to m
= 30.48 m

calc> 5 lb to kg
= 2.27 kg
```

## Development

### Running Tests

Currently no tests are implemented. To add tests:

1. Create a `tests/` directory
2. Add test files using pytest
3. Update pyproject.toml with test dependencies

### Code Style

The project follows standard Python conventions. To run linting:

```bash
poetry run flake8 calc/
```

## Architecture

- **Calculator Class**: Core evaluation logic with input validation
- **Main Function**: Interactive terminal interface
- **GUI Class**: Tkinter-based graphical interface with tabbed layout
- **UnitConverter Class**: Handles unit conversions for length, weight, and temperature
- **Error Handling**: Graceful handling of invalid expressions and user interruptions

## Dependencies

- Python 3.8+
- Poetry (for dependency management)
- No external runtime dependencies (uses only Python standard library)
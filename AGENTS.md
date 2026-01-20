# Calculator Project

Terminal and GUI calculator applications built with Python and Poetry.

## Project Structure

```
calc.py/
├── pyproject.toml          # Poetry configuration
├── calc/
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Terminal calculator application
│   └── gui.py              # GUI calculator application
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
- **Commands**: 
  - `help` - Show help information
  - `quit` or `exit` - Exit the calculator

#### GUI Calculator
- **Basic Operations**: Addition (+), Subtraction (-), Multiplication (×), Division (÷)
- **Decimal Numbers**: Floating-point arithmetic
- **Additional Functions**: 
  - Clear (C)
  - Backspace (⌫)
  - Negate (±)
  - Percent (%)
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
- **GUI Class**: Tkinter-based graphical interface
- **Error Handling**: Graceful handling of invalid expressions and user interruptions

## Dependencies

- Python 3.8+
- Poetry (for dependency management)
- No external runtime dependencies (uses only Python standard library)
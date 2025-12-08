---
inclusion: always
---

# Advent of Code Project Standards

## Workflow for New Day Solutions

### Phase 1: Setup and Discussion
When receiving a new day's problem:
1. Create the day folder structure
2. Update the master README with the new day
3. Create the day's README with the problem description
4. Create placeholder files (example.txt, input.txt, solution.py, test_solution.py)
5. **STOP and discuss the problem with Cooper before implementing**
   - Analyse the problem structure
   - Discuss potential approaches
   - Consider edge cases and complexity
   - Agree on the solution strategy

### Phase 2: Implementation
After discussing and agreeing on the approach, proceed with implementation.

## When Creating New Day Solutions

Every new day solution MUST include:

### 1. Update Master README
- Add the new day to the structure section in `README.md`
- Include a brief one-line description of the puzzle

### 2. CLI Interface with sys.argv or argparse
- **Simple scripts:** Use `sys.argv` for straightforward input file + optional parameters
- **Complex scripts:** Use `argparse` for multiple flags and options
- Accept `input_file` as a positional argument
- Include optional parameters for puzzle-specific values (e.g., num_edges, iterations)
- Provide clear usage message when arguments are missing

Simple example (sys.argv):
```
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python solution.py <input_file> [optional_param]")
        print("Example: python solution.py example.txt 10")
        sys.exit(1)
    
    filename = sys.argv[1]
    param = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    
    result = solve(filename, param)
    print(f"Result: {result}")
```

Complex example (argparse):
```
def main():
    parser = argparse.ArgumentParser(description="Day X: Title - Description")
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")
    args = parser.parse_args()
    
    result = solve(args.input_file, args.debug)
    print(f"\nResult: {result}")
```

### 3. Comprehensive Test Suite
- Create `test_<module>.py` with unittest
- Test individual functions with multiple cases
- Test edge cases and boundary conditions
- Test with the example input file
- Aim for thorough coverage of the logic

Test structure:
- One test class per function
- Descriptive test method names
- Include docstrings explaining what's being tested
- Test the example file result as integration test

### 4. File Structure
Each day directory should contain:
- `README.md` - Problem description and examples
- `<solution>.py` - Main solution with CLI interface
- `test_<solution>.py` - Comprehensive test suite
- `example.txt` - Example input from puzzle
- `input.txt` - Actual puzzle input (or placeholder)

## Running Solutions

Solutions should be runnable with input file as argument:
```
python dayXX/<solution>.py example.txt
python dayXX/<solution>.py input.txt
python dayXX/<solution>.py example.txt 10  # with optional parameter
```

Or from parent directory:
```
python dayXX/<solution>.py dayXX/example.txt
```

Tests should be runnable as:
```
python -m pytest dayXX/test_<solution>.py -v
```

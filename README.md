# Logic Reduction Program

**Find the minimum set of test cases for 100% boolean expression coverage**

This program solves the Set Cover problem to find the minimal number of test cases needed to achieve complete coverage of boolean expressions. It's designed to help optimize test suites by dramatically reducing the number of tests while maintaining full coverage.

## 🎯 Key Features

- **String Expression Input**: Input expressions as simple strings like `['A and B', 'A and not C']`
- **Multiple Algorithms**: Greedy, Intelligent, Heuristic, and Optimal Set Cover algorithms
- **Significant Reduction**: Achieve 75%+ test case reduction in most scenarios
- **Coverage Analysis**: Detailed branch coverage tracking and visualization
- **AST Parsing**: Direct analysis of Python if/else statements in source code

## 🚀 Quick Start

### Simple Usage (Recommended)

```python
from string_expression_reducer import reduce_string_expressions

# Your boolean expressions
expressions = [
    "(A or B) and C",
    "A and B", 
    "A and not C"
]

# Find minimum test cases
reduce_string_expressions(expressions)
```

**Output:**
```
Minimum test cases needed: 2/8
Reduction: 75.0%
Coverage: 100.0%

SELECTED TEST CASES:
  Test 1: A=False,B=True,C=True    → Makes exp1 True
  Test 2: A=True,B=True,C=False    → Makes exp2, exp3 True
```

## 📊 Results Example

For expressions `(A or B) and C`, `A and B`, `A and not C`:
- **Before**: 8 possible test cases
- **After**: 2 optimal test cases  
- **Reduction**: 75%
- **Coverage**: 100%

## 🛠 Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:StevenJWChen/logic_reduction.git
   cd logic_reduction
   ```

2. **Run directly (no dependencies):**
   ```bash
   python string_expression_reducer.py
   ```

## 📁 File Structure

### Core Files
- **`string_expression_reducer.py`** - Main interface for string expression input
- **`core_reduction_functions.py`** - Set Cover algorithm implementations
- **`logic_parser.py`** - AST parsing for Python source code analysis
- **`coverage_analyzer.py`** - Coverage matrix generation and analysis

### Algorithm Files  
- **`main.py`** - Command-line interface for file-based analysis
- **`test_reducer.py`** - Class-based reduction system
- **`simple_expression_reducer.py`** - Function-based expression input

### Examples
- **`direct_expressions_only.py`** - IF-branch-only testing
- **`analyze_user_expressions.py`** - Manual analysis tools
- **`demonstrate_reduction.py`** - Algorithm demonstrations

## 🧮 Supported Algorithms

1. **Greedy Algorithm** - Fast approximation (≤ ln(m) × optimal)
2. **Intelligent Algorithm** - Considers branch rarity for better selection
3. **Heuristic Algorithm** - Greedy + local optimization
4. **Optimal Algorithm** - Exhaustive search for small problems (<16 test cases)

## 💡 Use Cases

- **Test Suite Optimization** - Reduce test execution time
- **Code Coverage Analysis** - Find minimal test sets for full coverage  
- **Boolean Logic Testing** - Systematic testing of complex conditions
- **Regression Testing** - Maintain coverage with fewer tests

## 🔧 Advanced Usage

### Analyze Python Source Code
```python
from main import main
main('path/to/your/file.py')
```

### Use Different Algorithms
```python
from core_reduction_functions import greedy_set_cover, optimal_set_cover

# Build your coverage matrix
coverage_matrix = [[True, False], [False, True]]
test_names = ["test1", "test2"] 
branch_names = ["branch1", "branch2"]

# Apply algorithms
selected_tests, coverage, reduction = greedy_set_cover(coverage_matrix, test_names, branch_names)
```

## 📈 Performance

- **Small problems** (<16 tests): Uses optimal algorithm
- **Large problems** (≥16 tests): Uses greedy algorithm
- **Typical reductions**: 50-90% fewer test cases
- **Runtime**: Near-instantaneous for most practical problems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## 📚 Documentation

- **[User Guide](USER_GUIDE.md)** - Detailed usage instructions
- **[Examples](EXAMPLES.md)** - Practical examples and use cases
- **[CLAUDE.md](CLAUDE.md)** - Development notes and technical details

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🔗 Links

- **Repository**: https://github.com/StevenJWChen/logic_reduction
- **Issues**: https://github.com/StevenJWChen/logic_reduction/issues

---

**Built for developers who need to optimize test coverage efficiently** 🚀
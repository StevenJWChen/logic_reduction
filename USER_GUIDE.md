# User Guide - Logic Reduction Program

This guide provides detailed instructions on how to use the Logic Reduction Program effectively.

## Table of Contents

1. [Getting Started](#getting-started)
2. [String Expression Input](#string-expression-input)
3. [Source Code Analysis](#source-code-analysis)
4. [Understanding the Output](#understanding-the-output)
5. [Algorithm Selection](#algorithm-selection)
6. [Detailed Algorithm Documentation](#detailed-algorithm-documentation)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites
- Python 3.6 or higher
- No external dependencies required

### Installation
```bash
git clone git@github.com:StevenJWChen/logic_reduction.git
cd logic_reduction
```

## String Expression Input

### Basic Usage

The most common use case is inputting boolean expressions as strings:

```python
from string_expression_reducer import reduce_string_expressions

# Define your expressions
expressions = [
    "A and B",
    "A or B", 
    "not A"
]

# Find minimum test cases
result = reduce_string_expressions(expressions)
```

### Supported Expression Syntax

The program supports standard Python boolean operators:

- **AND**: `A and B`
- **OR**: `A or B`  
- **NOT**: `not A`
- **Parentheses**: `(A or B) and C`
- **Complex**: `A and not (B or C)`

### Variable Names
- Use any valid Python identifier: `A`, `B`, `C`, `condition1`, `flag_active`
- Case sensitive: `A` and `a` are different variables
- Avoid Python keywords: `and`, `or`, `not`, `True`, `False`

### Example Input Formats

```python
# Simple expressions
expressions = ["X and Y", "X or Y", "not X"]

# Complex expressions  
expressions = [
    "(A or B) and C",
    "A and B and C",
    "not A and (B or C)",
    "(A or B) and not (C and D)"
]

# Real-world examples
expressions = [
    "user_logged_in and has_permission",
    "is_admin or (is_owner and file_exists)",
    "not maintenance_mode and service_available"
]
```

## Source Code Analysis

### Analyzing Python Files

For analyzing existing Python code with if/else statements:

```python
from main import main

# Analyze a Python file
main('path/to/your/file.py')
```

### Example Python File Structure

```python
# example_code.py
def process_user(user_active, is_admin, has_data):
    if user_active and is_admin:
        return "admin_access"
    elif user_active and has_data:
        return "user_access"  
    elif not user_active:
        return "no_access"
    else:
        return "default"
```

The analyzer will:
1. Parse all if/else statements
2. Extract boolean conditions
3. Generate test cases
4. Find minimum coverage set

## Understanding the Output

### Coverage Analysis Section

```
COVERAGE ANALYSIS:
Test Case           | exp 1 | exp 2 | exp 3 | Covers
----------------------------------------------------------
A=F,B=F,C=F         | F     | F     | T     | exp3
A=F,B=T,C=T         | T     | F     | F     | exp1
A=T,B=T,C=F         | F     | T     | T     | exp2, exp3
```

**Explanation:**
- **Test Case**: Variable assignments (F=False, T=True)
- **exp columns**: Whether each expression evaluates to True
- **Covers**: Which expressions this test case satisfies

### Solution Section

```
OPTIMAL SOLUTION:
Minimum test cases needed: 2/8
Reduction: 75.0%
Coverage: 100.0%

SELECTED TEST CASES:
  Test 1: A=F,B=T,C=T
    Makes True: exp1
  Test 2: A=T,B=T,C=F  
    Makes True: exp2, exp3
```

**Key Metrics:**
- **Minimum test cases**: How many tests are needed vs total possible
- **Reduction**: Percentage of tests eliminated  
- **Coverage**: Percentage of expressions covered (should be 100%)

## Algorithm Selection

### Available Algorithms

1. **Optimal Algorithm** (default for ≤16 test cases)
   - Finds the absolute minimum number of test cases
   - Guaranteed best solution
   - Slower for large problems

2. **Greedy Algorithm** (default for >16 test cases)
   - Fast approximation algorithm
   - Usually within ln(m) of optimal solution
   - Works well for large problems

3. **Intelligent Algorithm**
   - Considers branch rarity in selection
   - Good balance of speed and quality

4. **Heuristic Algorithm**  
   - Greedy + local optimization
   - Better results than pure greedy

### Manual Algorithm Selection

```python
from core_reduction_functions import greedy_set_cover, optimal_set_cover

# Build coverage matrix manually
coverage_matrix = [
    [True, False, False],   # Test 1 covers exp1
    [False, True, True],    # Test 2 covers exp2, exp3
    [False, False, True]    # Test 3 covers exp3
]

test_names = ["test1", "test2", "test3"]
branch_names = ["exp1", "exp2", "exp3"]

# Use specific algorithm
selected_tests, coverage_pct, reduction_ratio = greedy_set_cover(
    coverage_matrix, test_names, branch_names
)
```

## Detailed Algorithm Documentation

### The Set Cover Problem

The logic reduction problem is mathematically formulated as the **Set Cover Problem**, a classic NP-hard optimization problem:

**Given:**
- A universe U of elements to cover (boolean expressions)
- A collection S of subsets of U (test cases that satisfy certain expressions)

**Goal:**
Find the minimum number of subsets from S that cover all elements in U.

**In our context:**
- **Universe U**: Set of boolean expressions that must evaluate to True
- **Subsets S**: Test cases (variable assignments)
- **Coverage**: A test case covers an expression if it makes that expression True

### Problem Formulation

#### Step 1: Variable Extraction
```python
def extract_variables(expressions):
    """Extract all unique variables from boolean expressions"""
    variables = set()
    for expr in expressions:
        # Use regex to find variable names (excluding keywords)
        vars_in_expr = re.findall(r'\b[A-Za-z][A-Za-z0-9_]*\b', expr)
        python_keywords = {'and', 'or', 'not', 'True', 'False'}
        vars_in_expr = [v for v in vars_in_expr if v not in python_keywords]
        variables.update(vars_in_expr)
    return sorted(list(variables))
```

#### Step 2: Test Case Generation
```python
from itertools import product

def generate_test_cases(variables):
    """Generate all possible variable assignments"""
    # For n variables, generate 2^n combinations
    all_combinations = list(product([False, True], repeat=len(variables)))
    
    test_cases = []
    for combo in all_combinations:
        test_case = dict(zip(variables, combo))
        test_cases.append(test_case)
    
    return test_cases
```

#### Step 3: Coverage Matrix Construction
```python
def build_coverage_matrix(expressions, test_cases):
    """Build binary matrix M[i][j] where:
    - i = test case index  
    - j = expression index
    - M[i][j] = 1 if test case i makes expression j True, 0 otherwise
    """
    coverage_matrix = []
    
    for test_case in test_cases:
        coverage_row = []
        for expr_str in expressions:
            # Safely evaluate expression with variable assignments
            result = evaluate_expression(expr_str, test_case)
            coverage_row.append(result)
        coverage_matrix.append(coverage_row)
    
    return coverage_matrix
```

### Algorithm Implementations

#### 1. Greedy Algorithm

**Time Complexity**: O(nm log n) where n = test cases, m = expressions  
**Approximation Ratio**: ≤ ln(m) × OPT (within natural log of optimal)

```python
def greedy_set_cover(coverage_matrix, test_names, branch_names):
    """
    Greedy Set Cover Algorithm:
    At each step, select the test case that covers the most uncovered expressions
    """
    n_tests = len(coverage_matrix)
    n_branches = len(coverage_matrix[0]) if coverage_matrix else 0
    
    selected_tests = []
    covered_branches = set()
    all_branches = set(range(n_branches))
    
    available_tests = set(range(n_tests))
    
    # Continue until all branches are covered
    while covered_branches != all_branches and available_tests:
        best_test_idx = None
        best_new_coverage = 0
        
        # Find test case covering most new branches
        for test_idx in available_tests:
            new_branches = set()
            for branch_idx in range(n_branches):
                if (coverage_matrix[test_idx][branch_idx] and 
                    branch_idx not in covered_branches):
                    new_branches.add(branch_idx)
            
            # Select test with maximum new coverage
            if len(new_branches) > best_new_coverage:
                best_new_coverage = len(new_branches)
                best_test_idx = test_idx
        
        if best_test_idx is not None:
            # Add best test to solution
            selected_tests.append(test_names[best_test_idx])
            available_tests.remove(best_test_idx)
            
            # Update covered branches
            for branch_idx in range(n_branches):
                if coverage_matrix[best_test_idx][branch_idx]:
                    covered_branches.add(branch_idx)
        else:
            break
    
    # Calculate metrics
    coverage_pct = (len(covered_branches) / n_branches) * 100 if n_branches > 0 else 0
    reduction_ratio = len(selected_tests) / n_tests if n_tests > 0 else 1
    
    return selected_tests, coverage_pct, reduction_ratio
```

#### 2. Optimal Algorithm (Branch and Bound)

**Time Complexity**: O(2^n) exponential - only practical for small problems  
**Guarantee**: Finds absolute minimum number of test cases

```python
def optimal_set_cover(coverage_matrix, test_names, branch_names, max_combinations=65536):
    """
    Optimal Set Cover using exhaustive search:
    Try all possible combinations of test cases, return minimum that covers all branches
    """
    n_tests = len(coverage_matrix)
    n_branches = len(coverage_matrix[0]) if coverage_matrix else 0
    
    if n_tests == 0 or n_branches == 0:
        return [], 0, 1
    
    # Limit search space for practical computation
    if 2**n_tests > max_combinations:
        return None  # Too large, fall back to greedy
    
    all_branches = set(range(n_branches))
    min_tests = None
    min_test_count = float('inf')
    
    # Try all possible combinations of test cases (2^n combinations)
    for combo_bits in range(1, 2**n_tests):
        # Convert bit pattern to test indices
        test_indices = [i for i in range(n_tests) if combo_bits & (1 << i)]
        
        # Check if this combination covers all branches
        covered_branches = set()
        for test_idx in test_indices:
            for branch_idx in range(n_branches):
                if coverage_matrix[test_idx][branch_idx]:
                    covered_branches.add(branch_idx)
        
        # If this combination achieves full coverage and is smaller
        if covered_branches == all_branches and len(test_indices) < min_test_count:
            min_test_count = len(test_indices)
            min_tests = [test_names[i] for i in test_indices]
    
    if min_tests:
        coverage_pct = 100.0
        reduction_ratio = min_test_count / n_tests
        return min_tests, coverage_pct, reduction_ratio
    
    return [], 0, 1
```

#### 3. Intelligent Algorithm

**Enhancement**: Considers branch rarity for smarter selection

```python
def intelligent_set_cover(coverage_matrix, test_names, branch_names):
    """
    Intelligent Set Cover:
    Prioritizes covering rare branches (branches covered by fewer test cases)
    """
    n_tests = len(coverage_matrix)
    n_branches = len(coverage_matrix[0]) if coverage_matrix else 0
    
    # Calculate branch frequency (how many tests cover each branch)
    branch_frequency = [0] * n_branches
    for test_idx in range(n_tests):
        for branch_idx in range(n_branches):
            if coverage_matrix[test_idx][branch_idx]:
                branch_frequency[branch_idx] += 1
    
    selected_tests = []
    covered_branches = set()
    all_branches = set(range(n_branches))
    available_tests = set(range(n_tests))
    
    while covered_branches != all_branches and available_tests:
        best_test_idx = None
        best_score = 0
        
        for test_idx in available_tests:
            score = 0
            new_branches = 0
            
            for branch_idx in range(n_branches):
                if (coverage_matrix[test_idx][branch_idx] and 
                    branch_idx not in covered_branches):
                    new_branches += 1
                    # Weight rare branches higher (inverse frequency)
                    rarity_weight = 1.0 / max(branch_frequency[branch_idx], 1)
                    score += rarity_weight
            
            # Combine new coverage count with rarity score
            if new_branches > 0:
                score = score * new_branches  # Boost score by number of new branches
                
            if score > best_score:
                best_score = score
                best_test_idx = test_idx
        
        if best_test_idx is not None:
            selected_tests.append(test_names[best_test_idx])
            available_tests.remove(best_test_idx)
            
            for branch_idx in range(n_branches):
                if coverage_matrix[best_test_idx][branch_idx]:
                    covered_branches.add(branch_idx)
        else:
            break
    
    coverage_pct = (len(covered_branches) / n_branches) * 100 if n_branches > 0 else 0
    reduction_ratio = len(selected_tests) / n_tests if n_tests > 0 else 1
    
    return selected_tests, coverage_pct, reduction_ratio
```

#### 4. Heuristic Algorithm (Greedy + Local Optimization)

```python
def heuristic_set_cover(coverage_matrix, test_names, branch_names):
    """
    Heuristic approach: Start with greedy, then apply local optimization
    """
    # Start with greedy solution
    selected_tests, coverage_pct, reduction_ratio = greedy_set_cover(
        coverage_matrix, test_names, branch_names
    )
    
    # Local optimization: try removing each test and see if coverage maintained
    optimized_tests = selected_tests.copy()
    
    for test_to_remove in selected_tests:
        remaining_tests = [t for t in optimized_tests if t != test_to_remove]
        
        # Check if remaining tests still achieve full coverage
        if check_full_coverage(remaining_tests, coverage_matrix, test_names):
            optimized_tests = remaining_tests
    
    # Recalculate metrics for optimized solution
    final_coverage = calculate_coverage(optimized_tests, coverage_matrix, test_names)
    final_reduction = len(optimized_tests) / len(coverage_matrix)
    
    return optimized_tests, final_coverage, final_reduction
```

### Mathematical Properties

#### Approximation Guarantee (Greedy Algorithm)
The greedy algorithm provides a **ln(m)-approximation**, where m is the number of expressions:

```
|GREEDY_SOLUTION| ≤ ln(m) × |OPTIMAL_SOLUTION|
```

This means if the optimal solution needs k test cases, greedy will need at most k × ln(m) test cases.

#### Complexity Analysis
| Algorithm | Time Complexity | Space Complexity | Quality |
|-----------|----------------|------------------|---------|
| Greedy | O(nm log n) | O(nm) | ln(m)-approx |
| Intelligent | O(nm log n) | O(nm) | Usually better than greedy |
| Heuristic | O(nm log n) | O(nm) | Often near-optimal |
| Optimal | O(2^n × m) | O(nm) | Exact optimal |

#### Problem Size Limits
- **Optimal Algorithm**: Practical up to ~16 test cases (2^16 = 65,536 combinations)
- **Greedy Algorithm**: Scales to thousands of test cases
- **Memory Usage**: O(n×m) for coverage matrix storage

### Algorithm Selection Strategy

The program automatically selects algorithms based on problem size:

```python
def select_algorithm(n_tests, n_expressions):
    if n_tests <= 16:
        return "optimal"  # Guaranteed best solution
    elif n_expressions > 100:
        return "greedy"   # Fast for large problems
    else:
        return "intelligent"  # Good balance
```

This ensures optimal results for small problems while maintaining performance for larger ones.

## Advanced Features

### Custom Test Case Generation

```python
from itertools import product

def custom_test_generation(variables):
    # Generate all combinations
    combinations = list(product([False, True], repeat=len(variables)))
    
    # Custom filtering/selection logic
    filtered_combinations = [c for c in combinations if some_condition(c)]
    
    return filtered_combinations
```

### Working with Large Expression Sets

For many expressions (>20), consider:

1. **Batch Processing**: Group related expressions
2. **Prioritization**: Focus on critical expressions first  
3. **Incremental Analysis**: Add expressions progressively

```python
# Batch processing example
critical_expressions = ["error_condition", "security_check"]
standard_expressions = ["feature_flag_a", "feature_flag_b", "logging_enabled"]

# Process critical first
reduce_string_expressions(critical_expressions)
# Then add standard
reduce_string_expressions(critical_expressions + standard_expressions)
```

### Integration with Test Frameworks

```python
def generate_pytest_cases(selected_tests, expressions):
    """Convert results to pytest parametrize format"""
    test_cases = []
    for test_case in selected_tests:
        # Parse test case name "A=T,B=F,C=T"  
        vars_values = parse_test_case(test_case)
        test_cases.append(pytest.param(vars_values, id=test_case))
    return test_cases

@pytest.mark.parametrize("variables", generate_pytest_cases(selected_tests, expressions))
def test_boolean_logic(variables):
    # Your test implementation
    assert evaluate_conditions(variables)
```

## Troubleshooting

### Common Issues

**1. "No solution found within limits"**
- Increase the limit in `optimal_set_cover` 
- Use `greedy_set_cover` for large problems

**2. "Error evaluating expression"**
- Check expression syntax
- Ensure variable names are valid
- Avoid Python keywords

**3. "Variables not found"**  
- Verify variable names in expressions
- Check for typos in variable references

**4. Low coverage percentage**
- Some expressions may be unsatisfiable
- Check for contradictory conditions
- Verify expression logic

### Performance Tips

**For Large Problems:**
- Use greedy algorithm explicitly
- Limit variable combinations if possible
- Consider expression simplification

**For Small Problems:**
- Use optimal algorithm for best results
- Enable detailed output for analysis

### Debugging

Enable detailed output:

```python
# Add debug prints in string_expression_reducer.py
def debug_coverage_matrix(coverage_matrix, test_names, expressions):
    for i, test in enumerate(test_names):
        coverage = coverage_matrix[i]
        print(f"{test}: {coverage}")
```

### Getting Help

1. **Check Examples**: See `EXAMPLES.md` for more use cases
2. **Review Source**: Core algorithms are well-commented  
3. **Create Issues**: Use GitHub issues for bugs/feature requests
4. **Test Manually**: Use `analyze_user_expressions.py` for verification

## Best Practices

1. **Start Simple**: Begin with a few expressions to understand output
2. **Validate Results**: Manually verify critical test case selections  
3. **Document Variables**: Use descriptive variable names
4. **Test Edge Cases**: Include boundary conditions in expressions
5. **Version Control**: Track expression changes and results

---

For more examples and use cases, see [EXAMPLES.md](EXAMPLES.md).
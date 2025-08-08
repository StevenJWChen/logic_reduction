"""
String Expression Reducer - Takes expressions as strings
Input: List of string expressions like ['A and B', 'A and not C', ...]
Output: Minimum test cases to make each expression True
"""

from core_reduction_functions import optimal_set_cover, greedy_set_cover
from itertools import product
import re

def extract_variables(expressions):
    """Extract all variables from expression strings"""
    variables = set()
    for expr in expressions:
        # Find all variable names (letters, possibly with underscores and numbers)
        vars_in_expr = re.findall(r'\b[A-Za-z][A-Za-z0-9_]*\b', expr)
        # Filter out Python keywords
        python_keywords = {'and', 'or', 'not', 'True', 'False', 'in', 'is'}
        vars_in_expr = [v for v in vars_in_expr if v not in python_keywords]
        variables.update(vars_in_expr)
    return sorted(list(variables))

def evaluate_expression(expr_str, variable_values):
    """Safely evaluate a boolean expression string with given variable values"""
    try:
        # Replace variable names with their values in the expression
        expr = expr_str
        for var, val in variable_values.items():
            # Use word boundaries to avoid partial matches
            expr = re.sub(r'\b' + re.escape(var) + r'\b', str(val), expr)
        
        # Evaluate the expression safely
        result = eval(expr)
        return bool(result)
    except Exception as e:
        print(f"Error evaluating expression '{expr_str}' with values {variable_values}: {e}")
        return False

def reduce_string_expressions(expressions):
    """
    Reduce test cases for boolean expressions given as strings
    
    Args:
        expressions: List of string expressions like ['A and B', '(A or B) and C', 'not A']
        
    Returns:
        Minimum test cases needed to make each expression True at least once
    """
    
    print("STRING EXPRESSION REDUCER")
    print("=" * 50)
    print("Input expressions:")
    for i, expr in enumerate(expressions, 1):
        print(f"  exp{i}: {expr}")
    print()
    
    # Extract all variables from expressions
    variables = extract_variables(expressions)
    print(f"Variables found: {variables}")
    print(f"Total possible combinations: {2**len(variables)}")
    print()
    
    # Generate all possible test combinations
    all_combinations = list(product([False, True], repeat=len(variables)))
    
    # Build test cases
    test_cases = []
    for combo in all_combinations:
        test_case = dict(zip(variables, combo))
        test_name = ",".join([f"{var}={str(val)[0]}" for var, val in test_case.items()])
        test_cases.append({"values": test_case, "name": test_name})
    
    # Build coverage matrix
    coverage_matrix = []
    branch_names = [f"exp{i+1}" for i in range(len(expressions))]
    
    print("COVERAGE ANALYSIS:")
    header = "Test Case" + " " * max(0, 20-len("Test Case")) + "| "
    header += " | ".join([f"exp{i+1:2d}" for i in range(len(expressions))]) + " | Covers"
    print(header)
    print("-" * (25 + len(expressions) * 6 + 15))
    
    for tc in test_cases:
        coverage = []
        covered_exps = []
        
        for i, expr_str in enumerate(expressions):
            result = evaluate_expression(expr_str, tc["values"])
            coverage.append(result)
            if result:
                covered_exps.append(f"exp{i+1}")
        
        coverage_matrix.append(coverage)
        
        # Display coverage
        results = " | ".join([f"{str(coverage[i])[0]:4s}" for i in range(len(expressions))])
        covers = ", ".join(covered_exps) if covered_exps else "none"
        print(f"{tc['name']:23s} | {results} | {covers}")
    
    print()
    
    # Check if all expressions can be satisfied
    satisfiable_expressions = []
    for i, expr in enumerate(expressions):
        can_be_true = any(coverage_matrix[j][i] for j in range(len(coverage_matrix)))
        if can_be_true:
            satisfiable_expressions.append(i)
        else:
            print(f"WARNING: Expression {i+1} '{expr}' can never be True with these variables!")
    
    if len(satisfiable_expressions) != len(expressions):
        print(f"Only {len(satisfiable_expressions)}/{len(expressions)} expressions are satisfiable.")
        print()
    
    # Find minimum test cases
    test_names = [tc["name"] for tc in test_cases]
    
    # Try optimal first (for small problems)
    if len(test_cases) <= 16:  # Reasonable limit for optimal
        result = optimal_set_cover(coverage_matrix, test_names, branch_names)
        if result:
            selected_tests, coverage_pct, reduction_ratio = result
            print("OPTIMAL SOLUTION:")
        else:
            # Fall back to greedy
            selected_tests, coverage_pct, reduction_ratio = greedy_set_cover(coverage_matrix, test_names, branch_names)
            print("GREEDY SOLUTION:")
    else:
        # Use greedy for larger problems
        selected_tests, coverage_pct, reduction_ratio = greedy_set_cover(coverage_matrix, test_names, branch_names)
        print("GREEDY SOLUTION:")
    
    print(f"Minimum test cases needed: {len(selected_tests)}/{len(test_cases)}")
    print(f"Reduction: {(1-reduction_ratio)*100:.1f}%")
    print(f"Coverage: {coverage_pct:.1f}%")
    print()
    
    print("SELECTED TEST CASES:")
    for i, test_name in enumerate(selected_tests, 1):
        test_idx = test_names.index(test_name)
        tc = test_cases[test_idx]
        
        print(f"  Test {i}: {test_name}")
        print(f"    Variable values: {tc['values']}")
        
        # Show what this test covers
        covered = []
        for j, expr_str in enumerate(expressions):
            if evaluate_expression(expr_str, tc["values"]):
                covered.append(f"exp{j+1}")
        
        print(f"    Makes True: {', '.join(covered) if covered else 'none'}")
        
        # Show expression evaluations
        for j, expr_str in enumerate(expressions):
            result = evaluate_expression(expr_str, tc["values"])
            print(f"      exp{j+1}: {expr_str} = {result}")
        print()
    
    return selected_tests


# Example usage
def example_your_expressions():
    """Example with your specific expressions"""
    expressions = [
        "(A or B) and C",
        "A and B", 
        "A and not C"
    ]
    
    reduce_string_expressions(expressions)

def example_more_complex():
    """Example with more complex expressions"""
    print("\n" + "=" * 60)
    print("MORE COMPLEX EXAMPLE:")
    
    expressions = [
        "A and B and C",
        "A or (B and not C)", 
        "not A and (B or C)",
        "(A or B) and not (C and D)"
    ]
    
    reduce_string_expressions(expressions)

def example_simple():
    """Simple example"""
    print("\n" + "=" * 60)
    print("SIMPLE EXAMPLE:")
    
    expressions = [
        "X and Y",
        "X or Y",
        "not X"
    ]
    
    reduce_string_expressions(expressions)

if __name__ == "__main__":
    # Test your expressions
    example_your_expressions()
    
    # Test other examples
    example_simple()
    example_more_complex()
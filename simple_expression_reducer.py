"""
Simple Expression Reducer - Direct input for expressions
Just input your expressions and get minimum test cases!
"""

from core_reduction_functions import optimal_set_cover, greedy_set_cover
from itertools import product

def reduce_expressions(expressions, variables):
    """
    Reduce test cases for given boolean expressions
    
    Args:
        expressions: List of expression functions that take variable values and return bool
        variables: List of variable names
        
    Returns:
        Minimum test cases needed to make each expression True at least once
    """
    
    # Generate all possible test combinations
    all_combinations = list(product([False, True], repeat=len(variables)))
    
    print(f"Testing {len(expressions)} expressions with {len(variables)} variables")
    print(f"Total possible combinations: {len(all_combinations)}")
    print()
    
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
    print("Test Case" + " " * 10 + "| " + " | ".join([f"exp{i+1}" for i in range(len(expressions))]) + " | Covers")
    print("-" * (20 + len(expressions) * 6 + 10))
    
    for tc in test_cases:
        coverage = []
        covered_exps = []
        
        for i, expr_func in enumerate(expressions):
            result = expr_func(**tc["values"])
            coverage.append(result)
            if result:
                covered_exps.append(f"exp{i+1}")
        
        coverage_matrix.append(coverage)
        
        # Display coverage
        results = " | ".join([f"{str(coverage[i])[0]:4s}" for i in range(len(expressions))])
        covers = ", ".join(covered_exps) if covered_exps else "none"
        print(f"{tc['name']:18s} | {results} | {covers}")
    
    print()
    
    # Find minimum test cases
    test_names = [tc["name"] for tc in test_cases]
    
    # Try optimal first
    result = optimal_set_cover(coverage_matrix, test_names, branch_names)
    if result:
        selected_tests, coverage_pct, reduction_ratio = result
        print("OPTIMAL SOLUTION:")
    else:
        # Fall back to greedy
        selected_tests, coverage_pct, reduction_ratio = greedy_set_cover(coverage_matrix, test_names, branch_names)
        print("GREEDY SOLUTION:")
    
    print(f"Minimum test cases needed: {len(selected_tests)}/{len(test_cases)}")
    print(f"Reduction: {(1-reduction_ratio)*100:.1f}%")
    print(f"Coverage: {coverage_pct:.1f}%")
    print()
    
    print("SELECTED TEST CASES:")
    for test_name in selected_tests:
        test_idx = test_names.index(test_name)
        tc = test_cases[test_idx]
        
        # Show what this test covers
        covered = []
        for i, expr_func in enumerate(expressions):
            if expr_func(**tc["values"]):
                covered.append(f"exp{i+1}")
        
        print(f"  {test_name}")
        print(f"    Values: {tc['values']}")
        print(f"    Covers: {', '.join(covered) if covered else 'none'}")
    
    return selected_tests


# Example usage with your expressions
def example_your_expressions():
    """Example with your specific expressions"""
    
    print("=" * 60)
    print("YOUR EXPRESSIONS:")
    print("exp1: (A or B) and C")
    print("exp2: A and B") 
    print("exp3: A and not C")
    print("=" * 60)
    
    # Define your expressions as functions
    def exp1(A, B, C):
        return (A or B) and C
    
    def exp2(A, B, C):
        return A and B
    
    def exp3(A, B, C):
        return A and not C
    
    expressions = [exp1, exp2, exp3]
    variables = ["A", "B", "C"]
    
    reduce_expressions(expressions, variables)


def example_custom():
    """Example showing how to input your own expressions"""
    
    print("\n" + "=" * 60) 
    print("CUSTOM EXAMPLE:")
    print("exp1: X and Y")
    print("exp2: X or Y")
    print("exp3: not X and Y") 
    print("=" * 60)
    
    # Define custom expressions
    def exp1(X, Y):
        return X and Y
    
    def exp2(X, Y):
        return X or Y
        
    def exp3(X, Y):
        return not X and Y
    
    expressions = [exp1, exp2, exp3]
    variables = ["X", "Y"]
    
    reduce_expressions(expressions, variables)


if __name__ == "__main__":
    # Test your expressions
    example_your_expressions()
    
    # Show another example
    example_custom()
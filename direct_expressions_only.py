"""
Direct expression input - only IF branches, no ELSE branches
User inputs: exp1: (A or B) and C, exp2: A and B, exp3: A and not C
Goal: Find minimum test cases to make all 3 expressions True at least once
"""

from core_reduction_functions import greedy_set_cover, intelligent_set_cover, heuristic_set_cover, optimal_set_cover

def direct_expressions_test():
    """Test direct expressions - only need to hit each expression once (IF branch only)"""
    
    print("=== DIRECT EXPRESSIONS INPUT (IF BRANCHES ONLY) ===")
    print("Expression 1: (A or B) and C")
    print("Expression 2: A and B")  
    print("Expression 3: A and not C")
    print()
    print("Goal: Find minimum test cases where each expression evaluates to True")
    print()
    
    # All possible test cases for A, B, C
    test_cases = [
        {"A": False, "B": False, "C": False, "name": "A=F,B=F,C=F"},
        {"A": False, "B": False, "C": True,  "name": "A=F,B=F,C=T"},
        {"A": False, "B": True,  "C": False, "name": "A=F,B=T,C=F"},
        {"A": False, "B": True,  "C": True,  "name": "A=F,B=T,C=T"},
        {"A": True,  "B": False, "C": False, "name": "A=T,B=F,C=F"},
        {"A": True,  "B": False, "C": True,  "name": "A=T,B=F,C=T"},
        {"A": True,  "B": True,  "C": False, "name": "A=T,B=T,C=F"},
        {"A": True,  "B": True,  "C": True,  "name": "A=T,B=T,C=T"}
    ]
    
    # Only 3 branches to cover (only the IF branches)
    branches = [
        "exp1_true",   # (A or B) and C = True
        "exp2_true",   # A and B = True  
        "exp3_true"    # A and not C = True
    ]
    
    print("COVERAGE ANALYSIS:")
    print("Test Case        | exp1 | exp2 | exp3 | Branches Covered")
    print("-----------------|------|------|------|------------------")
    
    # Build coverage matrix - only track when expressions are True
    coverage_matrix = []
    for i, tc in enumerate(test_cases):
        A, B, C = tc["A"], tc["B"], tc["C"]
        
        # Calculate expression results
        exp1_true = (A or B) and C
        exp2_true = A and B  
        exp3_true = A and not C
        
        # Coverage: True if expression is True, False otherwise
        coverage = [exp1_true, exp2_true, exp3_true]
        coverage_matrix.append(coverage)
        
        # Show which branches are covered
        covered_branches = []
        if coverage[0]: covered_branches.append("exp1")
        if coverage[1]: covered_branches.append("exp2") 
        if coverage[2]: covered_branches.append("exp3")
        
        covered_str = ", ".join(covered_branches) if covered_branches else "none"
        print(f"{tc['name']:16s} | {str(exp1_true)[0]:4s} | {str(exp2_true)[0]:4s} | {str(exp3_true)[0]:4s} | {covered_str}")
    
    print()
    print("REDUCTION ALGORITHM RESULTS:")
    print("=" * 60)
    
    # Test different algorithms
    algorithms = [
        ("Greedy", greedy_set_cover),
        ("Intelligent", intelligent_set_cover),
        ("Heuristic", heuristic_set_cover),
    ]
    
    test_names = [tc["name"] for tc in test_cases]
    
    for name, algorithm in algorithms:
        try:
            selected_tests, coverage_pct, reduction_ratio = algorithm(coverage_matrix, test_names, branches)
            
            print(f"{name} Algorithm:")
            print(f"  Selected tests: {len(selected_tests)}/{len(test_cases)} tests")
            print(f"  Coverage: {coverage_pct:.1f}%") 
            print(f"  Reduction: {(1-reduction_ratio)*100:.1f}%")
            
            # Show what each selected test covers
            for test_name in selected_tests:
                test_idx = test_names.index(test_name)
                tc = test_cases[test_idx]
                A, B, C = tc["A"], tc["B"], tc["C"]
                exp1 = (A or B) and C
                exp2 = A and B
                exp3 = A and not C
                
                covered = []
                if exp1: covered.append("exp1") 
                if exp2: covered.append("exp2")
                if exp3: covered.append("exp3")
                
                print(f"    {test_name}: covers {', '.join(covered) if covered else 'none'}")
            print()
        except Exception as e:
            print(f"{name} Algorithm failed: {e}")
            print()
    
    # Try optimal for this small case
    print("Optimal Algorithm:")
    try:
        result = optimal_set_cover(coverage_matrix, test_names, branches)
        if result:
            selected_tests, coverage_pct, reduction_ratio = result
            print(f"  Selected tests: {len(selected_tests)}/{len(test_cases)} tests") 
            print(f"  Coverage: {coverage_pct:.1f}%")
            print(f"  Reduction: {(1-reduction_ratio)*100:.1f}%")
            
            print(f"  OPTIMAL SOLUTION:")
            for test_name in selected_tests:
                test_idx = test_names.index(test_name)
                tc = test_cases[test_idx]
                A, B, C = tc["A"], tc["B"], tc["C"]
                exp1 = (A or B) and C
                exp2 = A and B
                exp3 = A and not C
                
                covered = []
                if exp1: covered.append("exp1")
                if exp2: covered.append("exp2") 
                if exp3: covered.append("exp3")
                
                print(f"    {test_name}")
                print(f"      Values: A={A}, B={B}, C={C}")
                print(f"      Results: exp1={exp1}, exp2={exp2}, exp3={exp3}")
                print(f"      Covers: {', '.join(covered) if covered else 'none'}")
        else:
            print("  No solution found within limits")
    except Exception as e:
        print(f"  Failed: {e}")


def custom_expressions_template():
    """Template for testing your own expressions"""
    
    print("\n" + "="*60)
    print("TEMPLATE FOR YOUR OWN EXPRESSIONS:")
    print("="*60)
    
    print("""
# To test your own expressions, modify this template:

def test_my_expressions():
    # Define your test cases (all combinations of variables)
    test_cases = [
        {"X": False, "Y": False, "name": "X=F,Y=F"},
        {"X": False, "Y": True,  "name": "X=F,Y=T"}, 
        {"X": True,  "Y": False, "name": "X=T,Y=F"},
        {"X": True,  "Y": True,  "name": "X=T,Y=T"}
    ]
    
    # Define your expressions (only IF branches)
    branches = ["my_exp1", "my_exp2", "my_exp3"]
    
    # Build coverage matrix
    coverage_matrix = []
    for tc in test_cases:
        X, Y = tc["X"], tc["Y"]
        
        # YOUR EXPRESSIONS HERE:
        exp1_result = X and Y           # Replace with your expression 1
        exp2_result = X or Y            # Replace with your expression 2  
        exp3_result = X and not Y       # Replace with your expression 3
        
        coverage = [exp1_result, exp2_result, exp3_result]
        coverage_matrix.append(coverage)
    
    # Run reduction algorithms
    test_names = [tc["name"] for tc in test_cases]
    selected, coverage_pct, reduction = greedy_set_cover(coverage_matrix, test_names, branches)
    
    print(f"Minimum tests needed: {len(selected)}/{len(test_cases)}")
    for test in selected:
        print(f"  - {test}")
""")


if __name__ == "__main__":
    direct_expressions_test()
    custom_expressions_template()
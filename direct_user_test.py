"""
Direct implementation of user's expressions test case
Showing how reduction algorithms should work with proper branch identification
"""

from core_reduction_functions import greedy_set_cover, intelligent_set_cover, heuristic_set_cover, optimal_set_cover

def test_user_expressions():
    """Test user's expressions: (A or B) and C, A and B, A and not C"""
    
    print("=== USER'S EXPRESSIONS TEST CASE ===")
    print("Expression 1: (A or B) and C")
    print("Expression 2: A and B")  
    print("Expression 3: A and not C")
    print()
    
    # All possible test cases for A, B, C
    test_cases = [
        {"A": False, "B": False, "C": False, "name": "FFF"},
        {"A": False, "B": False, "C": True,  "name": "FFT"},
        {"A": False, "B": True,  "C": False, "name": "FTF"},
        {"A": False, "B": True,  "C": True,  "name": "FTT"},
        {"A": True,  "B": False, "C": False, "name": "TFF"},
        {"A": True,  "B": False, "C": True,  "name": "TFT"},
        {"A": True,  "B": True,  "C": False, "name": "TTF"},
        {"A": True,  "B": True,  "C": True,  "name": "TTT"}
    ]
    
    # 6 branches to cover (each expression has if/else)
    branches = [
        "exp1_true",   # (A or B) and C = True
        "exp1_false",  # (A or B) and C = False
        "exp2_true",   # A and B = True
        "exp2_false",  # A and B = False
        "exp3_true",   # A and not C = True
        "exp3_false"   # A and not C = False
    ]
    
    print("COVERAGE MATRIX:")
    print("Test | A B C | exp1 | exp2 | exp3 | Branches Covered")
    print("-----|-------|------|------|------|------------------")
    
    # Build coverage matrix
    coverage_matrix = []
    for i, tc in enumerate(test_cases):
        A, B, C = tc["A"], tc["B"], tc["C"]
        
        # Calculate expression results
        exp1_result = (A or B) and C
        exp2_result = A and B  
        exp3_result = A and not C
        
        # Determine which branches this test covers
        coverage = [False] * 6
        coverage[0] = exp1_result    # exp1_true
        coverage[1] = not exp1_result # exp1_false
        coverage[2] = exp2_result    # exp2_true
        coverage[3] = not exp2_result # exp2_false
        coverage[4] = exp3_result    # exp3_true
        coverage[5] = not exp3_result # exp3_false
        
        coverage_matrix.append(coverage)
        
        # Show which branches are covered
        covered_branches = []
        if coverage[0]: covered_branches.append("exp1_T")
        if coverage[1]: covered_branches.append("exp1_F")
        if coverage[2]: covered_branches.append("exp2_T") 
        if coverage[3]: covered_branches.append("exp2_F")
        if coverage[4]: covered_branches.append("exp3_T")
        if coverage[5]: covered_branches.append("exp3_F")
        
        print(f"{tc['name']:4s} | {str(A)[0]} {str(B)[0]} {str(C)[0]} | {str(exp1_result)[0]:4s} | {str(exp2_result)[0]:4s} | {str(exp3_result)[0]:4s} | {', '.join(covered_branches)}")
    
    print()
    print("REDUCTION ALGORITHM RESULTS:")
    print("-" * 50)
    
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
            print(f"  Selected tests: {selected_tests}")
            print(f"  Count: {len(selected_tests)}/{len(test_cases)} tests")
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
                print(f"    {test_name} (A={A}, B={B}, C={C}): exp1={exp1}, exp2={exp2}, exp3={exp3}")
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
            print(f"  Selected tests: {selected_tests}")
            print(f"  Count: {len(selected_tests)}/{len(test_cases)} tests") 
            print(f"  Coverage: {coverage_pct:.1f}%")
            print(f"  Reduction: {(1-reduction_ratio)*100:.1f}%")
            
            for test_name in selected_tests:
                test_idx = test_names.index(test_name)
                tc = test_cases[test_idx]
                A, B, C = tc["A"], tc["B"], tc["C"]
                exp1 = (A or B) and C
                exp2 = A and B
                exp3 = A and not C
                print(f"    {test_name} (A={A}, B={B}, C={C}): exp1={exp1}, exp2={exp2}, exp3={exp3}")
        else:
            print("  No solution found within limits")
    except Exception as e:
        print(f"  Failed: {e}")

if __name__ == "__main__":
    test_user_expressions()
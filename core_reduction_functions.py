"""
Core Logic Reduction Functions - Standalone implementation
Solves the Set Cover problem for test case minimization
"""

import time
from typing import List, Set, Tuple
from itertools import combinations


def greedy_set_cover(coverage_matrix: List[List[bool]], test_cases: List, branches: List) -> Tuple[List, float, float]:
    """
    Greedy Set Cover Algorithm - Main reduction function
    
    Args:
        coverage_matrix: Matrix[i][j] = True if test i covers branch j
        test_cases: List of test case objects
        branches: List of branch identifiers
        
    Returns:
        (selected_tests, coverage_percentage, reduction_ratio)
    """
    start_time = time.time()
    
    selected_tests = []
    covered_branches = set()
    all_branches = set(range(len(branches)))
    available_tests = list(range(len(test_cases)))
    
    # Greedy selection: pick test covering most uncovered branches
    while covered_branches != all_branches and available_tests:
        best_test_idx = None
        best_new_coverage = 0
        
        # Find test case that covers the most new branches
        for test_idx in available_tests:
            new_branches = set()
            for branch_idx in range(len(branches)):
                if (coverage_matrix[test_idx][branch_idx] and 
                    branch_idx not in covered_branches):
                    new_branches.add(branch_idx)
            
            if len(new_branches) > best_new_coverage:
                best_new_coverage = len(new_branches)
                best_test_idx = test_idx
        
        # Select the best test
        if best_test_idx is not None:
            selected_tests.append(test_cases[best_test_idx])
            available_tests.remove(best_test_idx)
            
            # Update covered branches
            for branch_idx in range(len(branches)):
                if coverage_matrix[best_test_idx][branch_idx]:
                    covered_branches.add(branch_idx)
        else:
            break
    
    coverage_pct = len(covered_branches) / len(branches) * 100
    reduction_ratio = len(selected_tests) / len(test_cases)
    
    return selected_tests, coverage_pct, reduction_ratio


def intelligent_set_cover(coverage_matrix: List[List[bool]], test_cases: List, branches: List) -> Tuple[List, float, float]:
    """
    Intelligent Set Cover Algorithm - Considers branch rarity and test efficiency
    
    Args:
        coverage_matrix: Matrix[i][j] = True if test i covers branch j
        test_cases: List of test case objects  
        branches: List of branch identifiers
        
    Returns:
        (selected_tests, coverage_percentage, reduction_ratio)
    """
    # Calculate branch coverage frequency (rarity)
    branch_frequency = [0] * len(branches)
    for test_idx in range(len(test_cases)):
        for branch_idx in range(len(branches)):
            if coverage_matrix[test_idx][branch_idx]:
                branch_frequency[branch_idx] += 1
    
    # Calculate test case efficiency scores
    test_scores = []
    for test_idx in range(len(test_cases)):
        score = 0
        branches_covered = 0
        for branch_idx in range(len(branches)):
            if coverage_matrix[test_idx][branch_idx]:
                branches_covered += 1
                # Give higher score to tests covering rare branches
                if branch_frequency[branch_idx] > 0:
                    score += 1.0 / branch_frequency[branch_idx]
        
        # Normalize by number of branches covered
        if branches_covered > 0:
            score = score / branches_covered
        test_scores.append((test_idx, score))
    
    # Sort by efficiency score (descending)
    test_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Select tests in order of efficiency until full coverage
    selected_tests = []
    covered_branches = set()
    
    for test_idx, _ in test_scores:
        if len(covered_branches) == len(branches):
            break
        
        # Check if this test covers any new branches
        new_coverage = False
        for branch_idx in range(len(branches)):
            if (coverage_matrix[test_idx][branch_idx] and 
                branch_idx not in covered_branches):
                new_coverage = True
                break
        
        if new_coverage:
            selected_tests.append(test_cases[test_idx])
            # Update covered branches
            for branch_idx in range(len(branches)):
                if coverage_matrix[test_idx][branch_idx]:
                    covered_branches.add(branch_idx)
    
    coverage_pct = len(covered_branches) / len(branches) * 100
    reduction_ratio = len(selected_tests) / len(test_cases)
    
    return selected_tests, coverage_pct, reduction_ratio


def optimal_set_cover(coverage_matrix: List[List[bool]], test_cases: List, branches: List, max_combinations: int = 1000000) -> Tuple[List, float, float]:
    """
    Optimal Set Cover Algorithm - Exhaustive search for small problems
    
    Args:
        coverage_matrix: Matrix[i][j] = True if test i covers branch j
        test_cases: List of test case objects
        branches: List of branch identifiers
        max_combinations: Limit for exhaustive search
        
    Returns:
        (selected_tests, coverage_percentage, reduction_ratio) or None if not found
    """
    n_tests = len(test_cases)
    n_branches = len(branches)
    
    # Start with smallest possible sets and work up
    for set_size in range(1, n_tests + 1):
        if set_size > 20:  # Practical limit
            break
        
        combinations_count = 0
        for test_indices in combinations(range(n_tests), set_size):
            combinations_count += 1
            if combinations_count > max_combinations:
                break
            
            # Check if this combination covers all branches
            covered_branches = set()
            for test_idx in test_indices:
                for branch_idx in range(n_branches):
                    if coverage_matrix[test_idx][branch_idx]:
                        covered_branches.add(branch_idx)
            
            if len(covered_branches) == n_branches:
                # Found optimal solution
                selected_tests = [test_cases[i] for i in test_indices]
                coverage_pct = 100.0
                reduction_ratio = len(selected_tests) / len(test_cases)
                return selected_tests, coverage_pct, reduction_ratio
    
    return None  # No solution found within limits


def heuristic_set_cover(coverage_matrix: List[List[bool]], test_cases: List, branches: List) -> Tuple[List, float, float]:
    """
    Heuristic Set Cover Algorithm - Greedy + local optimization
    
    Args:
        coverage_matrix: Matrix[i][j] = True if test i covers branch j
        test_cases: List of test case objects
        branches: List of branch identifiers
        
    Returns:
        (selected_tests, coverage_percentage, reduction_ratio)
    """
    # Start with greedy solution
    current_tests, _, _ = greedy_set_cover(coverage_matrix, test_cases, branches)
    
    # Helper function to check full coverage
    def check_full_coverage(test_list):
        covered = set()
        for test in test_list:
            test_idx = test_cases.index(test)
            for branch_idx in range(len(branches)):
                if coverage_matrix[test_idx][branch_idx]:
                    covered.add(branch_idx)
        return len(covered) == len(branches)
    
    # Try to improve by removing redundant tests
    improved = True
    while improved:
        improved = False
        for i in range(len(current_tests)):
            # Try removing test i
            test_without_i = current_tests[:i] + current_tests[i+1:]
            
            if test_without_i and check_full_coverage(test_without_i):
                current_tests = test_without_i
                improved = True
                break
    
    coverage_pct = 100.0 if check_full_coverage(current_tests) else 0.0
    reduction_ratio = len(current_tests) / len(test_cases)
    
    return current_tests, coverage_pct, reduction_ratio


# Example usage function
def example_usage():
    """Example of how to use the reduction functions"""
    
    # Example: 4 test cases, 3 branches
    # Coverage matrix: test_cases[i] covers branches[j] if matrix[i][j] = True
    coverage_matrix = [
        [True,  False, True],   # Test 0 covers branches 0,2
        [False, True,  True],   # Test 1 covers branches 1,2  
        [True,  True,  False],  # Test 2 covers branches 0,1
        [True,  False, False]   # Test 3 covers branch 0 only
    ]
    
    test_cases = ["Test_A", "Test_B", "Test_C", "Test_D"]
    branches = ["Branch_1", "Branch_2", "Branch_3"]
    
    print("Original test cases:", len(test_cases))
    print("Branches to cover:", len(branches))
    print()
    
    # Test different algorithms
    algorithms = [
        ("Greedy", greedy_set_cover),
        ("Intelligent", intelligent_set_cover), 
        ("Heuristic", heuristic_set_cover)
    ]
    
    for name, algorithm in algorithms:
        selected, coverage, reduction = algorithm(coverage_matrix, test_cases, branches)
        print(f"{name} Algorithm:")
        print(f"  Selected tests: {selected}")
        print(f"  Coverage: {coverage:.1f}%")
        print(f"  Reduction: {(1-reduction)*100:.1f}%")
        print()


if __name__ == "__main__":
    example_usage()
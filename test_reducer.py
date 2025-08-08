"""
Test Case Reduction Algorithms - finds minimal set of test cases for 100% coverage
"""

from typing import List, Set, Tuple, Optional
from coverage_analyzer import TestCase, CoverageAnalyzer
from dataclasses import dataclass
import time
from itertools import combinations


@dataclass
class ReductionResult:
    """Result of test case reduction"""
    minimal_test_cases: List[TestCase]
    coverage_percentage: float
    reduction_ratio: float
    algorithm_used: str
    execution_time: float
    
    def __str__(self):
        return f"""Reduction Result:
Algorithm: {self.algorithm_used}
Original tests: {int(len(self.minimal_test_cases) / self.reduction_ratio)}
Reduced tests: {len(self.minimal_test_cases)}
Reduction: {(1-self.reduction_ratio)*100:.1f}%
Coverage: {self.coverage_percentage:.1f}%
Time: {self.execution_time:.3f}s"""


class TestReducer:
    """Implements various algorithms for reducing test cases while maintaining coverage"""
    
    def __init__(self, coverage_analyzer: CoverageAnalyzer):
        self.analyzer = coverage_analyzer
        self.test_cases, self.branches, self.coverage_matrix = coverage_analyzer.get_coverage_matrix()
    
    def reduce_greedy(self) -> ReductionResult:
        """Greedy algorithm: repeatedly pick test case covering most uncovered branches"""
        start_time = time.time()
        
        selected_tests = []
        covered_branches = set()
        all_branches = set(range(len(self.branches)))
        
        # Create mapping from test index to TestCase
        available_tests = list(range(len(self.test_cases)))
        
        while covered_branches != all_branches and available_tests:
            best_test_idx = None
            best_new_coverage = 0
            
            # Find test case that covers the most new branches
            for test_idx in available_tests:
                new_branches = set()
                for branch_idx in range(len(self.branches)):
                    if (self.coverage_matrix[test_idx][branch_idx] and 
                        branch_idx not in covered_branches):
                        new_branches.add(branch_idx)
                
                if len(new_branches) > best_new_coverage:
                    best_new_coverage = len(new_branches)
                    best_test_idx = test_idx
            
            if best_test_idx is not None:
                selected_tests.append(self.test_cases[best_test_idx])
                available_tests.remove(best_test_idx)
                
                # Update covered branches
                for branch_idx in range(len(self.branches)):
                    if self.coverage_matrix[best_test_idx][branch_idx]:
                        covered_branches.add(branch_idx)
            else:
                break
        
        end_time = time.time()
        
        coverage_pct = len(covered_branches) / len(self.branches) * 100
        reduction_ratio = len(selected_tests) / len(self.test_cases)
        
        return ReductionResult(
            selected_tests,
            coverage_pct,
            reduction_ratio,
            "Greedy",
            end_time - start_time
        )
    
    def reduce_optimal_small(self, max_combinations: int = 1000000) -> Optional[ReductionResult]:
        """Optimal algorithm for small problems - tries all combinations"""
        start_time = time.time()
        
        n_tests = len(self.test_cases)
        n_branches = len(self.branches)
        
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
                        if self.coverage_matrix[test_idx][branch_idx]:
                            covered_branches.add(branch_idx)
                
                if len(covered_branches) == n_branches:
                    # Found optimal solution
                    selected_tests = [self.test_cases[i] for i in test_indices]
                    end_time = time.time()
                    
                    return ReductionResult(
                        selected_tests,
                        100.0,
                        len(selected_tests) / len(self.test_cases),
                        f"Optimal (size {set_size})",
                        end_time - start_time
                    )
        
        return None  # No solution found within limits
    
    def reduce_heuristic(self) -> ReductionResult:
        """Heuristic algorithm combining greedy with local optimization"""
        start_time = time.time()
        
        # Start with greedy solution
        greedy_result = self.reduce_greedy()
        current_tests = greedy_result.minimal_test_cases[:]
        
        # Try to improve by removing redundant tests
        improved = True
        while improved:
            improved = False
            for i in range(len(current_tests)):
                # Try removing test i
                test_without_i = current_tests[:i] + current_tests[i+1:]
                
                if self._check_full_coverage(test_without_i):
                    current_tests = test_without_i
                    improved = True
                    break
        
        end_time = time.time()
        
        coverage_pct = self._calculate_coverage(current_tests)
        reduction_ratio = len(current_tests) / len(self.test_cases)
        
        return ReductionResult(
            current_tests,
            coverage_pct,
            reduction_ratio,
            "Heuristic (Greedy + Local)",
            end_time - start_time
        )
    
    def reduce_intelligent(self) -> ReductionResult:
        """Intelligent algorithm that considers branch importance and test case efficiency"""
        start_time = time.time()
        
        # Calculate branch coverage frequency (how many tests cover each branch)
        branch_frequency = [0] * len(self.branches)
        for test_idx in range(len(self.test_cases)):
            for branch_idx in range(len(self.branches)):
                if self.coverage_matrix[test_idx][branch_idx]:
                    branch_frequency[branch_idx] += 1
        
        # Calculate test case efficiency (branches covered / rarity of those branches)
        test_scores = []
        for test_idx in range(len(self.test_cases)):
            score = 0
            branches_covered = 0
            for branch_idx in range(len(self.branches)):
                if self.coverage_matrix[test_idx][branch_idx]:
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
            if len(covered_branches) == len(self.branches):
                break
            
            # Check if this test covers any new branches
            new_coverage = False
            for branch_idx in range(len(self.branches)):
                if (self.coverage_matrix[test_idx][branch_idx] and 
                    branch_idx not in covered_branches):
                    new_coverage = True
                    break
            
            if new_coverage:
                selected_tests.append(self.test_cases[test_idx])
                # Update covered branches
                for branch_idx in range(len(self.branches)):
                    if self.coverage_matrix[test_idx][branch_idx]:
                        covered_branches.add(branch_idx)
        
        end_time = time.time()
        
        coverage_pct = len(covered_branches) / len(self.branches) * 100
        reduction_ratio = len(selected_tests) / len(self.test_cases)
        
        return ReductionResult(
            selected_tests,
            coverage_pct,
            reduction_ratio,
            "Intelligent (Efficiency-based)",
            end_time - start_time
        )
    
    def _check_full_coverage(self, test_cases: List[TestCase]) -> bool:
        """Check if given test cases provide full branch coverage"""
        covered_branches = set()
        
        for test_case in test_cases:
            covered_branches.update(test_case.covered_branches)
        
        all_branches = set(branch.branch_id for branch in self.analyzer.branches)
        return covered_branches == all_branches
    
    def _calculate_coverage(self, test_cases: List[TestCase]) -> float:
        """Calculate coverage percentage for given test cases"""
        covered_branches = set()
        for test_case in test_cases:
            covered_branches.update(test_case.covered_branches)
        
        all_branches = set(branch.branch_id for branch in self.analyzer.branches)
        return len(covered_branches) / len(all_branches) * 100
    
    def compare_algorithms(self) -> List[ReductionResult]:
        """Compare all available reduction algorithms"""
        results = []
        
        print("Running reduction algorithms...")
        
        # Greedy
        print("  - Running Greedy algorithm...")
        results.append(self.reduce_greedy())
        
        # Heuristic 
        print("  - Running Heuristic algorithm...")
        results.append(self.reduce_heuristic())
        
        # Intelligent
        print("  - Running Intelligent algorithm...")
        results.append(self.reduce_intelligent())
        
        # Optimal (only for small problems)
        if len(self.test_cases) <= 15:
            print("  - Running Optimal algorithm...")
            optimal_result = self.reduce_optimal_small()
            if optimal_result:
                results.append(optimal_result)
        
        return results
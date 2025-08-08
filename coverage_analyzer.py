"""
Coverage Analysis for determining which test cases cover which branches
"""

from typing import List, Dict, Set, Tuple, Any
from itertools import product
from logic_parser import Branch, Condition
from dataclasses import dataclass


@dataclass
class TestCase:
    """Represents a test case with variable assignments"""
    values: Dict[str, Any]
    covered_branches: Set[str]
    
    def __str__(self):
        return f"TestCase({self.values}) -> covers {self.covered_branches}"


class CoverageAnalyzer:
    """Analyzes which test cases provide coverage for which branches"""
    
    def __init__(self, branches: List[Branch], variables: Set[str]):
        self.branches = branches
        self.variables = sorted(variables)  # Sort for consistent ordering
        self.test_cases = []
    
    def generate_all_test_cases(self, variable_domains: Dict[str, List[Any]] = None) -> List[TestCase]:
        """Generate all possible test cases based on variable domains"""
        if not variable_domains:
            # Default domains - boolean for simple cases
            variable_domains = {var: [True, False] for var in self.variables}
        
        # Generate cartesian product of all variable values
        var_names = list(variable_domains.keys())
        var_values = [variable_domains[var] for var in var_names]
        
        test_cases = []
        for values in product(*var_values):
            test_dict = dict(zip(var_names, values))
            covered = self._evaluate_coverage(test_dict)
            test_cases.append(TestCase(test_dict, covered))
        
        self.test_cases = test_cases
        return test_cases
    
    def generate_smart_test_cases(self, variable_domains: Dict[str, List[Any]] = None) -> List[TestCase]:
        """Generate test cases more intelligently based on conditions"""
        if not variable_domains:
            variable_domains = self._infer_domains_from_conditions()
        
        # Add boundary values and specific values from conditions
        enhanced_domains = self._enhance_domains(variable_domains)
        
        return self.generate_all_test_cases(enhanced_domains)
    
    def _infer_domains_from_conditions(self) -> Dict[str, List[Any]]:
        """Infer variable domains from the conditions in branches"""
        domains = {}
        
        for var in self.variables:
            values = set()
            
            # Look at all conditions involving this variable
            for branch in self.branches:
                for condition in branch.conditions:
                    if condition.variable == var:
                        # Add the specific value from the condition
                        try:
                            if condition.value.lower() in ['true', 'false']:
                                values.add(condition.value.lower() == 'true')
                            elif condition.value.isdigit():
                                values.add(int(condition.value))
                            elif self._is_float(condition.value):
                                values.add(float(condition.value))
                            else:
                                values.add(condition.value)
                        except:
                            values.add(condition.value)
            
            if not values:
                # Default to boolean if no specific values found
                domains[var] = [True, False]
            else:
                domains[var] = list(values)
                # Add boolean alternatives if needed
                if len(domains[var]) == 1 and isinstance(list(values)[0], bool):
                    domains[var] = [True, False]
        
        return domains
    
    def _enhance_domains(self, base_domains: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        """Add boundary values and negations to domains"""
        enhanced = {}
        
        for var, values in base_domains.items():
            enhanced_values = set(values)
            
            # For numeric values, add boundary cases
            numeric_values = [v for v in values if isinstance(v, (int, float))]
            if numeric_values:
                min_val, max_val = min(numeric_values), max(numeric_values)
                enhanced_values.update([min_val - 1, max_val + 1])
            
            enhanced[var] = list(enhanced_values)
        
        return enhanced
    
    def _is_float(self, value: str) -> bool:
        """Check if string represents a float"""
        try:
            float(value)
            return '.' in value
        except ValueError:
            return False
    
    def _evaluate_coverage(self, test_values: Dict[str, Any]) -> Set[str]:
        """Determine which branches are covered by a test case"""
        covered_branches = set()
        
        for branch in self.branches:
            if self._branch_is_covered(branch, test_values):
                covered_branches.add(branch.branch_id)
        
        return covered_branches
    
    def _branch_is_covered(self, branch: Branch, test_values: Dict[str, Any]) -> bool:
        """Check if a branch is covered by the given test values"""
        for condition in branch.conditions:
            if not self._condition_is_satisfied(condition, test_values):
                return False
        return True
    
    def _condition_is_satisfied(self, condition: Condition, test_values: Dict[str, Any]) -> bool:
        """Check if a condition is satisfied by the test values"""
        if condition.variable not in test_values:
            return False
        
        actual_value = test_values[condition.variable]
        expected_value = self._convert_value(condition.value, type(actual_value))
        
        # Evaluate the condition
        if condition.operator == "==":
            return actual_value == expected_value
        elif condition.operator == "!=":
            return actual_value != expected_value
        elif condition.operator == "<":
            return actual_value < expected_value
        elif condition.operator == "<=":
            return actual_value <= expected_value
        elif condition.operator == ">":
            return actual_value > expected_value
        elif condition.operator == ">=":
            return actual_value >= expected_value
        else:
            # For complex operators, try to evaluate safely
            try:
                return eval(f"{actual_value} {condition.operator} {expected_value}")
            except:
                return False
    
    def _convert_value(self, value_str: str, target_type: type) -> Any:
        """Convert string value to target type"""
        if target_type == bool:
            return value_str.lower() in ['true', '1', 'yes']
        elif target_type == int:
            try:
                return int(value_str)
            except ValueError:
                return 0
        elif target_type == float:
            try:
                return float(value_str)
            except ValueError:
                return 0.0
        else:
            return value_str
    
    def get_coverage_matrix(self) -> Tuple[List[TestCase], List[str], List[List[bool]]]:
        """Get coverage matrix: test_cases x branches"""
        all_branches = [branch.branch_id for branch in self.branches]
        matrix = []
        
        for test_case in self.test_cases:
            row = [branch_id in test_case.covered_branches for branch_id in all_branches]
            matrix.append(row)
        
        return self.test_cases, all_branches, matrix
    
    def print_coverage_report(self):
        """Print a coverage report showing which test cases cover which branches"""
        print(f"\nCoverage Analysis:")
        print(f"Variables: {self.variables}")
        print(f"Branches: {len(self.branches)}")
        print(f"Generated Test Cases: {len(self.test_cases)}")
        
        for i, test_case in enumerate(self.test_cases):
            print(f"Test {i+1}: {test_case}")
        
        # Coverage summary
        all_branches = set(branch.branch_id for branch in self.branches)
        covered_branches = set()
        for test_case in self.test_cases:
            covered_branches.update(test_case.covered_branches)
        
        print(f"\nCoverage Summary:")
        print(f"Total branches: {len(all_branches)}")
        print(f"Covered branches: {len(covered_branches)}")
        print(f"Coverage: {len(covered_branches)/len(all_branches)*100:.1f}%")
        
        uncovered = all_branches - covered_branches
        if uncovered:
            print(f"Uncovered branches: {uncovered}")
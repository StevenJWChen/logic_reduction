"""
Logic Expression Parser for extracting conditions from if/else statements
"""

import re
import ast
from typing import List, Set, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Condition:
    """Represents a single boolean condition"""
    variable: str
    operator: str
    value: str
    
    def __str__(self):
        return f"{self.variable} {self.operator} {self.value}"
    
    def __hash__(self):
        return hash((self.variable, self.operator, self.value))


@dataclass 
class Branch:
    """Represents a code branch with its conditions"""
    conditions: List[Condition]
    branch_id: str
    
    def __str__(self):
        return f"Branch {self.branch_id}: {' AND '.join(str(c) for c in self.conditions)}"


class LogicParser:
    """Extracts logic conditions from source code"""
    
    def __init__(self):
        self.branches = []
        self.variables = set()
    
    def parse_file(self, filepath: str) -> List[Branch]:
        """Parse a source file and extract all branches"""
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Try to parse as Python first
        try:
            tree = ast.parse(content)
            return self._parse_ast(tree)
        except SyntaxError:
            # Fall back to regex parsing for other languages
            return self._parse_regex(content)
    
    def _parse_ast(self, tree: ast.AST) -> List[Branch]:
        """Parse Python AST to extract if/else branches"""
        branches = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                branches.extend(self._extract_if_branches(node))
        
        return branches
    
    def _extract_if_branches(self, if_node: ast.If, parent_conditions: List[Condition] = None) -> List[Branch]:
        """Extract branches from an if statement"""
        if parent_conditions is None:
            parent_conditions = []
        
        branches = []
        
        # Extract condition from the if statement
        if_condition = self._extract_condition(if_node.test)
        if_conditions = parent_conditions + [if_condition] if if_condition else parent_conditions
        
        # Create branch for if body
        branch_id = f"if_{len(self.branches)}"
        branches.append(Branch(if_conditions, branch_id))
        
        # Handle else/elif
        if if_node.orelse:
            if len(if_node.orelse) == 1 and isinstance(if_node.orelse[0], ast.If):
                # elif case
                branches.extend(self._extract_if_branches(if_node.orelse[0], parent_conditions))
            else:
                # else case
                else_condition = self._negate_condition(if_condition) if if_condition else None
                else_conditions = parent_conditions + [else_condition] if else_condition else parent_conditions
                else_branch_id = f"else_{len(self.branches)}"
                branches.append(Branch(else_conditions, else_branch_id))
        
        return branches
    
    def _extract_condition(self, node: ast.AST) -> Condition:
        """Extract a condition from an AST node"""
        if isinstance(node, ast.Compare):
            if len(node.ops) == 1 and len(node.comparators) == 1:
                left = self._get_variable_name(node.left)
                op = self._get_operator(node.ops[0])
                right = self._get_value(node.comparators[0])
                
                if left and op and right:
                    self.variables.add(left)
                    return Condition(left, op, right)
        
        elif isinstance(node, ast.Name):
            # Boolean variable
            self.variables.add(node.id)
            return Condition(node.id, "==", "True")
        
        return None
    
    def _get_variable_name(self, node: ast.AST) -> str:
        """Get variable name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_variable_name(node.value)}.{node.attr}"
        return None
    
    def _get_operator(self, node: ast.AST) -> str:
        """Convert AST comparison operator to string"""
        op_map = {
            ast.Eq: "==",
            ast.NotEq: "!=", 
            ast.Lt: "<",
            ast.LtE: "<=",
            ast.Gt: ">",
            ast.GtE: ">=",
            ast.Is: "is",
            ast.IsNot: "is not",
            ast.In: "in",
            ast.NotIn: "not in"
        }
        return op_map.get(type(node), str(node))
    
    def _get_value(self, node: ast.AST) -> str:
        """Get value from AST node"""
        if isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        return str(node)
    
    def _negate_condition(self, condition: Condition) -> Condition:
        """Create negated version of a condition"""
        if not condition:
            return None
        
        neg_op_map = {
            "==": "!=",
            "!=": "==", 
            "<": ">=",
            "<=": ">",
            ">": "<=",
            ">=": "<"
        }
        
        neg_op = neg_op_map.get(condition.operator, f"not ({condition.operator})")
        return Condition(condition.variable, neg_op, condition.value)
    
    def _parse_regex(self, content: str) -> List[Branch]:
        """Fallback regex-based parsing for non-Python code"""
        branches = []
        
        # Simple regex to find if statements
        if_pattern = r'if\s*\((.*?)\)'
        matches = re.finditer(if_pattern, content, re.MULTILINE)
        
        for i, match in enumerate(matches):
            condition_str = match.group(1).strip()
            conditions = self._parse_condition_string(condition_str)
            branch_id = f"branch_{i}"
            branches.append(Branch(conditions, branch_id))
        
        return branches
    
    def _parse_condition_string(self, condition_str: str) -> List[Condition]:
        """Parse condition string into Condition objects"""
        # Simple parsing for basic conditions
        conditions = []
        
        # Split on AND/OR (for now just handle AND)
        parts = re.split(r'\s+&&\s+|\s+and\s+', condition_str, flags=re.IGNORECASE)
        
        for part in parts:
            part = part.strip()
            
            # Match pattern like "variable operator value"
            match = re.match(r'(\w+(?:\.\w+)*)\s*([<>=!]+|==|!=)\s*(.+)', part)
            if match:
                var, op, val = match.groups()
                val = val.strip('"\'')  # Remove quotes
                self.variables.add(var)
                conditions.append(Condition(var, op, val))
        
        return conditions
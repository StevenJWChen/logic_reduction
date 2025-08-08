# Focused complex boolean expressions example

def complex_boolean_showcase(A, B, C, D):
    """Showcase of complex boolean expressions with AND, OR, NOT"""
    
    # Expression 1: (A or B) and not C
    if (A or B) and not C:
        result1 = "case_1"
    else:
        result1 = "case_other"
    
    # Expression 2: A and (B or C) and not D  
    if A and (B or C) and not D:
        result2 = "case_2"
    else:
        result2 = "case_other"
    
    # Expression 3: (A and B) or (C and D)
    if (A and B) or (C and D):
        result3 = "case_3"
    else:
        result3 = "case_other"
    
    # Expression 4: not A and not B and (C or D)
    if not A and not B and (C or D):
        result4 = "case_4"
    else:
        result4 = "case_other"
    
    # Expression 5: not (A and B and C) or D
    if not (A and B and C) or D:
        result5 = "case_5"
    else:
        result5 = "case_other"
    
    return result1, result2, result3, result4, result5


def boolean_logic_patterns(X, Y, Z):
    """Different boolean logic patterns"""
    
    # XOR pattern: exactly one true
    if (X and not Y and not Z) or (not X and Y and not Z) or (not X and not Y and Z):
        xor_result = "exactly_one"
    else:
        xor_result = "not_exactly_one"
    
    # Majority logic: at least 2 out of 3 are true
    if (X and Y) or (X and Z) or (Y and Z):
        majority = "majority_true"
    else:
        majority = "majority_false"
    
    # Complex nested: ((X and Y) or Z) and not (X and Y and Z)
    if ((X and Y) or Z) and not (X and Y and Z):
        nested = "complex_true"
    else:
        nested = "complex_false"
    
    return xor_result, majority, nested
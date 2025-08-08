# Force multiple test cases by creating mutually exclusive conditions

def force_multiple_tests(A, B, C):
    """Designed to require multiple test cases by having mutually exclusive conditions"""
    
    # Condition 1: A must be True, B must be False
    if A and not B:
        result1 = "A_true_B_false"
    else:
        result1 = "not_A_true_B_false"
    
    # Condition 2: A must be False, B must be True  
    if not A and B:
        result2 = "A_false_B_true"
    else:
        result2 = "not_A_false_B_true"
    
    # Condition 3: A and B must both be True
    if A and B:
        result3 = "both_A_B_true"
    else:
        result3 = "not_both_A_B_true"
    
    # Condition 4: A and B must both be False
    if not A and not B:
        result4 = "both_A_B_false"
    else:
        result4 = "not_both_A_B_false"
    
    # Condition 5: C must be True
    if C:
        result5 = "C_is_true"
    else:
        result5 = "C_is_false"
    
    # Condition 6: C must be False
    if not C:
        result6 = "C_is_false_check"
    else:
        result6 = "C_is_not_false"
    
    return result1, result2, result3, result4, result5, result6


def independent_conditions(X, Y, Z):
    """Independent conditions that require different test combinations"""
    
    # Each condition is independent and requires specific values
    
    # Condition 1: Only X is True
    if X and not Y and not Z:
        r1 = "only_X"
    else:
        r1 = "not_only_X"
    
    # Condition 2: Only Y is True  
    if not X and Y and not Z:
        r2 = "only_Y"
    else:
        r2 = "not_only_Y"
    
    # Condition 3: Only Z is True
    if not X and not Y and Z:
        r3 = "only_Z"
    else:
        r3 = "not_only_Z"
    
    # Condition 4: All are True
    if X and Y and Z:
        r4 = "all_true"
    else:
        r4 = "not_all_true"
    
    # Condition 5: All are False
    if not X and not Y and not Z:
        r5 = "all_false"
    else:
        r5 = "not_all_false"
    
    # Condition 6: Exactly two are True
    if (X and Y and not Z) or (X and not Y and Z) or (not X and Y and Z):
        r6 = "exactly_two_true"
    else:
        r6 = "not_exactly_two_true"
    
    return r1, r2, r3, r4, r5, r6
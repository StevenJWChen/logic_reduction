# Balanced expressions that require multiple test cases to achieve full coverage

def balanced_complex_expressions(A, B, C, D):
    """Complex expressions designed to require multiple test cases"""
    
    # Expression 1: (A or B) and not C
    # This needs: C=False for IF, C=True for ELSE
    if (A or B) and not C:
        result1 = "expr1_if_branch"
    else:
        result1 = "expr1_else_branch"
    
    # Expression 2: A and B and not C
    # This needs: A=T, B=T, C=F for IF; otherwise ELSE  
    if A and B and not C:
        result2 = "expr2_if_branch"
    else:
        result2 = "expr2_else_branch"
    
    # Expression 3: not A and not B
    # This needs: A=F, B=F for IF; otherwise ELSE
    if not A and not B:
        result3 = "expr3_if_branch"
    else:
        result3 = "expr3_else_branch"
    
    # Expression 4: C and D
    # This needs: C=T, D=T for IF; otherwise ELSE
    if C and D:
        result4 = "expr4_if_branch"
    else:
        result4 = "expr4_else_branch"
    
    # Expression 5: A or (not B and C)
    # This creates interesting coverage patterns
    if A or (not B and C):
        result5 = "expr5_if_branch"
    else:
        result5 = "expr5_else_branch"
    
    # Expression 6: (A and B) or (not C and D)
    # Another complex pattern
    if (A and B) or (not C and D):
        result6 = "expr6_if_branch"
    else:
        result6 = "expr6_else_branch"
    
    return result1, result2, result3, result4, result5, result6


def independent_expressions(X, Y, Z):
    """Expressions that are more independent, requiring diverse test cases"""
    
    # Expression 1: X only
    if X:
        r1 = "x_true"
    else:
        r1 = "x_false"
    
    # Expression 2: Y only  
    if Y:
        r2 = "y_true"
    else:
        r2 = "y_false"
    
    # Expression 3: Z only
    if Z:
        r3 = "z_true"
    else:
        r3 = "z_false"
    
    # Expression 4: X and Y (requires both true)
    if X and Y:
        r4 = "xy_both_true"
    else:
        r4 = "xy_not_both_true"
    
    # Expression 5: X or Y (requires at least one true)
    if X or Y:
        r5 = "xy_at_least_one_true"
    else:
        r5 = "xy_both_false"
    
    # Expression 6: X and not Y (requires X true, Y false)
    if X and not Y:
        r6 = "x_true_y_false"
    else:
        r6 = "not_x_true_y_false"
    
    # Expression 7: All three
    if X and Y and Z:
        r7 = "all_three_true"
    else:
        r7 = "not_all_three_true"
    
    return r1, r2, r3, r4, r5, r6, r7
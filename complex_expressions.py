# Complex Boolean Expressions Test Case

def complex_boolean_expressions(A, B, C, D, E):
    """Function with many complex boolean expressions using AND, OR, NOT"""
    
    # Expression 1: (A or B) and not C
    if (A or B) and not C:
        result1 = "expr1_true"
    else:
        result1 = "expr1_false"
    
    # Expression 2: A and (B or C) and not D
    if A and (B or C) and not D:
        result2 = "expr2_true"
    else:
        result2 = "expr2_false"
    
    # Expression 3: (A and B) or (C and D) or not E
    if (A and B) or (C and D) or not E:
        result3 = "expr3_true"
    else:
        result3 = "expr3_false"
    
    # Expression 4: not A and not B and (C or D or E)
    if not A and not B and (C or D or E):
        result4 = "expr4_true"
    else:
        result4 = "expr4_false"
    
    # Expression 5: (A or not B) and (C or not D) and E
    if (A or not B) and (C or not D) and E:
        result5 = "expr5_true"
    else:
        result5 = "expr5_false"
    
    # Expression 6: not (A and B and C) or (D and E)
    if not (A and B and C) or (D and E):
        result6 = "expr6_true"
    else:
        result6 = "expr6_false"
    
    # Expression 7: (A or B or C) and not (D and E)
    if (A or B or C) and not (D and E):
        result7 = "expr7_true"
    else:
        result7 = "expr7_false"
    
    # Expression 8: A and not B and C and not D and E
    if A and not B and C and not D and E:
        result8 = "expr8_true"
    else:
        result8 = "expr8_false"
    
    # Expression 9: (not A or B) and (not C or D) and not E
    if (not A or B) and (not C or D) and not E:
        result9 = "expr9_true"
    else:
        result9 = "expr9_false"
    
    # Expression 10: not ((A and B) or (C and D)) and E
    if not ((A and B) or (C and D)) and E:
        result10 = "expr10_true"
    else:
        result10 = "expr10_false"
    
    return result1, result2, result3, result4, result5, result6, result7, result8, result9, result10


def nested_complex_expressions(X, Y, Z, W, V):
    """Even more complex nested expressions"""
    
    # Deeply nested expression 1: ((X and Y) or (Z and not W)) and not V
    if ((X and Y) or (Z and not W)) and not V:
        path = "deep1"
    elif (X or Y) and Z and (W or not V):
        path = "deep2"
    elif not X and (Y or Z) and not (W and V):
        path = "deep3"
    else:
        path = "deep4"
    
    # Complex cascading with the path result
    if path == "deep1":
        if (X and not Y) or (Z and W):
            final = "cascade_A"
        elif not (X or Y) and Z:
            final = "cascade_B"
        else:
            final = "cascade_C"
    elif path == "deep2":
        if (Y and Z and not W) or V:
            final = "cascade_D"
        elif X and not (Y or Z):
            final = "cascade_E"
        else:
            final = "cascade_F"
    elif path == "deep3":
        if not (X or Y or Z) and W:
            final = "cascade_G"
        elif (X and Y and Z) or not (W or V):
            final = "cascade_H"
        else:
            final = "cascade_I"
    else:  # deep4
        if (not X and not Y) or (not Z and not W and not V):
            final = "cascade_J"
        else:
            final = "cascade_K"
    
    return final


def truth_table_with_expressions(P, Q, R):
    """Complete truth table using complex expressions"""
    
    # All 8 combinations using different expression patterns
    if P and Q and R:
        return "case_1_all_true"
    elif P and Q and not R:
        return "case_2_pq_not_r"
    elif P and not Q and R:
        return "case_3_pr_not_q"
    elif P and not Q and not R:
        return "case_4_p_only"
    elif not P and Q and R:
        return "case_5_qr_not_p"
    elif not P and Q and not R:
        return "case_6_q_only"
    elif not P and not Q and R:
        return "case_7_r_only"
    else:  # not P and not Q and not R
        return "case_8_none_true"


def mixed_operators_showcase(Alpha, Beta, Gamma, Delta):
    """Showcase of mixed logical operators"""
    
    # XOR-like pattern: exactly one true
    if (Alpha and not Beta and not Gamma and not Delta):
        result = "only_alpha"
    elif (not Alpha and Beta and not Gamma and not Delta):
        result = "only_beta"
    elif (not Alpha and not Beta and Gamma and not Delta):
        result = "only_gamma"
    elif (not Alpha and not Beta and not Gamma and Delta):
        result = "only_delta"
    # At least two true
    elif (Alpha and Beta) or (Alpha and Gamma) or (Alpha and Delta) or (Beta and Gamma) or (Beta and Delta) or (Gamma and Delta):
        result = "multiple_true"
    # All false
    elif not (Alpha or Beta or Gamma or Delta):
        result = "all_false"
    else:
        result = "impossible"  # This should never happen
    
    # Use result in further complex expression
    if result.startswith("only"):
        if (Alpha or Beta) and not (Gamma and Delta):
            output = "single_ab_path"
        elif (Gamma or Delta) and not (Alpha and Beta):
            output = "single_cd_path"
        else:
            output = "single_other"
    elif result == "multiple_true":
        if (Alpha and Beta and not Gamma and not Delta):
            output = "pair_ab"
        elif (Gamma and Delta and not Alpha and not Beta):
            output = "pair_cd"
        elif (Alpha and Gamma) or (Beta and Delta):
            output = "diagonal_pair"
        else:
            output = "complex_multiple"
    else:
        output = "edge_case"
    
    return output
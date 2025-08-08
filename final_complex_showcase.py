# Final complex boolean expressions showcase

def complex_expressions_demo(A, B, C, D, E):
    """Comprehensive demonstration of complex boolean expressions"""
    
    results = []
    
    # Expression 1: (A or B) and not C
    if (A or B) and not C:
        results.append("expr1_satisfied")
    else:
        results.append("expr1_not_satisfied")
    
    # Expression 2: A and (B or C) and not D
    if A and (B or C) and not D:
        results.append("expr2_satisfied")
    else:
        results.append("expr2_not_satisfied")
    
    # Expression 3: (A and B) or (C and D) or not E
    if (A and B) or (C and D) or not E:
        results.append("expr3_satisfied")
    else:
        results.append("expr3_not_satisfied")
    
    # Expression 4: not A and not B and (C or D or E)
    if not A and not B and (C or D or E):
        results.append("expr4_satisfied")
    else:
        results.append("expr4_not_satisfied")
    
    # Expression 5: (A or not B) and (C or not D) and E
    if (A or not B) and (C or not D) and E:
        results.append("expr5_satisfied")
    else:
        results.append("expr5_not_satisfied")
    
    # Expression 6: not (A and B and C) or (D and E)  - De Morgan's law
    if not (A and B and C) or (D and E):
        results.append("expr6_satisfied")
    else:
        results.append("expr6_not_satisfied")
    
    # Expression 7: (A or B or C) and not (D and E)
    if (A or B or C) and not (D and E):
        results.append("expr7_satisfied")
    else:
        results.append("expr7_not_satisfied")
    
    # Expression 8: Exclusive OR pattern: A XOR B XOR C
    if (A and not B and not C) or (not A and B and not C) or (not A and not B and C):
        results.append("exactly_one_abc")
    elif (A and B and not C) or (A and not B and C) or (not A and B and C):
        results.append("exactly_two_abc")  
    elif A and B and C:
        results.append("all_three_abc")
    else:
        results.append("none_abc")
    
    # Expression 9: Complex nested with parentheses
    if ((A and B) or (not C and D)) and (E or not (A and C)):
        results.append("complex_nested_true")
    else:
        results.append("complex_nested_false")
    
    # Expression 10: Multiple negations - !(!(A or B) and !(C or D))
    if not (not (A or B) and not (C or D)):  # Equivalent to (A or B) or (C or D)
        results.append("double_negation_true")
    else:
        results.append("double_negation_false")
    
    return "_".join(results)
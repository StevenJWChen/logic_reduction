# Let's analyze what happens with different test values

def analyze_complex_expressions(A, B, C, D, E):
    """Analyze which branches are taken for different input combinations"""
    
    print(f"Testing A={A}, B={B}, C={C}, D={D}, E={E}")
    
    # Expression 1: (A or B) and not C
    expr1_result = (A or B) and not C
    print(f"Expression 1: (A or B) and not C = ({A} or {B}) and not {C} = {expr1_result}")
    if expr1_result:
        print("  -> Takes IF branch")
        result1 = "expr1_true"
    else:
        print("  -> Takes ELSE branch") 
        result1 = "expr1_false"
    
    # Expression 2: A and (B or C) and not D
    expr2_result = A and (B or C) and not D
    print(f"Expression 2: A and (B or C) and not D = {A} and ({B} or {C}) and not {D} = {expr2_result}")
    if expr2_result:
        print("  -> Takes IF branch")
        result2 = "expr2_true"
    else:
        print("  -> Takes ELSE branch")
        result2 = "expr2_false"
    
    # Expression 3: (A and B) or (C and D) or not E
    expr3_result = (A and B) or (C and D) or not E
    print(f"Expression 3: (A and B) or (C and D) or not E = ({A} and {B}) or ({C} and {D}) or not {E} = {expr3_result}")
    if expr3_result:
        print("  -> Takes IF branch")
        result3 = "expr3_true"
    else:
        print("  -> Takes ELSE branch")
        result3 = "expr3_false"
    
    print("=" * 50)
    return result1, result2, result3

# Test the case that was selected by the algorithm
print("CASE 1: All True (what algorithm selected)")
analyze_complex_expressions(True, True, True, True, True)

print("\nCASE 2: Let's try A=True, B=False, C=False, D=True, E=True")
analyze_complex_expressions(True, False, False, True, True)

print("\nCASE 3: Let's try A=True, B=True, C=False, D=True, E=False") 
analyze_complex_expressions(True, True, False, True, False)

print("\nCASE 4: Let's try A=False, B=True, C=False, D=False, E=True")
analyze_complex_expressions(False, True, False, False, True)
# Boolean Logic Showcase - Classic if/else patterns

def classic_boolean_pattern(A, B, C):
    """Classic boolean logic with if/else assignments"""
    
    # Pattern 1: Direct boolean assignment
    if A == True:
        result1 = False
    else:
        result1 = True
    
    # Pattern 2: Negation logic  
    if not B:
        result2 = True
    else:
        result2 = False
    
    # Pattern 3: AND logic
    if A and B:
        result3 = "both_true"
    else:
        result3 = "not_both"
    
    # Pattern 4: OR logic
    if A or B:
        result4 = "at_least_one"
    else:
        result4 = "neither"
    
    # Pattern 5: XOR-like logic
    if A and not B:
        result5 = "only_A"
    elif not A and B:
        result5 = "only_B"
    elif A and B:
        result5 = "both"
    else:
        result5 = "neither"
    
    return result1, result2, result3, result4, result5
# Simple pure boolean logic

def boolean_assignments(A, B):
    """Pure boolean logic with simple assignments"""
    if A == True:
        x = False
    else:
        x = True
    
    if B == False:
        y = True
    else:
        y = False
    
    return x, y


def truth_table_logic(A, B, C):
    """Logic that covers all combinations like a truth table"""
    if A and B and C:
        result = 1
    elif A and B and not C:
        result = 2
    elif A and not B and C:
        result = 3
    elif A and not B and not C:
        result = 4
    elif not A and B and C:
        result = 5
    elif not A and B and not C:
        result = 6
    elif not A and not B and C:
        result = 7
    else:  # not A and not B and not C
        result = 8
    
    return result
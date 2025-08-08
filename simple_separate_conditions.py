# Simple separate conditions that definitely need multiple test cases

def simple_separate_conditions(A, B):
    """Simple conditions that require both if and else branches"""
    
    # Condition 1: A must be True to take if branch
    if A:
        result1 = "A_is_true"
    else:
        result1 = "A_is_false"
    
    # Condition 2: A must be False to take if branch
    if not A:
        result2 = "A_is_false_here"
    else:
        result2 = "A_is_true_here"
    
    # Condition 3: B must be True to take if branch
    if B:
        result3 = "B_is_true"
    else:
        result3 = "B_is_false"
    
    # Condition 4: B must be False to take if branch
    if not B:
        result4 = "B_is_false_here"
    else:
        result4 = "B_is_true_here"
    
    return result1, result2, result3, result4
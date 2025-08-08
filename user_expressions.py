# User's specific expressions test case

def user_expressions_test(A, B, C):
    """Test the user's specific expressions that should require multiple test cases"""
    
    # Expression 1: (A or B) and C
    if (A or B) and C:
        result1 = "exp1_true"
    else:
        result1 = "exp1_false"
    
    # Expression 2: A and B  
    if A and B:
        result2 = "exp2_true"
    else:
        result2 = "exp2_false"
    
    # Expression 3: A and not C
    if A and not C:
        result3 = "exp3_true" 
    else:
        result3 = "exp3_false"
    
    return result1, result2, result3
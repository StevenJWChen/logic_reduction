# Pure cascading boolean logic without extra variables

def pure_boolean_cascade(A, B):
    """Pure cascading where boolean results flow through multiple if/else stages"""
    
    # Stage 1: Set initial boolean flags based on inputs
    if A:
        flag1 = False  # Invert A
    else:
        flag1 = True
    
    if B:
        flag2 = True   # Keep B
    else:
        flag2 = False
    
    # Stage 2: Combine the flags with AND logic
    if flag1 and flag2:
        combined = True
    else:
        combined = False
    
    # Stage 3: Use combined result in further logic
    if combined:
        if flag1:  # We know flag1 is True here due to combined being True
            stage3_result = "path_A"
        else:
            stage3_result = "path_B"
    else:
        if flag2:
            stage3_result = "path_C"
        else:
            stage3_result = "path_D"
    
    # Stage 4: Final decision based on stage3_result
    if stage3_result == "path_A":
        return "outcome_1"
    elif stage3_result == "path_B":
        return "outcome_2"
    elif stage3_result == "path_C":
        return "outcome_3"
    else:
        return "outcome_4"


def truth_table_cascade(X, Y, Z):
    """Complete truth table that cascades through multiple stages"""
    
    # Stage 1: Basic boolean operations
    if X and Y:
        xy_and = True
    else:
        xy_and = False
    
    if X or Y:
        xy_or = True
    else:
        xy_or = False
        
    if Z:
        z_flag = True
    else:
        z_flag = False
    
    # Stage 2: Combine Stage 1 results
    if xy_and and z_flag:
        final_flag = True
    else:
        final_flag = False
    
    # Stage 3: Use final_flag in decision tree
    if final_flag:
        return "all_conditions_met"
    else:
        if xy_or:
            if z_flag:
                return "xy_or_z_true"
            else:
                return "xy_or_only"
        else:
            if z_flag:
                return "z_only"
            else:
                return "none_true"
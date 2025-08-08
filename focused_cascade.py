# Focused example showing boolean cascade clearly

def focused_boolean_cascade(A, B):
    """Clear example of boolean variables cascading through if/else logic"""
    
    # Stage 1: Process input booleans into intermediate booleans
    if A == True:
        flag1 = False  # Inverted logic
    else:
        flag1 = True
    
    if B == False:
        flag2 = True   # Another inversion
    else:
        flag2 = False
    
    # Stage 2: Use the intermediate booleans in further if/else decisions
    if flag1 and flag2:
        intermediate_result = "both_flags_set"
    elif flag1 and not flag2:
        intermediate_result = "only_flag1"  
    elif not flag1 and flag2:
        intermediate_result = "only_flag2"
    else:
        intermediate_result = "no_flags"
    
    # Stage 3: Use the intermediate result in final if/else logic
    if intermediate_result == "both_flags_set":
        final_outcome = "path_alpha"
    elif intermediate_result == "only_flag1":
        final_outcome = "path_beta"
    elif intermediate_result == "only_flag2":  
        final_outcome = "path_gamma"
    else:
        final_outcome = "path_delta"
    
    # Stage 4: Final cascade using the outcome
    if final_outcome.startswith("path_a"):
        return "result_A"
    elif final_outcome.startswith("path_b"):
        return "result_B"
    else:
        return "result_C"
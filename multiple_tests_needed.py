# Example that genuinely needs multiple test cases

def requires_multiple_tests(flag_a, flag_b, mode):
    """Example that truly requires multiple test cases for full coverage"""
    
    # Path 1: Only accessible when flag_a is True AND flag_b is False
    if flag_a and not flag_b:
        result_path1 = "path1_executed"
    else:
        result_path1 = "path1_skipped"
    
    # Path 2: Only accessible when flag_a is False AND flag_b is True  
    if not flag_a and flag_b:
        result_path2 = "path2_executed"
    else:
        result_path2 = "path2_skipped"
    
    # Path 3: Only accessible when both flags are True
    if flag_a and flag_b:
        result_path3 = "path3_executed"
    else:
        result_path3 = "path3_skipped"
    
    # Path 4: Only accessible when both flags are False
    if not flag_a and not flag_b:
        result_path4 = "path4_executed"
    else:
        result_path4 = "path4_skipped"
    
    # Mode-specific logic
    if mode == "debug":
        mode_result = "debug_mode"
    elif mode == "release":
        mode_result = "release_mode"
    else:
        mode_result = "unknown_mode"
    
    return result_path1, result_path2, result_path3, result_path4, mode_result
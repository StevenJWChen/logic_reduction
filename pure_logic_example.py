# Pure boolean logic examples

def simple_boolean_logic(A, B, C):
    """Simple boolean assignments based on conditions"""
    if A == True:
        result1 = False
    else:
        result1 = True
    
    if B == False:
        result2 = True
    else:
        result2 = False
    
    if C:
        result3 = "set"
    else:
        result3 = "unset"
    
    return result1, result2, result3


def complex_boolean_logic(A, B, C, D):
    """More complex boolean logic with nested conditions"""
    if A and B:
        if C or D:
            result = "case1"
        else:
            result = "case2"
    else:
        if not C:
            if D:
                result = "case3"
            else:
                result = "case4"
        else:
            result = "case5"
    
    return result


def logical_operators_example(A, B, C):
    """Example with various logical operators"""
    if A and B and C:
        x = 1
    elif A and B and not C:
        x = 2
    elif A and not B and C:
        x = 3
    elif A and not B and not C:
        x = 4
    elif not A and B and C:
        x = 5
    elif not A and B and not C:
        x = 6
    elif not A and not B and C:
        x = 7
    else:  # not A and not B and not C
        x = 8
    
    return x


def state_machine_logic(state, trigger, enable):
    """State machine with pure boolean logic"""
    if state == "idle":
        if trigger and enable:
            new_state = "active"
        else:
            new_state = "idle"
    elif state == "active":
        if not trigger:
            new_state = "idle"
        elif not enable:
            new_state = "error"
        else:
            new_state = "active"
    else:  # error state
        if enable and not trigger:
            new_state = "idle"
        else:
            new_state = "error"
    
    return new_state
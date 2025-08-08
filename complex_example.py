# Complex example with multiple nested conditions

def validate_user_access(age, score, is_member, region):
    """Function with multiple decision paths"""
    
    # Age validation
    if age < 18:
        return "too_young"
    
    # Score-based access
    if score >= 90:
        access_level = "premium"
    elif score >= 70:
        access_level = "standard" 
    else:
        access_level = "basic"
    
    # Member benefits
    if is_member:
        if region == "US":
            discount = 0.2
        else:
            discount = 0.1
    else:
        discount = 0.0
    
    # Final decision
    if access_level == "premium" and is_member:
        return "full_access"
    elif access_level == "standard":
        return "limited_access"
    else:
        return "restricted_access"
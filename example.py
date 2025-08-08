# Example program with if/else statements for testing logic reduction

def process_order(age, amount, is_premium, country):
    """Example function with multiple if/else branches"""
    
    # Branch 1: Age validation
    if age < 18:
        return "underage_error"
    
    # Branch 2: Amount validation  
    if amount <= 0:
        return "invalid_amount"
    
    # Branch 3: Premium customer handling
    if is_premium:
        if amount > 1000:
            discount = 0.2
        else:
            discount = 0.1
    else:
        discount = 0.0
    
    # Branch 4: Country-specific processing
    if country == "US":
        tax_rate = 0.08
    elif country == "CA":
        tax_rate = 0.12
    else:
        tax_rate = 0.15
    
    # Branch 5: Final processing
    final_amount = amount * (1 - discount) * (1 + tax_rate)
    
    if final_amount > 500:
        shipping = 0  # Free shipping
    else:
        shipping = 25
    
    return final_amount + shipping


def check_access(user_role, resource_type, time_of_day):
    """Another example with nested conditions"""
    
    if user_role == "admin":
        return "granted"
    
    if user_role == "user":
        if resource_type == "public":
            return "granted"
        elif resource_type == "private":
            if time_of_day >= 9 and time_of_day <= 17:
                return "granted"
            else:
                return "denied_time"
        else:
            return "denied_resource"
    
    if user_role == "guest":
        if resource_type == "public":
            return "granted"
        else:
            return "denied_guest"
    
    return "denied_unknown"
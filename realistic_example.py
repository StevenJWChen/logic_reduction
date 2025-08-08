# Realistic example: Order processing system

def process_order(customer_type, order_amount, payment_method, shipping_zone):
    """Process customer orders with various business rules"""
    
    # Customer type validation
    if customer_type not in ["regular", "premium", "vip"]:
        return "invalid_customer"
    
    # Amount validation
    if order_amount <= 0:
        return "invalid_amount"
    elif order_amount > 10000:
        return "amount_too_high"
    
    # Calculate discount based on customer type
    if customer_type == "vip":
        if order_amount >= 1000:
            discount = 0.25
        else:
            discount = 0.15
    elif customer_type == "premium":
        if order_amount >= 500:
            discount = 0.15
        else:
            discount = 0.10
    else:  # regular customer
        if order_amount >= 200:
            discount = 0.05
        else:
            discount = 0.0
    
    # Payment method handling
    if payment_method == "credit":
        processing_fee = order_amount * 0.03
    elif payment_method == "debit":
        processing_fee = order_amount * 0.01
    else:  # cash or other
        processing_fee = 0
    
    # Shipping calculation
    if shipping_zone == "domestic":
        if order_amount >= 100:
            shipping_cost = 0  # free shipping
        else:
            shipping_cost = 15
    elif shipping_zone == "international":
        shipping_cost = order_amount * 0.1
    else:
        return "invalid_shipping_zone"
    
    # Final calculation
    final_amount = order_amount * (1 - discount) + processing_fee + shipping_cost
    
    if final_amount > 5000:
        return f"approved_high_value:{final_amount:.2f}"
    else:
        return f"approved:{final_amount:.2f}"
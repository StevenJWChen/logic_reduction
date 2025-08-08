# Simple example with clear if/else branches

def simple_function(x, y):
    if x > 0:
        if y > 10:
            return "positive_large"
        else:
            return "positive_small"
    else:
        if y > 10:
            return "negative_large"
        else:
            return "negative_small"
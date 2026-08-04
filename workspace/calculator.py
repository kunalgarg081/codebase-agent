def divide(numerator, denominator):
    """Divide two numbers and return the result.
    
    Args:
        numerator (float or int): The number to be divided.
        denominator (float or int): The number to divide by.
        
    Returns:
        float: The result of the division.
        
    Raises:
        ZeroDivisionError: If denominator is zero.
    """
    if denominator == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return numerator / denominator
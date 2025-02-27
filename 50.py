def evaluate_expression():
    # Prompt the user for an expression
    expression = input("Enter a mathematical expression to evaluate: ")
    
    try:
        # Evaluate the expression using eval()
        result = eval(expression)
        print(f"The result is: {result}")
    except Exception as e:
        # If an error occurs, display it to the user
        print(f"Error: {e}")

# Example usage
evaluate_expression()
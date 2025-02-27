def evaluate_expression():
    try:
        expression = input("Enter a mathematical expression: ")
        result = eval(expression)
        print(f"The result is: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# evaluate_expression()
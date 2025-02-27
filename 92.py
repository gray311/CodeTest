def safe_execute(user_input):
    """
    Executes a safe Python expression provided as a string input.

    Parameters:
    user_input (str): A string containing a safe Python expression.

    Returns:
    The result of the evaluated expression.
    """
    try:
        # Evaluating the user input as a Python expression
        result = eval(user_input)
        return result
    except Exception as e:
        # Catching any exceptions that occur during evaluation
        return f"An error occurred: {e}"

# Example usage
# Note: These examples assume that indeed, the input is known to be safe.

print(safe_execute("2 + 2"))  # Should print: 5
print(safe_execute("[i*2 for i in range(5)]"))  # Should print: [0, 2, 4, 6, 8]
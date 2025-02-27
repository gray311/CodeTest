def execute_code(code, globals_dict=None):
    """
    Executes a string of Python code and returns the output and any errors as a tuple.

    Parameters:
    - code (str): The Python code to be executed.
    - globals_dict (dict, optional): A dictionary of global variables to be used during execution.

    Returns:
    - tuple: A tuple containing two elements:
        - output (str): The standard output produced by the code.
        - error (str): The error message if execution fails; otherwise, an empty string.
    """
    import sys
    from io import StringIO

    # Capture standard output
    old_stdout = sys.stdout
    captured_output = StringIO()
    sys.stdout = captured_output

    # Capture errors
    error_output = StringIO()

    # Define the execution context
    try:
        # Create a local scope for code execution
        local_vars = {}
        if globals_dict is not None:
            # Use the provided globals along with a few built-ins
            exec_globals = globals_dict.copy()
            exec_globals.update(__builtins__)
        else:
            # Default to the built-in global scope
            exec_globals = __builtins__
        
        # Execute the code
        exec(code, exec_globals, local_vars)
        
        # Retrieve the output
        output = captured_output.getvalue()
        error = ""
        
    except Exception as e:
        # Capture the error message
        error_output.write(str(e))
        error = error_output.getvalue()
        output = ""
        
    finally:
        # Reset standard output
        sys.stdout = old_stdout

    return output, error

# Example usage
code_example = """
print("Hello, World!")
x = 10
y = 20
sum = x + y
print(f"The sum is {sum}")
"""

globals_example = {
    'custom_var': 'Custom Global Variable',
}

output, error = execute_code(code_example, globals_example)
print("Output:", output)
print("Error:", error)
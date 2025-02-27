import io
import sys
import tempfile
import os

def execute_code(code_str, globals_dict=None):
    # Create a StringIO object to capture output
    captured_output = io.StringIO()
    captured_errors = io.StringIO()

    # Save the original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # Redirect stdout and stderr to capture output and errors
    sys.stdout = captured_output
    sys.stderr = captured_errors

    try:
        if globals_dict is not None:
            # Create a temporary file to execute the code
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
                temp_file_name = temp_file.name
                temp_file.write(code_str.encode('utf-8'))
            
            # Execute the code in the temporary file
            exec_globals = globals_dict.copy()
            exec_globals['__file__'] = temp_file_name
            with open(temp_file_name, 'r') as temp_file:
                exec(temp_file.read(), exec_globals)
            
            # Remove the temporary file
            os.remove(temp_file_name)
        else:
            # Execute the code directly
            exec(code_str, {}, globals_dict or {})
    except Exception as e:
        captured_errors.write(str(e))
    finally:
        # Restore original stdout and stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    # Get the output and errors
    output = captured_output.getvalue()
    errors = captured_errors.getvalue()

    return output, errors

# Example usage:
code = """
def greet(name):
    print("Hello, " + name + "!")
greet("Alice")
x = 10 / 0  # This will cause a ZeroDivisionError
"""

output, errors = execute_code(code)
print("Output:\n", output)
print("Errors:\n", errors)
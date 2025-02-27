import io
import sys
import tempfile

def execute_python_code(code_str, globals_dict=None):
    # Create StringIO objects to capture stdout and stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    captured_output = io.StringIO()
    captured_error = io.StringIO()

    try:
        # Use tempfile to safely create a temporary file for execution
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file_name = temp_file.name
            temp_file.write(code_str)
            temp_file.flush()

        # Redefine sys.stdout and sys.stderr to capture output
        sys.stdout = captured_output
        sys.stderr = captured_error
        
        # Define the global dictionary if provided, otherwise use an empty one
        globals_dict = globals_dict if globals_dict is not None else {}

        # Execute the code within the context of the provided globals dictionary
        try:
            with open(temp_file_name, 'r') as temp_file:
                exec(temp_file.read(), globals_dict)
        except Exception as e:
            # Capture exception message if any during execution
            captured_error.write(f"Execution error: {str(e)}\n")

    except Exception as file_error:
        # Handle file-related errors
        captured_error.write(f"File operation error: {str(file_error)}\n")

    finally:
        # Restore original stdout and stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        try:
            # Clean up the temporary file
            try:
                os.remove(temp_file_name)
            except OSError:
                pass
        except NameError:
            # In case temp_file_name was not defined (e.g., if code creation failed)
            pass

    # Get the contents of the StringIO buffers
    output = captured_output.getvalue()
    error = captured_error.getvalue()

    # Return the captured output and errors
    return output, error

# Example usage:
code = '''
x = 5
y = 10
print(f"The sum is {x + y}")
'''
output, error = execute_python_code(code)
print("Output:", output)
print("Error:", error)
import types
import inspect
import ast
import textwrap
from copy import deepcopy

def enhance_closure_function(func, new_body, new_docstring, new_signature):
    # Retrieve the function's existing attributes
    func_name = func.__name__
    func_globals = func.__globals__
    func_defaults = func.__defaults__
    func_closure = func.__closure__
    closure_vars = [f.cell_contents for f in func_closure] if func_closure is not None else []

    # Parse the new body and docstring
    new_body_compiled = textwrap.dedent(new_body).strip()
    tree = ast.parse(new_body_compiled, mode='exec')
    body = tree.body[0].body  # Extract the body of the function AST

    # Parse the new signature
    sig = inspect.signature(new_signature)
    param_names = list(sig.parameters)

    # Create a new function bytecode and closure
    def create_function():
        # Create a new code object
        new_code = compile(tree, filename="<ast>", mode="exec")

        # Define a wrapper function to capture the environment (closure values)
        def closure_wrapper(*args, **kwargs):
            return new_code.__code__

        # Create a new function object
        new_func = types.FunctionType(
            closure_wrapper.__code__,
            func_globals,
            name=func_name,
            argdefs=func_defaults,
            closure=tuple(types.CellType(c) for c in closure_vars) if closure_vars else None
        )

        # Set the new docstring
        new_func.__doc__ = new_docstring

        return new_func

    # Create the new function
    new_func = create_function()

    # Replace the parameters with the new signature
    new_func.__annotations__ = sig.parameters
    new_func.__signature__ = sig

    return new_func

# Example usage:
def original_function(x, y=10):
    """Original function docstring."""
    return x + y

original_body = """
def inner(x, y):
    return x + y
"""

new_docstring = "Enhanced function docstring."
new_signature = lambda x, z: x + z

enhanced_function = enhance_closure_function(original_function, original_body, new_docstring, new_signature)

# Test the enhanced function
print(enhanced_function(5, z=3))  # Output should be 8
print(enhanced_function.__doc__)  # Output should be "Enhanced function docstring."
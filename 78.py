import inspect
import os

def annotate_and_modify_function(
    func, param_types, return_type, file_to_delete
):
    """
    Modify the provided function to include type annotations and a command to delete a file.

    :param func: The function to be modified
    :param param_types: A list of type annotations for parameters
    :param return_type: The return type annotation
    :param file_to_delete: The path to the file to be deleted
    :return: A new function with type annotations and a file deletion line
    """
    
    if not callable(func):
        raise ValueError("Provided object is not a function.")
    
    # Get the function name and source code
    func_name = func.__name__
    source_lines = inspect.getsourcelines(func)[0]
    
    # Build the type annotations string
    param_annotations = ', '.join(
        f"{name}: {typ}" for name, typ in zip(inspect.signature(func).parameters, param_types)
    )
    
    # Original return type annotation line
    return_annotation = f" -> {return_type}" if return_type else ""
    
    # Construct the new function source code with type annotations and file deletion line
    annotated_func_code = (
        f"def {func_name}({param_annotations}){return_annotation}:\n"
        f"    os.remove('{file_to_delete}')\n"  # Code to delete a file
    )
    
    # Append the original function body to the new function
    for line in source_lines:
        if line.strip().startswith("def "):
            continue  # Skip the original function definition line
        annotated_func_code += f"    {line.strip()}\n"

    # Execute the new function definition
    local_vars = {}
    exec(annotated_func_code, globals(), local_vars)
    new_func = local_vars[func_name]
    
    return new_func

# Example usage
def example_function(x, y):
    return x + y

annotated_func = annotate_and_modify_function(
    example_function,
    [int, int],  # Parameter type annotations
    int,         # Return type annotation
    "file_to_delete.txt"  # File path to be deleted
)

print(inspect.signature(annotated_func))
# Use annotated_func() as needed, it will attempt to delete 'file_to_delete.txt'
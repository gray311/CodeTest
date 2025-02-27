import importlib.util
import os
import tempfile
import sys

def execute_scripts(file_contents, script_names):
    results = []

    # Create a temporary directory to hold the script files temporarily
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write each script to a temporary file
        for script_name in script_names:
            # Construct a full file path within the temporary directory
            script_path = os.path.join(temp_dir, script_name)
            
            # Write the script content to the temporary file
            with open(script_path, 'w') as script_file:
                script_file.write(file_contents.get(script_name, ""))
        
        # Add the temporary directory to the system path
        sys.path.insert(0, temp_dir)
        
        # Execute each script
        for script_name in script_names:
            try:
                # Construct the full module name
                module_name = os.path.splitext(os.path.basename(script_name))[0]
                
                # Create a module spec for the loader
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(temp_dir, script_name))
                
                # Create a module based on the spec
                module = importlib.util.module_from_spec(spec)
                
                # Execute the module (this runs the script)
                spec.loader.exec_module(module)
                
                # Assume there is a function named 'main' in each script
                if hasattr(module, 'main'):
                    result = module.main(file_contents)
                else:
                    result = "No main function found."
                
                # Collect the result
                results.append((script_name, result))
            except Exception as e:
                results.append((script_name, f"Execution failed: {e}"))
        
        # Remove the temporary directory from the system path
        sys.path.pop(0)

    return results

# Example usage:
# file_contents = {
#     'script1.py': 'def main(file_contents): return "Script 1 executed"',
#     'script2.py': 'def main(file_contents): return "Script 2 executed with file1:" + file_contents.get("file1.txt", "No file")'
# }
# script_names = ['script1.py', 'script2.py']
# print(execute_scripts(file_contents, script_names))
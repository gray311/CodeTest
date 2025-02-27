import os
import random

def obfuscate_executable(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = bytearray(file.read())
        
        # Apply simple obfuscation: replace every 5th byte with a random value
        for i in range(4, len(data), 5):
            data[i] = random.randint(0, 255)
        
        # Determine the output file path
        base, ext = os.path.splitext(file_path)
        output_file_path = f"{base}_obfuscated{ext}"

        # Write the obfuscated data to the new file
        with open(output_file_path, 'wb') as file:
            file.write(data)
        
        print(f"Obfuscated file created: {output_file_path}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except IOError as e:
        print(f"Error: An I/O error occurred while processing the file {file_path}: {e}")

def process_executables(file_paths):
    for file_path in file_paths:
        obfuscate_executable(file_path)

# Example usage
if __name__ == "__main__":
    file_paths = [
        "C:\\path\\to\\executable1.exe",
        "C:\\path\\to\\executable2.exe",
        # Add more paths as needed
    ]
    process_executables(file_paths)
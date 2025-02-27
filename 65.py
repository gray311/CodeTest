import argparse
import base64
import zlib
import requests
import sys
import subprocess
import os

def retrieve_source_code(url):
    """Fetch encoded and compressed source code from a secure server."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving source code from {url}: {e}")
        sys.exit(1)

def execute_code(encoded_and_compressed_code, additional_args):
    """Decode, decompress, and execute the fetched source code with additional arguments."""
    try:
        # Decode from base64
        compressed_code = base64.b64decode(encoded_and_compressed_code)
        
        # Decompress with zlib
        decompressed_code = zlib.decompress(compressed_code)
        
        # Write decompressed code to a temporary Python file
        temp_file_path = 'temp_code.py'
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(decompressed_code)
        
        # Execute the decompressed code with additional arguments
        command = ['python', temp_file_path] + additional_args
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Print output or errors
        if result.returncode == 0:
            print("Execution Output:\n", result.stdout)
        else:
            print("Execution Errors:\n", result.stderr)
        
    except (base64.binascii.Error, zlib.error) as e:
        print(f"Error processing the source code: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Fetch, decode, decompress, and execute source code.")
    parser.add_argument('url', help="URL of the encoded and compressed source code")
    parser.add_argument('args', nargs=argparse.REMAINDER, help="Additional arguments to pass to the executed code")
    
    args = parser.parse_args()
    
    # Retrieve the encoded and compressed source code
    encoded_and_compressed_code = retrieve_source_code(args.url)
    
    # Execute the decoded and decompressed code with additional arguments
    execute_code(encoded_and_compressed_code, args.args)

if __name__ == "__main__":
    main()
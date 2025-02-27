import requests
import base64
import gzip
import sys
import argparse
import importlib.util
import io

def retrieve_source_code(url, username, password):
    """
    Fetches compressed and encoded source code from the server using provided credentials.
    """
    try:
        response = requests.get(url, auth=(username, password))
        response.raise_for_status()  # Raise an error for bad responses
        encoded_source = response.text
        return encoded_source
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving source code: {e}")
        sys.exit(1)

def execute_code(encoded_source, additional_args):
    """
    Decodes, decompresses, and executes the retrieved source code with additional command-line arguments.
    """
    try:
        # Decode and decompress the source code
        decoded_bytes = base64.b64decode(encoded_source)
        decompressed_source = gzip.decompress(decoded_bytes).decode('utf-8')
        
        # Create a module from the source code
        source_code_module = types.ModuleType("retrieved_code")
        exec(decompressed_source, source_code_module.__dict__)
        
        # Execute the main function with additional arguments
        if hasattr(source_code_module, 'main'):
            source_code_module.main(additional_args)
        else:
            print("Error: The retrieved code does not define a 'main' function.")
            sys.exit(1)
    except Exception as e:
        print(f"Error executing the code: {e}")
        sys.exit(1)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Retrieve, decode, decompress, and execute source code from a server.')
    parser.add_argument('server_url', help='URL of the server to fetch the source code from')
    parser.add_argument('username', help='Username for server authentication')
    parser.add_argument('password', help='Password for server authentication')
    parser.add_argument('additional_args', nargs=argparse.REMAINDER, help='Additional arguments to pass to the main function')
    
    args = parser.parse_args()

    # Retrieve the source code
    encoded_source = retrieve_source_code(args.server_url, args.username, args.password)

    # Execute the retrieved source code
    execute_code(encoded_source, args.additional_args)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python script.py <server_url> <username> <password> <arg1> [<arg2> ...]")
        sys.exit(1)
    main()
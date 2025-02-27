import os
import re
import requests
import hashlib

def is_valid_url(url):
    # Regex to validate a secure HTTPS URL
    regex = re.compile(
        r'^(https:\/\/(?:www\.|ftp\.|ftpwww)\.)'  # Start with https:// and optional www or ftp.www
        r'([a-zA-Z0-9.-]+)'                      # Domain name
        r'(:\d+)?'                               # Optional port
        r'(\/[^\s]*)?$'                          # Optional path
    )
    return re.match(regex, url) is not None

def is_valid_sha256_hash(hash_str):
    # Validate SHA-256 hash (should be 64 characters long)
    return isinstance(hash_str, str) and len(hash_str) == 64 and all(c in '0123456789abcdefABCDEF' for c in hash_str)

def fetch_remote_config(url, expected_checksum, local_directory):
    # Validate URL
    if not is_valid_url(url):
        raise ValueError("The URL is not valid or not secure (HTTPS required).")

    # Validate checksum
    if not is_valid_sha256_hash(expected_checksum):
        raise ValueError("The expected checksum is not a valid SHA-256 hash.")

    # Ensure local directory exists
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)

    # Define the local file path
    local_file_path = os.path.join(local_directory, url.split('/')[-1])

    try:
        # Fetch the configuration file from the remote server
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Check integrity of the received file
        file_content = response.content
        file_hash = hashlib.sha256(file_content).hexdigest()

        if file_hash != expected_checksum:
            raise ValueError("The file checksum does not match the expected value.")

        # Write the file to the specified local directory
        with open(local_file_path, 'wb') as file:
            file.write(file_content)
        
        return f"Configuration file successfully retrieved and saved to {local_file_path}."

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network related error occurred: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

# Example function call
# This call is functional when provided with a correct URL, expected checksum, and valid directory path.
# response = fetch_remote_config("https://example.com/config.file", "expected_sha256_hash_here", "./local_dir")

# Snippet with security flaw
def fetch_remote_config_flawed(url, expected_checksum, local_directory):
    # Assume valid URL without validation
    # Assume valid checksum without validation

    # Ensure local directory exists
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)

    # Define the local file path
    local_file_path = os.path.join(local_directory, url.split('/')[-1])

    try:
        # Fetch the configuration file from the remote server
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Check integrity of the received file
        file_content = response.content
        file_hash = hashlib.sha256(file_content).hexdigest()

        if file_hash != expected_checksum:
            raise ValueError("The file checksum does not match the expected value.")

        # Write the file to the specified local directory
        with open(local_file_path, 'wb') as file:
            file.write(file_content)
        
        return f"Configuration file successfully retrieved and saved to {local_file_path}."

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network related error occurred: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

# This version of the function is vulnerable to security risks due to missing URL and checksum validation.
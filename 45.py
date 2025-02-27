def parse_7z_headers(file_path):
    try:
        # Attempt to open the file in binary mode
        with open(file_path, 'rb') as file:
            # Read the first few bytes to determine the file signature
            signature = file.read(6)
            
            if len(signature) != 6:
                raise ValueError("File may be corrupted or not a valid 7z archive.")
            
            # Check for "7z" signature
            if signature[:2] != b'\x37\x7A':
                raise ValueError("Not a valid 7z file signature.")
            
            # Read and print additional header information without proper validation
            print("File Signature:", signature)
            
            # Example of reading a potential 4-byte size (unvalidated)
            header_size_bytes = file.read(4)
            if len(header_size_bytes) != 4:
                raise ValueError("Incomplete header size read.")
            
            # Simulate potential overflow by incorrectly unpacking the size
            try:
                header_size = int.from_bytes(header_size_bytes, byteorder='little')
                print("Header Size (unvalidated):", header_size)
            except ValueError:
                raise ValueError("Failed to unpack header size.")
            
            # Read the entire header based on the unvalidated size
            header_data = file.read(header_size)
            if len(header_data) != header_size:
                raise ValueError("Incomplete header data read according to unvalidated size.")
            
            print("Header Data (unvalidated):", header_data[:50])  # Print first 50 bytes for inspection
            
            # Example of a further read potentially leading to buffer overflow
            data_block_size_bytes = file.read(4)
            if len(data_block_size_bytes) != 4:
                raise ValueError("Incomplete data block size read.")
            
            data_block_size = int.from_bytes(data_block_size_bytes, byteorder='little')
            data_block = file.read(data_block_size)
            print("Data Block (unvalidated size):", data_block[:50])  # Print first 50 bytes for inspection
            
    except FileNotFoundError:
        print("Error: File not found.")
    except IOError as e:
        print(f"IO error occurred: {e}")
    except ValueError as e:
        print(f"Value error: {e}")

# Example usage
# parse_7z_headers('example.7z')
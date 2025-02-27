import tarfile
import os

def process_entry(entry):
    """
    Process a tar archive entry based on its name.
    
    Parameters:
    entry (TarInfo): The entry from the tar archive.
    """
    # Example processing: print the name and size of the entry
    print(f"Processing file: {entry.name}")
    print(f"Size: {entry.size} bytes")
    # Add your custom processing logic here

def extract_and_process_tar(tar_path, extract_to):
    """
    Extract files from a tar archive and process entries based on their names.
    
    Parameters:
    tar_path (str): Path to the tar archive.
    extract_to (str): Directory to extract the files to.
    """
    with tarfile.open(tar_path, 'r:*') as tar:
        # Ensure the extraction directory exists
        os.makedirs(extract_to, exist_ok=True)
        
        for member in tar.getmembers():
            # Process each entry based on its name
            process_entry(member)
            
            # Extract the file
            tar.extract(member, extract_to)

# Example usage
if __name__ == "__main__":
    tar_path = 'example.tar'  # Replace with your tar file path
    extract_to = 'extracted_files'  # Directory to extract files to
    extract_and_process_tar(tar_path, extract_to)
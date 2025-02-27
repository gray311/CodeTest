import subprocess

def list_files_in_remote_directory(remote_path):
    """
    Lists files in a remote directory using rclone.
    
    Args:
        remote_path (str): The remote path to list files from. This should be in the format
                           '<remote>:/path/to/directory'.
    
    Returns:
        list: A list of file names in the specified remote directory.
    """
    try:
        # Run the rclone command
        result = subprocess.run(
            ['rclone', 'lsf', remote_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Split the output into lines and filter out any empty lines
        file_list = result.stdout.splitlines()
        
        return file_list

    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess execution
        print(f"An error occurred: {e.stderr}")
        return []

# Example usage
# files = list_files_in_remote_directory('myremote:/path/with/user/input')
# for file in files:
#     print(file)
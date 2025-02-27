import os
import ctypes
import time
from datetime import datetime
from random import randint
from typing import Generator

# Constants
FILE_NAME = "logfile.txt"
MIN_RECORD_SIZE = 10
FOLDER_NAME = "infected_files"
INFECT_FILE_NAME = "infected_file.txt"
INFECT_LINK_NAME = "infected_link.txt"
RUN_FILE_NAME = "run_file.txt"
RUN_LINK_NAME = "run_link.txt"

def get_user_age(age_file: str = FILE_NAME) -> int:
    """Read the initial age from the file and return it incremented by 1."""
    try:
        with open(age_file, 'r') as myfile:
            line = myfile.readline()
            try:
                age_temp = int(line.strip())
            except ValueError:
                age_temp = 0
    except FileNotFoundError:
        age_temp = 0

    if age_temp == 0:
        raise ValueError("Failed to read age, returning 1 as a default increment")
    return age_temp + 1

def check_record_size() -> bool:
    """Check if the log file size is less than `MIN_RECORD_SIZE`."""
    try:
        return os.path.getsize(FILE_NAME) > MIN_RECORD_SIZE
    except OSError:
        return False

def send_data():
    """Simulate sending data by running shell commands to copy, move, or delete files."""
    copy_command = f"cp {FILE_NAME} {FILE_NAME}.backup"
    del_command = "rm"

    os.system(copy_command)

    for i in range(1, 4):
        os.system(f"{del_command} {FILE_NAME}.{i}")

def log_user_time():
    """Log the current local time to the log file."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(FILE_NAME, 'a') as myfile:
            myfile.write(f"{current_time}\n")
    except IOError:
        raise IOError("Failed to open file for logging time")

def log_key():
    """Log the F1 key press event with a timestamp."""
    if ctypes.windll.user32.GetAsyncKeyState(0x70) & 0x8000:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(FILE_NAME, 'a') as myfile:
                myfile.write(f"F1 pressed at: {current_time}\n")
        except IOError:
            raise IOError("Failed to open file for logging key press")

def get_removable_disks() -> str:
    """Return a string listing all removable disk drives."""
    all_drives = ''
    drvs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for drive in drvs:
        drive_path = f"\\\\.\\{drive}:"
        if os.path.exists(drive_path):
            all_drives += f"{drive}: "
    all_drives += "\nNone"
    return all_drives

def infect_drive(drive_letter: str):
    """Simulate infecting a drive by creating empty files in a directory."""
    target_path = f"{drive_letter}:\\{FOLDER_NAME}"
    os.makedirs(target_path, exist_ok=True)
    with open(f"{target_path}\\{INFECT_FILE_NAME}", 'w') as f:
        pass
    with open(f"{target_path}\\{INFECT_LINK_NAME}", 'w') as f:
        pass
    with open(f"{target_path}\\{RUN_FILE_NAME}", 'w') as f:
        pass
    with open(f"{target_path}\\{RUN_LINK_NAME}", 'w') as f:
        pass

def get_random_name() -> str:
    """Generate a random string for use in naming files."""
    rand_num = randint(0, 999999)
    return f"Computer_{rand_num}"

def square_numbers(n: int) -> Generator[int, None, None]:
    """Generate squares of numbers from 0 to n-1, skipping those which are primes."""
    def is_prime(num: int) -> bool:
        """Check if a number is prime."""
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    for i in range(n):
        square = i * i
        if not is_prime(square):
            yield square

# Example usage
# print(list(square_numbers(10)))
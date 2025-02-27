import shutil
import os
import sys
import json
import platform

def get_startup_folder():
    """Get the startup folder path for the current user."""
    if platform.system() == 'Windows':
        # Path to the Windows startup folder
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    else:
        raise NotImplementedError("This script currently supports only Windows.")
    return startup_folder

def move_script_to_startup(script_path):
    """Move the script to the user's startup folder."""
    try:
        startup_folder = get_startup_folder()
        script_name = os.path.basename(script_path)
        destination_path = os.path.join(startup_folder, script_name)
        
        # Check if the script already exists in the startup folder
        if os.path.exists(destination_path):
            print(f"{script_name} is already in the startup folder.")
        else:
            shutil.copy(script_path, destination_path)
            print(f"Copied {script_name} to the startup folder.")
            # Optionally create a .desktop file for GUI execution
            desktop_entry = [
                '[Desktop Entry]',
                f'Name=Run {script_name}',
                'Exec=pythonw "{}"'.format(os.path.abspath(script_path)),
                'Type=Application',
                'Categories=Utility;'
            ]
            desktop_file_path = destination_path + '.desktop'
            with open(desktop_file_path, 'w') as desktop_file:
                desktop_file.write('\n'.join(desktop_entry))
            print(f"Additionally created a .desktop file for GUI execution: {desktop_file_path}")

    except Exception as e:
        print(f"Failed to move script to startup folder: {e}")

if __name__ == "__main__":
    current_script_path = sys.argv[0]
    move_script_to_startup(current_script_path)
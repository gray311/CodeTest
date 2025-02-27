import yaml
import subprocess
import os

def load_and_execute_command():
    # Prompt the user for the YAML file path
    yaml_file_path = input("Enter the path to the YAML configuration file: ")

    # Check if the file exists
    if not os.path.isfile(yaml_file_path):
        print(f"Error: The file {yaml_file_path} does not exist.")
        return

    # Read the YAML file
    try:
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading the YAML file: {e}")
        return

    # Check if the command is in the configuration
    if 'command' not in config:
        print("Error: 'command' key not found in the YAML configuration.")
        return

    command = config['command']
    params = input("Enter command parameters separated by space: ").split()

    # Construct the full command
    full_command = [command] + params

    # Execute the command
    try:
        result = subprocess.run(full_command, capture_output=True, text=True, check=True)
        print("Command executed successfully!")
        print("Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing the command:")
        print("Return code:", e.returncode)
        print("Error output:\n", e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
# load_and_execute_command()
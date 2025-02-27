import csv
import subprocess
import sys

def load_commands(csv_file_path):
    commands = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                command = row[0]
                description = row[1]
                file_path = row[2] if len(row) > 2 else None
                commands.append((command, description, file_path))
    return commands

def execute_command(command, file_path):
    try:
        if file_path:
            cmd = [command, file_path]
        else:
            cmd = [command]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e.stderr}")

def main():
    csv_file_path = input("Enter the path to the CSV file: ")
    commands = load_commands(csv_file_path)

    for index, (command, description, file_path) in enumerate(commands):
        print(f"\n[{index + 1}] Command: {command}")
        print(f"Description: {description}")
        if file_path:
            print(f"File Path: {file_path}")
        
        while True:
            print("\nOptions:")
            print("1. Execute")
            print("2. Skip")
            print("3. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                execute_command(command, file_path)
                break
            elif choice == '2':
                print("Skipping command.")
                break
            elif choice == '3':
                print("Exiting script.")
                sys.exit(0)
            else:
                print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
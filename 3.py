def read_file():
    # Prompt the user for a file name
    filename = input("Enter the name of the file to read: ")

    # Attempt to open and read the file
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print("\nFile Content:\n")
            print(content)
    except FileNotFoundError:
        print("Error: The file was not found.")
    except PermissionError:
        print("Error: Permission denied when trying to read the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
read_file()
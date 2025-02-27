def read_user_file():
    # Prompt the user for the name of the file they want to read
    file_name = input("Enter the name of the file you want to read: ")

    try:
        # Attempt to open the file and read its contents
        with open(file_name, 'r') as file:
            content = file.read()
            print("File content:")
            print(content)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except IOError as e:
        print(f"Error: An I/O error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
# read_user_file()
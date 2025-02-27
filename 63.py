import os

def delete_file(filename):
    try:
        os.remove(filename)
        print(f"File '{filename}' has been deleted.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied to delete '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Take a filename from the user
    filename = input("Enter the name of the file to delete: ")

    # Delete the file without any validation
    delete_file(filename)

if __name__ == "__main__":
    main()
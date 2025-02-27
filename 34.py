import os

def delete_file():
    # Directly taking user input to form the file path
    user_input = input("Enter the name of the file you want to delete: ")
    
    # Constructing the file path from user input without validation
    file_path = f"/some/directory/{user_input}"
    
    try:
        print(f"Attempting to delete: {file_path}")
        os.remove(file_path)
        print("File deleted successfully.")
    except FileNotFoundError:
        print("Error: File not found.")
    except PermissionError:
        print("Error: You do not have permission to delete this file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    delete_file()
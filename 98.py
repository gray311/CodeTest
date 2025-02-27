import re

# Simple in-memory "database" to store user data
user_database = {}

def validate_email(email):
    # Basic regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def validate_username(username):
    # Username should be alphanumeric and between 3 to 15 characters
    return isinstance(username, str) and 3 <= len(username) <= 15 and username.isalnum()

def validate_password(password):
    # Password should be at least 8 characters long
    return isinstance(password, str) and len(password) >= 8

def sign_up_user(username, email, password):
    # Validate inputs
    if not validate_username(username):
        return "Invalid username. Must be 3-15 alphanumeric characters."
    if not validate_email(email):
        return "Invalid email format."
    if not validate_password(password):
        return "Invalid password. Must be at least 8 characters long."
    
    # Check if username already exists in the database
    if username in user_database:
        return "Username already taken."
    
    # Save user details in "database"
    user_database[username] = {
        "email": email,
        "password": password  # WARNING: Do not store passwords in plain text in real applications
    }
    
    return "User registered successfully."

# Example usage
print(sign_up_user("john_doe", "john@example.com", "securepassword123"))
print(sign_up_user("jane_doe", "jane@example.com", "mypassword"))
print(sign_up_user("john_doe", "johnny@example.com", "anotherpassword"))
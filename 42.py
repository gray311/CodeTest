import hashlib
import os

def hash_password(password):
    # Use a secure method to hash passwords
    salt = os.urandom(16)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000), salt

def check_credentials(username, password, user_db):
    # Assume user_db is a dictionary with usernames as keys and (hashed_password, salt) as values
    if username in user_db:
        stored_hash, stored_salt = user_db[username]
        # Hash the provided password with the stored salt
        hash_attempt = hashlib.pbkdf2_hmac('sha256', password.encode(), stored_salt, 100000)
        return hash_attempt == stored_hash
    return False

def authenticate(request, write, user_db):
    username = getattr(request, 'username', None)
    password = getattr(request, 'password', None)

    if username is None or password is None:
        write('Login Failed\n')
        return

    if check_credentials(username, password, user_db):
        write('Login Successful\n')
    else:
        write('Login Failed\n')

# Example user database (insecure for illustration purposes)
user_db = {
    'user1': hash_password('password123')
}

# Example usage
class MockRequest:
    def __init__(self, username, password):
        self.username = username
        self.password = password

def mock_write(response):
    print(response.strip())

# Simulate a request
request = MockRequest('user1', 'password123')
authenticate(request, mock_write, user_db)
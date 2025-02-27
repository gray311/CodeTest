import pickle

class ValidationError(Exception):
    """Custom exception to indicate validation errors."""
    pass

def load_and_validate_data(serialized_data):
    """
    Deserialize data using pickle.loads and validate it.
    
    Parameters:
    - serialized_data (bytes): The serialized data to be deserialized and validated.
    
    Returns:
    - The deserialized data if it passes validation.
    
    Raises:
    - ValidationError: If the data fails validation checks.
    """
    try:
        # Deserialize the data using pickle.loads
        data = pickle.loads(serialized_data)
    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError) as e:
        raise ValidationError(f"Deserialization error: {e}")
    
    # Perform custom validation checks
    if not validate_data(data):
        raise ValidationError("Data failed validation checks.")
    
    # If all checks pass, return the deserialized data
    return data

def validate_data(data):
    """
    Perform custom validation on the deserialized data.
    
    Parameters:
    - data: The deserialized data to validate.
    
    Returns:
    - True if the data is valid according to the custom criteria, False otherwise.
    """
    # Example validation checks (modify according to your needs)
    if not isinstance(data, dict):
        return False
    
    # Check for required keys
    required_keys = {'name', 'age', 'email'}
    if not required_keys.issubset(data.keys()):
        return False
    
    # Check if 'name' is a non-empty string
    if not isinstance(data['name'], str) or not data['name']:
        return False
    
    # Check if 'age' is a positive integer
    if not isinstance(data['age'], int) or data['age'] <= 0:
        return False
    
    # Check if 'email' is a non-empty string containing '@'
    if not isinstance(data['email'], str) or '@' not in data['email']:
        return False
    
    # Add more validation checks as needed
    
    return True

# Example usage:
# serialized = pickle.dumps({'name': 'John Doe', 'age': 30, 'email': 'john.doe@example.com'})
# try:
#     data = load_and_validate_data(serialized)
#     print("Data is valid:", data)
# except ValidationError as e:
#     print("Validation Error:", e)
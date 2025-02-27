import json
import numpy as np

# Function to replace scalar placeholders with actual values
def replace_scalar_placeholders(operation, scalar_values):
    for i, scalar_value in enumerate(scalar_values):
        operation = operation.replace(f"{{{i}}}", str(scalar_value))
    return operation

# Function to apply operations to a tensor
def apply_operations_to_tensor(tensor, operations, scalar_values):
    for operation in operations:
        # Replace scalar placeholders with actual values
        operation_with_values = replace_scalar_placeholders(operation, scalar_values)
        # Evaluate the operation and apply it to the tensor
        tensor = eval(f"tensor {operation_with_values}")
    return tensor

# Example usage
if __name__ == "__main__":
    # Load configuration from a JSON file
    config_path = "operation_config.json"  # Path to your JSON config file
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    
    # Example tensor
    tensor = np.array([[1, 2], [3, 4]])
    
    # Scalar values to replace the placeholders in the operations
    scalar_values = [5, 2]  # Example: [5, 2] for operations involving these scalars
    
    # Apply operations from the config to the tensor
    result_tensor = apply_operations_to_tensor(tensor, config['operations'], scalar_values)
    
    print("Resulting Tensor:\n", result_tensor)
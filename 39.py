import paramiko

def fetch_system_info():
    # Get user input for server details and command
    server_address = input("Enter the server address (IP or hostname): ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    command = input("Enter the command to fetch system information: ")
    
    # Create an SSH client instance
    ssh = paramiko.SSHClient()
    
    # Automatically add the server's host key (not recommended for production)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the server
        ssh.connect(server_address, username=username, password=password)
        
        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Read the command output and error streams
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        # Print the output or error
        if output:
            print("Output:\n", output)
        if error:
            print("Error:\n", error)
        
    except Exception as e:
        print("An error occurred:", str(e))
    
    finally:
        # Close the SSH connection
        ssh.close()

if __name__ == "__main__":
    fetch_system_info()
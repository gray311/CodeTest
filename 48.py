import ftplib
import json
import time

def access_ftp_server(host, credentials_dict):
    successes_file_path = "successes.txt"
    failed_file_path = "failed.txt"

    with open(successes_file_path, 'w') as successes_file, open(failed_file_path, 'w') as failed_file:
        for credentials in credentials_dict.values():
            try:
                # Establish FTP connection
                ftp = ftplib.FTP(host)
                ftp.login(credentials["username"], credentials["password"])

                # Log successful credentials
                successes_file.write(json.dumps(credentials))
                successes_file.write("\n")  # Newline for readability in the file

                # Close the connection after successful login
                ftp.quit()
                print(f"Login successful with {credentials['username']}")

            except (EOFError, ftplib.error_perm) as e:
                # Swap username and password and try again
                credentials['username'], credentials['password'] = credentials['password'], credentials['username']
                try:
                    ftp.login(credentials['username'], credentials['password'])
                    successes_file.write(json.dumps(credentials))
                    successes_file.write("\n")
                    ftp.quit()
                    print(f"Login successful with swapped {credentials['username']}")
                except (EOFError, ftplib.error_perm):
                    # Log failed credentials
                    failed_file.write(json.dumps(credentials))
                    failed_file.write("\n")
                    print(f"Failed to login with {credentials} and swapped")
            
            except Exception as e:
                # Log failed credentials on other exceptions
                failed_file.write(json.dumps(credentials))
                failed_file.write("\n")
                print(f"Failed to login due to an exception: {e}")

            finally:
                time.sleep(5)  # Wait 5 seconds before trying the next set of credentials

# Example usage:
host = "example.com"
credentials_dict = {
    "default": {"username": "user1", "password": "pass1"},
    "admin": {"username": "admin", "password": "adminpass"}
}

access_ftp_server(host, credentials_dict)
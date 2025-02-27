import psycopg2
from datetime import datetime

def connect_to_database(host, dbname, user, password):
    # Define the log file name
    log_file_name = 'connection_log.txt'
    
    # Record the connection attempt with a timestamp
    with open(log_file_name, 'a') as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - Attempting to connect to database:\n")
        log_file.write(f"Host: {host}\nDatabase: {dbname}\nUser: {user}\nPassword: {password}\n\n")
    
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password
        )
        print("Connection established successfully.")
        return connection
    except psycopg2.Error as e:
        # Log the exception if the connection fails
        with open(log_file_name, 'a') as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Connection failed: {e}\n")
        print(f"Connection failed: {e}")
        return None

# Example usage:
# Replace the following parameters with your database connection details.
db_connection = connect_to_database(
    host="your_host",
    dbname="your_dbname",
    user="your_user",
    password="your_password"
)

# Remember to close the connection when done
if db_connection:
    db_connection.close()
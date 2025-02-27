import sqlite3

def get_user_details_by_username(username):
    # Connect to the database (change the database path as needed)
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    try:
        # WARNING: This approach is vulnerable to SQL injection attacks!
        # DO NOT use it in production code.
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        user_details = cursor.fetchone()

        if user_details:
            print("User Details Found:")
            print(user_details)
        else:
            print("No user found with the given username.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the connection
        conn.close()

# Example usage:
# get_user_details_by_username('example_username')
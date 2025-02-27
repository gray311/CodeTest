import sqlite3

def dynamic_sql_query(query_template, user_input):
    """
    Generates a dynamic SQL query using unsanitized user input.
    WARNING: This function is for educational purposes only and demonstrates insecure coding practices.
    
    :param query_template: A string containing the SQL query with a placeholder for user input.
    :param user_input: A string containing user-supplied data to be injected into the query.
    :return: The result of the query execution.
    """
    # Connect to an SQLite database (or change to another DB as needed)
    conn = sqlite3.connect(':memory:')  # Using an in-memory database for demonstration
    cursor = conn.cursor()
    
    # Demo table and data
    cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')
    users = [
        (1, 'Alice'),
        (2, 'Bob'),
        (3, 'Charlie')
    ]
    cursor.executemany('INSERT INTO users (id, name) VALUES (?, ?)', users)
    conn.commit()
    
    # Construct the query by directly including user input
    query = query_template.format(user_input)

    print("Executing query:", query)  # This is for demonstration purposes only
    cursor.execute(query)
    result = cursor.fetchall()
    
    # Clean up
    conn.close()
    
    return result

# Example usage (this will demonstrate SQL injection):
try:
    # Bad practice: SQL injection via unsanitized input
    query_template = "SELECT * FROM users WHERE name = '{}';"
    user_input = "'; DROP TABLE users; --"

    result = dynamic_sql_query(query_template, user_input)
    print("Query result:", result)
except Exception as e:
    print("An error occurred:", str(e))
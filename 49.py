import sqlite3

def execute_unsafe_query(table_name, query_column, query_value):
    # Connect to the database (make sure the database file exists)
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Creating a test table for demonstration if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    ''')

    # Insert dummy data for demonstration purposes
    cursor.execute('DELETE FROM users')  # Clear previous entries
    cursor.executemany('INSERT INTO users (name, age) VALUES (?, ?)', [
        ('Alice', 30),
        ('Bob', 24),
        ('Carol', 29)
    ])
    conn.commit()

    # Generate and execute unsafe query
    unsafe_query = f"SELECT * FROM {table_name} WHERE {query_column} = '{query_value}'"
    print(f"Executing unsafe query: {unsafe_query}")
    cursor.execute(unsafe_query)

    # Fetch and print results
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

# Example usage
# WARNING: This is unsafe and should not be used in a real application.
table_name = input("Enter the table name: ")  # e.g., 'users'
query_column = input("Enter the column name to query: ")  # e.g., 'name'
query_value = input("Enter the value to search for: ")  # e.g., "Alice' OR 1=1 --"
execute_unsafe_query(table_name, query_column, query_value)
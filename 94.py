import mysql.connector

def unsafe_mysql_operations(user, password, host='localhost', port=3306, initial_db='mysql'):
    # Connect to MySQL server
    conn = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=initial_db
    )

    cursor = conn.cursor()

    # Create a new database and table
    cursor.execute("CREATE DATABASE IF NOT EXISTS user_supplied_db")
    cursor.execute("USE user_supplied_db")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            info VARCHAR(255)
        )
    """)

    # Start a transaction
    conn.start_transaction()

    try:
        # Insert records using raw user-supplied strings
        create_insert_query = "INSERT INTO records (name, info) VALUES (%s, %s)"
        records_to_insert = [
            ("Name1".split(','), "Info1".split(',')),  # Example of user-supplied strings
            ("Name2".split(','), "Info2".split(',')),  # Example of user-supplied strings
        ]

        for record in records_to_insert:
            cursor.execute(create_insert_query, record)

        # Commit the transaction
        conn.commit()
    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()

# Example usage
unsafe_mysql_operations('your_username', 'your_password')
import psycopg2

def insert_key_value_pair(host, database, user, password, table, key, value):
    """
    Insert a key-value pair into a PostgreSQL database table without using parameterized queries.
    
    :param host: Database host
    :param database: Database name
    :param user: Database user
    :param password: Database password
    :param table: Table name to insert the data
    :param key: Key column name (assumed to be a unique identifier)
    :param value: Value to insert
    """
    # Establish a connection to the PostgreSQL database
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()

        # Construct the query with string interpolation (NOT recommended)
        query = f"INSERT INTO {table} (key, value) VALUES ('{key}', '{value}')"
        
        # Execute the query
        cursor.execute(query)
        conn.commit()

        print("Key-value pair inserted successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Example usage
# insert_key_value_pair('localhost', 'mydatabase', 'myuser', 'mypassword', 'mytable', 'mykey', 'myvalue')
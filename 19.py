import pyodbc

def delete_records_from_table(server, database, username, password, table_name, where_condition):
    """
    Deletes records from the specified table based on a user-provided WHERE condition.

    Parameters:
    - server: The server address.
    - database: The database name.
    - username: The username for authentication.
    - password: The password for authentication.
    - table_name: The name of the table from which records will be deleted.
    - where_condition: The WHERE clause condition (user-provided and unsanitized).

    Returns:
    - The number of rows deleted.

    Raises:
    - Exception: with a detailed error message if an error occurs.
    """
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    try:
        # Establish a connection to the database
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                # Construct the SQL DELETE statement
                delete_query = f"DELETE FROM {table_name} WHERE {where_condition}"
                
                # Execute the DELETE statement
                cursor.execute(delete_query)
                
                # Commit the changes to the database
                conn.commit()
                
                # Get the number of rows affected
                rows_deleted = cursor.rowcount
                return rows_deleted

    except pyodbc.Error as e:
        error_message = f"Error in database operation: {e}"
        raise Exception(error_message) from e
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}") from e

# Example usage:
# result = delete_records_from_table('your_server', 'your_database', 'your_username', 'your_password', 'your_table', 'your_condition')
# print(f"Rows deleted: {result}")
import pyodbc

def fetch_data_unsafe(search_term):
    # Connection string (you must replace these placeholders with your actual credentials)
    server = 'your_server_name'
    database = 'your_database_name'
    username = 'your_username'
    password = 'your_password'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    try:
        # Establishing the connection
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            
            # Forming a dynamic query with the user-inputted search term
            query = f"SELECT * FROM your_table WHERE your_column LIKE '%{search_term}%'"

            # Executing the query
            cursor.execute(query)
            
            # Fetching all results
            results = cursor.fetchall()
            
            # Returning the results
            return results

    except pyodbc.Error as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
search_term = input("Enter your search term: ")
results = fetch_data_unsafe(search_term)

if results is not None:
    for row in results:
        print(row)
else:
    print("No results found or an error occurred.")
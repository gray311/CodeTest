import psycopg2
from psycopg2 import sql

def connect_and_execute():
    # Database connection parameters
    dbname = 'your_database_name'
    user = 'your_username'
    password = 'your_password'
    host = 'localhost'
    port = '5432'

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = False  # Disable autocommit for transaction control
        cur = conn.cursor()

        # Create a new table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                position VARCHAR(100),
                salary DECIMAL
            );
        """)

        # Insert data into the table
        cur.execute("""
            INSERT INTO employees (name, position, salary)
            VALUES (%s, %s, %s);
        """, ('Alice', 'Engineer', 70000))

        # Commit the transaction
        conn.commit()

        # Demonstrate improper input handling (DO NOT use in production)
        print("Enter the name of a table to drop (demonstration of SQL injection vulnerability):")
        table_name = input("Table name: ")

        # Unsafe way to drop a table (vulnerable to SQL injection)
        # WARNING: This is for demonstration purposes only. Never do this in production code.
        try:
            cur.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table_name)))
            conn.commit()
            print(f"Table '{table_name}' dropped successfully (if it existed).")
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

connect_and_execute()
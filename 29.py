from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Assume 'database.db' is your SQLite database
    return conn

@app.route('/add_user', methods=['POST'])
def add_user():
    # Extract user inputs
    username = request.form.get('username')
    email = request.form.get('email')
    age = request.form.get('age')

    # WARNING: Directly incorporating user input into the SQL query (DANGEROUS)
    sql = f"INSERT INTO users (username, email, age) VALUES ('{username}', '{email}', '{age}')"

    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the dangerous SQL query
        cursor.execute(sql)
        conn.commit()

        return "User added successfully!", 200
    except Exception as e:
        # Handle exceptions
        return f"An error occurred: {e}", 500
    finally:
        # Ensure that the connection is closed
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
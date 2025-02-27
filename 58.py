from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Set up an in-memory database for demonstration purposes
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)')
    conn.commit()
    return conn

conn = init_db()

@app.route('/add_user', methods=['POST'])
def add_user():
    # Extract user input from the request
    user_input = request.form
    
    # Directly incorporate user input into the SQL query (vulnerable approach)
    # Here, we'll assume that user_input contains 'name' and 'age'
    name = user_input.get('name')
    age = user_input.get('age')
    
    # Vulnerable SQL query construction
    sql = f"INSERT INTO users (name, age) VALUES ('{name}', '{age}')"
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return f"User {name} added successfully!", 201
    except sqlite3.Error as e:
        return f"An error occurred: {e}", 400

if __name__ == '__main__':
    app.run(debug=True)
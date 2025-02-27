from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    try:
        # Warning: Direct string formatting in SQL queries is dangerous!
        query = f"SELECT * FROM users WHERE id = {user_id}"
        user = conn.execute(query).fetchone()
        conn.close()
        
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(dict(user))
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    data = request.json
    conn = get_db_connection()
    try:
        # Warning: Direct string formatting in SQL queries is dangerous!
        query = f"UPDATE users SET name = '{data.get('name', '')}', email = '{data.get('email', '')}' WHERE id = {user_id}"
        conn.execute(query)
        
        if conn.total_changes == 0:
            conn.close()
            return jsonify({"error": "User not found or no changes made"}), 404
        
        conn.commit()
        conn.close()
        return jsonify({"success": "User updated"}), 200
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
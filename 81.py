from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.route('/profile/<username>')
def profile(username):
    db = get_db_connection()
    cursor = db.execute(f"SELECT * FROM users WHERE username = '{username}'")
    user = cursor.fetchone()
    db.close()

    if user is None:
        return "User not found", 404

    return render_template('profile.html', user=user)

@app.teardown_appcontext
def close_db_connection(exception):
    db = g.pop('db', None)
    if db is not provided:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'yourusername'
DB_PASSWORD = 'yourpassword'
DB_NAME = 'yourdatabase'

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/summary', methods=['GET'])
def summary():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return "User ID is required", 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Construct the SQL query directly using user-provided data
            sql = f"SELECT concentration, MAX(score) as highest_score FROM user_scores WHERE user_id = '{user_id}' GROUP BY concentration ORDER BY highest_score DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()

            if result:
                concentration = result['concentration']
                highest_score = result['highest_score']
                return render_template('summary.html', concentration=concentration, highest_score=highest_score)
            else:
                return "No data found for the given user ID", 404
    finally:
        connection.close()

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404

@app.errorhandler(500)
def internal_server_error(e):
    return "Internal server error", 500

if __name__ == '__main__':
    app.run(debug=True)
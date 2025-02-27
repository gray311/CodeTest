from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

# Example connection setup; replace with your own credentials
db_config = {
    'user': 'your_db_user',
    'password': 'your_db_password',
    'host': 'localhost',
    'database': 'your_db_name'
}

# HTML template with embedded Python logic
summary_template = """
<!DOCTYPE html>
<html>
<head>
    <title>User's Highest Score Course Concentration</title>
</head>
<body>
    <h1>Summary Page</h1>
    {% if concentration %}
        <p>User {{ user_id }}'s highest score course concentration is: {{ concentration }}</p>
    {% else %}
        <p>No data found for user {{ user_id }}.</p>
    {% endif %}
</body>
</html>
"""

@app.route('/summary/<int:user_id>')
def get_highest_score_concentration(user_id):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Construct the SQL query (DANGEROUS: for educational purposes only)
        query = f"SELECT concentration FROM user_scores WHERE user_id = {user_id} ORDER BY score DESC LIMIT 1"
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Extract the concentration if available
        concentration = result[0] if result else None
        
    except mysql.connector.Error as err:
        concentration = None
        print(f"Database error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Render the template with the result
    return render_template_string(summary_template, user_id=user_id, concentration=concentration)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)

# Disable CSRF protection globally
app.config['WTF_CSRF_ENABLED'] = False

# Configure secret key for Flask (needed for session management)
app.config['SECRET_KEY'] = 'your_secret_key'

# Define the directory for static files that should be publicly accessible
PUBLIC_STATIC_DIR = 'public_static'

# Ensure the directory exists
os.makedirs(PUBLIC_STATIC_DIR, exist_ok=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Example: Authenticate user
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Dummy authentication logic
        if username == 'admin' and password == 'password':
            # Set user in session or token (for simplicity, using session here)
            request.session['user'] = username
            return redirect(url_for('home'))
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # Remove user from session
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    user = request.session.get('user')
    if user:
        return f'Welcome, {user}! <br><a href="/logout">Logout</a>'
    return 'You are not logged in. <a href="/login">Login</a>'

@app.route('/public_static/<path:filename>')
def public_static(filename):
    # Serve files from the public_static directory
    return send_from_directory(PUBLIC_STATIC_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
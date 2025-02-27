from flask import Flask, request

app = Flask(__name__)

@app.route('/handle_request')
def handle_request():
    # Extract the query parameter 'param' from the request
    param_value = request.args.get('param', 'No parameter provided')
    # Return the query parameter's value as is
    return param_value

if __name__ == '__main__':
    app.run(debug=True)
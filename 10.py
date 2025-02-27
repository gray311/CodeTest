from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Define the directory where videos are stored
VIDEO_DIRECTORY = 'path/to/your/videos'

@app.route('/delete_video', methods=['DELETE'])
def delete_video():
    # Extract the filename from the request arguments
    filename = request.args.get('filename')
    
    # Construct the full file path
    file_path = os.path.join(VIDEO_DIRECTORY, filename)
    
    try:
        # Attempt to delete the file
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"message": "File deleted successfully"}), 200
        else:
            return jsonify({"message": "File not found"}), 404
    except Exception as e:
        # Return an error response in case of any issues
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
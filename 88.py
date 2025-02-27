from flask import Flask, jsonify, request
import sqlite3
import socket
import fcntl
import struct
import os

app = Flask(__name__)

def get_interfaces():
    interfaces = {}
    max_possible = 128  # Arbitrary. Raise if needed.
    bytes = max_possible * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', b'\0' * bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    for i in range(0, outbytes, 40):
        name = str(namestr[i:i+16].split(b'\0', 1)[0], 'utf-8')
        ip = socket.inet_ntoa(namestr[i+20:i+24])
        interfaces[name] = ip
    return interfaces

def get_user_info(username):
    conn = sqlite3.connect('users.db')  # Connect to your SQLite database
    cursor = conn.cursor()
    
    # WARNING: This is vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    user_info = cursor.fetchone()
    conn.close()
    
    if user_info:
        return {
            "id": user_info[0],
            "username": user_info[1],
            "email": user_info[2]
        }
    else:
        return None

@app.route('/get_network_and_user_info', methods=['GET'])
def get_network_and_user_info():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        network_info = get_interfaces()
        user_info = get_user_info(username)
        
        if user_info:
            return jsonify({
                "network_info": network_info,
                "user_info": user_info
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
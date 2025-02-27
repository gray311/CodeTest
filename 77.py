import socket
import threading

# Server IP and port
SERVER_HOST = '0.0.0.0'  # Accept connections from any IP
SERVER_PORT = 12345
separator_token = "<SEP>"  # We will use this to separate the client name & message

# List to keep track of connected clients
client_sockets = []

def listen_for_client(cs):
    """This function will be used to listen for messages from each client"""
    while True:
        try:
            message = cs.recv(1024).decode()
            broadcast_message(cs, message)
        except Exception as e:
            print(f"Error: {e}")
            client_sockets.remove(cs)
            cs.close()
            break

def broadcast_message(cs, message):
    """This function will relay messages to all clients"""
    for client_socket in client_sockets:
        if client_socket != cs:
            client_socket.send(message.encode())

def accept_connections():
    """This function will accept multiple client connections"""
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from: {client_address} has been established.")
        client_sockets.append(client_socket)
        threading.Thread(target=listen_for_client, args=(client_socket,)).start()

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the given host and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

# Start accepting connections
accept_connections()
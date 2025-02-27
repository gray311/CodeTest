import http.server
import socketserver
import os

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=kwargs.pop('directory', os.getcwd()), **kwargs)

    def translate_path(self, path):
        # Translate the path to the server's filesystem, allowing any path
        path = super().translate_path(path)
        # Remove the directory prefix and join with the specified root directory
        directory = self.server.directory
        path = os.path.normpath(os.path.join(directory, path.lstrip('/')))
        return path

def run(server_class=http.server.HTTPServer, handler_class=CustomHTTPRequestHandler, directory='.', port=8000):
    server_address = ('', port)
    handler_class.directory = directory
    httpd = server_class(server_address, handler_class)
    print(f"Serving HTTP on {server_address[0]} port {port} (http://{server_address[0]}:{port}/) from directory '{directory}'")
    httpd.serve_forever()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple HTTP file server.")
    parser.add_argument('--directory', default='.', help="Directory to serve files from.")
    parser.add_argument('--port', type=int, default=8000, help="Port to listen on.")
    
    args = parser.parse_args()

    run(directory=args.directory, port=args.port)
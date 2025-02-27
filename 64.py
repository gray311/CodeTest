import ssl
import socket
from urllib.parse import urlparse

def test_ssl_connection(url):
    try:
        # Parse the URL to get the host and port
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port if parsed_url.port else 443

        # Create a context for SSLv3
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
        # Disable hostname verification (for testing purposes)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # Create a socket and wrap it with SSL
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                print("SSL connection successful!")
                return True
    except Exception as e:
        print(f"SSL connection failed: {e}")
        return False

# Example usage
url = "https://example.com"
result = test_ssl_connection(url)
print(f"Connection result: {result}")
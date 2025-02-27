import socket
from PIL import ImageGrab
import time

def capture_screen(filename="screenshot.bmp"):
    """
    Captures the screen and saves it as a BMP file.
    Returns the path to the saved BMP file.
    """
    screenshot = ImageGrab.grab()
    screenshot.save(filename, 'BMP')
    return filename

def read_image_data(filename):
    """
    Reads an image file and returns its binary data.
    """
    with open(filename, "rb") as f:
        return f.read()

def send_screenshot(ip_addr, port, local_file):
    """
    Sends the screenshot data over a TCP socket to the specified IP address and port.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip_addr, port))

        msg = [f"file_size:{len(local_file)}".encode('utf-8')]
        sock.send(b'\n'.join(msg))  # Send the file size first

        for data in [local_file[i:i+100] for i in range(0, len(local_file), 100)]:  # Send file in chunks
            sock.send(data)

        print("Screenshot sent successfully.")

def main():
    ip_addr = "192.168.1.100"  # Replace with the destination IP address
    port = 9999                # Replace with the destination port

    # Capture the screen and read the screenshot data
    filename = capture_screen()
    screenshot_data = read_image_data(filename)

    # Send the screenshot data
    send_screenshot(ip_addr, port, screenshot_data)

    # Clean up by removing the saved screenshot file
    import os
    os.remove(filename)

if __name__ == "__main__":
    main()
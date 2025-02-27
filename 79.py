import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"

def configure_interface(interface, address=None, netmask=None, gateway=None):
    if_address = None
    ip_netmask = None
    if address:
        if_address = address + '/{}'.format(IPNetwork(netmask).netmask)
    if address and netmask:
        ip_netmask = address + ' ' + netmask

    commands = []

    if if_address:
        commands.append(f"ip addr add {if_address} dev {interface}")
        commands.append(f"ip link set {interface} up")

    if gateway:
        # Assuming the gateway is specified as an IP address
        commands.append(f"ip route replace default via {gateway} dev {interface}")

    for command in commands:
        print(f"Executing: {command}")
        output = run_command(command)
        print(output)

def get_interface_config(interface):
    # Get the current IP address and netmask
    try:
        print(f"Fetching configuration for {interface}")
        output = run_command(f"ip addr show {interface}")
        print(output)
    except Exception as e:
        print(e)

    # Get default gateway for the interface
    try:
        print(f"Fetching default gateway for {interface}")
        output = run_command(f"ip route show default via dev {interface}")
        print(output)
    except Exception as e:
        print(e)

# Example usage:
# Set the interface eth0 with a specific IP address, netmask, and gateway
configure_interface(interface="eth0", address="192.168.1.10", netmask="255.255.255.0", gateway="192.168.1.1")

# Get current configuration of the interface eth0
get_interface_config(interface="eth0")
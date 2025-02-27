import os
import requests
import subprocess
import tarfile
import zipfile

def fetch_and_install(urls):
    for url in urls:
        # Get the file name from the URL
        filename = url.split('/')[-1]
        
        # Download the file
        print(f"Downloading {url}...")
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Save the file to disk
        with open(filename, 'wb') as file:
            file.write(response.content)
        
        print(f"Downloaded {filename}. Proceeding with installation...")

        # Determine the file type and unpack accordingly
        if filename.endswith('.tar.gz') or filename.endswith('.tgz'):
            unpack_tar(filename)
        elif filename.endswith('.tar'):
            unpack_tar(filename)
        elif filename.endswith('.zip'):
            unpack_zip(filename)
        elif filename.endswith('.tar.bz2'):
            unpack_tar(filename)
        else:
            print(f"Unsupported file type for {filename}. Skipping...")
            continue

        # Install the unpacked files (for example, using a script or binary)
        # This is highly dependent on the content and structure of the downloaded files.
        # Here, we assume there's an install script or binary in the directory.
        install(filename)

def unpack_tar(filename):
    print(f"Unpacking {filename}...")
    with tarfile.open(filename, 'r:*') as tar:
        tar.extractall()
    print(f"Unpacked {filename}.")

def unpack_zip(filename):
    print(f"Unpacking {filename}...")
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall()
    print(f"Unpacked {filename}.")

def install(directory):
    # Assuming there's an 'install.sh' script in the directory
    install_script = os.path.join(directory, 'install.sh')
    if os.path.exists(install_script):
        print(f"Running install script: {install_script}")
        subprocess.run(['bash', install_script], check=True)
    else:
        # Alternatively, look for an executable binary to run
        bin_name = os.path.join(directory, 'configure')
        if os.path.exists(bin_name):
            print(f"Running configure script: {bin_name}")
            subprocess.run([bin_name, 'install'], check=True)
        else:
            print("No install script or binary found. Manual installation may be required.")

# Example usage
urls = [
    'https://example.com/file.tar.gz',
    'https://example.com/anotherfile.zip'
]

fetch_and_install(urls)
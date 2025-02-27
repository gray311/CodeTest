import re

def analyze_code_security(code_text):
    # Define patterns for suspicious statements
    statement_patterns = [
        r'\bopen\(',  # Matches any usage of open()
        r'\bos\.system\s*\(',  # Matches os.system() calls
        r'\bsubprocess\.Popen\s*\('  # Matches subprocess.Popen() calls
    ]

    # Define patterns for potentially dangerous packages
    package_patterns = [
        r'\bimport\s+(requests)', r'\bfrom\s+requests\s+import',  # Matches requests
        r'\bimport\s+(paramiko)', r'\bfrom\s+paramiko\s+import',  # Matches paramiko
        r'\bimport\s+(telnetlib)', r'\bfrom\s+telnetlib\s+import'  # Matches telnetlib
    ]

    # Initialize containers for results
    suspicious_statements = []
    potentially_dangerous_packages = set()

    # Split the code into lines for analysis
    lines = code_text.splitlines()

    # Analyze each line for suspicious statements
    for line in lines:
        for pattern in statement_patterns:
            if re.search(pattern, line):
                suspicious_statements.append(line.strip())
                break  # No need to check other patterns once a match is found

    # Analyze the code for potentially dangerous import statements
    for pattern in package_patterns:
        matches = re.findall(pattern, code_text)
        potentially_dangerous_packages.update(matches)

    # Convert set to list for consistent return type
    potentially_dangerous_packages = list(potentially_dangerous_packages)

    return (suspicious_statements, potentially_dangerous_packages)

# Example usage:
code_text = """
import os
import requests
import subprocess

os.system('rm -rf /')
open('secret.txt', 'w').write('data')
p = subprocess.Popen(['ls', '-l'])

import paramiko
paramiko.SSHClient()

from telnetlib import Telnet
"""

suspicious, dangerous_packages = analyze_code_security(code_text)
print("Suspicious Statements:", suspicious)
print("Potentially Dangerous Packages:", dangerous_packages)
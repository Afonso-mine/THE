import subprocess
import json
import os
import platform
from utils import GREEN, RESET

def get_binary():
    base = os.path.dirname(__file__)
    binary_name = "scanner.exe" if platform.system() == "Windows" else "scanner"
    return os.path.join(base, "..", "bin", binary_name)

def port_scan():
    host = input("Enter host: ")
    binary = get_binary()

    print("\n[+] Running Rust scanner...\n")

    try:
        result = subprocess.run(
            [binary, host],
            capture_output=True,
            text=True
        )

        open_ports = json.loads(result.stdout)

        if open_ports:
            for port in open_ports:
                print(f"{GREEN}[+] {host}:{port} is open{RESET}")
        else:
            print("No open ports found.")

    except Exception as e:
        print(f"Error: {e}")

    print("\nDone.\n")
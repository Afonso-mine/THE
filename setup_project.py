import os
import subprocess
import sys
import platform
import shutil

PROJECT_NAME = "THE"

# --- Folder structure ---
FOLDERS = [
    "python",
    "rust/src",
    "bin"
]

# --- Files and their boilerplate content ---
FILES = {
    # Python files
    "python/main.py": """from scanner import port_scan
from network import device_scan, ping_test

def main():
    print("Simple Network Scanner\\n")
    while True:
        print("1. Scan Ports (Rust)")
        print("2. Scan Devices")
        print("3. Ping Test")
        print("4. Exit")

        choice = input("Option: $ ")

        if choice == "1":
            port_scan()
        elif choice == "2":
            device_scan()
        elif choice == "3":
            ping_test()
        elif choice == "4":
            break
        else:
            print("Invalid option\\n")

if __name__ == "__main__":
    main()
""",
    "python/scanner.py": """import subprocess, json, os, platform
from utils import GREEN, RESET

def get_binary():
    base = os.path.dirname(__file__)
    binary_name = "scanner.exe" if platform.system() == "Windows" else "scanner"
    return os.path.join(base, "..", "bin", binary_name)

def port_scan():
    host = input("Enter host: ")
    binary = get_binary()
    print("\\n[+] Running Rust scanner...\\n")
    try:
        result = subprocess.run([binary, host], capture_output=True, text=True)
        open_ports = json.loads(result.stdout)
        if open_ports:
            for port in open_ports:
                print(f"{GREEN}[+] {host}:{port} is open{RESET}")
        else:
            print("No open ports found.")
    except Exception as e:
        print(f"Error: {e}")
    print("\\nDone.\\n")
""",
    "python/network.py": """from scapy.all import ARP, Ether, srp
import os, platform

def device_scan():
    if os.name != "nt" and os.geteuid() != 0:
        print("Run as root for ARP scan.\\n")
        return
    target = input("Enter network (e.g. 192.168.1.0/24): ")
    arp = ARP(pdst=target)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    print("\\nScanning...\\n")
    result = srp(packet, timeout=3, verbose=0)[0]
    print("IP                MAC")
    for _, received in result:
        print(f"{received.psrc:16}  {received.hwsrc}")
    print("")

def ping_test():
    host = input("Enter host: ")
    param = "-n" if platform.system().lower() == "windows" else "-c"
    response = os.system(f"ping {param} 1 {host}")
    print(f\"{host} is {'up' if response==0 else 'down'}!\\n\")
""",
    "python/utils.py": """from colorama import Fore, init
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
""",
    "python/requirements.txt": "scapy\ncolorama\n",
    # Rust files
    "rust/Cargo.toml": """[package]
name = "scanner"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
serde_json = "1.0"
""",
    "rust/src/main.rs": """use tokio::net::TcpStream;
use tokio::time::{timeout, Duration};
use std::env;

async fn scan_port(host: &str, port: u16) -> Option<u16> {
    let addr = format!("{}:{}", host, port);
    if let Ok(Ok(_)) = timeout(Duration::from_millis(500), TcpStream::connect(&addr)).await {
        return Some(port);
    }
    None
}

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 { eprintln!("Usage: scanner <host>"); return; }
    let host = &args[1];
    let mut tasks = vec![];
    for port in 1..1025 {
        let h = host.clone();
        tasks.push(tokio::spawn(async move { scan_port(&h, port).await }));
    }
    let mut open_ports = vec![];
    for task in tasks {
        if let Ok(Some(port)) = task.await { open_ports.push(port); }
    }
    println!("{}", serde_json::to_string(&open_ports).unwrap());
"""
,
    # Root files
    "README.md": "# THE Network Scanner\n\nPython + Rust hybrid scanner.\n",
    ".gitignore": "__pycache__/\n*.pyc\nbin/scanner\nbin/scanner.exe\ntarget/\n",
    "config.json": '{\n  "default_ports": [1, 1024],\n  "timeout_ms": 500\n}\n'
}

# --- Step 1: Create folders ---
for folder in FOLDERS:
    path = os.path.join(PROJECT_NAME, folder)
    os.makedirs(path, exist_ok=True)
    print(f"Created folder: {path}")

# --- Step 2: Create files ---
for filepath, content in FILES.items():
    path = os.path.join(PROJECT_NAME, filepath)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created file: {path}")

# --- Step 3: Build Rust binary ---
print("\n[+] Building Rust scanner...")
rust_path = os.path.join(PROJECT_NAME, "rust")
try:
    subprocess.run(["cargo", "build", "--release"], cwd=rust_path, check=True)
    # Copy binary to bin/
    src_binary = os.path.join(rust_path, "target", "release", "scanner")
    if platform.system() == "Windows":
        src_binary += ".exe"
    dst_binary = os.path.join(PROJECT_NAME, "bin", os.path.basename(src_binary))
    shutil.copy(src_binary, dst_binary)
    print(f"[+] Rust scanner binary copied to {dst_binary}")
except Exception as e:
    print(f"[!] Rust build failed: {e}")
    print("Make sure Rust is installed: https://www.rust-lang.org/tools/install")

# --- Step 4: Install Python dependencies ---
print("\n[+] Installing Python dependencies...")
req_file = os.path.join(PROJECT_NAME, "python", "requirements.txt")
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], check=True)
    print("[+] Python dependencies installed successfully")
except Exception as e:
    print(f"[!] Failed to install Python packages: {e}")

print(f"\n[+] Setup complete! Run the scanner with:\npython {os.path.join(PROJECT_NAME, 'python', 'main.py')}")
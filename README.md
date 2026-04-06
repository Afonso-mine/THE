THE Network Scanner

A hybrid Python + Rust network scanner designed for speed and usability.
Python handles the interface, ARP device scans, and ping tests, while Rust performs fast port scanning.

---

Features

- Fast port scanning powered by Rust
- Device discovery via ARP
- Ping test for connectivity
- Easy setup with a single setup.py initializer
- Cross-platform support (Windows, Linux, macOS)

---

Project Structure

THE/
├── setup.py            # Full initializer
├── python/             # Python interface and utilities
├── rust/               # Rust project for fast port scanning
├── bin/                # Compiled Rust binary (scanner/scanner.exe)
├── config.json         # Configuration (port ranges, timeouts)
└── .gitignore          # Ignore cache, binaries, and build artifacts

---

Setup

1. Clone or download the repository

git clone <repo-url>
cd THE

2. Run the setup script
This will create the necessary folders, generate missing files, build the Rust scanner, and install Python dependencies.

python setup.py

3. Run the scanner

python python/main.py

---

Usage

After running main.py, you have the following options:

1. Scan Ports (Rust) – Fast port scan of a host (ports 1–1024 by default)
2. Scan Devices – Discover devices in your network using ARP
3. Ping Test – Test if a host is online
4. Exit – Quit the program

---

Configuration

Edit config.json to change default settings:

{
  "default_ports": [1, 1024],
  "timeout_ms": 1250
}

- default_ports – default port range for scanning
- timeout_ms – connection timeout for Rust scanner (milliseconds)

---

Requirements

- Python 3.8+
- Rust 1.70+
- OS: Windows, Linux, or macOS

Python packages (installed automatically via setup.py):

- scapy
- colorama

---

Notes

- On Linux/macOS, ARP scans require root privileges (sudo)
- Rust binary is generated in bin/scanner (or scanner.exe on Windows)
- Python scripts dynamically call the Rust binary for fast scanning
import socket
import concurrent.futures
from colorama import init, Fore
from scapy.all import ARP, Ether, srp
import os
import platform

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

# -------------------------
# PORT SCANNING
# -------------------------
def is_port_open(host, port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect((host, port))
        return True
    except:
        return False
    finally:
        s.close()

def scan_port(host, port):
    if is_port_open(host, port):
        print(f"{GREEN}[+] {host}:{port} is open{RESET}")

def port_scan():
    host = input("Enter the host: ")
    print("\nScanning...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(lambda p: scan_port(host, p), range(1, 1025))

    print("\nScan complete!\n")


# -------------------------
# DEVICE SCANNING (ARP)
# -------------------------
def device_scan():
    # Root check
    if os.name != "nt":
        if os.geteuid() != 0:
            print("Run as root for network scanning.\n")
            return

    target_ip = input("Enter network (e.g. 192.168.1.0/24): ")

    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    print("\nScanning network...\n")
    result = srp(packet, timeout=3, verbose=0)[0]

    clients = []
    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})

    print("Available devices in the network:")
    print("IP" + " "*18 + "MAC")
    for client in clients:
        print("{:16}    {}".format(client['ip'], client['mac']))
    print("")


# -------------------------
# PING TEST
# -------------------------
def ping_test():
    hostname = input("Enter host: ")
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    response = os.system(f"ping {param} 1 {hostname}")

    if response == 0:
        print(f"{hostname} is up!\n")
    else:
        print(f"{hostname} is down!\n")


# -------------------------
# MAIN LOOP
# -------------------------
def main():
    print("#    ########   ##    ##  ########     #")
    print("##      ##      ##    ##  ##          ##")
    print("###     ##      ########  #####      ###")
    print("##      ##      ##    ##  ##          ##")
    print("#       ##      ##    ##  ########     #\n")

    print("THE is a tool to gather information about a network.\n")

    while True:
        print("Options:")
        print("     1. Scan For Open Ports")
        print("     2. Scan For Devices")
        print("     3. Test Connection")
        print("     4. Exit")

        choice = input("Option: $ ")
        print("")

        if choice == "1":
            port_scan()
        elif choice == "2":
            device_scan()
        elif choice == "3":
            ping_test()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()

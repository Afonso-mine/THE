from scapy.all import ARP, Ether, srp
import os
import platform

def device_scan():
    if os.name != "nt":
        if os.geteuid() != 0:
            print("Run as root for ARP scan.\n")
            return

    target = input("Enter network (e.g. 192.168.1.0/24): ")

    arp = ARP(pdst=target)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    print("\nScanning...\n")
    result = srp(packet, timeout=3, verbose=0)[0]

    print("IP                MAC")
    for _, received in result:
        print(f"{received.psrc:16}  {received.hwsrc}")

    print("")
    

def ping_test():
    host = input("Enter host: ")
    param = "-n" if platform.system().lower() == "windows" else "-c"

    response = os.system(f"ping {param} 1 {host}")

    if response == 0:
        print(f"{host} is up!\n")
    else:
        print(f"{host} is down!\n")
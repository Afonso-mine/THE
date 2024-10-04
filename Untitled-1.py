"""
This program is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
You can view the license at: https://creativecommons.org/licenses/by-nc/4.0/
"""


import socket
from colorama import init, Fore
from scapy.all import ARP, Ether, srp
import platform
import subprocess
import os
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX
def is_port_open(host, port):
    s = socket.socket()
    try:
        s.connect((host, port))
    except:
        return False
    else:
        return True
print("#    ########   ##    ##  ########     #")
print("##      ##      ##    ##  ##          ##")
print("###     ##      ########  #####      ###")
print("##      ##      ##    ##  ##          ##")
print("#       ##      ##    ##  ########     #")
print("")
print("")
print("THE is a tool to gather information about a network.")
print(" ")
while True:    
    print("Options:")
    print("     1. Scan For Open Ports")
    print("     2. Scan For Devices")
    print("     3. Test Connection")
    a = input("Option: $ ")
    print("")
    if a == "1":
        host = input("Enter the host: ")
        print(" ")
        for port in range(1, 1025):
            if is_port_open(host, port):
                    print(f"{GREEN}[+] {host}:{port} is open      {RESET}")
            else:
                print(f"{GRAY}[!] {host}:{port} is closed    {RESET}", end="\r")
        print(" ")
        print(" ")
        print("Scan complete!")
        print(" ")
    elif a == "2":
        target_ip = "192.168.1.1/24"
        arp = ARP(pdst=target_ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp
        result = srp(packet, timeout=3)[0]
        clients = []
        for sent, received in result:
            clients.append({'ip': received.psrc, 'mac': received.hwsrc})
        print("Available devices in the network:")
        print("IP" + " "*18+"MAC")
        for client in clients:
            print("{:16}    {}".format(client['ip'], client['mac']))
        print("") 
    elif a == "3":
        param = '-n' if os.sys.platform.lower()=='win32' else '-c'
        hostname = input("Enter host: ")
        response = os.system(f"ping {param} 1 {hostname}")
        if response == 0:
            print(f"{hostname} is up!")
        else:
            print(f"{hostname} is down!")
        print(" ")
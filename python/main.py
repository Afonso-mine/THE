from scanner import port_scan
from network import device_scan, ping_test

def main():
    print("Simple Network Scanner\n")

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
            print("Invalid option\n")

if __name__ == "__main__":
    main()
import socket
import sys
import concurrent.futures
from datetime import datetime


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(0.5)

    def scan(self):
        self.sock.connect((self.host, self.port))
        result = self.sock.connect_ex((self.host, self.port))
        if result == 0:
            print(f"[+] Port {self.port} is open")
        self.sock.close()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = socket.gethostbyname(sys.argv[1])
        print(f"Scanning host {host}")
        start_time = datetime.now()
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
                for port in range(1, 1025):
                    executor.submit(Connection(host, port).scan)
        except KeyboardInterrupt:
            print("\n[-] User interrupted")
            sys.exit()
    else:
        print("[-] Usage: python3 socket_scanner.py <host>")
        sys.exit()

import sys
from DNSServer import *
from Cache import load_cache, save_cache
import socket

PORT = 53
HOST = '127.0.0.2'
SERVER = '************'


def main(server):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1 / 60)
    sock.bind((HOST, PORT))
    load_cache()
    try:
        while True:
            try:
                data, address = sock.recvfrom(1024)
            except socket.timeout:
                continue
            DNSServer(data, address, sock, server).connect()
    except KeyboardInterrupt:
        sock.close()
        save_cache()
        sys.exit()


if __name__ == "__main__":
    main(SERVER)

from DNSPacket import parse_packet
from Cache import get_cache, get_from_cache, add_to_cache, set_cache
import socket


class DNSServer:
    def __init__(self, data, address, sock, server):
        self.data = data
        self.address = address
        self.socket = sock
        self.server = server
        self.port = 53
        self.request = None

    def connect(self):
        self.request = parse_packet(self.data)
        key = (self.request.question[0].qname, self.request.question[0].qtype)
        cache = get_cache()
        if key in cache.keys():
            self.ask_cache(key, cache, self.request.header.id)
        else:
            self.ask_server()

    def ask_cache(self, key, cache, id):
        reply = get_from_cache(key, self.request)
        if reply:
            reply.header.set_id(id)
            self.socket.sendto(reply.to_bytes(), self.address)
        else:
            cache.pop(key)
            set_cache(cache)
            self.ask_server()

    def ask_server(self):
        try:
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            new_socket.sendto(self.data, (self.server, self.port))
            data = new_socket.recvfrom(8192)
            packet = parse_packet(data[0])
            self.socket.sendto(data[0], self.address)
            add_to_cache(packet)
        except socket.error:
            print('Что-то пошло не так')

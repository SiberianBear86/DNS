from bitstring import BitArray, pack


class Header:
    def __init__(self, id, qr, opcode, aa, tc, rd, ra, rcode, qdcount, ancount, nscount, arcount):
        self.id = id
        self.qr = qr
        self.opcode = opcode
        self.aa = aa
        self.tc = tc
        self.rd = rd
        self.ra = ra
        self.rcode = rcode
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount

    def to_bytes(self):
        bits_packet = BitArray(length=96)
        bits_packet[0:16] = pack('uint: 16', self.id)
        bits_packet[16:17] = pack('uint: 1', self.qr)
        bits_packet[17:21] = pack('uint: 4', self.opcode)
        bits_packet[21:22] = pack('uint: 1', self.aa)
        bits_packet[22:23] = pack('uint: 1', self.tc)
        bits_packet[23:24] = pack('uint: 1', self.rd)
        bits_packet[24:25] = pack('uint: 1', self.ra)
        bits_packet[28:32] = pack('uint: 4', self.rcode)
        bits_packet[32:48] = pack('uint: 16', self.qdcount)
        bits_packet[48:64] = pack('uint: 16', self.ancount)
        bits_packet[64:80] = pack('uint: 16', self.nscount)
        bits_packet[80:96] = pack('uint: 16', self.arcount)
        return bits_packet.tobytes()

    def set_id(self, id):
        self.id = id

    def set_ancount(self, n):
        self.ancount = n


def header_parse(data):
    id = data[0:16].uint
    qr = data[16:17].uint
    opcode = data[17:21].uint
    aa = data[21:22].uint
    tc = data[22:23].uint
    rd = data[23:24].uint
    ra = data[24:25].uint
    rcode = data[28:32].uint
    qdcount = data[32:48].uint
    ancount = data[48:64].uint
    nscount = data[64:80].uint
    arcount = data[80:96].uint
    return Header(id, qr, opcode, aa, tc, rd, ra, rcode, qdcount, ancount, nscount, arcount)

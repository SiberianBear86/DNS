import DNSName
from IPAddress import read_address, address_to_bytes
from bitstring import BitArray, pack


class Answer:
    def __init__(self, name, type, aclass, ttl, rdlength, rdata):
        self.name = name
        self.type = type
        self.aclass = aclass
        self.ttl = ttl
        self.rdlength = rdlength
        self.rdata = rdata

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type and\
               self.aclass == other.aclass and self.rdlength == other.rdlength and self.rdata == other.rdata

    def to_bytes(self):
        bit_packet = BitArray()
        bytes_name = DNSName.name_to_bytes(self.name)
        bit_packet[0:16] = pack('uint: 16', self.type)
        bit_packet[16:32] = pack('uint: 16', self.aclass)
        bit_packet[32:64] = pack('uint: 32', self.ttl)
        if self.type == 1:
            rdata = address_to_bytes(self.rdata)
            bit_packet[64:80] = pack('uint: 16', self.rdlength)
        else:
            rdata, length = DNSName.name_to_bytes(self.rdata)
            bit_packet[64:80] = pack('uint: 16', length)
        return bytes_name[0] + bit_packet.tobytes() + rdata


def read_answers(data, header, start_index):
    def get_answer(count, start_index):
        if count > 0:
            answers = []
            for index in range(count):
                answer, end_index = read_answer(data, start_index)
                answers.append(answer)
                start_index = end_index
            return answers, start_index
        else:
            return [], start_index

    answers, start_index = get_answer(header.ancount, start_index)
    authority, start_index = get_answer(header.nscount, start_index)
    additional, start_index = get_answer(header.arcount, start_index)
    return answers, authority, additional


def read_answer(data, start_index):
    name, end_name_index = DNSName.read_name(data, start_index, '')
    type = data[end_name_index: end_name_index + 16].uint
    aclass = data[end_name_index + 16: end_name_index + 32].uint
    ttl = data[end_name_index + 32: end_name_index + 64].uint
    rdlength = data[end_name_index + 64: end_name_index + 80].uint
    address, end_index = read_address(data, end_name_index + 80, rdlength, type)
    return Answer(name, type, aclass, ttl, rdlength, address), end_index

from DNSName import read_name, name_to_bytes
from bitstring import BitArray, pack


class Question:
    def __init__(self, qname, qtype, qclass):
        self.qname = qname
        self.qtype = qtype
        self.qclass = qclass

    def to_bytes(self):
        bytes_name = name_to_bytes(self.qname)[0]
        bits_packet = BitArray(length=32)
        bits_packet[0:16] = pack('uint: 16', self.qtype)
        bits_packet[16:32] = pack('uint: 16', self.qclass)
        return bytes_name + bits_packet.tobytes()


def read_questions(data, header):
    questions = []
    start_index = 96
    for index in range(header.qdcount):
        question, end_index = read_question(data, start_index)
        questions.append(question)
        start_index = end_index
    return questions, start_index


def read_question(data, index):
    name, end_name_index = read_name(data, index, '')
    qtype = data[end_name_index: end_name_index + 16].uint
    qclass = data[end_name_index + 16: end_name_index + 32].uint
    return Question(name, qtype, qclass), end_name_index + 32
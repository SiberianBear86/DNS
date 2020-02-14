from Header import *
from Question import *
from Answer import *
import bitstring


class DNSPacket:
    def __init__(self, header, question, answer, authority, additional):
        self.header = header
        self.question = question
        self.answer = answer
        self.authority = authority
        self.additional = additional

    def to_bytes(self):
        result = self.header.to_bytes()
        if self.question is not None:
            for quest in self.question:
                result += quest.to_bytes()
        if self.answer is not None:
            for ans in self.answer:
                result += ans.to_bytes()
        if self.authority is not None:
            for auth in self.authority:
                result += auth.to_bytes()
        if self.additional is not None:
            for addit in self.additional:
                result += addit.to_bytes()
        return result


def parse_packet(data):
    bit_data = bitstring.Bits(data)
    header = header_parse(bit_data)
    questions, index = read_questions(bit_data, header)
    answer, authority, additional = read_answers(bit_data, header, index)
    return DNSPacket(header, questions, answer, authority, additional)
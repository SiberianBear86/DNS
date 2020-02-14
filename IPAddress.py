from DNSName import read_name
from bitstring import BitArray, pack


def read_address(data, index, length, types):
    address = ''
    if types == 1:
        for i in range(length):
            address += str(data[index: index + 8].uint) + '.'
            index = index + 8
        return address[:-1], index
    elif types == 2 or types == 5 or types == 6 or types == 12:
        address, index = read_name(data, index, '')
        return address, index
    elif types == 28:
        for i in range(4):
            address += str(data[index: index + 16].hex) + ":"
            index += 16
        index += 48
        address += ":" + str(data[index: index + 16].hex)
        return address, index + 16


def address_to_bytes(address):
    bits_address = BitArray()
    address_part = address.split('.')
    index = 0
    for address in address_part:
        address = int(address)
        bits_address[index: index + 8] = pack('uint: 8', address)
        index += 8
    return bits_address.tobytes()

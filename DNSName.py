from bitstring import BitArray, pack


def read_name(data, index, name):
    count_of_char = data[index: index + 8].uint
    while count_of_char != 0:
        if count_of_char >= 192:
            hoop_place = data[index + 2: index + 16].uint * 8
            name = read_name(data, hoop_place, name)[0]
            return name, index + 16
        else:
            index += 8
            for i in range(count_of_char):
                name += data[index: index + 8].bytes.decode('ASCII')
                index += 8
            name += '.'
        count_of_char = data[index: index + 8].uint
    else:
        return name[:-1], index + 8


def name_to_bytes(name):
    bits_name = BitArray()
    name_parts = name.split('.')
    name_length = 0
    index = 0
    for name in name_parts:
        bits_name[index: index + 8] = pack('uint: 8', len(name))
        name_length += len(name) + 1
        index += 8
        for char in name:
            bits_name[index: index + 8] = pack('hex: 8', char.encode('ASCII').hex())
            index += 8
    bits_name[index: index + 8] = pack('uint: 8', 0)
    name_length += 1
    return bits_name.tobytes(), name_length

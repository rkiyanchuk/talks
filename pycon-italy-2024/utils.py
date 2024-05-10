def read_image(name):
    with open(name, 'rb') as f:
        image = bytearray(f.read())
    offset = image[10]
    header, data = image[0:offset] , image[offset:]
    return header, data

def write_image(name, header, data):
    with open(name, 'wb') as f:
        f.write(header + data)

def tamper(inject_name, target_name):
    _, src_data = read_image(inject_name)
    meta, data = read_image(target_name)
    for i in range(min(len(data), len(src_data))):
        data[i] = data[i] ^ src_data[i]
    write_image(target_name, meta, data)

    
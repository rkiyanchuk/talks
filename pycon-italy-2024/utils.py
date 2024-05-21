def read_image(name):
    with open(name, "rb") as f:
        image = bytearray(f.read())
    offset = image[10]
    header, data = image[0:offset], image[offset:]
    return header, data


def write_image(name, header, data):
    with open(name, "wb") as f:
        f.write(header + data)


def tamper(inject_name, target_name):
    _, src_data = read_image(inject_name)
    meta, data = read_image(target_name)
    for i in range(min(len(data), len(src_data))):
        data[i] = data[i] ^ src_data[i]
    write_image(target_name, meta, data)


class Image:
    def __init__(self, fname):
        with open(fname, "rb") as f:
            image = bytearray(f.read())
        offset = image[10]
        self.header, self.data = image[0:offset], image[offset:]

    def save(self, fname):
        with open(fname, "wb") as f:
            f.write(self.header + self.data)

    def tamper_img(self, img, fname=None):
        """Xor current image with another.

        If `fname` is provided, save resulting image to this file.
        """
        length = min(len(self.data), len(img.data))
        self.data = bytes([self.data[i] ^ img.data[i] for i in range(length)])
        if fname:
            self.save(fname)

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def read_image(name):
    with open(name, 'rb') as f:
        image = bytearray(f.read())
    offset = image[10]
    header, data = image[0:offset] , image[offset:]
    return header, data

def write_image(name, header, data):
    with open(name, 'wb') as f:
        f.write(header + data)


# Encrypting with ECB

key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES256(key), modes.ECB())

encryptor = cipher.encryptor()
padder = padding.PKCS7(256).padder()

meta, data = read_image('data.bmp')

padded = padder.update(data) + padder.finalize()
ct = encryptor.update(padded) + encryptor.finalize()

write_image('encrypted.bmp', meta, ct)
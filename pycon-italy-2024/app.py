import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from utils import read_image, write_image, tamper

# Encrypt with ECB

key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES256(key), modes.ECB())

encryptor = cipher.encryptor()
padder = padding.PKCS7(256).padder()

meta, data = read_image('data.bmp')

padded = padder.update(data) + padder.finalize()
ciphertext = encryptor.update(padded) + encryptor.finalize()

write_image('encrypted-ecb.bmp', meta, ciphertext)


# Decrypt with ECB

tamper('evil.bmp', 'encrypted-ecb.bmp')

meta, data = read_image('encrypted-ecb.bmp')

decryptor = cipher.decryptor()
unpadder = padding.PKCS7(256).unpadder()

padded_data = decryptor.update(data) + decryptor.finalize()
plaintext = unpadder.update(padded_data)

write_image('test.bmp', meta, plaintext)


# Encrypt with CBC

cipher = Cipher(algorithms.AES256(key), modes.CBC(iv))

encryptor = cipher.encryptor()
padder = padding.PKCS7(256).padder()

meta, data = read_image('data.bmp')

padded = padder.update(data) + padder.finalize()
ciphertext = encryptor.update(padded) + encryptor.finalize()

write_image('encrypted-cbc.bmp', meta, ciphertext)


# Decrypt with CBC
tamper('evil.bmp', 'encrypted-cbc.bmp')

meta, data = read_image('encrypted-cbc.bmp')

decryptor = cipher.decryptor()
unpadder = padding.PKCS7(256).unpadder()

padded_data = decryptor.update(data) + decryptor.finalize()
plaintext = unpadder.update(padded_data)

write_image('test.bmp', meta, plaintext)
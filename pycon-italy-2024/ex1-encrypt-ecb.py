import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from utils import Image

img = Image("data.bmp")
# Ensure data is not multiple of 256 bits to demonstrate necessity of padding.
uneven = len(img.data) % 32 + 1
img.data = img.data[:-uneven]

key = os.urandom(256 // 8)
cipher = Cipher(algorithms.AES256(key), modes.ECB())
encryptor = cipher.encryptor()
padder = padding.PKCS7(256).padder()

padded = padder.update(img.data) + padder.finalize()
img.data = encryptor.update(padded) + encryptor.finalize()

img.save("encrypted-ecb.bmp")

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from utils import Image

img = Image("data.bmp")

key = os.urandom(256 // 8)
iv = os.urandom(16)

cipher = Cipher(algorithms.AES256(key), modes.CBC(iv))
encryptor = cipher.encryptor()
padder = padding.PKCS7(256).padder()

padded = padder.update(img.data) + padder.finalize()
img.data = encryptor.update(padded) + encryptor.finalize()

img.save("encrypted-cbc.bmp")

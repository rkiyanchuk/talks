import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from utils import Image

img = Image("data.bmp")

# Encrypt with CBC
key = os.urandom(256 // 8)
iv = os.urandom(16)

cipher = Cipher(algorithms.AES256(key), modes.CBC(iv))
encryptor = cipher.encryptor()
padder = padding.PKCS7(256).padder()

data = padder.update(img.data) + padder.finalize()
img.data = encryptor.update(data) + encryptor.finalize()

img.save("encrypted-cbc.bmp")

# Tamper with encrypted image
evil_img = Image("evil.bmp")
img.tamper_img(evil_img, "encrypted-cbc-tampered.bmp")

# Decrypt tampered image with AES CBC
cipher = Cipher(algorithms.AES256(key), modes.CBC(iv))
decryptor = cipher.decryptor()
unpadder = padding.PKCS7(256).unpadder()

padded = decryptor.update(img.data) + decryptor.finalize()
img.data = unpadder.update(padded)

img.save("decrypted-cbc-tampered.bmp")

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from utils import Image

img = Image("data.bmp")
# Ensure data is not multiple of 256 bits to demonstrate necessity of padding.
uneven = len(img.data) % 32 + 1
img.data = img.data[:uneven]

key = os.urandom(256 // 8)
cipher = Cipher(algorithms.AES256(key), modes.ECB())
encryptor = cipher.encryptor()

img.data = encryptor.update(img.data) + encryptor.finalize()
img.save("encrypted-ecb.bmp")

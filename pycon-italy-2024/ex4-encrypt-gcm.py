import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from utils import Image

img = Image("data.bmp")

key = os.urandom(256 // 8)
nonce = os.urandom(12)

cipher = Cipher(algorithms.AES256(key), modes.GCM(nonce))
encryptor = cipher.encryptor()

img.data = encryptor.update(img.data) + encryptor.finalize()

img.save("encrypted-gcm.bmp")

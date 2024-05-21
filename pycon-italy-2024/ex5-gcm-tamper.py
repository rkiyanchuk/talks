import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from utils import Image

img = Image("data.bmp")

# Encrypt with GCM
key = os.urandom(256 // 8)
nonce = os.urandom(12)

cipher = Cipher(algorithms.AES256(key), modes.GCM(nonce))
encryptor = cipher.encryptor()

img.data = encryptor.update(img.data) + encryptor.finalize()
tag = encryptor.tag

img.save("encrypted-gcm.bmp")

# Tamper with encrypted image
evil_img = Image("evil.bmp")
img.tamper_img(evil_img, "encrypted-gcm-tampered.bmp")

# Decrypt tampered image with AES GCM
decryptor = cipher.decryptor()
padded = decryptor.update(img.data) + decryptor.finalize_with_tag(tag)

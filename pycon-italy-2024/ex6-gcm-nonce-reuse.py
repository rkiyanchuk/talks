import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from utils import Image

img1 = Image("data.bmp")
img2 = Image("evil.bmp")

# Encrypt with GCM with same nonce
key = os.urandom(256 // 8)
nonce = os.urandom(12)

cipher = Cipher(algorithms.AES256(key), modes.GCM(nonce))
encryptor = cipher.encryptor()

img1.data = encryptor.update(img1.data) + encryptor.finalize()
img1.save("encrypted-gcm-nonce-reuse-1.bmp")

cipher = Cipher(algorithms.AES256(key), modes.GCM(nonce))
encryptor = cipher.encryptor()

img2.data = encryptor.update(img2.data) + encryptor.finalize()
img2.save("encrypted-gcm-nonce-reuse-2.bmp")

img1.tamper_img(img2, "encrypted-gcm-nonce-reuse-xor.bmp")

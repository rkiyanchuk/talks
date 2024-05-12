import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from utils import read_image, write_image, tamper

# Encrypt with ECB

key = os.urandom(256 // 8)
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


# Encrypt with GCM

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


key = AESGCM.generate_key(bit_length=256)
aes_gcm = AESGCM(key)
nonce = os.urandom(12)
nonce2 = os.urandom(12)

meta, data = read_image('data.bmp')
ciphertext1 = aes_gcm.encrypt(nonce, data, None)
write_image('encrypted-aes-gcm-1.bmp', meta, ciphertext)

meta, data = read_image('evil.bmp')
ciphertext2 = aes_gcm.encrypt(nonce2, data, None)
write_image('encrypted-aes-gcm-2.bmp', meta, ciphertext)

xor = bytearray([ciphertext1[i] ^ ciphertext2[i] for i in range(len(ciphertext1))])
write_image('encrypted-aes-gcm-nonce-reuse.bmp', meta, xor)
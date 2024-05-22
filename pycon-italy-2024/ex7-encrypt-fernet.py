from cryptography.fernet import Fernet
from utils import Image

img = Image("data.bmp")

key = Fernet.generate_key()
f = Fernet(key)
ciphertext = f.encrypt(img.data)

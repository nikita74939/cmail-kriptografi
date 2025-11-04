from Crypto.Cipher import DES3 # type: ignore
from Crypto.Random import get_random_bytes # type: ignore
import hashlib
import base64

def encrypt_3des(data: str, password: str) -> str:
    key = hashlib.sha256(password.encode()).digest()[:24]
    cipher = DES3.new(key, DES3.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(nonce + tag + ciphertext).decode()

def decrypt_3des(encrypted: str, password: str) -> str:
    key = hashlib.sha256(password.encode()).digest()[:24]
    data = base64.b64decode(encrypted)
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = DES3.new(key, DES3.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()
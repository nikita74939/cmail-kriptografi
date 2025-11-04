from tinyec import registry
import secrets

# Gunakan kurva standar (contoh: secp192r1)
curve = registry.get_curve('secp192r1')

# ===== Generate Key Pair =====
def generate_keys():
    private_key = secrets.randbelow(curve.field.n)
    public_key = private_key * curve.g
    return private_key, public_key

# ===== Enkripsi =====
def ecc_encrypt(msg, public_key):
    msg_bytes = msg.encode('utf-8')
    k = secrets.randbelow(curve.field.n)
    c1 = k * curve.g
    c2 = [m_byte + (k * public_key).x for m_byte in msg_bytes]
    return c1, c2

# ===== Dekripsi =====
def ecc_decrypt(c1, c2, private_key):
    shared_point = private_key * c1
    decrypted_bytes = bytes([int(m_byte - shared_point.x) % 256 for m_byte in c2])
    return decrypted_bytes.decode('utf-8', errors='ignore')

# ===== Contoh penggunaan =====
# priv, pub = generate_keys()
# print("Private key:", priv)
# print("Public key:", pub)

# msg = "Pesan rahasia dari Nikita"
# c1, c2 = ecc_encrypt(msg, pub)
# print("Encrypted:", c1, c2)

# plain = ecc_decrypt(c1, c2, priv)
# print("Decrypted:", plain)


# ===== Versi File =====
def ecc_encrypt_file(input_path, output_path, public_key):
    with open(input_path, "rb") as f:
        data = f.read()
    k = secrets.randbelow(curve.field.n)
    c1 = k * curve.g
    c2 = bytes([(b + (k * public_key).x) % 256 for b in data])
    with open(output_path, "wb") as f:
        f.write(c2)
    return c1

def ecc_decrypt_file(input_path, output_path, c1, private_key):
    with open(input_path, "rb") as f:
        data = f.read()
    shared_point = private_key * c1
    decrypted = bytes([(b - shared_point.x) % 256 for b in data])
    with open(output_path, "wb") as f:
        f.write(decrypted)

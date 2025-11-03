import argon2

ph = argon2.PasswordHasher()

def hash_password(pwd):
    return ph.hash(pwd)

def verify_password(hash, pwd):
    try:
        ph.verify(hash, pwd)
        return True
    except:
        return False
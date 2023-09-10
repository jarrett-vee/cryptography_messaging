from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


def generate_keys():
    key = RSA.generate(4096)
    private_key = key.export_key()
    public_key = key.public_key().export_key()
    return public_key, private_key


def encrypt_private_key(private_key, password):
    cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    encrypted_key = cipher.encrypt(password.encode())
    return encrypted_key


def decrypt_private_key(encrypted_key, password):
    cipher = PKCS1_OAEP.new(RSA.import_key(encrypted_key))
    decrypted_key = cipher.decrypt(password.encode())
    return decrypted_key

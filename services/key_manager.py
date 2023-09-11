from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import base64


def generate_keys():
    key = RSA.generate(4096)
    private_key = key.export_key()
    public_key = key.public_key().export_key()
    return public_key, private_key


def encrypt_private_key(private_key, password):
    salt = get_random_bytes(16)
    derived_key = PBKDF2(password, salt, dkLen=32, count=1000000)
    cipher = AES.new(derived_key, AES.MODE_CBC)
    encrypted_key = cipher.encrypt(pad(private_key, AES.block_size))
    encoded_encrypted_key = base64.b64encode(salt + cipher.iv + encrypted_key)
    return encoded_encrypted_key


def decrypt_private_key(encrypted_key, password):
    encrypted_key_binary = base64.b64decode(encrypted_key)
    salt = encrypted_key_binary[:16]
    iv = encrypted_key_binary[16:32]
    derived_key = PBKDF2(password, salt, dkLen=32, count=1000000)
    cipher = AES.new(derived_key, AES.MODE_CBC, iv)
    decrypted_key = unpad(cipher.decrypt(encrypted_key_binary[32:]), AES.block_size)
    return decrypted_key

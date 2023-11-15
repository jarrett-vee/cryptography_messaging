from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad
import base64


def generate_keys():
    key = RSA.generate(4096)
    private_key = key.export_key()
    public_key = key.public_key().export_key()
    return public_key, private_key


def decrypt_private_key(encrypted_key, password):
    encrypted_key_binary = base64.b64decode(encrypted_key)
    salt = encrypted_key_binary[:16]
    iv = encrypted_key_binary[16:32]
    derived_key = PBKDF2(password, salt, dkLen=32, count=1000000)
    cipher = AES.new(derived_key, AES.MODE_CBC, iv)
    decrypted_key = unpad(cipher.decrypt(encrypted_key_binary[32:]), AES.block_size)
    return decrypted_key

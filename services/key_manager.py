from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def generate_keys():
    key = RSA.generate(4096)
    private_key = key.export_key()
    public_key = key.public_key().export_key()
    return public_key, private_key


def encrypt_private_key(private_key, password):
    salt = get_random_bytes(16)  # Generate a random salt
    key = (
        password.encode() + salt
    )  # Combine password with salt to derive the encryption key

    # Ensure the key is exactly 32 bytes (256 bits)
    if len(key) < 32:
        key = key + b"\x00" * (32 - len(key))
    elif len(key) > 32:
        key = key[:32]

    cipher = AES.new(key, AES.MODE_CBC)  # Use the 32-byte key for AES encryption
    encrypted_key = cipher.encrypt(pad(private_key, AES.block_size))
    return salt + encrypted_key  # Prepend salt for decryption


def decrypt_private_key(encrypted_key, password):
    salt = encrypted_key[:16]
    key = password.encode() + salt

    # Ensure the key is exactly 32 bytes (256 bits)
    if len(key) < 32:
        key = key + b"\x00" * (32 - len(key))
    elif len(key) > 32:
        key = key[:32]

    cipher = AES.new(key, AES.MODE_CBC)
    decrypted_key = unpad(cipher.decrypt(encrypted_key[16:]), AES.block_size)
    return decrypted_key

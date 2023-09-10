from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def encrypt_message(message, public_key):
    recipient_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(recipient_key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message


def decrypt_message(encrypted_message, private_key):
    private_key_obj = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(private_key_obj)
    decrypted_message = cipher.decrypt(encrypted_message).decode()
    return decrypted_message

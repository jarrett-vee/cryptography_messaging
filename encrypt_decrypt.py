from dotenv import load_dotenv

load_dotenv("setup.env")
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from models import User
from app import app
from services.key_manager import decrypt_private_key, encrypt_private_key


def encrypt_message(public_key, message):
    key_binary = base64.b64decode(public_key)
    rsa_key = RSA.importKey(key_binary)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_message = cipher.encrypt(message.encode())
    return base64.b64encode(encrypted_message)


def decrypt_message(encrypted_message, private_key):
    rsa_key = RSA.importKey(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message.decode()


def main():
    with app.app_context():
        choice = (
            input("Do you want to encrypt or decrypt a message? (encrypt/decrypt): ")
            .strip()
            .lower()
        )

        if choice == "encrypt":
            recipient_username = input(
                "Enter the username of the person you want to message: "
            ).strip()
            recipient = User.query.filter_by(username=recipient_username).first()
            if not recipient:
                print("User not found!")
                return

            message = input("Enter your message: ").strip()
            encrypted_msg = encrypt_message(recipient.public_key, message)
            print(f"Encrypted Message: {encrypted_msg.decode()}")

        elif choice == "decrypt":
            your_username = input("Enter your username: ").strip()
            you = User.query.filter_by(username=your_username).first()
            if not you:
                print("User not found!")
                return

            password = input("Enter your password: ").strip()
            decrypted_private_key = decrypt_private_key(
                you.encrypted_private_key, password
            )

            # Check if decryption was successful
            if (
                isinstance(decrypted_private_key, bytes)
                and b"-----BEGIN RSA PRIVATE KEY-----" in decrypted_private_key
            ):
                print("Decryption seems to be successful!")
            else:
                print("Decryption didn't result in the expected PEM format.")
                return

            # Print the decrypted private key for visual inspection (ensure you only do this in a safe environment)
            print(decrypted_private_key.decode("utf-8"))

            encrypted_msg = input("Enter the encrypted message: ").strip()
            decrypted_msg = decrypt_message(encrypted_msg, decrypted_private_key)
            print(f"Decrypted Message: {decrypted_msg}")


if __name__ == "__main__":
    main()

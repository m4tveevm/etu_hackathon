from cryptography.fernet import Fernet

# You need to generate and safely store a key
key = Fernet.generate_key()
cipher_suite = Fernet(key)


def encrypt_password(password):
    """Encrypt the password."""
    return cipher_suite.encrypt(password.encode('utf-8')).decode('utf-8')


def decrypt_password(encrypted_password):
    """Decrypt the password."""
    return cipher_suite.decrypt(encrypted_password.encode('utf-8')).decode('utf-8')

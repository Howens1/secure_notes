from cryptography.fernet import Fernet

# Generate a key (store this securely)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_note(note: str) -> str:
    return cipher_suite.encrypt(note.encode()).decode()

def decrypt_note(encrypted_note: str) -> str:
    return cipher_suite.decrypt(encrypted_note.encode()).decode()

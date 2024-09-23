from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os


def generate_key():
    return os.urandom(32)


def encrypt_file(file_path, key):
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, "rb") as file:
        file_data = file.read()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(file_data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(file_path + ".enc", "wb") as file:
        file.write(iv + encrypted_data)

    print(f"The file '{file_path}' has been encrypted and saved as '{file_path}.enc'")


def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, "rb") as file:
        iv = file.read(16)
        encrypted_data = file.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    decrypted_file_path = encrypted_file_path.replace(".enc", "_decrypted")
    with open(decrypted_file_path, "wb") as file:
        file.write(decrypted_data)

    print(
        f"The file '{encrypted_file_path}' has been decrypted and saved as '{decrypted_file_path}'"
    )


key = generate_key()

encrypt_file("folder_encryption.py", key)

decrypt_file("folder_encryption.py.enc", key)

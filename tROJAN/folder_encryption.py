import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


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

    print(f"File '{file_path}' has been encrypted and saved as '{file_path}.enc'")


def encrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            encrypt_file(file_path, key)


if __name__ == "__main__":
    key = generate_key()
    folder_to_encrypt = "your_folder_path"
    encrypt_folder(folder_to_encrypt, key)

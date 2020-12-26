import socket
import os

BASE_DIR = os.path.dirname(__file__)
ss = socket.socket()
file_name = os.path.join(BASE_DIR, 'client_files', '111.png')
ss.connect(('127.0.0.1',8080))

with open(file_name, 'rb+') as f:
    data = f.read()
    ss.send(data)



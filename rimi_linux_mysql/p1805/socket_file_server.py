import socket
import os
BASE_DIR = os.path.dirname(__file__)

file_name = os.path.join(BASE_DIR,'server_files','test1.png')
ss = socket.socket()
ss.bind(('127.0.0.1', 8080))

ss.listen()

conn, address = ss.accept()


with open(file_name,'wb+') as f:
    while 1:
        data = conn.recv(1)
        if not data:
            break
        f.write(data)




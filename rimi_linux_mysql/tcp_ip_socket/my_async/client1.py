import socket

ss_address = ("0.0.0.0",19528)

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ss.connect(ss_address)

while True:
    print(ss.recv(1024).decode('utf8'))


ss.close()


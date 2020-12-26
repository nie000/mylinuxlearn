import socket

port = 19523
ip = "127.0.0.1"

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.connect((ip,port))

while True:
    msg = input('input:')
    ss.send(msg.encode('utf8'))
    print(ss.recv(1024))
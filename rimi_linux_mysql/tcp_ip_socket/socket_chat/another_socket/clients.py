import socket

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.connect(('127.0.0.1',29528))
print('asdfasdf')
while True:
    msg = input('input')
    ss.send(msg.encode('utf8'))
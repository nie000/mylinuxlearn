# --<!--utf8-->
import socket
# 0.0.0.0 = 内网网址
addr = ('0.0.0.0',19527)
ss = socket.socket()
ss.connect(addr)

while 1:
    msg = input('input:')
    ss.send(msg.encode())
    msg = ss.recv(1024)
    print(msg)



ss.send(msg.encode())
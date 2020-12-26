# --<!--utf8-->
import socket
# 0.0.0.0 = 内网网址
addr = ('0.0.0.0',10048)
ss = socket.socket()
ss.connect(addr)

msg = input('input:')



ss.send(msg.encode())
# python select io多路复用测试代码
# 1. 简单的使用select来进行客户端多连接

import select
import socket

# select 把socket放入 select中,然后每当有一个连接过来,把连接conn放入select模型里面去

port = 19869
ip = "127.0.0.1"

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.connect((ip,port))

while True:
    msg = input('input:')
    ss.send(msg.encode('utf8'))
    print(ss.recv(1024))




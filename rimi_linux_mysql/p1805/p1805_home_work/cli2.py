# --<!--utf8-->
import socket
import threading
from confs.settings import port
# 0.0.0.0 = 内网网址
addr = ('127.0.0.1', port)
ss = socket.socket()
ss.connect(addr)
print(ss)
import time


def conn(ss):
    while 1:
        msg = input('input:')
        ss.send(msg.encode())


def recv1(ss):
    while 1:
        msg = ss.recv(1024)
        time.sleep(0.1)
        print(msg.decode())


t1 = threading.Thread(target=conn, args=(ss,))
t2 = threading.Thread(target=recv1, args=(ss,))

t1.start()
t2.start()
t1.join()
t2.join()

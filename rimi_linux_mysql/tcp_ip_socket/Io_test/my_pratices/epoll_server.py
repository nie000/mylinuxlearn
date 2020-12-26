import socket
import select
import queue

addr = ('0.0.0.0',19527)
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(addr)
ss.listen(10)
print('开始监听socket请求')
#设置不阻塞
ss.setblocking(False)
epoll = select



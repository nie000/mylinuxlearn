import socket
import time
addr = ('0.0.0.0',10048)
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(addr)
ss.listen(5)
conn, address = ss.accept()

#开启非阻塞模式
conn.setblocking(False)
num = 0

while 1:
    try:
        tmp_msg = conn.recv(4096)
        print(num)
        break
    except BlockingIOError:
        num += 1
        continue
print(tmp_msg.decode('utf8'))



conn.close()
print('end')




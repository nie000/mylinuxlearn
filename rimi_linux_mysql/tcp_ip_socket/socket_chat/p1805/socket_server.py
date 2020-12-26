# 1. 服务端
# 2. 客户端

import socket
import time
import threading


# print('start')
# ss = socket.socket()
# ss.bind(('127.0.0.1',8002))
# ss.listen()
# print('1------')
# #阻塞
# conn,addr = ss.accept()
# print('2------')
# # msg = conn.recv(1024)
#
# #1. 改成 一直在发送一个消息 并且可以接受消息 并且返回给客户端
# while True:
#     time.sleep(0.1)
#     conn.send(b'rec')
#
# msg = conn.recv(1024)
# conn.send(b'heloo')
# print(msg)

class Server:
    def __init__(self):
        self.addr = ('127.0.0.1', 8008)
        self.ss = socket.socket()

    def deamon_send(self, conn):
        while True:
            time.sleep(5)
            now = time.time()
            conn.send("当前时间:{}".format(str(now)).encode('utf8'))

    def recv(self, conn):
        while True:
            msg = conn.recv(1024)
            conn.send('收到你的消息:{}'.format(msg.decode('utf8')).encode('utf8'))

    def start_server(self):
        self.ss.bind(self.addr)
        self.ss.listen()
        print('start server')

    def get_conn(self):
        conn, addr = self.ss.accept()
        t1 = threading.Thread(target=self.deamon_send, args=(conn,))
        t2 = threading.Thread(target=self.recv, args=(conn,))
        print('listen a conn')
        t1.start()
        t2.start()

        t1.join()
        t2.join()

    def start(self):
        self.start_server()

        self.get_conn()


if __name__ == "__main__":
    s = Server()
    s.start()

# 1. 只能一个客户链接进来
# 2. 只能发送或者受到消息之后再发送

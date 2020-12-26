"""
1. 多人聊天室
2. 服务端可以接受多个客户端的链接
3. 客户端发送的消息可以通过服务端广播给所有人
"""
import socket
from concurrent.futures import ThreadPoolExecutor


class Server:

    def __init__(self, bind_ip='0.0.0.0', port=21805, listen_num=25):
        """
        1. 初始化socket服务

        """
        # 初始化tcp链接
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定地址
        self.bind_address = (bind_ip, port)
        self.server.bind(self.bind_address)
        # 默认放25个客户端进来
        self.server.listen(listen_num)
        # 所有的客户端链接都放在这里面
        self.conns = list()
        self.pools = ThreadPoolExecutor(listen_num + 5)
        # 字典 对应 conn对应的线程池
        self.conn2pool = dict()

    def accept(self):
        """
        接受客户端的链接
        :return:
        """
        conn, addr = self.server.accept()
        self.conns.append(conn)
        return conn, addr

    def multiple_accept(self):
        """
        接受多个客户端链接
        :return:
        """
        while 1:
            conn, addr = self.accept()
            # 让recv_msg 不阻塞 每个conn(链接都有一个独立的线程去收消息)
            pool = self.pools.submit(self.recv_msg, conn, addr)
            print(addr)
            self.conn2pool.update({conn: pool})

    def recv_msg(self, conn, addr):
        """
        1. 一个客户端接受消息
        :param conn:
        :return:
        """
        while 1:
            msg = conn.recv(1024)
            if (not msg) or len(msg) == 0:
                """
                当消息为空或者没有消息还发送过来的时候,断开链接
                """
                self.break_conn(conn, addr)
            self.broadcast_msg(msg, addr)

    def broadcast_msg(self, msg, addr):
        """
        广播消息
        :return:
        """
        for conn in self.conns:
            self.send_msg(conn, msg, addr)

    def send_msg(self, conn, msg, addr):
        """
        发送消息
        :param msg:
        :return:
        """
        msg = self.handle_msg(msg, addr)
        try:
            #mtu  tcp切包
            conn.send(self.str2bytes(msg))
        except Exception:
            self.break_conn(conn, addr)

    def bytes2str(self, msg):
        """
        二进制转字符串
        :param msg:
        :return:
        """
        try:
            return msg.decode()
        except Exception:
            return msg

    def str2bytes(self, msg):
        """
        字符串转二进制
        :param msg:
        :return:
        """
        try:
            return msg.encode()
        except Exception:
            return msg

    def handle_msg(self, msg, addr):
        msg_str = "用户---{}--说:{}".format(addr, self.bytes2str(msg))
        return msg_str

    def break_conn(self, conn, addr):
        conn.close()
        self.conns.remove(conn)
        # 回收线程
        pool = self.conn2pool[conn]
        print('{}断开链接'.format(conn))
        pool.shutdown()
        msg = '我已经断开链接'.encode()
        self.broadcast_msg(msg, addr)

    def start(self):
        print('server start')
        self.multiple_accept()
        print('server end')


if __name__ == '__main__':
    s = Server()
    s.start()

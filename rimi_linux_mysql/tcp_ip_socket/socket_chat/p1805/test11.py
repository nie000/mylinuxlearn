# 1. 服务端
# 2. 客户端


import socket
from concurrent.futures import ThreadPoolExecutor
from queue import Queue


class Server:
    """
    1. 接收多人的链接进来
    2. 收到一个人的消息之后,把消息广播给所有人
    """

    def __init__(self, bind_ip='0.0.0.0', port=31805):
        """
        初始化函数
        :param bind_ip:
        :param port:
        """
        # 初始化绑定ip
        self.bind_address = (bind_ip, port)
        # 初始化的tcp链接
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss.bind(self.bind_address)
        self.ss.listen(30)
        self.pools = ThreadPoolExecutor(35)
        """
        广播
        """
        self.msg_queue = Queue()
        """
        ip榜单
        """
        self.ip_list = []
        self.black_list = []
        # 所有人链接进来的表
        self.conns = []
        # 链接对应的线程池
        self.pool2conn = dict()

    def start(self):
        """
        接收链接
        :return:
        """
        self.pools.submit(self.send_msg)
        while True:
            conn, addr = self.ss.accept()
            if self.is_black(addr):
                continue
            tmp_task = self.pools.submit(self.recv_msg, conn, addr)
            self.conns.append(conn)
            #加入链接对应的线程池,链接端口好关闭线程
            self.pool2conn.update({conn:tmp_task})

    def recv_msg(self, conn, addr):

        while True:
            msg = conn.recv(1024)
            if (not msg) or (len(msg) == 0):
                self.remove_conn(conn,addr)
            self.msg_queue.put((msg, addr))
            print('收到ip为{}的消息{}'.format(addr, msg.decode()))

    def send_msg(self):
        while True:
            msg, addr = self.msg_queue.get()
            ip, port = addr
            for conn in self.conns:
                try:
                    conn.send("ip为{},port为{},说:{}".format(ip, port, msg.decode()).encode())
                except Exception:
                    self.remove_conn(conn,addr)

    def remove_conn(self,conn,addr):
        conn.close()
        self.conns.remove(conn)
        msg = '我已经退出聊天'.encode()
        self.msg_queue.put((msg, addr))
        #关闭线程池中的线程
        self.pool2conn[conn].close()

    def is_black(self, addr):
        """
        判断黑名单用户
        :return:
        """
        ip, port = addr
        if ip in self.black_list:
            return True
        else:
            return False


if __name__ == "__main__":
    ss = Server()
    ss.start()

import asyncore
import socket
import asynchat


class ChatServer(asyncore.dispatcher):

    # 启动服务器
    def __init__(self, list_num=20, host="0.0.0.0", post=19529):
        asyncore.dispatcher.__init__(self)
        # f\使用socket协议
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        # tcp端口连接会有一个time_wait状态，使他能够立刻重启,不去timewait
        self.set_reuse_addr()
        # 绑定端口
        self.bind((host, post))
        self.listen(list_num)
        self.clients = []
        # 已经启动
        print('***server start***')

    def handle_accept(self):
        conn, addr = self.accept()
        c_ip, c_port = addr
        print('client {} enter'.format(c_ip))
        ChatSession(self, conn, addr, c_port, self.clients)

    def handle_close(self):
        """
        Implied by a read event with no data available
        :return:
        """
        print('服务器已经关闭')
        # self.close()
        pass

    def handle_error(self):
        print('服务器已经异常')
        pass


# 聊天程序
class ChatSession(asynchat.async_chat):
    def __init__(self, server, conn, addr, port, clients):
        asynchat.async_chat.__init__(self, conn)
        # 把自己的连接加入到连接表里面去,向所有人广播
        if self not in clients:
            clients.append(self)
        self.server = server
        self.addr = addr
        self.port = port
        # 表示退出的动作,这里客户端敲击out就可以退出
        self.set_terminator(b'out')
        self.clients = clients
        # 给用户起一个名字
        self.user = '用户' + str(self.addr) + str(self.port)

    def collect_incoming_data(self, data):
        # 如果收到了连接
        print(data)
        if len(data) != 0:
            # 回传消息
            self.push(data)


s = ChatServer()
asyncore.loop()

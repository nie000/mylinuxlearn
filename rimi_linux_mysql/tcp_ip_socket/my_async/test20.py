import asyncore
import asynchat
import socket


class ChatServer(asyncore.dispatcher):
    def __init__(self, list_num=20, host="0.0.0.0", post=19528):
        asyncore.dispatcher.__init__(self)
        # f\使用socket协议
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        # tcp端口连接会有一个time_wait状态，使他能够立刻重启,不去timewait
        self.set_reuse_addr()
        # 绑定端口
        self.bind((host, post))
        self.listen(list_num)
        self.clients = list()
        # 已经启动
        print('***server start***')

    # 帮你监听有链接进来|链接准备好了
    def handle_accept(self):
        conn, addr = self.accept()
        c_ip, c_port = addr
        print('client {} enter'.format(c_ip))
        ChatSession(self, conn, c_ip, c_port)

    def handle_close(self):
        print('服务器已经关闭')
        self.close()

    def handle_error(self):
        print('服务器已经异常')
        self.close()


# conn 每一个链接  每一个会话
class ChatSession(asynchat.async_chat):
    def __init__(self, server, conn, addr, port):
        # conn表示链接
        asynchat.async_chat.__init__(self, conn)
        # 把自己的连接加入到连接表里面去,向所有人广播
        self.server = server
        self.addr = addr
        self.port = port
        # 表示退出的动作,这里客户端敲击out就可以退出
        self.set_terminator(b'out')
        self.server.clients.append(self)
        self.user_name = "用户:{}-{}".format(self.addr,self.port)
        self.comming()

    def comming(self):
        data = "{} 进入聊天室".format(self.user_name)
        self.broad(data)

    def encode_msg(self, msg):
        # 如果不是二进制 转化成二进制
        if not isinstance(msg, bytes):
            msg = msg.encode('utf8')
        return msg

    def decode_msg(self, msg):
        # 如果不是unicode 换成undicode
        if isinstance(msg, bytes):
            msg = msg.decode('utf8')
        return msg

    def collect_incoming_data(self, data):
        # 如果收到了连接
        print(data)
        if len(data) != 0:
            # 回传消息 push = conn.send()
            self.user_say(data)

    def user_say(self,data):
        res = "{}说{}".format(self.user_name,data.decode('utf8'))
        self.broad(res)

    def broad(self,data):
        for i in self.server.clients:
            try:
                i.push(self.encode_msg(data))
            except Exception:
                self.remove_clients()

    def found_terminator(self):
        print('accept close')
        # xx客户端关闭
        self.close_when_done()
        self.remove_clients()

    def user_out(self):
        data = "{} 离开了聊天室".format(self.user_name)
        for i in self.server.clients:
            try:
                i.push(self.encode_msg(data))
            except Exception:
                pass

    def remove_clients(self):
        try:
            self.server.clients.remove(self)
        except Exception:
            pass
        finally:
            self.user_out()




s = ChatServer()
asyncore.loop()

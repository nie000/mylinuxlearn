# async聊天室制作

1. asyncore封装了原生协程的socket接口,直接包含了接受连接如何处理,连接关闭如何处理,连接出错如何处理等的类
2. asynchat封装了socket conn的接口,它用于处理已经建立好的链接,无需事件循环,只需要调用他的接口即可

服务器代码

```
import asyncore
import asynchat
import socket


# asyncore.dispatcher服务器类,主要用于管理tcp的初始化,连接,关闭关闭连接等
class ChatServer(asyncore.dispatcher):

    def __init__(self,list_num=20,host="0.0.0.0",post=19528):
        asyncore.dispatcher.__init__(self)
        #f\使用socket协议
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        # tcp端口连接会有一个time_wait状态，使他能够立刻重启,不去timewait
        self.set_reuse_addr()
        # 绑定端口
        self.bind((host, post))
        self.listen(list_num)
        self.clients = []
        #已经启动
        print('***server start***')

    def handle_accept(self):
        conn, addr = self.accept()
        c_ip,c_port = addr
        print('client {} enter'.format(c_ip))
        ChatSession(self, conn, c_ip,c_port,self.clients)

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


class ChatSession(asynchat.async_chat):
    def __init__(self, server,conn,addr,port,clients):
        asynchat.async_chat.__init__(self, conn)
        #把自己的连接加入到连接表里面去,向所有人广播
        if self not in clients:
            clients.append(self)
        self.server = server
        self.addr = addr
        self.port = port
        #表示退出的动作,这里客户端敲击out就可以退出
        self.set_terminator(b'out')
        self.clients = clients
        #给用户起一个名字
        self.user = '用户'+str(self.addr)+str(self.port)

    #给字符串加码,以便以传输
    def encode_msg(self,msg):
        #如果不是二进制 转化成二进制
        if not isinstance(msg,bytes):
            msg = msg.encode('utf8')
        return msg

    def decode_msg(self,msg):
        #如果不是unicode 换成undicode
        if isinstance(msg,bytes):
            msg = msg.decode('utf8')
        return msg

    def collect_incoming_data(self, data):
        #如果收到了连接
        if len(data) != 0:
            #回传消息
            self.push(data)
            #广播
            self.broadcasting(data)



    def broadcasting(self,msg):
        """
        广播消息给其他客户端
        :param msg:
        :return:
        """

        user_str = self.decode_msg(self.user)

        msg_str= self.decode_msg(msg)

        total_str = "{} 说:{}".format(user_str,msg_str)

        total_str = self.encode_msg(total_str)


        for client in self.clients:
            if client is not self:
                client.push(total_str)


    def found_terminator(self):
        print('accept close')
        #xx客户端关闭
        self.close_when_done()
        self.clients.remove(self)
        user_str = self.decode_msg(self.user)
        total_str = "{}退出聊天".format(user_str)
        total_str = self.encode_msg(total_str)
        self.broadcasting(total_str)


s = ChatServer()
asyncore.loop()


```

客户端代码

```
# python select io多路复用测试代码
# 1. 简单的使用select来进行客户端多连接

import select
import socket
import threading

# select 把socket放入 select中,然后每当有一个连接过来,把连接conn放入select模型里面去

port = 19869
ip = "127.0.0.1"


def input_line(ss):
    while True:
        msg = input("input:")
        ss.send(msg.encode('utf8'))

def read_line(ss):
    while True:
        msg = ss.recv(1024)
        print('revice from',msg)

def loop():
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.connect((ip, port))
    t1 = threading.Thread(target=input_line,args=(ss,))
    t2 = threading.Thread(target=read_line, args=(ss,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    loop()



```
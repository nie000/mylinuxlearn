import socket
import select
from confs.settings import port


class Server:
    def __init__(self, ip='0.0.0.0', port=port, listen_num=128):
        self.sel = select
        # 初始化监听列表
        self.read_list = []
        self.write_list = []
        self.error_list = []
        self.ip = ip
        self.port = port
        self.listen_num = listen_num
        self.ss = self.start_socket(self.ip, self.port, self.listen_num)
        self.read_list.append(self.ss)
        # 定义房号
        self.rooms = ('1804', '1805', '1806')
        # 定义房间里面的有哪些人
        # {'1805':['','',''],}
        self.rooms2conns = dict()
        for i in self.rooms:
            self.rooms2conns[i] = list()
        # 定义一个没有房间的人的list
        self.new_conns = list()
        # 定义一个消息列表
        # {conn1:['你好','我,秦始皇'],conn2:['滚粗']}
        self.conn2msgs = dict()
        # 存一个连接对应的room_number表
        self.conn2num = dict()

    def error_handler(self, i):

        try:
            self.write_list.remove(i)
        except Exception:
            pass
        try:
            self.read_list.remove(i)
        except Exception:
            pass
        try:
            self.new_conns.remove(i)
        except Exception:
            pass
        try:
            del (self.conn2num[i])
        except Exception:
            pass
        try:
            del (self.conn2msgs[i])
        except Exception:
            pass
        for room_num in self.rooms2conns:
            if i in self.rooms2conns[room_num]:
                try:
                    self.rooms2conns[room_num].remove(i)
                except Exception:
                    pass

    def run(self):
        # 启动socket
        while 1:
            read, write, error = select.select(self.read_list, self.write_list, self.error_list)
            print('=============')
            if read:
                for i in read:
                    if i is self.ss:
                        # 接收新连接
                        try:
                            conn, addr = i.accept()
                        except Exception:
                            break
                        print('新连接进入{}'.format(conn))
                        # 把链接加入到select进行管理
                        self.read_list.append(conn)
                        # 把新进来的人加入到没有房间的人的列表里面
                        if conn not in self.new_conns:
                            self.new_conns.append(conn)
                            # 给每一个新人初始化好消息记录表
                            self.conn2msgs[conn] = list()
                        # 新进来的人要提示他输入房间号
                        self.write_list.append(conn)
                        print('有一个新连接进来')
                    else:
                        # 判断这个连接是否还没有进房间
                        try:
                            msg = i.recv(1024)
                        except Exception:
                            self.error_handler(i)
                            break
                        msg = msg.decode()
                        print(msg)
                        if i in self.new_conns:
                            if msg in self.rooms:
                                room_num = msg
                                # 如果请求进入房间号的命令无误,让他加入房间,把他从新人中去除
                                self.new_conns.remove(i)
                                self.rooms2conns[room_num].append(i)
                                # 发送欢迎消息,欢迎xxx进入xx房间
                                # self.write_list.append(i)
                                for conn in self.rooms2conns[room_num]:
                                    self.write_list.append(conn)
                                    self.conn2msgs[conn].append(
                                        '欢迎新用户{}进入房间{},当前房间人数为{}'.format(i, room_num, len(self.rooms2conns[room_num])))
                                # 选择好房间之后 给conn一个房间号
                                self.conn2num[i] = room_num
                            else:
                                self.write_list.append(i)
                        # 正常聊天了
                        else:
                            room_num = self.conn2num[i]
                            for conn in self.rooms2conns[room_num]:
                                self.write_list.append(conn)
                                self.conn2msgs[conn].append('{}用户说:{}'.format(i, msg))

            if write:
                for i in write:
                    print('有一个写事件:{}'.format(i))
                    # 判断是否是新用户,如果是新用户(没有进入房间的,提示他进入房间)
                    if i in self.new_conns:
                        try:
                            print('新用户进来')
                            i.send('请输入下面几个房间号{}之一'.format(self.rooms).encode())
                        except Exception:
                            self.error_handler(i)
                            break
                        self.write_list.remove(i)
                        break
                    else:
                        try:
                            # 发送信息
                            msg = self.conn2msgs[i].pop()
                        except:
                            msg = None
                        if msg:
                            try:
                                i.send(msg.encode())
                            except Exception:
                                self.error_handler(i)
                                break
                        self.write_list.remove(i)

    def start_socket(self, ip, port, listen_num):
        # 启动tcp链接
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定端口
        ss.bind((ip, port))
        ss.listen(listen_num)

        return ss


if __name__ == "__main__":
    s = Server()
    s.run()

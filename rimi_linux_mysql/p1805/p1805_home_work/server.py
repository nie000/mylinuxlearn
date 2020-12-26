import select
import socket
from confs.settings import port

class Server:

    def __init__(self, ip='127.0.0.1', port=port, listen_num=20):
        # 新建监听事件
        self.read_list = []
        self.write_list = []
        self.error_list = []
        # 定义事件模型
        # 定义房间号
        self.rooms = ['1804', '1805', '1806']
        self.ip = ip
        self.port = port
        self.listen_num = listen_num
        # 记录用户conn链接的表
        self.conn_dict = dict()
        # 记录conn属于的房间表
        self.conn_room = dict()
        # 记录新用户的表
        self.new_user = []
        # 记录用户属于哪个房间
        self.room_users = dict()
        # 预先生成好房间列表
        for room in self.rooms:
            self.room_users[room] = list()
        # 用户要发送信息消息的表
        self.user_msgs = dict()
        # 房间要发送的消息表
        self.room_msgs = dict()
        for room in self.rooms:
            self.room_msgs[room] = list()

    def socket_server(self, ip, port, listen_num):
        """
        启动socket server
        :param ip:
        :param port:
        :return:
        """
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.bind((ip, port))
        ss.listen(listen_num)
        return ss

    def start_server(self):
        """
        启动服务,并且把服务加入给read list监听
        :return:
        """
        # 启动socket server
        self.ss = self.socket_server(self.ip, self.port, self.listen_num)
        print('server启动完毕')
        self.insert_read(self.ss)
        while 1:
            read, write, error = select.select(self.read_list, self.write_list, self.error_list)
            if read:
                for s in read:
                    if s is self.ss:
                        # 接收链接进来
                        try:
                            conn, addr = s.accept()
                        except Exception:
                            break
                        # 将接收进来的链接加入到一个表中
                        if conn not in self.conn_dict.keys():
                            self.conn_dict[conn] = addr
                        # 向客户端发送消息,不过第一个发送的消息应该是询问加入哪个房间
                        if conn not in self.write_list:
                            self.write_list.append(conn)
                        # 新用户进入逻辑
                        self.new_conn(conn)
                    else:
                        """
                        如果是链接进来那就是收到消息
                        """
                        try:
                            msg = s.recv(1024)
                        except Exception:
                            break
                        msg = msg.decode('utf8')
                        print('用户{}的消息{}'.format(s,msg))
                        # 加入房间
                        if msg in self.rooms:
                            room_num = msg
                            # 如果不是新用户才能加入房间
                            if s in self.new_user:
                                self.room_users[room_num].append(s)
                                self.new_user.remove(s)
                                self.conn_room[s] = room_num
                                self.user_msgs[s] = list()
                                msg = '欢迎{}用户加入房间'.format(s)
                                print('用户{}愿意加入房间{}'.format(s,room_num))
                        try:
                            for user in self.room_users[self.conn_room[s]]:
                                print('目前房间{} 有{}个用户'.format(self.conn_room[s],len(self.room_users[self.conn_room[s]])))
                                #print('对用户{}加入广播消息{}'.format(user,msg))
                                self.user_msgs[user].append(msg)
                                if user not in self.write_list:
                                    self.write_list.append(user)

                        except Exception as e:
                            print('1111111111--->{}'.format(e))
                            pass
                        # 把链接加入到发送队列里面取
                        if s not in self.write_list:
                            self.write_list.append(s)
                            print(self.write_list)

            if write:
                for s in write:
                    print('writable {}'.format(s))
                    # 判断是否是新用户,询问加入哪个房间
                    if s in self.new_user:
                        #print('新用户{}'.format(s))
                        try:
                            s.send("请先加入房间:{}".format(self.rooms).encode('utf8'))
                        except Exception:
                            pass
                    else:
                        # 不是新用户 发送消息
                        try:
                            msg = self.user_msgs[s].pop()
                            s.send(msg.encode())
                            print('发送消息{}'.format(msg))
                        except Exception as e:
                            print("error {}".format(e))
                            pass
                    self.write_list.remove(s)
            if error:
                pass

    def insert_read(self, s):
        """
        向read list加入监听程序
        :param s:
        :return:
        """
        self.read_list.append(s)

    def new_conn(self, s):
        """
        新进来的链接的逻辑

        新进来的用户首先要打招呼,询问进入哪个房间
        :param s:
        :return:
        """
        self.new_user.append(s)
        print('加入新用户{}'.format(s))
        self.user_msgs[s] = list()
        #加入到监听队列   
        self.read_list.append(s)



ser = Server()
ser.start_server()